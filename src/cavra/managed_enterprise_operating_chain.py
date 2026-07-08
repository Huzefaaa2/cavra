from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

from cavra.managed_enterprise_cutover_runbook import validate_managed_enterprise_cutover_runbook
from cavra.managed_enterprise_live_validation_plan import validate_managed_enterprise_live_validation_plan
from cavra.managed_enterprise_operating_announcement import validate_managed_enterprise_operating_announcement
from cavra.managed_enterprise_operating_release_index import validate_managed_enterprise_operating_release_index
from cavra.managed_enterprise_stabilization_report import validate_managed_enterprise_stabilization_report
from cavra.managed_enterprise_steady_state_handoff import validate_managed_enterprise_steady_state_handoff


MANAGED_ENTERPRISE_OPERATING_CHAIN_SCHEMA = "cavra.managed-enterprise-operating-chain.v1"
MANAGED_ENTERPRISE_OPERATING_CHAIN_RESULT_SCHEMA = "cavra.managed-enterprise-operating-chain.result.v1"

Validator = Callable[[dict[str, Any]], dict[str, Any]]

REQUIRED_CHAIN_ARTIFACTS: dict[str, dict[str, Any]] = {
    "live_validation_plan": {
        "path_field": "live_validation_plan_path",
        "ready_flag": "ready_for_managed_enterprise_live_validation",
        "validator": validate_managed_enterprise_live_validation_plan,
        "objective": "Real tenant, connector, SMTP/report, runtime workflow, AISPM, and closeout refs validate.",
    },
    "cutover_runbook": {
        "path_field": "cutover_runbook_path",
        "ready_flag": "ready_for_managed_enterprise_cutover",
        "validator": validate_managed_enterprise_cutover_runbook,
        "objective": "Activation, go/no-go, rollback, customer closeout, and status sync validate.",
    },
    "stabilization_report": {
        "path_field": "stabilization_report_path",
        "ready_flag": "ready_for_managed_enterprise_stabilization_closeout",
        "validator": validate_managed_enterprise_stabilization_report,
        "objective": "First post-cutover health window validates.",
    },
    "steady_state_handoff": {
        "path_field": "steady_state_handoff_path",
        "ready_flag": "ready_for_managed_enterprise_steady_state",
        "validator": validate_managed_enterprise_steady_state_handoff,
        "objective": "Normal operating ownership, cadence, support, AISPM, and evidence custody validate.",
    },
    "operating_release_index": {
        "path_field": "operating_release_index_path",
        "ready_flag": "ready_for_managed_enterprise_operating_release",
        "validator": validate_managed_enterprise_operating_release_index,
        "objective": "Final operating release index validates.",
    },
    "operating_announcement": {
        "path_field": "operating_announcement_path",
        "ready_flag": "ready_for_managed_enterprise_operating_announcement",
        "validator": validate_managed_enterprise_operating_announcement,
        "objective": "Customer-safe operating announcement validates.",
    },
}

REQUIRED_PROFILE_FIELDS = {
    "operating_chain_ref",
    "release_owner_ref",
    "evidence_room_ref",
    "approval_record_ref",
}

REQUIRED_REDACTION_CONTROLS = {
    "contains_no_credentials",
    "contains_no_customer_pii",
    "contains_no_private_release_notes",
    "contains_no_raw_alert_payloads",
    "contains_no_raw_contracts",
    "contains_no_raw_logs",
    "contains_no_raw_model_data",
    "contains_no_raw_prompts",
    "contains_no_secrets",
    "contains_no_tenant_names",
}

FORBIDDEN_FIELDS = {
    "api_key",
    "connection_string",
    "contract_value",
    "customer_name",
    "email",
    "legal_terms",
    "password",
    "private_key",
    "private_release_notes",
    "raw_alert",
    "raw_alerts",
    "raw_contract",
    "raw_contracts",
    "raw_log",
    "raw_logs",
    "raw_model",
    "raw_prompt",
    "raw_prompts",
    "secret",
    "smtp_password",
    "smtp_username",
    "tenant_name",
    "token",
    "training_data",
}

ALLOWED_REF_PREFIXES = (
    "audit://",
    "evidence://",
    "release://",
    "runbook://",
    "share://",
    "ticket://",
    "vault://",
    "workflow://",
    "sample://",
)


