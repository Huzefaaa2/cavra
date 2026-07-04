from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from cavra.runtime import ActionDecision, RuntimeGuard

GENERIC_ADAPTER_MANIFEST_SCHEMA = "cavra.generic-agent-adapter.manifest.v1"
GENERIC_ACTION_TAXONOMY_SCHEMA = "cavra.generic-agent-adapter.taxonomy.v1"
GENERIC_ACTION_EVALUATION_SCHEMA = "cavra.generic-agent-adapter.evaluation.v1"
GENERIC_ADAPTER_READINESS_SCHEMA = "cavra.generic-agent-adapter.readiness.v1"

SUPPORTED_ADAPTER_DOMAINS = {
    "engineering",
    "identity",
    "data",
    "finance",
    "sales",
    "support",
    "model_governance",
    "communications",
    "workflow",
}
SUPPORTED_ACTION_EFFECTS = {"read", "write", "delete", "approve", "grant", "export", "promote", "send", "execute"}
SUPPORTED_RISK_LEVELS = {"low", "medium", "high", "critical"}
REQUIRED_READINESS_ARTIFACTS = {
    "taxonomy_schema",
    "adapter_manifest_schema",
    "sample_adapter_manifest",
    "sample_action_fixture",
    "evaluation_report",
    "ci_validator",
}

ACTION_TAXONOMY: dict[str, dict[str, Any]] = {
    "knowledge.search": {"domain": "data", "effect": "read", "risk_level": "low", "default_decision": "allow"},
    "ticket.summarize": {"domain": "support", "effect": "read", "risk_level": "low", "default_decision": "allow"},
    "crm.update_record": {"domain": "sales", "effect": "write", "risk_level": "medium", "default_decision": "require_approval"},
    "customer.email_send": {
        "domain": "communications",
        "effect": "send",
        "risk_level": "medium",
        "default_decision": "require_approval",
    },
    "data.export_dataset": {"domain": "data", "effect": "export", "risk_level": "high", "default_decision": "require_approval"},
    "model.promote": {
        "domain": "model_governance",
        "effect": "promote",
        "risk_level": "high",
        "default_decision": "require_approval",
    },
    "identity.grant_role": {"domain": "identity", "effect": "grant", "risk_level": "critical", "default_decision": "block"},
    "finance.release_payment": {"domain": "finance", "effect": "approve", "risk_level": "critical", "default_decision": "block"},
    "workflow.close_control": {"domain": "workflow", "effect": "approve", "risk_level": "high", "default_decision": "require_approval"},
}

RUNTIME_ACTION_TYPES = {"read_file", "write_file", "execute_command", "git_operation", "mcp_tool_call"}
APPROVAL_EFFECTS = {"write", "delete", "approve", "grant", "export", "promote", "send", "execute"}
BLOCKED_CRITICAL_ACTIONS = {"identity.grant_role", "finance.release_payment"}


@dataclass(frozen=True)
class GenericAgentAction:
    action_id: str
    adapter_id: str
    action_type: str
    target: str
    requested_operation: str
    agent_id: str = "generic-agent"
    actor: str = "ai-agent"
    tenant_id: str | None = None
    workspace_id: str | None = None
    risk_level: str | None = None
    metadata: dict[str, Any] | None = None

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> GenericAgentAction:
        return cls(
            action_id=str(payload.get("action_id") or payload.get("id") or "generic-action"),
            adapter_id=str(payload.get("adapter_id") or "unknown-adapter"),
            action_type=str(payload.get("action_type") or "unknown.action"),
            target=str(payload.get("target") or ""),
            requested_operation=str(payload.get("requested_operation") or payload.get("operation") or ""),
            agent_id=str(payload.get("agent_id") or "generic-agent"),
            actor=str(payload.get("actor") or "ai-agent"),
            tenant_id=_optional_string(payload.get("tenant_id")),
            workspace_id=_optional_string(payload.get("workspace_id")),
            risk_level=_optional_string(payload.get("risk_level")),
            metadata=payload.get("metadata", {}) if isinstance(payload.get("metadata", {}), dict) else {},
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "action_id": self.action_id,
            "adapter_id": self.adapter_id,
            "action_type": self.action_type,
            "target": self.target,
            "requested_operation": self.requested_operation,
            "agent_id": self.agent_id,
            "actor": self.actor,
            "tenant_id": self.tenant_id,
            "workspace_id": self.workspace_id,
            "risk_level": self.risk_level,
            "metadata": self.metadata or {},
        }


