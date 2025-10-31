CREATE OR REPLACE TABLE flags_px AS
SELECT DISTINCT c.member_id, px.metric, c.svc_date
FROM norm_medical_claims c
JOIN codebook_px px ON c.px1 = px.code;
