import json
import time
from base64 import urlsafe_b64encode
from pathlib import Path

from cavra.approvals import (
    ApprovalStore,
    SQLiteApprovalStore,
    actor_context_from_claims,
    actor_context_from_oidc_token,
    attach_approval_to_decision,
    build_provider_request_specs,
    create_approval_request,
    deliver_provider_requests,
    export_approval_notification_payloads,
    export_provider_delivery_result,
    load_oidc_config,
    load_provider_config,
    load_rbac_rules,
    load_routing_rules,
    route_approver_group,
    validate_oidc_token,
)
from cavra.evidence import build_evidence_metadata, create_evidence_bundle
from cavra.runtime import RuntimeGuard


def _approval_decision() -> dict[str, object]:
    return RuntimeGuard(policy_pack="cavra-ai-agent-baseline").evaluate_file_access(
        Path("iam/admin-role.tf"),
        "write",
    ).to_dict()


def _b64url(data: bytes) -> str:
    return urlsafe_b64encode(data).decode("ascii").rstrip("=")


def _signed_rs256_token(claims: dict[str, object], *, kid: str = "test-key"):
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import padding, rsa

    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_numbers = private_key.public_key().public_numbers()
    jwk = {
        "kty": "RSA",
        "kid": kid,
        "alg": "RS256",
        "use": "sig",
        "n": _b64url(public_numbers.n.to_bytes((public_numbers.n.bit_length() + 7) // 8, "big")),
        "e": _b64url(public_numbers.e.to_bytes((public_numbers.e.bit_length() + 7) // 8, "big")),
    }
    header = {"alg": "RS256", "kid": kid, "typ": "JWT"}
    signing_input = ".".join(
        [
            _b64url(json.dumps(header, separators=(",", ":")).encode("utf-8")),
            _b64url(json.dumps(claims, separators=(",", ":")).encode("utf-8")),
        ]
    ).encode("ascii")
    signature = private_key.sign(signing_input, padding.PKCS1v15(), hashes.SHA256())
    return f"{signing_input.decode('ascii')}.{_b64url(signature)}", {"keys": [jwk]}, private_key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    )


def test_create_and_approve_request(tmp_path: Path) -> None:
    store = ApprovalStore(tmp_path / "approvals.json")
    approval = store.create_request(_approval_decision(), requested_by="developer")

    decided = store.decide(
        approval["approval_id"],
        state="approved",
        actor="platform-security",
        reason="Reviewed scoped IAM change.",
        external_ref="CHG-100",
    )

    assert approval["state"] == "pending"
    assert decided["state"] == "approved"
    assert decided["decided_by"] == "platform-security"
    assert decided["external_ref"] == "CHG-100"
    assert store.list(state="approved")["total"] == 1


def test_approval_requires_reason_and_blocks_double_decision(tmp_path: Path) -> None:
    store = ApprovalStore(tmp_path / "approvals.json")
    approval = store.create_request(_approval_decision())

    try:
        store.decide(approval["approval_id"], state="approved", actor="security", reason="")
    except ValueError as exc:
        assert "reason is required" in str(exc)
    else:
        raise AssertionError("expected missing reason to fail")

    store.decide(approval["approval_id"], state="denied", actor="security", reason="Not enough context.")
    try:
        store.decide(approval["approval_id"], state="approved", actor="security", reason="Changed mind.")
    except ValueError as exc:
        assert "only pending approvals" in str(exc)
    else:
        raise AssertionError("expected final approval to reject a second decision")


def test_break_glass_records_mandatory_evidence(tmp_path: Path) -> None:
    store = ApprovalStore(tmp_path / "approvals.json")

    approval = store.break_glass(
        decision=_approval_decision(),
        actor="incident-commander",
        reason="Production recovery for active incident.",
        external_ref="INC-777",
    )

    assert approval["state"] == "break_glass"
    assert approval["break_glass"] is True
    assert approval["break_glass_reason"] == "Production recovery for active incident."
    assert approval["external_ref"] == "INC-777"
    assert any(item["event"] == "break_glass" for item in approval["history"])


def test_approval_outcome_is_recorded_in_evidence(tmp_path: Path) -> None:
    decision = _approval_decision()
    approval = create_approval_request(decision, requested_by="developer")
    decision_with_approval = attach_approval_to_decision(decision, approval)

    create_evidence_bundle([decision_with_approval], tmp_path / "bundle", session_id="approval-session")
    metadata = build_evidence_metadata(tmp_path / "bundle")
    attestation = (tmp_path / "bundle" / "pr-attestation.md").read_text(encoding="utf-8")

    assert metadata["approval_outcomes"][0]["approval_id"] == approval["approval_id"]
    assert "Approval Outcomes" in attestation
    assert approval["approval_id"] in attestation


def test_routing_rules_select_approver_group() -> None:
    decision = _approval_decision()
    decision.pop("approver_group", None)

    assert route_approver_group(decision) == "IAM"


def test_repository_routing_file_overrides_default(tmp_path: Path) -> None:
    routing = tmp_path / "routing.json"
    routing.write_text(
        """
        {
          "approval_routing": [
            {
              "rule_id_prefix": "filesystem.write",
              "target_contains": "iam/",
              "approver_group": "Cloud IAM Owners"
            }
          ]
        }
        """,
        encoding="utf-8",
    )
    decision = _approval_decision()
    decision.pop("approver_group", None)

    assert route_approver_group(decision, load_routing_rules(routing)) == "Cloud IAM Owners"


def test_routing_file_accepts_raw_rule_list(tmp_path: Path) -> None:
    routing = tmp_path / "routing.json"
    routing.write_text(
        '[{"rule_id_prefix":"filesystem.write","target_contains":"iam/","approver_group":"Cloud IAM Owners"}]',
        encoding="utf-8",
    )

    assert load_routing_rules(routing)[0]["approver_group"] == "Cloud IAM Owners"


def test_actor_claims_authorize_matching_approval_group(tmp_path: Path) -> None:
    store = ApprovalStore(tmp_path / "approvals.json")
    approval = store.create_request(_approval_decision(), requested_by="developer")
    actor_context = actor_context_from_claims({"email": "iam@example.com", "groups": ["IAM"]})

    decided = store.decide(
        approval["approval_id"],
        state="approved",
        actor="iam@example.com",
        reason="Reviewed IAM change.",
        actor_context=actor_context,
    )

    assert decided["state"] == "approved"


def test_actor_claims_can_map_external_groups() -> None:
    context = actor_context_from_claims(
        {"email": "owner@example.com", "groups": ["github-team:iam-admins"]},
        rbac_rules={"group_mappings": {"github-team:iam-admins": "IAM"}},
    )

    assert "IAM" in context["groups"]


def test_signed_oidc_token_validates_issuer_audience_and_signature() -> None:
    token, jwks, _private_key = _signed_rs256_token(
        {
            "iss": "https://issuer.example",
            "aud": "cavra-approvals",
            "sub": "user-123",
            "email": "iam@example.com",
            "groups": ["IAM"],
            "exp": int(time.time()) + 300,
        }
    )

    claims = validate_oidc_token(
        token,
        {"issuer": "https://issuer.example", "audience": "cavra-approvals", "jwks": jwks},
    )

    assert claims["email"] == "iam@example.com"


def test_signed_oidc_token_rejects_wrong_audience() -> None:
    token, jwks, _private_key = _signed_rs256_token(
        {
            "iss": "https://issuer.example",
            "aud": "other-audience",
            "sub": "user-123",
            "groups": ["IAM"],
            "exp": int(time.time()) + 300,
        }
    )

    try:
        validate_oidc_token(token, {"issuer": "https://issuer.example", "audience": "cavra-approvals", "jwks": jwks})
    except ValueError as exc:
        assert "audience" in str(exc)
    else:
        raise AssertionError("expected wrong audience to fail")


def test_signed_oidc_token_supports_repository_rbac_policy(tmp_path: Path) -> None:
    token, jwks, _private_key = _signed_rs256_token(
        {
            "iss": "https://issuer.example",
            "aud": "cavra-approvals",
            "sub": "user-123",
            "email": "owner@example.com",
            "groups": ["github-team:payments-owners"],
            "repository": "payments/api",
            "exp": int(time.time()) + 300,
        }
    )
    rbac_path = tmp_path / "approval-rbac.json"
    rbac_path.write_text(
        json.dumps(
            {
                "approval_rbac": {
                    "group_mappings": {"github-team:payments-owners": "Payments Owners"},
                    "repository_permissions": [
                        {
                            "repository": "payments/api",
                            "approver_group": "IAM",
                            "groups": ["Payments Owners"],
                            "actions": ["approved", "denied"],
                        }
                    ],
                }
            }
        ),
        encoding="utf-8",
    )
    decision = _approval_decision()
    decision["repository"] = "payments/api"
    store = ApprovalStore(tmp_path / "approvals.json")
    approval = store.create_request(decision, requested_by="developer")
    rbac_rules = load_rbac_rules(rbac_path)
    actor_context = actor_context_from_oidc_token(
        token,
        {"issuer": "https://issuer.example", "audience": "cavra-approvals", "jwks": jwks},
        rbac_rules=rbac_rules,
    )

    decided = store.decide(
        approval["approval_id"],
        state="approved",
        actor="owner@example.com",
        reason="Repository owner approved.",
        actor_context=actor_context,
        rbac_rules=rbac_rules,
    )

    assert decided["state"] == "approved"


def test_oidc_config_loader_reads_jwks_path(tmp_path: Path) -> None:
    _token, jwks, _private_key = _signed_rs256_token(
        {
            "iss": "https://issuer.example",
            "aud": "cavra-approvals",
            "sub": "user-123",
            "exp": int(time.time()) + 300,
        }
    )
    jwks_path = tmp_path / "jwks.json"
    config_path = tmp_path / "oidc.json"
    jwks_path.write_text(json.dumps(jwks), encoding="utf-8")
    config_path.write_text(
        json.dumps({"issuer": "https://issuer.example", "audience": "cavra-approvals", "jwks_path": jwks_path.name}),
        encoding="utf-8",
    )

    config = load_oidc_config(config_path)

    assert config["jwks"]["keys"][0]["kid"] == "test-key"


def test_actor_claims_reject_wrong_approval_group(tmp_path: Path) -> None:
    store = ApprovalStore(tmp_path / "approvals.json")
    approval = store.create_request(_approval_decision(), requested_by="developer")
    actor_context = actor_context_from_claims({"email": "dev@example.com", "groups": ["Developers"]})

    try:
        store.decide(
            approval["approval_id"],
            state="approved",
            actor="dev@example.com",
            reason="Trying to approve.",
            actor_context=actor_context,
        )
    except ValueError as exc:
        assert "not authorized" in str(exc)
    else:
        raise AssertionError("expected unauthorized actor to fail")


def test_sqlite_approval_store_searches_and_updates(tmp_path: Path) -> None:
    store = SQLiteApprovalStore(tmp_path / "approvals.db")
    approval = store.create_request(_approval_decision(), requested_by="developer")

    store.decide(approval["approval_id"], state="approved", actor="iam-owner", reason="Reviewed.")
    result = store.list(state="approved", approver_group="IAM")

    assert result["total"] == 1
    assert result["items"][0]["state"] == "approved"


def test_export_approval_notification_payloads(tmp_path: Path) -> None:
    store = ApprovalStore(tmp_path / "approvals.json")
    approval = store.create_request(_approval_decision(), requested_by="developer")

    result = export_approval_notification_payloads(approval, tmp_path / "notifications")

    assert (tmp_path / "notifications" / "slack-approval-payload.json").exists()
    assert (tmp_path / "notifications" / "teams-approval-payload.json").exists()
    assert (tmp_path / "notifications" / "jira-approval-payload.json").exists()
    assert (tmp_path / "notifications" / "servicenow-approval-payload.json").exists()
    assert (tmp_path / "notifications" / "webhook-approval-payload.json").exists()
    assert len(result.files) == 5


def test_provider_request_specs_do_not_require_live_credentials(tmp_path: Path) -> None:
    store = ApprovalStore(tmp_path / "approvals.json")
    approval = store.create_request(_approval_decision(), requested_by="developer")

    specs = build_provider_request_specs(approval)

    assert specs["jira"]["method"] == "POST"
    assert "${JIRA_TOKEN}" in specs["jira"]["headers"]["authorization"]
    assert specs["slack"]["body"]["text"].startswith("CAVRA approval")


def test_deliver_provider_requests_uses_secret_backed_config(tmp_path: Path, monkeypatch) -> None:
    store = ApprovalStore(tmp_path / "approvals.json")
    approval = store.create_request(_approval_decision(), requested_by="developer")
    config = {
        "approval_providers": {
            "jira": {
                "enabled": True,
                "url": "https://jira.example/rest/api/3/issue",
                "token_env": "JIRA_TOKEN",
            }
        }
    }
    monkeypatch.setenv("JIRA_TOKEN", "secret-token")
    calls = []

    def sender(spec: dict[str, object], *, timeout_seconds: float) -> dict[str, object]:
        calls.append((spec, timeout_seconds))
        return {"status_code": 201}

    result = deliver_provider_requests(approval, config, provider="jira", sender=sender, timeout_seconds=2.5)

    assert result["success"] is True
    assert result["deliveries"][0]["status_code"] == 201
    assert result["deliveries"][0]["request"]["headers"]["authorization"] == "REDACTED"
    assert calls[0][0]["headers"]["authorization"] == "Bearer secret-token"
    assert calls[0][1] == 2.5


def test_deliver_provider_requests_retries_and_records_failure(tmp_path: Path) -> None:
    store = ApprovalStore(tmp_path / "approvals.json")
    approval = store.create_request(_approval_decision(), requested_by="developer")
    attempts = {"count": 0}

    def sender(spec: dict[str, object], *, timeout_seconds: float) -> dict[str, object]:
        attempts["count"] += 1
        return {"status_code": 503, "error": "service unavailable"}

    result = deliver_provider_requests(
        approval,
        {"approval_providers": {"webhook": {"url": "https://approval.example/hook"}}},
        provider="webhook",
        retries=1,
        sender=sender,
    )

    assert result["success"] is False
    assert result["deliveries"][0]["attempt_count"] == 2
    assert result["deliveries"][0]["error"] == "service unavailable"
    assert attempts["count"] == 2


def test_deliver_provider_requests_requires_configured_secret(tmp_path: Path) -> None:
    store = ApprovalStore(tmp_path / "approvals.json")
    approval = store.create_request(_approval_decision(), requested_by="developer")

    try:
        deliver_provider_requests(
            approval,
            {"approval_providers": {"jira": {"url": "https://jira.example/rest/api/3/issue"}}},
            provider="jira",
        )
    except ValueError as exc:
        assert "must configure token_env" in str(exc)
    else:
        raise AssertionError("expected live Jira delivery without credentials to fail")


def test_provider_config_loader_and_delivery_export(tmp_path: Path) -> None:
    config_path = tmp_path / "providers.json"
    config_path.write_text('{"approval_providers":{"webhook":{"url":"https://approval.example/hook"}}}', encoding="utf-8")
    config = load_provider_config(config_path)
    output = export_provider_delivery_result(
        {
            "schema_version": "cavra.approval.delivery.v1",
            "approval_id": "apr_test",
            "success": True,
            "deliveries": [],
        },
        tmp_path / "delivery",
    )

    assert config["approval_providers"]["webhook"]["url"] == "https://approval.example/hook"
    assert output.exists()
