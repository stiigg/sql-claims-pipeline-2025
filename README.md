# Claims Analytics Pipeline (HIPAA Safe Harbor)

## Quickstart
1. Place input files in `secure_input/`.
2. Run schema + pipeline:
   ```bash
   START=2024-01-01 END=2024-12-31 make run
   ```
3. Generate Methods + Excel report:
   ```bash
   make report
   ```
4. Inspect artifacts in `artifacts/`.
5. After client sign-off, destroy working dirs:
   ```bash
   make destroy
   ```

## Notes
- Swap to Snowflake/BigQuery by replacing DuckDB connection in `scripts/run_pipeline.py` and providing warehouse-specific loaders.
- SQL is ANSI-compliant for portability; update denominator logic and QC assertions per client needs.
- Ensure HIPAA Safe Harbor compliance by running in isolated, access-controlled environments.
