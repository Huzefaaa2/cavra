from __future__ import annotations

import json
import subprocess
from pathlib import Path

from fastapi.testclient import TestClient

from cavra.api import create_app
from cavra.approvals import actor_can_decide, actor_context_from_claims, create_approval_request
from cavra.enterprise_identity import (
    actor_has_enterprise_scope,
    build_enterprise_identity_contract,
    build_enterprise_identity_readiness,
    enterprise_actor_claims_context,
    validate_enterprise_live_identity_packet,
)


LIVE_IDENTITY_SAMPLE = Path("examples/identity/enterprise-live-identity-validation.sample.json")


def test_enterprise_identity_contract_covers_r2_1_controls() -> None:
    contract = build_enterprise_identity_contract()
    policy = contract["policy"]

    assert contract["schema_version"] == "cavra.enterprise.identity_contract.v1"
    assert policy["identity_providers"]["oidc"]["status"] == "supported"
    assert policy["identity_providers"]["saml"]["status"] == "bridge_required"
    assert policy["identity_providers"]["scim"]["status"] == "private_enterprise_sync_contract"
    assert set(policy["rbac"]["required_roles"]) >= {
        "ciso",
        "security_operator",
        "platform_security",
        "model_owner",
        "auditor",
        "break_glass_approver",
    }
    assert set(policy["abac"]["required_attributes"]) >= {
        "tenant_id",
        "workspace_id",
        "environment",
        "repository",
        "model_owner_ref",
        "data_classification",
    }
    assert policy["break_glass"]["external_reference_required"] is True


def test_enterprise_identity_readiness_blocks_incomplete_policy() -> None:
    readiness = build_enterprise_identity_readiness(
        oidc_configured=True,
        rbac_configured=True,
        policy={"rbac": {"required_roles": ["auditor"]}},
    )

    assert readiness["status"] == "blocked"
    assert readiness["ready_for_enterprise_identity"] is False
    assert any(check["check_id"] == "rbac_roles" and check["status"] == "blocker" for check in readiness["checks"])


def test_enterprise_identity_readiness_accepts_default_contract_with_runtime_warning() -> None:
    readiness = build_enterprise_identity_readiness(oidc_configured=False, rbac_configured=False)

    assert readiness["status"] == "contract_ready"
    assert readiness["ready_for_enterprise_identity"] is True
    assert any(check["check_id"] == "oidc_runtime_config" and check["status"] == "warn" for check in readiness["checks"])


def test_enterprise_actor_claims_map_groups_to_roles_and_abac_scope() -> None:
    actor = enterprise_actor_claims_context(
        {
            "sub": "user-123",
            "email": "model-owner@example.com",
            "groups": ["CAVRA-Model-Owners"],
            "tenant_id": "tenant-a",
            "workspace_id": "workspace-prod",
            "repository": "payments/api",
            "environment": "production",
            "model_owner_ref": "team:model-risk",
            "data_classification": "restricted",
        }
    )

    assert "model_owner" in actor["roles"]
    assert actor_has_enterprise_scope(
        actor,
        action="approve_model_artifact",
        resource={"tenant_id": "tenant-a", "workspace_id": "workspace-prod"},
    )
    assert not actor_has_enterprise_scope(
        actor,
        action="approve_model_artifact",
        resource={"tenant_id": "tenant-b", "workspace_id": "workspace-prod"},
    )


def test_enterprise_abac_enforces_model_owner_scope_on_approvals() -> None:
    approval = create_approval_request(
        {
            "decision_id": "dec_model_1",
            "rule_id": "mcp.model.publish",
            "asset_type": "model_artifact",
            "tenant_id": "tenant-a",
            "workspace_id": "workspace-prod",
            "repository": "payments/api",
            "model_owner_ref": "team:model-risk",
        },
        approver_group="AI Governance",
    )
    actor = actor_context_from_claims(
        {
            "sub": "user-123",
            "email": "model-owner@example.com",
            "groups": ["CAVRA-Model-Owners", "AI Governance"],
            "tenant_id": "tenant-a",
            "workspace_id": "workspace-prod",
        }
    )
    mismatched_actor = {**actor, "tenant_id": "tenant-b"}
    operator_actor = actor_context_from_claims(
        {
            "sub": "user-456",
            "email": "operator@example.com",
            "groups": ["CAVRA-Security-Operations", "AI Governance"],
            "tenant_id": "tenant-a",
            "workspace_id": "workspace-prod",
        }
    )

    assert actor_can_decide(actor, approval, action="approved")
    assert not actor_can_decide(mismatched_actor, approval, action="approved")
    assert not actor_can_decide(operator_actor, approval, action="approved")


def test_enterprise_abac_enforces_runtime_scope_on_approvals() -> None:
    approval = create_approval_request(
        {
            "decision_id": "dec_runtime_1",
            "rule_id": "filesystem.write.sensitive",
            "tenant_id": "tenant-a",
            "workspace_id": "workspace-prod",
            "repository": "payments/api",
            "environment": "production",
        },
        approver_group="Platform Security",
    )
    platform_actor = actor_context_from_claims(
        {
            "sub": "user-789",
            "email": "platform@example.com",
            "groups": ["CAVRA-Platform-Security", "Platform Security"],
            "tenant_id": "tenant-a",
            "workspace_id": "workspace-prod",
        }
    )
    mismatched_workspace_actor = {**platform_actor, "workspace_id": "workspace-dev"}

    assert actor_can_decide(platform_actor, approval, action="approved")
    assert not actor_can_decide(mismatched_workspace_actor, approval, action="approved")


