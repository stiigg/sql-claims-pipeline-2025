COPY (
  SELECT * FROM (
    SELECT 'rowcount_norm_medical' AS check_name, COUNT(*) AS value FROM norm_medical_claims
    UNION ALL
    SELECT 'rowcount_encounters', COUNT(*) FROM encounters
  )
) TO 'artifacts/qc_summary.csv' WITH (HEADER, DELIMITER ',');
