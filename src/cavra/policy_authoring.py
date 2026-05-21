from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from cavra.approvals import approval_summary
from cavra.inventory import normalize_policy_rollout_record
from cavra.policy_engine import diff_policies, validate_policy, verify_policy_signature, write_policy_signature
from cavra.policy_registry import PolicyRegistry


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


def policy_content_digest(policy: dict[str, Any]) -> str:
    canonical = json.dumps(policy, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return f"sha256:{hashlib.sha256(canonical).hexdigest()}"


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


def build_policy_pack_publish_plan(payload: dict[str, Any], current_policy: dict[str, Any] | None = None) -> dict[str, Any]:
    draft = build_policy_pack_draft(payload)
    policy = draft["policy_pack"]
    pack_id = str(policy.get("metadata", {}).get("id", ""))
    digest = policy_content_digest(policy)
    diff = diff_policies(current_policy, policy).to_dict() if current_policy else {"added": [], "removed": [], "changed": []}
    risk = _policy_publish_risk(current_policy, diff)
    return {
        "schema_version": "cavra.policy_pack.publish_plan.v1",
        "product": "CAVRA",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "operation": "update" if current_policy else "create",
        "valid": draft["valid"],
        "errors": draft["errors"],
        "approval_required": True,
        "risk": risk,
        "policy_id": pack_id,
        "policy_digest": digest,
        "target_path": f"policies/{pack_id}/policy.yaml",
        "summary": draft["summary"],
        "diff": diff,
        "operator_notes": _policy_publish_operator_notes(risk, draft["valid"]),
    }


def build_policy_publish_decision(
    publish_plan: dict[str, Any],
    *,
    requested_by: str,
    approver_group: str = "Platform Security",
    repository: str | None = None,
) -> dict[str, Any]:
    if not publish_plan.get("valid"):
        raise ValueError("policy publish request requires a valid draft")
    policy_id = str(publish_plan.get("policy_id", ""))
    digest = str(publish_plan.get("policy_digest", ""))
    return {
        "decision_id": f"policy_publish:{policy_id}:{digest.removeprefix('sha256:')[:12]}",
        "session_id": "policy-authoring",
        "agent_id": "policy-authoring-console",
        "actor": requested_by,
        "repository": repository or "policy-catalog",
        "action_type": "policy_publish",
        "target": publish_plan.get("target_path"),
        "decision": "require_approval",
        "severity": publish_plan.get("risk", "high"),
        "policy_pack": policy_id,
        "rule_id": "policy.publish.requires_approval",
        "reason": "Policy pack write-back requires approval and signature before publishing.",
        "approver_group": approver_group,
        "policy_id": policy_id,
        "policy_digest": digest,
        "operation": publish_plan.get("operation"),
        "evidence_refs": [f"policy-draft://{policy_id}/{digest.removeprefix('sha256:')[:12]}"],
    }


def publish_policy_pack(
    payload: dict[str, Any],
    approval: dict[str, Any],
    *,
    policy_root: Path | None = None,
    signer: str = "policy-publisher",
    key: str | None = None,
    actor: str | None = None,
) -> dict[str, Any]:
    draft = build_policy_pack_draft(payload)
    if not draft["valid"]:
        raise ValueError("policy draft must be valid before publishing")
    policy = draft["policy_pack"]
    pack_id = str(policy.get("metadata", {}).get("id", ""))
    _validate_publish_pack_id(pack_id)
    digest = policy_content_digest(policy)
    _validate_policy_publish_approval(approval, policy_id=pack_id, policy_digest=digest)
    registry = PolicyRegistry(policy_root)
    registry.save_policy(pack_id, policy)
    policy_path = registry.root / pack_id / "policy.yaml"
    signature_path = write_policy_signature(policy_path, signer=signer, key=key)
    verified, message = verify_policy_signature(policy_path, signature_path=signature_path, key=key)
    if not verified:
        raise ValueError(f"published policy signature verification failed: {message}")
    return {
        "schema_version": "cavra.policy_pack.publish_result.v1",
        "product": "CAVRA",
        "status": "published",
        "published_at": datetime.now(timezone.utc).isoformat(),
        "published_by": actor or signer,
        "policy_id": pack_id,
        "policy_digest": digest,
        "policy_path": str(policy_path),
        "signature_path": str(signature_path),
        "signature_verified": verified,
        "signature_message": message,
        "approval": approval_summary(approval),
        "summary": summarize_policy(policy),
        "operator_notes": [
            "Published policy was schema-validated, approval-bound by digest, written to policy.yaml, and signed.",
            "Commit the policy file and signature through repository change control.",
        ],
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
    go_backend_readiness: dict[str, Any] | None = None,
    go_deployment_readiness: dict[str, Any] | None = None,
    go_promotion_readiness: dict[str, Any] | None = None,
    go_rollback_readiness: dict[str, Any] | None = None,
    go_rollback_rehearsal: dict[str, Any] | None = None,
    go_rollback_drill_history: dict[str, Any] | None = None,
) -> dict[str, Any]:
    stores = store_status.get("items", []) if isinstance(store_status, dict) else []
    missing_stores = [item.get("name") for item in stores if not item.get("exists")]
    go_backend_status = (go_backend_readiness or {}).get("status", "disabled")
    go_backend_mode = (go_backend_readiness or {}).get("mode", "disabled")
    go_deployment_status = (go_deployment_readiness or {}).get("status", "not_configured")
    go_deployment_ready = (
        go_deployment_status == "ready"
        or (go_backend_mode == "disabled" and go_deployment_status == "not_configured")
    )
    go_promotion_status = (go_promotion_readiness or {}).get("status", "not_requested")
    go_rollback_status = (go_rollback_readiness or {}).get("status", "not_requested")
    go_rehearsal_status = (go_rollback_rehearsal or {}).get("status", "not_requested")
    go_drill_status = (go_rollback_drill_history or {}).get("status", "not_requested")
    checks = [
        _check("oidc_configured", oidc_configured, "Console and approval actions validate signed OIDC tokens."),
        _check("rbac_configured", rbac_configured, "Repository-scoped RBAC policy is configured."),
        _check("cors_restricted", bool(cors_origins), "Allowed console origins are explicit."),
        _check("evidence_artifacts", evidence_artifact_root_configured, "Evidence artifact retrieval root is configured."),
        _check("policy_catalog", policy_pack_count > 0, f"{policy_pack_count} policy packs are discoverable."),
        _check("persistent_stores", not missing_stores, "Persistent API stores exist.", missing=missing_stores),
        _check(
            "go_backend_pilot",
            go_backend_status in {"disabled", "ready"},
            "Optional Go backend pilot is disabled or ready with Python fallback and parity gate evidence.",
            mode=go_backend_mode,
            go_backend_status=go_backend_status,
        ),
        _check(
            "go_backend_deployment_paths",
            go_deployment_ready,
            "Go backend CI runner and workstation deployment paths are ready when the pilot is enabled.",
            mode=go_backend_mode,
            go_deployment_status=go_deployment_status,
        ),
        _check(
            "go_backend_promotion_gate",
            go_promotion_status in {"not_requested", "ready"},
            "Promoted Go backend mode requires runtime, deployment, and audited parity evidence.",
            mode=go_backend_mode,
            go_promotion_status=go_promotion_status,
        ),
        _check(
            "go_backend_rollback_controls",
            go_rollback_status in {"not_requested", "ready"},
            "Promoted Go backend mode requires an approved rollback plan back to Python-only mode.",
            mode=go_backend_mode,
            go_rollback_status=go_rollback_status,
        ),
        _check(
            "go_backend_rollback_rehearsal",
            go_rehearsal_status in {"not_requested", "ready"},
            "Promoted Go backend mode requires rollback rehearsal evidence and dashboard visibility.",
            mode=go_backend_mode,
            go_rollback_rehearsal_status=go_rehearsal_status,
        ),
        _check(
            "go_backend_rollback_drill_history",
            go_drill_status in {"not_requested", "ready"},
            "Promoted Go backend mode requires fresh operational drill history for returning to Python-only mode.",
            mode=go_backend_mode,
            go_rollback_drill_history_status=go_drill_status,
        ),
    ]
    return {
        "schema_version": "cavra.deployment.production_readiness.v1",
        "product": "CAVRA",
        "status": "ready" if all(item["status"] == "pass" for item in checks) else "needs_attention",
        "checks": checks,
        "go_backend_pilot": go_backend_readiness
        or {
            "schema_version": "cavra.go-backend-pilot.readiness.v1",
            "mode": "disabled",
            "status": "disabled",
            "checks": [],
        },
        "go_backend_deployment": go_deployment_readiness
        or {
            "schema_version": "cavra.go-backend-pilot.deployment-readiness.v1",
            "mode": "disabled",
            "status": "not_configured",
            "checks": [],
            "ci_runner_targets": [],
            "workstation_targets": [],
            "channels": [],
        },
        "go_backend_promotion": go_promotion_readiness
        or {
            "schema_version": "cavra.go-backend-pilot.promotion-readiness.v1",
            "mode": "disabled",
            "status": "not_requested",
            "checks": [],
        },
        "go_backend_rollback": go_rollback_readiness
        or {
            "schema_version": "cavra.go-backend-pilot.rollback-readiness.v1",
            "mode": "disabled",
            "status": "not_requested",
            "checks": [],
        },
        "go_backend_rollback_rehearsal": go_rollback_rehearsal
        or {
            "schema_version": "cavra.go-backend-pilot.rollback-rehearsal.v1",
            "mode": "disabled",
            "status": "not_requested",
            "checks": [],
        },
        "go_backend_rollback_drill_history": go_rollback_drill_history
        or {
            "schema_version": "cavra.go-backend-pilot.rollback-drill-history.v1",
            "mode": "disabled",
            "status": "not_requested",
            "checks": [],
        },
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


def _policy_publish_risk(current_policy: dict[str, Any] | None, diff: dict[str, list[str]]) -> str:
    if current_policy is None:
        return "high"
    if diff.get("removed"):
        return "critical"
    sensitive_prefixes = ("approvals.", "git.", "mcp.", "evidence.", "compliance.")
    if any(item.startswith(sensitive_prefixes) for item in [*diff.get("added", []), *diff.get("changed", [])]):
        return "high"
    if diff.get("added") or diff.get("changed"):
        return "medium"
    return "low"


def _policy_publish_operator_notes(risk: str, valid: bool) -> list[str]:
    notes = [
        "Publishing writes policy.yaml and policy.yaml.sig.json only after approval.",
        "The approval request is bound to the draft policy digest to prevent approving one draft and publishing another.",
    ]
    if not valid:
        notes.insert(0, "Fix schema validation errors before requesting approval.")
    if risk in {"high", "critical"}:
        notes.append("Security or platform approval is required before write-back.")
    return notes


def _validate_policy_publish_approval(approval: dict[str, Any], *, policy_id: str, policy_digest: str) -> None:
    if approval.get("state") not in {"approved", "break_glass"}:
        raise ValueError("policy publish approval must be approved before write-back")
    decision = approval.get("decision", {})
    if not isinstance(decision, dict):
        raise ValueError("policy publish approval must include a decision payload")
    if decision.get("action_type") != "policy_publish":
        raise ValueError("approval is not for policy publish")
    if decision.get("policy_id") != policy_id or decision.get("policy_digest") != policy_digest:
        raise ValueError("approval does not match policy draft digest")


def _validate_publish_pack_id(pack_id: str) -> None:
    if not pack_id or pack_id in {".", ".."} or Path(pack_id).name != pack_id:
        raise ValueError("policy id is not safe for write-back")
