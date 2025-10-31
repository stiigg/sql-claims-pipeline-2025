# Environment & Security Attestation

- **Compute boundary:** Dedicated VPC subnet with no public ingress. Bastion access requires hardware-backed MFA and SSH certificate auth.
- **Storage controls:** Encrypted volumes (AES-256) for `secure_input/` and `secure_work/`. Snapshots disabled; backups encrypted and rotated per 30-day retention policy.
- **Network posture:** SFTP ingress restricted to client-supplied IP allowlist. All outbound traffic egresses via managed NAT with logging enabled.
- **Logging & monitoring:**
  - System logs retained for 90 days in `var/log` with immutable storage.
  - Pipeline audit bundles archived in `artifacts/audit_bundle_*` and encrypted using client-provided key material.
  - Benchmark telemetry (CPU, memory) captured in `artifacts/benchmark.json` for capacity validation.
- **Identity & access:**
  - Principle of least privilege enforced via IAM groups.
  - Access reviews performed before each ingestion cycle; revocations documented in this file.
- **Compliance references:** Controls mapped to HIPAA Security Rule requirements in `docs/POLICY_MAPPING_HIPAA.md`.

Update this attestation for each deployment by listing environment identifiers, key custodians, and any compensating controls required by the client.
