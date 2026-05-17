from __future__ import annotations

import base64
import hashlib
import hmac
import json
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
    manifest = build_manifest(files, signer=signer, key=key, private_key=private_key, created_at=created_at)
    manifest_path = write_json(destination / "manifest.json", manifest)
    return EvidenceBundleResult(destination, manifest_path, [*files, manifest_path])


def build_manifest(
    files: list[Path],
    *,
    signer: str = "local",
    key: str | None = None,
    private_key: Path | None = None,
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
        manifest_payload["signature"] = _sign_manifest_ed25519(canonical, private_key)
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
            _verify_manifest_ed25519(canonical, signature, public_key)
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
        "retention": retention,
    }


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


def _sign_manifest_ed25519(canonical: bytes, private_key_path: Path) -> dict[str, Any]:
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
    return {
        "algorithm": "Ed25519",
        "value": base64.b64encode(signature).decode("ascii"),
        "public_key_sha256": digest.finalize().hex(),
    }


def _verify_manifest_ed25519(canonical: bytes, signature: dict[str, Any], public_key_path: Path) -> None:
    try:
        from cryptography.exceptions import InvalidSignature
        from cryptography.hazmat.primitives import hashes, serialization
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
    public_key = serialization.load_pem_public_key(public_key_bytes)
    try:
        public_key.verify(base64.b64decode(signature.get("value", "")), canonical)
    except InvalidSignature as exc:
        raise ValueError("manifest signature mismatch") from exc
