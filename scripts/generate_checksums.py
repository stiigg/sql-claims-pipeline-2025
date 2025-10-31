"""Compute SHA256 checksums for files under secure_input/raw."""
from __future__ import annotations

import csv
import hashlib
import time
from pathlib import Path

RAW_DIR = Path("secure_input/raw")
ARTIFACT = Path("artifacts/checksums.csv")


def checksum_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    for path in sorted(RAW_DIR.glob("*")):
        if path.is_file():
            rows.append(
                {
                    "filename": path.name,
                    "sha256": checksum_file(path),
                    "bytes": path.stat().st_size,
                    "generated_at": timestamp,
                }
            )

    fieldnames = ["filename", "sha256", "bytes", "generated_at"]
    with ARTIFACT.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
