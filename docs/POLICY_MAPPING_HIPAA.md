# HIPAA Safeguard Mapping

| Workflow Component | Control Description | HIPAA Citation |
|--------------------|--------------------|----------------|
| SFTP ingestion with checksums | Ensures integrity of data in transit and validates against tampering | 45 CFR §164.312(c)(1), §164.312(e)(1) |
| Access-controlled staging area | Limits PHI exposure to authorized workforce members | 45 CFR §164.308(a)(3), §164.312(a)(1) |
| Schema validation & DQ scorecards | Maintains data integrity and accuracy for decision making | 45 CFR §164.306(a)(1) |
| Audit log bundle with git SHA | Enables traceability and non-repudiation of actions | 45 CFR §164.312(b) |
| Benchmark telemetry | Supports availability safeguards and capacity planning | 45 CFR §164.308(a)(7) |
| Secure destruction workflow | Protects against improper disposal of PHI | 45 CFR §164.310(d)(2)(i)-(ii) |
| Reproducibility documentation | Demonstrates compliance and facilitates audits | 45 CFR §164.316(b)(1) |

Confirm mapping with client compliance/legal teams before final sign-off.
