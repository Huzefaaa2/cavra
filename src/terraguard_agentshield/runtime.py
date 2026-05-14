from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from terraguard_agentshield.policy_registry import PolicyRegistry


@dataclass(frozen=True)
class ActionDecision:
    decision: str
    reason: str | None = None


class RuntimeGuard:
    def __init__(self, policy_pack: str | None = None) -> None:
        self.registry = PolicyRegistry()
        self.policy = self.registry.load_policy(policy_pack or "ai-agent-baseline")
        self.sensitive_read = self._patterns("filesystem", "block_read")
        self.sensitive_write = self._patterns("filesystem", "block_write")
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
                return ActionDecision("block", f"Matched sensitive path policy: {pattern}")
        return ActionDecision("allow")

    def evaluate_command(self, command: str) -> ActionDecision:
        cleaned = command.strip()
        for pattern in self.command_block:
            if self._match_pattern(cleaned, pattern):
                return ActionDecision("block", f"Matched blocked command policy: {pattern}")
        for pattern in self.command_allow:
            if self._match_pattern(cleaned, pattern):
                return ActionDecision("allow")
        return ActionDecision("require_approval", "No allow rule matched; review required.")

    def evaluate_git_action(self, action: str, target: str | None = None) -> ActionDecision:
        if action == "push" and target:
            if target.endswith("main") or target.endswith("master"):
                return ActionDecision("block", "Direct push to protected branch is blocked.")
        return ActionDecision("allow")

    @staticmethod
    def _match_pattern(value: str, pattern: str) -> bool:
        regex = re.escape(pattern).replace("\\*\\*", ".*").replace("\\*", ".*")
        return re.fullmatch(regex, value) is not None
