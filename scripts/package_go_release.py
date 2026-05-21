from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SIGNING_ENV = "CAVRA_GO_RELEASE_SIGNING_KEY"
GO_TARGETS = [
    "linux/amd64",
    "linux/arm64",
    "darwin/amd64",
    "darwin/arm64",
    "windows/amd64",
    "windows/arm64",
]


@dataclass(frozen=True)
class Artifact:
    path: Path
    relative_path: str
    sha256: str
    size_bytes: int
    kind: str


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, payload: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def load_go_modules(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    decoder = json.JSONDecoder()
    text = path.read_text(encoding="utf-8")
    index = 0
    modules: list[dict[str, Any]] = []
    while index < len(text):
        while index < len(text) and text[index].isspace():
            index += 1
        if index >= len(text):
            break
        item, index = decoder.raw_decode(text, index)
        if isinstance(item, dict):
            modules.append(item)
    return modules


def collect_artifacts(dist: Path) -> list[Artifact]:
    artifacts: list[Artifact] = []
    for path in sorted((dist / "bin").glob("*")):
        if path.is_file():
            artifacts.append(_artifact(dist, path, "go-binary"))
    installer_metadata = dist / "cavra-runtime.installers.json"
    if installer_metadata.exists():
        artifacts.append(_artifact(dist, installer_metadata, "installer-metadata"))
    endpoint_deployment = dist / "cavra-runtime.endpoint-deployment.json"
    if endpoint_deployment.exists():
        artifacts.append(_artifact(dist, endpoint_deployment, "managed-endpoint-deployment"))
    ci_runner_bundles = dist / "cavra-runtime.ci-runner-bundles.json"
    if ci_runner_bundles.exists():
        artifacts.append(_artifact(dist, ci_runner_bundles, "ci-runner-bundles"))
    for path in sorted((dist / "ci-runners").glob("**/*")):
        if path.is_file():
            artifacts.append(_artifact(dist, path, "ci-runner-wrapper"))
    channels = dist / "cavra-runtime.channels.json"
    if channels.exists():
        artifacts.append(_artifact(dist, channels, "release-channel-manifest"))
    updater_policy = dist / "cavra-runtime.updater-policy.json"
    if updater_policy.exists():
        artifacts.append(_artifact(dist, updater_policy, "updater-policy"))
    for path in sorted(dist.glob("*.spdx.json")):
        artifacts.append(_artifact(dist, path, "sbom"))
    bootstrap = dist / "offline-trust-root-bootstrap.json"
    if bootstrap.exists():
        artifacts.append(_artifact(dist, bootstrap, "offline-trust-bootstrap"))
    modules = dist / "go-modules.json"
    if modules.exists():
        artifacts.append(_artifact(dist, modules, "go-modules"))
    return artifacts


def _artifact(dist: Path, path: Path, kind: str) -> Artifact:
    return Artifact(
        path=path,
        relative_path=path.relative_to(dist).as_posix(),
        sha256=sha256_file(path),
        size_bytes=path.stat().st_size,
        kind=kind,
    )


def write_spdx_sbom(dist: Path, version: str, commit: str, modules: list[dict[str, Any]]) -> Path:
    now = datetime.now(timezone.utc).isoformat()
    packages = [
        {
            "SPDXID": "SPDXRef-Package-CAVRA-Go-Runtime",
            "name": "cavra-runtime",
            "versionInfo": version,
            "downloadLocation": "NOASSERTION",
            "filesAnalyzed": False,
            "licenseConcluded": "NOASSERTION",
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
    ]
    relationships = []
    for index, module in enumerate(modules):
        spdx_id = f"SPDXRef-GoModule-{index}"
        packages.append(
            {
                "SPDXID": spdx_id,
                "name": str(module.get("Path", "unknown")),
                "versionInfo": str(module.get("Version", "main")),
                "downloadLocation": "NOASSERTION",
                "filesAnalyzed": False,
                "licenseConcluded": "NOASSERTION",
                "licenseDeclared": "NOASSERTION",
                "copyrightText": "NOASSERTION",
            }
        )
        relationships.append(
            {
                "spdxElementId": "SPDXRef-Package-CAVRA-Go-Runtime",
                "relationshipType": "DEPENDS_ON",
                "relatedSpdxElement": spdx_id,
            }
        )
    return write_json(
        dist / "cavra-runtime.sbom.spdx.json",
        {
            "spdxVersion": "SPDX-2.3",
            "dataLicense": "CC0-1.0",
            "SPDXID": "SPDXRef-DOCUMENT",
            "name": f"CAVRA Go Runtime {version}",
            "documentNamespace": f"https://github.com/Huzefaaa2/cavra/releases/{version}/go-runtime/{commit}",
            "creationInfo": {"created": now, "creators": ["Tool: CAVRA Go release packaging"]},
            "packages": packages,
            "relationships": relationships,
        },
    )


def write_offline_trust_bootstrap(
    dist: Path,
    *,
    version: str,
    commit: str,
    ref: str,
    repository: str,
    key_id: str,
) -> Path:
    return write_json(
        dist / "offline-trust-root-bootstrap.json",
        {
            "schema_version": "cavra.offline-trust-bootstrap.v1",
            "product": "CAVRA",
            "component": "go-enforcement-plane",
            "version": version,
            "commit": commit,
            "ref": ref,
            "repository": repository,
            "mode": "air_gapped",
            "release_package": f"cavra-go-runtime-{version}.zip",
            "signature_key_id": key_id,
            "required_files": [
                "checksums.txt",
                "cavra-runtime.endpoint-deployment.json",
                "cavra-runtime.ci-runner-bundles.json",
                "cavra-runtime.installers.json",
                "cavra-runtime.channels.json",
                "cavra-runtime.updater-policy.json",
                "cavra-runtime.sbom.spdx.json",
                "cavra-runtime.provenance.intoto.json",
                "release-evidence.json",
                "release-evidence.md",
                "offline-trust-root-bootstrap.json",
            ],
            "verification_commands": [
                f"cavra release verify-airgap-bundle cavra-go-runtime-{version}.zip",
                f"cavra release verify-go-package go-runtime-{version}",
            ],
            "offline_operator_notes": [
                "Transfer the zip and published public trust material through an approved removable-media process.",
                "Run verification before placing binaries on developer machines, CI runners, or restricted networks.",
                "Use the endpoint deployment manifest to map signed binaries to approved managed endpoint channels.",
                "Preserve release evidence, checksums, provenance, signatures, and this bootstrap manifest with the change record.",
            ],
        },
    )


def write_installer_metadata(dist: Path, *, version: str, commit: str, repository: str) -> Path:
    generated_at = datetime.now(timezone.utc).isoformat()
    targets: list[dict[str, Any]] = []
    for binary in sorted((dist / "bin").glob("*")):
        if not binary.is_file():
            continue
        target = _binary_target(binary.name)
        install_path = (
            "%ProgramFiles%\\CAVRA\\cavra-runtime.exe"
            if target["os"] == "windows"
            else "/usr/local/bin/cavra-runtime"
        )
        install_command = (
            f'copy /Y "{binary.name}" "{install_path}"'
            if target["os"] == "windows"
            else f"install -m 0755 {binary.name} {install_path}"
        )
        targets.append(
            {
                "target": f"{target['os']}/{target['arch']}",
                "os": target["os"],
                "arch": target["arch"],
                "binary": binary.relative_to(dist).as_posix(),
                "binary_sha256": sha256_file(binary),
                "size_bytes": binary.stat().st_size,
                "install_method": "manual-binary",
                "install_path": install_path,
                "install_command": install_command,
                "verification_command": "sha256sum -c checksums.txt",
            }
        )
    return write_json(
        dist / "cavra-runtime.installers.json",
        {
            "schema_version": "cavra.go-runtime.installers.v1",
            "product": "CAVRA",
            "component": "go-enforcement-plane",
            "version": version,
            "commit": commit,
            "repository": repository,
            "generated_at": generated_at,
            "targets": targets,
            "operator_notes": [
                "Verify this installer metadata through checksums, SLSA provenance, and detached signatures before installation.",
                "Install only the binary matching the target operating system and architecture.",
                "Preserve this metadata with the change record for developer workstations, CI runners, and restricted networks.",
            ],
        },
    )


def write_ci_runner_bundle_metadata(dist: Path, *, version: str, commit: str, repository: str, repo_root: Path) -> Path:
    generated_at = datetime.now(timezone.utc).isoformat()
    wrappers_dir = dist / "ci-runners"
    github_action_dir = wrappers_dir / "github-action"
    wrappers_dir.mkdir(parents=True, exist_ok=True)
    github_action_dir.mkdir(parents=True, exist_ok=True)

    runner_source = repo_root / "examples" / "ci-runners" / "cavra-release-governance-runner.sh"
    action_source = (
        repo_root
        / "examples"
        / "github-actions"
        / "actions"
        / "cavra-release-governance-go-runtime"
        / "action.yml"
    )
    runner_script = wrappers_dir / "cavra-release-governance-runner.sh"
    github_action = github_action_dir / "action.yml"
    shutil.copy2(runner_source, runner_script)
    shutil.copy2(action_source, github_action)
    runner_script.chmod(0o755)

    installers = json.loads((dist / "cavra-runtime.installers.json").read_text(encoding="utf-8"))
    linux_amd64 = next(
        (
            target
            for target in installers.get("targets", [])
            if isinstance(target, dict) and target.get("target") == "linux/amd64"
        ),
        {},
    )
    runtime_binary = str(linux_amd64.get("binary", "bin/cavra-runtime_<version>_linux_amd64"))
    runtime_binary_sha256 = str(linux_amd64.get("binary_sha256", ""))

    return write_json(
        dist / "cavra-runtime.ci-runner-bundles.json",
        {
            "schema_version": "cavra.go-runtime.ci-runner-bundles.v1",
            "product": "CAVRA",
            "component": "go-enforcement-plane",
            "version": version,
            "commit": commit,
            "repository": repository,
            "generated_at": generated_at,
            "source_metadata": "cavra-runtime.endpoint-deployment.json",
            "runner_script": {
                "path": "ci-runners/cavra-release-governance-runner.sh",
                "sha256": sha256_file(runner_script),
                "required_environment": [
                    "CAVRA_RUNTIME_PATH",
                    "CAVRA_RELEASE_GOVERNANCE_REQUEST",
                    "CAVRA_EXPECTED_DECISION",
                    "CAVRA_EXPECTED_RULE_ID",
                    "CAVRA_RELEASE_GOVERNANCE_EVIDENCE_DIR",
                ],
            },
            "github_action": {
                "path": "ci-runners/github-action/action.yml",
                "sha256": sha256_file(github_action),
            },
            "runner_bundles": [
                _ci_runner_bundle(
                    platform="GitHub Actions",
                    target_id="github-actions-linux-amd64-runner",
                    binary=runtime_binary,
                    binary_sha256=runtime_binary_sha256,
                    reusable_wrapper="ci-runners/github-action/action.yml",
                    invocation="uses: ./ci-runners/github-action",
                ),
                _ci_runner_bundle(
                    platform="GitLab CI",
                    target_id="gitlab-linux-amd64-runner",
                    binary=runtime_binary,
                    binary_sha256=runtime_binary_sha256,
                    reusable_wrapper="ci-runners/cavra-release-governance-runner.sh",
                    invocation="bash ci-runners/cavra-release-governance-runner.sh",
                ),
                _ci_runner_bundle(
                    platform="Azure Pipelines",
                    target_id="azure-linux-amd64-runner",
                    binary=runtime_binary,
                    binary_sha256=runtime_binary_sha256,
                    reusable_wrapper="ci-runners/cavra-release-governance-runner.sh",
                    invocation="bash ci-runners/cavra-release-governance-runner.sh",
                ),
            ],
            "controls": [
                "verified-signed-runtime-before-runner-use",
                "typed-release-governance-request-required",
                "daemon-evidence-artifacts-published",
                "blocking-decision-fails-closed-by-default",
                "runner-wrapper-included-in-signed-release-package",
            ],
            "operator_steps": [
                "Verify the Go runtime release package before copying the runtime binary or runner wrappers into CI.",
                "Install only the signed runtime binary referenced by this manifest for the runner operating system and architecture.",
                "Set CAVRA_RELEASE_GOVERNANCE_REQUEST to a reviewed typed release-governance request JSON file.",
                "Publish the daemon evidence directory as a CI artifact for audit and release change records.",
            ],
        },
    )


def _ci_runner_bundle(
    *,
    platform: str,
    target_id: str,
    binary: str,
    binary_sha256: str,
    reusable_wrapper: str,
    invocation: str,
) -> dict[str, Any]:
    return {
        "platform": platform,
        "deployment_target": target_id,
        "runner_os": "linux",
        "runner_arch": "amd64",
        "runtime_binary": binary,
        "runtime_binary_sha256": binary_sha256,
        "runtime_path": "./cavra-runtime",
        "reusable_wrapper": reusable_wrapper,
        "invocation": invocation,
        "default_request": "examples/go-runtime/typed-release-governance/approved-promotion.json",
        "evidence_dir": ".cavra/go-daemon",
        "verification_commands": [
            "cavra release verify-go-package .",
            "sha256sum -c checksums.txt",
            "gh attestation verify cavra-go-runtime-<version>.zip --repo Huzefaaa2/cavra",
        ],
        "required_outputs": [
            ".cavra/go-daemon/release-governance-response.json",
            ".cavra/go-daemon/release-governance-evidence.jsonl",
        ],
    }


def write_managed_endpoint_deployment(dist: Path, *, version: str, commit: str, repository: str) -> Path:
    generated_at = datetime.now(timezone.utc).isoformat()
    installers_path = dist / "cavra-runtime.installers.json"
    installers = json.loads(installers_path.read_text(encoding="utf-8")) if installers_path.exists() else {}
    installer_targets = {
        str(target.get("target")): target
        for target in installers.get("targets", [])
        if isinstance(target, dict) and target.get("target")
    }
    deployments: list[dict[str, Any]] = []
    for template in _endpoint_deployment_templates():
        installer = installer_targets.get(template["installer_target"])
        if not installer:
            continue
        deployment = {
            "id": template["id"],
            "surface": template["surface"],
            "platform": template["platform"],
            "os": installer["os"],
            "arch": installer["arch"],
            "installer_target": template["installer_target"],
            "binary": installer["binary"],
            "binary_sha256": installer["binary_sha256"],
            "install_path": installer["install_path"],
            "install_command": installer["install_command"],
            "deployment_channel": template["deployment_channel"],
            "management_tool": template["management_tool"],
            "rollout_gate": "signed-package-verified-and-change-approved",
            "verification_commands": [
                f"cavra release verify-go-package go-runtime-{version}",
                f"cavra release smoke-installers go-runtime-{version} --skip-execution",
                "sha256sum -c checksums.txt",
            ],
            "rollback_steps": [
                "Pause the endpoint management rollout.",
                "Restore the previous signed CAVRA runtime package approved by change control.",
                "Run cavra release verify-go-package against the restored package before returning endpoints to service.",
            ],
            "evidence_required": [
                "release-evidence.json",
                "cavra-runtime.provenance.intoto.json",
                "cavra-runtime.installers.json",
                "cavra-runtime.endpoint-deployment.json",
                "checksums.txt",
            ],
        }
        deployments.append(deployment)
    if not deployments:
        for installer in installer_targets.values():
            target_name = str(installer["target"])
            deployments.append(
                {
                    "id": f"managed-endpoint-{target_name.replace('/', '-')}",
                    "surface": "managed-endpoint",
                    "platform": "Generic managed endpoint channel",
                    "os": installer["os"],
                    "arch": installer["arch"],
                    "installer_target": target_name,
                    "binary": installer["binary"],
                    "binary_sha256": installer["binary_sha256"],
                    "install_path": installer["install_path"],
                    "install_command": installer["install_command"],
                    "deployment_channel": "approved-endpoint-management-tool",
                    "management_tool": "Enterprise endpoint management platform",
                    "rollout_gate": "signed-package-verified-and-change-approved",
                    "verification_commands": [
                        f"cavra release verify-go-package go-runtime-{version}",
                        f"cavra release smoke-installers go-runtime-{version} --skip-execution",
                        "sha256sum -c checksums.txt",
                    ],
                    "rollback_steps": [
                        "Pause the endpoint management rollout.",
                        "Restore the previous signed CAVRA runtime package approved by change control.",
                    ],
                    "evidence_required": [
                        "release-evidence.json",
                        "cavra-runtime.provenance.intoto.json",
                        "cavra-runtime.installers.json",
                        "cavra-runtime.endpoint-deployment.json",
                        "checksums.txt",
                    ],
                }
            )
    return write_json(
        dist / "cavra-runtime.endpoint-deployment.json",
        {
            "schema_version": "cavra.go-runtime.endpoint-deployment.v1",
            "product": "CAVRA",
            "component": "go-enforcement-plane",
            "version": version,
            "commit": commit,
            "repository": repository,
            "generated_at": generated_at,
            "source_metadata": "cavra-runtime.installers.json",
            "controls": [
                "verify-go-package-before-install",
                "smoke-installers-before-rollout",
                "signed-endpoint-deployment-manifest",
                "managed-endpoint-change-record",
                "least-privilege-runner-install",
                "staged-workstation-rollout",
            ],
            "deployment_targets": deployments,
            "operator_steps": [
                "Verify the release package and endpoint deployment manifest before rollout.",
                "Run installer smoke validation in the release staging environment.",
                "Publish only the target-specific binary referenced by this manifest to each endpoint management channel.",
                "Roll out to a limited runner or workstation ring before enterprise-wide deployment.",
                "Preserve package evidence, endpoint deployment metadata, and rollout records with the change ticket.",
            ],
        },
    )


def write_release_channels_and_updater_policy(dist: Path, *, version: str, commit: str, repository: str) -> tuple[Path, Path]:
    generated_at = datetime.now(timezone.utc).isoformat()
    endpoint_deployment = json.loads((dist / "cavra-runtime.endpoint-deployment.json").read_text(encoding="utf-8"))
    workstation_targets = [
        target
        for target in endpoint_deployment.get("deployment_targets", [])
        if isinstance(target, dict) and target.get("surface") == "developer-workstation"
    ]
    if not workstation_targets:
        workstation_targets = [
            target
            for target in endpoint_deployment.get("deployment_targets", [])
            if isinstance(target, dict) and target.get("surface") != "ci-runner"
        ]
    channels = [_channel_manifest(channel, version, commit, workstation_targets) for channel in _release_channels()]
    updater_policy = {
        "schema_version": "cavra.go-runtime.updater-policy.v1",
        "product": "CAVRA",
        "component": "go-enforcement-plane",
        "version": version,
        "commit": commit,
        "repository": repository,
        "generated_at": generated_at,
        "source_channel_manifest": "cavra-runtime.channels.json",
        "default_auto_update": False,
        "controls": [
            "manual-approval-before-auto-update",
            "verify-go-package-before-update",
            "smoke-installers-before-update",
            "staged-workstation-rollout",
            "rollback-package-required",
            "evidence-retention-required",
        ],
        "policies": [
            _updater_channel_policy("canary", max_first_ring_percent=2, soak_hours=4),
            _updater_channel_policy("beta", max_first_ring_percent=10, soak_hours=24),
            _updater_channel_policy("stable", max_first_ring_percent=25, soak_hours=48),
        ],
        "operator_steps": [
            "Verify the release package before publishing a channel manifest.",
            "Approve the channel update in change control before enabling endpoint management rollout.",
            "Roll out canary or beta before stable unless emergency change control approves a direct stable release.",
            "Retain channel manifest, updater policy, delivery evidence, and rollback package references with the release change.",
        ],
    }
    updater_policy_path = write_json(dist / "cavra-runtime.updater-policy.json", updater_policy)
    channel_manifest_path = write_json(
        dist / "cavra-runtime.channels.json",
        {
            "schema_version": "cavra.go-runtime.channels.v1",
            "product": "CAVRA",
            "component": "go-enforcement-plane",
            "version": version,
            "commit": commit,
            "repository": repository,
            "generated_at": generated_at,
            "source_metadata": "cavra-runtime.endpoint-deployment.json",
            "updater_policy": "cavra-runtime.updater-policy.json",
            "channels": channels,
            "operator_notes": [
                "Publish channel manifests only after package verification and change approval.",
                "Managed workstation updaters must not auto-apply CAVRA runtime changes without this policy and approval evidence.",
                "Each channel references signed package artifacts and rollback requirements.",
            ],
        },
    )
    return channel_manifest_path, updater_policy_path


def _release_channels() -> list[dict[str, Any]]:
    return [
        {"channel": "canary", "ring_order": ["security-pilot"], "recommended": False},
        {"channel": "beta", "ring_order": ["platform-pilot", "engineering-pilot"], "recommended": False},
        {"channel": "stable", "ring_order": ["pilot", "broad", "enterprise"], "recommended": True},
    ]


def _channel_manifest(channel: dict[str, Any], version: str, commit: str, targets: list[dict[str, Any]]) -> dict[str, Any]:
    channel_name = str(channel["channel"])
    return {
        "channel": channel_name,
        "version": version,
        "commit": commit,
        "recommended": bool(channel.get("recommended")),
        "ring_order": channel.get("ring_order", []),
        "auto_update": False,
        "approval_required": True,
        "updater_policy_ref": f"cavra-runtime.updater-policy.json#{channel_name}",
        "controls": [
            "verify-go-package-before-channel-publish",
            "smoke-installers-before-channel-publish",
            "approval-required-before-workstation-update",
            "rollback-package-reference-required",
        ],
        "workstation_targets": [
            {
                "id": target.get("id"),
                "platform": target.get("platform"),
                "os": target.get("os"),
                "arch": target.get("arch"),
                "installer_target": target.get("installer_target"),
                "binary": target.get("binary"),
                "binary_sha256": target.get("binary_sha256"),
                "deployment_channel": target.get("deployment_channel"),
                "management_tool": target.get("management_tool"),
            }
            for target in targets
        ],
        "verification_commands": [
            "cavra release verify-go-package .",
            "cavra release smoke-installers . --skip-execution",
            f"cavra release channel-manifest . --channel {channel_name}",
        ],
        "rollback": {
            "required": True,
            "strategy": "restore-previous-signed-package",
            "approval": "release_rollback_endpoint_rollout",
        },
    }


def _updater_channel_policy(channel: str, *, max_first_ring_percent: int, soak_hours: int) -> dict[str, Any]:
    return {
        "channel": channel,
        "auto_update": False,
        "approval_required": True,
        "minimum_approval": "change-approved",
        "rollout_rings": [
            {"ring": "pilot", "max_percentage": max_first_ring_percent, "soak_hours": soak_hours},
            {"ring": "broad", "max_percentage": 50, "soak_hours": soak_hours * 2},
            {"ring": "enterprise", "max_percentage": 100, "soak_hours": soak_hours * 3},
        ],
        "hold_conditions": [
            "package verification failed",
            "installer smoke validation failed",
            "rollback package unavailable",
            "critical connector delivery alert active",
        ],
        "rollback": {
            "required": True,
            "max_minutes_to_pause": 15,
            "evidence": ["rollback execution record", "previous signed package verification"],
        },
    }


def _endpoint_deployment_templates() -> list[dict[str, str]]:
    return [
        {
            "id": "github-actions-linux-amd64-runner",
            "surface": "ci-runner",
            "platform": "GitHub Actions self-hosted runner",
            "installer_target": "linux/amd64",
            "deployment_channel": "runner-image-or-bootstrap-script",
            "management_tool": "GitHub Actions runner image pipeline",
        },
        {
            "id": "gitlab-linux-amd64-runner",
            "surface": "ci-runner",
            "platform": "GitLab Runner",
            "installer_target": "linux/amd64",
            "deployment_channel": "runner-image-or-bootstrap-script",
            "management_tool": "GitLab runner image pipeline",
        },
        {
            "id": "azure-linux-amd64-runner",
            "surface": "ci-runner",
            "platform": "Azure Pipelines self-hosted agent",
            "installer_target": "linux/amd64",
            "deployment_channel": "agent-image-or-bootstrap-script",
            "management_tool": "Azure Pipelines agent image pipeline",
        },
        {
            "id": "linux-systemd-amd64-workstation",
            "surface": "developer-workstation",
            "platform": "Linux developer workstation",
            "installer_target": "linux/amd64",
            "deployment_channel": "fleet-management-script",
            "management_tool": "Linux endpoint management",
        },
        {
            "id": "macos-jamf-arm64-workstation",
            "surface": "developer-workstation",
            "platform": "macOS developer workstation",
            "installer_target": "darwin/arm64",
            "deployment_channel": "jamf-policy",
            "management_tool": "Jamf Pro",
        },
        {
            "id": "macos-jamf-amd64-workstation",
            "surface": "developer-workstation",
            "platform": "macOS developer workstation",
            "installer_target": "darwin/amd64",
            "deployment_channel": "jamf-policy",
            "management_tool": "Jamf Pro",
        },
        {
            "id": "windows-intune-amd64-workstation",
            "surface": "developer-workstation",
            "platform": "Windows developer workstation",
            "installer_target": "windows/amd64",
            "deployment_channel": "intune-win32-app",
            "management_tool": "Microsoft Intune",
        },
    ]


def _binary_target(name: str) -> dict[str, str]:
    stem = name.removesuffix(".exe")
    if not stem.startswith("cavra-runtime_"):
        return {"os": "unknown", "arch": "unknown"}
    parts = stem.removeprefix("cavra-runtime_").rsplit("_", 2)
    if len(parts) != 3:
        return {"os": "unknown", "arch": "unknown"}
    return {"os": parts[1], "arch": parts[2]}


def write_checksums(dist: Path, artifacts: list[Artifact]) -> Path:
    path = dist / "checksums.txt"
    lines = [f"{artifact.sha256}  {artifact.relative_path}" for artifact in artifacts]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def write_slsa_provenance(
    dist: Path,
    *,
    version: str,
    commit: str,
    ref: str,
    event: str,
    dry_run: bool,
    signing_required: bool,
    repository: str,
    workflow_ref: str,
    run_id: str,
    run_attempt: str,
    builder_id: str,
    artifacts: list[Artifact],
) -> Path:
    now = datetime.now(timezone.utc).isoformat()
    run_uri = ""
    if repository and run_id:
        run_uri = f"https://github.com/{repository}/actions/runs/{run_id}"
        if run_attempt:
            run_uri = f"{run_uri}/attempts/{run_attempt}"
    payload = {
        "_type": "https://in-toto.io/Statement/v1",
        "subject": [
            {
                "name": artifact.relative_path,
                "digest": {"sha256": artifact.sha256},
            }
            for artifact in artifacts
        ],
        "predicateType": "https://slsa.dev/provenance/v1",
        "predicate": {
            "buildDefinition": {
                "buildType": "https://github.com/Attestations/GitHubActionsWorkflow@v1",
                "externalParameters": {
                    "event": event,
                    "ref": ref,
                    "repository": repository,
                    "version": version,
                    "workflow_ref": workflow_ref,
                },
                "internalParameters": {
                    "dry_run": dry_run,
                    "go_targets": GO_TARGETS,
                    "package_script": "scripts/package_go_release.py",
                    "signing_required": signing_required,
                },
                "resolvedDependencies": [
                    {
                        "uri": f"git+https://github.com/{repository}@{commit}" if repository else f"git:{commit}",
                        "digest": {"gitCommit": commit},
                    },
                    {
                        "uri": "pkg:golang/github.com/Huzefaaa2/cavra/go/cavra-runtime",
                        "digest": {"gitCommit": commit},
                    },
                ],
            },
            "runDetails": {
                "builder": {"id": builder_id},
                "metadata": {
                    "invocationId": run_uri or run_id or "local",
                    "startedOn": now,
                    "finishedOn": now,
                },
            },
        },
    }
    return write_json(dist / "cavra-runtime.provenance.intoto.json", payload)


def sign_artifact(path: Path, dist: Path, private_key_pem: str, *, key_id: str, signer: str) -> dict[str, Any]:
    try:
        from cryptography.hazmat.primitives import serialization
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("Install cryptography to sign Go release artifacts.") from exc

    pem = private_key_pem.replace("\\n", "\n").encode("utf-8")
    private_key = serialization.load_pem_private_key(pem, password=None)
    signature = private_key.sign(path.read_bytes())
    public_key = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    payload = {
        "schema_version": "cavra.go-release.signature.v1",
        "subject": path.relative_to(dist).as_posix(),
        "subject_sha256": sha256_file(path),
        "algorithm": "Ed25519",
        "key_id": key_id,
        "signer": signer,
        "public_key_sha256": hashlib.sha256(public_key).hexdigest(),
        "public_key_pem": public_key.decode("utf-8"),
        "value": base64.b64encode(signature).decode("ascii"),
    }
    signature_path = path.with_name(path.name + ".sig.json")
    write_json(signature_path, payload)
    return {
        "subject": payload["subject"],
        "signature": signature_path.relative_to(dist).as_posix(),
        "algorithm": payload["algorithm"],
        "key_id": key_id,
        "public_key_sha256": payload["public_key_sha256"],
    }


def write_evidence(
    dist: Path,
    *,
    version: str,
    commit: str,
    ref: str,
    event: str,
    signer: str,
    dry_run: bool,
    signing_required: bool,
    artifacts: list[Artifact],
    signatures: list[dict[str, Any]],
) -> Path:
    payload = {
        "schema_version": "cavra.go-release.evidence.v1",
        "product": "CAVRA",
        "component": "go-enforcement-plane",
        "version": version,
        "commit": commit,
        "ref": ref,
        "event": event,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "signer": signer,
        "dry_run": dry_run,
        "signing_required": signing_required,
        "signature_count": len(signatures),
        "artifacts": [artifact.__dict__ | {"path": artifact.relative_path} for artifact in artifacts],
        "signatures": signatures,
        "controls": [
            "reproducible-go-build-flags",
            "sha256-checksums",
            "spdx-sbom",
            "slsa-provenance",
            "ed25519-detached-signatures",
            "signed-installer-metadata",
            "managed-endpoint-deployment-manifests",
            "signed-ci-runner-bundles",
            "release-channel-manifests",
            "managed-workstation-updater-policy",
            "release-evidence-manifest",
        ],
    }
    for item in payload["artifacts"]:
        item.pop("path", None)
    return write_json(dist / "release-evidence.json", payload)


def write_markdown_summary(dist: Path, evidence_path: Path) -> Path:
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    lines = [
        "# CAVRA Go Runtime Release Evidence",
        "",
        f"Version: `{evidence['version']}`",
        f"Commit: `{evidence['commit']}`",
        f"Ref: `{evidence['ref']}`",
        f"Dry run: `{evidence['dry_run']}`",
        f"Signature count: `{evidence['signature_count']}`",
        "",
        "## Artifacts",
        "",
    ]
    for artifact in evidence["artifacts"]:
        lines.append(f"- `{artifact['relative_path']}` `{artifact['sha256']}`")
    lines.extend(["", "## Signatures", ""])
    if evidence["signatures"]:
        for signature in evidence["signatures"]:
            lines.append(f"- `{signature['subject']}` -> `{signature['signature']}`")
    else:
        lines.append("- No signing key was provided for this dry-run package.")
    path = dist / "release-evidence.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def package_release(args: argparse.Namespace) -> None:
    dist = Path(args.dist).resolve()
    dist.mkdir(parents=True, exist_ok=True)
    modules = load_go_modules(dist / "go-modules.json")
    write_spdx_sbom(dist, args.version, args.commit, modules)
    write_installer_metadata(dist, version=args.version, commit=args.commit, repository=args.repository)
    write_managed_endpoint_deployment(dist, version=args.version, commit=args.commit, repository=args.repository)
    write_ci_runner_bundle_metadata(
        dist,
        version=args.version,
        commit=args.commit,
        repository=args.repository,
        repo_root=Path(args.repo_root).resolve(),
    )
    write_release_channels_and_updater_policy(dist, version=args.version, commit=args.commit, repository=args.repository)
    write_offline_trust_bootstrap(
        dist,
        version=args.version,
        commit=args.commit,
        ref=args.ref,
        repository=args.repository,
        key_id=args.key_id,
    )
    artifacts = collect_artifacts(dist)
    provenance = write_slsa_provenance(
        dist,
        version=args.version,
        commit=args.commit,
        ref=args.ref,
        event=args.event,
        dry_run=args.dry_run,
        signing_required=args.signing_required,
        repository=args.repository,
        workflow_ref=args.workflow_ref,
        run_id=args.run_id,
        run_attempt=args.run_attempt,
        builder_id=args.builder_id,
        artifacts=artifacts,
    )
    artifacts.append(_artifact(dist, provenance, "slsa-provenance"))
    checksums = write_checksums(dist, artifacts)
    artifacts.append(_artifact(dist, checksums, "checksums"))

    signing_key = os.environ.get(SIGNING_ENV, "")
    if args.signing_required and not signing_key:
        raise SystemExit(f"{SIGNING_ENV} is required for a signed Go release package")
    signatures: list[dict[str, Any]] = []
    if signing_key:
        for artifact in artifacts:
            signatures.append(sign_artifact(artifact.path, dist, signing_key, key_id=args.key_id, signer=args.signer))
    else:
        write_json(
            dist / "unsigned-dry-run-notice.json",
            {
                "schema_version": "cavra.go-release.unsigned-notice.v1",
                "reason": f"{SIGNING_ENV} was not provided",
                "dry_run": args.dry_run,
            },
        )

    evidence_path = write_evidence(
        dist,
        version=args.version,
        commit=args.commit,
        ref=args.ref,
        event=args.event,
        signer=args.signer,
        dry_run=args.dry_run,
        signing_required=args.signing_required,
        artifacts=artifacts,
        signatures=signatures,
    )
    if signing_key:
        sign_artifact(evidence_path, dist, signing_key, key_id=args.key_id, signer=args.signer)
    write_markdown_summary(dist, evidence_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Package CAVRA Go runtime release evidence.")
    parser.add_argument("--dist", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--ref", required=True)
    parser.add_argument("--event", required=True)
    parser.add_argument("--signer", default="github-actions")
    parser.add_argument("--key-id", default="cavra-go-release")
    parser.add_argument("--repository", default=os.environ.get("GITHUB_REPOSITORY", "Huzefaaa2/cavra"))
    parser.add_argument("--repo-root", default=os.environ.get("GITHUB_WORKSPACE", "."))
    parser.add_argument("--workflow-ref", default=os.environ.get("GITHUB_WORKFLOW_REF", ""))
    parser.add_argument("--run-id", default=os.environ.get("GITHUB_RUN_ID", "local"))
    parser.add_argument("--run-attempt", default=os.environ.get("GITHUB_RUN_ATTEMPT", ""))
    parser.add_argument(
        "--builder-id",
        default=os.environ.get("CAVRA_GO_RELEASE_BUILDER_ID", "https://github.com/actions/runner/github-hosted"),
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--signing-required", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    package_release(parse_args())
