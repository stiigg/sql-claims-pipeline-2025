CREATE OR REPLACE TABLE flags_dx AS
WITH hits AS (
  SELECT c.member_id, c.svc_date, cb.metric
  FROM norm_medical_claims c
  JOIN codebook_dx cb
    ON c.dx1 LIKE cb.pattern OR c.dx2 LIKE cb.pattern
)
SELECT member_id, metric, MIN(svc_date) AS first_hit_date
FROM hits
GROUP BY 1,2;
