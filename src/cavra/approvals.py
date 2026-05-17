from __future__ import annotations

import json
import os
import sqlite3
import time
import uuid
from base64 import urlsafe_b64decode
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib import error, request


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


def load_rbac_rules(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    return _load_object_file(path, "approval RBAC policy")


def load_oidc_config(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    config = _load_object_file(path, "approval OIDC config")
    jwks_path = config.get("jwks_path")
    if jwks_path and "jwks" not in config:
        resolved_jwks_path = Path(jwks_path)
        if not resolved_jwks_path.is_absolute():
            resolved_jwks_path = path.parent / resolved_jwks_path
        config["jwks"] = _load_object_file(resolved_jwks_path, "approval OIDC JWKS")
    if not config.get("issuer") or not config.get("audience") or not config.get("jwks"):
        raise ValueError("approval OIDC config must include issuer, audience, and jwks or jwks_path")
    return config


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


def _load_object_file(path: Path, description: str) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"{description} file not found: {path}")
    if path.suffix.lower() in {".yaml", ".yml"}:
        try:
            import yaml
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError(f"Install PyYAML to load YAML {description} files.") from exc
        payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    else:
        payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{description} file must contain an object")
    return payload


def actor_context_from_claims(claims: dict[str, Any], *, rbac_rules: dict[str, Any] | None = None) -> dict[str, Any]:
    groups = claims.get("groups") or claims.get("roles") or []
    if isinstance(groups, str):
        groups = [groups]
    email = claims.get("email") or claims.get("preferred_username") or claims.get("sub") or "unknown"
    configured = _rbac_policy(rbac_rules or {})
    mapped_groups = set(groups)
    for source, target in configured.get("group_mappings", {}).items():
        if source in groups:
            mapped_groups.add(target)
    return {
        "actor": email,
        "subject": claims.get("sub"),
        "groups": sorted(str(item) for item in mapped_groups),
        "issuer": claims.get("iss"),
        "repository": claims.get("repository") or claims.get("repo"),
    }


def actor_context_from_oidc_token(token: str, oidc_config: dict[str, Any], *, rbac_rules: dict[str, Any] | None = None) -> dict[str, Any]:
    claims = validate_oidc_token(token, oidc_config)
    return actor_context_from_claims(claims, rbac_rules=rbac_rules)


def validate_oidc_token(token: str, oidc_config: dict[str, Any]) -> dict[str, Any]:
    try:
        header_b64, payload_b64, signature_b64 = token.split(".")
    except ValueError as exc:
        raise ValueError("OIDC token must be a compact JWT") from exc
    header = json.loads(_b64url_decode(header_b64))
    claims = json.loads(_b64url_decode(payload_b64))
    if header.get("alg") != "RS256":
        raise ValueError("OIDC token must use RS256")
    if claims.get("iss") != oidc_config.get("issuer"):
        raise ValueError("OIDC token issuer is not trusted")
    audience = claims.get("aud")
    expected_audience = oidc_config.get("audience")
    audiences = audience if isinstance(audience, list) else [audience]
    if expected_audience not in audiences:
        raise ValueError("OIDC token audience is not trusted")
    now = int(time.time())
    leeway = int(oidc_config.get("leeway_seconds", 60))
    if claims.get("exp") is None or int(claims["exp"]) < now - leeway:
        raise ValueError("OIDC token is expired")
    if claims.get("nbf") is not None and int(claims["nbf"]) > now + leeway:
        raise ValueError("OIDC token is not yet valid")
    signing_input = f"{header_b64}.{payload_b64}".encode("ascii")
    public_key = _public_key_from_jwks(oidc_config["jwks"], header.get("kid"))
    _verify_rs256(public_key, signing_input, _b64url_decode(signature_b64))
    return claims


def _b64url_decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return urlsafe_b64decode((value + padding).encode("ascii"))


def _public_key_from_jwks(jwks: dict[str, Any], kid: str | None):
    keys = jwks.get("keys", [])
    if not isinstance(keys, list):
        raise ValueError("OIDC JWKS must include keys")
    for key in keys:
        if kid and key.get("kid") != kid:
            continue
        if key.get("kty") != "RSA":
            continue
        try:
            from cryptography.hazmat.primitives.asymmetric import rsa
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError("Install cryptography to validate OIDC JWT signatures.") from exc
        n = int.from_bytes(_b64url_decode(str(key["n"])), "big")
        e = int.from_bytes(_b64url_decode(str(key["e"])), "big")
        return rsa.RSAPublicNumbers(e, n).public_key()
    raise ValueError("OIDC token signing key was not found in JWKS")


def _verify_rs256(public_key: Any, signing_input: bytes, signature: bytes) -> None:
    try:
        from cryptography.exceptions import InvalidSignature
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.asymmetric import padding
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("Install cryptography to validate OIDC JWT signatures.") from exc
    try:
        public_key.verify(signature, signing_input, padding.PKCS1v15(), hashes.SHA256())
    except InvalidSignature as exc:
        raise ValueError("OIDC token signature is invalid") from exc


def _repository_rbac_allows(
    actor_context: dict[str, Any],
    approval: dict[str, Any],
    *,
    action: str,
    rbac_rules: dict[str, Any],
) -> bool:
    policy = _rbac_policy(rbac_rules)
    rules = policy.get("repository_permissions", policy.get("repositories", []))
    if not isinstance(rules, list):
        return False
    actor_groups = set(actor_context.get("groups", []))
    repository = _approval_repository(approval)
    for rule in rules:
        if not isinstance(rule, dict):
            continue
        if rule.get("repository") and rule.get("repository") != repository:
            continue
        if rule.get("approver_group") and rule.get("approver_group") != approval.get("approver_group"):
            continue
        actions = {_decision_action_alias(str(item)) for item in rule.get("actions", ["approved", "denied"])}
        if _decision_action_alias(action) not in actions:
            continue
        allowed_groups = set(str(item) for item in rule.get("groups", []))
        if actor_groups & allowed_groups:
            return True
    return False


def repository_permissions_for_actor(actor_context: dict[str, Any], rbac_rules: dict[str, Any]) -> list[dict[str, Any]]:
    policy = _rbac_policy(rbac_rules)
    rules = policy.get("repository_permissions", policy.get("repositories", []))
    if not isinstance(rules, list):
        return []
    actor_groups = set(actor_context.get("groups", []))
    permissions = []
    for rule in rules:
        if not isinstance(rule, dict):
            continue
        allowed_groups = set(str(item) for item in rule.get("groups", []))
        if not actor_groups & allowed_groups:
            continue
        permissions.append(
            {
                "repository": rule.get("repository", "*"),
                "approver_group": rule.get("approver_group", "*"),
                "actions": sorted(_decision_action_alias(str(item)) for item in rule.get("actions", ["approved", "denied"])),
                "groups": sorted(allowed_groups),
            }
        )
    return permissions


def _approval_repository(approval: dict[str, Any]) -> str | None:
    decision = approval.get("decision", {})
    if not isinstance(decision, dict):
        return approval.get("repository")
    return approval.get("repository") or decision.get("repository") or decision.get("repo")


def _rbac_policy(rbac_rules: dict[str, Any]) -> dict[str, Any]:
    policy = rbac_rules.get("approval_rbac", rbac_rules)
    return policy if isinstance(policy, dict) else {}


def _decision_action_alias(action: str) -> str:
    aliases = {"approve": "approved", "deny": "denied", "expire": "expired"}
    return aliases.get(action, action)


def actor_can_decide(
    actor_context: dict[str, Any],
    approval: dict[str, Any],
    *,
    action: str = "approve",
    rbac_rules: dict[str, Any] | None = None,
) -> bool:
    if action == "expire" and "system" in actor_context.get("groups", []):
        return True
    if approval.get("break_glass") and "Change Advisory Board" not in actor_context.get("groups", []):
        return False
    if _repository_rbac_allows(actor_context, approval, action=action, rbac_rules=rbac_rules or {}):
        return True
    return approval.get("approver_group") in actor_context.get("groups", [])


def apply_approval_decision(
    approval: dict[str, Any],
    *,
    state: str,
    actor: str,
    reason: str,
    external_ref: str | None = None,
    actor_context: dict[str, Any] | None = None,
    rbac_rules: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if state not in {"approved", "denied", "expired"}:
        raise ValueError("state must be approved, denied, or expired")
    if approval.get("state") != "pending":
        raise ValueError("only pending approvals can be changed")
    if not actor:
        raise ValueError("actor is required")
    if not reason:
        raise ValueError("reason is required")
    if actor_context and not actor_can_decide(actor_context, approval, action=state, rbac_rules=rbac_rules):
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


def load_provider_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"approval provider config not found: {path}")
    if path.suffix.lower() in {".yaml", ".yml"}:
        try:
            import yaml
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError("Install PyYAML to load YAML approval provider config files.") from exc
        payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    else:
        payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("approval provider config must be an object")
    return payload


def build_configured_provider_request_specs(approval: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    providers = _provider_config(config)
    endpoints = {
        provider: _configured_value(provider_config, "url")
        for provider, provider_config in providers.items()
        if provider_config.get("enabled", True) and _configured_value(provider_config, "url")
    }
    specs = build_provider_request_specs(approval, endpoints=endpoints)
    configured: dict[str, Any] = {}
    for provider, provider_config in providers.items():
        if provider not in specs or not provider_config.get("enabled", True):
            continue
        spec = {**specs[provider], "headers": {**specs[provider].get("headers", {})}}
        if str(spec["headers"].get("authorization", "")).startswith("Bearer ${"):
            spec["headers"].pop("authorization")
        if not _configured_value(provider_config, "url"):
            raise ValueError(f"approval provider {provider} must configure url or url_env")
        spec["url"] = _configured_value(provider_config, "url")
        spec["headers"].update(_configured_headers(provider_config))
        if provider in {"jira", "servicenow"} and "authorization" not in spec["headers"]:
            raise ValueError(f"approval provider {provider} must configure token_env, authorization_env, or authorization header")
        configured[provider] = spec
    return configured


def deliver_provider_requests(
    approval: dict[str, Any],
    config: dict[str, Any],
    *,
    provider: str = "all",
    retries: int = 2,
    timeout_seconds: float = 10.0,
    sender: Any | None = None,
) -> dict[str, Any]:
    specs = build_configured_provider_request_specs(approval, config)
    providers = set(specs) if provider == "all" else {provider}
    unknown = providers - set(specs)
    if unknown:
        raise ValueError(f"approval provider is not configured: {', '.join(sorted(unknown))}")
    delivery_sender = sender or _send_http_json_request
    deliveries = [
        _deliver_one_provider(
            item,
            specs[item],
            retries=max(0, retries),
            timeout_seconds=max(0.1, timeout_seconds),
            sender=delivery_sender,
        )
        for item in sorted(providers)
    ]
    return {
        "schema_version": "cavra.approval.delivery.v1",
        "product": "CAVRA",
        "approval_id": approval.get("approval_id"),
        "decision_id": approval.get("decision_id"),
        "generated_at": utc_now(),
        "success": all(item["success"] for item in deliveries),
        "deliveries": deliveries,
    }


def _provider_config(config: dict[str, Any]) -> dict[str, dict[str, Any]]:
    providers = config.get("approval_providers", config.get("providers", config))
    if not isinstance(providers, dict):
        raise ValueError("approval provider config must contain provider objects")
    normalized: dict[str, dict[str, Any]] = {}
    for provider, provider_config in providers.items():
        if not isinstance(provider_config, dict):
            raise ValueError(f"approval provider {provider} config must be an object")
        normalized[str(provider)] = provider_config
    return normalized


def _configured_value(provider_config: dict[str, Any], key: str) -> str | None:
    env_value = provider_config.get(f"{key}_env")
    if env_value:
        configured = os.environ.get(str(env_value))
        if not configured:
            raise ValueError(f"environment variable {env_value} is required for approval provider {key}")
        return configured
    value = provider_config.get(key)
    return str(value) if value else None


def _configured_headers(provider_config: dict[str, Any]) -> dict[str, str]:
    headers = {str(key).lower(): str(value) for key, value in provider_config.get("headers", {}).items()}
    token = _configured_value(provider_config, "token")
    authorization = _configured_value(provider_config, "authorization")
    if authorization:
        headers["authorization"] = authorization
    elif token:
        scheme = str(provider_config.get("authorization_scheme", "Bearer"))
        headers["authorization"] = f"{scheme} {token}"
    return headers


def _deliver_one_provider(
    provider: str,
    spec: dict[str, Any],
    *,
    retries: int,
    timeout_seconds: float,
    sender: Any,
) -> dict[str, Any]:
    attempts = retries + 1
    last_result: dict[str, Any] | None = None
    for attempt in range(1, attempts + 1):
        started_at = utc_now()
        try:
            response = sender(spec, timeout_seconds=timeout_seconds)
            status_code = int(response.get("status_code", 0))
            success = 200 <= status_code < 300
            last_result = {
                "provider": provider,
                "success": success,
                "status_code": status_code,
                "attempt_count": attempt,
                "started_at": started_at,
                "completed_at": utc_now(),
                "error": None if success else response.get("error") or f"HTTP {status_code}",
                "request": _redacted_request_spec(spec),
            }
            if success:
                return last_result
        except Exception as exc:  # pragma: no cover - exercised through sender tests
            last_result = {
                "provider": provider,
                "success": False,
                "status_code": None,
                "attempt_count": attempt,
                "started_at": started_at,
                "completed_at": utc_now(),
                "error": str(exc),
                "request": _redacted_request_spec(spec),
            }
        if attempt < attempts:
            time.sleep(min(0.25 * attempt, 1.0))
    return last_result or {
        "provider": provider,
        "success": False,
        "status_code": None,
        "attempt_count": 0,
        "started_at": utc_now(),
        "completed_at": utc_now(),
        "error": "delivery was not attempted",
        "request": _redacted_request_spec(spec),
    }


def _send_http_json_request(spec: dict[str, Any], *, timeout_seconds: float) -> dict[str, Any]:
    body = json.dumps(spec.get("body", {})).encode("utf-8")
    headers = {str(key): str(value) for key, value in spec.get("headers", {}).items()}
    req = request.Request(str(spec["url"]), data=body, headers=headers, method=str(spec.get("method", "POST")))
    try:
        with request.urlopen(req, timeout=timeout_seconds) as response:
            return {"status_code": response.getcode(), "body": response.read(4096).decode("utf-8", errors="replace")}
    except error.HTTPError as exc:
        return {"status_code": exc.code, "body": exc.read(4096).decode("utf-8", errors="replace"), "error": str(exc)}
    except error.URLError as exc:
        return {"status_code": 0, "error": str(exc.reason)}


def _redacted_request_spec(spec: dict[str, Any]) -> dict[str, Any]:
    headers = {}
    for key, value in spec.get("headers", {}).items():
        lowered = str(key).lower()
        headers[lowered] = "REDACTED" if lowered in {"authorization", "x-api-key", "api-key"} else value
    return {
        "method": spec.get("method", "POST"),
        "url": _redact_url(str(spec.get("url", ""))),
        "headers": headers,
    }


def _redact_url(url: str) -> str:
    if "hooks.slack.com/services/" in url:
        return "https://hooks.slack.com/services/REDACTED"
    if "?" in url:
        return f"{url.split('?', 1)[0]}?REDACTED"
    return url


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


def export_provider_delivery_result(result: dict[str, Any], output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{result.get('approval_id', 'approval')}-provider-delivery.json"
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


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
        rbac_rules: dict[str, Any] | None = None,
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
                rbac_rules=rbac_rules,
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
        rbac_rules: dict[str, Any] | None = None,
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
                rbac_rules=rbac_rules,
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
