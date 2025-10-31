
import os
import json
import time
from pathlib import Path

import duckdb
import yaml

from tools.template_manifest import compute_manifest
from tools.codebook_build_tables import build as build_codebook

CFG_PIPELINE = Path('config/pipeline.yaml')
CFG_CONN = Path('config/connections.example.yaml')
ART_DIR = Path('artifacts')
WORK_DIR = Path('secure_work')

ART_DIR.mkdir(exist_ok=True)
WORK_DIR.mkdir(exist_ok=True)


def run_sql(conn, file_path, params=None):
    sql = Path(file_path).read_text()
    for k, v in (params or {}).items():
        sql = sql.replace(f":{k}", v)
    conn.execute(sql)


def main():
    start = os.environ.get('START')
    end = os.environ.get('END')
    if not (start and end):
        raise SystemExit("Set START and END env vars (YYYY-MM-DD)")

    pipeline = yaml.safe_load(CFG_PIPELINE.read_text())
    manifest = compute_manifest('sql')
    audit = {
        "start_ts": time.time(),
        "stages": [],
        "manifest": manifest,
        "params": {"start": start, "end": end},
    }

    conn = duckdb.connect(str(WORK_DIR / 'claims.duckdb'))

    build_codebook(conn)

    for stage in pipeline['stages']:
        t0 = time.time()
        run_sql(conn, stage, {
            'start_date': f"'{start}'",
            'end_date': f"'{end}'",
            'lookback_days': '365'
        })
        audit['stages'].append({"stage": stage, "secs": round(time.time() - t0, 3)})

    ART_DIR.joinpath('audit_log.json').write_text(json.dumps(audit, indent=2))


if __name__ == '__main__':
    main()
