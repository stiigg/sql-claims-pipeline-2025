"""Stub generator for synthetic claims data."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

OUTPUT_DIR = Path("secure_input/raw")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    elig = pd.DataFrame(
        {
            "member_id": ["SYN001", "SYN002"],
            "dob": ["1980-01-15", "1975-06-30"],
            "sex": ["F", "M"],
            "start_date": ["2023-01-01", "2023-01-01"],
            "end_date": ["2023-12-31", "2023-12-31"],
        }
    )
    elig.to_csv(OUTPUT_DIR / "eligibility_synthetic.csv", index=False)


if __name__ == "__main__":
    main()
