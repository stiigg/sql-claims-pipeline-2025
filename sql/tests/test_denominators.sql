SELECT CASE WHEN COUNT(DISTINCT member_id)=0
  THEN RAISE_ERROR('Denominator zero in cohort_base')
  ELSE 1 END AS pass
FROM cohort_base;
