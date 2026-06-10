from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timezone
from typing import Any

from cavra.activity import utc_now
from cavra.policy_authoring import build_policy_pack_draft


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
                "pre-action risk forecasts from local decision metadata before agent execution",
                "intent-to-action drift detection from declared intent and local decision metadata",
                "public-safe tool-chain graph from agent, tool, target, and decision metadata",
                "agent blast-radius map from repositories, surfaces, tools, policy packs, and approval metadata",
                "control coverage heatmap by agent, repository, and control surface from local activity metadata",
                "evidence confidence drilldown for decision and session evidence references",
                "evidence freshness and retention SLO summary from local activity timestamps",
                "deterministic executive risk narrative from local posture metrics",
                "read-only replay-to-policy draft suggestions from normalized trace decisions",
                "read-only replay-to-policy test fixture exports for reviewed policy drafts",
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
                "private asset-graph and identity-aware pre-action forecasting",
                "prompt-derived semantic intent extraction and private workflow correlation",
                "raw tool payload graphing and cross-system execution traces",
                "private asset, identity, cloud dependency, and permission blast-radius enrichment",
                "organization-wide control coverage heatmap with private asset, owner, and environment enrichment",
                "immutable evidence store validation, signature verification, and external evidence correlation",
                "evidence retention proof, object-lock status, KMS status, and archive lifecycle validation",
                "AI-assisted executive narratives with private tenant context and trend history",
                "AI-assisted policy authoring with private prompt, ticket, asset, and approval context",
                "CI write-back and tenant-history simulation for generated policy tests",
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
            "pre_action_risk_forecasts",
            "intent_action_drift",
            "tool_chain_graph",
            "agent_blast_radius",
            "control_coverage_heatmap",
            "evidence_confidence_drilldown",
            "evidence_freshness_slo",
            "executive_risk_narrative",
            "replay_to_policy_draft",
            "replay_to_policy_tests",
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
            "pre_action_risk_forecasts": "/aispm/pre-action-risk-forecasts",
            "intent_action_drift": "/aispm/intent-action-drift",
            "tool_chain_graph": "/aispm/tool-chain-graph",
            "agent_blast_radius": "/aispm/agent-blast-radius",
            "control_coverage_heatmap": "/aispm/control-coverage-heatmap",
            "evidence_confidence": "/aispm/evidence-confidence",
            "evidence_freshness": "/aispm/evidence-freshness",
            "executive_risk_narrative": "/aispm/executive-risk-narrative",
            "replay_to_policy_draft": "/aispm/replay-to-policy-draft",
            "replay_to_policy_tests": "/aispm/replay-to-policy-tests",
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
    pre_action_risk_forecasts = _pre_action_risk_forecasts(decisions)
    intent_action_drift = _intent_action_drift(decisions)
    tool_chain_graph = _tool_chain_graph(decisions)
    agent_blast_radius = _agent_blast_radius(decisions, sessions)
    control_coverage_heatmap = _control_coverage_heatmap(decisions, sessions)
    evidence_confidence_drilldown = _evidence_confidence_drilldown(decisions, sessions)
    generated_at = utc_now()
    evidence_freshness_slo = _evidence_freshness_slo(decisions, sessions, generated_at=generated_at)
    executive_risk_narrative = _executive_risk_narrative(
        decisions,
        sessions,
        findings,
        overview,
        evidence_freshness_slo,
    )
    replay_to_policy_draft = _replay_to_policy_draft(
        decisions,
        sessions=sessions,
        source_scope="local_activity_window",
    )
    return {
        "schema_version": AISPM_SCHEMA_VERSION,
        "product": "CAVRA",
        "edition": "community",
        "mode": "local_activity",
        "data_provenance": "local_activity_store",
        "tracking": "none",
        "telemetry": "disabled",
        "generated_at": generated_at,
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
        "pre_action_risk_forecasts": pre_action_risk_forecasts,
        "intent_action_drift": intent_action_drift,
        "tool_chain_graph": tool_chain_graph,
        "agent_blast_radius": agent_blast_radius,
        "control_coverage_heatmap": control_coverage_heatmap,
        "evidence_confidence_drilldown": evidence_confidence_drilldown,
        "evidence_freshness_slo": evidence_freshness_slo,
        "executive_risk_narrative": executive_risk_narrative,
        "replay_to_policy_draft": replay_to_policy_draft,
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


def build_aispm_pre_action_risk_forecasts(
    activity_store: Any,
    *,
    repository: str | None = None,
    agent_id: str | None = None,
    policy_pack: str | None = None,
    limit: int = 200,
) -> dict[str, Any]:
    """Build public-safe pre-action risk forecasts from local decisions.

    Community forecasts project impact from normalized decision metadata only.
    Enterprise owns private asset graphs, dependency graphs, identity context,
    cloud inventory, runtime state, and SaaS simulation before execution.
    """

    limit = max(1, min(limit, 500))
    decisions = activity_store.list_decisions(
        repository=repository,
        agent_id=agent_id,
        policy_pack=policy_pack,
        limit=limit,
    )["items"]
    items = _pre_action_risk_forecasts(decisions)
    status_counts = Counter(str(item.get("forecast_status", "monitor")) for item in items)
    severity_counts = Counter(str(item.get("severity", "low")) for item in items)
    return {
        "schema_version": "cavra.aispm.pre_action_risk_forecasts.v1",
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
            "total_forecasts": len(items),
            "critical_or_high_forecasts": severity_counts["critical"] + severity_counts["high"],
            "approval_recommended": status_counts["approval_recommended"],
            "block_recommended": status_counts["block_recommended"],
            "warn_recommended": status_counts["warn_recommended"],
            "evidence_confidence": _evidence_confidence(decisions),
        },
        "items": items,
        "redaction": {
            "private_asset_graph": LOCKED_ENTERPRISE_STATUS,
            "dependency_graph": LOCKED_ENTERPRISE_STATUS,
            "cloud_resource_inventory": LOCKED_ENTERPRISE_STATUS,
            "identity_blast_radius": LOCKED_ENTERPRISE_STATUS,
            "runtime_state": LOCKED_ENTERPRISE_STATUS,
            "prompt_intent_context": LOCKED_ENTERPRISE_STATUS,
        },
        "enterprise_unlocks": {
            "status": LOCKED_ENTERPRISE_STATUS,
            "capabilities": [
                "asset graph blast-radius forecasting",
                "identity and permission blast-radius analysis",
                "live dependency graph forecasting",
                "cost, performance, and SLO impact forecasts",
                "pre-action simulation against the private SaaS control plane",
            ],
            "private_package": "cavra_enterprise",
        },
    }


def build_aispm_intent_action_drift(
    activity_store: Any,
    *,
    repository: str | None = None,
    agent_id: str | None = None,
    policy_pack: str | None = None,
    limit: int = 200,
) -> dict[str, Any]:
    """Build public-safe intent-to-action drift signals from local decisions.

    Community compares declared intent metadata to the normalized action,
    target, control surface, and policy outcome. Enterprise owns prompt-derived
    intent extraction, semantic comparison against private tickets, and live
    workflow correlation.
    """

    limit = max(1, min(limit, 500))
    decisions = activity_store.list_decisions(
        repository=repository,
        agent_id=agent_id,
        policy_pack=policy_pack,
        limit=limit,
    )["items"]
    items = _intent_action_drift(decisions)
    status_counts = Counter(str(item.get("drift_status", "aligned")) for item in items)
    return {
        "schema_version": "cavra.aispm.intent_action_drift.v1",
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
            "total_items": len(items),
            "high_drift": status_counts["high_drift"],
            "needs_review": status_counts["needs_review"],
            "unknown_intent": status_counts["unknown_intent"],
            "aligned": status_counts["aligned"],
            "evidence_confidence": _evidence_confidence(decisions),
        },
        "items": items,
        "redaction": {
            "raw_prompt": LOCKED_ENTERPRISE_STATUS,
            "reasoning_trace": LOCKED_ENTERPRISE_STATUS,
            "conversation_history": LOCKED_ENTERPRISE_STATUS,
            "private_ticket_context": LOCKED_ENTERPRISE_STATUS,
            "full_tool_payload": LOCKED_ENTERPRISE_STATUS,
            "semantic_intent_model": LOCKED_ENTERPRISE_STATUS,
        },
        "enterprise_unlocks": {
            "status": LOCKED_ENTERPRISE_STATUS,
            "capabilities": [
                "prompt-derived semantic intent extraction",
                "task, ticket, and pull-request intent correlation",
                "private workflow and change-management context comparison",
                "live drift alerts for tool and target changes",
                "SIEM export for intent-to-action drift events",
            ],
            "private_package": "cavra_enterprise",
        },
    }


def build_aispm_tool_chain_graph(
    activity_store: Any,
    *,
    repository: str | None = None,
    agent_id: str | None = None,
    policy_pack: str | None = None,
    limit: int = 200,
) -> dict[str, Any]:
    """Build a public-safe tool-chain graph from local decision metadata.

    Community exposes redacted node/edge summaries only. Enterprise owns raw
    tool payloads, cross-system call graphs, connector spans, latency traces,
    and full session replay.
    """

    limit = max(1, min(limit, 500))
    decisions = activity_store.list_decisions(
        repository=repository,
        agent_id=agent_id,
        policy_pack=policy_pack,
        limit=limit,
    )["items"]
    graph = _tool_chain_graph(decisions)
    node_counts = Counter(str(node.get("node_type", "unknown")) for node in graph["nodes"])
    high_risk_edges = [edge for edge in graph["edges"] if int(edge.get("risk_score", 0)) >= 70]
    blocked_edges = [edge for edge in graph["edges"] if edge.get("decision") == "block"]
    return {
        "schema_version": "cavra.aispm.tool_chain_graph.v1",
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
            "node_count": len(graph["nodes"]),
            "edge_count": len(graph["edges"]),
            "agent_nodes": node_counts["agent"],
            "tool_nodes": node_counts["tool"],
            "target_nodes": node_counts["target"],
            "high_risk_edges": len(high_risk_edges),
            "blocked_edges": len(blocked_edges),
            "evidence_confidence": _evidence_confidence(decisions),
        },
        "nodes": graph["nodes"],
        "edges": graph["edges"],
        "hotspots": graph["hotspots"],
        "redaction": {
            "raw_tool_payload": LOCKED_ENTERPRISE_STATUS,
            "tool_result_body": LOCKED_ENTERPRISE_STATUS,
            "prompt_context": LOCKED_ENTERPRISE_STATUS,
            "connector_spans": LOCKED_ENTERPRISE_STATUS,
            "cross_system_call_graph": LOCKED_ENTERPRISE_STATUS,
            "private_network_targets": LOCKED_ENTERPRISE_STATUS,
        },
        "enterprise_unlocks": {
            "status": LOCKED_ENTERPRISE_STATUS,
            "capabilities": [
                "raw tool request and response graphing",
                "cross-system call graph from MCP, shell, Git, CI, cloud, and SaaS connectors",
                "latency and execution span correlation",
                "private network and identity-aware target mapping",
                "live tool-chain alerts and SIEM export",
            ],
            "private_package": "cavra_enterprise",
        },
    }


