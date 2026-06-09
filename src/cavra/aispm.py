from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any

from cavra.activity import utc_now


AISPM_SCHEMA_VERSION = "cavra.aispm.dashboard.v1"
LOCKED_ENTERPRISE_STATUS = "requires_cavra_enterprise"

RISK_WEIGHTS = {
    "critical": 30,
    "high": 18,
    "medium": 9,
    "low": 3,
}

DECISION_RISK_WEIGHTS = {
    "block": 16,
    "require_approval": 10,
    "warn": 5,
    "audit_only": 2,
    "allow_with_attestation": 1,
    "allow": 0,
}


def build_aispm_dashboard_contract() -> dict[str, Any]:
    """Describe the public-safe AISPM dashboard contract.

    Community exposes local/sample posture views only. Enterprise owns live
    ingestion, multi-tenant retention, private policy context, and runtime
    control actions.
    """

    return {
        "schema_version": "cavra.aispm.contract.v1",
        "product": "CAVRA",
        "community_boundary": {
            "status": "available",
            "capabilities": [
                "local activity posture summary",
                "public-safe sample dashboard",
                "decision timeline from local activity store",
                "risk finding summaries from stored decisions",
                "agent coverage summary from local sessions",
                "control coverage summary from observed local decisions",
                "near-miss queue for warnings and approval-gated actions",
                "public-safe trace replay packets from local session decisions",
                "public-safe approval lineage from local approval records",
                "public-safe behavior fingerprints and drift signals from local activity metadata",
                "policy context gap detection for decisions missing business-critical metadata",
            ],
            "data_provenance": ["local_activity_store", "sample_data"],
        },
        "enterprise_boundary": {
            "status": LOCKED_ENTERPRISE_STATUS,
            "capabilities": [
                "live multi-tenant ingestion",
                "prompt and reasoning trace capture",
                "tool-call graph",
                "full trace replay",
                "organization-wide control coverage",
                "kill switch and runtime overrides",
                "compliance exports and immutable retention",
            ],
            "private_package": "cavra_enterprise",
        },
        "objects": [
            "posture_overview",
            "agent_observability",
            "risk_findings",
            "execution_timeline",
            "control_coverage",
            "near_miss_queue",
            "trace_replay_packet",
            "approval_lineage",
            "behavior_fingerprints",
            "policy_context_gaps",
            "control_plane_readiness",
        ],
        "endpoints": {
            "posture": "/aispm/posture",
            "agents": "/aispm/agents",
            "findings": "/aispm/findings",
            "timeline": "/aispm/timeline",
            "control_coverage": "/aispm/control-coverage",
            "near_misses": "/aispm/near-misses",
            "trace_replay": "/aispm/trace-replay/{session_id}",
            "approval_lineage": "/aispm/approval-lineage",
            "behavior_fingerprints": "/aispm/behavior-fingerprints",
            "policy_context_gaps": "/aispm/policy-context-gaps",
        },
    }


def build_aispm_posture(
    activity_store: Any,
    *,
    repository: str | None = None,
    agent_id: str | None = None,
    policy_pack: str | None = None,
    limit: int = 200,
) -> dict[str, Any]:
    """Build a public-safe posture dashboard from existing activity metadata."""

    limit = max(1, min(limit, 500))
    decisions = activity_store.list_decisions(
        repository=repository,
        agent_id=agent_id,
        policy_pack=policy_pack,
        limit=limit,
    )["items"]
    sessions = activity_store.list_sessions(
        repository=repository,
        agent_id=agent_id,
        policy_pack=policy_pack,
        limit=limit,
    )["items"]
    findings = _risk_findings(decisions)
    timeline = _timeline(decisions, sessions)
    agents = _agent_observability(decisions, sessions)
    overview = _posture_overview(decisions, sessions, findings)
    behavior_fingerprints = _behavior_fingerprints(decisions, sessions)
    policy_context_gaps = _policy_context_gaps(decisions)
    return {
        "schema_version": AISPM_SCHEMA_VERSION,
        "product": "CAVRA",
        "edition": "community",
        "mode": "local_activity",
        "data_provenance": "local_activity_store",
        "tracking": "none",
        "telemetry": "disabled",
        "generated_at": utc_now(),
        "filters": {
            "repository": repository,
            "agent_id": agent_id,
            "policy_pack": policy_pack,
            "limit": limit,
        },
        "overview": overview,
        "agents": agents,
        "findings": findings,
        "timeline": timeline,
        "control_coverage": _control_coverage(decisions),
        "near_misses": _near_misses(decisions),
        "approval_lineage": [],
        "behavior_fingerprints": behavior_fingerprints,
        "policy_context_gaps": policy_context_gaps,
        "control_plane": _control_plane_readiness(decisions),
        "enterprise_unlocks": build_aispm_dashboard_contract()["enterprise_boundary"],
    }