def build_action_taxonomy() -> dict[str, Any]:
    return {
        "schema_version": GENERIC_ACTION_TAXONOMY_SCHEMA,
        "product": "CAVRA",
        "domains": sorted(SUPPORTED_ADAPTER_DOMAINS),
        "effects": sorted(SUPPORTED_ACTION_EFFECTS),
        "risk_levels": sorted(SUPPORTED_RISK_LEVELS),
        "actions": [
            {"action_type": action_type, **details} for action_type, details in sorted(ACTION_TAXONOMY.items())
        ],
        "runtime_mappings": {
            "read_file": "RuntimeGuard.evaluate_file_access(read)",
            "write_file": "RuntimeGuard.evaluate_file_access(write)",
            "execute_command": "RuntimeGuard.evaluate_command",
            "git_operation": "RuntimeGuard.evaluate_git_action",
            "mcp_tool_call": "RuntimeGuard.evaluate_mcp_tool_call",
            "generic_non_coding": "Generic action taxonomy policy",
        },
    }


def build_sample_adapter_manifest() -> dict[str, Any]:
    return {
        "schema_version": GENERIC_ADAPTER_MANIFEST_SCHEMA,
        "adapter_id": "cavra-reference-business-agent",
        "display_name": "CAVRA Reference Business Agent Adapter",
        "version": "2026.07",
        "domains": ["data", "identity", "sales", "support", "model_governance"],
        "supported_actions": [
            "knowledge.search",
            "ticket.summarize",
            "crm.update_record",
            "data.export_dataset",
            "identity.grant_role",
            "model.promote",
        ],
        "runtime_contract": {
            "pre_action_evaluation_required": True,
            "decision_required_before_execution": True,
            "evidence_ref_required_after_execution": True,
            "fail_closed_on_cavra_unavailable": True,
        },
        "security": {
            "tenant_scope_required": True,
            "workspace_scope_required": True,
            "raw_secret_egress_allowed": False,
            "raw_customer_data_egress_allowed": False,
            "human_approval_supported": True,
        },
        "compatibility": {
            "taxonomy_schema": GENERIC_ACTION_TAXONOMY_SCHEMA,
            "cavra_versions": ["1.0.0"],
            "api_contract": "openapi/cavra-api.openapi.json",
        },
    }


def build_sample_generic_actions() -> list[dict[str, Any]]:
    return [
        {
            "action_id": "generic-action-001",
            "adapter_id": "cavra-reference-business-agent",
            "agent_id": "support-copilot",
            "actor": "ai-agent",
            "tenant_id": "tenant-sample",
            "workspace_id": "workspace-support",
            "action_type": "ticket.summarize",
            "target": "ticket/INC-1042",
            "requested_operation": "summarize ticket and recommend response",
            "metadata": {"system": "servicedesk", "contains_customer_data": False},
        },
        {
            "action_id": "generic-action-002",
            "adapter_id": "cavra-reference-business-agent",
            "agent_id": "revenue-copilot",
            "actor": "ai-agent",
            "tenant_id": "tenant-sample",
            "workspace_id": "workspace-sales",
            "action_type": "crm.update_record",
            "target": "account/acme-corp",
            "requested_operation": "update renewal stage and next-step note",
            "metadata": {"system": "crm", "business_impact": "customer-facing"},
        },
        {
            "action_id": "generic-action-003",
            "adapter_id": "cavra-reference-business-agent",
            "agent_id": "identity-copilot",
            "actor": "ai-agent",
            "tenant_id": "tenant-sample",
            "workspace_id": "workspace-identity",
            "action_type": "identity.grant_role",
            "target": "user/alex@example.com",
            "requested_operation": "grant global administrator",
            "metadata": {"privilege": "global_admin", "system": "entra_id"},
        },
        {
            "action_id": "generic-action-004",
            "adapter_id": "cavra-reference-business-agent",
            "agent_id": "mlops-copilot",
            "actor": "ai-agent",
            "tenant_id": "tenant-sample",
            "workspace_id": "workspace-ml",
            "action_type": "model.promote",
            "target": "model/fraud-detector:v42",
            "requested_operation": "promote candidate model to production",
            "metadata": {"registry": "mlflow", "approval_ticket": "MLGOV-221"},
        },
    ]


