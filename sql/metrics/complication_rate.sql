WITH denom AS (SELECT COUNT(DISTINCT member_id) AS n FROM cohort_base),
comp AS (
  SELECT member_id FROM encounters
  WHERE complication_flag=1 AND svc_date BETWEEN :start_date AND :end_date
)
SELECT 'complication_rate' AS metric,
       COUNT(*) * 1.0 / NULLIF((SELECT n FROM denom),0) AS rate
FROM comp;
