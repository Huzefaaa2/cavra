from __future__ import annotations

import base64
import hashlib
import hmac
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


AUDIT_LOG_EVENT_SCHEMA = "cavra.audit-log.event.v1"
AUDIT_LOG_READINESS_SCHEMA = "cavra.audit-log.readiness.v1"
AUDIT_LOG_EVIDENCE_SCHEMA = "cavra.audit-log.evidence.v1"

SUPPORTED_IMMUTABLE_STORES = {
    "azure_immutable_blob",
    "s3_object_lock",
    "postgres_append_only",
    "worn_storage",
    "siem_archive",
}
REQUIRED_ALERTS = {
    "audit_write_failure",
    "audit_integrity_failure",
    "audit_retention_policy_failure",
    "audit_export_failure",
}
REQUIRED_EXPORTS = {
    "jsonl",
    "siem",
    "auditor_package",
}


@dataclass(frozen=True)
class AuditAppendResult:
    path: Path
    record: dict[str, Any]


def append_audit_event(
    path: Path,
    *,
    event_type: str,
    actor: str,
    action: str,
    target: str,
    decision: str,
    tenant_id: str | None = None,
    workspace_id: str | None = None,
    evidence_refs: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
    key: str | None = None,
    key_id: str | None = None,
    created_at: str | None = None,
) -> AuditAppendResult:
    path.parent.mkdir(parents=True, exist_ok=True)
    records = load_audit_log(path) if path.exists() else []
    previous_hash = records[-1]["record_hash"] if records else None
    record = {
        "schema_version": AUDIT_LOG_EVENT_SCHEMA,
        "sequence": len(records) + 1,
        "created_at": created_at or datetime.now(timezone.utc).isoformat(),
        "event_type": event_type,
        "actor": actor,
        "action": action,
        "target": target,
        "decision": decision,
        "tenant_id": tenant_id,
        "workspace_id": workspace_id,
        "evidence_refs": evidence_refs or [],
        "metadata": metadata or {},
        "previous_hash": previous_hash,
    }
    record["record_hash"] = audit_record_hash(record)
    if key:
        record["signature"] = audit_record_signature(record, key=key, key_id=key_id)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")
    return AuditAppendResult(path=path, record=record)