def validate_adapter_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _add_check(
        checks,
        "schema_version",
        "pass" if manifest.get("schema_version") == GENERIC_ADAPTER_MANIFEST_SCHEMA else "blocker",
        "Generic adapter manifest schema is valid."
        if manifest.get("schema_version") == GENERIC_ADAPTER_MANIFEST_SCHEMA
        else f"Manifest must use {GENERIC_ADAPTER_MANIFEST_SCHEMA}.",
    )
    _add_check(
        checks,
        "identity",
        "pass" if manifest.get("adapter_id") and manifest.get("version") else "blocker",
        "Adapter identity and version are declared.",
    )
    domains = set(manifest.get("domains", []) if isinstance(manifest.get("domains"), list) else [])
    unsupported_domains = sorted(domains - SUPPORTED_ADAPTER_DOMAINS)
    _add_check(
        checks,
        "domains",
        "pass" if domains and not unsupported_domains else "blocker",
        "Adapter domains are supported."
        if domains and not unsupported_domains
        else f"Unsupported or missing adapter domains: {', '.join(unsupported_domains) or 'none declared'}.",
    )
    supported_actions = set(manifest.get("supported_actions", []) if isinstance(manifest.get("supported_actions"), list) else [])
    unsupported_actions = sorted(supported_actions - set(ACTION_TAXONOMY))
    _add_check(
        checks,
        "supported_actions",
        "pass" if supported_actions and not unsupported_actions else "blocker",
        "Adapter supported actions map to the public CAVRA taxonomy."
        if supported_actions and not unsupported_actions
        else f"Unsupported or missing actions: {', '.join(unsupported_actions) or 'none declared'}.",
    )
    runtime = manifest.get("runtime_contract", {}) if isinstance(manifest.get("runtime_contract"), dict) else {}
    runtime_ok = all(
        runtime.get(flag) is True
        for flag in [
            "pre_action_evaluation_required",
            "decision_required_before_execution",
            "evidence_ref_required_after_execution",
            "fail_closed_on_cavra_unavailable",
        ]
    )
    _add_check(
        checks,
        "runtime_contract",
        "pass" if runtime_ok else "blocker",
        "Adapter runtime contract requires pre-action CAVRA decisions and fail-closed behavior.",
    )
    security = manifest.get("security", {}) if isinstance(manifest.get("security"), dict) else {}
    security_ok = (
        security.get("tenant_scope_required") is True
        and security.get("workspace_scope_required") is True
        and security.get("raw_secret_egress_allowed") is False
        and security.get("raw_customer_data_egress_allowed") is False
    )
    _add_check(
        checks,
        "security",
        "pass" if security_ok else "blocker",
        "Adapter security boundary prevents raw secret/customer-data egress and requires scope.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    return {
        "schema_version": "cavra.generic-agent-adapter.manifest-validation.v1",
        "adapter_id": manifest.get("adapter_id", "unknown"),
        "valid": blocker_count == 0,
        "blocker_count": blocker_count,
        "checks": checks,
    }


def evaluate_generic_action(action: GenericAgentAction | dict[str, Any], *, policy_pack: str = "cavra-ai-agent-baseline") -> dict[str, Any]:
    normalized = action if isinstance(action, GenericAgentAction) else GenericAgentAction.from_dict(action)
    guard = RuntimeGuard(
        policy_pack=policy_pack,
        session_id=f"generic-adapter:{normalized.adapter_id}",
        agent_id=normalized.agent_id,
        actor=normalized.actor,
    )
    if normalized.action_type in RUNTIME_ACTION_TYPES:
        decision = _evaluate_runtime_action(guard, normalized)
    else:
        decision = _evaluate_taxonomy_action(guard, normalized)
    payload = decision.to_dict()
    payload.update(
        {
            "schema_version": GENERIC_ACTION_EVALUATION_SCHEMA,
            "action_id": normalized.action_id,
            "adapter_id": normalized.adapter_id,
            "tenant_id": normalized.tenant_id,
            "workspace_id": normalized.workspace_id,
            "taxonomy": _taxonomy_entry(normalized.action_type),
            "metadata_summary": _metadata_summary(normalized.metadata or {}),
        }
    )
    return payload


