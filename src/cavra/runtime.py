from __future__ import annotations

import re
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from cavra.policy_registry import PolicyRegistry
from cavra.registry import RegistryStore


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
        registry_store: RegistryStore | None = None,
    ) -> None:
        self.registry = PolicyRegistry()
        self.policy_pack = policy_pack or "cavra-ai-agent-baseline"
        self.policy = self.registry.load_policy(self.policy_pack)
        self.session_id = session_id
        self.agent_id = agent_id
        self.actor = actor
        self.registry_store = registry_store
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
        if self.registry_store is not None:
            registry_decision = self.registry_store.evaluate_mcp(server, tool, capability)
            return self._decision(
                registry_decision["decision"],
                registry_decision["reason"],
                action_type="mcp_tool_call",
                target=f"{server}:{tool}",
                requested_operation=capability or tool,
                rule_id=registry_decision["rule_id"],
                severity=registry_decision["severity"],
                approver_group=registry_decision.get("approver_group"),
            )
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

    def evaluate_release_governance_record(
        self,
        record: dict[str, Any] | None,
        *,
        target: str | None = None,
        requested_operation: str = "verify",
    ) -> ActionDecision:
        payload = record or {}
        kind = _string_value(payload, "metadata_kind") or target or "release-governance-record"
        action_type = "release_governance_record"
        if not payload:
            return self._decision(
                "require_approval",
                "Release governance record payload is missing.",
                action_type=action_type,
                target=target or kind,
                requested_operation=requested_operation,
                rule_id="release_governance.record.missing",
                severity="medium",
                approver_group="Release Governance",
            )

        approval_state = _approval_state(payload)
        approval_id = _approval_id(payload)
        required_count = _int_value(payload, "approval_required_count")
        requires_approval = required_count > 0 or bool(approval_state) or _approval_required_kind(kind)

        if approval_state == "approved":
            if not approval_id and requires_approval:
                return self._decision(
                    "block",
                    f"{kind} is approved but does not include an approval_id.",
                    action_type=action_type,
                    target=target or kind,
                    requested_operation=requested_operation,
                    rule_id="release_governance.approval.missing",
                    severity="critical",
                    approver_group="Release Governance",
                )
            return self._decision(
                "allow",
                f"{kind} is backed by an approved release governance approval.",
                action_type=action_type,
                target=target or kind,
                requested_operation=requested_operation,
                rule_id="release_governance.approval.approved",
            )
        if approval_state == "pending":
            return self._decision(
                "require_approval",
                f"{kind} is waiting for release governance approval.",
                action_type=action_type,
                target=target or kind,
                requested_operation=requested_operation,
                rule_id="release_governance.approval.pending",
                severity="high",
                approver_group="Release Governance",
            )
        if approval_state in {"denied", "rejected", "expired", "cancelled", "canceled"}:
            return self._decision(
                "block",
                f"{kind} is bound to a non-approved approval state: {approval_state}.",
                action_type=action_type,
                target=target or kind,
                requested_operation=requested_operation,
                rule_id="release_governance.approval.denied",
                severity="critical",
                approver_group="Release Governance",
            )
        if approval_state:
            return self._decision(
                "require_approval",
                f"{kind} has an unknown approval state: {approval_state}.",
                action_type=action_type,
                target=target or kind,
                requested_operation=requested_operation,
                rule_id="release_governance.approval.unknown",
                severity="medium",
                approver_group="Release Governance",
            )
        if _delivery_failed(payload):
            return self._decision(
                "block",
                f"{kind} includes failed release delivery evidence.",
                action_type=action_type,
                target=target or kind,
                requested_operation=requested_operation,
                rule_id="release_governance.delivery.failed",
                severity="high",
                approver_group="Release Governance",
            )
        if _critical_release_signal(payload):
            return self._decision(
                "require_approval",
                f"{kind} contains critical release governance signals.",
                action_type=action_type,
                target=target or kind,
                requested_operation=requested_operation,
                rule_id="release_governance.signal.critical",
                severity="high",
                approver_group="Release Governance",
            )
        if requires_approval:
            decision = "require_approval"
            rule_id = "release_governance.approval.required"
            severity = "high"
            if _release_execution_kind(kind):
                decision = "block"
                rule_id = "release_governance.approval.missing"
                severity = "critical"
            return self._decision(
                decision,
                f"{kind} requires an approval record before execution.",
                action_type=action_type,
                target=target or kind,
                requested_operation=requested_operation,
                rule_id=rule_id,
                severity=severity,
                approver_group="Release Governance",
            )
        if _known_release_governance_kind(kind):
            return self._decision(
                "allow",
                f"{kind} is recognized release governance evidence with no blocking signal.",
                action_type=action_type,
                target=target or kind,
                requested_operation=requested_operation,
                rule_id="release_governance.record.verified",
            )
        return self._decision(
            "allow",
            f"{kind} does not require release governance approval.",
            action_type=action_type,
            target=target or kind,
            requested_operation=requested_operation,
            rule_id="release_governance.approval.not_required",
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


def _approval_required_kind(kind: str) -> bool:
    return kind in {
        "release-channel-promotion-request",
        "endpoint-reconciliation-automation",
        "endpoint-drift-remediation-request",
        "endpoint-drift-remediation-execution",
        "endpoint-remediation-handoff",
        "rollout-promotion-execution",
        "rollout-rollback-execution",
    }


def _release_execution_kind(kind: str) -> bool:
    return kind in {
        "endpoint-drift-remediation-execution",
        "rollout-promotion-execution",
        "rollout-rollback-execution",
    }


def _known_release_governance_kind(kind: str) -> bool:
    return kind in {
        "endpoint-inventory-ingestion",
        "endpoint-inventory-freshness-report",
        "managed-endpoint-reconciliation",
        "endpoint-management-export",
        "endpoint-management-publication-delivery",
        "endpoint-reconciliation-automation",
        "endpoint-drift-remediation-request",
        "endpoint-drift-remediation-execution",
        "endpoint-remediation-handoff",
        "endpoint-remediation-handoff-status",
        "endpoint-remediation-sla-report",
        "endpoint-remediation-sla-notification-plan",
        "endpoint-remediation-sla-notification-ack",
        "endpoint-remediation-sla-escalation-plan",
        "endpoint-remediation-sla-escalation-review",
        "endpoint-remediation-sla-escalation-recurrence-plan",
        "endpoint-remediation-sla-escalation-suppression-audit",
        "endpoint-remediation-sla-escalation-recurrence-retry-plan",
        "endpoint-remediation-sla-escalation-owner-digest",
        "endpoint-remediation-sla-escalation-suppression-trend",
        "endpoint-remediation-sla-escalation-recurrence-automation-run",
        "endpoint-remediation-sla-escalation-recurrence-automation-health-alert-plan",
        "endpoint-remediation-sla-escalation-recurrence-automation-health-alert-ack",
        "release-channel-promotion-request",
        "release-connector-delivery",
        "rollout-promotion-execution",
        "rollout-rollback-execution",
        "rollout-evidence-capture",
        "rollout-evidence-verification",
        "rollout-artifact-retrieval",
        "rollout-artifact-integrity",
    }


def _delivery_failed(record: dict[str, Any]) -> bool:
    if _string_value(record, "metadata_kind") not in {
        "endpoint-management-publication-delivery",
        "release-connector-delivery",
    }:
        return False
    return not _bool_value(record, "delivery_success")


def _critical_release_signal(record: dict[str, Any]) -> bool:
    alert_level = _normalize_state(_string_value(record, "alert_level"))
    drift_status = _normalize_state(_string_value(record, "drift_status"))
    handoff_status = _normalize_state(_string_value(record, "handoff_status"))
    verification_status = _normalize_state(_string_value(record, "verification_status"))
    integrity_status = _normalize_state(_string_value(record, "integrity_status"))
    return (
        alert_level in {"critical", "blocked", "breached"}
        or drift_status in {"drifted", "non_compliant", "drift_detected"}
        or handoff_status in {"blocked", "failed"}
        or verification_status in {"failed", "blocked", "mismatch"}
        or integrity_status in {"failed", "mismatch", "tampered"}
        or _int_value(record, "blocked_count") > 0
        or _int_value(record, "critical_count") > 0
        or _int_value(record, "breached_count") > 0
        or _int_value(record, "failed_delivery_count") > 0
        or _int_value(record, "connector_delivery_failure_count") > 0
        or _int_value(record, "failed_verification_count") > 0
        or _int_value(record, "integrity_failure_count") > 0
    )


def _approval_id(record: dict[str, Any]) -> str:
    value = _string_value(record, "approval_id")
    if value:
        return value
    approval = record.get("approval")
    if isinstance(approval, dict):
        return _string_value(approval, "approval_id")
    return ""


def _approval_state(record: dict[str, Any]) -> str:
    value = _string_value(record, "approval_state")
    if value:
        return _normalize_state(value)
    approval = record.get("approval")
    if isinstance(approval, dict):
        return _normalize_state(_string_value(approval, "state"))
    return ""


def _string_value(record: dict[str, Any], key: str) -> str:
    value = record.get(key)
    if value is None:
        return ""
    return str(value).strip()


def _int_value(record: dict[str, Any], key: str) -> int:
    value = record.get(key)
    if isinstance(value, bool) or value is None:
        return 0
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    return 0


def _bool_value(record: dict[str, Any], key: str) -> bool:
    value = record.get(key)
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return _normalize_state(value) in {"true", "yes", "success", "succeeded"}
    return str(value).lower() == "true"


def _normalize_state(value: str) -> str:
    return value.strip().lower().replace("-", "_")
