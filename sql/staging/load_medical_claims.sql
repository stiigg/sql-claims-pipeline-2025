COPY stg_medical_claims
FROM 'secure_input/medical_claims_*.csv'
(AUTO_DETECT TRUE, HEADER TRUE);
