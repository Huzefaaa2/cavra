from __future__ import annotations

import base64
import hashlib
import hmac
import io
import json
import sqlite3
import zipfile
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class EvidenceBundleResult:
    bundle_dir: Path
    manifest_path: Path
    files: list[Path]


@dataclass(frozen=True)
class ExportResult:
    output_dir: Path
    files: list[Path]


EVIDENCE_ARTIFACTS: dict[str, dict[str, str]] = {
    "manifest.json": {
        "kind": "manifest",
        "media_type": "application/json",
        "description": "Evidence bundle manifest with checksums and signature metadata.",
    },
    "evidence.json": {
        "kind": "evidence",
        "media_type": "application/json",
        "description": "Complete CAVRA decision evidence for the session.",
    },
    "pr-attestation.md": {
        "kind": "attestation",
        "media_type": "text/markdown",
        "description": "Reviewer-ready PR attestation for AI-assisted changes.",
    },
    "compliance-mapping.md": {
        "kind": "compliance",
        "media_type": "text/markdown",
        "description": "Control-objective mapping for audit review.",
    },
    "siem-event.json": {
        "kind": "siem",
        "media_type": "application/json",
        "description": "SIEM-ready session event payload.",
    },
    "sandbox-run-summary.json": {
        "kind": "summary",
        "media_type": "application/json",
        "description": "Compact session summary for console and demo workflows.",
    },
    "retention-policy.json": {
        "kind": "retention",
        "media_type": "application/json",
        "description": "Evidence retention, legal hold, and disposition policy.",
    },
}


ROLLOUT_EVIDENCE_ARTIFACTS: dict[str, dict[str, str]] = {
    "managed-endpoint-rollout-evidence.json": {
        "kind": "rollout-evidence",
        "media_type": "application/json",
        "description": "Verified managed endpoint rollout evidence payload.",
    },
    "managed-endpoint-rollout-evidence.md": {
        "kind": "rollout-summary",
        "media_type": "text/markdown",
        "description": "Reviewer-ready managed endpoint rollout evidence summary.",
    },
    "checksums.txt": {
        "kind": "rollout-checksums",
        "media_type": "text/plain",
        "description": "Checksums for allowlisted managed endpoint rollout evidence files.",
    },
}


ENDPOINT_MANAGEMENT_EXPORT_ARTIFACTS: dict[str, dict[str, str]] = {
    "endpoint-management-export-manifest.json": {
        "kind": "endpoint-export-manifest",
        "media_type": "application/json",
        "description": "Endpoint-management export manifest with release, provider, approval, and file metadata.",
    },
    "endpoint-management-export-manifest.md": {
        "kind": "endpoint-export-summary",
        "media_type": "text/markdown",
        "description": "Reviewer-ready endpoint-management export summary.",
    },
    "jamf-policy.json": {
        "kind": "jamf-policy",
        "media_type": "application/json",
        "description": "Jamf import policy for managed CAVRA runtime rollout.",
    },
    "intune-win32-app.json": {
        "kind": "intune-win32-app",
        "media_type": "application/json",
        "description": "Microsoft Intune Win32 app import metadata for managed CAVRA runtime rollout.",
    },
    "linux-fleet-manifest.json": {
        "kind": "linux-fleet-manifest",
        "media_type": "application/json",
        "description": "Linux fleet management manifest for managed CAVRA runtime rollout.",
    },
    "linux-install-cavra-runtime.sh": {
        "kind": "linux-install-script",
        "media_type": "text/x-shellscript",
        "description": "Linux install script for managed CAVRA runtime rollout.",
    },
    "checksums.txt": {
        "kind": "endpoint-export-checksums",
        "media_type": "text/plain",
        "description": "Checksums for allowlisted endpoint-management export files.",
    },
}


class EvidenceArtifactError(ValueError):
    pass


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


def generate_ed25519_keypair(private_key_path: Path, public_key_path: Path) -> tuple[Path, Path]:
    try:
        from cryptography.hazmat.primitives import serialization
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("Install cryptography to use Ed25519 evidence signatures.") from exc

    private_key = Ed25519PrivateKey.generate()
    private_key_path.parent.mkdir(parents=True, exist_ok=True)
    public_key_path.parent.mkdir(parents=True, exist_ok=True)
    private_key_path.write_bytes(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )
    public_key_path.write_bytes(
        private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
    )
    return private_key_path, public_key_path


def public_key_fingerprint(public_key_path: Path) -> str:
    return hashlib.sha256(public_key_path.read_bytes()).hexdigest()


def default_key_id(public_key_path: Path) -> str:
    return public_key_fingerprint(public_key_path)[:16]


def build_key_trust_root(
    public_key_path: Path,
    *,
    key_id: str | None = None,
    owner: str = "platform-security",
    status: str = "active",
    valid_from: str | None = None,
    valid_until: str | None = None,
) -> dict[str, Any]:
    fingerprint = public_key_fingerprint(public_key_path)
    return {
        "schema_version": "cavra.evidence.trust-root.v1",
        "product": "CAVRA",
        "key_id": key_id or fingerprint[:16],
        "owner": owner,
        "status": status,
        "algorithm": "Ed25519",
        "public_key_sha256": fingerprint,
        "public_key_pem": public_key_path.read_text(encoding="utf-8"),
        "valid_from": valid_from or datetime.now(timezone.utc).isoformat(),
        "valid_until": valid_until,
    }


def export_key_trust_root(
    public_key_path: Path,
    output_path: Path,
    *,
    key_id: str | None = None,
    owner: str = "platform-security",
    status: str = "active",
    valid_from: str | None = None,
    valid_until: str | None = None,
) -> Path:
    return write_json(
        output_path,
        build_key_trust_root(
            public_key_path,
            key_id=key_id,
            owner=owner,
            status=status,
            valid_from=valid_from,
            valid_until=valid_until,
        ),
    )


def build_trust_root_bundle(trust_roots: list[Path]) -> dict[str, Any]:
    roots = [json.loads(path.read_text(encoding="utf-8")) for path in trust_roots]
    key_ids = [root.get("key_id") for root in roots]
    duplicates = sorted({key_id for key_id in key_ids if key_id and key_ids.count(key_id) > 1})
    if duplicates:
        raise ValueError(f"duplicate trust-root key IDs: {', '.join(duplicates)}")
    for root in roots:
        if root.get("schema_version") != "cavra.evidence.trust-root.v1":
            raise ValueError(f"invalid trust-root schema for key_id={root.get('key_id', 'unknown')}")
        if root.get("algorithm") != "Ed25519":
            raise ValueError(f"unsupported trust-root algorithm for key_id={root.get('key_id', 'unknown')}")
        if not root.get("key_id"):
            raise ValueError("trust root is missing key_id")
        if not root.get("public_key_pem") or not root.get("public_key_sha256"):
            raise ValueError(f"trust root {root['key_id']} is missing public key material")
    return {
        "schema_version": "cavra.evidence.trust-root-bundle.v1",
        "product": "CAVRA",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "trust_roots": sorted(roots, key=lambda root: str(root.get("key_id"))),
    }


def export_trust_root_bundle(trust_roots: list[Path], output_path: Path) -> Path:
    if not trust_roots:
        raise ValueError("at least one trust root is required")
    return write_json(output_path, build_trust_root_bundle(trust_roots))


