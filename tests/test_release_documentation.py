import json
import shutil
import subprocess
import sys
from pathlib import Path


def test_community_ga_release_checklist_is_linked_from_public_docs() -> None:
    checklist = Path("docs/community-ga-release-checklist.md").read_text(encoding="utf-8")
    wiki_checklist = Path("docs/wiki/Community-GA-Release-Checklist.md").read_text(encoding="utf-8")
    readme = Path("README.md").read_text(encoding="utf-8")
    wiki_home = Path("docs/wiki/Home.md").read_text(encoding="utf-8")
    release_policy = Path("docs/release-documentation-policy.md").read_text(encoding="utf-8")

    required_terms = [
        "Policy signing",
        "Runtime modes",
        "Golden decisions",
        "Evidence Console",
        "Deployment validation",
        "Go runtime readiness",
        "Public boundary",
    ]
    for term in required_terms:
        assert term in checklist
        assert term in wiki_checklist

    assert "docs/community-ga-release-checklist.md" in readme
    assert "Community-GA-Release-Checklist.md" in wiki_home
    assert "Community GA release checklist" in release_policy


def test_community_ga_release_packet_template_is_linked_and_structured() -> None:
    template = Path("docs/community-ga-release-packet-template.md").read_text(encoding="utf-8")
    wiki_template = Path("docs/wiki/Community-GA-Release-Packet-Template.md").read_text(
        encoding="utf-8"
    )
    schema = json.loads(
        Path("docs/release-packets/community-ga-release-packet.schema.json").read_text(
            encoding="utf-8"
        )
    )
    example = json.loads(
        Path("examples/release-packets/community-ga-release-packet.example.json").read_text(
            encoding="utf-8"
        )
    )
    readme = Path("README.md").read_text(encoding="utf-8")
    wiki_home = Path("docs/wiki/Home.md").read_text(encoding="utf-8")
    validation_doc = Path("docs/community-ga-release-packet-validation.md").read_text(
        encoding="utf-8"
    )
    wiki_validation_doc = Path("docs/wiki/Community-GA-Release-Packet-Validation.md").read_text(
        encoding="utf-8"
    )
    release_policy = Path("docs/release-documentation-policy.md").read_text(encoding="utf-8")
    checklist = Path("docs/community-ga-release-checklist.md").read_text(encoding="utf-8")

    required_gates = {
        "Public boundary",
        "Policy signing",
        "Policy validation",
        "Runtime modes",
        "Golden decisions",
        "Evidence Console",
        "Deployment validation",
        "Go runtime readiness",
        "Documentation",
        "CI evidence",
    }

    assert "docs/community-ga-release-packet-template.md" in readme
    assert "docs/community-ga-release-packet-validation.md" in readme
    assert "Community-GA-Release-Packet-Template.md" in wiki_home
    assert "Community-GA-Release-Packet-Validation.md" in wiki_home
    assert "Community GA release packet" in release_policy
    assert "Community GA release packet template" in checklist
    assert "community-ga-release-packet.schema.json" in template
    assert "community-ga-release-packet.example.json" in template
    assert "Public Boundary Review" in template
    assert "Public Boundary Review" in wiki_template
    assert "scripts/validate-release-packets.py" in validation_doc
    assert "scripts/validate-release-packets.py" in wiki_validation_doc

    schema_required = set(schema["required"])
    for field in (
        "packet_id",
        "release_state",
        "gates",
        "validation_commands",
        "accepted_risks",
        "public_boundary_review",
        "decision",
        "next_recommendation",
    ):
        assert field in schema_required
        assert field in example

    example_gate_names = {gate["name"] for gate in example["gates"]}
    assert required_gates == example_gate_names
    assert example["release_state"] in {
        "ready_for_community_ga",
        "ready_with_accepted_risk",
        "blocked",
    }
    assert example["public_boundary_review"]["enterprise_code_present"] is False
    assert example["public_boundary_review"]["secrets_present"] is False


def test_community_ga_dry_run_release_packet_is_linked_and_complete() -> None:
    packet_md = Path("docs/release-packets/community-ga-dry-run-2026-06-04.md").read_text(
        encoding="utf-8"
    )
    packet_json = json.loads(
        Path("docs/release-packets/community-ga-dry-run-2026-06-04.json").read_text(
            encoding="utf-8"
        )
    )
    wiki_packet = Path("docs/wiki/Community-GA-Dry-Run-Release-Packet.md").read_text(
        encoding="utf-8"
    )
    readme = Path("README.md").read_text(encoding="utf-8")
    wiki_home = Path("docs/wiki/Home.md").read_text(encoding="utf-8")
    roadmap = Path("docs/production-roadmap.md").read_text(encoding="utf-8")
    next_slice = Path("docs/roadmap-status-next-slice.md").read_text(encoding="utf-8")

    required_gates = {
        "Public boundary",
        "Policy signing",
        "Policy validation",
        "Runtime modes",
        "Golden decisions",
        "Evidence Console",
        "Deployment validation",
        "Go runtime readiness",
        "Documentation",
        "CI evidence",
    }
    packet_gate_names = {gate["name"] for gate in packet_json["gates"]}

    assert "docs/release-packets/community-ga-dry-run-2026-06-04.md" in readme
    assert "Community-GA-Dry-Run-Release-Packet.md" in wiki_home
    assert "community-ga-dry-run-2026-06-04.json" in roadmap
    assert "GitHub Release notes" in next_slice
    assert "not an official tagged GA release" in packet_md
    assert "not an official tagged GA release" in wiki_packet

    assert packet_json["packet_id"] == "community-ga-dry-run-2026-06-04"
    assert packet_json["release_state"] == "ready_with_accepted_risk"
    assert packet_json["commit"] == "65f63df48304"
    assert required_gates == packet_gate_names
    assert packet_json["decision"]["status"] == "approve"
    assert packet_json["public_boundary_review"]["validation_result"] == "pass"
    assert packet_json["public_boundary_review"]["enterprise_code_present"] is False
    assert packet_json["public_boundary_review"]["secrets_present"] is False
    assert len(packet_json["accepted_risks"]) == 2
    assert all(risk["severity"] == "low" for risk in packet_json["accepted_risks"])
    assert packet_json["next_recommendation"] == (
        "Create a final tagged Community GA release packet when the maintainer is ready "
        "to publish an official Community GA release."
    )


