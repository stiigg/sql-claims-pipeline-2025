CREATE OR REPLACE TABLE dm_qc_summary AS
SELECT
  (SELECT COUNT(*) FROM stg_elig) AS elig_rows,
  (SELECT SUM(qc_missing) FROM stg_elig) AS elig_missing,
  (SELECT COUNT(*) FROM stg_claims) AS claims_rows,
  (SELECT SUM(qc_missing) FROM stg_claims) AS claims_missing;