def build_managed_enterprise_operating_chain_manifest(*, evidence_mode: str = "sample") -> dict[str, Any]:
    prefix = "sample" if evidence_mode == "sample" else "evidence"
    suffix = "sample.json" if evidence_mode == "sample" else "live.sanitized.example.json"
    return {
        "schema_version": MANAGED_ENTERPRISE_OPERATING_CHAIN_SCHEMA,
        "product": "CAVRA",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "chain_profile": {
            "operating_chain_ref": f"{prefix}://managed-enterprise-operating-chain",
            "release_owner_ref": f"{prefix}://owner/managed-enterprise-operating-chain",
            "evidence_room_ref": f"{prefix}://evidence-room/managed-enterprise-operating-chain",
            "approval_record_ref": f"{prefix}://approval/managed-enterprise-operating-chain",
        },
        "artifact_paths": {
            "live_validation_plan_path": (
                f"examples/managed-enterprise-live-validation/managed-enterprise-live-validation-plan.{suffix}"
            ),
            "cutover_runbook_path": f"examples/managed-enterprise-cutover/managed-enterprise-cutover-runbook.{suffix}",
            "stabilization_report_path": (
                f"examples/managed-enterprise-stabilization/managed-enterprise-stabilization-report.{suffix}"
            ),
            "steady_state_handoff_path": (
                f"examples/managed-enterprise-steady-state/managed-enterprise-steady-state-handoff.{suffix}"
            ),
            "operating_release_index_path": (
                "examples/managed-enterprise-operating-release/"
                f"managed-enterprise-operating-release-index.{suffix}"
            ),
            "operating_announcement_path": (
                "examples/managed-enterprise-operating-announcement/"
                f"managed-enterprise-operating-announcement.{suffix}"
            ),
        },
        "redaction_controls": {
            control: True
            for control in sorted(REQUIRED_REDACTION_CONTROLS)
        },
    }


