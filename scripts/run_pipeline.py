
import json
import os
import subprocess
import time
from pathlib import Path

import duckdb
import psutil
import yaml

from tools.template_manifest import compute_manifest
from tools.codebook_build_tables import build as build_codebook

PIPELINE_PATHS = [Path('config/pipeline.yaml'), Path('config/pipeline.yml')]
ART_DIR = Path('artifacts')
WORK_DIR = Path('secure_work')

ART_DIR.mkdir(exist_ok=True)
WORK_DIR.mkdir(exist_ok=True)


def load_pipeline() -> list[str]:
    for path in PIPELINE_PATHS:
        if path.exists():
            pipeline = yaml.safe_load(path.read_text())
            break
    else:
        raise FileNotFoundError("No pipeline configuration found.")

    stages = pipeline.get('stages', [])
    if isinstance(stages, dict):
        ordered = []
        for group in stages.values():
            ordered.extend(group)
        stages = ordered
    return stages


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

    stages = load_pipeline()
    manifest = compute_manifest('sql')
    audit = {
        "start_ts": time.time(),
        "stages": [],
        "manifest": manifest,
        "params": {"start": start, "end": end},
        "operator": os.environ.get('OPERATOR', os.environ.get('USER')),
    }

    conn = duckdb.connect(str(WORK_DIR / 'claims.duckdb'))

    build_codebook(conn)

    process = psutil.Process()

    for stage in stages:
        t0 = time.time()
        cpu_before = process.cpu_times()
        rss_before = process.memory_info().rss
        run_sql(conn, stage, {
            'start_date': f"'{start}'",
            'end_date': f"'{end}'",
            'lookback_days': '365'
        })
        cpu_after = process.cpu_times()
        rss_after = process.memory_info().rss
        audit['stages'].append({
            "stage": stage,
            "secs": round(time.time() - t0, 3),
            "cpu_user_secs": round(cpu_after.user - cpu_before.user, 3),
            "cpu_system_secs": round(cpu_after.system - cpu_before.system, 3),
            "rss_mb": round(rss_after / (1024 * 1024), 2),
        })

    audit['end_ts'] = time.time()
    audit['wall_clock_secs'] = round(audit['end_ts'] - audit['start_ts'], 3)
    try:
        audit['git_sha'] = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
    except subprocess.CalledProcessError:
        audit['git_sha'] = None

    ART_DIR.joinpath('audit_log.json').write_text(json.dumps(audit, indent=2))


if __name__ == '__main__':
    main()
