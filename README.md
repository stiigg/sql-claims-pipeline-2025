# SQL Claims Pipeline 2025

HIPAA-conscious, **SQL-first** claims analytics pipeline with:
- Versioned metric **codebook**
- DuckDB-friendly **SQL unit tests**
- **Template manifest hashing** & change alerts
- **Methods & Limitations** report generator
- Starter **RBAC** policy
- CI workflow to lint & run static checks

> This repository mirrors 2024–2025 best practices for standardized, auditable, and reproducible healthcare claims analytics.

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# snapshot template manifest
python tools/template_manifest.py

# generate methods & limitations report (expects artifacts/metrics.csv + artifacts/audit.jsonl)
python scripts/generate_methods_report.py

# compare manifest to detect SQL template changes
python tools/template_manifest.py --compare
```

## SQL Tests (DuckDB)
- Place your staging/transform artifacts in DuckDB.
- Run the assertions in `sql/tests/*.sql` against your DuckDB database.

## Repo Layout
- `config/metrics_codebook.yaml` – metric definitions & limitations
- `config/rbac_policy.yaml` – example governance policy
- `sql/tests/*` – SQL assertions
- `sql/qc_summary.sql` – QC summary table
- `tools/template_manifest.py` – template hashing & alerts
- `scripts/generate_methods_report.py` – report generator
- `artifacts/` – audit & outputs (not tracked in CI; locally generated)

## Compliance Notes
This sample includes pseudonymization patterns and governance scaffolding. For production, integrate:
- Encrypted storage, SFTP ingestion, KMS-managed salts/keys
- Role-based access and audit trail persistence
- Deletion certificates and retention policies

## License
Apache-2.0
