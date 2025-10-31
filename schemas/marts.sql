CREATE TABLE IF NOT EXISTS dim_members (
  member_id VARCHAR PRIMARY KEY, dob DATE, sex VARCHAR
);

CREATE TABLE IF NOT EXISTS fact_encounters (
  member_id VARCHAR, encounter_type VARCHAR, svc_date DATE,
  admit_date DATE, discharge_date DATE, dx_group VARCHAR, complication_flag INTEGER
);
