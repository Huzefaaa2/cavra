from __future__ import annotations

import base64
import hashlib
import hmac
import json
from dataclasses import dataclass
from datetime import datetime, timezone
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


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, payload: dict[str, Any]) -> Path:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


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
        },
        "azure_immutable_blob": {
            "account": azure_account,
            "container": azure_container,
            "immutability_policy_days": retention_days,
            "allow_protected_append_writes": False,
            "required_versioning": True,
            "required_infrastructure_encryption": True,
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
        "",
        "## Azure Immutable Blob",
        "",
        f"- Account: `{plan['azure_immutable_blob']['account']}`",
        f"- Container: `{plan['azure_immutable_blob']['container']}`",
        "- Blob versioning: required",
        "- Infrastructure encryption: required",
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


def create_evidence_bundle(
    decisions: list[dict[str, Any]],
    destination: Path,
    *,
    session_id: str = "local",
    signer: str = "local",
    key: str | None = None,
) -> EvidenceBundleResult:
    destination.mkdir(parents=True, exist_ok=True)
    evidence_path = write_json(
        destination / "evidence.json",
        {
            "product": "CAVRA",
            "tagline": "Before the agent acts, CAVRA decides.",
            "session_id": session_id,
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
            "events": len(decisions),
            "blocked": sum(1 for item in decisions if item.get("decision") == "block"),
            "approval_required": sum(1 for item in decisions if item.get("decision") == "require_approval"),
        },
    )
    files = [evidence_path, attestation_path, compliance_path, siem_path, summary_path]
    manifest = build_manifest(files, signer=signer, key=key)
    manifest_path = write_json(destination / "manifest.json", manifest)
    return EvidenceBundleResult(destination, manifest_path, [*files, manifest_path])


def build_manifest(files: list[Path], *, signer: str = "local", key: str | None = None) -> dict[str, Any]:
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
        "created_at": datetime.now(timezone.utc).isoformat(),
        "signer": signer,
        "files": file_entries,
    }
    canonical = json.dumps(manifest_payload, sort_keys=True).encode("utf-8")
    if key:
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


def verify_evidence_bundle(bundle_dir: Path, *, key: str | None = None) -> tuple[bool, list[str]]:
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
    elif signature.get("algorithm") == "SHA256":
        expected = hashlib.sha256(canonical).hexdigest()
        if signature.get("value") != expected:
            errors.append("manifest digest mismatch")
    return not errors, errors


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
