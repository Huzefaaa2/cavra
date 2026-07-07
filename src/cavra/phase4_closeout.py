from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

from cavra.certified_connectors import validate_certified_connectors_packet
from cavra.connector_sdk import validate_enterprise_connector_sdk_packet
from cavra.model_registry_connectors import validate_model_registry_connectors_packet
from cavra.zero_trust_scanner import validate_zero_trust_scanner_packet


PHASE4_CLOSEOUT_SCHEMA = "cavra.phase4-connector-scanner.closeout.v1"
PHASE4_CLOSEOUT_RESULT_SCHEMA = "cavra.phase4-connector-scanner.closeout-result.v1"

REQUIRED_PHASE4_GATES = {
    "R4.1": {
        "title": "Connector SDK and certification",
        "packet_path": "examples/connectors/enterprise-connector-sdk.live.sanitized.example.json",
        "ready_key": "ready_for_enterprise_live_connector_certification",
        "validator": "connector_sdk",
        "docs": [
            "docs/connector-sdk-certification.md",
            "docs/connector-sdk-r4-closeout.md",
            "docs/wiki/Connector-SDK-And-Certification.md",
            "docs/wiki/Connector-SDK-And-Certification-R4.1-Closeout.md",
        ],
        "workflow": ".github/workflows/connector-sdk.yml",
        "customer_live_evidence_required": [
            "provider_sandbox_transcript_ref",
            "credential_custody_ref",
            "partner_support_owner_ref",
        ],
    },
    "R4.2": {
        "title": "Priority certified connectors",
        "packet_path": "examples/connectors/enterprise-priority-connectors.live.sanitized.example.json",
        "ready_key": "ready_for_live_priority_connectors",
        "validator": "priority_connectors",
        "docs": [
            "docs/priority-certified-connectors.md",
            "docs/priority-connectors-r4-closeout.md",
            "docs/wiki/Priority-Certified-Connectors.md",
            "docs/wiki/Priority-Certified-Connectors-R4.2-Closeout.md",
        ],
        "workflow": ".github/workflows/priority-connectors.yml",
        "customer_live_evidence_required": [
            "provider_delivery_run_ref",
            "firewall_allowlist_ref",
            "token_rotation_ref",
            "support_escalation_ref",
        ],
    },
    "R4.3": {
        "title": "Model registry connectors",
        "packet_path": (
            "examples/model-registries/"
            "enterprise-model-registry-connectors.live.sanitized.example.json"
        ),
        "ready_key": "ready_for_live_model_registry_connectors",
        "validator": "model_registry_connectors",
        "docs": [
            "docs/model-registry-connectors.md",
            "docs/model-registry-connectors-r4-closeout.md",
            "docs/wiki/Model-Registry-Connectors.md",
            "docs/wiki/Model-Registry-Connectors-R4.3-Closeout.md",
        ],
        "workflow": ".github/workflows/model-registry-connectors.yml",
        "customer_live_evidence_required": [
            "registry_sandbox_ref",
            "model_owner_mapping_ref",
            "artifact_access_control_ref",
            "no_raw_model_egress_run_ref",
        ],
    },
    "R4.4": {
        "title": "Zero-trust scanner agent",
        "packet_path": "examples/zero-trust-scanner/enterprise-zero-trust-scanner.live.sanitized.example.json",
        "ready_key": "ready_for_live_zero_trust_scanner",
        "validator": "zero_trust_scanner",
        "docs": [
            "docs/zero-trust-scanner-agent.md",
            "docs/zero-trust-scanner-r4-closeout.md",
            "docs/wiki/Zero-Trust-Scanner-Agent.md",
            "docs/wiki/Zero-Trust-Scanner-Agent-R4.4-Closeout.md",
        ],
        "workflow": ".github/workflows/zero-trust-scanner.yml",
        "customer_live_evidence_required": [
            "scanner_deployment_ref",
            "private_network_evidence_ref",
            "egress_control_run_ref",
            "incident_drill_ref",
        ],
    },
}


def build_phase4_closeout_packet(repo_root: Path) -> dict[str, Any]:
    gates = []
    for gate_id in sorted(REQUIRED_PHASE4_GATES):
        gate = REQUIRED_PHASE4_GATES[gate_id]
        packet_path = repo_root / str(gate["packet_path"])
        readiness_result = _validate_gate_packet(gate["validator"], _read_json(packet_path))
        gates.append(
            {
                "gate_id": gate_id,
                "title": gate["title"],
                "packet_path": gate["packet_path"],
                "validator": gate["validator"],
                "ready_key": gate["ready_key"],
                "public_contract_ready": _gate_public_ready(
                    readiness_result,
                    str(gate["ready_key"]),
                ),
                "readiness_result": readiness_result,
                "public_artifacts": _public_artifacts_for_gate(gate, include_packet=True),
                "customer_live_evidence_required": gate[
                    "customer_live_evidence_required"
                ],
                "customer_live_evidence": {},
            }
        )
    return {
        "schema_version": PHASE4_CLOSEOUT_SCHEMA,
        "product": "CAVRA",
        "phase": "R4 connector and scanner closeout",
        "evidence_mode": "public_contract_rollup",
        "scope": {
            "public_contracts": (
                "validated from repository source, live-sanitized examples, docs, "
                "and CI workflows"
            ),
            "customer_live_evidence": (
                "not included in the public repository; must be supplied by a "
                "managed or enterprise deployment"
            ),
        },
        "gates": gates,
    }


