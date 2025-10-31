run:
	START=$(START) END=$(END) python scripts/run_pipeline.py

qc:
	duckdb -c ".read sql/qc/qc_summary.sql" secure_work/claims.duckdb > artifacts/qc_summary.csv

report:
	python scripts/generate_methods_report.py && python scripts/export_excel_report.py

destroy:
	python scripts/destroy_data_securely.py
