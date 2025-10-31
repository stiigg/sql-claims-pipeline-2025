
from pathlib import Path

import duckdb
import yaml


def build(conn: duckdb.DuckDBPyConnection, path: str = "config/metrics_codebook.yaml") -> None:
    cfg = yaml.safe_load(Path(path).read_text())
    dx_rows, px_rows = [], []
    for metric, spec in cfg["metrics"].items():
        for pat in spec.get("icd10_include", []):
            dx_rows.append((metric, pat))
        for code in spec.get("cpt_include", []):
            px_rows.append((metric, str(code)))
    conn.execute("CREATE OR REPLACE TABLE codebook_dx(metric VARCHAR, pattern VARCHAR)")
    if dx_rows:
        conn.executemany("INSERT INTO codebook_dx VALUES (?, ?)", dx_rows)
    conn.execute("CREATE OR REPLACE TABLE codebook_px(metric VARCHAR, code VARCHAR)")
    if px_rows:
        conn.executemany("INSERT INTO codebook_px VALUES (?, ?)", px_rows)
