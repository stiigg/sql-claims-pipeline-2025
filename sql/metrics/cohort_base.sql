CREATE OR REPLACE TABLE cohort_base AS
SELECT DISTINCT m.member_id, m.age, m.sex
FROM member_months m
WHERE m.month_start BETWEEN :start_date AND :end_date;
