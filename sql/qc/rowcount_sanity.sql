SELECT 'stg_medical_claims' AS table_name, COUNT(*) AS row_count FROM stg_medical_claims
UNION ALL
SELECT 'stg_rx_claims', COUNT(*) FROM stg_rx_claims
UNION ALL
SELECT 'stg_eligibility', COUNT(*) FROM stg_eligibility;
