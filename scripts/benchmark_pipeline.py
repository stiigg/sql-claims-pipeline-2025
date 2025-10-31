"""Summarize runtime and resource usage for the most recent pipeline run."""
from __future__ import annotations

import json
import time
from pathlib import Path

import psutil

AUDIT_LOG = Path("artifacts/audit_log.json")
BENCHMARK = Path("artifacts/benchmark.json")


def main() -> None:
    BENCHMARK.parent.mkdir(exist_ok=True)
    benchmark = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "cpu_percent": psutil.cpu_percent(interval=0.1),
        "rss_mb": psutil.Process().memory_info().rss / (1024 * 1024),
        "stages": [],
        "wall_clock_seconds": None,
    }

    if AUDIT_LOG.exists():
        data = json.loads(AUDIT_LOG.read_text())
        benchmark["stages"] = data.get("stages", [])
        if benchmark["stages"]:
            benchmark["wall_clock_seconds"] = sum(stage.get("secs", 0) for stage in benchmark["stages"])
        benchmark["parameters"] = data.get("params")
        benchmark["git_sha"] = data.get("git_sha")

    BENCHMARK.write_text(json.dumps(benchmark, indent=2))
    print("Benchmark report written to", BENCHMARK)


if __name__ == "__main__":
    main()
