
# SQL Claims Pipeline – Plus Pack

Adds research-aligned governance & reproducibility features:

- **metrics_codebook.yaml**: versioned metric definitions with codes, windows, exclusions, limitations
- **sql/tests/**: DuckDB-friendly SQL "assertions" for key rules (denominators nonnegative, males excluded from mammo numerator, age bounds)
- **tools/template_manifest.py**: build/compare a hash manifest of SQL templates (alerts on change)
- **scripts/generate_methods_report.py**: produce `reports/methods_and_limitations.md` from audit + metrics + codebook
- **sql/qc_summary.sql**: summarize missingness/row counts
- **config/rbac_policy.yaml**: example role-based access policy (analyst/auditor/phi_admin)

## Typical run order
1. Run your base pipeline to generate `artifacts/metrics.csv` and `artifacts/audit.jsonl`.
2. Record a manifest: `python tools/template_manifest.py`
3. Generate the Methods & Limitations doc: `python scripts/generate_methods_report.py`
4. When templates change, compare & alert: `python tools/template_manifest.py --compare`

> Integrate these steps into Airflow/Prefect tasks for continuous auditing.
