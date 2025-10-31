CREATE OR REPLACE TABLE member_months AS
SELECT
  e.member_id,
  DATE_TRUNC('month', d)::DATE AS month_start,
  FLOOR(DATEDIFF('year', e.dob, d)) AS age,
  e.sex
FROM stg_eligibility e,
LATERAL GENERATE_SERIES(e.coverage_start, e.coverage_end, INTERVAL '1 month') AS d;