def load_audit_log(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid audit JSONL at line {line_number}") from exc
    return records


def verify_append_only_audit_log(
    path: Path,
    *,
    key: str | None = None,
    key_id: str | None = None,
) -> dict[str, Any]:
    errors: list[str] = []
    try:
        records = load_audit_log(path)
    except ValueError as exc:
        return _audit_verification_result(path, [], [str(exc)])
    previous_hash: str | None = None
    for index, record in enumerate(records, start=1):
        if record.get("schema_version") != AUDIT_LOG_EVENT_SCHEMA:
            errors.append(f"record {index}: invalid schema_version")
        if record.get("sequence") != index:
            errors.append(f"record {index}: sequence mismatch")
        if record.get("previous_hash") != previous_hash:
            errors.append(f"record {index}: previous_hash mismatch")
        expected_hash = audit_record_hash(record)
        if record.get("record_hash") != expected_hash:
            errors.append(f"record {index}: record_hash mismatch")
        if key:
            expected_signature = audit_record_signature(record, key=key, key_id=key_id)
            if record.get("signature") != expected_signature:
                errors.append(f"record {index}: signature mismatch")
        previous_hash = record.get("record_hash")
    return _audit_verification_result(path, records, errors)


def audit_record_hash(record: dict[str, Any]) -> str:
    payload = _record_without_integrity_fields(record)
    return hashlib.sha256(_canonical_json(payload)).hexdigest()


def audit_record_signature(record: dict[str, Any], *, key: str, key_id: str | None = None) -> dict[str, str]:
    payload = _record_without_integrity_fields(record)
    payload["record_hash"] = audit_record_hash(record)
    digest = hmac.new(key.encode("utf-8"), _canonical_json(payload), hashlib.sha256).digest()
    return {
        "algorithm": "HS256",
        "key_id": key_id or "audit-log-hmac",
        "value": base64.b64encode(digest).decode("ascii"),
    }


def build_enterprise_audit_log_contract() -> dict[str, Any]:
    return {
        "schema_version": "cavra.audit-log.contract.v1",
        "product": "CAVRA",
        "purpose": "Immutable append-only audit log contract separate from evidence bundles.",
        "event_schema": AUDIT_LOG_EVENT_SCHEMA,
        "supported_immutable_stores": sorted(SUPPORTED_IMMUTABLE_STORES),
        "required_alerts": sorted(REQUIRED_ALERTS),
        "required_exports": sorted(REQUIRED_EXPORTS),
        "required_controls": [
            "audit log is separate from evidence bundles",
            "records are append-only and hash chained",
            "retention is at least 2555 days for regulated evidence",
            "tamper detection is tested",
            "auditor and SIEM export are supported",
            "write, integrity, retention, and export failure alerts are configured",
        ],
    }


def build_enterprise_audit_log_readiness(
    packet: dict[str, Any] | None = None,
    *,
    require_live: bool = False,
) -> dict[str, Any]:
    if packet is None:
        return {
            "schema_version": AUDIT_LOG_READINESS_SCHEMA,
            "product": "CAVRA",
            "evidence_mode": "contract",
            "ready_for_enterprise_audit_log_contract": True,
            "ready_for_enterprise_live_audit_log": False,
            "status": "ready_with_warnings",
            "blocker_count": 0,
            "warning_count": 1,
            "checks": [
                {
                    "name": "evidence_packet",
                    "status": "warn",
                    "message": "Enterprise audit-log contract is available, but no sample or live packet was supplied.",
                }
            ],
        }
    return validate_enterprise_audit_log_packet(packet, require_live=require_live)


def validate_enterprise_audit_log_packet(packet: dict[str, Any], *, require_live: bool = False) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _check_schema(packet, checks)
    _check_evidence_mode(packet, checks, require_live=require_live)
    _check_storage(packet.get("storage", {}), checks)
    _check_integrity(packet.get("integrity", {}), checks)
    _check_retention(packet.get("retention", {}), checks)
    _check_exports(packet.get("exports", {}), checks)
    _check_monitoring(packet.get("monitoring", {}), checks)
    _check_operating_evidence(packet.get("operating_evidence", {}), checks)

    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    contract_ready = blocker_count == 0
    live_ready = contract_ready and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": AUDIT_LOG_READINESS_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_enterprise_audit_log_contract": contract_ready,
        "ready_for_enterprise_live_audit_log": live_ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def _audit_verification_result(path: Path, records: list[dict[str, Any]], errors: list[str]) -> dict[str, Any]:
    return {
        "schema_version": "cavra.audit-log.verification.v1",
        "product": "CAVRA",
        "path": str(path),
        "valid": not errors,
        "record_count": len(records),
        "first_sequence": records[0].get("sequence") if records else None,
        "last_sequence": records[-1].get("sequence") if records else None,
        "last_record_hash": records[-1].get("record_hash") if records else None,
        "errors": errors,
    }


def _canonical_json(payload: dict[str, Any]) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _record_without_integrity_fields(record: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in record.items() if key not in {"record_hash", "signature"}}


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})


def _check_schema(packet: dict[str, Any], checks: list[dict[str, str]]) -> None:
    if packet.get("schema_version") == AUDIT_LOG_EVIDENCE_SCHEMA:
        _add_check(checks, "schema_version", "pass", "Audit-log evidence packet schema is valid.")
    else:
        _add_check(checks, "schema_version", "blocker", "Packet must use cavra.audit-log.evidence.v1.")


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    evidence_mode = packet.get("evidence_mode")
    if evidence_mode == "live":
        _add_check(checks, "evidence_mode", "pass", "Live audit-log evidence packet supplied.")
    elif evidence_mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample audit-log packet validates contract shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "Live audit-log validation requires evidence_mode=live.")


