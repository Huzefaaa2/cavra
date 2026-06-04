from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_package_metadata_uses_pyproject_as_source_of_truth() -> None:
    pyproject = Path("pyproject.toml").read_text(encoding="utf-8")
    setup_py = Path("setup.py").read_text(encoding="utf-8")
    manifest = Path("MANIFEST.in").read_text(encoding="utf-8")

    assert 'requires = ["setuptools>=77", "wheel"]' in pyproject
    assert 'license = "BUSL-1.1"' in pyproject
    assert 'license-files = ["LICENSE", "NOTICE"]' in pyproject
    assert "[project.urls]" in pyproject
    assert "License :: Other/Proprietary License" not in pyproject
    assert "setup()" in setup_py
    assert "install_requires" not in setup_py
    assert "project_urls" not in setup_py
    assert "find_packages" not in setup_py
    assert "recursive-include .github *.md *.yml" in manifest
    assert "recursive-include .github *.md *.yml *.yaml" not in manifest
    assert Path("src/cavra/schemas/__init__.py").is_file()


def test_python_package_metadata_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate-python-package-metadata.py"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "CAVRA Python package metadata validation passed." in result.stdout
