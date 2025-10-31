"""Populate the Excel reporting template with computed metrics."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
import yaml
from openpyxl import Workbook, load_workbook

CONFIG = Path("config/report_mapping.yml")
METRICS = Path("artifacts/metrics_summary.csv")
DEMOGRAPHICS = Path("artifacts/demographics.csv")
REPORT = Path("artifacts/report.xlsx")


def load_config() -> dict[str, Any]:
    if CONFIG.exists():
        return yaml.safe_load(CONFIG.read_text())
    return {"outputs": {}}


def load_metrics() -> dict[str, dict[str, Any]]:
    if not METRICS.exists():
        return {}
    df = pd.read_csv(METRICS)
    metrics = {}
    for _, row in df.iterrows():
        metric_id = row.get("metric_id") or row.get("metric")
        metrics[str(metric_id)] = row.dropna().to_dict()
    return metrics


def load_demographics() -> dict[str, Any]:
    if not DEMOGRAPHICS.exists():
        return {}
    return pd.read_csv(DEMOGRAPHICS).iloc[0].dropna().to_dict()


def resolve_value(key: str, metrics: dict[str, dict[str, Any]], demographics: dict[str, Any]) -> Any:
    parts = key.split(".")
    if not parts:
        return None
    if parts[0] == "metrics" and len(parts) >= 3:
        metric_id = parts[1]
        field = parts[2]
        return metrics.get(metric_id, {}).get(field)
    if parts[0] == "demographics" and len(parts) >= 2:
        return demographics.get(parts[1])
    return None


def populate_template(config: dict[str, Any], metrics: dict[str, dict[str, Any]], demographics: dict[str, Any]) -> Workbook:
    template_path = Path(config.get("workbook_template", ""))
    if template_path.exists():
        workbook = load_workbook(template_path)
    else:
        workbook = Workbook()
        first_sheet = next(iter(config.get("outputs", {})), "Summary")
        workbook.active.title = first_sheet
    for sheet_name, assignments in config.get("outputs", {}).items():
        if sheet_name in workbook.sheetnames:
            sheet = workbook[sheet_name]
        else:
            sheet = workbook.create_sheet(sheet_name)
        for cell, key in assignments.items():
            sheet[cell] = resolve_value(key, metrics, demographics)
    return workbook


def write_raw_tabs(workbook: Workbook, metrics_df: pd.DataFrame | None, demographics_df: pd.DataFrame | None) -> None:
    if metrics_df is not None:
        if "RawMetrics" in workbook.sheetnames:
            ws = workbook["RawMetrics"]
            workbook.remove(ws)
        ws = workbook.create_sheet("RawMetrics")
        ws.append(list(metrics_df.columns))
        for row in metrics_df.itertuples(index=False, name=None):
            ws.append(list(row))
    if demographics_df is not None:
        if "RawDemographics" in workbook.sheetnames:
            ws = workbook["RawDemographics"]
            workbook.remove(ws)
        ws = workbook.create_sheet("RawDemographics")
        ws.append(list(demographics_df.columns))
        for row in demographics_df.itertuples(index=False, name=None):
            ws.append(list(row))


def main() -> None:
    config = load_config()
    metrics = load_metrics()
    demographics = load_demographics()
    metrics_df = pd.read_csv(METRICS) if METRICS.exists() else None
    demo_df = pd.read_csv(DEMOGRAPHICS) if DEMOGRAPHICS.exists() else None

    workbook = populate_template(config, metrics, demographics)
    write_raw_tabs(workbook, metrics_df, demo_df)

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    workbook.save(REPORT)
    print(f"Excel report generated at {REPORT}")


if __name__ == "__main__":
    main()
