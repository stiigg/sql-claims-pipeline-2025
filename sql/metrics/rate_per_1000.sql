-- :metric_name, :start_date, :end_date
WITH denom AS (
  SELECT COUNT(DISTINCT member_id) AS n FROM cohort_base
),
numer AS (
  SELECT COUNT(DISTINCT f.member_id) AS n
  FROM flags_dx f JOIN cohort_base c USING (member_id)
  WHERE f.metric = :metric_name
    AND f.first_hit_date BETWEEN :start_date AND :end_date
)
SELECT :metric_name AS metric,
       numer.n AS numerator,
       (SELECT n FROM denom) AS denominator,
       (numer.n * 1000.0) / NULLIF((SELECT n FROM denom),0) AS rate_per_1000
FROM numer;
