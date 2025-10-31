run:
	START=$(START) END=$(END) python scripts/run_pipeline.py

ingest: sftp checksums ingestlog normalize dict

sftp:
	python scripts/sftp_fetch.py

checksums:
	python scripts/generate_checksums.py

ingestlog:
	python scripts/generate_ingestion_log.py

normalize:
	mkdir -p secure_work
	duckdb secure_work/claims.duckdb -c ".read sql/staging/load_medical_claims.sql"
	duckdb secure_work/claims.duckdb -c ".read sql/staging/load_rx_claims.sql"
	duckdb secure_work/claims.duckdb -c ".read sql/staging/load_eligibility.sql"

dict:
	python scripts/generate_data_dictionary.py

validate:
	python scripts/validate_schema_and_dq.py

metrics:
	python scripts/compute_metrics.py

demographics:
	python scripts/compute_demographics.py

report:
	python scripts/export_excel_report.py
	python scripts/generate_methods_report.py

benchmark:
	python scripts/benchmark_pipeline.py

audit:
	python scripts/build_audit_bundle.py

cert_destroy:
	python scripts/destroy_data_securely.py
	python scripts/generate_destruction_certificate.py

handover:
	python scripts/build_audit_bundle.py --handover

qc:
	mkdir -p artifacts
	duckdb secure_work/claims.duckdb -c ".read sql/qc/qc_summary.sql" > artifacts/qc_summary.csv

destroy:
	python scripts/destroy_data_securely.py

test:
	pytest -q || true
	duckdb secure_work/claims.duckdb -c ".read tests/test_reconciliation.sql" || true
