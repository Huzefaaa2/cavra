from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from cavra.activity import ActivityStore, SQLiteActivityStore
from cavra.approvals import (
    ApprovalStore,
    SQLiteApprovalStore,
    actor_context_from_claims,
    actor_context_from_oidc_token,
    attach_approval_to_decision,
    deliver_provider_requests,
    load_oidc_config,
    load_provider_config,
    load_rbac_rules,
    load_routing_rules,
)
from cavra.evidence import EvidenceMetadataStore, SQLiteEvidenceMetadataStore
from cavra.integrations import IntegrationStore, SQLiteIntegrationStore
from cavra.inventory import InventoryStore, SQLiteInventoryStore
from cavra.operations import build_persistent_api_retention_plan, persistent_api_store_status
from cavra.policy_registry import PolicyRegistry, PolicyRegistryError
from cavra.registry import (
    RegistryStore,
    SQLiteRegistryStore,
    classify_mcp_capability,
    default_agent_profiles,
    default_mcp_tool_classifications,
)
from cavra.runtime import RuntimeGuard
from cavra.sandbox import compliance_mapping, create_sandbox_run, evidence_json, pr_attestation

try:
    from fastapi import FastAPI, HTTPException, Response
    from fastapi.middleware.cors import CORSMiddleware
except ImportError:  # pragma: no cover
    FastAPI = None
    HTTPException = None
    Response = None
    CORSMiddleware = None


