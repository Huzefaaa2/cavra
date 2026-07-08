from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

from cavra.ai_red_team import validate_ai_red_team_readiness_packet
from cavra.benchmark_slo import validate_benchmark_readiness_packet
from cavra.generic_agent_adapter import validate_generic_adapter_readiness_packet
from cavra.zero_trust_reference_deployments import validate_reference_deployment_readiness_packet


PHASE6_ROLLUP_SCHEMA = "cavra.phase6-ecosystem-expansion.rollup.v1"
PHASE6_ROLLUP_RESULT_SCHEMA = "cavra.phase6-ecosystem-expansion.rollup-result.v1"

REQUIRED_PHASE6_GATES = {
    "R6.1": {
        "title": "Benchmark and SLO regression gates",
        "packet_path": "examples/benchmark-slo/enterprise-benchmark-slo.live.sanitized.example.json",
        "ready_key": "ready_for_live_benchmark_slo_gate",
        "validator": "benchmark_slo",
        "docs": ["docs/benchmark-slo-regression-gates.md", "docs/wiki/Benchmark-SLO-Regression-Gates.md"],
        "workflow": ".github/workflows/benchmark-slo.yml",
        "customer_live_evidence_required": [
            "tenant_benchmark_run_ref",
            "production_ha_evidence_ref",
            "failure_drill_recording_ref",
        ],
    },
    "R6.2": {
        "title": "Generic agent adapter SDK and action taxonomy",
        "packet_path": "examples/generic-adapters/enterprise-generic-agent-adapter.live.sanitized.example.json",
        "ready_key": "ready_for_live_generic_adapter_sdk",
        "validator": "generic_adapter",
        "docs": ["docs/generic-agent-adapter-sdk.md", "docs/wiki/Generic-Agent-Adapter-SDK-And-Action-Taxonomy.md"],
        "workflow": ".github/workflows/generic-agent-adapter.yml",
        "customer_live_evidence_required": [
            "provider_adapter_install_ref",
            "customer_action_fixture_ref",
            "tenant_runtime_evaluation_ref",
        ],
    },
    "R6.3": {
        "title": "AI red-team and supply-chain gates",
        "packet_path": "examples/ai-red-team/enterprise-ai-red-team.live.sanitized.example.json",
        "ready_key": "ready_for_live_ai_red_team_gate",
        "validator": "ai_red_team",
        "docs": ["docs/ai-red-team-and-supply-chain-gates.md", "docs/wiki/AI-Red-Team-And-Supply-Chain-Gates.md"],
        "workflow": ".github/workflows/ai-red-team.yml",
        "customer_live_evidence_required": [
            "customer_prompt_suite_ref",
            "customer_scanner_plugin_ref",
            "red_team_closeout_ref",
        ],
    },
    "R6.4": {
        "title": "Zero-trust reference deployments",
        "packet_path": "examples/reference-deployments/zero-trust-reference-deployments.live.sanitized.example.json",
        "ready_key": "ready_for_live_zero_trust_reference_deployments",
        "validator": "zero_trust_reference_deployments",
        "docs": ["docs/zero-trust-reference-deployments.md", "docs/wiki/Zero-Trust-Reference-Deployments.md"],
        "workflow": ".github/workflows/zero-trust-reference-deployments.yml",
        "customer_live_evidence_required": [
            "docker_compose_smoke_ref",
            "helm_template_ref",
            "terraform_validate_ref",
            "azure_what_if_ref",
            "scanner_operation_ref",
        ],
    },
}