def test_community_ga_v010_release_packet_is_linked_and_ready() -> None:
    packet_md = Path("docs/release-packets/community-ga-v0.1.0.md").read_text(
        encoding="utf-8"
    )
    packet_json = json.loads(
        Path("docs/release-packets/community-ga-v0.1.0.json").read_text(encoding="utf-8")
    )
    wiki_packet = Path("docs/wiki/Community-GA-v0.1.0-Release-Packet.md").read_text(
        encoding="utf-8"
    )
    readme = Path("README.md").read_text(encoding="utf-8")
    wiki_home = Path("docs/wiki/Home.md").read_text(encoding="utf-8")
    roadmap = Path("docs/production-roadmap.md").read_text(encoding="utf-8")
    next_slice = Path("docs/roadmap-status-next-slice.md").read_text(encoding="utf-8")

    required_gates = {
        "Public boundary",
        "Policy signing",
        "Policy validation",
        "Runtime modes",
        "Golden decisions",
        "Evidence Console",
        "Deployment validation",
        "Go runtime readiness",
        "Documentation",
        "CI evidence",
    }
    packet_gate_names = {gate["name"] for gate in packet_json["gates"]}

    assert "docs/release-packets/community-ga-v0.1.0.md" in readme
    assert "Community-GA-v0.1.0-Release-Packet.md" in wiki_home
    assert "community-ga-v0.1.0.json" in roadmap
    assert "GitHub Release notes" in next_slice
    assert "community-v0.1.0" in packet_md
    assert "community-v0.1.0" in wiki_packet

    assert packet_json["packet_id"] == "community-ga-v0.1.0"
    assert packet_json["release_state"] == "ready_for_community_ga"
    assert packet_json["tag"] == "community-v0.1.0"
    assert packet_json["accepted_risks"] == []
    assert required_gates == packet_gate_names
    assert {gate["status"] for gate in packet_json["gates"]} <= {"pass", "disabled"}
    assert packet_json["decision"]["status"] == "approve"
    assert packet_json["public_boundary_review"]["validation_result"] == "pass"
    assert packet_json["public_boundary_review"]["enterprise_code_present"] is False
    assert packet_json["public_boundary_review"]["secrets_present"] is False
    assert packet_json["next_recommendation"] == (
        "Publish Community GA GitHub Release notes and attach distribution artifacts after "
        "the community-v0.1.0 release workflow completes."
    )


def test_release_packet_validation_script_accepts_repository_packets() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate-release-packets.py"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "CAVRA release packet validation passed." in result.stdout


def test_release_packet_validation_script_rejects_missing_required_gate(tmp_path: Path) -> None:
    schema_dir = tmp_path / "docs" / "release-packets"
    example_dir = tmp_path / "examples" / "release-packets"
    schema_dir.mkdir(parents=True)
    example_dir.mkdir(parents=True)
    shutil.copy(
        "docs/release-packets/community-ga-release-packet.schema.json",
        schema_dir / "community-ga-release-packet.schema.json",
    )
    packet = json.loads(
        Path("docs/release-packets/community-ga-dry-run-2026-06-04.json").read_text(
            encoding="utf-8"
        )
    )
    packet["gates"] = [gate for gate in packet["gates"] if gate["name"] != "CI evidence"]
    (schema_dir / "community-ga-invalid.json").write_text(json.dumps(packet), encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "scripts/validate-release-packets.py", "--root", str(tmp_path)],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "missing required gates: CI evidence" in result.stdout


def test_release_packet_validation_runs_in_public_ci_workflows() -> None:
    workflow_paths = [
        ".github/workflows/community-ci.yml",
        ".github/workflows/security-scan.yml",
        ".github/workflows/cavra-governance.yml",
        ".github/workflows/release-community.yml",
    ]

    for workflow_path in workflow_paths:
        workflow = Path(workflow_path).read_text(encoding="utf-8")
        assert "python scripts/validate-release-packets.py" in workflow, workflow_path
