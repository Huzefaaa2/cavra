from __future__ import annotations

import json
import sqlite3
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


APPROVAL_STATES = {"pending", "approved", "denied", "expired", "break_glass"}


@dataclass(frozen=True)
class ExportResult:
    output_dir: Path
    files: list[Path]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def create_approval_request(
    decision: dict[str, Any],
    *,
    approver_group: str | None = None,
    requested_by: str = "ai-agent",
    ttl_hours: int = 24,
    routing_rules: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    decision_id = decision.get("decision_id")
    if not decision_id:
        raise ValueError("decision must include decision_id")
    rules = routing_rules if routing_rules is not None else default_routing_rules()
    group = approver_group or route_approver_group(decision, rules) or decision.get("approver_group")
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


def default_routing_rules() -> list[dict[str, Any]]:
    return [
        {"rule_id_prefix": "filesystem.write", "target_contains": "iam/", "approver_group": "IAM"},
        {"rule_id_prefix": "filesystem.write", "target_contains": ".github/workflows", "approver_group": "Platform Security"},
        {"rule_id_prefix": "commands.default", "severity": "medium", "approver_group": "Repository Owners"},
        {"rule_id_prefix": "commands.block", "target_contains": "terraform", "approver_group": "Cloud Security"},
        {"rule_id_prefix": "mcp.", "approver_group": "AI Governance"},
    ]


def load_routing_rules(path: Path | None) -> list[dict[str, Any]]:
    if path is None:
        return default_routing_rules()
    if not path.exists():
        raise FileNotFoundError(f"approval routing file not found: {path}")
    if path.suffix.lower() in {".yaml", ".yml"}:
        try:
            import yaml
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError("Install PyYAML to load YAML approval routing files.") from exc
        payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    else:
        payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        rules = payload
    elif isinstance(payload, dict):
        rules = payload.get("approval_routing", payload.get("routing_rules", payload))
    else:
        raise ValueError("approval routing file must contain a list of rules")
    if not isinstance(rules, list):
        raise ValueError("approval routing file must contain a list of rules")
    for rule in rules:
        if not isinstance(rule, dict) or not rule.get("approver_group"):
            raise ValueError("each approval routing rule must include approver_group")
    return rules


def route_approver_group(decision: dict[str, Any], routing_rules: list[dict[str, Any]] | None = None) -> str | None:
    rules = routing_rules if routing_rules is not None else default_routing_rules()
    for rule in rules:
        if _route_rule_matches(decision, rule):
            return str(rule["approver_group"])
    return None


def _route_rule_matches(decision: dict[str, Any], rule: dict[str, Any]) -> bool:
    for key in ("rule_id", "action_type", "severity", "policy_pack"):
        if rule.get(key) and decision.get(key) != rule[key]:
            return False
    if rule.get("rule_id_prefix") and not str(decision.get("rule_id", "")).startswith(str(rule["rule_id_prefix"])):
        return False
    if rule.get("target_contains") and str(rule["target_contains"]) not in str(decision.get("target", "")):
        return False
    return True


def actor_context_from_claims(claims: dict[str, Any], *, rbac_rules: dict[str, Any] | None = None) -> dict[str, Any]:
    groups = claims.get("groups") or claims.get("roles") or []
    if isinstance(groups, str):
        groups = [groups]
    email = claims.get("email") or claims.get("preferred_username") or claims.get("sub") or "unknown"
    configured = rbac_rules or {}
    mapped_groups = set(groups)
    for source, target in configured.get("group_mappings", {}).items():
        if source in groups:
            mapped_groups.add(target)
    return {
        "actor": email,
        "subject": claims.get("sub"),
        "groups": sorted(str(item) for item in mapped_groups),
        "issuer": claims.get("iss"),
    }


def actor_can_decide(actor_context: dict[str, Any], approval: dict[str, Any], *, action: str = "approve") -> bool:
    if action == "expire" and "system" in actor_context.get("groups", []):
        return True
    if approval.get("break_glass") and "Change Advisory Board" not in actor_context.get("groups", []):
        return False
    return approval.get("approver_group") in actor_context.get("groups", [])


def apply_approval_decision(
    approval: dict[str, Any],
    *,
    state: str,
    actor: str,
    reason: str,
    external_ref: str | None = None,
    actor_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if state not in {"approved", "denied", "expired"}:
        raise ValueError("state must be approved, denied, or expired")
    if approval.get("state") != "pending":
        raise ValueError("only pending approvals can be changed")
    if not actor:
        raise ValueError("actor is required")
    if not reason:
        raise ValueError("reason is required")
    if actor_context and not actor_can_decide(actor_context, approval, action=state):
        raise ValueError("actor is not authorized for approval group")
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


def build_approval_notification_payloads(approval: dict[str, Any]) -> dict[str, Any]:
    summary = approval_summary(approval)
    title = f"CAVRA approval {approval.get('state')} for {approval.get('decision_id')}"
    reason = approval.get("decision_reason") or approval.get("break_glass_reason") or approval.get("decision", {}).get("reason")
    return {
        "slack": {
            "text": title,
            "blocks": [
                {"type": "header", "text": {"type": "plain_text", "text": title}},
                {
                    "type": "section",
                    "fields": [
                        {"type": "mrkdwn", "text": f"*Approver group:* {approval.get('approver_group')}"},
                        {"type": "mrkdwn", "text": f"*State:* {approval.get('state')}"},
                        {"type": "mrkdwn", "text": f"*Requested by:* {approval.get('requested_by')}"},
                        {"type": "mrkdwn", "text": f"*External ref:* {approval.get('external_ref', 'n/a')}"},
                    ],
                },
            ],
        },
        "teams": {
            "@type": "MessageCard",
            "@context": "https://schema.org/extensions",
            "summary": title,
            "themeColor": "E0A800" if approval.get("state") == "pending" else "2E7D32",
            "sections": [
                {
                    "activityTitle": title,
                    "facts": [
                        {"name": "Approver group", "value": str(approval.get("approver_group"))},
                        {"name": "State", "value": str(approval.get("state"))},
                        {"name": "Reason", "value": str(reason or "n/a")},
                    ],
                }
            ],
        },
        "jira": {
            "fields": {
                "summary": title,
                "description": json.dumps(summary, indent=2, sort_keys=True),
                "labels": ["cavra", "ai-agent-approval", str(approval.get("state"))],
            }
        },
        "servicenow": {
            "short_description": title,
            "description": json.dumps(summary, indent=2, sort_keys=True),
            "assignment_group": approval.get("approver_group"),
            "correlation_id": approval.get("correlation_id"),
        },
        "webhook": {
            "schema_version": "cavra.approval.notification.v1",
            "product": "CAVRA",
            "event_type": f"cavra.approval.{approval.get('state')}",
            "timestamp": utc_now(),
            "payload": approval,
        },
    }


def build_provider_request_specs(approval: dict[str, Any], *, endpoints: dict[str, str] | None = None) -> dict[str, Any]:
    payloads = build_approval_notification_payloads(approval)
    endpoints = endpoints or {}
    return {
        "slack": {
            "method": "POST",
            "url": endpoints.get("slack", "https://hooks.slack.com/services/REPLACE_ME"),
            "headers": {"content-type": "application/json"},
            "body": payloads["slack"],
        },
        "teams": {
            "method": "POST",
            "url": endpoints.get("teams", "https://outlook.office.com/webhook/REPLACE_ME"),
            "headers": {"content-type": "application/json"},
            "body": payloads["teams"],
        },
        "jira": {
            "method": "POST",
            "url": endpoints.get("jira", "https://jira.example/rest/api/3/issue"),
            "headers": {"content-type": "application/json", "authorization": "Bearer ${JIRA_TOKEN}"},
            "body": payloads["jira"],
        },
        "servicenow": {
            "method": "POST",
            "url": endpoints.get("servicenow", "https://instance.service-now.com/api/now/table/change_request"),
            "headers": {"content-type": "application/json", "authorization": "Bearer ${SERVICENOW_TOKEN}"},
            "body": payloads["servicenow"],
        },
        "webhook": {
            "method": "POST",
            "url": endpoints.get("webhook", "https://approval-webhook.example/cavra"),
            "headers": {"content-type": "application/json"},
            "body": payloads["webhook"],
        },
    }


def export_approval_notification_payloads(
    approval: dict[str, Any],
    output_dir: Path,
    *,
    provider: str = "all",
) -> ExportResult:
    payloads = build_approval_notification_payloads(approval)
    providers = set(payloads) if provider == "all" else {provider}
    unknown = providers - set(payloads)
    if unknown:
        raise ValueError(f"unknown approval notification provider: {', '.join(sorted(unknown))}")
    output_dir.mkdir(parents=True, exist_ok=True)
    files: list[Path] = []
    for item in sorted(providers):
        path = output_dir / f"{item}-approval-payload.json"
        path.write_text(json.dumps(payloads[item], indent=2, sort_keys=True) + "\n", encoding="utf-8")
        files.append(path)
    return ExportResult(output_dir=output_dir, files=files)


def export_provider_request_specs(
    approval: dict[str, Any],
    output_dir: Path,
    *,
    provider: str = "all",
    endpoints: dict[str, str] | None = None,
) -> ExportResult:
    specs = build_provider_request_specs(approval, endpoints=endpoints)
    providers = set(specs) if provider == "all" else {provider}
    unknown = providers - set(specs)
    if unknown:
        raise ValueError(f"unknown approval provider: {', '.join(sorted(unknown))}")
    output_dir.mkdir(parents=True, exist_ok=True)
    files: list[Path] = []
    for item in sorted(providers):
        path = output_dir / f"{item}-approval-request.json"
        path.write_text(json.dumps(specs[item], indent=2, sort_keys=True) + "\n", encoding="utf-8")
        files.append(path)
    return ExportResult(output_dir=output_dir, files=files)


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
        routing_rules: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        return self.upsert(
            create_approval_request(
                decision,
                approver_group=approver_group,
                requested_by=requested_by,
                ttl_hours=ttl_hours,
                routing_rules=routing_rules,
            )
        )

    def decide(
        self,
        approval_id: str,
        *,
        state: str,
        actor: str,
        reason: str,
        external_ref: str | None = None,
        actor_context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
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
                actor_context=actor_context,
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


class SQLiteApprovalStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS approvals (
                    approval_id TEXT PRIMARY KEY,
                    decision_id TEXT NOT NULL,
                    session_id TEXT,
                    state TEXT NOT NULL,
                    approver_group TEXT NOT NULL,
                    requested_by TEXT,
                    requested_at TEXT NOT NULL,
                    expires_at TEXT NOT NULL,
                    decided_by TEXT,
                    decided_at TEXT,
                    external_ref TEXT,
                    break_glass INTEGER NOT NULL DEFAULT 0,
                    payload TEXT NOT NULL
                )
                """
            )
            connection.execute("CREATE INDEX IF NOT EXISTS idx_approvals_state ON approvals (state)")
            connection.execute("CREATE INDEX IF NOT EXISTS idx_approvals_group ON approvals (approver_group)")
            connection.execute("CREATE INDEX IF NOT EXISTS idx_approvals_requested_at ON approvals (requested_at)")

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
        clauses: list[str] = []
        params: list[Any] = []
        if state:
            clauses.append("state = ?")
            params.append(state)
        if approver_group:
            clauses.append("approver_group = ?")
            params.append(approver_group)
        where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        with self._connect() as connection:
            total = connection.execute(f"SELECT COUNT(*) AS count FROM approvals {where}", params).fetchone()["count"]
            rows = connection.execute(
                f"""
                SELECT payload FROM approvals
                {where}
                ORDER BY requested_at DESC, approval_id ASC
                LIMIT ? OFFSET ?
                """,
                [*params, limit, offset],
            ).fetchall()
        return {
            "items": [json.loads(row["payload"]) for row in rows],
            "total": total,
            "limit": limit,
            "offset": offset,
        }

    def get(self, approval_id: str) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute("SELECT payload FROM approvals WHERE approval_id = ?", (approval_id,)).fetchone()
        return json.loads(row["payload"]) if row else None

    def upsert(self, approval: dict[str, Any]) -> dict[str, Any]:
        approval_id = approval.get("approval_id")
        if not approval_id:
            raise ValueError("approval must include approval_id")
        state = approval.get("state")
        if state not in APPROVAL_STATES:
            raise ValueError(f"unsupported approval state: {state}")
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO approvals (
                    approval_id, decision_id, session_id, state, approver_group, requested_by, requested_at,
                    expires_at, decided_by, decided_at, external_ref, break_glass, payload
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(approval_id) DO UPDATE SET
                    decision_id=excluded.decision_id,
                    session_id=excluded.session_id,
                    state=excluded.state,
                    approver_group=excluded.approver_group,
                    requested_by=excluded.requested_by,
                    requested_at=excluded.requested_at,
                    expires_at=excluded.expires_at,
                    decided_by=excluded.decided_by,
                    decided_at=excluded.decided_at,
                    external_ref=excluded.external_ref,
                    break_glass=excluded.break_glass,
                    payload=excluded.payload
                """,
                (
                    approval_id,
                    approval.get("decision_id"),
                    approval.get("session_id"),
                    approval.get("state"),
                    approval.get("approver_group"),
                    approval.get("requested_by"),
                    approval.get("requested_at"),
                    approval.get("expires_at"),
                    approval.get("decided_by"),
                    approval.get("decided_at"),
                    approval.get("external_ref"),
                    1 if approval.get("break_glass") else 0,
                    json.dumps(approval, sort_keys=True),
                ),
            )
        return approval

    def create_request(
        self,
        decision: dict[str, Any],
        *,
        approver_group: str | None = None,
        requested_by: str = "ai-agent",
        ttl_hours: int = 24,
        routing_rules: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        return self.upsert(
            create_approval_request(
                decision,
                approver_group=approver_group,
                requested_by=requested_by,
                ttl_hours=ttl_hours,
                routing_rules=routing_rules,
            )
        )

    def decide(
        self,
        approval_id: str,
        *,
        state: str,
        actor: str,
        reason: str,
        external_ref: str | None = None,
        actor_context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
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
                actor_context=actor_context,
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