def build_phase6_rollup_packet(repo_root: Path) -> dict[str, Any]:
    gates = []
    for gate_id in sorted(REQUIRED_PHASE6_GATES):
        gate = REQUIRED_PHASE6_GATES[gate_id]
        packet_path = repo_root / str(gate["packet_path"])
        readiness_result = _validate_gate_packet(
            gate["validator"],
            _read_json(packet_path),
            repo_root=repo_root,
        )
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
        "schema_version": PHASE6_ROLLUP_SCHEMA,
        "product": "CAVRA",
        "phase": "R6 ecosystem expansion",
        "evidence_mode": "public_contract_rollup",
        "scope": {
            "public_contracts": "validated from repository source, examples, docs, and CI workflows",
            "customer_live_evidence": "not included in public repository; must be supplied by a live deployment",
        },
        "gates": gates,
    }


def validate_phase6_rollup_packet(
    packet: dict[str, Any],
    *,
    repo_root: Path,
    require_customer_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass" if packet.get("schema_version") == PHASE6_ROLLUP_SCHEMA else "blocker",
        "Phase 6 rollup schema is valid."
        if packet.get("schema_version") == PHASE6_ROLLUP_SCHEMA
        else f"Packet must use {PHASE6_ROLLUP_SCHEMA}.",
    )
    gates = packet.get("gates", [])
    gate_by_id = {str(gate.get("gate_id")): gate for gate in gates if isinstance(gate, dict)}
    missing_gates = sorted(set(REQUIRED_PHASE6_GATES) - set(gate_by_id))
    _add_check(
        checks,
        "required_gates",
        "pass" if not missing_gates else "blocker",
        "All R6 gates are present." if not missing_gates else f"Missing R6 gates: {', '.join(missing_gates)}.",
    )
    for gate_id in sorted(set(REQUIRED_PHASE6_GATES) & set(gate_by_id)):
        _check_gate(gate_id, gate_by_id[gate_id], checks, repo_root=repo_root, require_customer_live=require_customer_live)
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    public_ready = blocker_count == 0 and all(
        gate_by_id.get(gate_id, {}).get("public_contract_ready") is True for gate_id in REQUIRED_PHASE6_GATES
    )
    customer_live_ready = public_ready and require_customer_live and warning_count == 0
    return {
        "schema_version": PHASE6_ROLLUP_RESULT_SCHEMA,
        "product": packet.get("product", "CAVRA"),
        "phase": packet.get("phase", "R6 ecosystem expansion"),
        "ready_for_phase6_public_contract_release": public_ready,
        "ready_for_customer_live_phase6_closeout": customer_live_ready,
        "status": "blocked" if blocker_count else ("ready_with_customer_live_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def write_phase6_rollup_artifacts(repo_root: Path, output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    packet = build_phase6_rollup_packet(repo_root)
    result = validate_phase6_rollup_packet(packet, repo_root=repo_root)
    packet_path = output_dir / "phase6-ecosystem-rollup.json"
    result_path = output_dir / "phase6-ecosystem-rollup-result.json"
    packet_path.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "schema_version": "cavra.phase6-ecosystem-expansion.rollup-export.v1",
        "written": {
            "packet": str(packet_path),
            "result": str(result_path),
        },
        "ready_for_phase6_public_contract_release": result["ready_for_phase6_public_contract_release"],
        "ready_for_customer_live_phase6_closeout": result["ready_for_customer_live_phase6_closeout"],
    }


def _check_gate(
    gate_id: str,
    gate: dict[str, Any],
    checks: list[dict[str, str]],
    *,
    repo_root: Path,
    require_customer_live: bool,
) -> None:
    expected = REQUIRED_PHASE6_GATES[gate_id]
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


def _validate_gate_packet(validator: str, payload: dict[str, Any], *, repo_root: Path) -> dict[str, Any]:
    validators: dict[str, Callable[..., dict[str, Any]]] = {
        "benchmark_slo": validate_benchmark_readiness_packet,
        "generic_adapter": validate_generic_adapter_readiness_packet,
        "ai_red_team": validate_ai_red_team_readiness_packet,
        "zero_trust_reference_deployments": validate_reference_deployment_readiness_packet,
    }
    if validator == "zero_trust_reference_deployments":
        return validators[validator](payload, repo_root=repo_root, require_live=True)
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
