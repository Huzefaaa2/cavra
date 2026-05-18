from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from cavra.runtime import RuntimeGuard


SCENARIOS = [
    {
        "id": "before-the-agent-acts",
        "title": "Before the Agent Acts",
        "description": "Run representative AI-agent actions through real CAVRA policy decisions.",
        "default_policy_pack": "cavra-ai-agent-baseline",
        "personas": ["Developer", "CISO", "Platform Engineer", "Auditor"],
        "policy_modes": ["enforce", "audit_only", "strict"],
    }
]


def sandbox_scenarios() -> list[dict[str, Any]]:
    return SCENARIOS


def before_agent_acts_events(
    *,
    run_id: str,
    persona: str,
    policy_mode: str,
    policy_pack: str = "cavra-ai-agent-baseline",
) -> list[dict[str, Any]]:
    guard = RuntimeGuard(policy_pack=policy_pack, agent_id="sandbox-agent", actor="simulated-ai-agent")
    decisions = [
        guard.evaluate_file_access(Path(".env"), "read"),
        guard.evaluate_file_access(Path("iam/admin-role.tf"), "write"),
        guard.evaluate_command("terraform plan"),
        guard.evaluate_command("terraform apply -auto-approve"),
        guard.evaluate_mcp_tool_call("unknown filesystem MCP server", "read_file", "filesystem"),
        guard.evaluate_git_action("push", "origin/main"),
        guard.generate_pr_attestation_decision("create PR"),
    ]
    business_impact = {
        "read_file": "Prevents secret exposure into AI-agent context.",
        "write_file": "Routes privilege-impacting infrastructure changes to security reviewers.",
        "execute_command": "Separates read-only planning from production-impacting execution.",
        "mcp_tool_call": "Prevents untrusted tool expansion through unknown MCP servers.",
        "git_operation": "Preserves protected-branch and review controls.",
        "pull_request": "Allows collaboration with audit-ready evidence.",
    }
    remediation = {
        "block": "Use an approved workflow or request policy exception with evidence.",
        "require_approval": "Open an approval request for the mapped approver group.",
        "allow": "Continue; decision is recorded for audit.",
        "allow_with_attestation": "Attach the generated CAVRA attestation to the PR.",
    }
    events = []
    for index, decision in enumerate(decisions, start=1):
        payload = decision.to_dict()
        events.append(
            {
                **payload,
                "event_id": f"evt_{index}",
                "decision_id": payload.get("decision_id") or f"dec_{run_id}_{index}",
                "session_id": run_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "agent": "Simulated AI-agent scenario using real CAVRA policy decisions.",
                "agent_id": "sandbox-agent",
                "actor": "simulated-ai-agent",
                "repository": "sandbox/before-the-agent-acts",
                "persona": persona,
                "policy_mode": policy_mode,
                "business_impact": business_impact.get(payload["action_type"], "Decision recorded."),
                "evidence_generated": payload["evidence_refs"],
                "remediation": remediation.get(payload["decision"], "Review decision."),
            }
        )
    return events


def create_sandbox_run(
    policy_mode: str = "enforce",
    persona: str = "Developer",
    scenario: str = "before-the-agent-acts",
    policy_pack: str = "cavra-ai-agent-baseline",
) -> dict[str, Any]:
    if scenario != "before-the-agent-acts":
        raise ValueError(f"unknown sandbox scenario: {scenario}")
    run_id = f"run_{uuid.uuid4().hex[:10]}"
    normalized_mode = _normalize_policy_mode(policy_mode)
    events = before_agent_acts_events(
        run_id=run_id,
        persona=persona,
        policy_mode=normalized_mode,
        policy_pack=policy_pack,
    )
    blocked = sum(1 for event in events if event["decision"] == "block")
    approvals = sum(1 for event in events if event["decision"] == "require_approval")
    return {
        "schema_version": "cavra.sandbox.run.v1",
        "product": "CAVRA",
        "run_id": run_id,
        "scenario": scenario,
        "persona": persona,
        "policy_mode": normalized_mode,
        "policy_pack": policy_pack,
        "tagline": "Before the agent acts, CAVRA decides.",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "decision_count": len(events),
        "blocked_count": blocked,
        "approval_required_count": approvals,
        "source": "cavra-api",
        "artifacts": _run_artifacts(run_id),
        "events": events,
    }


