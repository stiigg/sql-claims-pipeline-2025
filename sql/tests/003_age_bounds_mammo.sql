-- Assert mammogram denominator age bounds 40-74
WITH period AS (SELECT DATE '{AS_OF_END}' AS end_date),
violations AS (
 SELECT e.member_id
 FROM stg_elig_pseudo e, period p
 WHERE e.sex='F' AND (datediff('year', e.dob, p.end_date) < 40 OR datediff('year', e.dob, p.end_date) > 74)
)
SELECT CASE WHEN EXISTS (SELECT 1 FROM violations) THEN
 RAISE_ERROR('Age bounds violation in mammogram denominator candidates')
ELSE 0 END AS ok;
