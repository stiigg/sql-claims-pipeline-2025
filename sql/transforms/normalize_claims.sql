CREATE OR REPLACE TABLE norm_medical_claims AS
SELECT
  claim_id, member_id,
  CAST(svc_date AS DATE) AS svc_date,
  UPPER(dx1) AS dx1, UPPER(dx2) AS dx2,
  UPPER(px1) AS px1, UPPER(pos) AS pos, UPPER(drg) AS drg,
  CAST(admit_date AS DATE) AS admit_date,
  CAST(discharge_date AS DATE) AS discharge_date,
  UPPER(discharge_status) AS discharge_status
FROM stg_medical_claims;

CREATE OR REPLACE TABLE norm_rx_claims AS
SELECT rx_id, member_id, CAST(fill_date AS DATE) AS fill_date,
       UPPER(ndc) AS ndc, days_supply
FROM stg_rx_claims;
