-- :screening_metric, :start_date, :end_date, :min_age, :max_age, :sex_filter, :lookback_days
WITH eligible AS (
  SELECT member_id
  FROM cohort_base
  WHERE age BETWEEN :min_age AND :max_age
    AND (:sex_filter = 'ANY' OR sex = :sex_filter)
),
screens AS (
  SELECT DISTINCT c.member_id
  FROM norm_medical_claims c
  JOIN codebook_px px ON c.px1 = px.code AND px.metric = :screening_metric
  WHERE c.svc_date BETWEEN :start_date - INTERVAL '1 day' * :lookback_days AND :end_date
)
SELECT :screening_metric AS metric,
       COUNT(DISTINCT screens.member_id) AS numerator,
       COUNT(DISTINCT eligible.member_id) AS denominator,
       (COUNT(DISTINCT screens.member_id) * 1.0) / NULLIF(COUNT(DISTINCT eligible.member_id),0) AS screening_rate
FROM eligible LEFT JOIN screens USING (member_id);
