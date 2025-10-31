-- Assert denominators are nonnegative
WITH res AS (
  SELECT * FROM dm_metrics_latest
)
SELECT CASE WHEN MIN(denominator) < 0 THEN
  RAISE_ERROR('Negative denominator detected')
ELSE 0 END AS ok FROM res;