def export_trust_root_distribution(
    trust_roots: list[Path],
    output_dir: Path,
    *,
    environment: str = "production",
    distribution_id: str | None = None,
    channels: list[str] | None = None,
) -> ExportResult:
    if not trust_roots:
        raise ValueError("at least one trust root is required")
    output_dir.mkdir(parents=True, exist_ok=True)
    bundle = build_trust_root_bundle(trust_roots)
    created_at = datetime.now(timezone.utc).isoformat()
    distribution_id = distribution_id or f"trust-roots-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
    channels = channels or ["source-control", "secure-portal", "offline-transfer"]

    bundle_path = write_json(output_dir / "evidence-trust-roots.json", bundle)
    manifest = build_trust_root_distribution_manifest(
        bundle,
        distribution_id=distribution_id,
        environment=environment,
        channels=channels,
        created_at=created_at,
        bundle_path=bundle_path,
        output_dir=output_dir,
    )
    manifest_path = write_json(output_dir / "trust-root-distribution-manifest.json", manifest)
    readme_path = output_dir / "trust-root-distribution.md"
    readme_path.write_text(render_trust_root_distribution(manifest), encoding="utf-8")
    checksums_path = output_dir / "checksums.txt"
    checksum_artifacts = [bundle_path, manifest_path, readme_path]
    checksums_path.write_text(
        "\n".join(f"{sha256_file(path)}  {path.relative_to(output_dir).as_posix()}" for path in checksum_artifacts)
        + "\n",
        encoding="utf-8",
    )
    return ExportResult(output_dir, [bundle_path, manifest_path, readme_path, checksums_path])


def build_trust_root_distribution_manifest(
    bundle: dict[str, Any],
    *,
    distribution_id: str,
    environment: str,
    channels: list[str],
    created_at: str,
    bundle_path: Path,
    output_dir: Path,
) -> dict[str, Any]:
    trust_roots = bundle.get("trust_roots", [])
    key_summaries = [
        {
            "key_id": root.get("key_id"),
            "owner": root.get("owner"),
            "status": root.get("status"),
            "algorithm": root.get("algorithm"),
            "public_key_sha256": root.get("public_key_sha256"),
            "valid_from": root.get("valid_from"),
            "valid_until": root.get("valid_until"),
        }
        for root in trust_roots
        if isinstance(root, dict)
    ]
    active_key_ids = sorted(str(root["key_id"]) for root in key_summaries if root.get("status") == "active" and root.get("key_id"))
    retired_key_ids = sorted(str(root["key_id"]) for root in key_summaries if root.get("status") == "retired" and root.get("key_id"))
    revoked_key_ids = sorted(str(root["key_id"]) for root in key_summaries if root.get("status") == "revoked" and root.get("key_id"))
    return {
        "schema_version": "cavra.evidence.trust-root-distribution.v1",
        "product": "CAVRA",
        "distribution_id": distribution_id,
        "environment": environment,
        "created_at": created_at,
        "bundle": {
            "path": bundle_path.relative_to(output_dir).as_posix(),
            "sha256": sha256_file(bundle_path),
            "schema_version": bundle.get("schema_version"),
            "trust_root_count": len(key_summaries),
            "active_key_ids": active_key_ids,
            "retired_key_ids": retired_key_ids,
            "revoked_key_ids": revoked_key_ids,
        },
        "channels": channels,
        "keys": key_summaries,
        "verification_commands": [
            "sha256sum -c checksums.txt",
            "cavra evidence verify .cavra/evidence/latest --trust-root evidence-trust-roots.json",
        ],
        "operator_steps": [
            "Distribute only the public trust-root files in this directory; never include private signing keys.",
            "Verify checksums before importing the bundle into CI, reviewer workstations, API services, or audit tooling.",
            "Publish the updated trust-root distribution before evidence bundles are signed by a new active key.",
            "Retain retired keys for historical evidence verification and remove revoked keys only after incident response approval.",
        ],
    }


def render_trust_root_distribution(manifest: dict[str, Any]) -> str:
    lines = [
        "# CAVRA Trust-Root Distribution",
        "",
        f"Distribution ID: `{manifest['distribution_id']}`",
        f"Environment: `{manifest['environment']}`",
        f"Created at: `{manifest['created_at']}`",
        "",
        "## Bundle",
        "",
        f"- Path: `{manifest['bundle']['path']}`",
        f"- SHA-256: `{manifest['bundle']['sha256']}`",
        f"- Trust roots: `{manifest['bundle']['trust_root_count']}`",
        "",
        "## Active Keys",
        "",
    ]
    active_key_ids = manifest.get("bundle", {}).get("active_key_ids", [])
    if active_key_ids:
        for key_id in active_key_ids:
            lines.append(f"- `{key_id}`")
    else:
        lines.append("- No active keys in this distribution.")
    lines.extend(["", "## Distribution Channels", ""])
    for channel in manifest.get("channels", []):
        lines.append(f"- `{channel}`")
    lines.extend(["", "## Operator Steps", ""])
    for step in manifest.get("operator_steps", []):
        lines.append(f"- {step}")
    lines.extend(["", "## Verification", ""])
    for command in manifest.get("verification_commands", []):
        lines.append(f"```bash\n{command}\n```")
    lines.append("")
    return "\n".join(lines)


