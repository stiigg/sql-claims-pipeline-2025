"""Render the destruction certificate template with runtime metadata."""
from __future__ import annotations

import os
import time
from pathlib import Path

TEMPLATE = Path("policies/DATA_DESTRUCTION_CERT_TEMPLATE.md")
ARTIFACT = Path("artifacts/destruction_certificate.md")
GIT_SHA = Path("artifacts/git_sha.txt")


def template_context() -> dict[str, str]:
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    git_sha = GIT_SHA.read_text().strip() if GIT_SHA.exists() else ""
    return {
        "client_name": os.environ.get("CLIENT_NAME", "<client>") or "<client>",
        "project_name": os.environ.get("PROJECT_NAME", "<engagement>") or "<engagement>",
        "datasets": os.environ.get("DATASETS", "<datasets>") or "<datasets>",
        "method": os.environ.get("DESTRUCTION_METHOD", "secure delete"),
        "location": os.environ.get("ENVIRONMENT_LOCATION", "<environment>") or "<environment>",
        "timestamp": timestamp,
        "operator": os.environ.get("OPERATOR", os.environ.get("USER", "operator")),
        "git_sha": git_sha,
    }


def main() -> None:
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    if not TEMPLATE.exists():
        ARTIFACT.write_text("Template missing. Please restore policies/DATA_DESTRUCTION_CERT_TEMPLATE.md\n")
        return
    ctx = template_context()
    content = TEMPLATE.read_text()
    rendered = content
    for key, value in ctx.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", value)
    ARTIFACT.write_text(rendered)
    print(f"Wrote destruction certificate to {ARTIFACT}")


if __name__ == "__main__":
    main()
