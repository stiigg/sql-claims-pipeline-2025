SELECT 'norm_medical_claims' AS table_name,
       SUM(member_id IS NULL) AS missing_member_id,
       SUM(svc_date  IS NULL) AS missing_svc_date
FROM norm_medical_claims;
