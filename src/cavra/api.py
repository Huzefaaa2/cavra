from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from cavra.evidence import EvidenceMetadataStore
from cavra.policy_registry import PolicyRegistry
from cavra.runtime import RuntimeGuard
from cavra.sandbox import compliance_mapping, create_sandbox_run, evidence_json, pr_attestation

try:
    from fastapi import FastAPI, HTTPException, Response
except ImportError:  # pragma: no cover
    FastAPI = None
    HTTPException = None
    Response = None


def create_app():
    if FastAPI is None:
        raise RuntimeError("Install fastapi and uvicorn to run the CAVRA API.")
    app = FastAPI(
        title="CAVRA API",
        description="Controlled Agentic Verification & Runtime Authority API for AI-agent runtime governance.",
        version="0.1.0",
    )
    runs: dict[str, dict] = {}
    evidence_store = EvidenceMetadataStore(
        Path(os.environ.get("CAVRA_EVIDENCE_METADATA_STORE", ".cavra/api/evidence-metadata.json"))
    )

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "product": "CAVRA"}

    @app.get("/version")
    def version() -> dict[str, str]:
        return {"version": "0.1.0", "name": "CAVRA Runtime Server"}

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
    @app.get("/approvals")
    @app.get("/integrations")
    @app.get("/mcp/servers")
    @app.get("/mcp/trust")
    @app.get("/risk/events")
    @app.get("/compliance/mappings")
    def empty_collection() -> list[dict]:
        return []

    @app.get("/evidence")
    def evidence_index() -> list[dict]:
        return evidence_store.list()

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


app = create_app() if FastAPI is not None else None
