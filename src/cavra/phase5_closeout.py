from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

from cavra.continuous_monitoring import validate_continuous_monitoring_packet
from cavra.opa_rego_policy import validate_opa_rego_policy_packet
from cavra.policy_lifecycle import validate_policy_lifecycle_packet


PHASE5_CLOSEOUT_SCHEMA = "cavra.phase5-policy-event-core.closeout.v1"
PHASE5_CLOSEOUT_RESULT_SCHEMA = "cavra.phase5-policy-event-core.closeout-result.v1"

REQUIRED_PHASE5_GATES = {
    "R5.1": {
        "title": "OPA/Rego policy path",
        "packet_path": "examples/opa-rego/enterprise-opa-rego-policy.live.sanitized.example.json",
        "ready_key": "ready_for_live_opa_rego_policy_path",
        "validator": "opa_rego_policy",
        "docs": [
            "docs/policy-opa-rego-path.md",
            "docs/wiki/OPA-Rego-Policy-Path.md",
        ],
        "workflow": ".github/workflows/opa-rego-policy.yml",
        "customer_live_evidence_required": [
            "customer_policy_pr_ref",
            "opa_runtime_deployment_ref",
            "policy_review_approval_ref",
        ],
    },
    "R5.2": {
        "title": "Policy lifecycle tooling",
        "packet_path": "examples/policy-lifecycle/enterprise-policy-lifecycle.live.sanitized.example.json",
        "ready_key": "ready_for_live_policy_lifecycle",
        "validator": "policy_lifecycle",
        "docs": [
            "docs/policy-lifecycle-tooling.md",
            "docs/wiki/Policy-Lifecycle-Tooling.md",
        ],
        "workflow": ".github/workflows/policy-lifecycle.yml",
        "customer_live_evidence_required": [
            "customer_ui_validation_ref",
            "policy_rollout_approval_ref",
            "rollback_rehearsal_ref",
        ],
    },
    "R5.3": {
        "title": "Continuous monitoring event core",
        "packet_path": "examples/continuous-monitoring/enterprise-continuous-monitoring.live.sanitized.example.json",
        "ready_key": "ready_for_live_continuous_monitoring",
        "validator": "continuous_monitoring",
        "docs": [
            "docs/continuous-monitoring-event-core.md",
            "docs/wiki/Continuous-Monitoring-Event-Core.md",
        ],
        "workflow": ".github/workflows/continuous-monitoring.yml",
        "customer_live_evidence_required": [
            "customer_event_bus_config_ref",
            "monitor_dashboard_ref",
            "event_bus_evidence_ref",
        ],
    },
}


def build_phase5_closeout_packet(repo_root: Path) -> dict[str, Any]:
    gates = []
    for gate_id in sorted(REQUIRED_PHASE5_GATES):
        gate = REQUIRED_PHASE5_GATES[gate_id]
        packet_path = repo_root / str(gate["packet_path"])
        readiness_result = _validate_gate_packet(gate["validator"], _read_json(packet_path))
        gates.append(
            {
                "gate_id": gate_id,
                "title": gate["title"],
                "packet_path": gate["packet_path"],
                "validator": gate["validator"],
                "ready_key": gate["ready_key"],
                "public_contract_ready": _gate_public_ready(readiness_result, str(gate["ready_key"])),
                "readiness_result": readiness_result,
                "public_artifacts": _public_artifacts_for_gate(gate, include_packet=True),
                "customer_live_evidence_required": gate["customer_live_evidence_required"],
                "customer_live_evidence": {},
            }
        )
    return {
        "schema_version": PHASE5_CLOSEOUT_SCHEMA,
        "product": "CAVRA",
        "phase": "R5 policy lifecycle and event core closeout",
        "evidence_mode": "public_contract_rollup",
        "scope": {
            "public_contracts": "validated from repository source, live-sanitized examples, docs, and CI workflows",
            "customer_live_evidence": "not included in the public repository; must be supplied by a managed or enterprise deployment",
        },
        "gates": gates,
    }


