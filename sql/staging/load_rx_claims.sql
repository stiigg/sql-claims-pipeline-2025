COPY stg_rx_claims
FROM 'secure_input/rx_claims_*.csv'
(AUTO_DETECT TRUE, HEADER TRUE);
