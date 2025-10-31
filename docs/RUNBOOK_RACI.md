# Runbook & RACI Overview

## Contacts & Roles

| Role | Name / Team | Responsibility |
|------|--------------|----------------|
| Responsible (R) | Data Engineering Lead | Operates pipeline, monitors ingestion, resolves data quality issues |
| Accountable (A) | Engagement Principal | Approves releases, signs audit and destruction certifications |
| Consulted (C) | Security Officer | Reviews environment controls, handles incident response |
| Informed (I) | Client Data Owner | Receives delivery notifications and remediation summaries |

## Workflow Timeline

1. **Ingestion confirmation** – within 4 hours of receiving client files; log checksum and metadata.
2. **Schema & DQ validation** – within 24 hours; publish scorecard, failure samples, remediation plan if required.
3. **Metric computation** – within 3 business days post ingestion; refresh Excel + methods package.
4. **Client review** – share reporting package alongside audit bundle for validation.
5. **Secure destruction** – within 5 business days of client acceptance, or immediately on written request.

## Escalation Paths

- **P0 security incident:** Notify Security Officer and Engagement Principal within 1 hour. Suspend compute access until cleared.
- **P1 data defect impacting deliverables:** Engagement Principal and Client Data Owner notified within 1 business day; remediation tracked in `artifacts/dq_failures_*` notes.
- **SLA breach risk:** Raise to Accountable role and document mitigation in `docs/DELIVERABLES.md`.

## Runbook Checklist

- [ ] SFTP fetch completed (`make sftp`).
- [ ] Checksums + ingestion log generated (`make checksums ingestlog`).
- [ ] Staging normalization executed (`make normalize`).
- [ ] Data dictionary refreshed (`make dict`).
- [ ] Pipeline run recorded with audit log (`make run`).
- [ ] Validation + scorecard exported (`make validate`).
- [ ] Metrics, demographics, reports prepared (`make metrics demographics report`).
- [ ] Benchmark + audit bundle archived (`make benchmark audit`).
- [ ] Destruction certificate produced after client sign-off (`make cert_destroy`).

Keep this document updated with team contacts and escalation procedures per engagement.