def validate_phase5_closeout_packet(
    packet: dict[str, Any],
    *,
    repo_root: Path,
    require_customer_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass" if packet.get("schema_version") == PHASE5_CLOSEOUT_SCHEMA else "blocker",
        "Phase 5 closeout schema is valid."
        if packet.get("schema_version") == PHASE5_CLOSEOUT_SCHEMA
        else f"Packet must use {PHASE5_CLOSEOUT_SCHEMA}.",
    )
    gates = packet.get("gates", [])
    gate_by_id = {str(gate.get("gate_id")): gate for gate in gates if isinstance(gate, dict)}
    missing_gates = sorted(set(REQUIRED_PHASE5_GATES) - set(gate_by_id))
    _add_check(
        checks,
        "required_gates",
        "pass" if not missing_gates else "blocker",
        "All R5 policy lifecycle and event core gates are present."
        if not missing_gates
        else f"Missing R5 gates: {', '.join(missing_gates)}.",
    )
    for gate_id in sorted(set(REQUIRED_PHASE5_GATES) & set(gate_by_id)):
        _check_gate(gate_id, gate_by_id[gate_id], checks, repo_root=repo_root, require_customer_live=require_customer_live)
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    public_ready = blocker_count == 0 and all(
        gate_by_id.get(gate_id, {}).get("public_contract_ready") is True for gate_id in REQUIRED_PHASE5_GATES
    )
    customer_live_ready = public_ready and require_customer_live and warning_count == 0
    return {
        "schema_version": PHASE5_CLOSEOUT_RESULT_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "phase": packet.get("phase", "R5 policy lifecycle and event core closeout"),
        "ready_for_phase5_public_contract_release": public_ready,
        "ready_for_customer_live_phase5_closeout": customer_live_ready,
        "status": "blocked" if blocker_count else ("ready_with_customer_live_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def write_phase5_closeout_artifacts(repo_root: Path, output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    packet = build_phase5_closeout_packet(repo_root)
    result = validate_phase5_closeout_packet(packet, repo_root=repo_root)
    packet_path = output_dir / "phase5-policy-event-core-closeout.json"
    result_path = output_dir / "phase5-policy-event-core-closeout-result.json"
    packet_path.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "schema_version": "cavra.phase5-policy-event-core.closeout-export.v1",
        "written": {
            "packet": str(packet_path),
            "result": str(result_path),
        },
        "ready_for_phase5_public_contract_release": result["ready_for_phase5_public_contract_release"],
        "ready_for_customer_live_phase5_closeout": result["ready_for_customer_live_phase5_closeout"],
    }


def _check_gate(
    gate_id: str,
    gate: dict[str, Any],
    checks: list[dict[str, str]],
    *,
    repo_root: Path,
    require_customer_live: bool,
) -> None:
    expected = REQUIRED_PHASE5_GATES[gate_id]
    readiness_result = gate.get("readiness_result", {})
    ready_key = str(expected["ready_key"])
    ready = gate.get("public_contract_ready") is True and readiness_result.get(ready_key) is True
    _add_check(
        checks,
        f"{gate_id}_public_contract",
        "pass" if ready and int(readiness_result.get("blocker_count", 1)) == 0 else "blocker",
        f"{gate_id} public contract gate is ready."
        if ready
        else f"{gate_id} public contract gate is not ready or has blockers.",
    )
    artifacts = gate.get("public_artifacts", [])
    artifact_paths = [str(item.get("path")) for item in artifacts if isinstance(item, dict)]
    expected_paths = [str(item["path"]) for item in _public_artifacts_for_gate(expected, include_packet=True)]
    missing_artifacts = sorted(path for path in expected_paths if path not in artifact_paths or not (repo_root / path).exists())
    _add_check(
        checks,
        f"{gate_id}_public_artifacts",
        "pass" if not missing_artifacts else "blocker",
        f"{gate_id} public artifacts are present."
        if not missing_artifacts
        else f"{gate_id} missing public artifacts: {', '.join(missing_artifacts)}.",
    )
    customer_evidence = gate.get("customer_live_evidence", {})
    missing_customer_refs = [
        ref for ref in expected["customer_live_evidence_required"] if not isinstance(customer_evidence, dict) or not customer_evidence.get(ref)
    ]
    if not missing_customer_refs:
        _add_check(checks, f"{gate_id}_customer_live_evidence", "pass", f"{gate_id} customer live evidence refs are present.")
    elif require_customer_live:
        _add_check(
            checks,
            f"{gate_id}_customer_live_evidence",
            "blocker",
            f"{gate_id} customer live evidence refs are missing: {', '.join(missing_customer_refs)}.",
        )
    else:
        _add_check(
            checks,
            f"{gate_id}_customer_live_evidence",
            "warn",
            f"{gate_id} customer live evidence remains deployment-specific: {', '.join(missing_customer_refs)}.",
        )


def _validate_gate_packet(validator: str, payload: dict[str, Any]) -> dict[str, Any]:
    validators: dict[str, Callable[..., dict[str, Any]]] = {
        "opa_rego_policy": validate_opa_rego_policy_packet,
        "policy_lifecycle": validate_policy_lifecycle_packet,
        "continuous_monitoring": validate_continuous_monitoring_packet,
    }
    return validators[validator](payload, require_live=True)


def _gate_public_ready(readiness_result: dict[str, Any], ready_key: str) -> bool:
    return readiness_result.get(ready_key) is True and int(readiness_result.get("blocker_count", 1)) == 0


def _public_artifacts_for_gate(gate: dict[str, Any], *, include_packet: bool = False) -> list[dict[str, str]]:
    paths = []
    if include_packet:
        paths.append(str(gate["packet_path"]))
    paths.extend(str(path) for path in gate["docs"])
    paths.append(str(gate["workflow"]))
    return [{"path": path, "kind": _artifact_kind(path)} for path in paths]


def _artifact_kind(path: str) -> str:
    if path.startswith(".github/workflows/"):
        return "ci_workflow"
    if path.startswith("docs/wiki/"):
        return "wiki_doc"
    return "repo_doc"


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})
