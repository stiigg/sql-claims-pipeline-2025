-- Scorecard view to compute pass rates.
WITH totals AS (
  SELECT 'eligibility_staged' AS table_name, COUNT(*) AS rows FROM eligibility_staged
  UNION ALL SELECT 'medical_staged', COUNT(*) FROM medical_staged
  UNION ALL SELECT 'rx_staged', COUNT(*) FROM rx_staged
)
SELECT c.rule,
       c.fails,
       CASE
         WHEN c.rule LIKE 'eligibility.%' THEN 1 - (c.fails / NULLIF(t.rows,0))
         WHEN c.rule LIKE 'medical.%' THEN 1 - (c.fails / NULLIF(t.rows,0))
         WHEN c.rule LIKE 'rx.%' THEN 1 - (c.fails / NULLIF(t.rows,0))
       END AS pass_rate
FROM (SELECT * FROM read_csv_auto('artifacts/dq_scorecard.csv')) c
LEFT JOIN totals t
  ON (c.rule LIKE 'eligibility.%' AND t.table_name='eligibility_staged')
  OR (c.rule LIKE 'medical.%' AND t.table_name='medical_staged')
  OR (c.rule LIKE 'rx.%' AND t.table_name='rx_staged');