def evidence_json(run: dict[str, Any]) -> str:
    return json.dumps({"product": "CAVRA", "run": run}, indent=2)


def pr_attestation(run: dict[str, Any]) -> str:
    blocked = sum(1 for event in run["events"] if event["decision"] == "block")
    approvals = sum(1 for event in run["events"] if event["decision"] == "require_approval")
    return "\n".join(
        [
            "# CAVRA PR Attestation",
            "",
            "Before the agent acts, CAVRA decides.",
            "",
            f"Run: {run['run_id']}",
            f"Blocked actions: {blocked}",
            f"Approval-required actions: {approvals}",
            "",
            "This PR is allowed only with CAVRA evidence and reviewer guidance.",
        ]
    )


def compliance_mapping(run: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# CAVRA Compliance Mapping",
            "",
            "- Secret exposure: blocked `.env` read.",
            "- Change control: approval required for IAM modification.",
            "- Production safety: autonomous `terraform apply -auto-approve` blocked.",
            "- Tool governance: unknown filesystem MCP server blocked.",
            "- Source control: direct push to `main` blocked.",
            f"- Evidence run: `{run['run_id']}`.",
        ]
    )


def sandbox_evidence_metadata(run: dict[str, Any]) -> dict[str, Any]:
    return {
        "session_id": run["run_id"],
        "created_at": run.get("created_at"),
        "signer": "sandbox-api",
        "decision_count": run["decision_count"],
        "blocked_count": run["blocked_count"],
        "approval_required_count": run["approval_required_count"],
        "decisions": run["events"],
        "attestation_targets": [event["target"] for event in run["events"]],
        "artifact_count": len(run.get("artifacts", [])),
        "retention": {"retention_days": 30},
    }


def sandbox_activity_session(run: dict[str, Any]) -> dict[str, Any]:
    return {
        "session_id": run["run_id"],
        "agent_id": "sandbox-agent",
        "actor": "simulated-ai-agent",
        "repository": "sandbox/before-the-agent-acts",
        "policy_pack": run["policy_pack"],
        "state": "completed",
        "started_at": run.get("created_at"),
        "updated_at": run.get("created_at"),
        "decision_count": run["decision_count"],
        "blocked_count": run["blocked_count"],
        "approval_required_count": run["approval_required_count"],
        "evidence_refs": [f"sandbox://runs/{run['run_id']}"],
    }


def _run_artifacts(run_id: str) -> list[dict[str, Any]]:
    return [
        {
            "artifact": "evidence.json",
            "kind": "evidence",
            "media_type": "application/json",
            "download_url": f"/api/sandbox/runs/{run_id}/evidence",
        },
        {
            "artifact": "pr-attestation.md",
            "kind": "attestation",
            "media_type": "text/markdown",
            "download_url": f"/api/sandbox/runs/{run_id}/attestation",
        },
        {
            "artifact": "compliance-mapping.md",
            "kind": "compliance",
            "media_type": "text/markdown",
            "download_url": f"/api/sandbox/runs/{run_id}/compliance",
        },
    ]


def _normalize_policy_mode(policy_mode: str) -> str:
    normalized = policy_mode.strip().lower().replace("-", "_").replace(" ", "_")
    aliases = {
        "enforce": "enforce",
        "audit_only": "audit_only",
        "audit-only": "audit_only",
        "strict_regulated_repository": "strict",
        "strict": "strict",
    }
    return aliases.get(normalized, normalized or "enforce")