def validate_phase4_closeout_packet(
    packet: dict[str, Any],
    *,
    repo_root: Path,
    require_customer_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass" if packet.get("schema_version") == PHASE4_CLOSEOUT_SCHEMA else "blocker",
        "Phase 4 closeout schema is valid."
        if packet.get("schema_version") == PHASE4_CLOSEOUT_SCHEMA
        else f"Packet must use {PHASE4_CLOSEOUT_SCHEMA}.",
    )
    gates = packet.get("gates", [])
    gate_by_id = {
        str(gate.get("gate_id")): gate for gate in gates if isinstance(gate, dict)
    }
    missing_gates = sorted(set(REQUIRED_PHASE4_GATES) - set(gate_by_id))
    _add_check(
        checks,
        "required_gates",
        "pass" if not missing_gates else "blocker",
        "All R4 connector and scanner gates are present."
        if not missing_gates
        else f"Missing R4 gates: {', '.join(missing_gates)}.",
    )
    for gate_id in sorted(set(REQUIRED_PHASE4_GATES) & set(gate_by_id)):
        _check_gate(
            gate_id,
            gate_by_id[gate_id],
            checks,
            repo_root=repo_root,
            require_customer_live=require_customer_live,
        )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    public_ready = blocker_count == 0 and all(
        gate_by_id.get(gate_id, {}).get("public_contract_ready") is True
        for gate_id in REQUIRED_PHASE4_GATES
    )
    customer_live_ready = public_ready and require_customer_live and warning_count == 0
    return {
        "schema_version": PHASE4_CLOSEOUT_RESULT_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "phase": packet.get("phase", "R4 connector and scanner closeout"),
        "ready_for_phase4_public_contract_release": public_ready,
        "ready_for_customer_live_phase4_closeout": customer_live_ready,
        "status": "blocked"
        if blocker_count
        else ("ready_with_customer_live_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def write_phase4_closeout_artifacts(repo_root: Path, output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    packet = build_phase4_closeout_packet(repo_root)
    result = validate_phase4_closeout_packet(packet, repo_root=repo_root)
    packet_path = output_dir / "phase4-connector-scanner-closeout.json"
    result_path = output_dir / "phase4-connector-scanner-closeout-result.json"
    packet_path.write_text(
        json.dumps(packet, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    result_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return {
        "schema_version": "cavra.phase4-connector-scanner.closeout-export.v1",
        "written": {
            "packet": str(packet_path),
            "result": str(result_path),
        },
        "ready_for_phase4_public_contract_release": result[
            "ready_for_phase4_public_contract_release"
        ],
        "ready_for_customer_live_phase4_closeout": result[
            "ready_for_customer_live_phase4_closeout"
        ],
    }


def _check_gate(
    gate_id: str,
    gate: dict[str, Any],
    checks: list[dict[str, str]],
    *,
    repo_root: Path,
    require_customer_live: bool,
) -> None:
    expected = REQUIRED_PHASE4_GATES[gate_id]
    readiness_result = gate.get("readiness_result", {})
    ready_key = str(expected["ready_key"])
    ready = gate.get("public_contract_ready") is True and (
        readiness_result.get(ready_key) is True
    )
    _add_check(
        checks,
        f"{gate_id}_public_contract",
        "pass" if ready and int(readiness_result.get("blocker_count", 1)) == 0 else "blocker",
        f"{gate_id} public contract gate is ready."
        if ready
        else f"{gate_id} public contract gate is not ready or has blockers.",
    )
    artifacts = gate.get("public_artifacts", [])
    artifact_paths = [
        str(item.get("path")) for item in artifacts if isinstance(item, dict)
    ]
    expected_paths = [
        str(item["path"])
        for item in _public_artifacts_for_gate(expected, include_packet=True)
    ]
    missing_artifacts = sorted(
        path
        for path in expected_paths
        if path not in artifact_paths or not (repo_root / path).exists()
    )
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
        ref
        for ref in expected["customer_live_evidence_required"]
        if not isinstance(customer_evidence, dict) or not customer_evidence.get(ref)
    ]
    if not missing_customer_refs:
        _add_check(
            checks,
            f"{gate_id}_customer_live_evidence",
            "pass",
            f"{gate_id} customer live evidence refs are present.",
        )
    elif require_customer_live:
        _add_check(
            checks,
            f"{gate_id}_customer_live_evidence",
            "blocker",
            (
                f"{gate_id} customer live evidence refs are missing: "
                f"{', '.join(missing_customer_refs)}."
            ),
        )
    else:
        _add_check(
            checks,
            f"{gate_id}_customer_live_evidence",
            "warn",
            (
                f"{gate_id} customer live evidence remains deployment-specific: "
                f"{', '.join(missing_customer_refs)}."
            ),
        )


def _validate_gate_packet(validator: str, payload: dict[str, Any]) -> dict[str, Any]:
    validators: dict[str, Callable[..., dict[str, Any]]] = {
        "connector_sdk": validate_enterprise_connector_sdk_packet,
        "priority_connectors": validate_certified_connectors_packet,
        "model_registry_connectors": validate_model_registry_connectors_packet,
        "zero_trust_scanner": validate_zero_trust_scanner_packet,
    }
    return validators[validator](payload, require_live=True)


def _gate_public_ready(readiness_result: dict[str, Any], ready_key: str) -> bool:
    return (
        readiness_result.get(ready_key) is True
        and int(readiness_result.get("blocker_count", 1)) == 0
    )


def _public_artifacts_for_gate(
    gate: dict[str, Any],
    *,
    include_packet: bool = False,
) -> list[dict[str, str]]:
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


def _add_check(
    checks: list[dict[str, str]],
    name: str,
    status: str,
    message: str,
) -> None:
    checks.append({"name": name, "status": status, "message": message})
