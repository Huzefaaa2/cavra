from __future__ import annotations

import subprocess
from pathlib import Path


def test_release_trust_gate_repository_controls_pass() -> None:
    subprocess.run(["python3", "scripts/validate_release_trust_gate.py"], check=True)


def test_community_release_trust_artifact_generator(tmp_path: Path) -> None:
    dist = tmp_path / "dist"
    dist.mkdir()
    (dist / "cavra-1.0.0-py3-none-any.whl").write_bytes(b"wheel")
    (dist / "cavra-1.0.0.tar.gz").write_bytes(b"sdist")

    subprocess.run(
        [
            "python3",
            "scripts/generate_community_release_trust_artifacts.py",
            "--dist",
            str(dist),
        ],
        check=True,
    )
    subprocess.run(
        [
            "python3",
            "scripts/validate_release_trust_gate.py",
            "--dist",
            str(dist),
            "--version",
            "1.0.0",
        ],
        check=True,
    )

    assert (dist / "cavra-1.0.0-SHA256SUMS.txt").exists()
    assert (dist / "cavra-1.0.0.sbom.spdx.json").exists()
    assert (dist / "cavra-1.0.0.provenance.json").exists()
    assert (dist / "cavra-1.0.0.release-trust.json").exists()
