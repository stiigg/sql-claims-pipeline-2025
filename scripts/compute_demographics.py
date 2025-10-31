"""Export demographics from DuckDB cohort tables."""
from __future__ import annotations

import csv
from pathlib import Path

import duckdb

DB_PATH = Path("secure_work/claims.duckdb")
DEMOGRAPHICS_SQL = Path("sql/metrics/demographics.sql")
ARTIFACT = Path("artifacts/demographics.csv")


def render_sql(path: Path) -> str:
    return path.read_text()


def main() -> None:
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    if not DB_PATH.exists():
        with ARTIFACT.open("w", newline="") as fh:
            writer = csv.writer(fh)
            writer.writerow(["avg_age", "pct_female", "pct_male", "total_members"])
        return

    conn = duckdb.connect(str(DB_PATH))
    row = conn.execute(render_sql(DEMOGRAPHICS_SQL)).fetchdf().iloc[0].to_dict()
    with ARTIFACT.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(row.keys()))
        writer.writeheader()
        writer.writerow(row)


if __name__ == "__main__":
    main()
