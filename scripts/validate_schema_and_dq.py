"""Run data-quality rules and export scorecards."""
from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable

import duckdb
import yaml

DB_PATH = Path("secure_work/claims.duckdb")
RULES_CFG = Path("config/dq_rules.yaml")
SCORECARD = Path("artifacts/dq_scorecard.csv")
COVERAGE = Path("artifacts/coverage_summary.csv")
VALIDATION = Path("artifacts/schema_validation.json")
FAILURE_DIR = Path("artifacts")
DATE_COLUMNS = ("svc_date", "service_date", "fill_date", "claim_date", "start_date", "end_date")
TABLES_OF_INTEREST = ("eligibility_staged", "medical_staged", "rx_staged", "cohort_base")


def load_rules() -> list[dict[str, str]]:
    if not RULES_CFG.exists():
        return []
    cfg = yaml.safe_load(RULES_CFG.read_text())
    return cfg.get("rules", [])


def table_counts(con: duckdb.DuckDBPyConnection, tables: Iterable[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for table in tables:
        try:
            counts[table] = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        except duckdb.Error:
            counts[table] = 0
    return counts


def find_date_bounds(con: duckdb.DuckDBPyConnection, table: str) -> tuple[str | None, str | None]:
    for column in DATE_COLUMNS:
        try:
            bounds = con.execute(
                f"SELECT MIN({column}) AS start, MAX({column}) AS end FROM {table}"
            ).fetchone()
        except duckdb.Error:
            continue
        if bounds and any(bounds):
            return tuple(bounds)
    return (None, None)


def safe_rule_name(name: str) -> str:
    return name.replace("/", "_").replace(" ", "_")


def main() -> None:
    SCORECARD.parent.mkdir(parents=True, exist_ok=True)
    COVERAGE.parent.mkdir(parents=True, exist_ok=True)
    status = {"rules_evaluated": 0, "errors": []}

    if not DB_PATH.exists():
        for artifact in (SCORECARD, COVERAGE):
            with artifact.open("w", newline="") as fh:
                writer = csv.writer(fh)
                if artifact is SCORECARD:
                    writer.writerow(["rule", "fails", "pass_rate", "description"])
                else:
                    writer.writerow(["table", "rows", "first_date", "last_date"])
        VALIDATION.write_text(json.dumps(status, indent=2))
        return

    con = duckdb.connect(str(DB_PATH))
    counts = table_counts(con, TABLES_OF_INTEREST)

    rows = []
    rules = load_rules()
    for rule in rules:
        name = rule["name"]
        sql = rule["sql"]
        description = rule.get("description", "")
        try:
            fails = con.execute(f"SELECT COUNT(*) FROM ({sql})").fetchone()[0]
        except duckdb.Error as exc:  # capture query error
            status["errors"].append({"rule": name, "error": str(exc)})
            fails = None
        denominator = counts.get(name.split(".")[0] + "_staged", 0)
        pass_rate = None
        if isinstance(fails, int):
            status["rules_evaluated"] += 1
            if denominator:
                pass_rate = 1 - (fails / denominator)
            sample_query = f"SELECT * FROM ({sql}) LIMIT 100"
            try:
                df = con.execute(sample_query).fetchdf()
            except duckdb.Error:
                df = None
            if df is not None and fails:
                sample_path = FAILURE_DIR / f"dq_failures_{safe_rule_name(name)}.csv"
                df.to_csv(sample_path, index=False)
        rows.append({
            "rule": name,
            "fails": fails if fails is not None else "error",
            "pass_rate": pass_rate,
            "description": description,
        })

    with SCORECARD.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["rule", "fails", "pass_rate", "description"])
        writer.writeheader()
        writer.writerows(rows)

    coverage_rows = []
    for table in TABLES_OF_INTEREST:
        if counts.get(table, 0) == 0:
            continue
        first_date, last_date = find_date_bounds(con, table)
        coverage_rows.append(
            {
                "table": table,
                "rows": counts[table],
                "first_date": first_date,
                "last_date": last_date,
            }
        )

    with COVERAGE.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["table", "rows", "first_date", "last_date"])
        writer.writeheader()
        writer.writerows(coverage_rows)

    VALIDATION.write_text(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
