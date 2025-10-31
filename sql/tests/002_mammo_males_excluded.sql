-- Assert males are excluded from mammogram numerator
WITH mammo_claims AS (
  SELECT DISTINCT c.member_id
  FROM stg_claims_pseudo c
  JOIN mammogram_cpt m ON c.cpt = m.cpt
),
male_mammo AS (
  SELECT e.member_id FROM stg_elig_pseudo e
  JOIN mammo_claims mc USING(member_id)
  WHERE e.sex = 'M'
)
SELECT CASE WHEN EXISTS (SELECT 1 FROM male_mammo) THEN
  RAISE_ERROR('Male member found in mammogram claim set')
ELSE 0 END AS ok;
