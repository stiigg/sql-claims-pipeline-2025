COPY stg_eligibility
FROM 'secure_input/eligibility_*.csv'
(AUTO_DETECT TRUE, HEADER TRUE);