def validate_managed_enterprise_operating_chain(
    manifest: dict[str, Any],
    *,
    base_dir: Path | None = None,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    base = base_dir or Path(".")
    _add_check(
        checks,
        "schema_version",
        "pass" if manifest.get("schema_version") == MANAGED_ENTERPRISE_OPERATING_CHAIN_SCHEMA else "blocker",
        "Operating chain schema is valid."
        if manifest.get("schema_version") == MANAGED_ENTERPRISE_OPERATING_CHAIN_SCHEMA
        else f"Manifest must use {MANAGED_ENTERPRISE_OPERATING_CHAIN_SCHEMA}.",
    )
    _check_evidence_mode(manifest, checks, require_live=require_live)
    _check_ref_object(
        manifest.get("chain_profile", {}),
        checks,
        name="chain_profile",
        required_fields=REQUIRED_PROFILE_FIELDS,
    )
    _check_redaction_controls(manifest.get("redaction_controls", {}), checks)
    forbidden = sorted(find_forbidden_operating_chain_fields(manifest))
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Manifest contains only sanitized references, relative paths, and control booleans."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    artifact_results = _validate_artifacts(
        manifest.get("artifact_paths", {}),
        checks,
        base_dir=base,
        require_live=require_live,
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    child_ready = all(result.get("ready") is True for result in artifact_results.values())
    ready = blocker_count == 0 and warning_count == 0 and child_ready and manifest.get("evidence_mode") == "live"
    return {
        "schema_version": MANAGED_ENTERPRISE_OPERATING_CHAIN_RESULT_SCHEMA,
        "product": manifest.get("product", "CAVRA"),
        "evidence_mode": manifest.get("evidence_mode", "unknown"),
        "ready_for_managed_enterprise_operating_chain": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "artifact_count": len(artifact_results),
        "required_artifact_count": len(REQUIRED_CHAIN_ARTIFACTS),
        "artifact_results": artifact_results,
        "checks": checks,
    }


def write_managed_enterprise_operating_chain_artifacts(output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    sample = build_managed_enterprise_operating_chain_manifest(evidence_mode="sample")
    live = build_managed_enterprise_operating_chain_manifest(evidence_mode="live")
    sample_result = validate_managed_enterprise_operating_chain(sample, require_live=False)
    live_result = validate_managed_enterprise_operating_chain(live, require_live=True)
    written = {
        "sample": output_dir / "managed-enterprise-operating-chain.sample.json",
        "live_sanitized_example": output_dir / "managed-enterprise-operating-chain.live.sanitized.example.json",
        "sample_result": output_dir / "managed-enterprise-operating-chain.sample.result.json",
        "live_result": output_dir / "managed-enterprise-operating-chain.live.sanitized.result.json",
    }
    written["sample"].write_text(json.dumps(sample, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    written["live_sanitized_example"].write_text(json.dumps(live, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    written["sample_result"].write_text(json.dumps(sample_result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    written["live_result"].write_text(json.dumps(live_result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "schema_version": "cavra.managed-enterprise-operating-chain.export.v1",
        "written": {name: str(path) for name, path in written.items()},
        "ready_for_managed_enterprise_operating_chain": live_result["ready_for_managed_enterprise_operating_chain"],
    }


def find_forbidden_operating_chain_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_FIELDS:
                found.add(path)
            found.update(find_forbidden_operating_chain_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(find_forbidden_operating_chain_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _validate_artifacts(
    paths: Any,
    checks: list[dict[str, str]],
    *,
    base_dir: Path,
    require_live: bool,
) -> dict[str, dict[str, Any]]:
    if not isinstance(paths, dict):
        _add_check(checks, "artifact_paths", "blocker", "artifact_paths must be an object.")
        return {}
    results: dict[str, dict[str, Any]] = {}
    missing_fields = sorted(
        str(contract["path_field"])
        for contract in REQUIRED_CHAIN_ARTIFACTS.values()
        if contract["path_field"] not in paths
    )
    if missing_fields:
        _add_check(checks, "artifact_paths", "blocker", f"missing artifact paths: {', '.join(missing_fields)}")
    for artifact_id, contract in REQUIRED_CHAIN_ARTIFACTS.items():
        path_field = str(contract["path_field"])
        raw_path = paths.get(path_field)
        if not _is_safe_relative_path(raw_path):
            _add_check(checks, artifact_id, "blocker", f"{path_field} must be a safe relative path.")
            results[artifact_id] = {"ready": False, "path": raw_path, "blocker_count": 1, "warning_count": 0}
            continue
        artifact_path = (base_dir / raw_path).resolve()
        try:
            payload = json.loads(artifact_path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            _add_check(checks, artifact_id, "blocker", f"{path_field} does not exist: {raw_path}")
            results[artifact_id] = {"ready": False, "path": raw_path, "blocker_count": 1, "warning_count": 0}
            continue
        except json.JSONDecodeError as exc:
            _add_check(checks, artifact_id, "blocker", f"{path_field} is not valid JSON: {exc}")
            results[artifact_id] = {"ready": False, "path": raw_path, "blocker_count": 1, "warning_count": 0}
            continue
        validator: Callable[..., dict[str, Any]] = contract["validator"]
        result = validator(payload, require_live=require_live)
        ready_flag = str(contract["ready_flag"])
        artifact_ready = result.get(ready_flag) is True
        status = "pass" if result.get("blocker_count") == 0 and (not require_live or artifact_ready) else "blocker"
        _add_check(
            checks,
            artifact_id,
            status,
            f"{artifact_id} validates."
            if status == "pass"
            else f"{artifact_id} failed validation or readiness flag {ready_flag}.",
        )
        results[artifact_id] = {
            "ready": artifact_ready,
            "path": raw_path,
            "ready_flag": ready_flag,
            "blocker_count": result.get("blocker_count", 0),
            "warning_count": result.get("warning_count", 0),
        }
    return results


def _check_evidence_mode(manifest: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = manifest.get("evidence_mode")
    sanitized = manifest.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized operating chain supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample operating chain validates shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "Operating chain requires evidence_mode=live and sanitized=true.")


def _check_ref_object(
    value: Any,
    checks: list[dict[str, str]],
    *,
    name: str,
    required_fields: set[str],
) -> None:
    if not isinstance(value, dict):
        _add_check(checks, name, "blocker", f"{name} must be an object.")
        return
    missing = sorted(required_fields - set(value))
    invalid_refs = sorted(
        key
        for key, item in value.items()
        if key in required_fields and not _is_ref(item)
    )
    if missing or invalid_refs:
        details = []
        if missing:
            details.append(f"missing: {', '.join(missing)}")
        if invalid_refs:
            details.append(f"invalid refs: {', '.join(invalid_refs)}")
        _add_check(checks, name, "blocker", "; ".join(details))
    else:
        _add_check(checks, name, "pass", f"{name} references are complete.")


def _check_redaction_controls(controls: Any, checks: list[dict[str, str]]) -> None:
    if not isinstance(controls, dict):
        _add_check(checks, "redaction_controls", "blocker", "redaction_controls must be an object.")
        return
    missing = sorted(REQUIRED_REDACTION_CONTROLS - set(controls))
    false_controls = sorted(key for key in REQUIRED_REDACTION_CONTROLS if controls.get(key) is not True)
    if missing or false_controls:
        details = []
        if missing:
            details.append(f"missing: {', '.join(missing)}")
        if false_controls:
            details.append(f"must be true: {', '.join(false_controls)}")
        _add_check(checks, "redaction_controls", "blocker", "; ".join(details))
    else:
        _add_check(checks, "redaction_controls", "pass", "Redaction controls are asserted.")


def _is_ref(value: Any) -> bool:
    return isinstance(value, str) and value.startswith(ALLOWED_REF_PREFIXES)


def _is_safe_relative_path(value: Any) -> bool:
    if not isinstance(value, str) or not value or value.startswith(("~", "/", "\\")):
        return False
    path = Path(value)
    return not path.is_absolute() and ".." not in path.parts


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})
