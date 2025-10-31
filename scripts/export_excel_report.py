
from pathlib import Path

import pandas as pd

metrics_csv = Path('artifacts/metrics.csv')
demo_csv = Path('artifacts/demographics.csv')
report_path = Path('artifacts/report.xlsx')

report_path.parent.mkdir(exist_ok=True)

with pd.ExcelWriter(report_path, engine='xlsxwriter') as xl:
    if metrics_csv.exists():
        pd.read_csv(metrics_csv).to_excel(xl, sheet_name='Metrics', index=False)
    if demo_csv.exists():
        pd.read_csv(demo_csv).to_excel(xl, sheet_name='Demographics', index=False)
