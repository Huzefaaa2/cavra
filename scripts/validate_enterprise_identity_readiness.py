from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cavra.enterprise_identity import build_enterprise_identity_contract, build_enterprise_identity_readiness


REQUIRED_TEXT = {
    "src/cavra/enterprise_identity.py": [
        "cavra.enterprise.identity_policy.v1",
        "cavra.enterprise.identity_contract.v1",
        "cavra.enterprise.identity_readiness.v1",
        "REQUIRED_ENTERPRISE_ROLES",
        "REQUIRED_ABAC_ATTRIBUTES",
        "break_glass_approver",
        "SAML assertion is normalized",
        "private_enterprise_sync_contract",
    ],
    "src/cavra/approvals.py": [
        "actor_has_enterprise_scope",
        "_approval_resource_context",
        "_enterprise_approval_action",
        "approve_model_artifact",
        "approve_runtime_action",
    ],
    "src/cavra/api.py": [
        "CAVRA_ENTERPRISE_IDENTITY_POLICY",
        "/identity/enterprise-contract",
        "/identity/enterprise-readiness",
        "build_enterprise_identity_readiness",
    ],
    "docs/enterprise-identity-access-control.md": [
        "OIDC",
        "SAML bridge",
        "SCIM",
        "RBAC",
        "ABAC",
        "break-glass",
        "model_owner",
        "security_operator",
        "Runtime ABAC Enforcement",
        "approve_model_artifact",
    ],
    "docs/oidc-rbac-deployment.md": [
        "CAVRA_ENTERPRISE_IDENTITY_POLICY",
        "/identity/enterprise-readiness",
        "SAML bridge",
        "SCIM",
    ],
    "docs/product/cavra-unified-enterprise-product-enhancement-roadmap.md": [
        "| R2.1 |",
        "Enterprise identity readiness contract",
        "runtime scoped approval enforcement",
        "scripts/validate_enterprise_identity_readiness.py",
    ],
    "docs/wiki/Enterprise-Identity-And-Access-Control.md": [
        "OIDC",
        "SAML bridge",
        "SCIM",
        "ABAC",
        "Runtime Enforcement",
    ],
}


def validate_required_text() -> list[str]:
    failures: list[str] = []
    for relative_path, required_fragments in REQUIRED_TEXT.items():
        path = Path(relative_path)
        if not path.exists():
            failures.append(f"missing {relative_path}")
            continue
        text = path.read_text(encoding="utf-8")
        for fragment in required_fragments:
            if fragment not in text:
                failures.append(f"{relative_path} is missing required text: {fragment}")
    return failures


def validate_contract_shape() -> list[str]:
    failures: list[str] = []
    contract = build_enterprise_identity_contract()
    readiness = build_enterprise_identity_readiness(oidc_configured=False, rbac_configured=False)
    policy = contract.get("policy", {})
    if contract.get("schema_version") != "cavra.enterprise.identity_contract.v1":
        failures.append("enterprise identity contract schema mismatch")
    if readiness.get("schema_version") != "cavra.enterprise.identity_readiness.v1":
        failures.append("enterprise identity readiness schema mismatch")
    if readiness.get("status") != "contract_ready":
        failures.append("default enterprise identity policy should be structurally ready with runtime warnings")
    for section in ("oidc", "saml", "scim"):
        if section not in policy.get("identity_providers", {}):
            failures.append(f"identity provider section missing: {section}")
    for role in ("ciso", "security_operator", "platform_security", "model_owner", "auditor", "break_glass_approver"):
        if role not in policy.get("rbac", {}).get("required_roles", []):
            failures.append(f"enterprise role missing: {role}")
    for attribute in ("tenant_id", "workspace_id", "environment", "repository", "model_owner_ref", "data_classification"):
        if attribute not in policy.get("abac", {}).get("required_attributes", []):
            failures.append(f"ABAC attribute missing: {attribute}")
    return failures


def main() -> None:
    failures = validate_required_text()
    failures.extend(validate_contract_shape())
    if failures:
        raise SystemExit("\n".join(failures))
    print("enterprise identity readiness controls validated")


if __name__ == "__main__":
    main()
