from __future__ import annotations

import re
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from cavra.policy_registry import PolicyRegistry


@dataclass(frozen=True)
class ActionDecision:
    decision: str
    reason: str | None = None
    decision_id: str = ""
    session_id: str = "local"
    agent_id: str = "unknown-agent"
    actor: str = "ai-agent"
    action_type: str = "unknown"
    target: str = ""
    requested_operation: str = ""
    policy_pack: str = "cavra-ai-agent-baseline"
    policy_id: str = "cavra-ai-agent-baseline"
    rule_id: str = "runtime.default"
    severity: str = "low"
    evidence_refs: tuple[str, ...] = ()
    approver_group: str | None = None
    timestamp: str = ""
    correlation_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "session_id": self.session_id,
            "agent_id": self.agent_id,
            "actor": self.actor,
            "action_type": self.action_type,
            "target": self.target,
            "requested_operation": self.requested_operation,
            "policy_pack": self.policy_pack,
            "policy_id": self.policy_id,
            "rule_id": self.rule_id,
            "decision": self.decision,
            "severity": self.severity,
            "reason": self.reason,
            "evidence_refs": list(self.evidence_refs),
            "approver_group": self.approver_group,
            "timestamp": self.timestamp,
            "correlation_id": self.correlation_id,
        }


class RuntimeGuard:
    def __init__(
        self,
        policy_pack: str | None = None,
        *,
        session_id: str = "local",
        agent_id: str = "unknown-agent",
        actor: str = "ai-agent",
    ) -> None:
        self.registry = PolicyRegistry()
        self.policy_pack = policy_pack or "cavra-ai-agent-baseline"
        self.policy = self.registry.load_policy(self.policy_pack)
        self.session_id = session_id
        self.agent_id = agent_id
        self.actor = actor
        self.sensitive_read = self._patterns("filesystem", "block_read")
        self.sensitive_write = self._patterns("filesystem", "block_write")
        self.approval_write = self._patterns("filesystem", "require_approval_write")
        self.command_block = self._patterns("commands", "block")
        self.command_allow = self._patterns("commands", "allow")

    def _patterns(self, section: str, key: str) -> list[str]:
        items = self.policy.get(section, {}).get(key, [])
        if not isinstance(items, list):
            return []
        return [str(item) for item in items if item is not None]

    def evaluate_file_access(self, path: Path, mode: str) -> ActionDecision:
        target = str(path)
        patterns = self.sensitive_read if mode == "read" else self.sensitive_write
        for pattern in patterns:
            if self._match_pattern(target, pattern):
                return self._decision(
                    "block",
                    f"Matched sensitive path policy: {pattern}",
                    action_type=f"{mode}_file",
                    target=target,
                    requested_operation=mode,
                    rule_id=f"filesystem.{mode}.block",
                    severity="high",
                )
        if mode == "write":
            for pattern in self.approval_write:
                if self._match_pattern(target, pattern):
                    return self._decision(
                        "require_approval",
                        f"Matched approval-required path policy: {pattern}",
                        action_type="write_file",
                        target=target,
                        requested_operation=mode,
                        rule_id="filesystem.write.require_approval",
                        severity="high",
                        approver_group="Platform Security",
                    )
        return self._decision(
            "allow",
            "No sensitive path policy matched.",
            action_type=f"{mode}_file",
            target=target,
            requested_operation=mode,
            rule_id=f"filesystem.{mode}.allow",
        )

    def evaluate_command(self, command: str) -> ActionDecision:
        cleaned = command.strip()
        for pattern in self.command_block:
            if self._match_pattern(cleaned, pattern):
                return self._decision(
                    "block",
                    f"Matched blocked command policy: {pattern}",
                    action_type="execute_command",
                    target=cleaned,
                    requested_operation=cleaned,
                    rule_id="commands.block",
                    severity="critical" if "apply" in cleaned or "delete" in cleaned else "high",
                )
        for pattern in self.command_allow:
            if self._match_pattern(cleaned, pattern):
                return self._decision(
                    "allow",
                    f"Matched allowed command policy: {pattern}",
                    action_type="execute_command",
                    target=cleaned,
                    requested_operation=cleaned,
                    rule_id="commands.allow",
                )
        return self._decision(
            "require_approval",
            "No allow rule matched; review required.",
            action_type="execute_command",
            target=cleaned,
            requested_operation=cleaned,
            rule_id="commands.default.require_approval",
            severity="medium",
            approver_group="Repository Owners",
        )

    def evaluate_git_action(self, action: str, target: str | None = None) -> ActionDecision:
        if action == "push" and target:
            if target.endswith("main") or target.endswith("master"):
                return self._decision(
                    "block",
                    "Direct push to protected branch is prohibited.",
                    action_type="git_operation",
                    target=target,
                    requested_operation=action,
                    rule_id="git.protected_branch.block_direct_push",
                    severity="high",
                )
        return self._decision(
            "allow",
            "Git operation is allowed by policy.",
            action_type="git_operation",
            target=target or action,
            requested_operation=action,
            rule_id="git.allow",
        )

    def evaluate_mcp_tool_call(self, server: str, tool: str, capability: str | None = None) -> ActionDecision:
        mcp = self.policy.get("mcp", {})
        allowed = set(mcp.get("allowed_servers", []) or [])
        blocked = set(mcp.get("blocked_servers", []) or [])
        target = f"{server}:{tool}"
        if server in blocked or (mcp.get("block_unknown_servers", True) and server not in allowed):
            return self._decision(
                "block",
                "Untrusted MCP server with filesystem/tool capability is not approved.",
                action_type="mcp_tool_call",
                target=target,
                requested_operation=capability or tool,
                rule_id="mcp.server.trust.block_unknown",
                severity="high",
            )
        return self._decision(
            "allow",
            "MCP server is trusted for this tool call.",
            action_type="mcp_tool_call",
            target=target,
            requested_operation=capability or tool,
            rule_id="mcp.server.trust.allow",
        )

    def generate_pr_attestation_decision(self, target: str = "pull_request") -> ActionDecision:
        return self._decision(
            "allow_with_attestation",
            "PR is allowed with CAVRA evidence and reviewer guidance.",
            action_type="pull_request",
            target=target,
            requested_operation="create",
            rule_id="git.pull_request.allow_with_attestation",
            severity="medium",
        )

    @staticmethod
    def _match_pattern(value: str, pattern: str) -> bool:
        regex = re.escape(pattern).replace("\\*\\*", ".*").replace("\\*", ".*")
        return re.fullmatch(regex, value) is not None

    def _decision(
        self,
        decision: str,
        reason: str,
        *,
        action_type: str,
        target: str,
        requested_operation: str,
        rule_id: str,
        severity: str = "low",
        approver_group: str | None = None,
    ) -> ActionDecision:
        decision_id = f"dec_{uuid.uuid4().hex[:12]}"
        return ActionDecision(
            decision=decision,
            reason=reason,
            decision_id=decision_id,
            session_id=self.session_id,
            agent_id=self.agent_id,
            actor=self.actor,
            action_type=action_type,
            target=target,
            requested_operation=requested_operation,
            policy_pack=self.policy_pack,
            policy_id=self.policy_pack,
            rule_id=rule_id,
            severity=severity,
            evidence_refs=(f"evidence://{self.session_id}/{decision_id}",),
            approver_group=approver_group,
            timestamp=datetime.now(timezone.utc).isoformat(),
            correlation_id=f"corr_{uuid.uuid4().hex[:12]}",
        )
