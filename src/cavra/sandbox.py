from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from cavra.runtime import RuntimeGuard


def before_agent_acts_events(policy_pack: str = "cavra-ai-agent-baseline") -> list[dict[str, Any]]:
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
                "event_id": f"evt_{index}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "agent": "Simulated AI-agent scenario using real CAVRA policy decisions.",
                "business_impact": business_impact.get(payload["action_type"], "Decision recorded."),
                "evidence_generated": payload["evidence_refs"],
                "remediation": remediation.get(payload["decision"], "Review decision."),
                **payload,
            }
        )
    return events


def create_sandbox_run(policy_mode: str = "enforce", persona: str = "Developer") -> dict[str, Any]:
    run_id = f"run_{uuid.uuid4().hex[:10]}"
    events = before_agent_acts_events()
    return {
        "run_id": run_id,
        "scenario": "before-the-agent-acts",
        "persona": persona,
        "policy_mode": policy_mode,
        "tagline": "Before the agent acts, CAVRA decides.",
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