def create_app():
    if FastAPI is None:
        raise RuntimeError("Install fastapi and uvicorn to run the CAVRA API.")
    app = FastAPI(
        title="CAVRA API",
        description="Controlled Agentic Verification & Runtime Authority API for AI-agent runtime governance.",
        version="0.1.0",
    )
    cors_origins = _csv_env("CAVRA_CORS_ORIGINS")
    if cors_origins and CORSMiddleware is not None:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=cors_origins,
            allow_credentials=False,
            allow_methods=["GET", "POST", "OPTIONS"],
            allow_headers=["*"],
        )
    runs: dict[str, dict] = {}
    evidence_store = (
        SQLiteEvidenceMetadataStore(Path(os.environ["CAVRA_EVIDENCE_METADATA_DB"]))
        if os.environ.get("CAVRA_EVIDENCE_METADATA_DB")
        else EvidenceMetadataStore(Path(os.environ.get("CAVRA_EVIDENCE_METADATA_STORE", ".cavra/api/evidence-metadata.json")))
    )
    approval_store = (
        SQLiteApprovalStore(Path(os.environ["CAVRA_APPROVAL_DB"]))
        if os.environ.get("CAVRA_APPROVAL_DB")
        else ApprovalStore(Path(os.environ.get("CAVRA_APPROVAL_STORE", ".cavra/api/approvals.json")))
    )
    routing_rules = load_routing_rules(Path(os.environ["CAVRA_APPROVAL_ROUTING_FILE"])) if os.environ.get("CAVRA_APPROVAL_ROUTING_FILE") else None
    provider_config = load_provider_config(Path(os.environ["CAVRA_APPROVAL_PROVIDER_CONFIG"])) if os.environ.get("CAVRA_APPROVAL_PROVIDER_CONFIG") else None
    rbac_rules = load_rbac_rules(Path(os.environ["CAVRA_APPROVAL_RBAC_FILE"])) if os.environ.get("CAVRA_APPROVAL_RBAC_FILE") else {}
    oidc_config = load_oidc_config(Path(os.environ["CAVRA_APPROVAL_OIDC_CONFIG"])) if os.environ.get("CAVRA_APPROVAL_OIDC_CONFIG") else {}
    registry_store = (
        SQLiteRegistryStore(Path(os.environ["CAVRA_REGISTRY_DB"]))
        if os.environ.get("CAVRA_REGISTRY_DB")
        else RegistryStore(Path(os.environ.get("CAVRA_REGISTRY_STORE", ".cavra/api/registry.json")))
    )
    activity_store = (
        SQLiteActivityStore(Path(os.environ["CAVRA_ACTIVITY_DB"]))
        if os.environ.get("CAVRA_ACTIVITY_DB")
        else ActivityStore(Path(os.environ.get("CAVRA_ACTIVITY_STORE", ".cavra/api/activity.json")))
    )
    inventory_store = (
        SQLiteInventoryStore(Path(os.environ["CAVRA_INVENTORY_DB"]))
        if os.environ.get("CAVRA_INVENTORY_DB")
        else InventoryStore(Path(os.environ.get("CAVRA_INVENTORY_STORE", ".cavra/api/inventory.json")))
    )
    integration_store = (
        SQLiteIntegrationStore(Path(os.environ["CAVRA_INTEGRATION_DB"]))
        if os.environ.get("CAVRA_INTEGRATION_DB")
        else IntegrationStore(Path(os.environ.get("CAVRA_INTEGRATION_STORE", ".cavra/api/integrations.json")))
    )

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "product": "CAVRA"}

    @app.get("/version")
    def version() -> dict[str, str]:
        return {"version": "0.1.0", "name": "CAVRA Runtime Server"}

    @app.get("/console/config")
    def console_config() -> dict[str, object]:
        metadata_mode = "sqlite" if isinstance(evidence_store, SQLiteEvidenceMetadataStore) else "json"
        approval_mode = "sqlite" if isinstance(approval_store, SQLiteApprovalStore) else "json"
        registry_mode = "sqlite" if isinstance(registry_store, SQLiteRegistryStore) else "json"
        activity_mode = "sqlite" if isinstance(activity_store, SQLiteActivityStore) else "json"
        inventory_mode = "sqlite" if isinstance(inventory_store, SQLiteInventoryStore) else "json"
        integration_mode = "sqlite" if isinstance(integration_store, SQLiteIntegrationStore) else "json"
        return {
            "product": "CAVRA",
            "api_base_url": os.environ.get("CAVRA_PUBLIC_API_BASE_URL", ""),
            "metadata_mode": metadata_mode,
            "approval_mode": approval_mode,
            "registry_mode": registry_mode,
            "activity_mode": activity_mode,
            "inventory_mode": inventory_mode,
            "integration_mode": integration_mode,
            "approval_provider_delivery": "configured" if provider_config is not None else "disabled",
            "approval_oidc": "configured" if oidc_config else "disabled",
            "approval_rbac": "configured" if rbac_rules else "disabled",
            "registry_store": str(registry_store.path),
            "cors_origins": cors_origins,
            "endpoints": {
                "evidence": "/evidence",
                "evidence_item": "/evidence/{session_id}",
                "approvals": "/approvals",
                "sessions": "/sessions",
                "decisions": "/decisions",
                "repositories": "/repositories",
                "policy_rollouts": "/policy-rollouts",
                "policy_rollout_detail": "/policy-rollouts/{rollout_id}/detail",
                "console_security_boundary": "/console/security-boundary",
                "operations_stores": "/operations/stores",
                "operations_retention_plan": "/operations/retention-plan",
                "integrations": "/integrations",
                "agents": "/agents",
                "mcp_servers": "/mcp/servers",
                "mcp_trust": "/mcp/trust",
                "sandbox_run": "/api/sandbox/run",
            },
        }

    @app.get("/policies")
    @app.get("/policy-packs")
    def policies() -> list[dict]:
        return PolicyRegistry().list_policy_packs()

    @app.get("/decisions")
    def decision_index(
        session_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        repository: Optional[str] = None,
        policy_pack: Optional[str] = None,
        decision: Optional[str] = None,
        severity: Optional[str] = None,
        action_type: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict:
        return activity_store.list_decisions(
            session_id=session_id,
            agent_id=agent_id,
            repository=repository,
            policy_pack=policy_pack,
            decision=decision,
            severity=severity,
            action_type=action_type,
            limit=limit,
            offset=offset,
        )

    @app.post("/decisions")
    def decisions(payload: dict) -> dict:
        guard = RuntimeGuard(
            policy_pack=payload.get("policy_pack") or "cavra-ai-agent-baseline",
            session_id=payload.get("session_id", "local"),
            agent_id=payload.get("agent_id", "unknown-agent"),
            actor=payload.get("actor", "ai-agent"),
            registry_store=registry_store,
        )
        action_type = payload.get("action_type")
        target = payload.get("target", "")
        if action_type == "read_file":
            result = guard.evaluate_file_access(Path(target), "read").to_dict()
        elif action_type == "write_file":
            result = guard.evaluate_file_access(Path(target), "write").to_dict()
        elif action_type == "execute_command":
            result = guard.evaluate_command(target).to_dict()
        elif action_type == "git_operation":
            result = guard.evaluate_git_action(payload.get("operation", "push"), target).to_dict()
        else:
            result = guard.evaluate_mcp_tool_call(payload.get("server", "unknown"), payload.get("tool", "unknown"), payload.get("capability")).to_dict()
        if payload.get("repository"):
            result["repository"] = payload["repository"]
        return activity_store.upsert_decision(result)

    @app.get("/decisions/{decision_id}")
    def decision_item(decision_id: str) -> dict:
        item = activity_store.get_decision(decision_id)
        if item is None:
            raise HTTPException(status_code=404, detail="decision not found")
        return item

    @app.get("/sessions")
    def session_index(
        agent_id: Optional[str] = None,
        repository: Optional[str] = None,
        policy_pack: Optional[str] = None,
        state: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict:
        return activity_store.list_sessions(
            agent_id=agent_id,
            repository=repository,
            policy_pack=policy_pack,
            state=state,
            limit=limit,
            offset=offset,
        )

    @app.post("/sessions")
    def upsert_session(payload: dict) -> dict:
        try:
            return activity_store.upsert_session(payload)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail="invalid session record") from exc

    @app.get("/sessions/{session_id}")
    def session_item(session_id: str) -> dict:
        item = activity_store.get_session(session_id)
        if item is None:
            raise HTTPException(status_code=404, detail="session not found")
        return item

    @app.get("/operations/stores")
    def operations_store_index() -> dict:
        return persistent_api_store_status()

    @app.get("/console/security-boundary")
    def console_security_boundary() -> dict[str, object]:
        return _console_security_boundary(
            oidc_configured=bool(oidc_config),
            rbac_configured=bool(rbac_rules),
            cors_origins=cors_origins,
        )

    @app.get("/operations/retention-plan")
    def operations_retention_plan(
        retention_days: int = 2555,
        classification: str = "regulated-sdlc",
        legal_hold: bool = False,
    ) -> dict:
        try:
            return build_persistent_api_retention_plan(
                retention_days=retention_days,
                classification=classification,
                legal_hold=legal_hold,
            )
        except ValueError as exc:
            raise HTTPException(status_code=400, detail="invalid retention plan request") from exc

    @app.get("/repositories")
    def repository_index(
        provider: Optional[str] = None,
        owner: Optional[str] = None,
        policy_pack: Optional[str] = None,
        status: Optional[str] = None,
        risk_tier: Optional[str] = None,
    ) -> dict:
        return inventory_store.list_repositories(
            provider=provider,
            owner=owner,
            policy_pack=policy_pack,
            status=status,
            risk_tier=risk_tier,
        )

    @app.post("/repositories")
    def upsert_repository(payload: dict) -> dict:
        try:
            return inventory_store.upsert_repository(payload)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail="invalid repository record") from exc

    @app.get("/repositories/{repository_id:path}")
    def repository_item(repository_id: str) -> dict:
        item = inventory_store.get_repository(repository_id)
        if item is None:
            raise HTTPException(status_code=404, detail="repository not found")
        return item

    @app.get("/policy-rollouts")
    def policy_rollout_index(
        repository: Optional[str] = None,
        policy_pack: Optional[str] = None,
        state: Optional[str] = None,
        mode: Optional[str] = None,
        owner: Optional[str] = None,
    ) -> dict:
        return inventory_store.list_policy_rollouts(
            repository=repository,
            policy_pack=policy_pack,
            state=state,
            mode=mode,
            owner=owner,
        )

    @app.post("/policy-rollouts")
    def upsert_policy_rollout(payload: dict) -> dict:
        try:
            return inventory_store.upsert_policy_rollout(payload)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail="invalid policy rollout record") from exc

    @app.get("/policy-rollout-details/{rollout_id:path}")
    @app.get("/policy-rollouts/{rollout_id}/detail")
    def policy_rollout_detail(rollout_id: str) -> dict:
        rollout = inventory_store.get_policy_rollout(rollout_id)
        if rollout is None:
            raise HTTPException(status_code=404, detail="policy rollout not found")
        return _policy_rollout_detail(rollout, inventory_store, activity_store, integration_store)

    @app.get("/policy-rollouts/{rollout_id:path}")
    def policy_rollout_item(rollout_id: str) -> dict:
        item = inventory_store.get_policy_rollout(rollout_id)
        if item is None:
            raise HTTPException(status_code=404, detail="policy rollout not found")
        return item

    @app.get("/agents")
    def agents(status: Optional[str] = None, owner: Optional[str] = None) -> dict:
        return registry_store.list_agents(status=status, owner=owner)

    @app.get("/agents/profiles")
    def agent_profiles() -> dict:
        return default_agent_profiles()

    @app.post("/agents")
    def upsert_agent(payload: dict) -> dict:
        try:
            return registry_store.upsert_agent(payload)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail="invalid agent record") from exc

    @app.get("/agents/{agent_id}")
    def agent(agent_id: str) -> dict:
        item = registry_store.get_agent(agent_id)
        if item is None:
            raise HTTPException(status_code=404, detail="agent not found")
        return item

    @app.get("/mcp/servers")
    def mcp_servers(
        trust_tier: Optional[str] = None,
        approval_state: Optional[str] = None,
        capability: Optional[str] = None,
    ) -> dict:
        return registry_store.list_mcp_servers(trust_tier=trust_tier, approval_state=approval_state, capability=capability)

    @app.get("/mcp/tool-classifications")
    def mcp_tool_classifications(capability: Optional[str] = None) -> dict:
        if capability:
            item = classify_mcp_capability(capability)
            if item is None:
                raise HTTPException(status_code=404, detail="MCP capability classification not found")
            return item
        return default_mcp_tool_classifications()

    @app.post("/mcp/servers")
    def upsert_mcp_server(payload: dict) -> dict:
        try:
            return registry_store.upsert_mcp_server(payload)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail="invalid MCP server record") from exc

    @app.get("/mcp/servers/{server_id}")
    def mcp_server(server_id: str) -> dict:
        item = registry_store.get_mcp_server(server_id)
        if item is None:
            raise HTTPException(status_code=404, detail="MCP server not found")
        return item

    @app.get("/mcp/trust")
    def mcp_trust(server: str, tool: str = "unknown", capability: Optional[str] = None) -> dict:
        return registry_store.evaluate_mcp(server, tool, capability)

    @app.get("/integrations")
    def integration_index(
        provider: Optional[str] = None,
        category: Optional[str] = None,
        status: Optional[str] = None,
        owner: Optional[str] = None,
        environment: Optional[str] = None,
        health_status: Optional[str] = None,
    ) -> dict:
        return integration_store.list_integrations(
            provider=provider,
            category=category,
            status=status,
            owner=owner,
            environment=environment,
            health_status=health_status,
        )

    @app.post("/integrations")
    def upsert_integration(payload: dict) -> dict:
        try:
            return integration_store.upsert_integration(payload)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail="invalid integration record") from exc

    @app.get("/integrations/{integration_id}")
    def integration_item(integration_id: str) -> dict:
        item = integration_store.get_integration(integration_id)
        if item is None:
            raise HTTPException(status_code=404, detail="integration not found")
        return item

    @app.get("/risk/events")
    @app.get("/compliance/mappings")
    def empty_collection() -> list[dict]:
        return []

    @app.get("/approvals")
    def approvals(
        state: Optional[str] = None,
        approver_group: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict:
        return approval_store.list(state=state, approver_group=approver_group, limit=limit, offset=offset)

    @app.post("/approvals")
    def create_approval(payload: dict) -> dict:
        decision = payload["decision"] if isinstance(payload.get("decision"), dict) else payload
        try:
            return approval_store.create_request(
                decision,
                approver_group=payload.get("approver_group"),
                requested_by=payload.get("requested_by", "ai-agent"),
                ttl_hours=int(payload.get("ttl_hours", 24)),
                routing_rules=routing_rules,
            )
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post("/approvals/break-glass")
    def break_glass(payload: dict) -> dict:
        try:
            return approval_store.break_glass(
                decision=payload["decision"] if isinstance(payload.get("decision"), dict) else payload,
                actor=payload.get("actor", ""),
                reason=payload.get("reason", ""),
                approver_group=payload.get("approver_group", "Change Advisory Board"),
                external_ref=payload.get("external_ref"),
                ttl_hours=int(payload.get("ttl_hours", 4)),
            )
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.get("/approvals/{approval_id}")
    def approval(approval_id: str) -> dict:
        item = approval_store.get(approval_id)
        if item is None:
            raise HTTPException(status_code=404, detail="approval not found")
        return item

    @app.post("/approvals/{approval_id}/approve")
    def approve(approval_id: str, payload: dict) -> dict:
        return _decide_approval(approval_store, approval_id, state="approved", payload=payload, rbac_rules=rbac_rules, oidc_config=oidc_config)

    @app.post("/approvals/{approval_id}/deny")
    def deny(approval_id: str, payload: dict) -> dict:
        return _decide_approval(approval_store, approval_id, state="denied", payload=payload, rbac_rules=rbac_rules, oidc_config=oidc_config)

    @app.post("/approvals/{approval_id}/expire")
    def expire(approval_id: str, payload: Optional[dict] = None) -> dict:
        return _decide_approval(
            approval_store,
            approval_id,
            state="expired",
            payload=payload or {"actor": "system", "reason": "approval expired"},
            rbac_rules=rbac_rules,
            oidc_config=oidc_config,
        )

    @app.post("/approvals/{approval_id}/deliver")
    def deliver_approval(approval_id: str, payload: Optional[dict] = None) -> dict:
        item = approval_store.get(approval_id)
        if item is None:
            raise HTTPException(status_code=404, detail="approval not found")
        if provider_config is None:
            raise HTTPException(status_code=400, detail="approval provider config is not configured")
        payload = payload or {}
        try:
            return deliver_provider_requests(
                item,
                provider_config,
                provider=payload.get("provider", "all"),
                retries=int(payload.get("retries", 2)),
                timeout_seconds=float(payload.get("timeout_seconds", 10.0)),
            )
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post("/approvals/{approval_id}/attach-decision")
    def attach_decision_approval(approval_id: str, payload: dict) -> dict:
        item = approval_store.get(approval_id)
        if item is None:
            raise HTTPException(status_code=404, detail="approval not found")
        try:
            return attach_approval_to_decision(payload, item)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.get("/evidence")
    def evidence_index(
        session_id: Optional[str] = None,
        signer: Optional[str] = None,
        min_blocked: Optional[int] = None,
        has_approvals: Optional[bool] = None,
        limit: int = 50,
        offset: int = 0,
    ):
        if isinstance(evidence_store, SQLiteEvidenceMetadataStore):
            return evidence_store.search(
                session_id=session_id,
                signer=signer,
                min_blocked=min_blocked,
                has_approvals=has_approvals,
                limit=limit,
                offset=offset,
            )
        return _filter_json_evidence(
            evidence_store.list(),
            session_id=session_id,
            signer=signer,
            min_blocked=min_blocked,
            has_approvals=has_approvals,
            limit=limit,
            offset=offset,
        )

    @app.post("/evidence")
    def upsert_evidence_metadata(payload: dict) -> dict:
        try:
            return evidence_store.upsert(payload)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.get("/evidence/{session_id}")
    def evidence_metadata(session_id: str) -> dict:
        item = evidence_store.get(session_id)
        if item is None:
            raise HTTPException(status_code=404, detail="evidence metadata not found")
        return item

    @app.get("/api/sandbox/scenarios")
    def sandbox_scenarios() -> list[dict]:
        return [{"id": "before-the-agent-acts", "title": "Before the Agent Acts"}]

    @app.post("/api/sandbox/run")
    def sandbox_run(payload: Optional[dict] = None) -> dict:
        run = create_sandbox_run(**(payload or {}))
        runs[run["run_id"]] = run
        return run

    @app.get("/api/sandbox/runs/{run_id}")
    def get_run(run_id: str) -> dict:
        return runs[run_id]

    @app.get("/api/sandbox/runs/{run_id}/events")
    def get_events(run_id: str) -> list[dict]:
        return runs[run_id]["events"]

    @app.get("/api/sandbox/runs/{run_id}/evidence")
    def get_evidence(run_id: str):
        return Response(evidence_json(runs[run_id]), media_type="application/json")

    @app.get("/api/sandbox/runs/{run_id}/attestation")
    def get_attestation(run_id: str):
        return Response(pr_attestation(runs[run_id]), media_type="text/markdown")

    @app.get("/api/sandbox/runs/{run_id}/compliance")
    def get_compliance(run_id: str):
        return Response(compliance_mapping(runs[run_id]), media_type="text/markdown")

    @app.post("/api/sandbox/runs/{run_id}/replay")
    def replay(run_id: str) -> dict:
        previous = runs[run_id]
        run = create_sandbox_run(previous["policy_mode"], previous["persona"])
        runs[run["run_id"]] = run
        return run

    return app


def _csv_env(name: str) -> list[str]:
    return [item.strip() for item in os.environ.get(name, "").split(",") if item.strip()]


def _filter_json_evidence(
    items: list[dict],
    *,
    session_id: Optional[str] = None,
    signer: Optional[str] = None,
    min_blocked: Optional[int] = None,
    has_approvals: Optional[bool] = None,
    limit: int = 50,
    offset: int = 0,
) -> dict[str, object]:
    limit = max(1, min(limit, 500))
    offset = max(0, offset)
    filtered = items
    if session_id:
        filtered = [item for item in filtered if session_id in str(item.get("session_id", ""))]
    if signer:
        filtered = [item for item in filtered if item.get("signer") == signer]
    if min_blocked is not None:
        filtered = [item for item in filtered if int(item.get("blocked_count", 0)) >= min_blocked]
    if has_approvals is not None:
        filtered = [
            item
            for item in filtered
            if (int(item.get("approval_required_count", 0)) > 0) is has_approvals
        ]
    return {
        "items": filtered[offset : offset + limit],
        "total": len(filtered),
        "limit": limit,
        "offset": offset,
    }


def _policy_rollout_detail(
    rollout: dict,
    inventory_store: InventoryStore | SQLiteInventoryStore,
    activity_store: ActivityStore | SQLiteActivityStore,
    integration_store: IntegrationStore | SQLiteIntegrationStore,
) -> dict[str, object]:
    repository = inventory_store.get_repository(str(rollout.get("repository", "")))
    policy_pack_id = str(rollout.get("policy_pack", ""))
    try:
        policy_pack = PolicyRegistry().get_policy_pack(policy_pack_id)
    except PolicyRegistryError:
        policy_pack = {
            "id": policy_pack_id,
            "title": policy_pack_id or "unknown",
            "description": "Policy pack metadata is not available in this deployment.",
            "version": rollout.get("policy_version", "unknown"),
            "policy": {},
        }
    decisions = activity_store.list_decisions(
        repository=rollout.get("repository"),
        policy_pack=policy_pack_id,
        limit=100,
        offset=0,
    )
    integrations = integration_store.list_integrations()
    return {
        "schema_version": "cavra.policy_rollout.detail.v1",
        "product": "CAVRA",
        "rollout": rollout,
        "repository": repository,
        "policy_pack": {
            "id": policy_pack.get("id"),
            "title": policy_pack.get("title"),
            "description": policy_pack.get("description"),
            "version": policy_pack.get("version"),
            "rule_summary": _policy_rule_summary(policy_pack.get("policy", {})),
        },
        "activity_summary": _decision_summary(decisions.get("items", []), int(decisions.get("total", 0))),
        "integration_summary": _integration_summary(integrations.get("items", [])),
        "readiness": _rollout_readiness(rollout, repository, integrations.get("items", [])),
    }


def _decision_summary(decisions: list[dict], total: int) -> dict[str, object]:
    outcomes: dict[str, int] = {}
    severities: dict[str, int] = {}
    for item in decisions:
        outcome = str(item.get("decision", "unknown"))
        severity = str(item.get("severity", "unknown"))
        outcomes[outcome] = outcomes.get(outcome, 0) + 1
        severities[severity] = severities.get(severity, 0) + 1
    return {
        "total": total,
        "sample_size": len(decisions),
        "outcomes": outcomes,
        "severities": severities,
        "recent_decisions": decisions[:10],
    }


def _policy_rule_summary(policy: dict[str, object]) -> dict[str, int]:
    sections = {
        "filesystem": policy.get("filesystem", {}),
        "commands": policy.get("commands", {}),
        "git": policy.get("git", {}),
        "mcp": policy.get("mcp", {}),
        "approvals": policy.get("approvals", {}),
        "evidence": policy.get("evidence", {}),
    }
    return {name: _count_rule_entries(value) for name, value in sections.items()}


def _count_rule_entries(value: object) -> int:
    if isinstance(value, list):
        return len(value)
    if isinstance(value, dict):
        return sum(_count_rule_entries(item) for item in value.values())
    return 1 if value else 0


def _integration_summary(integrations: list[dict]) -> dict[str, object]:
    by_category: dict[str, int] = {}
    by_health: dict[str, int] = {}
    for item in integrations:
        category = str(item.get("category", "unknown"))
        health = str(item.get("health_status", "unknown"))
        by_category[category] = by_category.get(category, 0) + 1
        by_health[health] = by_health.get(health, 0) + 1
    return {
        "total": len(integrations),
        "by_category": by_category,
        "by_health": by_health,
        "active_or_configured": [
            item
            for item in integrations
            if item.get("status") in {"active", "configured"}
        ][:10],
    }


def _rollout_readiness(rollout: dict, repository: dict | None, integrations: list[dict]) -> dict[str, object]:
    checks = [
        {
            "id": "repository_registered",
            "status": "pass" if repository else "warn",
            "message": "Repository inventory record is present." if repository else "Repository inventory record is missing.",
        },
        {
            "id": "policy_coverage",
            "status": "pass" if int(rollout.get("coverage_percent", 0)) >= 80 else "warn",
            "message": f"Coverage is {int(rollout.get('coverage_percent', 0))}%.",
        },
        {
            "id": "source_control_integration",
            "status": "pass" if any(item.get("category") == "source_control" for item in integrations) else "warn",
            "message": "Source-control integration is inventoried."
            if any(item.get("category") == "source_control" for item in integrations)
            else "Source-control integration is not inventoried.",
        },
        {
            "id": "siem_or_storage_integration",
            "status": "pass"
            if any(item.get("category") in {"siem", "storage"} for item in integrations)
            else "warn",
            "message": "Evidence export or storage integration is inventoried."
            if any(item.get("category") in {"siem", "storage"} for item in integrations)
            else "Evidence export or storage integration is not inventoried.",
        },
    ]
    return {
        "status": "ready" if all(item["status"] == "pass" for item in checks) else "needs_attention",
        "checks": checks,
    }


def _console_security_boundary(
    *,
    oidc_configured: bool,
    rbac_configured: bool,
    cors_origins: list[str],
) -> dict[str, object]:
    return {
        "schema_version": "cavra.console.security_boundary.v1",
        "product": "CAVRA",
        "mode": "oidc_rbac_ready" if oidc_configured and rbac_configured else "local_or_demo",
        "oidc": {
            "configured": oidc_configured,
            "config_env": "CAVRA_APPROVAL_OIDC_CONFIG",
            "supported_algorithms": ["RS256"],
            "validated_claims": ["iss", "aud", "exp", "nbf", "groups", "roles", "email", "sub"],
        },
        "rbac": {
            "configured": rbac_configured,
            "config_env": "CAVRA_APPROVAL_RBAC_FILE",
            "boundaries": ["approval_group", "repository_permissions", "group_mappings"],
        },
        "cors": {
            "configured": bool(cors_origins),
            "origins": cors_origins,
        },
        "console_permissions": [
            "read_activity",
            "read_inventory",
            "read_integrations",
            "read_evidence_metadata",
            "approval_decision_requires_actor_claims_or_token_when_configured",
        ],
        "operator_notes": [
            "Host the console behind enterprise identity before production use.",
            "Keep backup and restore operations in the CLI or platform runbook, not browser actions.",
            "Use repository RBAC for approval decisions that affect scoped repositories.",
        ],
    }


def _decide_approval(
    approval_store: ApprovalStore,
    approval_id: str,
    *,
    state: str,
    payload: dict,
    rbac_rules: dict[str, object] | None = None,
    oidc_config: dict[str, object] | None = None,
) -> dict:
    actor_context = None
    if isinstance(payload.get("actor_claims"), dict):
        actor_context = actor_context_from_claims(payload["actor_claims"], rbac_rules=rbac_rules)
    elif isinstance(payload.get("actor_token"), str):
        if not oidc_config:
            raise HTTPException(status_code=400, detail="approval OIDC config is not configured")
        try:
            actor_context = actor_context_from_oidc_token(payload["actor_token"], oidc_config, rbac_rules=rbac_rules)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
    try:
        return approval_store.decide(
            approval_id,
            state=state,
            actor=payload.get("actor", ""),
            reason=payload.get("reason", ""),
            external_ref=payload.get("external_ref"),
            actor_context=actor_context,
            rbac_rules=rbac_rules,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="approval not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


app = create_app() if FastAPI is not None else None
