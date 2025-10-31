WITH idx AS (
  SELECT member_id, discharge_date
  FROM encounters
  WHERE encounter_type='INPATIENT'
    AND discharge_date BETWEEN :start_date AND :end_date
),
readmits AS (
  SELECT a.member_id
  FROM idx a
  JOIN encounters b ON a.member_id=b.member_id
   AND b.encounter_type='INPATIENT'
   AND b.admit_date > a.discharge_date
   AND DATEDIFF('day', a.discharge_date, b.admit_date) <= 30
)
SELECT 'readmission_rate' AS metric,
       (COUNT(*) * 1.0) / NULLIF((SELECT COUNT(*) FROM idx),0) AS rate
FROM readmits;
