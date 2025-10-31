"""Build a data dictionary from DuckDB staged tables."""
from __future__ import annotations

"""Build a data dictionary from DuckDB staged tables."""

import csv
from pathlib import Path

import duckdb

DB_PATH = Path("secure_work/claims.duckdb")
ARTIFACT = Path("artifacts/data_dictionary.csv")


def list_tables(con: duckdb.DuckDBPyConnection) -> list[str]:
    results = con.execute(
        "SELECT table_name FROM information_schema.tables "
        "WHERE table_schema='main' ORDER BY table_name"
    ).fetchall()
    return [row[0] for row in results]


def describe_table(con: duckdb.DuckDBPyConnection, table: str) -> list[dict[str, str]]:
    rows = []
    columns = con.execute(f"PRAGMA table_info('{table}')").fetchall()
    for cid, name, dtype, not_null, default, _ in columns:
        rows.append(
            {
                "table": table,
                "column": name,
                "type": dtype,
                "nullable": "no" if not_null else "yes",
                "default": default or "",
            }
        )
    return rows


def main() -> None:
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, str]] = []

    if not DB_PATH.exists():
        fieldnames = ["table", "column", "type", "nullable", "default"]
        with ARTIFACT.open("w", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=fieldnames)
            writer.writeheader()
        return

    con = duckdb.connect(str(DB_PATH))
    for table in list_tables(con):
        rows.extend(describe_table(con, table))

    fieldnames = ["table", "column", "type", "nullable", "default"]
    with ARTIFACT.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
