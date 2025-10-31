SELECT
  AVG(age) AS avg_age,
  100.0 * SUM(CASE WHEN sex='F' THEN 1 ELSE 0 END) / COUNT(*) AS pct_female,
  100.0 * SUM(CASE WHEN sex='M' THEN 1 ELSE 0 END) / COUNT(*) AS pct_male,
  COUNT(*) AS total_members
FROM cohort_base;