def build_aispm_behavior_fingerprints(
    activity_store: Any,
    *,
    repository: str | None = None,
    agent_id: str | None = None,
    policy_pack: str | None = None,
    limit: int = 200,
) -> dict[str, Any]:
    """Build public-safe agent behavior fingerprints from activity metadata.

    Community fingerprints use only normalized metadata that already exists in
    the local activity store. Private raw prompts, model reasoning, raw tool
    output, customer context, and organization-specific baselines remain
    Enterprise-only ingestion fields.
    """

    limit = max(1, min(limit, 500))
    decisions = activity_store.list_decisions(
        repository=repository,
        agent_id=agent_id,
        policy_pack=policy_pack,
        limit=limit,
    )["items"]
    sessions = activity_store.list_sessions(
        repository=repository,
        agent_id=agent_id,
        policy_pack=policy_pack,
        limit=limit,
    )["items"]
    items = _behavior_fingerprints(decisions, sessions)
    status_counts = Counter(str(item.get("drift_status", "baseline")) for item in items)
    return {
        "schema_version": "cavra.aispm.behavior_fingerprints.v1",
        "product": "CAVRA",
        "edition": "community",
        "mode": "local_activity",
        "data_provenance": "local_activity_store",
        "tracking": "none",
        "telemetry": "disabled",
        "generated_at": utc_now(),
        "filters": {
            "repository": repository,
            "agent_id": agent_id,
            "policy_pack": policy_pack,
            "limit": limit,
        },
        "summary": {
            "total_agents": len(items),
            "review_required": status_counts["review_required"],
            "unusual_behavior": status_counts["unusual_behavior"],
            "baseline": status_counts["baseline"],
            "evidence_confidence": _evidence_confidence(decisions),
        },
        "items": items,
        "redaction": {
            "prompt_capture": LOCKED_ENTERPRISE_STATUS,
            "reasoning_trace": LOCKED_ENTERPRISE_STATUS,
            "raw_tool_output": LOCKED_ENTERPRISE_STATUS,
            "tool_call_graph": LOCKED_ENTERPRISE_STATUS,
            "customer_context": LOCKED_ENTERPRISE_STATUS,
            "private_behavior_baselines": LOCKED_ENTERPRISE_STATUS,
        },
        "enterprise_unlocks": {
            "status": LOCKED_ENTERPRISE_STATUS,
            "capabilities": [
                "organization-specific behavior baselines",
                "cross-repository anomaly detection",
                "live streaming behavior drift alerts",
                "identity and RBAC-aware agent owner mapping",
                "SIEM export for behavior drift events",
            ],
            "private_package": "cavra_enterprise",
        },
    }


def build_aispm_policy_context_gaps(
    activity_store: Any,
    *,
    repository: str | None = None,
    agent_id: str | None = None,
    policy_pack: str | None = None,
    limit: int = 200,
) -> dict[str, Any]:
    """Build public-safe policy context gap findings from local decisions.

    Community can flag that required context is absent from a decision record.
    Enterprise owns private enrichment from CMDB, data catalogs, identity
    providers, cloud inventory, ticketing systems, and change calendars.
    """

    limit = max(1, min(limit, 500))
    decisions = activity_store.list_decisions(
        repository=repository,
        agent_id=agent_id,
        policy_pack=policy_pack,
        limit=limit,
    )["items"]
    items = _policy_context_gaps(decisions)
    status_counts = Counter(str(item.get("gap_status", "monitor")) for item in items)
    return {
        "schema_version": "cavra.aispm.policy_context_gaps.v1",
        "product": "CAVRA",
        "edition": "community",
        "mode": "local_activity",
        "data_provenance": "local_activity_store",
        "tracking": "none",
        "telemetry": "disabled",
        "generated_at": utc_now(),
        "filters": {
            "repository": repository,
            "agent_id": agent_id,
            "policy_pack": policy_pack,
            "limit": limit,
        },
        "summary": {
            "total_gaps": sum(len(item.get("missing_context", [])) for item in items),
            "decisions_with_gaps": len(items),
            "requires_context_review": status_counts["requires_context_review"],
            "monitor": status_counts["monitor"],
            "evidence_confidence": _evidence_confidence(decisions),
        },
        "items": items,
        "redaction": {
            "private_cmdb_records": LOCKED_ENTERPRISE_STATUS,
            "data_catalog_records": LOCKED_ENTERPRISE_STATUS,
            "identity_provider_claims": LOCKED_ENTERPRISE_STATUS,
            "cloud_inventory": LOCKED_ENTERPRISE_STATUS,
            "change_calendar": LOCKED_ENTERPRISE_STATUS,
            "ticketing_metadata": LOCKED_ENTERPRISE_STATUS,
        },
        "enterprise_unlocks": {
            "status": LOCKED_ENTERPRISE_STATUS,
            "capabilities": [
                "CMDB and service catalog enrichment",
                "data-owner and data-classification lookup",
                "cloud account and environment-tier enrichment",
                "change-window and ticket correlation",
                "policy decisions that require private context before execution",
            ],
            "private_package": "cavra_enterprise",
        },
    }


def build_sample_aispm_dashboard() -> dict[str, Any]:
    """Return deterministic sample data for the public static portal."""

    decisions = [
        {
            "decision_id": "sample-dec-001",
            "session_id": "sample-session-001",
            "agent_id": "codex-agent",
            "actor": "codex-agent",
            "repository": "payments/api",
            "action_type": "execute_command",
            "target": "terraform apply",
            "policy_pack": "cloud-iam-prod",
            "rule_id": "iac.production-change",
            "decision": "require_approval",
            "severity": "high",
            "reason": "Production-impacting infrastructure action requires approval.",
            "timestamp": "2026-06-09T00:00:00+00:00",
            "evidence_refs": ["sample://evidence/iac-production-change"],
        },
        {
            "decision_id": "sample-dec-002",
            "session_id": "sample-session-001",
            "agent_id": "codex-agent",
            "actor": "codex-agent",
            "repository": "payments/api",
            "action_type": "read_file",
            "target": ".env.production",
            "policy_pack": "cavra-ai-agent-baseline",
            "rule_id": "secrets.block-sensitive-read",
            "decision": "block",
            "severity": "critical",
            "reason": "Sensitive production secret file access is blocked.",
            "timestamp": "2026-06-09T00:01:00+00:00",
            "evidence_refs": ["sample://evidence/secret-read-block"],
        },
        {
            "decision_id": "sample-dec-003",
            "session_id": "sample-session-002",
            "agent_id": "claude-code-agent",
            "actor": "claude-code-agent",
            "repository": "platform/infra",
            "action_type": "mcp_tool_call",
            "target": "filesystem.write",
            "policy_pack": "mcp-enterprise",
            "rule_id": "mcp.untrusted-tool",
            "decision": "warn",
            "severity": "medium",
            "reason": "MCP tool requires registration before broad rollout.",
            "timestamp": "2026-06-09T00:02:00+00:00",
            "evidence_refs": ["sample://evidence/mcp-warning"],
        },
    ]
    sessions = [
        {
            "session_id": "sample-session-001",
            "agent_id": "codex-agent",
            "actor": "codex-agent",
            "repository": "payments/api",
            "policy_pack": "cloud-iam-prod",
            "state": "completed",
            "started_at": "2026-06-09T00:00:00+00:00",
            "updated_at": "2026-06-09T00:01:00+00:00",
            "decision_count": 2,
            "blocked_count": 1,
            "approval_required_count": 1,
            "evidence_refs": ["sample://evidence/iac-production-change", "sample://evidence/secret-read-block"],
        },
        {
            "session_id": "sample-session-002",
            "agent_id": "claude-code-agent",
            "actor": "claude-code-agent",
            "repository": "platform/infra",
            "policy_pack": "mcp-enterprise",
            "state": "active",
            "started_at": "2026-06-09T00:02:00+00:00",
            "updated_at": "2026-06-09T00:02:00+00:00",
            "decision_count": 1,
            "blocked_count": 0,
            "approval_required_count": 0,
            "evidence_refs": ["sample://evidence/mcp-warning"],
        },
    ]
    findings = _risk_findings(decisions)
    return {
        "schema_version": AISPM_SCHEMA_VERSION,
        "product": "CAVRA",
        "edition": "community",
        "mode": "sample",
        "data_provenance": "sample_data",
        "tracking": "none",
        "telemetry": "disabled",
        "generated_at": "2026-06-09T00:03:00+00:00",
        "filters": {"repository": None, "agent_id": None, "policy_pack": None, "limit": 200},
        "overview": _posture_overview(decisions, sessions, findings),
        "agents": _agent_observability(decisions, sessions),
        "findings": findings,
        "timeline": _timeline(decisions, sessions),
        "control_coverage": _control_coverage(decisions),
        "near_misses": _near_misses(decisions),
        "approval_lineage": _sample_approval_lineage(decisions),
        "behavior_fingerprints": _behavior_fingerprints(decisions, sessions),
        "policy_context_gaps": _policy_context_gaps(decisions),
        "control_plane": _control_plane_readiness(decisions),
        "enterprise_unlocks": build_aispm_dashboard_contract()["enterprise_boundary"],
    }


