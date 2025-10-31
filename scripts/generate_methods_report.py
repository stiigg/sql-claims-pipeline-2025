"""Generate a markdown methods report summarizing the run."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
import yaml

METRICS_CFG = Path("config/metrics.yml")
CODELIST_CFG = Path("config/code_lists.yml")
SCORECARD = Path("artifacts/dq_scorecard.csv")
COVERAGE = Path("artifacts/coverage_summary.csv")
METRICS_SUMMARY = Path("artifacts/metrics_summary.csv")
ARTIFACT_MD = Path("artifacts/methods_report.md")


def load_yaml(path: Path) -> dict[str, Any]:
    if path.exists():
        return yaml.safe_load(path.read_text())
    return {}


def load_csv(path: Path) -> pd.DataFrame | None:
    if path.exists():
        return pd.read_csv(path)
    return None


def metrics_section(cfg: dict[str, Any]) -> str:
    lines = ["## Metrics Catalog"]
    for metric_id, spec in cfg.get("metrics", {}).items():
        lines.append(f"### {metric_id}")
        lines.append(f"- Type: {spec.get('type')}")
        if spec.get("metric_name"):
            lines.append(f"- Metric name: {spec['metric_name']}")
        cohort = spec.get("cohort")
        if cohort:
            lines.append("- Cohort filters:")
            for key, value in cohort.items():
                lines.append(f"  - {key}: {value}")
        lines.append("")
    return "\n".join(lines)


def codelist_section(cfg: dict[str, Any]) -> str:
    lines = ["## Reference Code Lists"]
    for domain, mapping in cfg.items():
        lines.append(f"### {domain.upper()}")
        for key, path in mapping.items():
            lines.append(f"- {key}: `{path}`")
        lines.append("")
    return "\n".join(lines)


def dataframe_section(title: str, df: pd.DataFrame | None) -> str:
    if df is None or df.empty:
        return f"## {title}\nNo data available."
    return "\n".join([f"## {title}", df.to_markdown(index=False)])


def main() -> None:
    metrics_cfg = load_yaml(METRICS_CFG)
    codelists = load_yaml(CODELIST_CFG)
    dq_scorecard = load_csv(SCORECARD)
    coverage = load_csv(COVERAGE)
    metric_results = load_csv(METRICS_SUMMARY)

    sections = [
        "# Methods Report",
        metrics_section(metrics_cfg),
        codelist_section(codelists),
        dataframe_section("Data Quality Scorecard", dq_scorecard),
        dataframe_section("Coverage Summary", coverage),
        dataframe_section("Metric Results", metric_results),
    ]

    ARTIFACT_MD.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT_MD.write_text("\n\n".join(filter(None, sections)))
    print(f"Methods report written to {ARTIFACT_MD}")


if __name__ == "__main__":
    main()
