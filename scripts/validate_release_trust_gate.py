from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any


REQUIRED_TEXT = {
    "docs/release-trust-checklist.md": [
        "scripts/generate_community_release_trust_artifacts.py",
        "scripts/validate_release_trust_gate.py",
        "SBOM",
        "Provenance",
        "OpenAPI contract",
        "Roadmap Evidence Rule",
    ],
    "docs/api-versioning-and-openapi.md": [
        "openapi/cavra-api.openapi.json",
        "Breaking API changes require",
        "x-cavra-api-versioning.public_contract",
    ],
    "docs/product/cavra-unified-enterprise-product-enhancement-roadmap.md": [
        "| R1.3 |",
        "release trust gate",
        "Community release workflow",
    ],
    ".github/workflows/release-community.yml": [
        "scripts/validate_release_security.py",
        "scripts/validate_openapi_contract.py",
        "scripts/generate_community_release_trust_artifacts.py",
        "scripts/validate_release_trust_gate.py",
        "python -m build",
        "actions/upload-artifact@v4",
    ],
    ".github/workflows/go-release.yml": [
        "id-token: write",
        "attestations: write",
        "artifact-metadata: write",
        "scripts/package_go_release.py",
        "actions/attest@v4",
        "github-keyless-attestation.json",
    ],
    ".github/workflows/attest-community-release.yml": [
        "id-token: write",
        "attestations: write",
        "artifact-metadata: write",
        "actions/attest@v4",
        "gh attestation verify",
        "community-release-keyless-attestation-evidence.json",
    ],
    ".github/workflows/verify-community-release.yml": [
        "scripts/verify-community-release-artifacts.py",
    ],
    ".github/workflows/api-contract.yml": [
        "scripts/export_openapi_contract.py",
        "scripts/validate_openapi_contract.py",
    ],
    "scripts/generate_community_release_trust_artifacts.py": [
        "SPDX-2.3",
        "https://slsa.dev/provenance/v1",
        "cavra.community.release_trust.v1",
        "github-keyless-attestation-workflow",
    ],
    "scripts/validate_release_security.py": [
        "actions/attest@v4",
        "github-keyless-attestation.json",
    ],
    "scripts/package_go_release.py": [
        "cavra-runtime.sbom.spdx.json",
        "cavra-runtime.provenance.intoto.json",
        "cavra-runtime.signing-operations.json",
        "offline-trust-root-bootstrap.json",
    ],
    "openapi/cavra-api.openapi.json": [
        "\"openapi\": \"3.1.0\"",
        "x-cavra-api-versioning",
    ],
}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_required_text() -> list[str]:
    failures: list[str] = []
    for relative_path, fragments in REQUIRED_TEXT.items():
        path = Path(relative_path)
        if not path.exists():
            failures.append(f"missing {relative_path}")
            continue
        text = path.read_text(encoding="utf-8")
        for fragment in fragments:
            if fragment not in text:
                failures.append(f"{relative_path} is missing required text: {fragment}")
    return failures


def validate_generated_dist(dist: Path, version: str) -> list[str]:
    failures: list[str] = []
    required_files = {
        f"cavra-{version}-SHA256SUMS.txt": "checksum manifest",
        f"cavra-{version}.sbom.spdx.json": "SPDX SBOM",
        f"cavra-{version}.provenance.json": "SLSA/in-toto provenance",
        f"cavra-{version}.release-trust.json": "release trust evidence",
    }
    for file_name, label in required_files.items():
        if not (dist / file_name).exists():
            failures.append(f"missing {label}: {dist / file_name}")

    if failures:
        return failures

    checksums = (dist / f"cavra-{version}-SHA256SUMS.txt").read_text(encoding="utf-8")
    if "cavra-" not in checksums:
        failures.append("checksum manifest does not list CAVRA release artifacts")

    sbom = read_json(dist / f"cavra-{version}.sbom.spdx.json")
    if sbom.get("spdxVersion") != "SPDX-2.3":
        failures.append("SBOM must use SPDX-2.3")
    if not sbom.get("files"):
        failures.append("SBOM must enumerate release artifacts")

    provenance = read_json(dist / f"cavra-{version}.provenance.json")
    if provenance.get("_type") != "https://in-toto.io/Statement/v1":
        failures.append("provenance must be an in-toto statement")
    if provenance.get("predicateType") != "https://slsa.dev/provenance/v1":
        failures.append("provenance must use SLSA provenance predicate")
    if not provenance.get("subject"):
        failures.append("provenance must include release artifact subjects")

    release_trust = read_json(dist / f"cavra-{version}.release-trust.json")
    if release_trust.get("schema_version") != "cavra.community.release_trust.v1":
        failures.append("release trust evidence has the wrong schema")
    controls = set(release_trust.get("required_controls", []))
    for control in {
        "sha256-checksums",
        "spdx-2.3-sbom",
        "slsa-in-toto-provenance",
        "github-keyless-attestation-workflow",
        "openapi-contract-validation",
        "release-security-validation",
    }:
        if control not in controls:
            failures.append(f"release trust evidence missing control: {control}")
    return failures


def validate_openapi_contract() -> list[str]:
    result = subprocess.run(
        ["python3", "scripts/validate_openapi_contract.py"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        return []
    output = result.stdout + result.stderr
    return [f"OpenAPI contract validation failed:\n{output.strip()}"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dist", type=Path)
    parser.add_argument("--version", default="1.0.0")
    args = parser.parse_args()

    failures = validate_required_text()
    failures.extend(validate_openapi_contract())
    if args.dist is not None:
        failures.extend(validate_generated_dist(args.dist, args.version))

    if failures:
        raise SystemExit("\n".join(failures))
    print("release trust gate validated")


if __name__ == "__main__":
    main()
