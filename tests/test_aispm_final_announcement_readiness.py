from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_aispm_final_announcement_readiness_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate-aispm-final-announcement-readiness.py"],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    assert result.returncode == 0, result.stdout
    assert "AISPM final announcement readiness validation passed." in result.stdout


def test_aispm_final_announcement_readiness_contract() -> None:
    packet = json.loads(
        Path("docs/release-verifications/aispm-final-announcement-readiness.json").read_text(
            encoding="utf-8"
        )
    )

    assert packet["schema_version"] == "cavra.aispm.final_announcement_readiness.v1"
    assert packet["status"] == "ready"
    assert packet["announcement_decision"] == "ready_for_public_announcement"
    assert packet["portal_packet"] == "cavra-aispm-final-announcement-readiness-packet.json"
    assert {source["source_id"] for source in packet["required_sources"]} == {
        "launch_readiness_rollup",
        "release_evidence_index",
        "public_release_readiness",
        "trial_field_guide",
        "hosted_operator_status",
        "hosted_post_deploy_evidence",
        "community_release_verification",
        "release_notes",
    }
    assert {gate["gate_id"] for gate in packet["announcement_gates"]} == {
        "community_portal_ready",
        "release_evidence_ready",
        "field_guide_published",
        "hosted_release_operator_ready",
        "public_release_notes_ready",
        "public_safety_boundary_verified",
    }
    assert "Enterprise source code" in packet["public_safety_boundary"]


def test_aispm_final_announcement_readiness_is_wired() -> None:
    command = "python scripts/validate-aispm-final-announcement-readiness.py"
    for workflow_path in [
        ".github/workflows/community-ci.yml",
        ".github/workflows/release-community.yml",
        ".github/workflows/deploy-sandbox.yml",
    ]:
        assert command in Path(workflow_path).read_text(encoding="utf-8")

    for doc_path in [
        "README.md",
        "docs/release-verifications/aispm-release-evidence-index.md",
        "docs/release-verifications/aispm-launch-readiness-rollup.md",
        "docs/wiki/Home.md",
        "docs/wiki/AISPM-Dashboard-Roadmap.md",
    ]:
        text = Path(doc_path).read_text(encoding="utf-8")
        assert "docs/release-verifications/aispm-final-announcement-readiness.md" in text
        assert "docs/release-verifications/aispm-final-announcement-readiness.json" in text
        assert "scripts/validate-aispm-final-announcement-readiness.py" in text
