from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

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
from cavra.policy_registry import PolicyRegistry
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
        return {
            "product": "CAVRA",
            "api_base_url": os.environ.get("CAVRA_PUBLIC_API_BASE_URL", ""),
            "metadata_mode": metadata_mode,
            "approval_mode": approval_mode,
            "approval_provider_delivery": "configured" if provider_config is not None else "disabled",
            "approval_oidc": "configured" if oidc_config else "disabled",
            "approval_rbac": "configured" if rbac_rules else "disabled",
            "cors_origins": cors_origins,
            "endpoints": {
                "evidence": "/evidence",
                "evidence_item": "/evidence/{session_id}",
                "approvals": "/approvals",
                "sandbox_run": "/api/sandbox/run",
            },
        }

    @app.get("/policies")
    @app.get("/policy-packs")
    def policies() -> list[dict]:
        return PolicyRegistry().list_policy_packs()

    @app.post("/decisions")
    def decisions(payload: dict) -> dict:
        guard = RuntimeGuard(policy_pack=payload.get("policy_pack") or "cavra-ai-agent-baseline")
        action_type = payload.get("action_type")
        target = payload.get("target", "")
        if action_type == "read_file":
            return guard.evaluate_file_access(target, "read").to_dict()
        if action_type == "write_file":
            return guard.evaluate_file_access(target, "write").to_dict()
        if action_type == "execute_command":
            return guard.evaluate_command(target).to_dict()
        if action_type == "git_operation":
            return guard.evaluate_git_action(payload.get("operation", "push"), target).to_dict()
        return guard.evaluate_mcp_tool_call(payload.get("server", "unknown"), payload.get("tool", "unknown"), payload.get("capability")).to_dict()

    @app.get("/sessions")
    @app.get("/agents")
    @app.get("/repositories")
    @app.get("/integrations")
    @app.get("/mcp/servers")
    @app.get("/mcp/trust")
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
