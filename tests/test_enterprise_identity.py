from __future__ import annotations

import json
import subprocess
from pathlib import Path

from fastapi.testclient import TestClient

from cavra.api import create_app
from cavra.enterprise_identity import (
    actor_has_enterprise_scope,
    build_enterprise_identity_contract,
    build_enterprise_identity_readiness,
    enterprise_actor_claims_context,
)


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