def evaluate_generic_actions(actions: list[dict[str, Any]], *, policy_pack: str = "cavra-ai-agent-baseline") -> dict[str, Any]:
    evaluations = [evaluate_generic_action(action, policy_pack=policy_pack) for action in actions]
    return {
        "schema_version": "cavra.generic-agent-adapter.evaluation-report.v1",
        "product": "CAVRA",
        "generated_at": _now(),
        "policy_pack": policy_pack,
        "action_count": len(evaluations),
        "decision_counts": _decision_counts(evaluations),
        "evaluations": evaluations,
    }


def build_generic_adapter_readiness_packet(
    manifest: dict[str, Any],
    evaluations: dict[str, Any],
    *,
    evidence_mode: str = "sample",
    ci_run_ref: str = "sample://github-actions/generic-agent-adapter",
    taxonomy_ref: str = "artifact://generic-adapters/action-taxonomy.json",
    adapter_test_ref: str = "artifact://generic-adapters/evaluation-report.json",
    non_coding_scenario_ref: str = "sample://generic-adapters/non-coding-agent-actions",
) -> dict[str, Any]:
    return {
        "schema_version": GENERIC_ADAPTER_READINESS_SCHEMA,
        "product": "CAVRA",
        "evidence_mode": evidence_mode,
        "adapter_manifest": manifest,
        "manifest_validation": validate_adapter_manifest(manifest),
        "taxonomy": build_action_taxonomy(),
        "evaluation_report": evaluations,
        "readiness_artifacts": sorted(REQUIRED_READINESS_ARTIFACTS),
        "operating_evidence": {
            "ci_run_ref": ci_run_ref,
            "taxonomy_ref": taxonomy_ref,
            "adapter_test_ref": adapter_test_ref,
            "non_coding_scenario_ref": non_coding_scenario_ref,
        },
    }


