-- Materialized view of data-quality rule failures for reference.
WITH eligibility_missing AS (
  SELECT 'eligibility.member_id_missing' AS rule, COUNT(*) AS fails
  FROM eligibility_staged
  WHERE member_id IS NULL
), medical_orphans AS (
  SELECT 'medical.member_not_in_eligibility' AS rule, COUNT(*) AS fails
  FROM medical_staged m
  LEFT JOIN eligibility_staged e USING (member_id)
  WHERE e.member_id IS NULL
), rx_missing_ndc AS (
  SELECT 'rx.ndc_missing' AS rule, COUNT(*) AS fails
  FROM rx_staged
  WHERE ndc IS NULL
)
SELECT * FROM eligibility_missing
UNION ALL
SELECT * FROM medical_orphans
UNION ALL
SELECT * FROM rx_missing_ndc;