def test_enterprise_abac_preserves_legacy_group_only_approval() -> None:
    approval = create_approval_request(
        {
            "decision_id": "dec_legacy_1",
            "rule_id": "filesystem.write",
            "target": "iam/admin-role.tf",
        },
        approver_group="IAM",
    )

    assert actor_can_decide({"actor": "iam@example.com", "groups": ["IAM"]}, approval, action="approved")


def test_enterprise_live_identity_sample_is_structurally_valid_but_not_ready() -> None:
    packet = json.loads(LIVE_IDENTITY_SAMPLE.read_text(encoding="utf-8"))
    result = validate_enterprise_live_identity_packet(packet)

    assert result["schema_version"] == "cavra.enterprise.identity_live_validation_result.v1"
    assert result["ready_for_live_enterprise_identity"] is False
    assert any(check["check_id"] == "live_validation_mode" and check["status"] == "blocker" for check in result["checks"])


def test_enterprise_live_identity_packet_can_be_ready_with_live_evidence(tmp_path) -> None:
    packet = json.loads(LIVE_IDENTITY_SAMPLE.read_text(encoding="utf-8"))
    packet["packet_id"] = "identity-live-ready"
    packet["environment"]["validation_mode"] = "live"
    packet["generated_at"] = "2026-07-03T12:00:00Z"
    packet_path = tmp_path / "identity-live.json"
    result_path = tmp_path / "identity-live-result.json"
    packet_path.write_text(json.dumps(packet), encoding="utf-8")

    result = validate_enterprise_live_identity_packet(packet)
    subprocess.run(
        [
            "python3",
            "scripts/validate_enterprise_live_identity_packet.py",
            "--packet",
            str(packet_path),
            "--output",
            str(result_path),
        ],
        check=True,
    )

    assert result["ready_for_live_enterprise_identity"] is True
    assert result_path.exists()
    assert json.loads(result_path.read_text(encoding="utf-8"))["status"] == "ready"


def test_enterprise_live_identity_packet_rejects_secret_like_fields() -> None:
    packet = json.loads(LIVE_IDENTITY_SAMPLE.read_text(encoding="utf-8"))
    packet["environment"]["validation_mode"] = "live"
    packet["evidence"]["access_token"] = "do-not-commit"

    result = validate_enterprise_live_identity_packet(packet)

    assert result["ready_for_live_enterprise_identity"] is False
    assert any(check["check_id"] == "secret_redaction" and check["status"] == "blocker" for check in result["checks"])


def test_api_enterprise_identity_endpoints_report_contract(monkeypatch, tmp_path) -> None:
    policy_path = tmp_path / "identity-policy.json"
    policy_path.write_text(
        json.dumps(
            {
                "rbac": {
                    "role_groups": {
                        "ciso": ["CAVRA-CISO"],
                        "security_operator": ["CAVRA-SOC"],
                        "platform_security": ["CAVRA-Platform-Security"],
                        "model_owner": ["CAVRA-Model-Owners"],
                        "auditor": ["CAVRA-Auditors"],
                        "break_glass_approver": ["Change Advisory Board"],
                    }
                }
            }
        ),
        encoding="utf-8",
    )
    oidc_path = tmp_path / "oidc.json"
    rbac_path = tmp_path / "rbac.json"
    oidc_path.write_text('{"issuer":"https://issuer.example","audience":"cavra","jwks":{"keys":[]}}', encoding="utf-8")
    rbac_path.write_text('{"approval_rbac":{"group_mappings":{"CAVRA-SOC":"security_operator"}}}', encoding="utf-8")
    monkeypatch.setenv("CAVRA_ENTERPRISE_IDENTITY_POLICY", str(policy_path))
    monkeypatch.setenv("CAVRA_APPROVAL_OIDC_CONFIG", str(oidc_path))
    monkeypatch.setenv("CAVRA_APPROVAL_RBAC_FILE", str(rbac_path))

    client = TestClient(create_app())
    contract = client.get("/identity/enterprise-contract")
    readiness = client.get("/identity/enterprise-readiness")
    config = client.get("/console/config")

    assert contract.status_code == 200
    assert contract.json()["schema_version"] == "cavra.enterprise.identity_contract.v1"
    assert readiness.status_code == 200
    assert readiness.json()["status"] == "ready"
    assert readiness.json()["ready_for_enterprise_identity"] is True
    assert config.json()["enterprise_identity_policy"] == "configured"
    assert config.json()["endpoints"]["enterprise_identity_readiness"] == "/identity/enterprise-readiness"


def test_enterprise_identity_readiness_validator_passes() -> None:
    subprocess.run(["python3", "scripts/validate_enterprise_identity_readiness.py"], check=True)


def test_enterprise_live_identity_sample_validator_allows_not_ready_sample() -> None:
    subprocess.run(
        [
            "python3",
            "scripts/validate_enterprise_live_identity_packet.py",
            "--packet",
            str(LIVE_IDENTITY_SAMPLE),
            "--allow-not-ready",
        ],
        check=True,
    )
