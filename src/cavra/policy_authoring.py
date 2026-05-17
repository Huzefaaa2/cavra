from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from cavra.inventory import normalize_policy_rollout_record
from cavra.policy_engine import validate_policy


POLICY_SECTIONS = ("filesystem", "commands", "git", "mcp", "approvals", "evidence", "compliance")


def build_policy_pack_draft(payload: dict[str, Any]) -> dict[str, Any]:
    metadata = payload.get("metadata") if isinstance(payload.get("metadata"), dict) else {}
    pack_id = metadata.get("id") or payload.get("id")
    title = metadata.get("title") or payload.get("title")
    description = metadata.get("description") or payload.get("description")
    version = metadata.get("version") or payload.get("version") or datetime.now(timezone.utc).strftime("%Y.%m.%d")
    if not pack_id or not title or not description:
        raise ValueError("policy draft requires id, title, and description")
    policy: dict[str, Any] = {
        "metadata": {
            "id": str(pack_id),
            "title": str(title),
            "description": str(description),
            "version": str(version),
        }
    }
    inherits = metadata.get("inherits", payload.get("inherits"))
    if inherits:
        policy["metadata"]["inherits"] = inherits
    mode = metadata.get("mode", payload.get("mode"))
    if mode:
        policy["metadata"]["mode"] = mode
    for section in POLICY_SECTIONS:
        value = payload.get(section)
        if isinstance(value, dict):
            policy[section] = value
    errors = validate_policy(policy)
    return {
        "schema_version": "cavra.policy_pack.draft.v1",
        "product": "CAVRA",
        "valid": not errors,
        "errors": errors,
        "policy_pack": policy,
        "summary": summarize_policy(policy),
        "operator_notes": [
            "Draft generation is read-only and does not write to the policy directory.",
            "Commit reviewed policy YAML through repository change control before rollout.",
        ],
    }


def summarize_policy(policy: dict[str, Any]) -> dict[str, Any]:
    return {
        "policy_id": policy.get("metadata", {}).get("id"),
        "title": policy.get("metadata", {}).get("title"),
        "version": policy.get("metadata", {}).get("version"),
        "inherits": policy.get("metadata", {}).get("inherits"),
        "mode": policy.get("metadata", {}).get("mode", "enforce"),
        "rule_counts": {
            "filesystem": _count_rules(policy.get("filesystem", {})),
            "commands": _count_rules(policy.get("commands", {})),
            "git": _count_rules(policy.get("git", {})),
            "mcp": _count_rules(policy.get("mcp", {})),
            "approvals": _count_rules(policy.get("approvals", {})),
            "evidence": _count_rules(policy.get("evidence", {})),
            "compliance": _count_rules(policy.get("compliance", {})),
        },
    }


def build_rollout_change_plan(current: dict[str, Any] | None, requested: dict[str, Any]) -> dict[str, Any]:
    after = normalize_policy_rollout_record({**(current or {}), **requested})
    before = current or None
    changes = _rollout_changes(before, after)
    risk = _rollout_change_risk(before, after, changes)
    return {
        "schema_version": "cavra.policy_rollout.change_plan.v1",
        "product": "CAVRA",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "operation": "update" if current else "create",
        "risk": risk,
        "approval_required": risk in {"high", "critical"} or after.get("mode") in {"strict", "break_glass"},
        "before": before,
        "after": after,
        "changes": changes,
        "operator_notes": _rollout_operator_notes(risk),
    }


def production_readiness_report(
    *,
    oidc_configured: bool,
    rbac_configured: bool,
    cors_origins: list[str],
    evidence_artifact_root_configured: bool,
    policy_pack_count: int,
    store_status: dict[str, Any],
) -> dict[str, Any]:
    stores = store_status.get("items", []) if isinstance(store_status, dict) else []
    missing_stores = [item.get("name") for item in stores if not item.get("exists")]
    checks = [
        _check("oidc_configured", oidc_configured, "Console and approval actions validate signed OIDC tokens."),
        _check("rbac_configured", rbac_configured, "Repository-scoped RBAC policy is configured."),
        _check("cors_restricted", bool(cors_origins), "Allowed console origins are explicit."),
        _check("evidence_artifacts", evidence_artifact_root_configured, "Evidence artifact retrieval root is configured."),
        _check("policy_catalog", policy_pack_count > 0, f"{policy_pack_count} policy packs are discoverable."),
        _check("persistent_stores", not missing_stores, "Persistent API stores exist.", missing=missing_stores),
    ]
    return {
        "schema_version": "cavra.deployment.production_readiness.v1",
        "product": "CAVRA",
        "status": "ready" if all(item["status"] == "pass" for item in checks) else "needs_attention",
        "checks": checks,
        "store_summary": {
            "total": len(stores),
            "missing": missing_stores,
        },
        "operator_notes": [
            "Validate this report in the same environment that hosts the API and console.",
            "Keep restore operations in CLI or platform runbooks, not browser-facing endpoints.",
            "Attach this report to release evidence before enterprise pilots.",
        ],
    }


def _check(check_id: str, passed: bool, message: str, **extra: Any) -> dict[str, Any]:
    return {"id": check_id, "status": "pass" if passed else "warn", "message": message, **extra}


def _count_rules(value: object) -> int:
    if isinstance(value, list):
        return len(value)
    if isinstance(value, dict):
        return sum(_count_rules(item) for item in value.values())
    return 1 if value else 0


def _rollout_changes(before: dict[str, Any] | None, after: dict[str, Any]) -> list[dict[str, Any]]:
    if before is None:
        return [{"field": key, "before": None, "after": after.get(key)} for key in sorted(after)]
    changes = []
    for key in sorted(set(before) | set(after)):
        if before.get(key) != after.get(key):
            changes.append({"field": key, "before": before.get(key), "after": after.get(key)})
    return changes


def _rollout_change_risk(before: dict[str, Any] | None, after: dict[str, Any], changes: list[dict[str, Any]]) -> str:
    if after.get("mode") == "break_glass":
        return "critical"
    if before and before.get("mode") == "audit_only" and after.get("mode") in {"enforce", "strict"}:
        return "high"
    if after.get("mode") == "strict" or after.get("state") == "active":
        return "medium"
    if len(changes) > 3:
        return "medium"
    return "low"


def _rollout_operator_notes(risk: str) -> list[str]:
    notes = ["Review policy diff, evidence references, and repository owner before applying."]
    if risk in {"high", "critical"}:
        notes.append("Route this rollout change through security approval before enforcement.")
    return notes
