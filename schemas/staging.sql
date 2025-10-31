CREATE TABLE IF NOT EXISTS stg_medical_claims (
  claim_id VARCHAR, member_id VARCHAR, svc_date DATE,
  dx1 VARCHAR, dx2 VARCHAR, px1 VARCHAR, pos VARCHAR, drg VARCHAR,
  admit_date DATE, discharge_date DATE, discharge_status VARCHAR
);

CREATE TABLE IF NOT EXISTS stg_rx_claims (
  rx_id VARCHAR, member_id VARCHAR, fill_date DATE,
  ndc VARCHAR, days_supply INTEGER
);

CREATE TABLE IF NOT EXISTS stg_eligibility (
  member_id VARCHAR, dob DATE, sex VARCHAR,
  coverage_start DATE, coverage_end DATE
);
