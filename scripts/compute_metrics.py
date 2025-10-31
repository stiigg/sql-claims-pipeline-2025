"""Compute engagement metrics using DuckDB outputs."""
from __future__ import annotations

import csv
from pathlib import Path

import duckdb
import yaml

DB_PATH = Path("secure_work/claims.duckdb")
CFG_METRICS = Path("config/metrics.yml")
ART_DIR = Path("artifacts")
SUMMARY = ART_DIR / "metrics_summary.csv"
METRIC_DIR = ART_DIR / "metrics"

RATE_SQL = Path("sql/metrics/rate_per_1000.sql")
SCREEN_SQL = Path("sql/metrics/screening_rate.sql")
UTIL_SQL = Path("sql/metrics/utilization_rates.sql")
READMIT_SQL = Path("sql/metrics/readmission_rate.sql")


def render_sql(path: Path, params: dict[str, str]) -> str:
    sql = path.read_text()
    for key, value in params.items():
        sql = sql.replace(f":{key}", value)
    return sql


def write_metric_csv(path: Path, row: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)


def main() -> None:
    ART_DIR.mkdir(exist_ok=True)
    METRIC_DIR.mkdir(parents=True, exist_ok=True)

    if not DB_PATH.exists() or not CFG_METRICS.exists():
        with SUMMARY.open("w", newline="") as fh:
            writer = csv.writer(fh)
            writer.writerow(["metric_id", "metric", "measure", "value"])
        return

    cfg = yaml.safe_load(CFG_METRICS.read_text())
    window = cfg.get("global", {})
    start = window.get("measurement_start")
    end = window.get("measurement_end")

    conn = duckdb.connect(str(DB_PATH))
    util_cache = None
    summary_rows: list[dict[str, object]] = []

    for metric_id, spec in cfg.get("metrics", {}).items():
        metric_type = spec.get("type")
        metric_name = spec.get("metric_name", metric_id)
        params = {
            "start_date": f"'{start}'",
            "end_date": f"'{end}'",
        }

        if metric_type == "prevalence_per_1000":
            params |= {"metric_name": f"'{metric_name}'"}
            sql = render_sql(RATE_SQL, params)
            row = conn.execute(sql).fetchdf().iloc[0].to_dict()
        elif metric_type == "screening_pct":
            cohort = spec.get("cohort", {})
            params |= {
                "screening_metric": f"'{metric_name}'",
                "min_age": str(cohort.get("min_age", 0)),
                "max_age": str(cohort.get("max_age", 120)),
                "sex_filter": f"'{cohort.get('sex', 'ANY')}'",
                "lookback_days": str(cohort.get("lookback_days", 365)),
            }
            sql = render_sql(SCREEN_SQL, params)
            row = conn.execute(sql).fetchdf().iloc[0].to_dict()
        elif metric_type == "utilization_per_1000":
            if util_cache is None:
                util_cache = conn.execute(render_sql(UTIL_SQL, params)).fetchdf()
            match = util_cache[util_cache["metric"] == metric_name]
            if match.empty:
                row = {"metric": metric_name, "rate_per_1000": None}
            else:
                row = match.iloc[0].to_dict()
        elif metric_type == "readmission_rate":
            sql = render_sql(READMIT_SQL, params)
            row = conn.execute(sql).fetchdf().iloc[0].to_dict()
        else:
            row = {"metric": metric_name}

        row["metric_id"] = metric_id
        summary_rows.append(row)
        write_metric_csv(METRIC_DIR / f"{metric_id}.csv", row)

    # Flatten summary rows for combined CSV
    fieldnames: set[str] = set()
    for row in summary_rows:
        fieldnames.update(row.keys())
    field_list = sorted(fieldnames)
    with SUMMARY.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=field_list)
        writer.writeheader()
        writer.writerows(summary_rows)


if __name__ == "__main__":
    main()