def build_aispm_approval_lineage(
    approval_store: Any,
    activity_store: Any | None = None,
    *,
    state: str | None = None,
    approver_group: str | None = None,
    session_id: str | None = None,
    limit: int = 200,
) -> dict[str, Any]:
    """Build Community-safe approval lineage from local approval records.

    The lineage intentionally omits raw identity-provider claims, authorization
    tokens, private routing rules, and connector payloads. Human actors are
    reduced to role-style labels unless the stored actor is an automation
    identity.
    """

    limit = max(1, min(limit, 500))
    approvals = approval_store.list(state=state, approver_group=approver_group, limit=limit)["items"]
    if session_id:
        approvals = [item for item in approvals if item.get("session_id") == session_id]

    decisions_by_id: dict[str, dict[str, Any]] = {}
    if activity_store is not None:
        for item in activity_store.list_decisions(limit=limit)["items"]:
            decisions_by_id[str(item.get("decision_id"))] = item

    items = [_approval_lineage_item(approval, decisions_by_id.get(str(approval.get("decision_id")))) for approval in approvals]
    summary_counts = Counter(str(item.get("state", "unknown")) for item in items)
    return {
        "schema_version": "cavra.aispm.approval_lineage.v1",
        "product": "CAVRA",
        "edition": "community",
        "mode": "local_activity",
        "data_provenance": "local_approval_store",
        "tracking": "none",
        "telemetry": "disabled",
        "generated_at": utc_now(),
        "filters": {
            "state": state,
            "approver_group": approver_group,
            "session_id": session_id,
            "limit": limit,
        },
        "summary": {
            "total": len(items),
            "pending": summary_counts["pending"],
            "approved": summary_counts["approved"],
            "denied": summary_counts["denied"],
            "expired": summary_counts["expired"],
            "break_glass": summary_counts["break_glass"],
            "evidence_confidence": _approval_evidence_confidence(items),
        },
        "items": items,
        "redaction": {
            "identity_provider_claims": LOCKED_ENTERPRISE_STATUS,
            "raw_rbac_policy": LOCKED_ENTERPRISE_STATUS,
            "private_routing_rules": LOCKED_ENTERPRISE_STATUS,
            "connector_payloads": LOCKED_ENTERPRISE_STATUS,
            "human_actor_identifiers": "role labels only",
        },
        "enterprise_unlocks": {
            "status": LOCKED_ENTERPRISE_STATUS,
            "capabilities": [
                "identity-provider backed approver context",
                "RBAC-scoped lineage by role and tenant",
                "approval latency SLOs and escalations",
                "immutable multi-tenant approval audit retention",
                "SIEM and ITSM approval workflow exports",
            ],
            "private_package": "cavra_enterprise",
        },
    }


def build_aispm_trace_replay_packet(
    activity_store: Any,
    session_id: str,
    *,
    limit: int = 200,
) -> dict[str, Any] | None:
    """Build a Community-safe replay packet from local session decisions.

    Community replay reconstructs the public decision sequence only. Raw
    prompts, model reasoning, tool output, and customer-specific context remain
    private Enterprise ingestion fields and are represented as locked metadata.
    """

    limit = max(1, min(limit, 500))
    session = activity_store.get_session(session_id)
    decisions = activity_store.list_decisions(session_id=session_id, limit=limit)["items"]
    if session is None and not decisions:
        return None

    ordered_decisions = sorted(decisions, key=lambda item: str(item.get("timestamp", "")))
    steps = [_trace_step(index + 1, decision) for index, decision in enumerate(ordered_decisions)]
    evidence_refs = sorted({ref for decision in ordered_decisions for ref in decision.get("evidence_refs", [])})
    decision_counts = Counter(str(item.get("decision", "unknown")) for item in ordered_decisions)
    severity_counts = Counter(str(item.get("severity", "low")) for item in ordered_decisions)
    return {
        "schema_version": "cavra.aispm.trace_replay.v1",
        "product": "CAVRA",
        "edition": "community",
        "mode": "local_activity",
        "data_provenance": "local_activity_store",
        "tracking": "none",
        "telemetry": "disabled",
        "generated_at": utc_now(),
        "session": _trace_session_summary(session, session_id, ordered_decisions),
        "summary": {
            "step_count": len(steps),
            "blocked_actions": decision_counts["block"],
            "approval_required_actions": decision_counts["require_approval"],
            "warned_actions": decision_counts["warn"],
            "critical_or_high_steps": severity_counts["critical"] + severity_counts["high"],
            "evidence_confidence": _evidence_confidence(ordered_decisions),
        },
        "steps": steps,
        "evidence_refs": evidence_refs,
        "redaction": {
            "target_redaction": "sensitive targets are summarized",
            "prompt_capture": LOCKED_ENTERPRISE_STATUS,
            "reasoning_trace": LOCKED_ENTERPRISE_STATUS,
            "raw_tool_output": LOCKED_ENTERPRISE_STATUS,
            "full_trace_replay": LOCKED_ENTERPRISE_STATUS,
            "customer_context": LOCKED_ENTERPRISE_STATUS,
        },
        "enterprise_unlocks": {
            "status": LOCKED_ENTERPRISE_STATUS,
            "capabilities": [
                "raw prompt and response replay",
                "model reasoning trace capture",
                "tool-call graph with raw tool results",
                "approval lineage with identity-provider context",
                "immutable multi-tenant replay retention",
            ],
            "private_package": "cavra_enterprise",
        },
    }


