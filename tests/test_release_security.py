from __future__ import annotations

import subprocess
from pathlib import Path


def test_release_security_workflow_and_docs_are_present() -> None:
    assert Path("SECURITY.md").exists()
    assert Path("docs/vulnerability-disclosure.md").exists()
    assert Path("docs/release-security-advisories.md").exists()
    assert Path(".github/workflows/release-security.yml").exists()

    subprocess.run(["python3", "scripts/validate_release_security.py"], check=True)


def test_release_security_workflow_validates_expected_controls() -> None:
    workflow = Path(".github/workflows/release-security.yml").read_text(encoding="utf-8")

    assert "Release Security Readiness" in workflow
    assert "scripts/validate_release_security.py" in workflow
    assert "SECURITY.md" in workflow
    assert "docs/release-security-advisories.md" in workflow
