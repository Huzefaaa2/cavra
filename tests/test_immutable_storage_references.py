import subprocess
from pathlib import Path


AWS_DIR = Path("examples/immutable-storage/aws-s3-object-lock")
AZURE_DIR = Path("examples/immutable-storage/azure-blob-immutability")


def test_immutable_storage_reference_scripts_are_shell_syntax_valid() -> None:
    for script in [
        AWS_DIR / "deploy.sh",
        AWS_DIR / "upload-evidence.sh",
        AZURE_DIR / "deploy.sh",
        AZURE_DIR / "upload-evidence.sh",
    ]:
        subprocess.run(["bash", "-n", str(script)], check=True)


def test_aws_s3_object_lock_reference_contains_required_controls() -> None:
    deploy = (AWS_DIR / "deploy.sh").read_text(encoding="utf-8")
    upload = (AWS_DIR / "upload-evidence.sh").read_text(encoding="utf-8")
    env = (AWS_DIR / "variables.example.env").read_text(encoding="utf-8")

    assert "--object-lock-enabled-for-bucket" in deploy
    assert "put-bucket-versioning" in deploy
    assert "put-object-lock-configuration" in deploy
    assert "aws:kms" in deploy
    assert "DenyInsecureTransport" in deploy
    assert "CAVRA_RETENTION_MODE=COMPLIANCE" in env
    assert "aws s3 sync" in upload
    assert "retention-policy.json" in upload
    assert "ObjectLockRetainUntilDate" in upload


def test_azure_blob_immutability_reference_contains_required_controls() -> None:
    deploy = (AZURE_DIR / "deploy.sh").read_text(encoding="utf-8")
    upload = (AZURE_DIR / "upload-evidence.sh").read_text(encoding="utf-8")

    assert "--allow-blob-public-access false" in deploy
    assert "--https-only true" in deploy
    assert "--enable-versioning true" in deploy
    assert "immutability-policy create" in deploy
    assert "immutability-policy lock" in deploy
    assert "legal-hold set" in deploy
    assert "az storage blob upload-batch" in upload
    assert "retention-policy.json" in upload
    assert "--overwrite false" in upload


def test_immutable_storage_docs_reference_deployment_bundles() -> None:
    doc = Path("docs/immutable-evidence-storage.md").read_text(encoding="utf-8")
    wiki = Path("docs/wiki/Immutable-Evidence-Storage.md").read_text(encoding="utf-8")

    assert str(AWS_DIR) in doc
    assert str(AZURE_DIR) in doc
    assert "compiled-policy loading for the Go enforcement plane" in doc
    assert str(AWS_DIR) in wiki
    assert str(AZURE_DIR) in wiki