def build_aispm_agent_blast_radius(
    activity_store: Any,
    *,
    repository: str | None = None,
    agent_id: str | None = None,
    policy_pack: str | None = None,
    limit: int = 200,
) -> dict[str, Any]:
    """Build a public-safe agent blast-radius map from local metadata.

    Community maps an agent's observed reach across repositories, tools,
    control surfaces, policy packs, approval routes, and redacted target
    classes. Enterprise owns private asset graphs, identity permissions, cloud
    dependency context, customer topology, and live connector enrichment.
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
    items = _agent_blast_radius(decisions, sessions)
    level_counts = Counter(str(item.get("blast_radius_level", "low")) for item in items)
    repositories = {repo for item in items for repo in item.get("repositories", [])}
    approval_paths = {path for item in items for path in item.get("approval_paths", [])}
    return {
        "schema_version": "cavra.aispm.agent_blast_radius.v1",
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
            "critical_agents": level_counts["critical"],
            "high_agents": level_counts["high"],
            "medium_agents": level_counts["medium"],
            "low_agents": level_counts["low"],
            "affected_repositories": len(repositories),
            "approval_paths": len(approval_paths),
            "evidence_confidence": _evidence_confidence(decisions),
        },
        "items": items,
        "redaction": {
            "private_asset_graph": LOCKED_ENTERPRISE_STATUS,
            "identity_permission_graph": LOCKED_ENTERPRISE_STATUS,
            "cloud_account_inventory": LOCKED_ENTERPRISE_STATUS,
            "dependency_graph": LOCKED_ENTERPRISE_STATUS,
            "secret_names": LOCKED_ENTERPRISE_STATUS,
            "customer_topology": LOCKED_ENTERPRISE_STATUS,
        },
        "enterprise_unlocks": {
            "status": LOCKED_ENTERPRISE_STATUS,
            "capabilities": [
                "identity and permission-aware blast-radius analysis",
                "cloud account, Kubernetes, SaaS, and repository dependency graphing",
                "private asset criticality and owner enrichment",
                "secret and data classification mapping without public disclosure",
                "live blast-radius alerts and executive risk narrative export",
            ],
            "private_package": "cavra_enterprise",
        },
    }


def build_aispm_control_coverage_heatmap(
    activity_store: Any,
    *,
    repository: str | None = None,
    agent_id: str | None = None,
    policy_pack: str | None = None,
    limit: int = 200,
) -> dict[str, Any]:
    """Build a public-safe control coverage heatmap from local metadata.

    Community heatmaps pivot normalized decisions by agent, repository, and
    control surface. Private repository ownership, user identities, CMDB
    criticality, environment tier, and organization-wide live baselines remain
    Enterprise-only enrichment.
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
    heatmap = _control_coverage_heatmap(decisions, sessions)
    status_counts = Counter(cell["coverage_status"] for row in heatmap["rows"] for cell in row["cells"])
    return {
        "schema_version": "cavra.aispm.control_coverage_heatmap.v1",
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
            "row_count": len(heatmap["rows"]),
            "surface_count": len(heatmap["surfaces"]),
            "cell_count": sum(len(row["cells"]) for row in heatmap["rows"]),
            "enforced_cells": status_counts["enforced"],
            "approval_gated_cells": status_counts["approval_gated"],
            "warning_only_cells": status_counts["warning_only"],
            "observed_cells": status_counts["observed"] + status_counts["attested"],
            "not_observed_cells": status_counts["not_observed_locally"],
            "coverage_score": heatmap["coverage_score"],
            "evidence_confidence": _evidence_confidence(decisions),
        },
        "surfaces": heatmap["surfaces"],
        "rows": heatmap["rows"],
        "top_gaps": heatmap["top_gaps"],
        "redaction": {
            "private_repository_owner_graph": LOCKED_ENTERPRISE_STATUS,
            "identity_provider_claims": LOCKED_ENTERPRISE_STATUS,
            "repository_permission_matrix": LOCKED_ENTERPRISE_STATUS,
            "environment_criticality": LOCKED_ENTERPRISE_STATUS,
            "cmdb_service_mapping": LOCKED_ENTERPRISE_STATUS,
            "live_org_baselines": LOCKED_ENTERPRISE_STATUS,
        },
        "enterprise_unlocks": {
            "status": LOCKED_ENTERPRISE_STATUS,
            "capabilities": [
                "organization-wide live control coverage baselines",
                "repository owner, service criticality, and environment-tier enrichment",
                "identity and permission-scoped heatmap filtering",
                "policy pack rollout coverage by business unit",
                "coverage SLO alerts and executive compliance exports",
            ],
            "private_package": "cavra_enterprise",
        },
    }


def build_aispm_evidence_confidence_drilldown(
    activity_store: Any,
    *,
    repository: str | None = None,
    agent_id: str | None = None,
    policy_pack: str | None = None,
    limit: int = 200,
) -> dict[str, Any]:
    """Build a public-safe evidence confidence drilldown.

    Community evaluates only normalized evidence reference metadata already
    stored with decisions and sessions. It does not verify private artifacts,
    inspect evidence payloads, or call a license/SaaS evidence service.
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
    drilldown = _evidence_confidence_drilldown(decisions, sessions)
    return {
        "schema_version": "cavra.aispm.evidence_confidence.v1",
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
        "summary": drilldown["summary"],
        "facts": drilldown["facts"],
        "redaction": {
            "raw_evidence_payload": LOCKED_ENTERPRISE_STATUS,
            "private_artifact_contents": LOCKED_ENTERPRISE_STATUS,
            "signature_trust_chain": LOCKED_ENTERPRISE_STATUS,
            "identity_provider_claims": LOCKED_ENTERPRISE_STATUS,
            "external_ticket_payloads": LOCKED_ENTERPRISE_STATUS,
            "customer_data": LOCKED_ENTERPRISE_STATUS,
            "tenant_evidence_store": LOCKED_ENTERPRISE_STATUS,
        },
        "enterprise_unlocks": {
            "status": LOCKED_ENTERPRISE_STATUS,
            "capabilities": [
                "immutable evidence store verification",
                "signed artifact and provenance validation",
                "SIEM, GRC, and ticket correlation",
                "evidence freshness SLO alerts",
                "long-term retention and auditor export workflows",
            ],
            "private_package": "cavra_enterprise",
        },
    }


def build_aispm_evidence_freshness_slo(
    activity_store: Any,
    *,
    repository: str | None = None,
    agent_id: str | None = None,
    policy_pack: str | None = None,
    limit: int = 200,
) -> dict[str, Any]:
    """Build a public-safe evidence freshness and retention SLO packet.

    Community can compute timestamp freshness and reference-level retention
    hints from local activity metadata. Private archive validation, object-lock
    status, KMS status, lifecycle policy checks, and tenant evidence stores are
    Enterprise-only.
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
    generated_at = utc_now()
    slo = _evidence_freshness_slo(decisions, sessions, generated_at=generated_at)
    return {
        "schema_version": "cavra.aispm.evidence_freshness.v1",
        "product": "CAVRA",
        "edition": "community",
        "mode": "local_activity",
        "data_provenance": "local_activity_store",
        "tracking": "none",
        "telemetry": "disabled",
        "generated_at": generated_at,
        "filters": {
            "repository": repository,
            "agent_id": agent_id,
            "policy_pack": policy_pack,
            "limit": limit,
        },
        "slo_policy": slo["slo_policy"],
        "summary": slo["summary"],
        "items": slo["items"],
        "redaction": {
            "tenant_evidence_store": LOCKED_ENTERPRISE_STATUS,
            "immutable_archive_probe": LOCKED_ENTERPRISE_STATUS,
            "object_lock_status": LOCKED_ENTERPRISE_STATUS,
            "kms_key_health": LOCKED_ENTERPRISE_STATUS,
            "retention_lifecycle_policy": LOCKED_ENTERPRISE_STATUS,
            "external_archive_metadata": LOCKED_ENTERPRISE_STATUS,
            "auditor_export_manifest": LOCKED_ENTERPRISE_STATUS,
        },
        "enterprise_unlocks": {
            "status": LOCKED_ENTERPRISE_STATUS,
            "capabilities": [
                "immutable evidence archive health validation",
                "object-lock, KMS, and lifecycle policy readiness checks",
                "tenant retention SLO alerts and breach escalation",
                "archive restore drills and auditor export manifests",
                "cross-system evidence freshness correlation",
            ],
            "private_package": "cavra_enterprise",
        },
    }


