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
