from __future__ import annotations

import subprocess
from pathlib import Path


PHASE1_REQUIRED_FILES = {
    ".github/CODEOWNERS": [
        "CAVRA ownership map",
        "/src/cavra/api.py",
        "/docs/product/",
    ],
    "docs/governance/maintainer-governance.md": [
        "Maintainer Roles",
        "Security-Sensitive Change Classes",
        "Maintainer Onboarding Checklist",
        "RFC Requirement",
    ],
    "docs/governance/rfc-process.md": [
        "RFC Lifecycle",
        "Threat model",
        "Roadmap Status Updates",
    ],
    "docs/api-versioning-and-openapi.md": [
        "openapi/cavra-api.openapi.json",
        "Breaking API changes require",
        "x-cavra-api-versioning.public_contract",
    ],
    "docs/release-trust-checklist.md": [
        "SBOM",
        "Provenance",
        "OpenAPI contract",
        "Roadmap Evidence Rule",
    ],
    "docs/trust/ciso-enterprise-trust-pack.md": [
        "CISO",
        "No raw model egress",
        "Buyer Review Map",
        "Current Phase 1 Status",
    ],
}


def test_phase1_trust_governance_artifacts_exist() -> None:
    failures: list[str] = []
    for relative_path, required_fragments in PHASE1_REQUIRED_FILES.items():
        path = Path(relative_path)
        if not path.exists():
            failures.append(f"missing {relative_path}")
            continue
        text = path.read_text(encoding="utf-8")
        for fragment in required_fragments:
            if fragment not in text:
                failures.append(f"{relative_path} missing {fragment}")

    if failures:
        raise AssertionError("\n".join(failures))


def test_phase1_release_and_api_validators_pass() -> None:
    subprocess.run(["python3", "scripts/validate_release_security.py"], check=True)
    subprocess.run(["python3", "scripts/validate_openapi_contract.py"], check=True)