def _posture_overview(
    decisions: list[dict[str, Any]],
    sessions: list[dict[str, Any]],
    findings: list[dict[str, Any]],
) -> dict[str, Any]:
    decision_counts = Counter(str(item.get("decision", "unknown")) for item in decisions)
    severity_counts = Counter(str(item.get("severity", "low")) for item in decisions)
    risk_penalty = sum(DECISION_RISK_WEIGHTS.get(str(item.get("decision", "")), 0) for item in decisions)
    risk_penalty += sum(RISK_WEIGHTS.get(str(item.get("severity", "low")), 0) for item in findings)
    posture_score = max(0, min(100, 100 - risk_penalty))
    return {
        "posture_score": posture_score,
        "risk_level": _risk_level(posture_score),
        "total_sessions": len(sessions),
        "total_decisions": len(decisions),
        "blocked_actions": decision_counts["block"],
        "approval_required_actions": decision_counts["require_approval"],
        "warned_actions": decision_counts["warn"],
        "risk_findings": len(findings),
        "critical_findings": severity_counts["critical"],
        "high_findings": severity_counts["high"],
        "latest_activity_at": max(
            [str(item.get("timestamp", "")) for item in decisions if item.get("timestamp")]
            + [str(item.get("updated_at", "")) for item in sessions if item.get("updated_at")],
            default=None,
        ),
        "evidence_confidence": _evidence_confidence(decisions),
    }


