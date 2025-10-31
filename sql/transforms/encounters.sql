CREATE OR REPLACE TABLE encounters AS
SELECT
  member_id,
  CASE
    WHEN pos IN ('23') THEN 'ER'
    WHEN drg IS NOT NULL THEN 'INPATIENT'
    ELSE 'OUTPATIENT'
  END AS encounter_type,
  svc_date, admit_date, discharge_date,
  CASE WHEN dx1 LIKE 'T8%' THEN 1 ELSE 0 END AS complication_flag,
  CASE
    WHEN dx1 LIKE 'J%25' THEN 'primary_care_treatable'
    WHEN dx1 LIKE 'R%10' THEN 'nonemergent'
    ELSE 'other'
  END AS dx_group
FROM norm_medical_claims;
