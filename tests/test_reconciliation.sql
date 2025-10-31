-- Basic reconciliation smoke test.
-- This query should return zero rows when fact tables reconcile with eligibility.
SELECT member_id
FROM medical_staged
WHERE member_id NOT IN (SELECT member_id FROM eligibility_staged)
LIMIT 10;