def build_aispm_executive_risk_narrative(
    activity_store: Any,
    *,
    repository: str | None = None,
    agent_id: str | None = None,
    policy_pack: str | None = None,
    limit: int = 200,
) -> dict[str, Any]:
    """Build a deterministic public-safe executive risk narrative.

    Community narratives summarize local/sample posture metrics only. Private
    tenant trends, business owner context, customer impact, and AI-generated
    board-ready language remain Enterprise-only.
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
    generated_at = utc_now()
    findings = _risk_findings(decisions)
    overview = _posture_overview(decisions, sessions, findings)
    freshness = _evidence_freshness_slo(decisions, sessions, generated_at=generated_at)
    narrative = _executive_risk_narrative(decisions, sessions, findings, overview, freshness)
    return {
        "schema_version": "cavra.aispm.executive_risk_narrative.v1",
        "product": "CAVRA",
        "edition": "community",
        "mode": "local_activity",
        "data_provenance": "local_activity_store",
        "tracking": "none",
        "telemetry": "disabled",
        "generated_at": generated_at,
        "filters": {
            "repository": repository,
            "agent_id": agent_id,
            "policy_pack": policy_pack,
            "limit": limit,
        },
        "narrative": narrative,
        "redaction": {
            "raw_prompts": LOCKED_ENTERPRISE_STATUS,
            "model_reasoning": LOCKED_ENTERPRISE_STATUS,
            "private_business_context": LOCKED_ENTERPRISE_STATUS,
            "customer_impact_analysis": LOCKED_ENTERPRISE_STATUS,
            "trend_history": LOCKED_ENTERPRISE_STATUS,
            "ai_generated_board_summary": LOCKED_ENTERPRISE_STATUS,
            "tenant_benchmarking": LOCKED_ENTERPRISE_STATUS,
        },
        "enterprise_unlocks": {
            "status": LOCKED_ENTERPRISE_STATUS,
            "capabilities": [
                "AI-assisted board and CSO narrative generation",
                "private trend history and tenant benchmarking",
                "business owner, service criticality, and customer-impact enrichment",
                "scheduled executive brief delivery",
                "GRC and incident packet export",
            ],
            "private_package": "cavra_enterprise",
        },
    }


def build_aispm_replay_to_policy_draft(
    activity_store: Any,
    *,
    session_id: str | None = None,
    repository: str | None = None,
    agent_id: str | None = None,
    policy_pack: str | None = None,
    limit: int = 200,
) -> dict[str, Any]:
    """Build a read-only policy draft from public-safe replay metadata.

    Community converts normalized policy decisions into candidate controls. It
    does not inspect raw prompts, model reasoning, raw tool payloads, ticket
    bodies, private asset graphs, or customer context.
    """

    limit = max(1, min(limit, 500))
    if session_id:
        decisions = activity_store.list_decisions(session_id=session_id, limit=limit)["items"]
        get_session = getattr(activity_store, "get_session", None)
        session = get_session(session_id) if callable(get_session) else None
        source_sessions = [session] if session else []
    else:
        decisions = activity_store.list_decisions(
            repository=repository,
            agent_id=agent_id,
            policy_pack=policy_pack,
            limit=limit,
        )["items"]
        source_sessions = activity_store.list_sessions(
            repository=repository,
            agent_id=agent_id,
            policy_pack=policy_pack,
            limit=limit,
        )["items"]
    draft = _replay_to_policy_draft(
        decisions,
        sessions=source_sessions,
        source_scope=session_id or repository or agent_id or policy_pack or "local_activity_window",
    )
    return {
        "schema_version": "cavra.aispm.replay_to_policy_draft.v1",
        "product": "CAVRA",
        "edition": "community",
        "mode": "local_activity",
        "data_provenance": "local_activity_store",
        "tracking": "none",
        "telemetry": "disabled",
        "generated_at": utc_now(),
        "filters": {
            "session_id": session_id,
            "repository": repository,
            "agent_id": agent_id,
            "policy_pack": policy_pack,
            "limit": limit,
        },
        **draft,
        "redaction": {
            "raw_prompts": LOCKED_ENTERPRISE_STATUS,
            "model_reasoning": LOCKED_ENTERPRISE_STATUS,
            "raw_tool_payloads": LOCKED_ENTERPRISE_STATUS,
            "ticket_or_change_context": LOCKED_ENTERPRISE_STATUS,
            "private_asset_graph": LOCKED_ENTERPRISE_STATUS,
            "customer_context": LOCKED_ENTERPRISE_STATUS,
            "private_approval_policy": LOCKED_ENTERPRISE_STATUS,
        },
        "enterprise_unlocks": {
            "status": LOCKED_ENTERPRISE_STATUS,
            "capabilities": [
                "AI-assisted rule authoring from prompts, reasoning traces, and tool payloads",
                "private ticket, CMDB, asset, identity, and service criticality enrichment",
                "approval-bound policy publish workflow automation",
                "policy simulation against tenant history before rollout",
                "organization-wide policy-pack recommendation campaigns",
            ],
            "private_package": "cavra_enterprise",
        },
    }


def build_aispm_replay_to_policy_tests(
    activity_store: Any,
    *,
    session_id: str | None = None,
    repository: str | None = None,
    agent_id: str | None = None,
    policy_pack: str | None = None,
    limit: int = 200,
) -> dict[str, Any]:
    """Export public-safe policy test fixtures from replay-derived controls.

    Community exports deterministic assertion fixtures only. It does not run
    private tenant-history simulation, use raw prompts, or validate private
    connector payloads.
    """

    draft_packet = build_aispm_replay_to_policy_draft(
        activity_store,
        session_id=session_id,
        repository=repository,
        agent_id=agent_id,
        policy_pack=policy_pack,
        limit=limit,
    )
    fixture = _replay_to_policy_test_fixture(
        draft_packet["recommendations"],
        draft_packet["policy_draft"]["policy_pack"],
        source_scope=draft_packet["summary"].get("source_scope", "local_activity_window"),
    )
    return {
        "schema_version": "cavra.aispm.replay_to_policy_tests.v1",
        "product": "CAVRA",
        "edition": "community",
        "mode": "local_activity",
        "data_provenance": draft_packet["data_provenance"],
        "tracking": "none",
        "telemetry": "disabled",
        "generated_at": utc_now(),
        "filters": draft_packet["filters"],
        "summary": {
            "source_decisions": draft_packet["summary"]["source_decisions"],
            "recommended_rules": draft_packet["summary"]["recommended_rules"],
            "test_cases": len(fixture["cases"]),
            "fixture_valid": True,
            "source_scope": draft_packet["summary"].get("source_scope", "local_activity_window"),
            "policy_id": fixture["policy_id"],
        },
        "test_fixture": fixture,
        "export": {
            "status": "read_only_preview",
            "suggested_path": f"tests/fixtures/replay-to-policy/{fixture['policy_id']}.json",
            "next_step": "Review the fixture, commit it with the policy draft, and validate through repository CI before rollout.",
            "approval_required": True,
        },
        "redaction": {
            "raw_prompts": LOCKED_ENTERPRISE_STATUS,
            "model_reasoning": LOCKED_ENTERPRISE_STATUS,
            "raw_tool_payloads": LOCKED_ENTERPRISE_STATUS,
            "private_simulation_history": LOCKED_ENTERPRISE_STATUS,
            "ticket_or_change_context": LOCKED_ENTERPRISE_STATUS,
            "customer_context": LOCKED_ENTERPRISE_STATUS,
        },
        "enterprise_unlocks": {
            "status": LOCKED_ENTERPRISE_STATUS,
            "capabilities": [
                "policy test generation from prompts, reasoning traces, and raw tool payloads",
                "tenant-history simulation before policy rollout",
                "private ticket, asset, identity, and service criticality enrichment",
                "CI write-back for approved policy tests",
                "organization-wide regression campaigns for generated policy packs",
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
            "declared_intent": "Apply approved production infrastructure change",
            "policy_pack": "cloud-iam-prod",
            "rule_id": "iac.production-change",
            "tool": "shell",
            "tool_capability": "runtime_execution",
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
            "declared_intent": "Inspect deployment configuration",
            "policy_pack": "cavra-ai-agent-baseline",
            "rule_id": "secrets.block-sensitive-read",
            "tool": "filesystem",
            "tool_capability": "file_read",
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
            "declared_intent": "Write generated infrastructure documentation",
            "policy_pack": "mcp-enterprise",
            "rule_id": "mcp.untrusted-tool",
            "tool": "filesystem.write",
            "server": "filesystem-mcp",
            "tool_capability": "workspace_write",
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
    overview = _posture_overview(decisions, sessions, findings)
    evidence_freshness_slo = _evidence_freshness_slo(decisions, sessions, generated_at="2026-06-09T00:03:00+00:00")
    replay_to_policy_draft = _replay_to_policy_draft(
        decisions,
        sessions=sessions,
        source_scope="sample-session-001",
    )
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
        "overview": overview,
        "agents": _agent_observability(decisions, sessions),
        "findings": findings,
        "timeline": _timeline(decisions, sessions),
        "control_coverage": _control_coverage(decisions),
        "near_misses": _near_misses(decisions),
        "approval_lineage": _sample_approval_lineage(decisions),
        "behavior_fingerprints": _behavior_fingerprints(decisions, sessions),
        "policy_context_gaps": _policy_context_gaps(decisions),
        "pre_action_risk_forecasts": _pre_action_risk_forecasts(decisions),
        "intent_action_drift": _intent_action_drift(decisions),
        "tool_chain_graph": _tool_chain_graph(decisions),
        "agent_blast_radius": _agent_blast_radius(decisions, sessions),
        "control_coverage_heatmap": _control_coverage_heatmap(decisions, sessions),
        "evidence_confidence_drilldown": _evidence_confidence_drilldown(decisions, sessions),
        "evidence_freshness_slo": evidence_freshness_slo,
        "executive_risk_narrative": _executive_risk_narrative(
            decisions,
            sessions,
            findings,
            overview,
            evidence_freshness_slo,
        ),
        "replay_to_policy_draft": replay_to_policy_draft,
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


def _pre_action_risk_forecasts(decisions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    forecasts: list[dict[str, Any]] = []
    for decision in decisions:
        status = _forecast_status(decision)
        target_summary, target_redacted = _safe_target_summary(decision)
        surface = _control_surface(decision)
        forecasts.append(
            {
                "forecast_id": f"forecast-{decision.get('decision_id', 'unknown')}",
                "decision_id": decision.get("decision_id"),
                "session_id": decision.get("session_id"),
                "agent_id": decision.get("agent_id", "unknown-agent"),
                "repository": decision.get("repository", "local"),
                "policy_pack": decision.get("policy_pack", "cavra-ai-agent-baseline"),
                "rule_id": decision.get("rule_id", "runtime.default"),
                "action_type": decision.get("action_type", "unknown"),
                "target_summary": target_summary,
                "target_redacted": target_redacted,
                "decision": decision.get("decision", "unknown"),
                "severity": decision.get("severity", "low"),
                "risk_classification": _risk_classification(decision),
                "control_surface": surface,
                "forecast_status": status,
                "projected_blast_radius": _projected_blast_radius(surface),
                "likely_impacts": _likely_forecast_impacts(surface),
                "pre_action_controls": _pre_action_controls(status, surface),
                "confidence": "metadata_forecast",
                "evidence_refs": list(decision.get("evidence_refs", [])),
                "timestamp": decision.get("timestamp"),
            }
        )
    return sorted(
        forecasts,
        key=lambda item: (
            _forecast_priority(str(item.get("forecast_status", ""))),
            str(item.get("timestamp", "")),
        ),
        reverse=True,
    )


def _forecast_status(decision: dict[str, Any]) -> str:
    outcome = str(decision.get("decision", "unknown"))
    severity = str(decision.get("severity", "low"))
    if outcome == "block" or severity == "critical":
        return "block_recommended"
    if outcome == "require_approval" or severity == "high":
        return "approval_recommended"
    if outcome in {"warn", "allow_with_attestation"} or severity == "medium":
        return "warn_recommended"
    return "monitor"


def _forecast_priority(status: str) -> int:
    priorities = {
        "block_recommended": 4,
        "approval_recommended": 3,
        "warn_recommended": 2,
        "monitor": 1,
    }
    return priorities.get(status, 0)


def _projected_blast_radius(surface: str) -> str:
    radii = {
        "sensitive_data": "secret_scope",
        "infrastructure_iac": "production_infrastructure",
        "mcp_tools": "tooling_surface",
        "source_control": "source_control_scope",
        "runtime_commands": "runtime_scope",
        "general_policy": "local_policy_scope",
    }
    return radii.get(surface, "local_policy_scope")


def _likely_forecast_impacts(surface: str) -> list[str]:
    impacts = {
        "sensitive_data": [
            "credential_or_sensitive_data_exposure",
            "data_exfiltration",
            "audit_scope_expansion",
        ],
        "infrastructure_iac": [
            "production_infrastructure_change",
            "configuration_drift",
            "service_availability_impact",
        ],
        "mcp_tools": [
            "untrusted_tool_write_access",
            "workspace_mutation",
            "toolchain_expansion",
        ],
        "source_control": [
            "protected_branch_mutation",
            "release_integrity_impact",
            "review_bypass_risk",
        ],
        "runtime_commands": [
            "local_runtime_mutation",
            "dependency_or_script_execution",
            "workstation_state_change",
        ],
        "general_policy": ["policy_visibility_gap"],
    }
    return impacts.get(surface, impacts["general_policy"])


def _pre_action_controls(status: str, surface: str) -> list[str]:
    controls = {
        "block_recommended": ["block_before_execution", "require_operator_review", "capture_evidence"],
        "approval_recommended": ["require_human_approval", "verify_change_window", "attach_evidence"],
        "warn_recommended": ["warn_operator", "require_attestation", "monitor_follow_up"],
        "monitor": ["record_decision", "capture_evidence"],
    }.get(status, ["record_decision", "capture_evidence"])
    surface_controls = {
        "sensitive_data": ["redact_sensitive_target"],
        "infrastructure_iac": ["require_blast_radius_context"],
        "mcp_tools": ["verify_tool_trust_tier"],
        "source_control": ["verify_branch_protection"],
        "runtime_commands": ["verify_execution_environment"],
    }
    return list(dict.fromkeys([*controls, *surface_controls.get(surface, [])]))


def _intent_action_drift(decisions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    drift_items: list[dict[str, Any]] = []
    for decision in decisions:
        declared_intent = _declared_intent(decision)
        target_summary, target_redacted = _safe_target_summary(decision)
        surface = _control_surface(decision)
        signals = _intent_drift_signals(decision, declared_intent, surface, target_redacted)
        drift_score = _intent_drift_score(decision, signals)
        drift_items.append(
            {
                "drift_id": f"intent-drift-{decision.get('decision_id', 'unknown')}",
                "decision_id": decision.get("decision_id"),
                "session_id": decision.get("session_id"),
                "agent_id": decision.get("agent_id", "unknown-agent"),
                "repository": decision.get("repository", "local"),
                "policy_pack": decision.get("policy_pack", "cavra-ai-agent-baseline"),
                "rule_id": decision.get("rule_id", "runtime.default"),
                "declared_intent": declared_intent or "intent not recorded",
                "action_type": decision.get("action_type", "unknown"),
                "target_summary": target_summary,
                "target_redacted": target_redacted,
                "decision": decision.get("decision", "unknown"),
                "severity": decision.get("severity", "low"),
                "risk_classification": _risk_classification(decision),
                "control_surface": surface,
                "drift_status": _intent_drift_status(drift_score, declared_intent),
                "drift_score": drift_score,
                "drift_signals": signals,
                "recommended_action": _intent_drift_recommended_action(signals, surface),
                "confidence": "metadata_intent_comparison",
                "evidence_refs": list(decision.get("evidence_refs", [])),
                "timestamp": decision.get("timestamp"),
            }
        )
    return sorted(
        drift_items,
        key=lambda item: (int(item.get("drift_score", 0)), str(item.get("timestamp", ""))),
        reverse=True,
    )


def _declared_intent(decision: dict[str, Any]) -> str | None:
    aliases = (
        "declared_intent",
        "intent",
        "requested_intent",
        "user_intent",
        "task_intent",
        "business_intent",
    )
    containers = [
        decision,
        decision.get("context") if isinstance(decision.get("context"), dict) else {},
        decision.get("metadata") if isinstance(decision.get("metadata"), dict) else {},
        decision.get("labels") if isinstance(decision.get("labels"), dict) else {},
    ]
    for container in containers:
        if not isinstance(container, dict):
            continue
        for key in aliases:
            value = container.get(key)
            if value not in {None, ""}:
                return str(value)
    return None


def _intent_drift_signals(
    decision: dict[str, Any],
    declared_intent: str | None,
    surface: str,
    target_redacted: bool,
) -> list[str]:
    signals: list[str] = []
    normalized_intent = (declared_intent or "").lower()
    action_type = str(decision.get("action_type", "")).lower()
    target = str(decision.get("target") or decision.get("requested_operation") or "").lower()
    outcome = str(decision.get("decision", "unknown"))
    severity = str(decision.get("severity", "low"))

    if not declared_intent:
        signals.append("missing_declared_intent")
    if target_redacted and not _intent_contains_any(normalized_intent, ["secret", "credential", "token", ".env", "sensitive"]):
        signals.append("sensitive_target_not_declared")
    if surface == "infrastructure_iac" and not _intent_contains_any(
        normalized_intent, ["infrastructure", "terraform", "tofu", "deploy", "apply", "cloud", "kubernetes", "change"]
    ):
        signals.append("infrastructure_action_not_declared")
    if surface == "mcp_tools" and "write" in target and not _intent_contains_any(
        normalized_intent, ["write", "modify", "update", "generate", "tool", "filesystem"]
    ):
        signals.append("tool_write_not_declared")
    if surface == "source_control" and not _intent_contains_any(normalized_intent, ["git", "branch", "commit", "pull request", "pr"]):
        signals.append("source_control_action_not_declared")
    if surface == "runtime_commands" and not _intent_contains_any(normalized_intent, ["run", "execute", "script", "command", "install"]):
        signals.append("runtime_execution_not_declared")
    if outcome == "block":
        signals.append("blocked_after_declared_intent")
    if outcome == "require_approval":
        signals.append("approval_required_after_declared_intent")
    if severity in {"critical", "high"}:
        signals.append("critical_or_high_intent_drift")
    if declared_intent and action_type and action_type.replace("_", " ") not in normalized_intent:
        signals.append("action_type_not_explicit_in_intent")
    return list(dict.fromkeys(signals))


def _intent_contains_any(intent: str, terms: list[str]) -> bool:
    return any(term in intent for term in terms)


def _intent_drift_score(decision: dict[str, Any], signals: list[str]) -> int:
    weights = {
        "missing_declared_intent": 35,
        "sensitive_target_not_declared": 35,
        "infrastructure_action_not_declared": 24,
        "tool_write_not_declared": 20,
        "source_control_action_not_declared": 20,
        "runtime_execution_not_declared": 20,
        "blocked_after_declared_intent": 18,
        "approval_required_after_declared_intent": 10,
        "critical_or_high_intent_drift": 14,
        "action_type_not_explicit_in_intent": 6,
    }
    score = sum(weights.get(signal, 0) for signal in signals)
    severity = str(decision.get("severity", "low"))
    if severity == "critical":
        score += 8
    elif severity == "high":
        score += 5
    return max(0, min(score, 100))


def _intent_drift_status(drift_score: int, declared_intent: str | None) -> str:
    if not declared_intent:
        return "unknown_intent"
    if drift_score >= 70:
        return "high_drift"
    if drift_score >= 35:
        return "needs_review"
    return "aligned"


def _intent_drift_recommended_action(signals: list[str], surface: str) -> str:
    if "missing_declared_intent" in signals:
        return "Require the agent or workflow to attach declared intent before evaluating the action."
    if "sensitive_target_not_declared" in signals:
        return "Block or escalate until the declared intent explicitly covers sensitive-data access."
    if surface == "infrastructure_iac":
        return "Verify the requested change, blast radius, approval route, and execution target before allowing the action."
    if surface == "mcp_tools":
        return "Verify tool trust tier, write scope, and declared workflow intent before allowing broad tool use."
    if surface == "source_control":
        return "Verify branch protection, review path, and requested repository change before allowing mutation."
    if surface == "runtime_commands":
        return "Verify execution environment and command purpose before allowing runtime execution."
    return "Compare declared intent with the observed action and require attestation if the scope changed."


def _tool_chain_graph(decisions: list[dict[str, Any]]) -> dict[str, Any]:
    nodes_by_id: dict[str, dict[str, Any]] = {}
    edges: list[dict[str, Any]] = []
    hotspot_counts: dict[str, Counter[str]] = defaultdict(Counter)
    hotspot_evidence: dict[str, list[str]] = defaultdict(list)

    for decision in decisions:
        agent_id = str(decision.get("agent_id", "unknown-agent"))
        repository = str(decision.get("repository", "local"))
        tool_label = _tool_label(decision)
        target_summary, target_redacted = _safe_target_summary(decision)
        surface = _control_surface(decision)
        risk_score = _tool_chain_risk_score(decision, target_redacted)
        risk_band = _tool_chain_risk_band(risk_score)
        decision_id = str(decision.get("decision_id", "unknown"))
        edge_id_prefix = f"tool-edge-{decision_id}"

        agent_node = _graph_node(
            node_id=_node_id("agent", agent_id),
            node_type="agent",
            label=agent_id,
            risk_band="observed",
            metadata={"repository": repository},
        )
        tool_node = _graph_node(
            node_id=_node_id("tool", tool_label),
            node_type="tool",
            label=tool_label,
            risk_band=risk_band,
            metadata={"control_surface": surface, "tool_capability": _tool_capability(decision)},
        )
        target_node = _graph_node(
            node_id=_node_id("target", f"{surface}:{target_summary}"),
            node_type="target",
            label=target_summary,
            risk_band=risk_band,
            metadata={"control_surface": surface, "target_redacted": target_redacted},
        )
        policy_node = _graph_node(
            node_id=_node_id("policy", str(decision.get("policy_pack", "cavra-ai-agent-baseline"))),
            node_type="policy",
            label=str(decision.get("policy_pack", "cavra-ai-agent-baseline")),
            risk_band="observed",
            metadata={"rule_id": str(decision.get("rule_id", "runtime.default"))},
        )

        for node in (agent_node, tool_node, target_node, policy_node):
            existing = nodes_by_id.get(str(node["node_id"]))
            if existing:
                existing["decision_count"] = int(existing.get("decision_count", 0)) + 1
                existing["risk_score"] = max(int(existing.get("risk_score", 0)), int(node.get("risk_score", 0)))
                existing["risk_band"] = _tool_chain_risk_band(int(existing["risk_score"]))
            else:
                nodes_by_id[str(node["node_id"])] = node

        common = {
            "decision_id": decision.get("decision_id"),
            "session_id": decision.get("session_id"),
            "agent_id": agent_id,
            "repository": repository,
            "action_type": decision.get("action_type", "unknown"),
            "decision": decision.get("decision", "unknown"),
            "severity": decision.get("severity", "low"),
            "risk_classification": _risk_classification(decision),
            "control_surface": surface,
            "risk_score": risk_score,
            "risk_band": risk_band,
            "evidence_refs": list(decision.get("evidence_refs", [])),
            "timestamp": decision.get("timestamp"),
        }
        edges.extend(
            [
                {
                    "edge_id": f"{edge_id_prefix}-agent-tool",
                    "source": agent_node["node_id"],
                    "target": tool_node["node_id"],
                    "relationship": "invoked_tool",
                    **common,
                },
                {
                    "edge_id": f"{edge_id_prefix}-tool-target",
                    "source": tool_node["node_id"],
                    "target": target_node["node_id"],
                    "relationship": "requested_target",
                    "target_redacted": target_redacted,
                    **common,
                },
                {
                    "edge_id": f"{edge_id_prefix}-policy-decision",
                    "source": policy_node["node_id"],
                    "target": tool_node["node_id"],
                    "relationship": "governed_tool",
                    **common,
                },
            ]
        )

        hotspot_key = f"{agent_id}::{repository}"
        hotspot_counts[hotspot_key]["decisions"] += 1
        hotspot_counts[hotspot_key][str(decision.get("decision", "unknown"))] += 1
        hotspot_counts[hotspot_key][surface] += 1
        hotspot_counts[hotspot_key]["risk_score"] = max(hotspot_counts[hotspot_key]["risk_score"], risk_score)
        hotspot_evidence[hotspot_key].extend(list(decision.get("evidence_refs", [])))

    hotspots = [
        {
            "hotspot_id": _node_id("hotspot", key),
            "agent_id": key.split("::", 1)[0],
            "repository": key.split("::", 1)[1],
            "decision_count": counts["decisions"],
            "blocked_edges": counts["block"],
            "approval_required_edges": counts["require_approval"],
            "warned_edges": counts["warn"],
            "dominant_surface": _dominant_surface(counts),
            "risk_score": counts["risk_score"],
            "risk_band": _tool_chain_risk_band(counts["risk_score"]),
            "evidence_refs": list(dict.fromkeys(hotspot_evidence[key]))[:8],
        }
        for key, counts in hotspot_counts.items()
    ]

    return {
        "nodes": sorted(nodes_by_id.values(), key=lambda item: (str(item.get("node_type")), str(item.get("label")))),
        "edges": sorted(edges, key=lambda item: (int(item.get("risk_score", 0)), str(item.get("timestamp", ""))), reverse=True),
        "hotspots": sorted(hotspots, key=lambda item: (int(item.get("risk_score", 0)), int(item.get("decision_count", 0))), reverse=True),
    }


def _graph_node(
    *,
    node_id: str,
    node_type: str,
    label: str,
    risk_band: str,
    metadata: dict[str, Any],
) -> dict[str, Any]:
    return {
        "node_id": node_id,
        "node_type": node_type,
        "label": label,
        "risk_band": risk_band,
        "risk_score": _risk_band_score(risk_band),
        "decision_count": 1,
        "metadata": metadata,
    }


def _node_id(prefix: str, value: str) -> str:
    cleaned = "".join(ch if ch.isalnum() else "-" for ch in value.lower()).strip("-")
    while "--" in cleaned:
        cleaned = cleaned.replace("--", "-")
    return f"{prefix}-{cleaned or 'unknown'}"[:120]


def _tool_label(decision: dict[str, Any]) -> str:
    for container in (
        decision,
        decision.get("context") if isinstance(decision.get("context"), dict) else {},
        decision.get("metadata") if isinstance(decision.get("metadata"), dict) else {},
        decision.get("labels") if isinstance(decision.get("labels"), dict) else {},
    ):
        if not isinstance(container, dict):
            continue
        for key in ("tool", "tool_name", "server", "mcp_server", "operation"):
            value = container.get(key)
            if value not in {None, ""}:
                return str(value)
    action_type = str(decision.get("action_type", "unknown"))
    target = str(decision.get("target") or decision.get("requested_operation") or "")
    if action_type == "mcp_tool_call" and target:
        return target
    if "command" in action_type and target:
        return "shell"
    if "file" in action_type:
        return "filesystem"
    if "git" in action_type:
        return "git"
    return action_type or "unknown-tool"


def _tool_capability(decision: dict[str, Any]) -> str:
    for container in (
        decision,
        decision.get("context") if isinstance(decision.get("context"), dict) else {},
        decision.get("metadata") if isinstance(decision.get("metadata"), dict) else {},
        decision.get("labels") if isinstance(decision.get("labels"), dict) else {},
    ):
        if not isinstance(container, dict):
            continue
        value = container.get("tool_capability") or container.get("capability")
        if value not in {None, ""}:
            return str(value)
    return _control_surface(decision)


def _tool_chain_risk_score(decision: dict[str, Any], target_redacted: bool) -> int:
    score = RISK_WEIGHTS.get(str(decision.get("severity", "low")), 3)
    score += DECISION_RISK_WEIGHTS.get(str(decision.get("decision", "audit_only")), 0)
    surface = _control_surface(decision)
    if surface == "sensitive_data":
        score += 34
    elif surface == "infrastructure_iac":
        score += 24
    elif surface == "mcp_tools":
        score += 18
    elif surface in {"runtime_commands", "source_control"}:
        score += 14
    if target_redacted:
        score += 10
    if str(decision.get("decision", "")) == "block":
        score += 8
    return max(0, min(score, 100))


def _tool_chain_risk_band(score: int) -> str:
    if score >= 70:
        return "critical"
    if score >= 50:
        return "high"
    if score >= 25:
        return "medium"
    return "low"


def _risk_band_score(risk_band: str) -> int:
    return {
        "critical": 85,
        "high": 62,
        "medium": 38,
        "low": 12,
        "observed": 5,
    }.get(risk_band, 0)


def _dominant_surface(counts: Counter[str]) -> str:
    surfaces = [
        "sensitive_data",
        "infrastructure_iac",
        "mcp_tools",
        "source_control",
        "runtime_commands",
        "general_policy",
    ]
    return max(surfaces, key=lambda surface: counts[surface], default="general_policy")


def _agent_blast_radius(decisions: list[dict[str, Any]], sessions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped_decisions: dict[str, list[dict[str, Any]]] = defaultdict(list)
    grouped_sessions: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for decision in decisions:
        grouped_decisions[str(decision.get("agent_id", "unknown-agent"))].append(decision)
    for session in sessions:
        grouped_sessions[str(session.get("agent_id", "unknown-agent"))].append(session)

    items: list[dict[str, Any]] = []
    for agent_id in sorted(set(grouped_decisions) | set(grouped_sessions)):
        agent_decisions = grouped_decisions.get(agent_id, [])
        agent_sessions = grouped_sessions.get(agent_id, [])
        decision_counts = Counter(str(item.get("decision", "unknown")) for item in agent_decisions)
        repositories = sorted(
            {
                str(item.get("repository", "local"))
                for item in [*agent_decisions, *agent_sessions]
                if item.get("repository") not in {None, ""}
            }
        )
        control_surfaces = sorted({_control_surface(item) for item in agent_decisions})
        policy_packs = sorted({str(item.get("policy_pack", "cavra-ai-agent-baseline")) for item in agent_decisions})
        tool_labels = sorted({_tool_label(item) for item in agent_decisions})
        target_classes = sorted({_blast_target_class(item) for item in agent_decisions})
        approval_paths = sorted(
            {
                _approval_path(item)
                for item in agent_decisions
                if _approval_path(item) not in {None, ""}
            }
        )
        sensitive_count = sum(1 for item in agent_decisions if _control_surface(item) == "sensitive_data")
        infrastructure_count = sum(1 for item in agent_decisions if _control_surface(item) == "infrastructure_iac")
        score = _agent_blast_radius_score(
            repositories=repositories,
            control_surfaces=control_surfaces,
            decision_counts=decision_counts,
            sensitive_count=sensitive_count,
            infrastructure_count=infrastructure_count,
            tool_labels=tool_labels,
            approval_paths=approval_paths,
        )
        items.append(
            {
                "agent_id": agent_id,
                "blast_radius_level": _agent_blast_radius_level(score),
                "blast_radius_score": score,
                "repository_count": len(repositories),
                "repositories": repositories,
                "control_surfaces": control_surfaces,
                "policy_packs": policy_packs,
                "tool_labels": tool_labels,
                "target_classes": target_classes,
                "sensitive_target_count": sensitive_count,
                "production_infrastructure_count": infrastructure_count,
                "approval_paths": approval_paths,
                "decision_count": len(agent_decisions),
                "session_count": len(agent_sessions),
                "blocked_actions": decision_counts["block"],
                "approval_required_actions": decision_counts["require_approval"],
                "warned_actions": decision_counts["warn"],
                "top_risks": _agent_blast_top_risks(
                    control_surfaces=control_surfaces,
                    decision_counts=decision_counts,
                    sensitive_count=sensitive_count,
                    infrastructure_count=infrastructure_count,
                    repository_count=len(repositories),
                ),
                "recommended_controls": _agent_blast_recommended_controls(
                    control_surfaces=control_surfaces,
                    decision_counts=decision_counts,
                    approval_paths=approval_paths,
                    repository_count=len(repositories),
                ),
                "evidence_refs": list(dict.fromkeys(ref for item in agent_decisions for ref in item.get("evidence_refs", [])))[:8],
                "last_seen_at": max(
                    [str(item.get("timestamp", "")) for item in agent_decisions if item.get("timestamp")]
                    + [str(item.get("updated_at", "")) for item in agent_sessions if item.get("updated_at")],
                    default=None,
                ),
            }
        )
    return sorted(
        items,
        key=lambda item: (int(item.get("blast_radius_score", 0)), int(item.get("decision_count", 0))),
        reverse=True,
    )


def _blast_target_class(decision: dict[str, Any]) -> str:
    surface = _control_surface(decision)
    target_summary, target_redacted = _safe_target_summary(decision)
    if target_redacted:
        return f"{surface}:redacted"
    if surface == "sensitive_data":
        return "sensitive_data:nonredacted_metadata"
    if surface == "infrastructure_iac":
        return "production_infrastructure"
    if surface == "mcp_tools":
        return "tooling_surface"
    if surface == "source_control":
        return "source_control_scope"
    if surface == "runtime_commands":
        return "runtime_scope"
    return target_summary if target_summary != "target not recorded" else "local_policy_scope"


def _approval_path(decision: dict[str, Any]) -> str | None:
    context = decision.get("context") if isinstance(decision.get("context"), dict) else {}
    metadata = decision.get("metadata") if isinstance(decision.get("metadata"), dict) else {}
    for container in (decision, context, metadata):
        for key in ("approval_route", "approver_group", "approval_path"):
            value = container.get(key)
            if value not in {None, ""}:
                return str(value)
    if decision.get("decision") == "require_approval":
        return "approval_required_unassigned"
    return None


def _agent_blast_radius_score(
    *,
    repositories: list[str],
    control_surfaces: list[str],
    decision_counts: Counter[str],
    sensitive_count: int,
    infrastructure_count: int,
    tool_labels: list[str],
    approval_paths: list[str],
) -> int:
    score = 5
    score += min(16, max(0, len(repositories) - 1) * 6)
    score += min(14, max(0, len(control_surfaces) - 1) * 5)
    score += min(10, max(0, len(tool_labels) - 1) * 3)
    score += decision_counts["block"] * 18
    score += decision_counts["require_approval"] * 12
    score += decision_counts["warn"] * 5
    score += min(20, sensitive_count * 16)
    score += min(18, infrastructure_count * 12)
    if not approval_paths and (sensitive_count or infrastructure_count or decision_counts["require_approval"]):
        score += 8
    return max(0, min(score, 100))


def _agent_blast_radius_level(score: int) -> str:
    if score >= 75:
        return "critical"
    if score >= 55:
        return "high"
    if score >= 30:
        return "medium"
    return "low"


def _agent_blast_top_risks(
    *,
    control_surfaces: list[str],
    decision_counts: Counter[str],
    sensitive_count: int,
    infrastructure_count: int,
    repository_count: int,
) -> list[str]:
    risks: list[str] = []
    if sensitive_count:
        risks.append("sensitive_data_reach")
    if infrastructure_count:
        risks.append("production_infrastructure_reach")
    if decision_counts["block"]:
        risks.append("blocked_action_history")
    if decision_counts["require_approval"]:
        risks.append("approval_gated_actions")
    if repository_count > 1:
        risks.append("multi_repository_scope")
    if "mcp_tools" in control_surfaces:
        risks.append("tooling_surface_reach")
    if "source_control" in control_surfaces:
        risks.append("source_control_scope")
    return risks or ["local_policy_scope"]


def _agent_blast_recommended_controls(
    *,
    control_surfaces: list[str],
    decision_counts: Counter[str],
    approval_paths: list[str],
    repository_count: int,
) -> list[str]:
    controls = ["capture_signed_evidence", "review_agent_scope"]
    if decision_counts["block"]:
        controls.append("keep_block_enforcement_enabled")
    if decision_counts["require_approval"] or not approval_paths:
        controls.append("bind_explicit_approval_route")
    if "sensitive_data" in control_surfaces:
        controls.append("redact_sensitive_targets")
    if "infrastructure_iac" in control_surfaces:
        controls.append("require_blast_radius_context")
    if "mcp_tools" in control_surfaces:
        controls.append("verify_tool_trust_tier")
    if repository_count > 1:
        controls.append("limit_repository_scope")
    return list(dict.fromkeys(controls))


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
    surfaces = _control_surface_catalog()
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


def _control_surface_catalog() -> dict[str, dict[str, str]]:
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
    return surfaces


def _control_coverage_heatmap(
    decisions: list[dict[str, Any]],
    sessions: list[dict[str, Any]],
) -> dict[str, Any]:
    surfaces = _control_surface_catalog()
    row_keys = {
        (
            str(item.get("agent_id", "unknown-agent")),
            str(item.get("repository", "local")),
        )
        for item in [*decisions, *sessions]
        if item.get("agent_id") not in {None, ""}
    }
    if not row_keys and decisions:
        row_keys = {
            (
                str(item.get("agent_id", "unknown-agent")),
                str(item.get("repository", "local")),
            )
            for item in decisions
        }

    rows: list[dict[str, Any]] = []
    scored_cells: list[dict[str, Any]] = []
    for agent_id, repository in sorted(row_keys):
        row_decisions = [
            item
            for item in decisions
            if str(item.get("agent_id", "unknown-agent")) == agent_id
            and str(item.get("repository", "local")) == repository
        ]
        policy_packs = sorted({str(item.get("policy_pack", "cavra-ai-agent-baseline")) for item in row_decisions})
        cells = []
        for surface_id, surface in surfaces.items():
            cell_decisions = [item for item in row_decisions if _control_surface(item) == surface_id]
            decision_counts = Counter(str(item.get("decision", "unknown")) for item in cell_decisions)
            status = _coverage_status(decision_counts, bool(cell_decisions))
            evidence_refs = list(dict.fromkeys(ref for item in cell_decisions for ref in item.get("evidence_refs", [])))[:6]
            cell = {
                "surface_id": surface_id,
                "label": surface["label"],
                "coverage_status": status,
                "coverage_score": _coverage_heat_score(status),
                "decision_count": len(cell_decisions),
                "blocked_actions": decision_counts["block"],
                "approval_required_actions": decision_counts["require_approval"],
                "warned_actions": decision_counts["warn"],
                "evidence_confidence": _evidence_confidence(cell_decisions),
                "evidence_refs": evidence_refs,
                "recommended_action": _coverage_heatmap_recommendation(surface_id, status),
            }
            cells.append(cell)
            scored_cells.append({**cell, "agent_id": agent_id, "repository": repository})
        rows.append(
            {
                "row_id": f"coverage-{_slug(agent_id)}-{_slug(repository)}",
                "agent_id": agent_id,
                "repository": repository,
                "policy_packs": policy_packs,
                "decision_count": len(row_decisions),
                "cells": cells,
            }
        )

    coverage_score = int(round(sum(cell["coverage_score"] for cell in scored_cells) / len(scored_cells))) if scored_cells else 0
    top_gaps = [
        {
            "gap_id": f"coverage-gap-{_slug(cell['agent_id'])}-{_slug(cell['repository'])}-{cell['surface_id']}",
            "agent_id": cell["agent_id"],
            "repository": cell["repository"],
            "surface_id": cell["surface_id"],
            "label": cell["label"],
            "coverage_status": cell["coverage_status"],
            "recommended_action": cell["recommended_action"],
            "evidence_confidence": cell["evidence_confidence"],
        }
        for cell in scored_cells
        if cell["coverage_status"] in {"not_observed_locally", "warning_only"}
    ][:8]
    return {
        "surfaces": [
            {"surface_id": surface_id, "label": surface["label"], "description": surface["description"]}
            for surface_id, surface in surfaces.items()
        ],
        "rows": rows,
        "top_gaps": top_gaps,
        "coverage_score": coverage_score,
    }


def _evidence_confidence_drilldown(
    decisions: list[dict[str, Any]],
    sessions: list[dict[str, Any]],
) -> dict[str, Any]:
    facts: list[dict[str, Any]] = []

    for decision in decisions:
        refs = _evidence_refs(decision)
        level = _evidence_confidence_level(refs, has_metadata=True)
        facts.append(
            {
                "fact_id": f"evidence-{decision.get('decision_id', 'unknown')}",
                "fact_type": "policy_decision",
                "source_id": str(decision.get("decision_id", "unknown")),
                "session_id": decision.get("session_id"),
                "agent_id": decision.get("agent_id", "unknown-agent"),
                "repository": decision.get("repository", "local"),
                "policy_pack": decision.get("policy_pack", "cavra-ai-agent-baseline"),
                "control_surface": _control_surface(decision),
                "decision": decision.get("decision", "unknown"),
                "severity": decision.get("severity", "low"),
                "confidence_level": level,
                "confidence_score": _evidence_confidence_score(level),
                "evidence_count": len(refs),
                "signed_evidence_count": len([ref for ref in refs if _is_signed_evidence_ref(ref)]),
                "evidence_refs": refs[:8],
                "metadata_fields": _present_metadata_fields(
                    decision,
                    [
                        "decision_id",
                        "session_id",
                        "agent_id",
                        "repository",
                        "policy_pack",
                        "rule_id",
                        "action_type",
                        "target",
                        "timestamp",
                    ],
                ),
                "recommended_action": _evidence_confidence_recommendation(level),
                "timestamp": decision.get("timestamp"),
            }
        )

    decision_session_ids = {str(item.get("session_id")) for item in decisions if item.get("session_id")}
    for session in sessions:
        session_id = str(session.get("session_id", "unknown"))
        if session_id in decision_session_ids:
            continue
        refs = _evidence_refs(session)
        level = _evidence_confidence_level(refs, has_metadata=True)
        facts.append(
            {
                "fact_id": f"evidence-session-{session_id}",
                "fact_type": "agent_session",
                "source_id": session_id,
                "session_id": session_id,
                "agent_id": session.get("agent_id", "unknown-agent"),
                "repository": session.get("repository", "local"),
                "policy_pack": session.get("policy_pack", "cavra-ai-agent-baseline"),
                "control_surface": "agent_session",
                "decision": "session_observed",
                "severity": "low",
                "confidence_level": level,
                "confidence_score": _evidence_confidence_score(level),
                "evidence_count": len(refs),
                "signed_evidence_count": len([ref for ref in refs if _is_signed_evidence_ref(ref)]),
                "evidence_refs": refs[:8],
                "metadata_fields": _present_metadata_fields(
                    session,
                    [
                        "session_id",
                        "agent_id",
                        "repository",
                        "policy_pack",
                        "state",
                        "started_at",
                        "updated_at",
                    ],
                ),
                "recommended_action": _evidence_confidence_recommendation(level),
                "timestamp": session.get("updated_at") or session.get("started_at"),
            }
        )

    counts = Counter(str(item["confidence_level"]) for item in facts)
    score = int(round(sum(int(item["confidence_score"]) for item in facts) / len(facts))) if facts else 0
    facts = sorted(
        facts,
        key=lambda item: (int(item["confidence_score"]), str(item.get("timestamp", ""))),
    )
    return {
        "summary": {
            "total_facts": len(facts),
            "signed_evidence_items": counts["signed_evidence"],
            "activity_evidence_items": counts["activity_evidence_refs"],
            "sample_evidence_items": counts["sample_evidence_refs"],
            "metadata_only_items": counts["activity_metadata_only"],
            "missing_evidence_items": counts["missing_evidence"],
            "evidence_score": score,
            "lowest_confidence_level": facts[0]["confidence_level"] if facts else "no_local_activity",
            "highest_confidence_level": max(
                (str(item["confidence_level"]) for item in facts),
                key=lambda level: _evidence_confidence_score(level),
                default="no_local_activity",
            ),
        },
        "facts": facts[:50],
    }


def _evidence_freshness_slo(
    decisions: list[dict[str, Any]],
    sessions: list[dict[str, Any]],
    *,
    generated_at: str,
) -> dict[str, Any]:
    now = _parse_timestamp(generated_at)
    items: list[dict[str, Any]] = []

    for decision in decisions:
        refs = _evidence_refs(decision)
        observed_at = str(decision.get("timestamp") or "")
        freshness = _freshness_status(observed_at, now)
        retention = _retention_status(refs)
        items.append(
            {
                "item_id": f"freshness-{decision.get('decision_id', 'unknown')}",
                "item_type": "policy_decision",
                "source_id": str(decision.get("decision_id", "unknown")),
                "session_id": decision.get("session_id"),
                "agent_id": decision.get("agent_id", "unknown-agent"),
                "repository": decision.get("repository", "local"),
                "policy_pack": decision.get("policy_pack", "cavra-ai-agent-baseline"),
                "control_surface": _control_surface(decision),
                "severity": decision.get("severity", "low"),
                "decision": decision.get("decision", "unknown"),
                "observed_at": observed_at or None,
                "age_hours": _age_hours(observed_at, now),
                "freshness_status": freshness,
                "retention_status": retention,
                "slo_status": _evidence_slo_status(freshness, retention),
                "evidence_refs": refs[:8],
                "recommended_action": _evidence_freshness_recommendation(freshness, retention),
            }
        )

    decision_session_ids = {str(item.get("session_id")) for item in decisions if item.get("session_id")}
    for session in sessions:
        session_id = str(session.get("session_id", "unknown"))
        if session_id in decision_session_ids:
            continue
        refs = _evidence_refs(session)
        observed_at = str(session.get("updated_at") or session.get("started_at") or "")
        freshness = _freshness_status(observed_at, now)
        retention = _retention_status(refs)
        items.append(
            {
                "item_id": f"freshness-session-{session_id}",
                "item_type": "agent_session",
                "source_id": session_id,
                "session_id": session_id,
                "agent_id": session.get("agent_id", "unknown-agent"),
                "repository": session.get("repository", "local"),
                "policy_pack": session.get("policy_pack", "cavra-ai-agent-baseline"),
                "control_surface": "agent_session",
                "severity": "low",
                "decision": "session_observed",
                "observed_at": observed_at or None,
                "age_hours": _age_hours(observed_at, now),
                "freshness_status": freshness,
                "retention_status": retention,
                "slo_status": _evidence_slo_status(freshness, retention),
                "evidence_refs": refs[:8],
                "recommended_action": _evidence_freshness_recommendation(freshness, retention),
            }
        )

    freshness_counts = Counter(str(item["freshness_status"]) for item in items)
    retention_counts = Counter(str(item["retention_status"]) for item in items)
    slo_counts = Counter(str(item["slo_status"]) for item in items)
    ages = [int(item["age_hours"]) for item in items if item.get("age_hours") is not None]
    freshness_score = _slo_score([_freshness_score(str(item["freshness_status"])) for item in items])
    retention_score = _slo_score([_retention_score(str(item["retention_status"])) for item in items])
    items = sorted(
        items,
        key=lambda item: (
            _slo_sort_order(str(item["slo_status"])),
            -1 if item.get("age_hours") is None else int(item["age_hours"]),
        ),
        reverse=True,
    )
    return {
        "slo_policy": {
            "fresh_hours": 24,
            "review_soon_hours": 168,
            "retention_reference_patterns": ["archive://", "immutable://", "s3://", "gs://", "azblob://"],
            "community_boundary": "metadata_only",
        },
        "summary": {
            "total_items": len(items),
            "fresh_items": freshness_counts["fresh"],
            "review_soon_items": freshness_counts["review_soon"],
            "stale_items": freshness_counts["stale"],
            "missing_timestamp_items": freshness_counts["timestamp_missing"],
            "retention_ready_items": retention_counts["retained_reference"],
            "sample_retention_items": retention_counts["sample_reference"],
            "retention_gap_items": retention_counts["evidence_ref_only"]
            + retention_counts["metadata_only"]
            + retention_counts["retention_missing"],
            "slo_met_items": slo_counts["met"],
            "slo_monitor_items": slo_counts["monitor"],
            "slo_breached_items": slo_counts["breached"],
            "freshness_score": freshness_score,
            "retention_score": retention_score,
            "oldest_age_hours": max(ages) if ages else None,
            "evidence_confidence": _evidence_confidence(decisions),
        },
        "items": items[:50],
    }


def _executive_risk_narrative(
    decisions: list[dict[str, Any]],
    sessions: list[dict[str, Any]],
    findings: list[dict[str, Any]],
    overview: dict[str, Any],
    evidence_freshness_slo: dict[str, Any],
) -> dict[str, Any]:
    blocked = int(overview.get("blocked_actions", 0))
    approvals = int(overview.get("approval_required_actions", 0))
    total_decisions = int(overview.get("total_decisions", len(decisions)))
    posture_score = int(overview.get("posture_score", 0))
    risk_level = str(overview.get("risk_level", "unknown"))
    freshness_summary = evidence_freshness_slo.get("summary", {})
    breached = int(freshness_summary.get("slo_breached_items", 0) or 0)
    monitor = int(freshness_summary.get("slo_monitor_items", 0) or 0)
    retention_gaps = int(freshness_summary.get("retention_gap_items", 0) or 0)
    top_risks = _executive_top_risks(findings, decisions, evidence_freshness_slo)
    recommended_actions = _executive_recommended_actions(risk_level, approvals, breached, retention_gaps, top_risks)
    headline = _executive_headline(risk_level, blocked, approvals, total_decisions, breached)
    sections = [
        {
            "section_id": "executive-summary",
            "title": "Executive Summary",
            "body": headline,
        },
        {
            "section_id": "risk-posture",
            "title": "Risk Posture",
            "body": (
                f"CAVRA observed {total_decisions} local policy decisions across "
                f"{len({str(item.get('agent_id', 'unknown-agent')) for item in decisions if item.get('agent_id')})} agent identities. "
                f"The current Community posture score is {posture_score}/100 with a {risk_level} risk level."
            ),
        },
        {
            "section_id": "evidence-readiness",
            "title": "Evidence Readiness",
            "body": (
                f"Evidence freshness has {breached} breached SLO item(s), {monitor} item(s) to monitor, "
                f"and {retention_gaps} retention gap(s). Community validates local timestamps and reference patterns only."
            ),
        },
        {
            "section_id": "operator-focus",
            "title": "Operator Focus",
            "body": "Focus on the highest-risk agent actions, close evidence gaps, and keep Enterprise-only live controls scoped for the next paid or trial deployment.",
        },
    ]
    return {
        "report_id": "aispm-executive-risk-narrative-community",
        "narrative_type": "deterministic_public_safe_summary",
        "audience": ["CSO", "CISO", "security leadership", "platform leadership"],
        "time_window": "local_activity_window",
        "headline": headline,
        "risk_level": risk_level,
        "posture_score": posture_score,
        "key_metrics": {
            "total_sessions": overview.get("total_sessions", len(sessions)),
            "total_decisions": total_decisions,
            "blocked_actions": blocked,
            "approval_required_actions": approvals,
            "risk_findings": overview.get("risk_findings", len(findings)),
            "evidence_slo_breaches": breached,
            "evidence_retention_gaps": retention_gaps,
            "freshness_score": freshness_summary.get("freshness_score", 0),
            "retention_score": freshness_summary.get("retention_score", 0),
        },
        "sections": sections,
        "top_risks": top_risks,
        "recommended_actions": recommended_actions,
        "evidence_refs": list(
            dict.fromkeys(ref for item in decisions for ref in _evidence_refs(item))
        )[:10],
        "limitations": [
            "Community narrative is deterministic and based on local/sample metadata only.",
            "Raw prompts, model reasoning, customer impact, trend history, and tenant benchmarks require CAVRA Enterprise.",
        ],
    }


def _executive_headline(risk_level: str, blocked: int, approvals: int, total_decisions: int, breached: int) -> str:
    if total_decisions == 0:
        return "No local AI-agent policy activity is available yet; connect activity data before relying on posture conclusions."
    control_phrase = f"{blocked} blocked action(s) and {approvals} approval-gated action(s)"
    evidence_phrase = f"{breached} evidence SLO breach(es)"
    return (
        f"CAVRA Community reports {risk_level} AI-agent posture from {total_decisions} local decision(s), "
        f"including {control_phrase}, with {evidence_phrase} requiring operator review."
    )


def _executive_top_risks(
    findings: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    evidence_freshness_slo: dict[str, Any],
) -> list[dict[str, Any]]:
    risks = [
        {
            "risk_id": str(item.get("finding_id", f"finding-{index + 1}")),
            "title": str(item.get("risk_classification", "policy_risk")).replace("_", " ").title(),
            "severity": str(item.get("severity", "low")),
            "agent_id": item.get("agent_id", "unknown-agent"),
            "repository": item.get("repository", "local"),
            "reason": item.get("reason", "Policy finding requires leadership review."),
            "evidence_refs": _evidence_refs(item),
        }
        for index, item in enumerate(findings[:5])
    ]
    breached_items = [
        item
        for item in evidence_freshness_slo.get("items", [])
        if item.get("slo_status") == "breached"
    ][:3]
    risks.extend(
        {
            "risk_id": f"evidence-slo-{item.get('source_id', index)}",
            "title": "Evidence SLO Breach",
            "severity": "medium",
            "agent_id": item.get("agent_id", "unknown-agent"),
            "repository": item.get("repository", "local"),
            "reason": item.get("recommended_action", "Evidence freshness or retention requires review."),
            "evidence_refs": _evidence_refs(item),
        }
        for index, item in enumerate(breached_items)
    )
    if not risks and decisions:
        risks.append(
            {
                "risk_id": "community-observed-activity",
                "title": "Observed AI-Agent Activity",
                "severity": "low",
                "agent_id": decisions[0].get("agent_id", "unknown-agent"),
                "repository": decisions[0].get("repository", "local"),
                "reason": "Local activity exists; continue collecting evidence and validating policy coverage.",
                "evidence_refs": _evidence_refs(decisions[0]),
            }
        )
    return risks[:6]


def _executive_recommended_actions(
    risk_level: str,
    approvals: int,
    breached: int,
    retention_gaps: int,
    top_risks: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    actions = []
    if risk_level in {"critical", "high"} or top_risks:
        actions.append(
            {
                "action_id": "review-top-ai-agent-risks",
                "priority": "high",
                "owner": "security leadership",
                "action": "Review the top AI-agent risks and confirm owners for remediation.",
            }
        )
    if approvals:
        actions.append(
            {
                "action_id": "validate-approval-latency",
                "priority": "medium",
                "owner": "platform leadership",
                "action": "Validate approval routes and latency for approval-gated AI-agent actions.",
            }
        )
    if breached or retention_gaps:
        actions.append(
            {
                "action_id": "close-evidence-slo-gaps",
                "priority": "high",
                "owner": "governance and audit",
                "action": "Refresh stale evidence and move retained evidence references into immutable storage.",
            }
        )
    actions.append(
        {
            "action_id": "plan-enterprise-live-posture",
            "priority": "medium",
            "owner": "security architecture",
            "action": "Plan Enterprise live ingestion for prompts, tool calls, trace history, trend reporting, and runtime controls.",
        }
    )
    return actions


def _replay_to_policy_draft(
    decisions: list[dict[str, Any]],
    *,
    sessions: list[dict[str, Any]],
    source_scope: str,
) -> dict[str, Any]:
    authorable = _policy_authoring_decisions(decisions)
    recommendations = _policy_rule_recommendations(authorable)
    draft_payload = _policy_draft_payload_from_recommendations(recommendations, source_scope)
    draft = build_policy_pack_draft(draft_payload)
    source_session_ids = sorted({str(item.get("session_id")) for item in [*decisions, *sessions] if item.get("session_id")})
    source_repositories = sorted({str(item.get("repository")) for item in [*decisions, *sessions] if item.get("repository")})
    return {
        "summary": {
            "source_scope": source_scope,
            "source_decisions": len(decisions),
            "authorable_decisions": len(authorable),
            "recommended_rules": len(recommendations),
            "draft_valid": draft["valid"],
            "source_sessions": source_session_ids[:8],
            "source_repositories": source_repositories[:8],
            "rule_counts": draft["summary"]["rule_counts"],
        },
        "recommendations": recommendations,
        "policy_draft": draft,
        "write_back": {
            "status": "read_only_preview",
            "next_step": "Review the draft, then use /policy-packs/publish-plan and the approval-bound publish flow.",
            "approval_required": True,
        },
        "operator_notes": [
            "Replay-to-policy authoring is read-only in Community and does not write to policies/.",
            "Recommendations use normalized decision metadata only; review every generated rule before publishing.",
            "Use signed PR review and approval-bound policy publishing before enforcement rollout.",
        ],
    }


def _policy_authoring_decisions(decisions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    authorable = [
        item
        for item in decisions
        if str(item.get("decision", "")) in {"block", "require_approval", "warn"}
        or str(item.get("severity", "")) in {"critical", "high"}
    ]
    return sorted(authorable, key=lambda item: str(item.get("timestamp", "")))


def _policy_rule_recommendations(decisions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    recommendations = []
    seen = set()
    for index, decision in enumerate(decisions, start=1):
        recommendation = _policy_rule_recommendation(index, decision)
        key = (
            recommendation["policy_section"],
            recommendation["rule_key"],
            str(recommendation["proposed_value"]),
        )
        if key in seen:
            continue
        seen.add(key)
        recommendations.append(recommendation)
    return recommendations


def _policy_rule_recommendation(index: int, decision: dict[str, Any]) -> dict[str, Any]:
    surface = _control_surface(decision)
    outcome = str(decision.get("decision", "review"))
    action_type = str(decision.get("action_type", "unknown"))
    target_summary, target_redacted = _safe_target_summary(decision)
    section, rule_key, proposed_value = _policy_rule_target(decision, surface, outcome)
    return {
        "recommendation_id": f"policy-rec-{index}-{_slug(str(decision.get('decision_id', 'decision')))}",
        "decision_id": decision.get("decision_id"),
        "session_id": decision.get("session_id"),
        "agent_id": decision.get("agent_id", "unknown-agent"),
        "repository": decision.get("repository", "local"),
        "policy_pack": decision.get("policy_pack", "cavra-ai-agent-baseline"),
        "control_surface": surface,
        "risk_classification": _risk_classification(decision),
        "severity": decision.get("severity", "low"),
        "decision": outcome,
        "action_type": action_type,
        "target_summary": target_summary,
        "target_redacted": target_redacted,
        "policy_section": section,
        "rule_key": rule_key,
        "proposed_value": proposed_value,
        "rationale": decision.get("reason") or "Observed CAVRA decision should be converted into an explicit reviewed policy rule.",
        "confidence": "metadata_derived",
        "evidence_refs": _evidence_refs(decision),
    }


def _policy_rule_target(decision: dict[str, Any], surface: str, outcome: str) -> tuple[str, str, Any]:
    action_type = str(decision.get("action_type", "")).lower()
    target = _policy_target_pattern(decision, surface)
    if surface == "sensitive_data":
        if "write" in action_type:
            return ("filesystem", "block_write" if outcome == "block" else "require_approval_write", target)
        return ("filesystem", "block_read", target)
    if surface == "infrastructure_iac":
        return ("commands", "block" if outcome == "block" else "require_approval", target)
    if surface == "runtime_commands":
        return ("commands", "block" if outcome == "block" else "require_approval", target)
    if surface == "source_control":
        if outcome == "block":
            return ("git", "block_direct_push_to_protected_branch", True)
        return ("git", "require_pull_request", True)
    if surface == "mcp_tools":
        return ("mcp", "block_unknown_servers" if outcome == "block" else "allowlist_enabled", True)
    return ("commands", "block" if outcome == "block" else "require_approval", target)


def _policy_target_pattern(decision: dict[str, Any], surface: str) -> str:
    raw_target = str(decision.get("target") or decision.get("requested_operation") or "").strip()
    lowered = raw_target.lower()
    if surface == "sensitive_data":
        if ".env" in lowered:
            return ".env*"
        if "token" in lowered:
            return "**/*token*"
        if "credential" in lowered:
            return "**/*credential*"
        return "**/*secret*"
    if surface == "infrastructure_iac":
        if "terraform apply" in lowered:
            return "terraform apply*"
        if "tofu apply" in lowered:
            return "tofu apply*"
        if "kubectl" in lowered:
            return "kubectl *"
    if surface == "source_control":
        return "protected_branch_change"
    if surface == "mcp_tools":
        return "untrusted_mcp_tool"
    if not raw_target or raw_target == "target not recorded":
        return "review-risky-agent-action*"
    if len(raw_target) > 80:
        return f"{raw_target[:77]}*"
    return f"{raw_target.rstrip('*')}*" if " " in raw_target and not raw_target.endswith("*") else raw_target


def _policy_draft_payload_from_recommendations(
    recommendations: list[dict[str, Any]],
    source_scope: str,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "id": f"cavra-replay-derived-{_slug(source_scope)}",
        "title": "Replay-Derived AI Agent Controls",
        "description": "Read-only Community draft generated from normalized AISPM replay decisions.",
        "version": datetime.now(timezone.utc).strftime("%Y.%m.%d"),
        "inherits": "cavra-ai-agent-baseline",
        "mode": "enforce",
        "approvals": {
            "replay_to_policy_authoring": {
                "approvers": ["Platform Security"],
                "source": "aispm_replay_to_policy",
            }
        },
        "evidence": {
            "require_pr_attestation": True,
            "require_replay_evidence": True,
            "source": "aispm_replay_to_policy",
        },
        "compliance": {
            "maps_to": ["SOC 2 Change Management", "NIST SSDF RV.1.3", "Internal AI Governance"],
        },
    }
    for recommendation in recommendations:
        section = str(recommendation["policy_section"])
        rule_key = str(recommendation["rule_key"])
        proposed_value = recommendation["proposed_value"]
        section_payload = payload.setdefault(section, {})
        if isinstance(proposed_value, bool):
            section_payload[rule_key] = proposed_value
            continue
        values = section_payload.setdefault(rule_key, [])
        if proposed_value not in values:
            values.append(proposed_value)
    return payload


def _replay_to_policy_test_fixture(
    recommendations: list[dict[str, Any]],
    policy_pack: dict[str, Any],
    *,
    source_scope: str,
) -> dict[str, Any]:
    policy_id = str(policy_pack.get("metadata", {}).get("id") or f"cavra-replay-derived-{_slug(source_scope)}")
    cases = [_replay_to_policy_test_case(index, item, policy_id) for index, item in enumerate(recommendations, start=1)]
    return {
        "schema_version": "cavra.policy_tests.replay_to_policy.v1",
        "policy_id": policy_id,
        "source_scope": source_scope,
        "case_count": len(cases),
        "cases": cases,
        "validation": {
            "community_mode": "review_only",
            "recommended_commands": [
                f"cavra policy validate policies/{policy_id}/policy.yaml",
                "cavra policy test",
            ],
            "notes": [
                "Generated cases are public-safe assertions derived from normalized CAVRA decisions.",
                "Review generated cases before committing them to repository CI.",
                "Private prompt, reasoning, ticket, and tenant-history simulation requires CAVRA Enterprise.",
            ],
        },
    }


def _replay_to_policy_test_case(index: int, recommendation: dict[str, Any], policy_id: str) -> dict[str, Any]:
    proposed_value = recommendation.get("proposed_value")
    target = proposed_value if isinstance(proposed_value, str) else recommendation.get("target_summary", "policy target")
    return {
        "case_id": f"replay-policy-test-{index}-{_slug(str(recommendation.get('decision_id') or recommendation.get('recommendation_id') or 'case'))}",
        "recommendation_id": recommendation.get("recommendation_id"),
        "decision_id": recommendation.get("decision_id"),
        "description": f"Assert {recommendation.get('policy_section', 'policy')}.{recommendation.get('rule_key', 'rule')} for {recommendation.get('control_surface', 'general_policy')}.",
        "input": {
            "action_type": recommendation.get("action_type", "unknown"),
            "target": target,
            "target_summary": recommendation.get("target_summary", "target not recorded"),
            "target_redacted": recommendation.get("target_redacted", False),
            "agent_id": recommendation.get("agent_id", "unknown-agent"),
            "repository": recommendation.get("repository", "local"),
            "policy_pack": policy_id,
        },
        "expected": {
            "decision": recommendation.get("decision", "review"),
            "severity": recommendation.get("severity", "low"),
            "policy_section": recommendation.get("policy_section", "policy"),
            "rule_key": recommendation.get("rule_key", "rule"),
            "proposed_value": proposed_value,
            "risk_classification": recommendation.get("risk_classification", "policy_decision_review"),
        },
        "assertion_type": "metadata_derived_policy_expectation",
        "public_safe": True,
        "evidence_refs": recommendation.get("evidence_refs", []),
    }


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


def _coverage_heat_score(status: str) -> int:
    return {
        "enforced": 100,
        "approval_gated": 82,
        "attested": 72,
        "observed": 58,
        "warning_only": 38,
        "not_observed_locally": 0,
    }.get(status, 0)


def _coverage_heatmap_recommendation(surface_id: str, status: str) -> str:
    surface = surface_id.replace("_", " ")
    if status == "not_observed_locally":
        return f"Add CAVRA policy coverage or test evidence for {surface} before relying on this agent/repository path."
    if status == "warning_only":
        return f"Move {surface} from warning-only visibility to block, approval, or attestation controls where risk justifies it."
    if status == "observed":
        return f"Confirm {surface} has explicit enforcement, approval, or attestation intent for this agent/repository path."
    if status == "attested":
        return f"Keep signed evidence for {surface} and review whether higher-risk actions need approval gates."
    if status == "approval_gated":
        return f"Validate approval routing and evidence freshness for {surface}."
    if status == "enforced":
        return f"Keep block enforcement and evidence capture active for {surface}."
    return f"Review {surface} coverage."


def _slug(value: str) -> str:
    normalized = "".join(char.lower() if char.isalnum() else "-" for char in value)
    return "-".join(part for part in normalized.split("-") if part)[:80] or "local"


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


def _evidence_refs(item: dict[str, Any]) -> list[str]:
    refs = item.get("evidence_refs", [])
    if not isinstance(refs, list):
        refs = [refs]
    return list(dict.fromkeys(str(ref) for ref in refs if ref not in {None, ""}))


def _is_signed_evidence_ref(ref: str) -> bool:
    normalized = ref.lower()
    return (
        normalized.startswith("signed://")
        or "signature" in normalized
        or "sigstore" in normalized
        or normalized.endswith(".sig")
    )


def _evidence_confidence_level(refs: list[str], *, has_metadata: bool) -> str:
    if any(_is_signed_evidence_ref(ref) for ref in refs):
        return "signed_evidence"
    if any(ref.startswith("sample://") for ref in refs):
        return "sample_evidence_refs"
    if refs:
        return "activity_evidence_refs"
    if has_metadata:
        return "activity_metadata_only"
    return "missing_evidence"


def _evidence_confidence_score(level: str) -> int:
    return {
        "signed_evidence": 100,
        "activity_evidence_refs": 74,
        "sample_evidence_refs": 45,
        "activity_metadata_only": 28,
        "missing_evidence": 0,
        "no_local_activity": 0,
    }.get(level, 0)


def _present_metadata_fields(item: dict[str, Any], fields: list[str]) -> list[str]:
    present = []
    for field in fields:
        value = item.get(field)
        if value is None or value == "" or value == []:
            continue
        present.append(field)
    return present


def _evidence_confidence_recommendation(level: str) -> str:
    if level == "signed_evidence":
        return "Keep signed evidence attached and validate freshness during release review."
    if level == "activity_evidence_refs":
        return "Promote evidence references to signed attestations for regulated workflows."
    if level == "sample_evidence_refs":
        return "Replace sample evidence with local or signed evidence before production evaluation."
    if level == "activity_metadata_only":
        return "Attach evidence references for this decision or session before audit reliance."
    return "Capture decision metadata and evidence references before relying on this control."


def _parse_timestamp(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _age_hours(observed_at: str, now: datetime | None) -> int | None:
    observed = _parse_timestamp(observed_at)
    if observed is None or now is None:
        return None
    return max(0, int(round((now - observed).total_seconds() / 3600)))


def _freshness_status(observed_at: str, now: datetime | None) -> str:
    age = _age_hours(observed_at, now)
    if age is None:
        return "timestamp_missing"
    if age <= 24:
        return "fresh"
    if age <= 168:
        return "review_soon"
    return "stale"


def _retention_status(refs: list[str]) -> str:
    if any(ref.startswith(("archive://", "immutable://", "s3://", "gs://", "azblob://")) for ref in refs):
        return "retained_reference"
    if any(ref.startswith("sample://") for ref in refs):
        return "sample_reference"
    if refs:
        return "evidence_ref_only"
    return "metadata_only"


def _evidence_slo_status(freshness: str, retention: str) -> str:
    if freshness in {"stale", "timestamp_missing"} or retention in {"metadata_only", "retention_missing"}:
        return "breached"
    if freshness == "review_soon" or retention in {"sample_reference", "evidence_ref_only"}:
        return "monitor"
    return "met"


def _freshness_score(status: str) -> int:
    return {
        "fresh": 100,
        "review_soon": 68,
        "stale": 18,
        "timestamp_missing": 0,
    }.get(status, 0)


def _retention_score(status: str) -> int:
    return {
        "retained_reference": 100,
        "sample_reference": 45,
        "evidence_ref_only": 38,
        "metadata_only": 0,
        "retention_missing": 0,
    }.get(status, 0)


def _slo_score(scores: list[int]) -> int:
    return int(round(sum(scores) / len(scores))) if scores else 0


def _slo_sort_order(status: str) -> int:
    return {"met": 0, "monitor": 1, "breached": 2}.get(status, 0)


def _evidence_freshness_recommendation(freshness: str, retention: str) -> str:
    if freshness == "timestamp_missing":
        return "Record decision/session timestamps before using this evidence for audit review."
    if freshness == "stale":
        return "Refresh or revalidate this evidence before relying on it for release or compliance review."
    if retention == "metadata_only":
        return "Attach evidence references and route the record to retained evidence storage."
    if retention == "evidence_ref_only":
        return "Promote this evidence reference into immutable retained storage for regulated workflows."
    if retention == "sample_reference":
        return "Replace sample evidence with retained local or signed evidence before production reliance."
    if freshness == "review_soon":
        return "Review freshness before the evidence crosses the seven-day SLO threshold."
    return "Freshness and retention metadata are acceptable for Community-level review."
