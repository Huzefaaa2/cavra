from __future__ import annotations

import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from terraguard_agentshield.audit import AuditAction, SessionAudit
from terraguard_agentshield.runtime import RuntimeGuard


@dataclass
class AgentSession:
    session_id: str
    tool: str
    repo: Path
    policy_pack: str | None
    audit: SessionAudit
    audit_path: Path


class AgentSessionManager:
    def __init__(self, repo: Path, tool: str, policy_pack: str | None = None, output_dir: Path = Path(".terraguard")) -> None:
        self.repo = repo.resolve()
        self.tool = tool
        self.policy_pack = policy_pack
        self.output_dir = output_dir
        self.guard = RuntimeGuard(policy_pack=self.policy_pack)

    def start_session(self) -> AgentSession:
        session_id = uuid.uuid4().hex[:12]
        audit = SessionAudit(session_id=session_id, tool=self.tool, repo=self.repo)

        # Example runtime checks for startup. Real runtime enforcement happens via integration.
        file_decision = self.guard.evaluate_file_access(self.repo / ".env", "read")
        audit.add_action(AuditAction(type="read_file", target=".env", decision=file_decision.decision, reason=file_decision.reason))

        command_decision = self.guard.evaluate_command("terraform apply")
        audit.add_action(AuditAction(type="execute_command", target="terraform apply", decision=command_decision.decision, reason=command_decision.reason))

        audit_path = audit.write(self.output_dir)
        return AgentSession(
            session_id=session_id,
            tool=self.tool,
            repo=self.repo,
            policy_pack=self.policy_pack,
            audit=audit,
            audit_path=audit_path,
        )