def validate_generic_adapter_readiness_packet(packet: dict[str, Any], *, require_live: bool = False) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    _check_packet_schema(packet, checks)
    _check_evidence_mode(packet, checks, require_live=require_live)
    manifest = packet.get("adapter_manifest", {}) if isinstance(packet.get("adapter_manifest"), dict) else {}
    manifest_validation = validate_adapter_manifest(manifest)
    _add_check(
        checks,
        "adapter_manifest",
        "pass" if manifest_validation["valid"] else "blocker",
        "Adapter manifest validates against the generic adapter SDK contract."
        if manifest_validation["valid"]
        else "Adapter manifest has blockers.",
    )
    taxonomy = packet.get("taxonomy", {}) if isinstance(packet.get("taxonomy"), dict) else {}
    _add_check(
        checks,
        "taxonomy",
        "pass" if _taxonomy_valid(taxonomy) else "blocker",
        "Action taxonomy is present and complete.",
    )
    report = packet.get("evaluation_report", {}) if isinstance(packet.get("evaluation_report"), dict) else {}
    _add_check(
        checks,
        "non_coding_scenario",
        "pass" if _scenario_valid(report) else "blocker",
        "Non-coding agent scenario covers allow, approval, and block decisions.",
    )
    artifacts = set(packet.get("readiness_artifacts", []) if isinstance(packet.get("readiness_artifacts"), list) else [])
    missing_artifacts = sorted(REQUIRED_READINESS_ARTIFACTS - artifacts)
    _add_check(
        checks,
        "readiness_artifacts",
        "pass" if not missing_artifacts else "blocker",
        "Required generic adapter readiness artifacts are listed."
        if not missing_artifacts
        else f"Missing readiness artifacts: {', '.join(missing_artifacts)}.",
    )
    _check_operating_evidence(packet.get("operating_evidence", {}), checks)
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    contract_ready = blocker_count == 0
    live_ready = contract_ready and packet.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": "cavra.generic-agent-adapter.readiness-result.v1",
        "product": "CAVRA",
        "evidence_mode": packet.get("evidence_mode", "unknown"),
        "ready_for_generic_adapter_contract": contract_ready,
        "ready_for_live_generic_adapter_sdk": live_ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def write_generic_adapter_artifacts(manifest: dict[str, Any], actions: list[dict[str, Any]], output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    taxonomy = build_action_taxonomy()
    evaluations = evaluate_generic_actions(actions)
    packet = build_generic_adapter_readiness_packet(manifest, evaluations)
    taxonomy_path = output_dir / "action-taxonomy.json"
    manifest_path = output_dir / "adapter-manifest.json"
    actions_path = output_dir / "non-coding-agent-actions.json"
    evaluation_path = output_dir / "evaluation-report.json"
    packet_path = output_dir / "generic-agent-adapter-readiness-packet.json"
    taxonomy_path.write_text(json.dumps(taxonomy, indent=2) + "\n", encoding="utf-8")
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    actions_path.write_text(json.dumps({"actions": actions}, indent=2) + "\n", encoding="utf-8")
    evaluation_path.write_text(json.dumps(evaluations, indent=2) + "\n", encoding="utf-8")
    packet_path.write_text(json.dumps(packet, indent=2) + "\n", encoding="utf-8")
    return {
        "schema_version": "cavra.generic-agent-adapter.export.v1",
        "output_dir": str(output_dir),
        "artifacts": {
            "taxonomy": str(taxonomy_path),
            "adapter_manifest": str(manifest_path),
            "sample_actions": str(actions_path),
            "evaluation_report": str(evaluation_path),
            "readiness_packet": str(packet_path),
        },
    }


def _evaluate_runtime_action(guard: RuntimeGuard, action: GenericAgentAction) -> ActionDecision:
    if action.action_type == "read_file":
        return guard.evaluate_file_access(Path(action.target), "read")
    if action.action_type == "write_file":
        return guard.evaluate_file_access(Path(action.target), "write")
    if action.action_type == "execute_command":
        return guard.evaluate_command(action.requested_operation or action.target)
    if action.action_type == "git_operation":
        return guard.evaluate_git_action(action.requested_operation or "push", action.target)
    return guard.evaluate_mcp_tool_call(
        str((action.metadata or {}).get("server") or action.target.split(":", 1)[0]),
        str((action.metadata or {}).get("tool") or "unknown"),
        str((action.metadata or {}).get("capability") or action.requested_operation or action.action_type),
    )


def _evaluate_taxonomy_action(guard: RuntimeGuard, action: GenericAgentAction) -> ActionDecision:
    taxonomy = _taxonomy_entry(action.action_type)
    risk_level = action.risk_level or taxonomy.get("risk_level", "medium")
    effect = str(taxonomy.get("effect", "write"))
    default_decision = str(taxonomy.get("default_decision", "require_approval"))
    if action.action_type not in ACTION_TAXONOMY:
        return guard._decision(
            "require_approval",
            "Generic action is outside the public taxonomy; review required.",
            action_type=action.action_type,
            target=action.target,
            requested_operation=action.requested_operation,
            rule_id="generic_adapter.taxonomy.unknown.require_approval",
            severity="medium",
            approver_group="Generic Adapter Owners",
        )
    if action.action_type in BLOCKED_CRITICAL_ACTIONS:
        return guard._decision(
            "block",
            f"{action.action_type} is a critical non-coding action and cannot execute without a certified private adapter flow.",
            action_type=action.action_type,
            target=action.target,
            requested_operation=action.requested_operation,
            rule_id=f"generic_adapter.{effect}.critical.block",
            severity="critical",
            approver_group="Security Operations",
        )
    if default_decision == "allow" and risk_level == "low":
        return guard._decision(
            "allow",
            "Low-risk generic action is read-only and allowed by taxonomy.",
            action_type=action.action_type,
            target=action.target,
            requested_operation=action.requested_operation,
            rule_id=f"generic_adapter.{effect}.allow",
            severity="low",
        )
    if effect in APPROVAL_EFFECTS:
        return guard._decision(
            "require_approval",
            f"{action.action_type} changes business state; approval is required before execution.",
            action_type=action.action_type,
            target=action.target,
            requested_operation=action.requested_operation,
            rule_id=f"generic_adapter.{effect}.require_approval",
            severity=str(risk_level),
            approver_group=_approver_group_for_domain(str(taxonomy.get("domain", "workflow"))),
        )
    return guard._decision(
        "require_approval",
        "Generic action effect is not explicitly allowed; review required.",
        action_type=action.action_type,
        target=action.target,
        requested_operation=action.requested_operation,
        rule_id="generic_adapter.default.require_approval",
        severity=str(risk_level),
        approver_group="Generic Adapter Owners",
    )


def _taxonomy_entry(action_type: str) -> dict[str, Any]:
    return ACTION_TAXONOMY.get(
        action_type,
        {"domain": "workflow", "effect": "write", "risk_level": "medium", "default_decision": "require_approval"},
    )


def _metadata_summary(metadata: dict[str, Any]) -> dict[str, Any]:
    return {
        "keys": sorted(str(key) for key in metadata),
        "contains_customer_data": bool(metadata.get("contains_customer_data", False)),
        "system": metadata.get("system") or metadata.get("registry") or "unspecified",
    }


def _decision_counts(evaluations: list[dict[str, Any]]) -> dict[str, int]:
    counts = {"allow": 0, "require_approval": 0, "block": 0}
    for evaluation in evaluations:
        decision = str(evaluation.get("decision"))
        counts[decision] = counts.get(decision, 0) + 1
    return counts


def _taxonomy_valid(taxonomy: dict[str, Any]) -> bool:
    actions = taxonomy.get("actions", []) if isinstance(taxonomy.get("actions"), list) else []
    action_types = {str(action.get("action_type")) for action in actions}
    return taxonomy.get("schema_version") == GENERIC_ACTION_TAXONOMY_SCHEMA and set(ACTION_TAXONOMY) <= action_types


def _scenario_valid(report: dict[str, Any]) -> bool:
    if report.get("schema_version") != "cavra.generic-agent-adapter.evaluation-report.v1":
        return False
    counts = report.get("decision_counts", {}) if isinstance(report.get("decision_counts"), dict) else {}
    return int(counts.get("allow", 0)) >= 1 and int(counts.get("require_approval", 0)) >= 1 and int(counts.get("block", 0)) >= 1


def _check_packet_schema(packet: dict[str, Any], checks: list[dict[str, str]]) -> None:
    _add_check(
        checks,
        "schema_version",
        "pass" if packet.get("schema_version") == GENERIC_ADAPTER_READINESS_SCHEMA else "blocker",
        "Generic adapter readiness packet schema is valid."
        if packet.get("schema_version") == GENERIC_ADAPTER_READINESS_SCHEMA
        else f"Packet must use {GENERIC_ADAPTER_READINESS_SCHEMA}.",
    )


def _check_evidence_mode(packet: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = packet.get("evidence_mode")
    if mode == "live":
        _add_check(checks, "evidence_mode", "pass", "Live generic adapter evidence packet supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample generic adapter packet validates contract shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "Live generic adapter validation requires evidence_mode=live.")


def _check_operating_evidence(evidence: dict[str, Any], checks: list[dict[str, str]]) -> None:
    required = ["ci_run_ref", "taxonomy_ref", "adapter_test_ref", "non_coding_scenario_ref"]
    missing = [field for field in required if not isinstance(evidence, dict) or not evidence.get(field)]
    _add_check(
        checks,
        "operating_evidence",
        "pass" if not missing else "blocker",
        "Generic adapter operating evidence references are present."
        if not missing
        else f"Operating evidence is missing: {', '.join(missing)}.",
    )


def _approver_group_for_domain(domain: str) -> str:
    return {
        "data": "Data Governance",
        "finance": "Finance Operations",
        "identity": "Identity Security",
        "model_governance": "Model Risk Governance",
        "sales": "Revenue Operations",
        "support": "Support Operations",
        "communications": "Customer Communications",
        "workflow": "Workflow Owners",
    }.get(domain, "Generic Adapter Owners")


def _optional_string(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value)
    return text if text else None


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
