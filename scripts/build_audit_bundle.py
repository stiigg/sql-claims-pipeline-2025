"""Bundle run artifacts for audit or handover."""
from __future__ import annotations

import argparse
import subprocess
import time
import zipfile
from pathlib import Path
from shutil import copy2

ART_DIR = Path("artifacts")
HANDOVER_DIR = ART_DIR / "handover"

FILES = [
    ART_DIR / "checksums.csv",
    ART_DIR / "ingestion_log.csv",
    ART_DIR / "data_dictionary.csv",
    ART_DIR / "dq_scorecard.csv",
    ART_DIR / "coverage_summary.csv",
    ART_DIR / "schema_validation.json",
    ART_DIR / "metrics_summary.csv",
    ART_DIR / "demographics.csv",
    ART_DIR / "report.xlsx",
    ART_DIR / "methods_report.md",
    ART_DIR / "methods_report.pdf",
    ART_DIR / "benchmark.json",
    ART_DIR / "git_sha.txt",
]


def ensure_git_sha() -> None:
    target = ART_DIR / "git_sha.txt"
    if target.exists():
        return
    try:
        sha = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    except subprocess.CalledProcessError:
        return
    ART_DIR.mkdir(exist_ok=True)
    target.write_text(f"{sha}\n")


def build_bundle(handover: bool = False) -> Path:
    ART_DIR.mkdir(exist_ok=True)
    ensure_git_sha()
    timestamp = time.strftime("%Y%m%dT%H%M%S")
    bundle_path = ART_DIR / f"audit_bundle_{timestamp}.zip"

    with zipfile.ZipFile(bundle_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in FILES:
            if path.exists():
                zf.write(path, path.relative_to(ART_DIR))
        for extra in ART_DIR.glob("dq_failures_*.csv"):
            zf.write(extra, extra.relative_to(ART_DIR))

    if handover:
        HANDOVER_DIR.mkdir(parents=True, exist_ok=True)
        copy2(bundle_path, HANDOVER_DIR / bundle_path.name)
        for path in [ART_DIR / "report.xlsx", ART_DIR / "methods_report.md", ART_DIR / "methods_report.pdf"]:
            if path.exists():
                copy2(path, HANDOVER_DIR / path.name)
    return bundle_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Build audit or handover bundle")
    parser.add_argument("--handover", action="store_true", help="Copy bundle into artifacts/handover")
    args = parser.parse_args()
    bundle = build_bundle(handover=args.handover)
    print(f"Created {bundle}")


if __name__ == "__main__":
    main()