def render_pr_attestation(session_id: str, decisions: list[dict[str, Any]]) -> str:
    blocked = [item for item in decisions if item.get("decision") == "block"]
    approvals = [item for item in decisions if item.get("decision") == "require_approval"]
    allowed = [item for item in decisions if item.get("decision") in {"allow", "allow_with_attestation"}]
    lines = [
        "# CAVRA PR Attestation",
        "",
        "Before the agent acts, CAVRA decides.",
        "",
        f"Session: `{session_id}`",
        "",
        "## Summary",
        "",
        f"- Allowed actions: {len(allowed)}",
        f"- Blocked actions: {len(blocked)}",
        f"- Approval-required actions: {len(approvals)}",
        "",
        "## Decisions",
        "",
    ]
    for decision in decisions:
        lines.append(
            f"- `{decision.get('action_type')}` `{decision.get('target')}` -> "
            f"**{decision.get('decision')}** via `{decision.get('rule_id')}`"
        )
    approvals = [item for item in decisions if item.get("approval")]
    if approvals:
        lines.extend(["", "## Approval Outcomes", ""])
        for decision in approvals:
            approval = decision.get("approval", {})
            lines.append(
                f"- `{approval.get('approval_id')}` `{decision.get('target')}` -> "
                f"**{approval.get('state')}** by `{approval.get('decided_by') or approval.get('approver_group')}`"
            )
    lines.extend(
        [
            "",
            "## Reviewer Guidance",
            "",
            "Review blocked and approval-required actions before merge. Attach this attestation to AI-assisted pull requests in regulated repositories.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_compliance_mapping(session_id: str, decisions: list[dict[str, Any]]) -> str:
    return "\n".join(
        [
            "# CAVRA Compliance Mapping",
            "",
            f"Session: `{session_id}`",
            "",
            "| Control objective | CAVRA evidence |",
            "| --- | --- |",
            "| Secret exposure prevention | File read decisions and blocked sensitive path rules |",
            "| Change control | Approval-required decisions and approver groups |",
            "| Least privilege | IAM, cloud, Kubernetes, and MCP control decisions |",
            "| Audit logging | Manifest, checksums, timestamps, rule IDs, and correlation IDs |",
            "| Human oversight | `require_approval` decisions and PR attestation |",
            "",
        ]
    )


def build_siem_event(session_id: str, decisions: list[dict[str, Any]]) -> dict[str, Any]:
    severities = [item.get("severity", "low") for item in decisions]
    blocked = sum(1 for item in decisions if item.get("decision") == "block")
    approvals = sum(1 for item in decisions if item.get("decision") == "require_approval")
    return {
        "event_type": "cavra.evidence_bundle",
        "product": "CAVRA",
        "session_id": session_id,
        "decision_count": len(decisions),
        "blocked_count": blocked,
        "approval_required_count": approvals,
        "max_severity": max(severities, default="low"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "decisions": decisions,
    }


def load_bundle_event(bundle_dir: Path) -> dict[str, Any]:
    path = bundle_dir / "siem-event.json"
    if not path.exists():
        raise FileNotFoundError(f"SIEM event not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def build_splunk_hec_events(event: dict[str, Any], *, index: str = "cavra") -> list[dict[str, Any]]:
    timestamp = _event_epoch(event)
    return [
        {
            "time": timestamp,
            "host": "cavra",
            "source": "cavra:evidence",
            "sourcetype": "cavra:evidence:json",
            "index": index,
            "event": event,
        }
    ]


def build_sentinel_events(event: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "TimeGenerated": event.get("timestamp"),
            "SourceSystem": "CAVRA",
            "EventName": event.get("event_type"),
            "ProductName": event.get("product"),
            "SessionId": event.get("session_id"),
            "DecisionCount": event.get("decision_count", 0),
            "BlockedCount": event.get("blocked_count", 0),
            "ApprovalRequiredCount": event.get("approval_required_count", 0),
            "Severity": _provider_severity(event.get("max_severity", "low"), provider="sentinel"),
            "RawEvent": event,
        }
    ]


def build_datadog_events(event: dict[str, Any], *, service: str = "cavra") -> list[dict[str, Any]]:
    status = _provider_severity(event.get("max_severity", "low"), provider="datadog")
    return [
        {
            "ddsource": "cavra",
            "service": service,
            "status": status,
            "message": (
                f"CAVRA evidence bundle {event.get('session_id')} "
                f"recorded {event.get('decision_count', 0)} decisions, "
                f"{event.get('blocked_count', 0)} blocked, "
                f"{event.get('approval_required_count', 0)} approval-required."
            ),
            "tags": [
                "product:cavra",
                f"session_id:{event.get('session_id')}",
                f"max_severity:{event.get('max_severity', 'low')}",
            ],
            "attributes": event,
        }
    ]


def build_webhook_payload(event: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "cavra.webhook.evidence.v1",
        "product": "CAVRA",
        "event_type": event.get("event_type"),
        "timestamp": event.get("timestamp"),
        "payload": event,
    }


def export_siem_payloads(
    bundle_dir: Path,
    output_dir: Path,
    *,
    provider: str = "all",
    splunk_index: str = "cavra",
    datadog_service: str = "cavra",
) -> ExportResult:
    event = load_bundle_event(bundle_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    providers = {"splunk", "sentinel", "datadog", "webhook"} if provider == "all" else {provider}
    unknown = providers - {"splunk", "sentinel", "datadog", "webhook"}
    if unknown:
        raise ValueError(f"unknown SIEM provider: {', '.join(sorted(unknown))}")

    files: list[Path] = []
    if "splunk" in providers:
        files.append(write_json(output_dir / "splunk-hec-events.json", {"events": build_splunk_hec_events(event, index=splunk_index)}))
    if "sentinel" in providers:
        files.append(write_json(output_dir / "sentinel-log-analytics.json", {"records": build_sentinel_events(event)}))
    if "datadog" in providers:
        files.append(write_json(output_dir / "datadog-events.json", {"events": build_datadog_events(event, service=datadog_service)}))
    if "webhook" in providers:
        files.append(write_json(output_dir / "webhook-payload.json", build_webhook_payload(event)))
    return ExportResult(output_dir, files)


def build_immutable_storage_plan(
    bundle_dir: Path,
    *,
    retention_days: int = 2555,
    s3_bucket: str = "cavra-evidence",
    s3_prefix: str = "evidence/",
    azure_account: str = "cavraevidence",
    azure_container: str = "evidence",
) -> dict[str, Any]:
    manifest = json.loads((bundle_dir / "manifest.json").read_text(encoding="utf-8"))
    files = [
        {
            "path": entry["path"],
            "sha256": entry["sha256"],
            "bytes": entry["bytes"],
            "s3_uri": f"s3://{s3_bucket}/{s3_prefix.rstrip('/')}/{entry['path']}",
            "azure_blob": f"https://{azure_account}.blob.core.windows.net/{azure_container}/{entry['path']}",
        }
        for entry in manifest.get("files", [])
    ]
    return {
        "schema_version": "cavra.immutable-storage-plan.v1",
        "product": "CAVRA",
        "bundle": {
            "manifest_signature": manifest.get("signature"),
            "created_at": manifest.get("created_at"),
            "signer": manifest.get("signer"),
        },
        "retention": {
            "mode": "compliance",
            "retention_days": retention_days,
            "delete_protection": True,
            "legal_hold_supported": True,
        },
        "s3_object_lock": {
            "bucket": s3_bucket,
            "prefix": s3_prefix,
            "object_lock_enabled": True,
            "default_retention_mode": "COMPLIANCE",
            "default_retention_days": retention_days,
            "required_bucket_versioning": True,
            "required_kms_encryption": True,
            "deployment_reference": "examples/immutable-storage/aws-s3-object-lock",
        },
        "azure_immutable_blob": {
            "account": azure_account,
            "container": azure_container,
            "immutability_policy_days": retention_days,
            "allow_protected_append_writes": False,
            "required_versioning": True,
            "required_infrastructure_encryption": True,
            "deployment_reference": "examples/immutable-storage/azure-blob-immutability",
        },
        "files": files,
    }


def render_immutable_storage_plan(plan: dict[str, Any]) -> str:
    lines = [
        "# CAVRA Immutable Evidence Storage Plan",
        "",
        f"Retention mode: `{plan['retention']['mode']}`",
        f"Retention days: `{plan['retention']['retention_days']}`",
        "",
        "## S3 Object Lock",
        "",
        f"- Bucket: `{plan['s3_object_lock']['bucket']}`",
        f"- Prefix: `{plan['s3_object_lock']['prefix']}`",
        "- Object Lock: enabled",
        "- Versioning: required",
        "- KMS encryption: required",
        f"- Deployment reference: `{plan['s3_object_lock']['deployment_reference']}`",
        "",
        "## Azure Immutable Blob",
        "",
        f"- Account: `{plan['azure_immutable_blob']['account']}`",
        f"- Container: `{plan['azure_immutable_blob']['container']}`",
        "- Blob versioning: required",
        "- Infrastructure encryption: required",
        f"- Deployment reference: `{plan['azure_immutable_blob']['deployment_reference']}`",
        "",
        "## Files",
        "",
    ]
    for item in plan.get("files", []):
        lines.append(f"- `{item['path']}` `{item['sha256']}`")
    lines.append("")
    return "\n".join(lines)


def export_immutable_storage_plan(
    bundle_dir: Path,
    output_dir: Path,
    *,
    retention_days: int = 2555,
    s3_bucket: str = "cavra-evidence",
    s3_prefix: str = "evidence/",
    azure_account: str = "cavraevidence",
    azure_container: str = "evidence",
) -> ExportResult:
    output_dir.mkdir(parents=True, exist_ok=True)
    plan = build_immutable_storage_plan(
        bundle_dir,
        retention_days=retention_days,
        s3_bucket=s3_bucket,
        s3_prefix=s3_prefix,
        azure_account=azure_account,
        azure_container=azure_container,
    )
    json_path = write_json(output_dir / "immutable-storage-plan.json", plan)
    markdown_path = output_dir / "immutable-storage-plan.md"
    markdown_path.write_text(render_immutable_storage_plan(plan), encoding="utf-8")
    return ExportResult(output_dir, [json_path, markdown_path])


def build_retention_policy(
    session_id: str,
    *,
    created_at: str,
    retention_days: int = 2555,
    classification: str = "regulated-sdlc",
    legal_hold: bool = False,
) -> dict[str, Any]:
    if retention_days < 1:
        raise ValueError("retention_days must be greater than zero")
    created = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    expires_at = created + timedelta(days=retention_days)
    return {
        "schema_version": "cavra.evidence.retention.v1",
        "product": "CAVRA",
        "session_id": session_id,
        "classification": classification,
        "created_at": created_at,
        "retention_days": retention_days,
        "retain_until": expires_at.isoformat(),
        "legal_hold": legal_hold,
        "delete_protection": True,
        "disposition": "retain" if legal_hold else "eligible_for_review_after_retain_until",
    }


def render_retention_policy(policy: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# CAVRA Evidence Retention Policy",
            "",
            f"Session: `{policy['session_id']}`",
            f"Classification: `{policy['classification']}`",
            f"Retention days: `{policy['retention_days']}`",
            f"Retain until: `{policy['retain_until']}`",
            f"Legal hold: `{policy['legal_hold']}`",
            f"Disposition: `{policy['disposition']}`",
            "",
        ]
    )


def export_retention_policy(
    bundle_dir: Path,
    output_dir: Path,
    *,
    retention_days: int = 2555,
    classification: str = "regulated-sdlc",
    legal_hold: bool = False,
) -> ExportResult:
    evidence_path = bundle_dir / "evidence.json"
    manifest_path = bundle_dir / "manifest.json"
    if not evidence_path.exists():
        raise FileNotFoundError(f"evidence not found: {evidence_path}")
    if not manifest_path.exists():
        raise FileNotFoundError(f"manifest not found: {manifest_path}")
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    policy = build_retention_policy(
        evidence.get("session_id", "unknown"),
        created_at=manifest.get("created_at", datetime.now(timezone.utc).isoformat()),
        retention_days=retention_days,
        classification=classification,
        legal_hold=legal_hold,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = write_json(output_dir / "retention-policy.json", policy)
    markdown_path = output_dir / "retention-policy.md"
    markdown_path.write_text(render_retention_policy(policy), encoding="utf-8")
    return ExportResult(output_dir, [json_path, markdown_path])


def create_evidence_bundle(
    decisions: list[dict[str, Any]],
    destination: Path,
    *,
    session_id: str = "local",
    signer: str = "local",
    key: str | None = None,
    private_key: Path | None = None,
    key_id: str | None = None,
    retention_days: int = 2555,
    classification: str = "regulated-sdlc",
    legal_hold: bool = False,
) -> EvidenceBundleResult:
    destination.mkdir(parents=True, exist_ok=True)
    created_at = datetime.now(timezone.utc).isoformat()
    evidence_path = write_json(
        destination / "evidence.json",
        {
            "product": "CAVRA",
            "tagline": "Before the agent acts, CAVRA decides.",
            "session_id": session_id,
            "created_at": created_at,
            "decisions": decisions,
        },
    )
    attestation_path = destination / "pr-attestation.md"
    attestation_path.write_text(render_pr_attestation(session_id, decisions), encoding="utf-8")
    compliance_path = destination / "compliance-mapping.md"
    compliance_path.write_text(render_compliance_mapping(session_id, decisions), encoding="utf-8")
    siem_path = write_json(destination / "siem-event.json", build_siem_event(session_id, decisions))
    summary_path = write_json(
        destination / "sandbox-run-summary.json",
        {
            "session_id": session_id,
            "created_at": created_at,
            "events": len(decisions),
            "blocked": sum(1 for item in decisions if item.get("decision") == "block"),
            "approval_required": sum(1 for item in decisions if item.get("decision") == "require_approval"),
        },
    )
    retention_path = write_json(
        destination / "retention-policy.json",
        build_retention_policy(
            session_id,
            created_at=created_at,
            retention_days=retention_days,
            classification=classification,
            legal_hold=legal_hold,
        ),
    )
    files = [evidence_path, attestation_path, compliance_path, siem_path, summary_path, retention_path]
    manifest = build_manifest(files, signer=signer, key=key, private_key=private_key, key_id=key_id, created_at=created_at)
    manifest_path = write_json(destination / "manifest.json", manifest)
    return EvidenceBundleResult(destination, manifest_path, [*files, manifest_path])


def build_manifest(
    files: list[Path],
    *,
    signer: str = "local",
    key: str | None = None,
    private_key: Path | None = None,
    key_id: str | None = None,
    created_at: str | None = None,
) -> dict[str, Any]:
    if key and private_key:
        raise ValueError("Use either HMAC key or private key, not both.")
    file_entries = [
        {
            "path": path.name,
            "sha256": sha256_file(path),
            "bytes": path.stat().st_size,
        }
        for path in files
    ]
    manifest_payload = {
        "schema_version": "cavra.evidence.bundle.v1",
        "product": "CAVRA",
        "created_at": created_at or datetime.now(timezone.utc).isoformat(),
        "signer": signer,
        "files": file_entries,
    }
    canonical = json.dumps(manifest_payload, sort_keys=True).encode("utf-8")
    if private_key:
        manifest_payload["signature"] = _sign_manifest_ed25519(canonical, private_key, key_id=key_id)
    elif key:
        signature = hmac.new(key.encode("utf-8"), canonical, hashlib.sha256).digest()
        manifest_payload["signature"] = {
            "algorithm": "HS256",
            "value": base64.b64encode(signature).decode("ascii"),
        }
    else:
        manifest_payload["signature"] = {
            "algorithm": "SHA256",
            "value": hashlib.sha256(canonical).hexdigest(),
        }
    return manifest_payload


def verify_evidence_bundle(
    bundle_dir: Path,
    *,
    key: str | None = None,
    public_key: Path | None = None,
    trust_root: Path | None = None,
    key_id: str | None = None,
    minimum_retention_days: int | None = None,
) -> tuple[bool, list[str]]:
    manifest_path = bundle_dir / "manifest.json"
    if not manifest_path.exists():
        return False, [f"missing manifest: {manifest_path}"]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    errors: list[str] = []
    for entry in manifest.get("files", []):
        path = bundle_dir / entry["path"]
        if not path.exists():
            errors.append(f"missing file: {entry['path']}")
            continue
        actual = sha256_file(path)
        if actual != entry["sha256"]:
            errors.append(f"checksum mismatch: {entry['path']}")
    signature = manifest.get("signature", {})
    unsigned = {key_: value for key_, value in manifest.items() if key_ != "signature"}
    canonical = json.dumps(unsigned, sort_keys=True).encode("utf-8")
    if key:
        expected = base64.b64encode(hmac.new(key.encode("utf-8"), canonical, hashlib.sha256).digest()).decode("ascii")
        if signature.get("value") != expected:
            errors.append("manifest signature mismatch")
    elif public_key:
        try:
            _verify_manifest_ed25519(canonical, signature, public_key, key_id=key_id)
        except ValueError as exc:
            errors.append(str(exc))
    elif trust_root:
        try:
            _verify_manifest_trust_root(canonical, signature, trust_root, key_id=key_id)
        except ValueError as exc:
            errors.append(str(exc))
    elif signature.get("algorithm") == "SHA256":
        expected = hashlib.sha256(canonical).hexdigest()
        if signature.get("value") != expected:
            errors.append("manifest digest mismatch")
    if minimum_retention_days is not None:
        retention_path = bundle_dir / "retention-policy.json"
        if not retention_path.exists():
            errors.append("missing retention policy")
        else:
            retention = json.loads(retention_path.read_text(encoding="utf-8"))
            if retention.get("retention_days", 0) < minimum_retention_days:
                errors.append("retention policy below minimum")
    return not errors, errors


def build_evidence_metadata(bundle_dir: Path) -> dict[str, Any]:
    evidence_path = bundle_dir / "evidence.json"
    manifest_path = bundle_dir / "manifest.json"
    retention_path = bundle_dir / "retention-policy.json"
    if not evidence_path.exists():
        raise FileNotFoundError(f"evidence not found: {evidence_path}")
    if not manifest_path.exists():
        raise FileNotFoundError(f"manifest not found: {manifest_path}")
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    retention = json.loads(retention_path.read_text(encoding="utf-8")) if retention_path.exists() else {}
    decisions = evidence.get("decisions", [])
    approval_outcomes = [item["approval"] for item in decisions if item.get("approval")]
    return {
        "schema_version": "cavra.evidence.metadata.v1",
        "product": "CAVRA",
        "session_id": evidence.get("session_id"),
        "bundle_dir": str(bundle_dir),
        "created_at": evidence.get("created_at") or manifest.get("created_at"),
        "decision_count": len(decisions),
        "blocked_count": sum(1 for item in decisions if item.get("decision") == "block"),
        "approval_required_count": sum(1 for item in decisions if item.get("decision") == "require_approval"),
        "manifest_signature": manifest.get("signature"),
        "signer": manifest.get("signer"),
        "retention": retention,
        "approval_outcomes": approval_outcomes,
        "approved_count": sum(1 for item in approval_outcomes if item.get("state") in {"approved", "break_glass"}),
        "denied_count": sum(1 for item in approval_outcomes if item.get("state") == "denied"),
        "break_glass_count": sum(1 for item in approval_outcomes if item.get("break_glass")),
    }


def list_evidence_artifacts(
    artifact_root: Path,
    session_id: str,
    *,
    metadata: dict[str, Any] | None = None,
    base_path: str = "",
    bundle_path: str = "",
) -> dict[str, Any]:
    session_dir = _evidence_artifact_dir(artifact_root, session_id, metadata)
    descriptors = _evidence_artifact_descriptors(metadata)
    artifacts = []
    for artifact_name, descriptor in descriptors.items():
        path = session_dir / artifact_name
        if not path.exists() or not path.is_file():
            continue
        item = {
            "artifact": artifact_name,
            "kind": descriptor["kind"],
            "description": descriptor["description"],
            "media_type": descriptor["media_type"],
            "bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        }
        if base_path:
            item["download_url"] = f"{base_path.rstrip('/')}/{artifact_name}"
        artifacts.append(item)
    return {
        "schema_version": "cavra.evidence.artifacts.v1",
        "product": "CAVRA",
        "session_id": session_id,
        "metadata_kind": (metadata or {}).get("metadata_kind", "session"),
        "artifact_root_configured": True,
        "artifact_count": len(artifacts),
        "artifacts": artifacts,
        "bundle_download_url": bundle_path,
        **_rollout_artifact_status(session_dir, metadata, artifacts),
        **_endpoint_management_export_artifact_status(session_dir, metadata, artifacts),
    }


def load_evidence_artifact(
    artifact_root: Path,
    session_id: str,
    artifact_name: str,
    *,
    metadata: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], bytes]:
    descriptors = _evidence_artifact_descriptors(metadata)
    if artifact_name not in descriptors:
        raise EvidenceArtifactError("unsupported evidence artifact")
    session_dir = _evidence_artifact_dir(artifact_root, session_id, metadata)
    path = _resolve_session_artifact(session_dir, artifact_name)
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"evidence artifact not found: {artifact_name}")
    _verify_endpoint_management_export_artifact(session_dir, artifact_name, metadata)
    descriptor = descriptors[artifact_name]
    metadata = {
        "artifact": artifact_name,
        "kind": descriptor["kind"],
        "description": descriptor["description"],
        "media_type": descriptor["media_type"],
        "bytes": path.stat().st_size,
        "sha256": sha256_file(path),
    }
    return metadata, path.read_bytes()


def build_evidence_artifact_archive(
    artifact_root: Path,
    session_id: str,
    *,
    metadata: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], bytes]:
    listing = list_evidence_artifacts(artifact_root, session_id, metadata=metadata)
    if not listing["artifacts"]:
        raise FileNotFoundError(f"no evidence artifacts found for session: {session_id}")
    session_dir = _evidence_artifact_dir(artifact_root, session_id, metadata)
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
        for item in listing["artifacts"]:
            artifact_name = item["artifact"]
            _verify_endpoint_management_export_artifact(session_dir, artifact_name, metadata)
            archive.write(_resolve_session_artifact(session_dir, artifact_name), arcname=artifact_name)
    payload = buffer.getvalue()
    metadata = {
        "artifact": f"{session_id}-evidence-bundle.zip",
        "kind": "bundle",
        "description": "Complete downloadable CAVRA evidence artifact bundle.",
        "media_type": "application/zip",
        "bytes": len(payload),
        "sha256": hashlib.sha256(payload).hexdigest(),
        "artifact_count": listing["artifact_count"],
    }
    return metadata, payload


def _evidence_artifact_descriptors(metadata: dict[str, Any] | None) -> dict[str, dict[str, str]]:
    if (metadata or {}).get("metadata_kind") == "managed-endpoint-rollout":
        return ROLLOUT_EVIDENCE_ARTIFACTS
    if (metadata or {}).get("metadata_kind") == "endpoint-management-export":
        return _endpoint_management_export_descriptors(metadata or {})
    return EVIDENCE_ARTIFACTS


def _evidence_artifact_dir(artifact_root: Path, session_id: str, metadata: dict[str, Any] | None) -> Path:
    _validate_evidence_session_id(session_id)
    metadata_kind = (metadata or {}).get("metadata_kind")
    if metadata_kind not in {"managed-endpoint-rollout", "endpoint-management-export"}:
        return _session_artifact_dir(artifact_root, session_id)
    bundle_dir = str((metadata or {}).get("bundle_dir") or "")
    if not bundle_dir:
        return _session_artifact_dir(artifact_root, session_id)
    root = artifact_root.resolve()
    artifact_dir = Path(bundle_dir).resolve()
    if not artifact_dir.is_relative_to(root):
        label = "endpoint-management export" if metadata_kind == "endpoint-management-export" else "rollout evidence"
        raise EvidenceArtifactError(f"{label} directory is outside artifact root")
    return artifact_dir


def _rollout_artifact_status(
    session_dir: Path,
    metadata: dict[str, Any] | None,
    artifacts: list[dict[str, Any]],
) -> dict[str, Any]:
    if (metadata or {}).get("metadata_kind") != "managed-endpoint-rollout":
        return {}
    artifact_names = {str(item["artifact"]) for item in artifacts}
    checksum_path = session_dir / "checksums.txt"
    checksum_entries, checksum_errors = _read_artifact_checksums(checksum_path)
    verified_artifacts: list[str] = []
    checksum_mismatches: list[str] = []
    unchecked_artifacts: list[str] = []
    expected_artifacts = sorted(ROLLOUT_EVIDENCE_ARTIFACTS)
    missing_artifacts = sorted(name for name in expected_artifacts if name not in artifact_names)
    for artifact_name in expected_artifacts:
        if artifact_name == "checksums.txt" or artifact_name not in artifact_names:
            continue
        expected_sha256 = checksum_entries.get(artifact_name)
        if not expected_sha256:
            unchecked_artifacts.append(artifact_name)
            continue
        actual_sha256 = sha256_file(session_dir / artifact_name)
        if actual_sha256 == expected_sha256:
            verified_artifacts.append(artifact_name)
        else:
            checksum_mismatches.append(artifact_name)
    if checksum_errors or checksum_mismatches:
        integrity_status = "failed"
    elif missing_artifacts or unchecked_artifacts:
        integrity_status = "incomplete"
    else:
        integrity_status = "verified"
    return {
        "rollout_artifact_integrity": {
            "status": integrity_status,
            "verified_artifacts": sorted(verified_artifacts),
            "missing_artifacts": missing_artifacts,
            "unchecked_artifacts": sorted(unchecked_artifacts),
            "checksum_mismatches": sorted(checksum_mismatches),
            "checksum_errors": checksum_errors,
        },
        "promotion_readiness": _rollout_promotion_readiness(metadata or {}, integrity_status),
    }


def _endpoint_management_export_descriptors(metadata: dict[str, Any]) -> dict[str, dict[str, str]]:
    files = metadata.get("files", [])
    allowed_files = {str(item) for item in files if isinstance(item, str)}
    if not allowed_files:
        manifest = metadata.get("manifest", {})
        manifest_files = manifest.get("files", []) if isinstance(manifest, dict) else []
        allowed_files = {str(item) for item in manifest_files if isinstance(item, str)}
    allowed_files.add("checksums.txt")
    return {
        artifact_name: descriptor
        for artifact_name, descriptor in ENDPOINT_MANAGEMENT_EXPORT_ARTIFACTS.items()
        if artifact_name in allowed_files
    }


def _endpoint_management_export_artifact_status(
    session_dir: Path,
    metadata: dict[str, Any] | None,
    artifacts: list[dict[str, Any]],
) -> dict[str, Any]:
    if (metadata or {}).get("metadata_kind") != "endpoint-management-export":
        return {}
    artifact_names = {str(item["artifact"]) for item in artifacts}
    descriptors = _endpoint_management_export_descriptors(metadata or {})
    checksum_path = session_dir / "checksums.txt"
    checksum_entries, checksum_errors = _read_artifact_checksums(checksum_path)
    verified_artifacts: list[str] = []
    checksum_mismatches: list[str] = []
    unchecked_artifacts: list[str] = []
    expected_artifacts = sorted(descriptors)
    missing_artifacts = sorted(name for name in expected_artifacts if name not in artifact_names)
    for artifact_name in expected_artifacts:
        if artifact_name == "checksums.txt" or artifact_name not in artifact_names:
            continue
        expected_sha256 = checksum_entries.get(artifact_name)
        if not expected_sha256:
            unchecked_artifacts.append(artifact_name)
            continue
        actual_sha256 = sha256_file(session_dir / artifact_name)
        if actual_sha256 == expected_sha256:
            verified_artifacts.append(artifact_name)
        else:
            checksum_mismatches.append(artifact_name)
    if checksum_errors or checksum_mismatches:
        integrity_status = "failed"
    elif missing_artifacts or unchecked_artifacts:
        integrity_status = "incomplete"
    else:
        integrity_status = "verified"
    return {
        "endpoint_management_export_integrity": {
            "status": integrity_status,
            "verified_artifacts": sorted(verified_artifacts),
            "missing_artifacts": missing_artifacts,
            "unchecked_artifacts": sorted(unchecked_artifacts),
            "checksum_mismatches": sorted(checksum_mismatches),
            "checksum_errors": checksum_errors,
        },
        "download_readiness": {
            "status": "ready" if integrity_status == "verified" else "blocked",
            "rationale": (
                "Endpoint-management export artifacts are checksum-verified and ready for governed download."
                if integrity_status == "verified"
                else "Endpoint-management export artifact checksums must verify before download."
            ),
        },
    }


def _verify_endpoint_management_export_artifact(
    session_dir: Path,
    artifact_name: str,
    metadata: dict[str, Any] | None,
) -> None:
    if (metadata or {}).get("metadata_kind") != "endpoint-management-export":
        return
    if artifact_name == "checksums.txt":
        return
    checksum_entries, checksum_errors = _read_artifact_checksums(session_dir / "checksums.txt")
    if checksum_errors:
        raise EvidenceArtifactError("endpoint-management export checksums are invalid")
    expected_sha256 = checksum_entries.get(artifact_name)
    if not expected_sha256:
        raise EvidenceArtifactError("endpoint-management export artifact is missing checksum coverage")
    actual_sha256 = sha256_file(session_dir / artifact_name)
    if actual_sha256 != expected_sha256:
        raise EvidenceArtifactError("endpoint-management export artifact checksum verification failed")


def _read_artifact_checksums(path: Path) -> tuple[dict[str, str], list[str]]:
    if not path.exists() or not path.is_file():
        return {}, ["missing checksums.txt"]
    entries: dict[str, str] = {}
    errors: list[str] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        parts = line.split()
        if len(parts) < 2 or len(parts[0]) != 64:
            errors.append(f"invalid checksum line {line_number}")
            continue
        entries[parts[-1]] = parts[0].lower()
    return entries, errors


def _rollout_promotion_readiness(metadata: dict[str, Any], integrity_status: str) -> dict[str, str]:
    rollout_status = str(metadata.get("rollout_status") or "unknown")
    if integrity_status != "verified":
        return {
            "status": "blocked",
            "rationale": "Rollout artifact checksums must verify before promotion.",
        }
    if rollout_status in {"failed", "rolled_back"}:
        return {
            "status": "blocked",
            "rationale": f"Rollout status is {rollout_status}.",
        }
    if rollout_status == "planned":
        return {
            "status": "review",
            "rationale": "Rollout is planned and needs staged execution evidence before promotion.",
        }
    if rollout_status in {"staged", "succeeded"}:
        return {
            "status": "ready",
            "rationale": "Rollout evidence is checksum-verified and the rollout state can proceed.",
        }
    return {
        "status": "review",
        "rationale": "Rollout status is not recognized for automatic promotion readiness.",
    }


def _session_artifact_dir(artifact_root: Path, session_id: str) -> Path:
    _validate_evidence_session_id(session_id)
    root = artifact_root.resolve()
    session_dir = (root / session_id).resolve()
    if not session_dir.is_relative_to(root):
        raise EvidenceArtifactError("evidence session escapes artifact root")
    return session_dir


def _validate_evidence_session_id(session_id: str) -> None:
    if not session_id or session_id in {".", ".."} or "/" in session_id or "\\" in session_id:
        raise EvidenceArtifactError("invalid evidence session ID")


def _resolve_session_artifact(session_dir: Path, artifact_name: str) -> Path:
    path = (session_dir / artifact_name).resolve()
    if path.name != artifact_name or not path.is_relative_to(session_dir):
        raise EvidenceArtifactError("evidence artifact escapes session directory")
    return path


class EvidenceMetadataStore:
    def __init__(self, path: Path) -> None:
        self.path = path

    def list(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        payload = json.loads(self.path.read_text(encoding="utf-8"))
        return payload.get("items", [])

    def get(self, session_id: str) -> dict[str, Any] | None:
        for item in self.list():
            if item.get("session_id") == session_id:
                return item
        return None

    def upsert(self, metadata: dict[str, Any]) -> dict[str, Any]:
        session_id = metadata.get("session_id")
        if not session_id:
            raise ValueError("metadata must include session_id")
        items = [item for item in self.list() if item.get("session_id") != session_id]
        item = {"schema_version": "cavra.evidence.metadata.v1", "product": "CAVRA", **metadata}
        items.append(item)
        write_json(self.path, {"items": sorted(items, key=lambda value: str(value.get("session_id")))})
        return item

    def index_bundle(self, bundle_dir: Path) -> dict[str, Any]:
        return self.upsert(build_evidence_metadata(bundle_dir))


class SQLiteEvidenceMetadataStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS evidence_metadata (
                    session_id TEXT PRIMARY KEY,
                    created_at TEXT,
                    signer TEXT,
                    decision_count INTEGER NOT NULL,
                    blocked_count INTEGER NOT NULL,
                    approval_required_count INTEGER NOT NULL,
                    payload TEXT NOT NULL
                )
                """
            )

    def upsert(self, metadata: dict[str, Any]) -> dict[str, Any]:
        session_id = metadata.get("session_id")
        if not session_id:
            raise ValueError("metadata must include session_id")
        item = {"schema_version": "cavra.evidence.metadata.v1", "product": "CAVRA", **metadata}
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO evidence_metadata (
                    session_id, created_at, signer, decision_count, blocked_count, approval_required_count, payload
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(session_id) DO UPDATE SET
                    created_at=excluded.created_at,
                    signer=excluded.signer,
                    decision_count=excluded.decision_count,
                    blocked_count=excluded.blocked_count,
                    approval_required_count=excluded.approval_required_count,
                    payload=excluded.payload
                """,
                (
                    session_id,
                    item.get("created_at"),
                    item.get("signer"),
                    int(item.get("decision_count", 0)),
                    int(item.get("blocked_count", 0)),
                    int(item.get("approval_required_count", 0)),
                    json.dumps(item, sort_keys=True),
                ),
            )
        return item

    def index_bundle(self, bundle_dir: Path) -> dict[str, Any]:
        return self.upsert(build_evidence_metadata(bundle_dir))

    def get(self, session_id: str) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT payload FROM evidence_metadata WHERE session_id = ?",
                (session_id,),
            ).fetchone()
        return json.loads(row["payload"]) if row else None

    def search(
        self,
        *,
        session_id: str | None = None,
        signer: str | None = None,
        min_blocked: int | None = None,
        has_approvals: bool | None = None,
        metadata_kind: str | None = None,
        rollout_status: str | None = None,
        environment: str | None = None,
        deployment_target: str | None = None,
        target_ring: str | None = None,
        approval_state: str | None = None,
        promotion_execution_status: str | None = None,
        rollback_execution_status: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict[str, Any]:
        limit = max(1, min(limit, 500))
        offset = max(0, offset)
        clauses: list[str] = []
        params: list[Any] = []
        if session_id:
            clauses.append("session_id LIKE ?")
            params.append(f"%{session_id}%")
        if signer:
            clauses.append("signer = ?")
            params.append(signer)
        if min_blocked is not None:
            clauses.append("blocked_count >= ?")
            params.append(min_blocked)
        if has_approvals is not None:
            clauses.append("approval_required_count > 0" if has_approvals else "approval_required_count = 0")
        where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        payload_filters = any(
            [
                metadata_kind,
                rollout_status,
                environment,
                deployment_target,
                target_ring,
                approval_state,
                promotion_execution_status,
                rollback_execution_status,
            ]
        )
        with self._connect() as connection:
            if payload_filters:
                rows = connection.execute(
                    f"""
                    SELECT payload FROM evidence_metadata
                    {where}
                    ORDER BY created_at DESC, session_id ASC
                    """,
                    params,
                ).fetchall()
                filtered = _filter_evidence_metadata_payloads(
                    [json.loads(row["payload"]) for row in rows],
                    metadata_kind=metadata_kind,
                    rollout_status=rollout_status,
                    environment=environment,
                    deployment_target=deployment_target,
                    target_ring=target_ring,
                    approval_state=approval_state,
                    promotion_execution_status=promotion_execution_status,
                    rollback_execution_status=rollback_execution_status,
                )
                total = len(filtered)
                items = filtered[offset : offset + limit]
            else:
                total = connection.execute(
                    f"SELECT COUNT(*) AS count FROM evidence_metadata {where}",
                    params,
                ).fetchone()["count"]
                rows = connection.execute(
                    f"""
                    SELECT payload FROM evidence_metadata
                    {where}
                    ORDER BY created_at DESC, session_id ASC
                    LIMIT ? OFFSET ?
                    """,
                    [*params, limit, offset],
                ).fetchall()
                items = [json.loads(row["payload"]) for row in rows]
        return {
            "items": items,
            "total": total,
            "limit": limit,
            "offset": offset,
        }


def _filter_evidence_metadata_payloads(
    items: list[dict[str, Any]],
    *,
    metadata_kind: str | None = None,
    rollout_status: str | None = None,
    environment: str | None = None,
    deployment_target: str | None = None,
    target_ring: str | None = None,
    approval_state: str | None = None,
    promotion_execution_status: str | None = None,
    rollback_execution_status: str | None = None,
) -> list[dict[str, Any]]:
    filtered = items
    if metadata_kind:
        filtered = [item for item in filtered if item.get("metadata_kind") == metadata_kind]
    if rollout_status:
        filtered = [item for item in filtered if item.get("rollout_status") == rollout_status]
    if environment:
        filtered = [item for item in filtered if item.get("environment") == environment]
    if deployment_target:
        filtered = [
            item
            for item in filtered
            if deployment_target in {str(target) for target in item.get("deployment_targets", [])}
        ]
    if target_ring:
        filtered = [item for item in filtered if item.get("target_ring") == target_ring]
    if approval_state:
        filtered = [item for item in filtered if item.get("approval_state") == approval_state]
    if promotion_execution_status:
        filtered = [
            item
            for item in filtered
            if item.get("promotion_execution_status") == promotion_execution_status
        ]
    if rollback_execution_status:
        filtered = [
            item
            for item in filtered
            if item.get("rollback_execution_status") == rollback_execution_status
        ]
    return filtered


def apply_sqlite_migrations(database_path: Path, migrations_dir: Path) -> dict[str, Any]:
    migration_files = sorted(migrations_dir.glob("*.sql"))
    if not migration_files:
        raise FileNotFoundError(f"no SQLite migrations found in {migrations_dir}")
    database_path.parent.mkdir(parents=True, exist_ok=True)
    applied: list[str] = []
    skipped: list[str] = []
    with sqlite3.connect(database_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS schema_migrations (
                id TEXT PRIMARY KEY,
                applied_at TEXT NOT NULL
            )
            """
        )
        existing = {
            row[0]
            for row in connection.execute("SELECT id FROM schema_migrations").fetchall()
        }
        for migration in migration_files:
            migration_id = migration.name
            if migration_id in existing:
                skipped.append(migration_id)
                continue
            connection.executescript(migration.read_text(encoding="utf-8"))
            connection.execute(
                "INSERT INTO schema_migrations (id, applied_at) VALUES (?, ?)",
                (migration_id, datetime.now(timezone.utc).isoformat()),
            )
            applied.append(migration_id)
    return {
        "database": str(database_path),
        "migrations_dir": str(migrations_dir),
        "applied": applied,
        "skipped": skipped,
    }


def _event_epoch(event: dict[str, Any]) -> float:
    timestamp = event.get("timestamp")
    if not timestamp:
        return datetime.now(timezone.utc).timestamp()
    normalized = str(timestamp).replace("Z", "+00:00")
    return datetime.fromisoformat(normalized).timestamp()


def _provider_severity(severity: str, *, provider: str) -> str:
    normalized = severity.lower()
    if provider == "sentinel":
        return {
            "critical": "High",
            "high": "High",
            "medium": "Medium",
            "low": "Low",
        }.get(normalized, "Informational")
    if provider == "datadog":
        return {
            "critical": "error",
            "high": "error",
            "medium": "warning",
            "low": "info",
        }.get(normalized, "info")
    return normalized


def _sign_manifest_ed25519(canonical: bytes, private_key_path: Path, *, key_id: str | None = None) -> dict[str, Any]:
    try:
        from cryptography.hazmat.primitives import hashes, serialization
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("Install cryptography to use Ed25519 evidence signatures.") from exc

    private_key = serialization.load_pem_private_key(private_key_path.read_bytes(), password=None)
    signature = private_key.sign(canonical)
    public_key = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    digest = hashes.Hash(hashes.SHA256())
    digest.update(public_key)
    fingerprint = digest.finalize().hex()
    return {
        "algorithm": "Ed25519",
        "key_id": key_id or fingerprint[:16],
        "value": base64.b64encode(signature).decode("ascii"),
        "public_key_sha256": fingerprint,
    }


def _verify_manifest_ed25519(
    canonical: bytes,
    signature: dict[str, Any],
    public_key_path: Path,
    *,
    key_id: str | None = None,
) -> None:
    try:
        from cryptography.hazmat.primitives import hashes
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("Install cryptography to use Ed25519 evidence signatures.") from exc

    if signature.get("algorithm") != "Ed25519":
        raise ValueError("manifest signature algorithm is not Ed25519")
    public_key_bytes = public_key_path.read_bytes()
    digest = hashes.Hash(hashes.SHA256())
    digest.update(public_key_bytes)
    expected_fingerprint = digest.finalize().hex()
    if signature.get("public_key_sha256") != expected_fingerprint:
        raise ValueError("manifest public key fingerprint mismatch")
    if key_id and signature.get("key_id") != key_id:
        raise ValueError("manifest key ID mismatch")
    _verify_ed25519_signature(canonical, signature, public_key_bytes)


def _verify_manifest_trust_root(
    canonical: bytes,
    signature: dict[str, Any],
    trust_root_path: Path,
    *,
    key_id: str | None = None,
) -> None:
    trust_root = json.loads(trust_root_path.read_text(encoding="utf-8"))
    if trust_root.get("schema_version") == "cavra.evidence.trust-root-bundle.v1":
        trust_root = _select_trust_root(trust_root, signature, key_id=key_id)
    if trust_root.get("status") != "active":
        raise ValueError("trust root is not active")
    expected_key_id = key_id or trust_root.get("key_id")
    if expected_key_id and signature.get("key_id") != expected_key_id:
        raise ValueError("manifest key ID mismatch")
    if signature.get("public_key_sha256") != trust_root.get("public_key_sha256"):
        raise ValueError("manifest public key fingerprint mismatch")
    _verify_ed25519_signature(canonical, signature, trust_root["public_key_pem"].encode("utf-8"))


def _select_trust_root(bundle: dict[str, Any], signature: dict[str, Any], *, key_id: str | None = None) -> dict[str, Any]:
    expected_key_id = key_id or signature.get("key_id")
    for trust_root in bundle.get("trust_roots", []):
        if expected_key_id and trust_root.get("key_id") != expected_key_id:
            continue
        if signature.get("public_key_sha256") == trust_root.get("public_key_sha256"):
            return trust_root
    raise ValueError("matching trust root not found")


def _verify_ed25519_signature(canonical: bytes, signature: dict[str, Any], public_key_bytes: bytes) -> None:
    try:
        from cryptography.exceptions import InvalidSignature
        from cryptography.hazmat.primitives import serialization
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("Install cryptography to use Ed25519 evidence signatures.") from exc

    public_key = serialization.load_pem_public_key(public_key_bytes)
    try:
        public_key.verify(base64.b64decode(signature.get("value", "")), canonical)
    except InvalidSignature as exc:
        raise ValueError("manifest signature mismatch") from exc


def build_attestation_verification(bundle_dir: Path) -> dict[str, Any]:
    evidence = json.loads((bundle_dir / "evidence.json").read_text(encoding="utf-8"))
    attestation_path = bundle_dir / "pr-attestation.md"
    if not attestation_path.exists():
        return {
            "schema_version": "cavra.pr-attestation.verification.v1",
            "product": "CAVRA",
            "session_id": evidence.get("session_id"),
            "valid": False,
            "errors": ["missing pr-attestation.md"],
        }
    attestation = attestation_path.read_text(encoding="utf-8")
    errors: list[str] = []
    session_id = evidence.get("session_id")
    decisions = evidence.get("decisions", [])
    if "CAVRA PR Attestation" not in attestation:
        errors.append("missing attestation title")
    if session_id and f"Session: `{session_id}`" not in attestation:
        errors.append("session ID mismatch")
    for decision in decisions:
        target = str(decision.get("target"))
        if target and target not in attestation:
            errors.append(f"missing decision target: {target}")
    return {
        "schema_version": "cavra.pr-attestation.verification.v1",
        "product": "CAVRA",
        "session_id": session_id,
        "valid": not errors,
        "errors": errors,
        "decision_count": len(decisions),
        "attestation_path": str(attestation_path),
    }


def render_attestation_verification(report: dict[str, Any]) -> str:
    lines = [
        "# CAVRA PR Attestation Verification",
        "",
        f"Session: `{report.get('session_id')}`",
        f"Valid: `{report.get('valid')}`",
        f"Decision count: `{report.get('decision_count', 0)}`",
        "",
    ]
    if report.get("errors"):
        lines.extend(["## Errors", ""])
        lines.extend(f"- {error}" for error in report["errors"])
        lines.append("")
    return "\n".join(lines)


def export_attestation_verification(bundle_dir: Path, output_dir: Path) -> ExportResult:
    output_dir.mkdir(parents=True, exist_ok=True)
    report = build_attestation_verification(bundle_dir)
    json_path = write_json(output_dir / "pr-attestation-verification.json", report)
    markdown_path = output_dir / "pr-attestation-verification.md"
    markdown_path.write_text(render_attestation_verification(report), encoding="utf-8")
    return ExportResult(output_dir, [json_path, markdown_path])