def _sample_approval_lineage(decisions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    approval_decision = next((item for item in decisions if item.get("decision") == "require_approval"), None)
    if not approval_decision:
        return []
    return [
        {
            "lineage_id": "lineage-sample-apr-001",
            "approval_id": "sample-apr-001",
            "decision_id": approval_decision.get("decision_id"),
            "session_id": approval_decision.get("session_id"),
            "state": "approved",
            "approver_group": "Cloud Security",
            "requested_by": "automation:codex-agent",
            "decided_by": "role:approver",
            "requested_at": "2026-06-09T00:00:10+00:00",
            "decided_at": "2026-06-09T00:00:40+00:00",
            "external_ref": "ticket://sample-change-42",
            "break_glass": False,
            "decision": {
                "action_type": approval_decision.get("action_type"),
                "target_summary": _safe_target_summary(approval_decision)[0],
                "risk_classification": _risk_classification(approval_decision),
                "severity": approval_decision.get("severity"),
                "repository": approval_decision.get("repository"),
                "policy_pack": approval_decision.get("policy_pack"),
                "rule_id": approval_decision.get("rule_id"),
            },
            "evidence_refs": ["approval://sample-apr-001", *approval_decision.get("evidence_refs", [])],
            "redacted_fields": ["identity_provider_claims", "raw_rbac_context"],
        }
    ]


def _approval_lineage_item(approval: dict[str, Any], stored_decision: dict[str, Any] | None) -> dict[str, Any]:
    decision = stored_decision or approval.get("decision") or {}
    target_summary, _target_redacted = _safe_target_summary(decision)
    return {
        "lineage_id": f"lineage-{approval.get('approval_id', 'unknown')}",
        "approval_id": approval.get("approval_id"),
        "decision_id": approval.get("decision_id") or decision.get("decision_id"),
        "session_id": approval.get("session_id") or decision.get("session_id"),
        "state": approval.get("state", "unknown"),
        "approver_group": approval.get("approver_group", "unassigned"),
        "requested_by": _safe_actor_label(approval.get("requested_by")),
        "decided_by": _safe_actor_label(approval.get("decided_by")),
        "requested_at": approval.get("requested_at"),
        "decided_at": approval.get("decided_at"),
        "expires_at": approval.get("expires_at"),
        "external_ref": approval.get("external_ref"),
        "break_glass": bool(approval.get("break_glass", False)),
        "decision": {
            "action_type": decision.get("action_type", "unknown"),
            "target_summary": target_summary,
            "risk_classification": _risk_classification(decision),
            "control_surface": _control_surface(decision),
            "severity": decision.get("severity", "low"),
            "repository": decision.get("repository", "local"),
            "policy_pack": decision.get("policy_pack", "cavra-ai-agent-baseline"),
            "rule_id": decision.get("rule_id", "runtime.default"),
        },
        "evidence_refs": list(approval.get("evidence_refs", [])),
        "redacted_fields": ["identity_provider_claims", "raw_rbac_context", "connector_payloads"],
    }


def _approval_evidence_confidence(items: list[dict[str, Any]]) -> str:
    if not items:
        return "no_approval_records"
    if all(item.get("evidence_refs") for item in items):
        return "approval_evidence_refs"
    return "approval_metadata_only"


def _safe_actor_label(actor: Any) -> str | None:
    if actor in {None, ""}:
        return None
    value = str(actor)
    lowered = value.lower()
    automation_markers = ("agent", "bot", "automation", "cavra", "codex", "claude")
    if any(marker in lowered for marker in automation_markers):
        return f"automation:{value}"
    return "role:approver"


def _agent_observability(decisions: list[dict[str, Any]], sessions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped_decisions: dict[str, list[dict[str, Any]]] = defaultdict(list)
    grouped_sessions: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for decision in decisions:
        grouped_decisions[str(decision.get("agent_id", "unknown-agent"))].append(decision)
    for session in sessions:
        grouped_sessions[str(session.get("agent_id", "unknown-agent"))].append(session)

    agent_ids = sorted(set(grouped_decisions) | set(grouped_sessions))
    agents: list[dict[str, Any]] = []
    for agent_id in agent_ids:
        agent_decisions = grouped_decisions.get(agent_id, [])
        agent_sessions = grouped_sessions.get(agent_id, [])
        decision_counts = Counter(str(item.get("decision", "unknown")) for item in agent_decisions)
        agents.append(
            {
                "agent_id": agent_id,
                "repository_count": len({str(item.get("repository", "local")) for item in agent_decisions + agent_sessions}),
                "session_count": len(agent_sessions),
                "decision_count": len(agent_decisions),
                "blocked_actions": decision_counts["block"],
                "approval_required_actions": decision_counts["require_approval"],
                "warned_actions": decision_counts["warn"],
                "last_seen_at": max(
                    [str(item.get("timestamp", "")) for item in agent_decisions if item.get("timestamp")]
                    + [str(item.get("updated_at", "")) for item in agent_sessions if item.get("updated_at")],
                    default=None,
                ),
                "coverage_status": "observed" if agent_decisions or agent_sessions else "unknown",
                "drift_status": "review_required"
                if decision_counts["block"] or decision_counts["require_approval"]
                else "baseline",
            }
        )
    return agents


def _behavior_fingerprints(decisions: list[dict[str, Any]], sessions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped_decisions: dict[str, list[dict[str, Any]]] = defaultdict(list)
    grouped_sessions: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for decision in decisions:
        grouped_decisions[str(decision.get("agent_id", "unknown-agent"))].append(decision)
    for session in sessions:
        grouped_sessions[str(session.get("agent_id", "unknown-agent"))].append(session)

    fingerprints: list[dict[str, Any]] = []
    for agent_id in sorted(set(grouped_decisions) | set(grouped_sessions)):
        agent_decisions = grouped_decisions.get(agent_id, [])
        agent_sessions = grouped_sessions.get(agent_id, [])
        decision_counts = Counter(str(item.get("decision", "unknown")) for item in agent_decisions)
        severity_counts = Counter(str(item.get("severity", "low")) for item in agent_decisions)
        action_counts = Counter(str(item.get("action_type", "unknown")) for item in agent_decisions)
        repositories = sorted(
            {str(item.get("repository", "local")) for item in [*agent_decisions, *agent_sessions] if item.get("repository")}
        )
        policy_packs = sorted({str(item.get("policy_pack", "cavra-ai-agent-baseline")) for item in agent_decisions})
        control_surfaces = sorted({_control_surface(item) for item in agent_decisions})
        risk_signals = _behavior_risk_signals(
            agent_decisions,
            repositories=repositories,
            policy_packs=policy_packs,
            control_surfaces=control_surfaces,
            action_counts=action_counts,
            decision_counts=decision_counts,
            severity_counts=severity_counts,
        )
        drift_score = _behavior_drift_score(
            decision_counts=decision_counts,
            severity_counts=severity_counts,
            repositories=repositories,
            policy_packs=policy_packs,
            control_surfaces=control_surfaces,
            action_counts=action_counts,
        )
        fingerprints.append(
            {
                "fingerprint_id": f"fingerprint-{agent_id}",
                "agent_id": agent_id,
                "repositories": repositories,
                "session_count": len(agent_sessions),
                "decision_count": len(agent_decisions),
                "action_profile": _counter_profile(action_counts),
                "decision_profile": _counter_profile(decision_counts),
                "policy_packs": policy_packs,
                "control_surfaces": control_surfaces,
                "risk_signals": risk_signals,
                "drift_status": _behavior_drift_status(drift_score, risk_signals),
                "drift_score": drift_score,
                "evidence_refs": sorted({ref for item in agent_decisions for ref in item.get("evidence_refs", [])})[:8],
                "last_seen_at": max(
                    [str(item.get("timestamp", "")) for item in agent_decisions if item.get("timestamp")]
                    + [str(item.get("updated_at", "")) for item in agent_sessions if item.get("updated_at")],
                    default=None,
                ),
            }
        )
    return sorted(fingerprints, key=lambda item: (-int(item.get("drift_score", 0)), str(item.get("agent_id", ""))))


def _counter_profile(counter: Counter[str]) -> list[dict[str, Any]]:
    return [{"name": name, "count": count} for name, count in counter.most_common()]


def _behavior_drift_score(
    *,
    decision_counts: Counter[str],
    severity_counts: Counter[str],
    repositories: list[str],
    policy_packs: list[str],
    control_surfaces: list[str],
    action_counts: Counter[str],
) -> int:
    score = (
        decision_counts["block"] * 20
        + decision_counts["require_approval"] * 14
        + decision_counts["warn"] * 8
        + decision_counts["allow_with_attestation"] * 4
        + severity_counts["critical"] * 18
        + severity_counts["high"] * 10
        + severity_counts["medium"] * 4
    )
    if len(repositories) > 1:
        score += min(12, (len(repositories) - 1) * 4)
    if len(policy_packs) > 1:
        score += min(10, (len(policy_packs) - 1) * 5)
    if len(control_surfaces) > 1:
        score += min(12, (len(control_surfaces) - 1) * 4)
    if len(action_counts) > 2:
        score += min(10, (len(action_counts) - 2) * 3)
    return max(0, min(score, 100))


def _behavior_drift_status(drift_score: int, risk_signals: list[str]) -> str:
    if "blocked_action" in risk_signals or "approval_gate" in risk_signals or drift_score >= 35:
        return "review_required"
    if risk_signals or drift_score >= 12:
        return "unusual_behavior"
    return "baseline"


def _behavior_risk_signals(
    decisions: list[dict[str, Any]],
    *,
    repositories: list[str],
    policy_packs: list[str],
    control_surfaces: list[str],
    action_counts: Counter[str],
    decision_counts: Counter[str],
    severity_counts: Counter[str],
) -> list[str]:
    signals: list[str] = []
    if decision_counts["block"]:
        signals.append("blocked_action")
    if decision_counts["require_approval"]:
        signals.append("approval_gate")
    if decision_counts["warn"]:
        signals.append("warned_action")
    if severity_counts["critical"] or severity_counts["high"]:
        signals.append("critical_or_high_decision")
    if "sensitive_data" in control_surfaces:
        signals.append("sensitive_data_access")
    if "infrastructure_iac" in control_surfaces:
        signals.append("infrastructure_change")
    if "mcp_tools" in control_surfaces:
        signals.append("mcp_or_tool_activity")
    if len(repositories) > 1:
        signals.append("multi_repository_activity")
    if len(policy_packs) > 1:
        signals.append("multiple_policy_packs")
    if len(action_counts) > 2:
        signals.append("broad_action_profile")
    if decisions and not any(item.get("evidence_refs") for item in decisions):
        signals.append("metadata_only_evidence")
    return signals


def _policy_context_gaps(decisions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    gaps: list[dict[str, Any]] = []
    for decision in decisions:
        required_context = _required_policy_context(decision)
        present_context: list[str] = []
        missing_context: list[str] = []
        for field in required_context:
            if _context_value(decision, field) in {None, ""}:
                missing_context.append(field)
            else:
                present_context.append(field)
        if not missing_context:
            continue
        surface = _control_surface(decision)
        gaps.append(
            {
                "gap_id": f"context-gap-{decision.get('decision_id', 'unknown')}",
                "decision_id": decision.get("decision_id"),
                "session_id": decision.get("session_id"),
                "agent_id": decision.get("agent_id", "unknown-agent"),
                "repository": decision.get("repository", "local"),
                "policy_pack": decision.get("policy_pack", "cavra-ai-agent-baseline"),
                "rule_id": decision.get("rule_id", "runtime.default"),
                "action_type": decision.get("action_type", "unknown"),
                "decision": decision.get("decision", "unknown"),
                "severity": decision.get("severity", "low"),
                "risk_classification": _risk_classification(decision),
                "control_surface": surface,
                "missing_context": missing_context,
                "present_context": present_context,
                "gap_status": _policy_context_gap_status(decision, missing_context),
                "recommended_action": _policy_context_recommended_action(surface, missing_context),
                "evidence_refs": list(decision.get("evidence_refs", [])),
                "timestamp": decision.get("timestamp"),
            }
        )
    return sorted(
        gaps,
        key=lambda item: (
            0 if item.get("gap_status") == "requires_context_review" else 1,
            str(item.get("timestamp", "")),
        ),
        reverse=False,
    )


def _required_policy_context(decision: dict[str, Any]) -> list[str]:
    surface = _control_surface(decision)
    severity = str(decision.get("severity", "low"))
    outcome = str(decision.get("decision", "unknown"))
    required = ["environment_tier", "system_criticality"]
    if surface == "sensitive_data":
        required.extend(["data_owner", "data_classification", "customer_region"])
    elif surface == "infrastructure_iac":
        required.extend(["service_owner", "change_window", "blast_radius"])
    elif surface == "mcp_tools":
        required.extend(["tool_owner", "tool_trust_tier", "business_justification"])
    elif surface == "source_control":
        required.extend(["repository_owner", "branch_protection_tier", "change_ticket"])
    elif surface == "runtime_commands":
        required.extend(["service_owner", "execution_environment", "change_ticket"])
    else:
        required.extend(["service_owner", "business_justification"])
    if severity in {"critical", "high"} or outcome in {"block", "require_approval"}:
        required.append("approval_route")
    return list(dict.fromkeys(required))


def _context_value(decision: dict[str, Any], field: str) -> Any:
    aliases = {
        "environment_tier": ("environment_tier", "environment", "deployment_environment", "env"),
        "system_criticality": ("system_criticality", "criticality", "risk_tier"),
        "data_owner": ("data_owner", "owner", "service_owner"),
        "data_classification": ("data_classification", "classification", "data_class"),
        "customer_region": ("customer_region", "region", "data_region"),
        "service_owner": ("service_owner", "owner", "team"),
        "change_window": ("change_window", "maintenance_window", "release_window"),
        "blast_radius": ("blast_radius", "impact_scope", "scope"),
        "tool_owner": ("tool_owner", "owner", "mcp_owner"),
        "tool_trust_tier": ("tool_trust_tier", "trust_tier", "mcp_trust_tier"),
        "business_justification": ("business_justification", "justification", "reason"),
        "repository_owner": ("repository_owner", "owner", "repo_owner"),
        "branch_protection_tier": ("branch_protection_tier", "branch_tier", "protection_tier"),
        "change_ticket": ("change_ticket", "ticket", "external_ref"),
        "execution_environment": ("execution_environment", "runtime_environment", "environment"),
        "approval_route": ("approval_route", "approver_group", "approval_group"),
    }
    keys = aliases.get(field, (field,))
    containers = [
        decision,
        decision.get("context") if isinstance(decision.get("context"), dict) else {},
        decision.get("metadata") if isinstance(decision.get("metadata"), dict) else {},
        decision.get("labels") if isinstance(decision.get("labels"), dict) else {},
    ]
    for container in containers:
        if not isinstance(container, dict):
            continue
        for key in keys:
            value = container.get(key)
            if value not in {None, ""}:
                return value
    return None


def _policy_context_gap_status(decision: dict[str, Any], missing_context: list[str]) -> str:
    severity = str(decision.get("severity", "low"))
    outcome = str(decision.get("decision", "unknown"))
    if severity in {"critical", "high"} or outcome in {"block", "require_approval"}:
        return "requires_context_review"
    if len(missing_context) >= 3:
        return "requires_context_review"
    return "monitor"


def _policy_context_recommended_action(surface: str, missing_context: list[str]) -> str:
    missing = ", ".join(missing_context)
    if surface == "sensitive_data":
        return f"Attach data-owner, classification, and regional context before relying on the decision. Missing: {missing}."
    if surface == "infrastructure_iac":
        return f"Attach service owner, change window, and blast-radius context before execution. Missing: {missing}."
    if surface == "mcp_tools":
        return f"Attach tool owner, trust tier, and business justification before broad tool use. Missing: {missing}."
    if surface == "source_control":
        return f"Attach repository owner, branch protection tier, and change ticket before source-control mutation. Missing: {missing}."
    return f"Attach missing business context before treating the decision as fully governed. Missing: {missing}."


def _risk_findings(decisions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for decision in decisions:
        outcome = str(decision.get("decision", ""))
        severity = str(decision.get("severity", "low"))
        if outcome not in {"block", "require_approval", "warn"} and severity not in {"critical", "high"}:
            continue
        findings.append(
            {
                "finding_id": f"finding-{decision.get('decision_id', 'unknown')}",
                "decision_id": decision.get("decision_id"),
                "session_id": decision.get("session_id"),
                "agent_id": decision.get("agent_id", "unknown-agent"),
                "repository": decision.get("repository", "local"),
                "severity": severity,
                "risk_classification": _risk_classification(decision),
                "decision": outcome,
                "rule_id": decision.get("rule_id"),
                "reason": decision.get("reason") or "CAVRA policy decision requires operator review.",
                "evidence_refs": list(decision.get("evidence_refs", [])),
                "timestamp": decision.get("timestamp"),
            }
        )
    return sorted(findings, key=lambda item: str(item.get("timestamp", "")), reverse=True)


def _timeline(decisions: list[dict[str, Any]], sessions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for session in sessions:
        events.append(
            {
                "event_id": f"session-{session.get('session_id')}",
                "event_type": "session",
                "session_id": session.get("session_id"),
                "agent_id": session.get("agent_id"),
                "repository": session.get("repository"),
                "title": f"Session {session.get('state', 'active')}",
                "outcome": session.get("state"),
                "timestamp": session.get("updated_at") or session.get("started_at"),
                "evidence_refs": list(session.get("evidence_refs", [])),
            }
        )
    for decision in decisions:
        events.append(
            {
                "event_id": f"decision-{decision.get('decision_id')}",
                "event_type": "policy_decision",
                "decision_id": decision.get("decision_id"),
                "session_id": decision.get("session_id"),
                "agent_id": decision.get("agent_id"),
                "repository": decision.get("repository"),
                "title": f"{decision.get('decision')} {decision.get('action_type')}",
                "outcome": decision.get("decision"),
                "severity": decision.get("severity"),
                "target": decision.get("target"),
                "timestamp": decision.get("timestamp"),
                "evidence_refs": list(decision.get("evidence_refs", [])),
            }
        )
    return sorted(events, key=lambda item: str(item.get("timestamp", "")), reverse=True)


def _control_coverage(decisions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    surfaces = {
        "sensitive_data": {
            "label": "Secrets and sensitive data",
            "description": "Reads or writes that could expose credentials, tokens, customer data, or protected files.",
        },
        "infrastructure_iac": {
            "label": "Infrastructure and IaC",
            "description": "Cloud, Terraform/OpenTofu, Kubernetes, and production infrastructure actions.",
        },
        "mcp_tools": {
            "label": "MCP and tool calls",
            "description": "External tool, MCP server, filesystem, browser, and automation actions.",
        },
        "source_control": {
            "label": "Source control",
            "description": "Git, branch, commit, PR, and repository mutation actions.",
        },
        "runtime_commands": {
            "label": "Runtime commands",
            "description": "Shell commands, scripts, package operations, and local execution.",
        },
        "general_policy": {
            "label": "General policy",
            "description": "Policy decisions that do not map to a more specific control surface.",
        },
    }
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for decision in decisions:
        grouped[_control_surface(decision)].append(decision)

    coverage: list[dict[str, Any]] = []
    for surface_id, surface in surfaces.items():
        surface_decisions = grouped.get(surface_id, [])
        decision_counts = Counter(str(item.get("decision", "unknown")) for item in surface_decisions)
        evidence_refs = [ref for item in surface_decisions for ref in item.get("evidence_refs", [])]
        coverage.append(
            {
                "surface_id": surface_id,
                "label": surface["label"],
                "description": surface["description"],
                "coverage_status": _coverage_status(decision_counts, bool(surface_decisions)),
                "decision_count": len(surface_decisions),
                "blocked_actions": decision_counts["block"],
                "approval_required_actions": decision_counts["require_approval"],
                "warned_actions": decision_counts["warn"],
                "evidence_confidence": _evidence_confidence(surface_decisions),
                "evidence_refs": evidence_refs[:8],
            }
        )
    return coverage


def _near_misses(decisions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    near_miss_decisions = []
    for decision in decisions:
        outcome = str(decision.get("decision", ""))
        severity = str(decision.get("severity", "low"))
        if outcome not in {"warn", "require_approval", "allow_with_attestation"} and severity not in {"critical", "high"}:
            continue
        if outcome == "block":
            continue
        near_miss_decisions.append(
            {
                "near_miss_id": f"near-miss-{decision.get('decision_id', 'unknown')}",
                "decision_id": decision.get("decision_id"),
                "session_id": decision.get("session_id"),
                "agent_id": decision.get("agent_id", "unknown-agent"),
                "repository": decision.get("repository", "local"),
                "surface_id": _control_surface(decision),
                "severity": severity,
                "decision": outcome,
                "risk_classification": _risk_classification(decision),
                "reason": decision.get("reason") or "CAVRA allowed the action with warning, approval, or attestation.",
                "operator_signal": _near_miss_signal(outcome),
                "evidence_refs": list(decision.get("evidence_refs", [])),
                "timestamp": decision.get("timestamp"),
            }
        )
    return sorted(near_miss_decisions, key=lambda item: str(item.get("timestamp", "")), reverse=True)


def _trace_session_summary(
    session: dict[str, Any] | None,
    session_id: str,
    decisions: list[dict[str, Any]],
) -> dict[str, Any]:
    first_decision = decisions[0] if decisions else {}
    last_decision = decisions[-1] if decisions else {}
    return {
        "session_id": session_id,
        "agent_id": (session or {}).get("agent_id") or first_decision.get("agent_id", "unknown-agent"),
        "actor": (session or {}).get("actor") or first_decision.get("actor", "ai-agent"),
        "repository": (session or {}).get("repository") or first_decision.get("repository", "local"),
        "policy_pack": (session or {}).get("policy_pack") or first_decision.get("policy_pack", "cavra-ai-agent-baseline"),
        "state": (session or {}).get("state", "decision_only"),
        "started_at": (session or {}).get("started_at") or first_decision.get("timestamp"),
        "updated_at": (session or {}).get("updated_at") or last_decision.get("timestamp"),
    }


def _trace_step(index: int, decision: dict[str, Any]) -> dict[str, Any]:
    target_summary, target_redacted = _safe_target_summary(decision)
    return {
        "step": index,
        "event_type": "policy_decision",
        "decision_id": decision.get("decision_id"),
        "session_id": decision.get("session_id"),
        "agent_id": decision.get("agent_id", "unknown-agent"),
        "repository": decision.get("repository", "local"),
        "action_type": decision.get("action_type", "unknown"),
        "target_summary": target_summary,
        "target_redacted": target_redacted,
        "decision": decision.get("decision"),
        "severity": decision.get("severity"),
        "rule_id": decision.get("rule_id"),
        "policy_pack": decision.get("policy_pack"),
        "risk_classification": _risk_classification(decision),
        "control_surface": _control_surface(decision),
        "reason": decision.get("reason") or "CAVRA policy decision recorded.",
        "evidence_refs": list(decision.get("evidence_refs", [])),
        "timestamp": decision.get("timestamp"),
    }


def _safe_target_summary(decision: dict[str, Any]) -> tuple[str, bool]:
    target = str(decision.get("target") or decision.get("requested_operation") or "")
    target_lower = target.lower()
    rule_id = str(decision.get("rule_id", "")).lower()
    if "secret" in target_lower or ".env" in target_lower or "token" in target_lower or "credential" in rule_id:
        return "sensitive target redacted", True
    if len(target) > 120:
        return f"{target[:117]}...", True
    return target or "target not recorded", False


def _control_plane_readiness(decisions: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "community_status": "local_activity_ready",
        "enterprise_status": LOCKED_ENTERPRISE_STATUS,
        "live_streaming": LOCKED_ENTERPRISE_STATUS,
        "kill_switch": LOCKED_ENTERPRISE_STATUS,
        "runtime_overrides": LOCKED_ENTERPRISE_STATUS,
        "policy_distribution": LOCKED_ENTERPRISE_STATUS,
        "trace_replay": "local_timeline_available" if decisions else "sample_or_enterprise_required",
        "data_provenance_required": True,
    }


def _risk_classification(decision: dict[str, Any]) -> str:
    action_type = str(decision.get("action_type", "")).lower()
    target = str(decision.get("target", "")).lower()
    rule_id = str(decision.get("rule_id", "")).lower()
    if "secret" in target or ".env" in target or "secret" in rule_id:
        return "credential_or_sensitive_data_exposure"
    if "terraform" in target or "tofu" in target or "iac" in rule_id:
        return "infrastructure_change_risk"
    if "mcp" in action_type or "mcp" in rule_id:
        return "tool_or_mcp_governance_risk"
    if "git" in action_type:
        return "source_control_risk"
    if "command" in action_type:
        return "runtime_command_risk"
    return "policy_violation"


def _control_surface(decision: dict[str, Any]) -> str:
    action_type = str(decision.get("action_type", "")).lower()
    target = str(decision.get("target", "")).lower()
    rule_id = str(decision.get("rule_id", "")).lower()
    if "secret" in target or ".env" in target or "credential" in rule_id or "secret" in rule_id:
        return "sensitive_data"
    if "terraform" in target or "tofu" in target or "kubernetes" in target or "iac" in rule_id:
        return "infrastructure_iac"
    if "mcp" in action_type or "mcp" in rule_id or "tool" in action_type:
        return "mcp_tools"
    if "git" in action_type or "pull_request" in action_type or "branch" in target:
        return "source_control"
    if "command" in action_type or "shell" in action_type or "script" in action_type:
        return "runtime_commands"
    return "general_policy"


def _coverage_status(decision_counts: Counter[str], observed: bool) -> str:
    if not observed:
        return "not_observed_locally"
    if decision_counts["block"]:
        return "enforced"
    if decision_counts["require_approval"]:
        return "approval_gated"
    if decision_counts["warn"]:
        return "warning_only"
    if decision_counts["allow_with_attestation"]:
        return "attested"
    return "observed"


def _near_miss_signal(outcome: str) -> str:
    if outcome == "require_approval":
        return "approval_prevented_unreviewed_execution"
    if outcome == "warn":
        return "warning_allowed_with_operator_visibility"
    if outcome == "allow_with_attestation":
        return "allowed_with_evidence_attestation"
    return "review_recommended"


def _risk_level(score: int) -> str:
    if score >= 85:
        return "low"
    if score >= 65:
        return "medium"
    if score >= 40:
        return "high"
    return "critical"


def _evidence_confidence(decisions: list[dict[str, Any]]) -> str:
    if not decisions:
        return "sample_or_empty"
    refs = [str(ref) for decision in decisions for ref in decision.get("evidence_refs", [])]
    if any(ref.startswith("signed://") or "signature" in ref for ref in refs):
        return "signed_evidence"
    if refs:
        return "activity_evidence_refs"
    return "activity_metadata_only"
