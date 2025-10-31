-- Example assertion: ensure no out-of-range members in a female-only screening cohort
WITH female_50_74 AS (
  SELECT * FROM cohort_base WHERE sex='F' AND age BETWEEN 50 AND 74
)
SELECT CASE WHEN EXISTS (
  SELECT 1 FROM cohort_base c
  WHERE c.member_id NOT IN (SELECT member_id FROM female_50_74)
  AND c.sex='F' AND (c.age<50 OR c.age>74)
) THEN RAISE_ERROR('Age bounds violated for female_50_74 cohort') ELSE 1 END AS pass;
