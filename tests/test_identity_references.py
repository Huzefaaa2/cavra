import subprocess
from pathlib import Path


ENTRA_DIR = Path("examples/identity/entra-id-oidc-rbac")
OKTA_DIR = Path("examples/identity/okta-oidc-rbac")


def test_identity_reference_scripts_are_shell_syntax_valid() -> None:
    for script in [
        ENTRA_DIR / "generate-cavra-identity-config.sh",
        OKTA_DIR / "generate-cavra-identity-config.sh",
    ]:
        subprocess.run(["bash", "-n", str(script)], check=True)


def test_entra_identity_reference_contains_required_cavra_controls() -> None:
    script = (ENTRA_DIR / "generate-cavra-identity-config.sh").read_text(encoding="utf-8")
    env = (ENTRA_DIR / "variables.example.env").read_text(encoding="utf-8")
    readme = (ENTRA_DIR / "README.md").read_text(encoding="utf-8")

    assert "login.microsoftonline.com/${CAVRA_ENTRA_TENANT_ID}/v2.0/.well-known/openid-configuration" in script
    assert "jwks_uri" in script
    assert "approval-oidc.json" in script
    assert "approval-rbac.yaml" in script
    assert "CAVRA_APPROVAL_OIDC_CONFIG" in script
    assert "CAVRA_APPROVAL_RBAC_FILE" in script
    assert "approval_rbac:" in script
    assert "repository_permissions:" in script
    assert "CAVRA_ENTRA_AUDIENCE=api://cavra-production" in env
    assert "tenant-specific issuer metadata" in readme


def test_okta_identity_reference_contains_required_cavra_controls() -> None:
    script = (OKTA_DIR / "generate-cavra-identity-config.sh").read_text(encoding="utf-8")
    env = (OKTA_DIR / "variables.example.env").read_text(encoding="utf-8")
    readme = (OKTA_DIR / "README.md").read_text(encoding="utf-8")

    assert "${issuer}/.well-known/openid-configuration" in script
    assert "jwks_uri" in script
    assert "approval-oidc.json" in script
    assert "approval-rbac.yaml" in script
    assert "CAVRA_APPROVAL_OIDC_CONFIG" in script
    assert "CAVRA_APPROVAL_RBAC_FILE" in script
    assert "approval_rbac:" in script
    assert "repository_permissions:" in script
    assert "CAVRA_OKTA_AUDIENCE=api://cavra-production" in env
    assert "issuer must exactly match" in readme.lower()


def test_oidc_rbac_docs_reference_identity_bundles_and_next_work() -> None:
    doc = Path("docs/oidc-rbac-deployment.md").read_text(encoding="utf-8")
    wiki = Path("docs/wiki/OIDC-RBAC-Deployment.md").read_text(encoding="utf-8")

    assert str(ENTRA_DIR) in doc
    assert str(OKTA_DIR) in doc
    assert "CAVRA_APPROVAL_OIDC_CONFIG" in doc
    assert "CAVRA_APPROVAL_RBAC_FILE" in doc
    assert "generated Go enforcement contracts" in doc
    assert str(ENTRA_DIR) in wiki
    assert str(OKTA_DIR) in wiki