def _check_storage(storage: dict[str, Any], checks: list[dict[str, str]]) -> None:
    if (
        storage.get("separate_from_evidence_bundles") is True
        and storage.get("append_only") is True
        and storage.get("external_mutation_disabled") is True
        and storage.get("store_type") in SUPPORTED_IMMUTABLE_STORES
        and bool(storage.get("provider_ref") or storage.get("provider_refs"))
    ):
        _add_check(checks, "storage", "pass", "Audit store is separate, append-only, immutable, and provider-backed.")
        return
    _add_check(checks, "storage", "blocker", "Audit storage must be separate, append-only, immutable, and provider-backed.")


def _check_integrity(integrity: dict[str, Any], checks: list[dict[str, str]]) -> None:
    if (
        integrity.get("hash_chained") is True
        and integrity.get("sample_log_verified") is True
        and integrity.get("tamper_detection_tested") is True
        and integrity.get("signature_or_hmac_enabled") is True
        and bool(integrity.get("latest_verification_evidence_ref"))
    ):
        _add_check(checks, "integrity", "pass", "Hash-chain, signature/HMAC, and tamper detection evidence are present.")
        return
    _add_check(checks, "integrity", "blocker", "Audit integrity must prove hash-chain verification, signing/HMAC, and tamper detection.")


def _check_retention(retention: dict[str, Any], checks: list[dict[str, str]]) -> None:
    retention_days = _as_int(retention.get("retention_days"))
    if (
        retention_days is not None
        and retention_days >= 2555
        and retention.get("legal_hold_supported") is True
        and retention.get("delete_protection") is True
        and bool(retention.get("retention_policy_ref"))
    ):
        _add_check(checks, "retention", "pass", f"Audit retention meets regulated target ({retention_days} days).")
        return
    _add_check(checks, "retention", "blocker", "Audit retention must be >=2555 days with legal hold and delete protection.")


def _check_exports(exports: dict[str, Any], checks: list[dict[str, str]]) -> None:
    formats = {str(item) for item in exports.get("formats", [])}
    if (
        REQUIRED_EXPORTS <= formats
        and exports.get("redaction_supported") is True
        and exports.get("auditor_export_tested") is True
        and exports.get("siem_export_tested") is True
        and bool(exports.get("latest_export_evidence_ref"))
    ):
        _add_check(checks, "exports", "pass", "Auditor, SIEM, and JSONL exports are covered with redaction evidence.")
        return
    _add_check(checks, "exports", "blocker", "Audit exports must cover JSONL, SIEM, auditor package, redaction, and tested delivery.")


def _check_monitoring(monitoring: dict[str, Any], checks: list[dict[str, str]]) -> None:
    alerts = {str(item) for item in monitoring.get("alerts", [])}
    if REQUIRED_ALERTS <= alerts and bool(monitoring.get("runbook_ref")):
        _add_check(checks, "monitoring", "pass", "Audit write, integrity, retention, and export alerts are configured.")
        return
    _add_check(checks, "monitoring", "blocker", "Audit monitoring must cover write, integrity, retention, and export failures.")


def _check_operating_evidence(evidence: dict[str, Any], checks: list[dict[str, str]]) -> None:
    required = {
        "change_control_ref": evidence.get("change_control_ref"),
        "tamper_drill_ref": evidence.get("tamper_drill_ref"),
        "recovery_drill_ref": evidence.get("recovery_drill_ref"),
        "auditor_handoff_ref": evidence.get("auditor_handoff_ref"),
    }
    missing = [name for name, value in required.items() if not value]
    if not missing:
        _add_check(checks, "operating_evidence", "pass", "Change control, tamper drill, recovery drill, and auditor handoff refs are present.")
        return
    _add_check(checks, "operating_evidence", "blocker", f"Audit operating evidence is missing: {', '.join(missing)}.")


def _as_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
