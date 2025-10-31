# Reproducibility Guide

1. `python -m venv .venv && source .venv/bin/activate`
2. `pip install -r requirements.txt`
3. Place client extracts inside `secure_input/raw/`. Run `make checksums ingestlog` to lock provenance.
4. Normalize input to staged tables via `make normalize` (DuckDB SQL transforms).
5. Configure run window: `export START=2024-01-01 END=2024-12-31` (override per engagement).
6. Execute full pipeline + metrics: `make run validate metrics demographics report`.
7. Capture runtime telemetry: `make benchmark`.
8. Build audit bundle: `make audit`.
9. Tag release: `git tag -a delivery-<client>-<date> -m "Delivery snapshot" && git push --tags`.
10. After client sign-off, produce destruction certificate with `make cert_destroy`.

Append the resulting `artifacts/` outputs to the handover folder for immutable storage. Include the commit SHA recorded in `artifacts/git_sha.txt` when sharing with the client.
