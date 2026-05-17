from __future__ import annotations

import json
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


APPROVAL_STATES = {"pending", "approved", "denied", "expired", "break_glass"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def create_approval_request(
    decision: dict[str, Any],
    *,
    approver_group: str | None = None,
    requested_by: str = "ai-agent",
    ttl_hours: int = 24,
) -> dict[str, Any]:
    decision_id = decision.get("decision_id")
    if not decision_id:
        raise ValueError("decision must include decision_id")
    group = approver_group or decision.get("approver_group")
    if not group:
        raise ValueError("approval request must include approver_group")
    created_at = utc_now()
    expires_at = (datetime.now(timezone.utc) + timedelta(hours=max(1, ttl_hours))).isoformat()
    approval_id = f"apr_{uuid.uuid4().hex[:12]}"
    return {
        "schema_version": "cavra.approval.v1",
        "product": "CAVRA",
        "approval_id": approval_id,
        "decision_id": decision_id,
        "session_id": decision.get("session_id", "local"),
        "correlation_id": decision.get("correlation_id"),
        "state": "pending",
        "approver_group": group,
        "requested_by": requested_by,
        "requested_at": created_at,
        "expires_at": expires_at,
        "decision": decision,
        "history": [
            {
                "event": "requested",
                "actor": requested_by,
                "timestamp": created_at,
                "reason": decision.get("reason"),
            }
        ],
        "evidence_refs": [f"approval://{approval_id}", *decision.get("evidence_refs", [])],
    }


def apply_approval_decision(
    approval: dict[str, Any],
    *,
    state: str,
    actor: str,
    reason: str,
    external_ref: str | None = None,
) -> dict[str, Any]:
    if state not in {"approved", "denied", "expired"}:
        raise ValueError("state must be approved, denied, or expired")
    if approval.get("state") != "pending":
        raise ValueError("only pending approvals can be changed")
    if not actor:
        raise ValueError("actor is required")
    if not reason:
        raise ValueError("reason is required")
    updated = {**approval}
    updated["state"] = state
    updated["decided_by"] = actor
    updated["decided_at"] = utc_now()
    updated["decision_reason"] = reason
    if external_ref:
        updated["external_ref"] = external_ref
    history = list(updated.get("history", []))
    history.append(
        {
            "event": state,
            "actor": actor,
            "timestamp": updated["decided_at"],
            "reason": reason,
            "external_ref": external_ref,
        }
    )
    updated["history"] = history
    return updated


def create_break_glass_approval(
    *,
    decision: dict[str, Any],
    actor: str,
    reason: str,
    approver_group: str = "Change Advisory Board",
    external_ref: str | None = None,
    ttl_hours: int = 4,
) -> dict[str, Any]:
    if not actor:
        raise ValueError("actor is required")
    if not reason:
        raise ValueError("break-glass reason is required")
    approval = create_approval_request(
        decision,
        approver_group=approver_group,
        requested_by=actor,
        ttl_hours=ttl_hours,
    )
    approved = apply_approval_decision(
        approval,
        state="approved",
        actor=actor,
        reason=reason,
        external_ref=external_ref,
    )
    approved["state"] = "break_glass"
    approved["break_glass"] = True
    approved["break_glass_reason"] = reason
    approved["expires_at"] = (datetime.now(timezone.utc) + timedelta(hours=max(1, ttl_hours))).isoformat()
    approved["history"].append(
        {
            "event": "break_glass",
            "actor": actor,
            "timestamp": utc_now(),
            "reason": reason,
            "external_ref": external_ref,
        }
    )
    return approved


def approval_summary(approval: dict[str, Any]) -> dict[str, Any]:
    return {
        "approval_id": approval.get("approval_id"),
        "decision_id": approval.get("decision_id"),
        "session_id": approval.get("session_id"),
        "state": approval.get("state"),
        "approver_group": approval.get("approver_group"),
        "requested_by": approval.get("requested_by"),
        "requested_at": approval.get("requested_at"),
        "expires_at": approval.get("expires_at"),
        "decided_by": approval.get("decided_by"),
        "decided_at": approval.get("decided_at"),
        "external_ref": approval.get("external_ref"),
        "break_glass": approval.get("break_glass", False),
        "evidence_refs": approval.get("evidence_refs", []),
    }


def attach_approval_to_decision(decision: dict[str, Any], approval: dict[str, Any]) -> dict[str, Any]:
    updated = {**decision}
    updated["approval"] = approval_summary(approval)
    evidence_refs = list(updated.get("evidence_refs", []))
    for ref in approval.get("evidence_refs", []):
        if ref not in evidence_refs:
            evidence_refs.append(ref)
    updated["evidence_refs"] = evidence_refs
    return updated


class ApprovalStore:
    def __init__(self, path: Path) -> None:
        self.path = path

    def list(
        self,
        *,
        state: str | None = None,
        approver_group: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> dict[str, Any]:
        limit = max(1, min(limit, 500))
        offset = max(0, offset)
        items = self._load()
        if state:
            items = [item for item in items if item.get("state") == state]
        if approver_group:
            items = [item for item in items if item.get("approver_group") == approver_group]
        items = sorted(items, key=lambda item: str(item.get("requested_at", "")), reverse=True)
        return {
            "items": items[offset : offset + limit],
            "total": len(items),
            "limit": limit,
            "offset": offset,
        }

    def get(self, approval_id: str) -> dict[str, Any] | None:
        for approval in self._load():
            if approval.get("approval_id") == approval_id:
                return approval
        return None

    def upsert(self, approval: dict[str, Any]) -> dict[str, Any]:
        approval_id = approval.get("approval_id")
        if not approval_id:
            raise ValueError("approval must include approval_id")
        state = approval.get("state")
        if state not in APPROVAL_STATES:
            raise ValueError(f"unsupported approval state: {state}")
        items = [item for item in self._load() if item.get("approval_id") != approval_id]
        items.append(approval)
        self._write(items)
        return approval

    def create_request(
        self,
        decision: dict[str, Any],
        *,
        approver_group: str | None = None,
        requested_by: str = "ai-agent",
        ttl_hours: int = 24,
    ) -> dict[str, Any]:
        return self.upsert(
            create_approval_request(
                decision,
                approver_group=approver_group,
                requested_by=requested_by,
                ttl_hours=ttl_hours,
            )
        )

    def decide(self, approval_id: str, *, state: str, actor: str, reason: str, external_ref: str | None = None) -> dict[str, Any]:
        approval = self.get(approval_id)
        if approval is None:
            raise KeyError(approval_id)
        return self.upsert(
            apply_approval_decision(
                approval,
                state=state,
                actor=actor,
                reason=reason,
                external_ref=external_ref,
            )
        )

    def break_glass(
        self,
        *,
        decision: dict[str, Any],
        actor: str,
        reason: str,
        approver_group: str = "Change Advisory Board",
        external_ref: str | None = None,
        ttl_hours: int = 4,
    ) -> dict[str, Any]:
        return self.upsert(
            create_break_glass_approval(
                decision=decision,
                actor=actor,
                reason=reason,
                approver_group=approver_group,
                external_ref=external_ref,
                ttl_hours=ttl_hours,
            )
        )

    def _load(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        payload = json.loads(self.path.read_text(encoding="utf-8"))
        return payload.get("items", [])

    def _write(self, items: list[dict[str, Any]]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps({"items": items}, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
