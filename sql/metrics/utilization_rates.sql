WITH denom AS (SELECT COUNT(DISTINCT member_id) AS n FROM cohort_base),
er AS (
  SELECT member_id FROM encounters
  WHERE encounter_type='ER' AND svc_date BETWEEN :start_date AND :end_date
),
er_avoid AS (
  SELECT member_id FROM encounters
  WHERE encounter_type='ER' AND dx_group IN ('nonemergent','primary_care_treatable')
    AND svc_date BETWEEN :start_date AND :end_date
),
inpt AS (
  SELECT member_id FROM encounters
  WHERE encounter_type='INPATIENT' AND admit_date BETWEEN :start_date AND :end_date
),
avoidable_adm AS (
  SELECT member_id FROM encounters
  WHERE encounter_type='INPATIENT' AND dx_group='pqi'
    AND admit_date BETWEEN :start_date AND :end_date
)
SELECT 'er_visit_rate' AS metric, (COUNT(*) * 1000.0) / (SELECT n FROM denom) AS rate_per_1000 FROM er
UNION ALL
SELECT 'avoidable_er_rate', (COUNT(*) * 1000.0) / (SELECT n FROM denom) FROM er_avoid
UNION ALL
SELECT 'inpatient_admission_rate', (COUNT(*) * 1000.0) / (SELECT n FROM denom) FROM inpt
UNION ALL
SELECT 'avoidable_admission_rate', (COUNT(*) * 1000.0) / (SELECT n FROM denom) FROM avoidable_adm;
