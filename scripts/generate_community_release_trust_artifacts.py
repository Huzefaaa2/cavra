from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


GENERATED_SUFFIXES = (
    "-SHA256SUMS.txt",
    ".provenance.json",
    ".sbom.spdx.json",
    ".release-trust.json",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_version(pyproject: Path) -> str:
    in_project = False
    for line in pyproject.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped == "[project]":
            in_project = True
            continue
        if in_project and stripped.startswith("["):
            break
        if in_project:
            match = re.match(r'version\s*=\s*"([^"]+)"', stripped)
            if match:
                return match.group(1)
    raise SystemExit(f"could not find [project] version in {pyproject}")


def collect_release_artifacts(dist: Path) -> list[dict[str, Any]]:
    artifacts: list[dict[str, Any]] = []
    for path in sorted(dist.iterdir()):
        if not path.is_file():
            continue
        if path.name.endswith(GENERATED_SUFFIXES):
            continue
        artifacts.append(
            {
                "file_name": path.name,
                "sha256": sha256_file(path),
                "size_bytes": path.stat().st_size,
            }
        )
    if not artifacts:
        raise SystemExit(f"no release artifacts found in {dist}")
    return artifacts


def write_json(path: Path, payload: dict[str, Any]) -> Path:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def write_checksums(dist: Path, version: str, artifacts: list[dict[str, Any]]) -> Path:
    path = dist / f"cavra-{version}-SHA256SUMS.txt"
    lines = [f"{artifact['sha256']}  {artifact['file_name']}" for artifact in artifacts]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def write_sbom(
    dist: Path,
    *,
    version: str,
    repository: str,
    commit: str,
    artifacts: list[dict[str, Any]],
) -> Path:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    return write_json(
        dist / f"cavra-{version}.sbom.spdx.json",
        {
            "spdxVersion": "SPDX-2.3",
            "dataLicense": "CC0-1.0",
            "SPDXID": "SPDXRef-DOCUMENT",
            "name": f"CAVRA Community {version} SBOM",
            "documentNamespace": f"https://github.com/{repository}/releases/community-v{version}/sbom/{commit}",
            "creationInfo": {
                "created": now,
                "creators": ["Tool: CAVRA Community release trust artifact generator"],
            },
            "packages": [
                {
                    "SPDXID": "SPDXRef-Package-CAVRA-Community",
                    "name": "cavra",
                    "versionInfo": version,
                    "downloadLocation": "NOASSERTION",
                    "filesAnalyzed": True,
                    "licenseConcluded": "BUSL-1.1",
                    "licenseDeclared": "BUSL-1.1",
                    "copyrightText": "NOASSERTION",
                    "externalRefs": [
                        {
                            "referenceCategory": "OTHER",
                            "referenceType": "commit",
                            "referenceLocator": commit,
                        }
                    ],
                }
            ],
            "files": [
                {
                    "SPDXID": f"SPDXRef-File-{index}",
                    "fileName": artifact["file_name"],
                    "checksums": [
                        {
                            "algorithm": "SHA256",
                            "checksumValue": artifact["sha256"],
                        }
                    ],
                }
                for index, artifact in enumerate(artifacts)
            ],
            "relationships": [
                {
                    "spdxElementId": "SPDXRef-Package-CAVRA-Community",
                    "relationshipType": "CONTAINS",
                    "relatedSpdxElement": f"SPDXRef-File-{index}",
                }
                for index, _artifact in enumerate(artifacts)
            ],
        },
    )


def write_provenance(
    dist: Path,
    *,
    version: str,
    repository: str,
    commit: str,
    ref: str,
    run_id: str,
    artifacts: list[dict[str, Any]],
) -> Path:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    subjects = [
        {
            "name": artifact["file_name"],
            "digest": {"sha256": artifact["sha256"]},
        }
        for artifact in artifacts
    ]
    return write_json(
        dist / f"cavra-{version}.provenance.json",
        {
            "_type": "https://in-toto.io/Statement/v1",
            "subject": subjects,
            "predicateType": "https://slsa.dev/provenance/v1",
            "predicate": {
                "buildDefinition": {
                    "buildType": "https://github.com/Huzefaaa2/cavra/.github/workflows/release-community.yml",
                    "externalParameters": {
                        "ref": ref,
                        "repository": repository,
                        "version": version,
                    },
                    "internalParameters": {
                        "run_id": run_id,
                    },
                    "resolvedDependencies": [
                        {
                            "uri": f"git+https://github.com/{repository}",
                            "digest": {"gitCommit": commit},
                        }
                    ],
                },
                "runDetails": {
                    "builder": {
                        "id": f"https://github.com/{repository}/actions/runs/{run_id}" if run_id else "",
                    },
                    "metadata": {
                        "invocationId": run_id,
                        "startedOn": now,
                        "finishedOn": now,
                    },
                },
            },
        },
    )


def write_release_trust(
    dist: Path,
    *,
    version: str,
    repository: str,
    commit: str,
    ref: str,
    run_id: str,
    artifacts: list[dict[str, Any]],
    generated_files: list[Path],
) -> Path:
    generated = [
        {
            "file_name": path.name,
            "sha256": sha256_file(path),
            "size_bytes": path.stat().st_size,
        }
        for path in generated_files
    ]
    return write_json(
        dist / f"cavra-{version}.release-trust.json",
        {
            "schema_version": "cavra.community.release_trust.v1",
            "product": "CAVRA Community",
            "version": version,
            "repository": repository,
            "commit": commit,
            "ref": ref,
            "run_id": run_id,
            "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            "status": "ready_for_attestation",
            "release_artifacts": artifacts,
            "trust_artifacts": generated,
            "required_controls": [
                "sha256-checksums",
                "spdx-2.3-sbom",
                "slsa-in-toto-provenance",
                "github-keyless-attestation-workflow",
                "openapi-contract-validation",
                "release-security-validation",
            ],
            "next_gate": "Attest Community Release workflow signs release assets with GitHub keyless attestation.",
        },
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dist", type=Path, default=Path("dist"))
    parser.add_argument("--pyproject", type=Path, default=Path("pyproject.toml"))
    args = parser.parse_args()

    dist = args.dist
    dist.mkdir(parents=True, exist_ok=True)
    version = load_version(args.pyproject)
    repository = os.environ.get("GITHUB_REPOSITORY", "Huzefaaa2/cavra")
    commit = os.environ.get("GITHUB_SHA", "local")
    ref = os.environ.get("GITHUB_REF", "local")
    run_id = os.environ.get("GITHUB_RUN_ID", "local")

    artifacts = collect_release_artifacts(dist)
    checksums = write_checksums(dist, version, artifacts)
    sbom = write_sbom(
        dist,
        version=version,
        repository=repository,
        commit=commit,
        artifacts=artifacts,
    )
    provenance = write_provenance(
        dist,
        version=version,
        repository=repository,
        commit=commit,
        ref=ref,
        run_id=run_id,
        artifacts=artifacts,
    )
    release_trust = write_release_trust(
        dist,
        version=version,
        repository=repository,
        commit=commit,
        ref=ref,
        run_id=run_id,
        artifacts=artifacts,
        generated_files=[checksums, sbom, provenance],
    )
    print(
        "Community release trust artifacts written: "
        f"{checksums.name}, {sbom.name}, {provenance.name}, {release_trust.name}"
    )


if __name__ == "__main__":
    main()
