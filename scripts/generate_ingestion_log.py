"""Generate ingestion metadata for raw inputs."""
from __future__ import annotations

import csv
import time
from pathlib import Path

import duckdb

RAW_DIR = Path("secure_input/raw")
ARTIFACT = Path("artifacts/ingestion_log.csv")
DATE_CANDIDATES = ("svc_date", "service_date", "date", "claim_date")


def detect_dates(con: duckdb.DuckDBPyConnection, table: str) -> tuple[str | None, str | None]:
    for column in DATE_CANDIDATES:
        try:
            result = con.execute(
                f"SELECT MIN({column}) AS start, MAX({column}) AS end FROM {table}"
            ).fetchone()
        except duckdb.Error:
            continue
        if result:
            return tuple(result)
    return (None, None)


def load_table(con: duckdb.DuckDBPyConnection, path: Path) -> str:
    name = path.stem.replace("-", "_")
    if path.suffix.lower() == ".parquet":
        con.execute(f"CREATE OR REPLACE TABLE {name} AS SELECT * FROM read_parquet('{path}')")
    else:
        con.execute(f"CREATE OR REPLACE TABLE {name} AS SELECT * FROM read_csv_auto('{path}')")
    return name


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, object]] = []
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    con = duckdb.connect()

    for path in sorted(RAW_DIR.glob("*")):
        if not path.is_file():
            continue
        table = load_table(con, path)
        count = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        first_date, last_date = detect_dates(con, table)
        rows.append(
            {
                "filename": path.name,
                "table": table,
                "rows": count,
                "bytes": path.stat().st_size,
                "first_date": first_date,
                "last_date": last_date,
                "loaded_at": timestamp,
            }
        )

    fieldnames = [
        "filename",
        "table",
        "rows",
        "bytes",
        "first_date",
        "last_date",
        "loaded_at",
    ]
    with ARTIFACT.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
