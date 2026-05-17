from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class AuditAction:
    type: str
    target: str
    decision: str
    reason: str | None = None
    rule_id: str | None = None
    severity: str | None = None
    evidence_refs: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.type,
            "target": self.target,
            "decision": self.decision,
            "reason": self.reason,
            "rule_id": self.rule_id,
            "severity": self.severity,
            "evidence_refs": self.evidence_refs,
        }


@dataclass
class SessionAudit:
    session_id: str
    tool: str
    repo: Path
    started_at: datetime = field(default_factory=datetime.utcnow)
    actions: list[AuditAction] = field(default_factory=list)

    def add_action(self, action: AuditAction) -> None:
        self.actions.append(action)

    def to_dict(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "tool": self.tool,
            "repo": str(self.repo),
            "started_at": self.started_at.isoformat() + "Z",
            "actions": [action.to_dict() for action in self.actions],
        }

    def write(self, destination: Path) -> Path:
        destination.mkdir(parents=True, exist_ok=True)
        audit_path = destination / f"session-{self.session_id}.json"
        audit_path.write_text(json.dumps(self.to_dict(), indent=2), encoding="utf-8")
        return audit_path


def create_attestation_markdown(audit: SessionAudit) -> str:
    allowed = [action for action in audit.actions if action.decision == "allow"]
    blocked = [action for action in audit.actions if action.decision == "block"]
    required = [action for action in audit.actions if action.decision == "require_approval"]

    lines = [
        "## CAVRA PR Attestation",
        "",
        "Controlled Agentic Verification & Runtime Authority",
        "",
        "Before the agent acts, CAVRA decides.",
        "",
        f"Agent: {audit.tool}",
        f"Session: {audit.session_id}",
        f"Repository: {audit.repo}",
        "",
        "### Decisions",
        f"- Allowed actions: {len(allowed)}",
        f"- Blocked actions: {len(blocked)}",
        f"- Approval-required actions: {len(required)}",
        "",
    ]

    if blocked:
        lines.append("### Blocked Actions")
        for action in blocked:
            lines.append(f"- `{action.target}` — {action.reason or 'blocked by policy'}")
        lines.append("")

    if required:
        lines.append("### Human Approval Required")
        for action in required:
            lines.append(f"- `{action.target}` — {action.reason or 'requires approval'}")
        lines.append("")

    return "\n".join(lines)


def action_from_decision(decision: Any) -> AuditAction:
    payload = decision.to_dict() if hasattr(decision, "to_dict") else {}
    return AuditAction(
        type=payload.get("action_type", "unknown"),
        target=payload.get("target", ""),
        decision=payload.get("decision", "audit_only"),
        reason=payload.get("reason"),
        rule_id=payload.get("rule_id"),
        severity=payload.get("severity"),
        evidence_refs=payload.get("evidence_refs", []),
    )
