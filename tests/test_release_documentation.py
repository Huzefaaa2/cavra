import importlib.util
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
    assert "Node 24 readiness" in next_slice
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
    assert "Node 24 readiness" in next_slice
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


def test_community_ga_v010_release_publication_is_linked_and_complete() -> None:
    publication = Path("docs/community-ga-v0.1.0-release-publication.md").read_text(
        encoding="utf-8"
    )
    wiki_publication = Path("docs/wiki/Community-GA-v0.1.0-Release-Publication.md").read_text(
        encoding="utf-8"
    )
    readme = Path("README.md").read_text(encoding="utf-8")
    wiki_home = Path("docs/wiki/Home.md").read_text(encoding="utf-8")
    roadmap = Path("docs/production-roadmap.md").read_text(encoding="utf-8")
    next_slice = Path("docs/roadmap-status-next-slice.md").read_text(encoding="utf-8")

    release_url = "https://github.com/Huzefaaa2/cavra/releases/tag/community-v0.1.0"
    workflow_url = "https://github.com/Huzefaaa2/cavra/actions/runs/26929259433"
    sdist_sha = "35370dea724612c8619100db812635c048b91ede65fd905e8d8c189b7c07c26e"
    wheel_sha = "1a586ce0fe91af6c24c14b0f8b833d722f9de9e24cfcb1fd81dafc0f016306d8"

    assert release_url in readme
    assert "docs/community-ga-v0.1.0-release-publication.md" in readme
    assert "Community-GA-v0.1.0-Release-Publication.md" in wiki_home
    assert release_url in roadmap
    assert "Node 24 readiness" in next_slice

    for document in (publication, wiki_publication):
        assert release_url in document
        assert workflow_url in document
        assert "cavra-0.1.0.tar.gz" in document
        assert "cavra-0.1.0-py3-none-any.whl" in document
        assert sdist_sha in document
        assert wheel_sha in document
        assert "Enterprise/private source included: no" in document


def test_community_ga_v010_post_release_verification_is_linked_and_complete() -> None:
    verification = Path(
        "docs/release-verifications/community-v0.1.0-post-release-verification.md"
    ).read_text(encoding="utf-8")
    verification_json = json.loads(
        Path(
            "docs/release-verifications/community-v0.1.0-post-release-verification.json"
        ).read_text(encoding="utf-8")
    )
    wiki_verification = Path(
        "docs/wiki/Community-GA-v0.1.0-Post-Release-Verification.md"
    ).read_text(encoding="utf-8")
    runbook = Path("docs/community-release-verification-runbook.md").read_text(
        encoding="utf-8"
    )
    release_notes = Path("docs/releases/community-v0.1.0.md").read_text(encoding="utf-8")
    changelog = Path("CHANGELOG.md").read_text(encoding="utf-8")
    readme = Path("README.md").read_text(encoding="utf-8")
    wiki_home = Path("docs/wiki/Home.md").read_text(encoding="utf-8")
    roadmap = Path("docs/production-roadmap.md").read_text(encoding="utf-8")
    next_slice = Path("docs/roadmap-status-next-slice.md").read_text(encoding="utf-8")
    workflow = Path(".github/workflows/verify-community-release.yml").read_text(
        encoding="utf-8"
    )
    verifier = Path("scripts/verify-community-release-artifacts.py")

    release_url = "https://github.com/Huzefaaa2/cavra/releases/tag/community-v0.1.0"
    sdist_sha = "35370dea724612c8619100db812635c048b91ede65fd905e8d8c189b7c07c26e"
    wheel_sha = "1a586ce0fe91af6c24c14b0f8b833d722f9de9e24cfcb1fd81dafc0f016306d8"

    assert release_url in verification
    assert release_url in wiki_verification
    assert (
        "docs/release-verifications/community-v0.1.0-post-release-verification.md"
        in readme
    )
    assert "Community-GA-v0.1.0-Post-Release-Verification.md" in wiki_home
    assert "docs/community-release-verification-runbook.md" in readme
    assert "docs/releases/community-v0.1.0.md" in readme
    assert "verify-community-release-artifacts.py" in roadmap
    assert "maintenance-release checklist" in next_slice
    assert "Verify Community Release" in runbook
    assert "Post-release verification" in release_notes
    assert "post-release verification evidence" in changelog
    assert "workflow_dispatch" in workflow
    assert "scripts/verify-community-release-artifacts.py" in workflow

    assert (
        verification_json["schema_version"]
        == "cavra.community_release_verification.v1"
    )
    assert verification_json["tag"] == "community-v0.1.0"
    assert verification_json["decision"] == "pass"
    assert verification_json["install_smoke"]["output"] == "cavra 0.1.0"
    assert verification_json["public_boundary"]["community_artifacts_only"] is True
    assert verification_json["public_boundary"]["enterprise_source_included"] is False
    assert verification_json["public_boundary"]["private_keys_included"] is False
    assert verification_json["public_boundary"]["customer_records_included"] is False
    assert {artifact["sha256"] for artifact in verification_json["artifacts"]} == {
        sdist_sha,
        wheel_sha,
    }
    assert all(artifact["downloadable"] for artifact in verification_json["artifacts"])
    assert all(artifact["checksum_match"] for artifact in verification_json["artifacts"])

    spec = importlib.util.spec_from_file_location(
        "verify_community_release_artifacts", verifier
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    sample = Path(
        "docs/release-verifications/community-v0.1.0-post-release-verification.json"
    )
    assert module.sha256_file(sample) == module.sha256_file(sample)
    assert module.DEFAULT_TAG == "community-v0.1.1"


def test_community_maintenance_release_checklist_is_linked_and_validated() -> None:
    checklist = Path("docs/community-maintenance-release-checklist.md").read_text(
        encoding="utf-8"
    )
    template = Path("docs/community-maintenance-release-evidence-template.md").read_text(
        encoding="utf-8"
    )
    schema = json.loads(
        Path("docs/release-verifications/community-maintenance-release.schema.json").read_text(
            encoding="utf-8"
        )
    )
    example = json.loads(
        Path(
            "examples/release-verifications/community-maintenance-release.example.json"
        ).read_text(encoding="utf-8")
    )
    readme = Path("README.md").read_text(encoding="utf-8")
    changelog = Path("CHANGELOG.md").read_text(encoding="utf-8")
    wiki_home = Path("docs/wiki/Home.md").read_text(encoding="utf-8")
    wiki_checklist = Path("docs/wiki/Community-Maintenance-Release-Checklist.md").read_text(
        encoding="utf-8"
    )
    roadmap = Path("docs/production-roadmap.md").read_text(encoding="utf-8")
    next_slice = Path("docs/roadmap-status-next-slice.md").read_text(encoding="utf-8")
    community_ci = Path(".github/workflows/community-ci.yml").read_text(encoding="utf-8")
    security_scan = Path(".github/workflows/security-scan.yml").read_text(
        encoding="utf-8"
    )
    release_workflow = Path(".github/workflows/release-community.yml").read_text(
        encoding="utf-8"
    )
    governance = Path(".github/workflows/cavra-governance.yml").read_text(
        encoding="utf-8"
    )

    required_gates = {
        "Release notes",
        "Changelog",
        "README link",
        "Wiki link",
        "Verification workflow",
        "Artifact checksums",
        "Install smoke",
        "Public boundary",
        "CI evidence",
    }

    assert "docs/community-maintenance-release-checklist.md" in readme
    assert "docs/community-maintenance-release-evidence-template.md" in readme
    assert "Community-Maintenance-Release-Checklist.md" in wiki_home
    assert "Community-Maintenance-Release-Evidence-Template.md" in wiki_home
    assert "Community maintenance-release governance" in roadmap
    assert "Node 24 readiness" in next_slice
    assert "release notes" in checklist
    assert "Python package metadata" in checklist
    assert "Release workflow guards" in checklist
    assert "scripts/validate-python-package-metadata.py" in checklist
    assert "pypi-v*" in checklist
    assert "go-runtime-v*" in checklist
    assert "community-maintenance-release.schema.json" in template
    assert "Python package metadata" in template
    assert "Release workflow guards" in template
    assert "Community maintenance-release checklist" in changelog
    assert "Required Gates" in wiki_checklist

    assert schema["properties"]["schema_version"]["const"] == (
        "cavra.community_maintenance_release.v1"
    )
    assert example["schema_version"] == "cavra.community_maintenance_release.v1"
    assert example["release_state"] == "ready_for_publication"
    assert example["accepted_risks"] == []
    assert {gate["name"] for gate in example["gates"]} == required_gates
    assert all(gate["status"] == "pass" for gate in example["gates"])
    assert example["public_boundary"]["enterprise_source_included"] is False
    assert example["public_boundary"]["paid_policy_packs_included"] is False
    assert example["public_boundary"]["customer_records_included"] is False
    assert example["public_boundary"]["private_keys_included"] is False
    assert example["decision"]["status"] == "approve"

    for workflow in (community_ci, security_scan, release_workflow, governance):
        assert "scripts/validate-maintenance-release-evidence.py" in workflow

    result = subprocess.run(
        [sys.executable, "scripts/validate-maintenance-release-evidence.py"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "CAVRA maintenance release evidence validation passed." in result.stdout


def test_community_release_note_freshness_is_linked_and_validated() -> None:
    doc = Path("docs/community-release-note-freshness.md").read_text(encoding="utf-8")
    wiki_doc = Path("docs/wiki/Community-Release-Note-Freshness.md").read_text(
        encoding="utf-8"
    )
    release_notes = Path("docs/releases/community-v0.1.0.md").read_text(
        encoding="utf-8"
    )
    readme = Path("README.md").read_text(encoding="utf-8")
    changelog = Path("CHANGELOG.md").read_text(encoding="utf-8")
    wiki_home = Path("docs/wiki/Home.md").read_text(encoding="utf-8")
    roadmap = Path("docs/production-roadmap.md").read_text(encoding="utf-8")
    next_slice = Path("docs/roadmap-status-next-slice.md").read_text(encoding="utf-8")
    community_ci = Path(".github/workflows/community-ci.yml").read_text(encoding="utf-8")
    security_scan = Path(".github/workflows/security-scan.yml").read_text(
        encoding="utf-8"
    )
    release_workflow = Path(".github/workflows/release-community.yml").read_text(
        encoding="utf-8"
    )
    governance = Path(".github/workflows/cavra-governance.yml").read_text(
        encoding="utf-8"
    )

    script = "scripts/validate-community-release-note-freshness.py"
    release_notes_path = "docs/releases/community-v0.1.0.md"
    verification_path = (
        "docs/release-verifications/community-v0.1.0-post-release-verification.md"
    )
    release_url = "https://github.com/Huzefaaa2/cavra/releases/tag/community-v0.1.0"

    assert "docs/community-release-note-freshness.md" in readme
    assert "Community-Release-Note-Freshness.md" in wiki_home
    assert release_notes_path in readme
    assert verification_path in readme
    assert release_url in release_notes
    assert verification_path in release_notes
    assert "Community-GA-v0.1.0-Release-Notes.md" in wiki_home
    assert "Community-GA-v0.1.0-Post-Release-Verification.md" in wiki_home
    assert script in doc
    assert script in wiki_doc
    assert script in roadmap
    assert "Node 24 readiness" in next_slice
    assert "release-note freshness validation" in changelog

    for workflow in (community_ci, security_scan, release_workflow, governance):
        assert script in workflow

    result = subprocess.run(
        [sys.executable, script],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "CAVRA Community release note freshness validation passed." in result.stdout


def test_community_v011_maintenance_release_is_linked_and_validated() -> None:
    release_notes = Path("docs/releases/community-v0.1.1.md").read_text(
        encoding="utf-8"
    )
    verification = Path(
        "docs/release-verifications/community-v0.1.1-maintenance-verification.md"
    ).read_text(encoding="utf-8")
    verification_json = json.loads(
        Path(
            "docs/release-verifications/community-v0.1.1-maintenance-verification.json"
        ).read_text(encoding="utf-8")
    )
    wiki_release_notes = Path("docs/wiki/Community-v0.1.1-Release-Notes.md").read_text(
        encoding="utf-8"
    )
    wiki_verification = Path(
        "docs/wiki/Community-v0.1.1-Maintenance-Verification.md"
    ).read_text(encoding="utf-8")
    readme = Path("README.md").read_text(encoding="utf-8")
    changelog = Path("CHANGELOG.md").read_text(encoding="utf-8")
    wiki_home = Path("docs/wiki/Home.md").read_text(encoding="utf-8")
    roadmap = Path("docs/production-roadmap.md").read_text(encoding="utf-8")
    next_slice = Path("docs/roadmap-status-next-slice.md").read_text(encoding="utf-8")

    release_url = "https://github.com/Huzefaaa2/cavra/releases/tag/community-v0.1.1"
    release_notes_path = "docs/releases/community-v0.1.1.md"
    verification_path = (
        "docs/release-verifications/community-v0.1.1-maintenance-verification.md"
    )

    required_gates = {
        "Release notes",
        "Changelog",
        "README link",
        "Wiki link",
        "Verification workflow",
        "Artifact checksums",
        "Install smoke",
        "Public boundary",
        "CI evidence",
    }

    assert release_url in release_notes
    assert release_url in verification
    assert release_notes_path in readme
    assert verification_path in readme
    assert verification_path in release_notes
    assert (
        "docs/release-verifications/community-v0.1.1-post-release-verification.md"
        in readme
    )
    assert (
        "docs/release-verifications/community-v0.1.1-post-release-verification.md"
        in release_notes
    )
    assert "Community-v0.1.1-Release-Notes.md" in wiki_home
    assert "Community-v0.1.1-Maintenance-Verification.md" in wiki_home
    assert "Community-v0.1.1-Post-Release-Verification.md" in wiki_home
    assert "CAVRA Community v0.1.1 Release Notes" in wiki_release_notes
    assert "ready_for_publication" in wiki_verification
    assert "Converted the Community v0.1.1 maintenance-release packet" in changelog
    assert "community-v0.1.1-maintenance-verification.md" in roadmap
    assert "Node 24 readiness" in next_slice

    assert verification_json["schema_version"] == "cavra.community_maintenance_release.v1"
    assert verification_json["packet_id"] == "community-v0.1.1-maintenance-verification"
    assert verification_json["release_state"] == "ready_for_publication"
    assert verification_json["tag"] == "community-v0.1.1"
    assert verification_json["release_notes"] == release_notes_path
    assert verification_json["verification_packet"] == verification_path
    assert {gate["name"] for gate in verification_json["gates"]} == required_gates
    assert all(gate["status"] == "pass" for gate in verification_json["gates"])
    assert "32ab7a220eb5f25ea5ab42ccbc62a43b7260de12b9a0d3f3d7bdafa1501a5d6a" in verification
    assert "b123c6d2aadd72b055ba916caa68953af94122d34f1215756804d74e91174950" in verification
    assert "cavra 0.1.1" in verification
    assert verification_json["public_boundary"]["enterprise_source_included"] is False
    assert verification_json["public_boundary"]["paid_policy_packs_included"] is False
    assert verification_json["public_boundary"]["customer_records_included"] is False
    assert verification_json["public_boundary"]["private_keys_included"] is False
    assert verification_json["accepted_risks"] == []
    assert verification_json["decision"]["status"] == "approve"
    assert "Node 24 readiness" in verification_json["next_recommendation"]

    maintenance_result = subprocess.run(
        [sys.executable, "scripts/validate-maintenance-release-evidence.py"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert maintenance_result.returncode == 0, (
        maintenance_result.stdout + maintenance_result.stderr
    )

    freshness_result = subprocess.run(
        [sys.executable, "scripts/validate-community-release-note-freshness.py"],
        check=False,
        capture_output=True,
        text=True,
    )
    assert freshness_result.returncode == 0, (
        freshness_result.stdout + freshness_result.stderr
    )


def test_community_v011_post_release_verification_is_linked_and_complete() -> None:
    verification = Path(
        "docs/release-verifications/community-v0.1.1-post-release-verification.md"
    ).read_text(encoding="utf-8")
    verification_json = json.loads(
        Path(
            "docs/release-verifications/community-v0.1.1-post-release-verification.json"
        ).read_text(encoding="utf-8")
    )
    wiki_verification = Path(
        "docs/wiki/Community-v0.1.1-Post-Release-Verification.md"
    ).read_text(encoding="utf-8")
    release_notes = Path("docs/releases/community-v0.1.1.md").read_text(
        encoding="utf-8"
    )
    readme = Path("README.md").read_text(encoding="utf-8")
    wiki_home = Path("docs/wiki/Home.md").read_text(encoding="utf-8")
    index = Path("docs/community-release-index.md").read_text(encoding="utf-8")
    dashboard = Path("docs/community-release-readiness-dashboard.md").read_text(
        encoding="utf-8"
    )

    release_url = "https://github.com/Huzefaaa2/cavra/releases/tag/community-v0.1.1"
    verification_path = (
        "docs/release-verifications/community-v0.1.1-post-release-verification.md"
    )
    sdist_sha = "b123c6d2aadd72b055ba916caa68953af94122d34f1215756804d74e91174950"
    wheel_sha = "32ab7a220eb5f25ea5ab42ccbc62a43b7260de12b9a0d3f3d7bdafa1501a5d6a"

    assert release_url in verification
    assert release_url in wiki_verification
    assert verification_path in readme
    assert verification_path in release_notes
    assert verification_path in index
    assert verification_path in dashboard
    assert "Community-v0.1.1-Post-Release-Verification.md" in wiki_home
    assert "cavra 0.1.1" in verification
    assert sdist_sha in verification
    assert wheel_sha in verification

    assert verification_json["schema_version"] == "cavra.community_release_verification.v1"
    assert verification_json["tag"] == "community-v0.1.1"
    assert verification_json["decision"] == "pass"
    assert verification_json["install_smoke"]["output"] == "cavra 0.1.1"
    assert verification_json["public_boundary"]["community_artifacts_only"] is True
    assert verification_json["public_boundary"]["enterprise_source_included"] is False
    assert verification_json["public_boundary"]["private_keys_included"] is False
    assert verification_json["public_boundary"]["customer_records_included"] is False
    assert {artifact["sha256"] for artifact in verification_json["artifacts"]} == {
        sdist_sha,
        wheel_sha,
    }
    assert all(artifact["downloadable"] for artifact in verification_json["artifacts"])
    assert all(artifact["checksum_match"] for artifact in verification_json["artifacts"])
    assert "Node 24 readiness" in verification_json["next_recommendation"]


def test_community_v012_readiness_is_linked_and_validated() -> None:
    readiness = Path("docs/community-v0.1.2-readiness.md").read_text(encoding="utf-8")
    wiki_readiness = Path("docs/wiki/Community-v0.1.2-Readiness.md").read_text(
        encoding="utf-8"
    )
    readme = Path("README.md").read_text(encoding="utf-8")
    wiki_home = Path("docs/wiki/Home.md").read_text(encoding="utf-8")
    changelog = Path("CHANGELOG.md").read_text(encoding="utf-8")
    inventory = Path("docs/current-feature-inventory.md").read_text(encoding="utf-8")
    community_ci = Path(".github/workflows/community-ci.yml").read_text(encoding="utf-8")
    release_community = Path(".github/workflows/release-community.yml").read_text(
        encoding="utf-8"
    )
    publish_pypi = Path(".github/workflows/publish-pypi.yml").read_text(
        encoding="utf-8"
    )
    go_release = Path(".github/workflows/go-release.yml").read_text(encoding="utf-8")

    assert "docs/community-v0.1.2-readiness.md" in readme
    assert "Community-v0.1.2-Readiness.md" in wiki_home
    assert "package metadata warnings" in changelog
    assert "Community v0.1.2 readiness:" in inventory

    for document in (readiness, wiki_readiness):
        assert "pyproject.toml" in document
        assert "setup.py" in document
        assert "scripts/validate-python-package-metadata.py" in document
        assert "License-Expression: BUSL-1.1" in document
        assert "pypi-v" in document
        assert "go-runtime-v" in document
        assert "Node 24 readiness" in document

    assert "scripts/validate-python-package-metadata.py" in community_ci
    assert "scripts/validate-python-package-metadata.py" in release_community
    assert "python -m twine check dist/*" in publish_pypi
    assert "startsWith(github.event.release.tag_name, 'pypi-v')" in publish_pypi
    assert "startsWith(github.event.release.tag_name, 'go-runtime-v')" in go_release


def test_community_v012_release_is_linked_and_validated() -> None:
    release_notes = Path("docs/releases/community-v0.1.2.md").read_text(
        encoding="utf-8"
    )
    verification = Path(
        "docs/release-verifications/community-v0.1.2-maintenance-verification.md"
    ).read_text(encoding="utf-8")
    verification_json = json.loads(
        Path(
            "docs/release-verifications/community-v0.1.2-maintenance-verification.json"
        ).read_text(encoding="utf-8")
    )
    post_release = Path(
        "docs/release-verifications/community-v0.1.2-post-release-verification.md"
    ).read_text(encoding="utf-8")
    post_release_json = json.loads(
        Path(
            "docs/release-verifications/community-v0.1.2-post-release-verification.json"
        ).read_text(encoding="utf-8")
    )
    wiki_release_notes = Path("docs/wiki/Community-v0.1.2-Release-Notes.md").read_text(
        encoding="utf-8"
    )
    wiki_verification = Path(
        "docs/wiki/Community-v0.1.2-Maintenance-Verification.md"
    ).read_text(encoding="utf-8")
    readme = Path("README.md").read_text(encoding="utf-8")
    wiki_home = Path("docs/wiki/Home.md").read_text(encoding="utf-8")
    changelog = Path("CHANGELOG.md").read_text(encoding="utf-8")
    inventory = Path("docs/current-feature-inventory.md").read_text(encoding="utf-8")
    release_index = Path("docs/community-release-index.md").read_text(encoding="utf-8")
    dashboard = Path("docs/community-release-readiness-dashboard.md").read_text(
        encoding="utf-8"
    )
    wiki_post_release = Path(
        "docs/wiki/Community-v0.1.2-Post-Release-Verification.md"
    ).read_text(encoding="utf-8")

    release_url = "https://github.com/Huzefaaa2/cavra/releases/tag/community-v0.1.2"
    release_notes_path = "docs/releases/community-v0.1.2.md"
    verification_path = (
        "docs/release-verifications/community-v0.1.2-maintenance-verification.md"
    )
    post_release_path = (
        "docs/release-verifications/community-v0.1.2-post-release-verification.md"
    )
    wheel_sha = "bbdb2f593ce3c14742446c1682c23bef7933925a02382a874e59b8ef7e389163"
    sdist_sha = "f7a477cfef65d77bd4c36520a83d256c1086e7b81ffcd9411ee9c68d017ab1d0"

    assert release_notes_path in readme
    assert verification_path in readme
    assert post_release_path in readme
    assert "Community-v0.1.2-Release-Notes.md" in wiki_home
    assert "Community-v0.1.2-Maintenance-Verification.md" in wiki_home
    assert "Community-v0.1.2-Post-Release-Verification.md" in wiki_home
    assert "Community v0.1.2 release record:" in inventory
    assert "Published Community v0.1.2 GitHub Release artifacts" in changelog

    for document in (
        release_notes,
        verification,
        post_release,
        wiki_release_notes,
        wiki_verification,
        wiki_post_release,
    ):
        normalized_document = " ".join(document.split())
        assert release_url in document
        assert "cavra 0.1.2" in document
        assert wheel_sha in document
        assert sdist_sha in document
        assert "Enterprise source code" in normalized_document

    assert release_notes_path in release_index
    assert post_release_path in release_index
    assert "| Community v0.1.2 | Published |" in release_index
    assert release_notes_path in dashboard
    assert post_release_path in dashboard
    assert "Ready" in dashboard

    assert verification_json["schema_version"] == "cavra.community_maintenance_release.v1"
    assert verification_json["packet_id"] == "community-v0.1.2-maintenance-verification"
    assert verification_json["release_state"] == "ready_for_publication"
    assert verification_json["tag"] == "community-v0.1.2"
    assert verification_json["release_notes"] == release_notes_path
    assert verification_json["verification_packet"] == verification_path
    gate_statuses = {gate["name"]: gate["status"] for gate in verification_json["gates"]}
    assert gate_statuses["Artifact checksums"] == "pass"
    assert gate_statuses["Install smoke"] == "pass"
    assert gate_statuses["Release notes"] == "pass"
    assert gate_statuses["Public boundary"] == "pass"
    assert verification_json["accepted_risks"] == []
    assert verification_json["public_boundary"]["enterprise_source_included"] is False
    assert verification_json["public_boundary"]["private_keys_included"] is False
    assert verification_json["decision"]["status"] == "approve"
    assert "Node 24 readiness" in verification_json["next_recommendation"]

    assert post_release_json["schema_version"] == "cavra.community_release_verification.v1"
    assert post_release_json["tag"] == "community-v0.1.2"
    assert post_release_json["version"] == "0.1.2"
    assert post_release_json["release_target"] == (
        "e3cd7a1d6a3435188b4225d3bf49d79a9f6de128"
    )
    assert {artifact["name"] for artifact in post_release_json["artifacts"]} == {
        "cavra-0.1.2-py3-none-any.whl",
        "cavra-0.1.2.tar.gz",
    }
    assert all(artifact["downloadable"] for artifact in post_release_json["artifacts"])
    assert all(artifact["checksum_match"] for artifact in post_release_json["artifacts"])
    assert post_release_json["install_smoke"]["output"] == "cavra 0.1.2"
    assert post_release_json["decision"] == "pass"


def test_community_release_index_is_linked_and_current() -> None:
    release_index = Path("docs/community-release-index.md").read_text(encoding="utf-8")
    wiki_release_index = Path("docs/wiki/Community-Release-Index.md").read_text(
        encoding="utf-8"
    )
    readme = Path("README.md").read_text(encoding="utf-8")
    changelog = Path("CHANGELOG.md").read_text(encoding="utf-8")
    wiki_home = Path("docs/wiki/Home.md").read_text(encoding="utf-8")
    roadmap = Path("docs/production-roadmap.md").read_text(encoding="utf-8")
    next_slice = Path("docs/roadmap-status-next-slice.md").read_text(encoding="utf-8")
    inventory = Path("docs/current-feature-inventory.md").read_text(encoding="utf-8")

    v010_release = "https://github.com/Huzefaaa2/cavra/releases/tag/community-v0.1.0"
    v011_release = "https://github.com/Huzefaaa2/cavra/releases/tag/community-v0.1.1"
    v012_release = "https://github.com/Huzefaaa2/cavra/releases/tag/community-v0.1.2"
    v010_notes = "docs/releases/community-v0.1.0.md"
    v011_notes = "docs/releases/community-v0.1.1.md"
    v012_notes = "docs/releases/community-v0.1.2.md"
    v010_verification = (
        "docs/release-verifications/community-v0.1.0-post-release-verification.md"
    )
    v011_verification = (
        "docs/release-verifications/community-v0.1.1-post-release-verification.md"
    )
    v012_verification = (
        "docs/release-verifications/community-v0.1.2-post-release-verification.md"
    )

    assert "docs/community-release-index.md" in readme
    assert "Community-Release-Index.md" in wiki_home
    assert "Community release index" in changelog
    assert "Community release index documentation" in roadmap
    assert "Node 24 readiness" in next_slice
    assert "Community release index:" in inventory

    for document in (release_index, wiki_release_index):
        assert "Community GA v0.1.0" in document
        assert "Community v0.1.1" in document
        assert "Community v0.1.2" in document
        assert "Published" in document
        assert v010_release in document
        assert v011_release in document
        assert v012_release in document
        assert v010_notes in document
        assert v011_notes in document
        assert v012_notes in document
        assert v010_verification in document
        assert v011_verification in document
        assert v012_verification in document
        assert "scripts/validate-community-release-note-freshness.py" in document
        assert "scripts/validate-community-release-index.py" in document
        assert "Node 24 readiness" in document


def test_community_release_index_freshness_is_linked_and_validated() -> None:
    doc = Path("docs/community-release-index-freshness.md").read_text(encoding="utf-8")
    wiki_doc = Path("docs/wiki/Community-Release-Index-Freshness.md").read_text(
        encoding="utf-8"
    )
    readme = Path("README.md").read_text(encoding="utf-8")
    changelog = Path("CHANGELOG.md").read_text(encoding="utf-8")
    wiki_home = Path("docs/wiki/Home.md").read_text(encoding="utf-8")
    roadmap = Path("docs/production-roadmap.md").read_text(encoding="utf-8")
    next_slice = Path("docs/roadmap-status-next-slice.md").read_text(encoding="utf-8")
    inventory = Path("docs/current-feature-inventory.md").read_text(encoding="utf-8")
    community_ci = Path(".github/workflows/community-ci.yml").read_text(encoding="utf-8")
    security_scan = Path(".github/workflows/security-scan.yml").read_text(
        encoding="utf-8"
    )
    release_workflow = Path(".github/workflows/release-community.yml").read_text(
        encoding="utf-8"
    )
    governance = Path(".github/workflows/cavra-governance.yml").read_text(
        encoding="utf-8"
    )

    script = "scripts/validate-community-release-index.py"

    assert "docs/community-release-index-freshness.md" in readme
    assert "Community-Release-Index-Freshness.md" in wiki_home
    assert "Community release index freshness validation" in changelog
    assert script in doc
    assert script in wiki_doc
    assert script in roadmap
    assert script in inventory
    assert "Node 24 readiness" in next_slice

    for workflow in (community_ci, security_scan, release_workflow, governance):
        assert script in workflow

    result = subprocess.run(
        [sys.executable, script],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "CAVRA Community release index validation passed." in result.stdout


def test_community_release_readiness_dashboard_is_linked_and_current() -> None:
    dashboard = Path("docs/community-release-readiness-dashboard.md").read_text(
        encoding="utf-8"
    )
    wiki_dashboard = Path("docs/wiki/Community-Release-Readiness-Dashboard.md").read_text(
        encoding="utf-8"
    )
    readme = Path("README.md").read_text(encoding="utf-8")
    changelog = Path("CHANGELOG.md").read_text(encoding="utf-8")
    wiki_home = Path("docs/wiki/Home.md").read_text(encoding="utf-8")
    roadmap = Path("docs/production-roadmap.md").read_text(encoding="utf-8")
    next_slice = Path("docs/roadmap-status-next-slice.md").read_text(encoding="utf-8")
    inventory = Path("docs/current-feature-inventory.md").read_text(encoding="utf-8")

    required_release_refs = [
        "Community GA v0.1.0",
        "Community v0.1.1",
        "Published",
        "Ready",
        "https://github.com/Huzefaaa2/cavra/releases/tag/community-v0.1.0",
        "https://github.com/Huzefaaa2/cavra/releases/tag/community-v0.1.1",
        "docs/releases/community-v0.1.0.md",
        "docs/releases/community-v0.1.1.md",
        "docs/release-verifications/community-v0.1.0-post-release-verification.md",
        "docs/release-verifications/community-v0.1.1-post-release-verification.md",
    ]
    required_control_refs = [
        "docs/community-release-index.md",
        "docs/community-release-note-freshness.md",
        "docs/community-release-index-freshness.md",
        "docs/community-maintenance-release-checklist.md",
        "docs/community-ga-release-packet-validation.md",
        "scripts/validate-community-release-readiness-dashboard.py",
        "scripts/validate-boundaries.sh",
    ]
    required_commands = [
        "python3 scripts/validate-release-packets.py",
        "python3 scripts/validate-maintenance-release-evidence.py",
        "python3 scripts/validate-community-release-note-freshness.py",
        "python3 scripts/validate-community-release-index.py",
        "python3 scripts/validate-community-release-readiness-dashboard.py",
        "bash scripts/validate-boundaries.sh .",
        "python3 -m pytest tests/test_release_documentation.py -q",
    ]
    required_workflows = [
        ".github/workflows/community-ci.yml",
        ".github/workflows/security-scan.yml",
        ".github/workflows/release-community.yml",
        ".github/workflows/cavra-governance.yml",
        ".github/workflows/verify-community-release.yml",
    ]

    assert "docs/community-release-readiness-dashboard.md" in readme
    assert "Community-Release-Readiness-Dashboard.md" in wiki_home
    assert "Community release readiness dashboard" in changelog
    assert "Community release readiness dashboard documentation" in roadmap
    assert "Community release readiness dashboard:" in inventory
    assert "Node 24 readiness" in next_slice

    for document in (dashboard, wiki_dashboard):
        for required_ref in required_release_refs + required_control_refs:
            assert required_ref in document
        for command in required_commands:
            assert command in document
        for workflow in required_workflows:
            assert workflow in document
        assert "Enterprise source code" in document
        assert "Node 24 readiness" in document


def test_community_release_readiness_dashboard_validation_is_linked_and_validated() -> None:
    doc = Path("docs/community-release-readiness-dashboard-validation.md").read_text(
        encoding="utf-8"
    )
    wiki_doc = Path(
        "docs/wiki/Community-Release-Readiness-Dashboard-Validation.md"
    ).read_text(encoding="utf-8")
    readme = Path("README.md").read_text(encoding="utf-8")
    changelog = Path("CHANGELOG.md").read_text(encoding="utf-8")
    wiki_home = Path("docs/wiki/Home.md").read_text(encoding="utf-8")
    roadmap = Path("docs/production-roadmap.md").read_text(encoding="utf-8")
    next_slice = Path("docs/roadmap-status-next-slice.md").read_text(encoding="utf-8")
    inventory = Path("docs/current-feature-inventory.md").read_text(encoding="utf-8")
    community_ci = Path(".github/workflows/community-ci.yml").read_text(encoding="utf-8")
    security_scan = Path(".github/workflows/security-scan.yml").read_text(
        encoding="utf-8"
    )
    release_workflow = Path(".github/workflows/release-community.yml").read_text(
        encoding="utf-8"
    )
    governance = Path(".github/workflows/cavra-governance.yml").read_text(
        encoding="utf-8"
    )

    script = "scripts/validate-community-release-readiness-dashboard.py"

    assert "docs/community-release-readiness-dashboard-validation.md" in readme
    assert "Community-Release-Readiness-Dashboard-Validation.md" in wiki_home
    assert "Community release readiness dashboard validation" in changelog
    assert "Community release readiness dashboard validation" in roadmap
    assert "Community release readiness dashboard validation:" in inventory
    assert "Node 24 readiness" in next_slice
    assert script in doc
    assert script in wiki_doc

    for workflow in (community_ci, security_scan, release_workflow, governance):
        assert script in workflow

    result = subprocess.run(
        [sys.executable, script],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert (
        "CAVRA Community release readiness dashboard validation passed."
        in result.stdout
    )


def test_community_ga_user_verifiable_path_is_linked_and_validated() -> None:
    doc = Path("docs/community-ga-user-verifiable-path.md").read_text(encoding="utf-8")
    wiki_doc = Path("docs/wiki/Community-GA-User-Verifiable-Path.md").read_text(
        encoding="utf-8"
    )
    readme = Path("README.md").read_text(encoding="utf-8")
    changelog = Path("CHANGELOG.md").read_text(encoding="utf-8")
    wiki_home = Path("docs/wiki/Home.md").read_text(encoding="utf-8")
    roadmap = Path("docs/production-roadmap.md").read_text(encoding="utf-8")
    next_slice = Path("docs/roadmap-status-next-slice.md").read_text(encoding="utf-8")
    dashboard = Path("docs/community-release-readiness-dashboard.md").read_text(
        encoding="utf-8"
    )
    packet = json.loads(
        Path("docs/release-packets/community-ga-v0.1.0.json").read_text(
            encoding="utf-8"
        )
    )
    verification = json.loads(
        Path(
            "docs/release-verifications/community-v0.1.0-post-release-verification.json"
        ).read_text(encoding="utf-8")
    )
    workflows = [
        Path(".github/workflows/community-ci.yml").read_text(encoding="utf-8"),
        Path(".github/workflows/security-scan.yml").read_text(encoding="utf-8"),
        Path(".github/workflows/release-community.yml").read_text(encoding="utf-8"),
        Path(".github/workflows/cavra-governance.yml").read_text(encoding="utf-8"),
    ]
    script = "scripts/validate-community-ga-path.py"

    for document in (doc, wiki_doc):
        for required in [
            "Policy",
            "Evidence",
            "Console",
            "Go Runtime",
            "Release Verification",
            "Public Boundary",
            "Operator Runbook",
            script,
        ]:
            assert required in document

    assert "docs/community-ga-user-verifiable-path.md" in readme
    assert "Community-GA-User-Verifiable-Path.md" in wiki_home
    assert "user-verifiable Community GA path" in changelog
    assert "Community GA user-verifiable path is documented" in roadmap
    assert "Node 24 readiness" in next_slice
    assert script in dashboard

    assert packet["release_state"] == "ready_for_community_ga"
    assert verification["decision"] == "pass"
    assert all(artifact["checksum_match"] for artifact in verification["artifacts"])

    for workflow in workflows:
        assert f"python {script}" in workflow

    result = subprocess.run(
        [sys.executable, script],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "CAVRA Community GA path validation passed." in result.stdout


def test_production_deployment_guide_validation_is_linked_and_enforced() -> None:
    doc = Path("docs/production-deployment-guide-validation.md").read_text(
        encoding="utf-8"
    )
    wiki_doc = Path("docs/wiki/Production-Deployment-Guide-Validation.md").read_text(
        encoding="utf-8"
    )
    deployment = Path("docs/deployment.md").read_text(encoding="utf-8")
    readiness = Path("docs/production-deployment-validation.md").read_text(
        encoding="utf-8"
    )
    readme = Path("README.md").read_text(encoding="utf-8")
    changelog = Path("CHANGELOG.md").read_text(encoding="utf-8")
    wiki_home = Path("docs/wiki/Home.md").read_text(encoding="utf-8")
    roadmap = Path("docs/production-roadmap.md").read_text(encoding="utf-8")
    next_slice = Path("docs/roadmap-status-next-slice.md").read_text(encoding="utf-8")
    inventory = Path("docs/current-feature-inventory.md").read_text(encoding="utf-8")
    workflows = [
        Path(".github/workflows/community-ci.yml").read_text(encoding="utf-8"),
        Path(".github/workflows/security-scan.yml").read_text(encoding="utf-8"),
        Path(".github/workflows/release-community.yml").read_text(encoding="utf-8"),
        Path(".github/workflows/cavra-governance.yml").read_text(encoding="utf-8"),
        Path(".github/workflows/deploy-sandbox.yml").read_text(encoding="utf-8"),
    ]
    script = "scripts/validate-production-deployment-guide.py"

    for document in (doc, wiki_doc):
        for required in [
            "Install",
            "Configuration",
            "Storage",
            "Backup",
            "Restore",
            "CORS/API",
            "GitHub Pages portal",
            "Evidence artifact root",
            "Persistent stores",
            "Operator Runbook",
            "Public Boundary",
            script,
            "cavra ops stores",
            "cavra ops backup",
            "cavra ops restore",
            "CAVRA_PUBLIC_API_BASE_URL",
            "CAVRA_CORS_ORIGINS",
            "Node 24 readiness",
        ]:
            assert required in document

    assert "docs/production-deployment-guide-validation.md" in readme
    assert "Production-Deployment-Guide-Validation.md" in wiki_home
    assert "production deployment guide validation" in changelog
    assert "Production deployment guide validation is documented" in roadmap
    assert "Production deployment guide validation:" in inventory
    assert "Node 24 readiness" in next_slice
    assert script in deployment
    assert script in readiness

    for workflow in workflows:
        assert f"python {script}" in workflow

    result = subprocess.run(
        [sys.executable, script],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "CAVRA production deployment guide validation passed." in result.stdout


def test_go_enforcement_production_hardening_is_linked_and_enforced() -> None:
    doc = Path("docs/go-enforcement-production-hardening.md").read_text(
        encoding="utf-8"
    )
    wiki_doc = Path("docs/wiki/Go-Enforcement-Production-Hardening.md").read_text(
        encoding="utf-8"
    )
    runtime_readme = Path("go/cavra-runtime/README.md").read_text(encoding="utf-8")
    daemon_doc = Path("docs/go-daemon-transport.md").read_text(encoding="utf-8")
    go_roadmap = Path("docs/go-enforcement-roadmap.md").read_text(encoding="utf-8")
    readme = Path("README.md").read_text(encoding="utf-8")
    changelog = Path("CHANGELOG.md").read_text(encoding="utf-8")
    wiki_home = Path("docs/wiki/Home.md").read_text(encoding="utf-8")
    production_roadmap = Path("docs/production-roadmap.md").read_text(encoding="utf-8")
    next_slice = Path("docs/roadmap-status-next-slice.md").read_text(encoding="utf-8")
    inventory = Path("docs/current-feature-inventory.md").read_text(encoding="utf-8")
    workflows = [
        Path(".github/workflows/community-ci.yml").read_text(encoding="utf-8"),
        Path(".github/workflows/security-scan.yml").read_text(encoding="utf-8"),
        Path(".github/workflows/release-community.yml").read_text(encoding="utf-8"),
        Path(".github/workflows/cavra-governance.yml").read_text(encoding="utf-8"),
    ]
    script = "scripts/validate-go-production-hardening.py"

    for document in (doc, wiki_doc):
        for required in [
            "Unix-socket",
            "gRPC",
            "air-gapped",
            "reproducibility",
            "upgrade validation",
            "performance",
            "operational readiness",
            "Python remains authoritative",
            "BenchmarkEvaluateAllowCommand",
            "go test -bench BenchmarkEvaluateAllowCommand ./runtime",
            "cavra release verify-airgap-bundle",
            "cavra release validate-upgrade",
            "cavra release verify-go-package",
            "Node 24 readiness",
            script,
        ]:
            assert required in document

    assert "docs/go-enforcement-production-hardening.md" in readme
    assert "Go-Enforcement-Production-Hardening.md" in wiki_home
    assert "Go enforcement production hardening" in changelog
    assert "Go enforcement production hardening is documented" in production_roadmap
    assert "Go enforcement production hardening:" in inventory
    assert "Node 24 readiness" in next_slice
    assert "Go enforcement production hardening is documented" in go_roadmap
    assert "BenchmarkEvaluateAllowCommand" in runtime_readme
    assert "gRPC remains a documented future transport" in runtime_readme
    assert "go test -bench BenchmarkEvaluateAllowCommand ./runtime" in daemon_doc

    for workflow in workflows:
        assert f"python {script}" in workflow

    result = subprocess.run(
        [sys.executable, script],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "CAVRA Go production hardening validation passed." in result.stdout


def test_enterprise_integration_validation_is_linked_and_enforced() -> None:
    doc = Path("docs/enterprise-integration-validation.md").read_text(encoding="utf-8")
    wiki_doc = Path("docs/wiki/Enterprise-Integration-Validation.md").read_text(
        encoding="utf-8"
    )
    orchestration_doc = Path("docs/agent-orchestration-architecture.md").read_text(
        encoding="utf-8"
    )
    integrations_doc = Path("docs/integrations.md").read_text(encoding="utf-8")
    connector_doc = Path("docs/connector-execution-hooks.md").read_text(
        encoding="utf-8"
    )
    readme = Path("README.md").read_text(encoding="utf-8")
    changelog = Path("CHANGELOG.md").read_text(encoding="utf-8")
    wiki_home = Path("docs/wiki/Home.md").read_text(encoding="utf-8")
    production_roadmap = Path("docs/production-roadmap.md").read_text(encoding="utf-8")
    next_slice = Path("docs/roadmap-status-next-slice.md").read_text(encoding="utf-8")
    inventory = Path("docs/current-feature-inventory.md").read_text(encoding="utf-8")
    workflows = [
        Path(".github/workflows/community-ci.yml").read_text(encoding="utf-8"),
        Path(".github/workflows/security-scan.yml").read_text(encoding="utf-8"),
        Path(".github/workflows/release-community.yml").read_text(encoding="utf-8"),
        Path(".github/workflows/cavra-governance.yml").read_text(encoding="utf-8"),
    ]
    script = "scripts/validate-enterprise-integration-readiness.py"

    for document in (doc, wiki_doc):
        for required in [
            "GitHub App",
            "orchestrator",
            "GitLab CI",
            "Azure DevOps",
            "Azure Pipelines",
            "SAML",
            "OIDC/RBAC",
            "SIEM",
            "ITSM",
            "Splunk",
            "Microsoft Sentinel",
            "Datadog",
            "Jira",
            "ServiceNow",
            "public-safe",
            "provider credentials",
            "customer data",
            "Enterprise source code",
            "Validation Command",
            "Operator Runbook",
            "Public Boundary",
            "User Stories",
            "Enterprise Challenge Solved",
            "Node 24 readiness",
            script,
        ]:
            assert required in document

    assert "docs/enterprise-integration-validation.md" in readme
    assert "Enterprise-Integration-Validation.md" in wiki_home
    assert "Enterprise integration validation" in changelog
    assert "Enterprise integration validation is documented" in production_roadmap
    assert "Enterprise integration validation:" in inventory
    assert "Node 24 readiness" in next_slice
    assert "The orchestrator should not own policy decisions" in orchestration_doc
    assert "GitLab CI" in integrations_doc
    assert "Azure Pipelines" in integrations_doc
    assert "SAML" in integrations_doc
    assert "Splunk HEC" in connector_doc
    assert "ServiceNow change request API" in connector_doc

    for workflow in workflows:
        assert f"python {script}" in workflow

    result = subprocess.run(
        [sys.executable, script],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "CAVRA enterprise integration validation passed." in result.stdout


def test_production_readiness_procurement_closeout_is_linked_and_enforced() -> None:
    doc = Path("docs/production-readiness-procurement-closeout.md").read_text(
        encoding="utf-8"
    )
    wiki_doc = Path("docs/wiki/Production-Readiness-Procurement-Closeout.md").read_text(
        encoding="utf-8"
    )
    procurement = Path("docs/procurement-readiness.md").read_text(encoding="utf-8")
    operations = Path("docs/persistent-api-operations.md").read_text(encoding="utf-8")
    migrations = Path("docs/evidence-metadata-migrations.md").read_text(
        encoding="utf-8"
    )
    advisory = Path("docs/release-security-advisories.md").read_text(encoding="utf-8")
    readme = Path("README.md").read_text(encoding="utf-8")
    changelog = Path("CHANGELOG.md").read_text(encoding="utf-8")
    wiki_home = Path("docs/wiki/Home.md").read_text(encoding="utf-8")
    production_roadmap = Path("docs/production-roadmap.md").read_text(encoding="utf-8")
    next_slice = Path("docs/roadmap-status-next-slice.md").read_text(encoding="utf-8")
    inventory = Path("docs/current-feature-inventory.md").read_text(encoding="utf-8")
    workflows = [
        Path(".github/workflows/community-ci.yml").read_text(encoding="utf-8"),
        Path(".github/workflows/security-scan.yml").read_text(encoding="utf-8"),
        Path(".github/workflows/release-community.yml").read_text(encoding="utf-8"),
        Path(".github/workflows/cavra-governance.yml").read_text(encoding="utf-8"),
    ]
    script = "scripts/validate-production-readiness-procurement-closeout.py"

    for document in (doc, wiki_doc):
        for required in [
            "performance",
            "concurrency",
            "backup",
            "restore",
            "upgrade",
            "migration",
            "SOC 2",
            "security advisory drill",
            "vulnerability response",
            "final release integrity",
            "SBOM",
            "SLSA provenance",
            "BenchmarkEvaluateAllowCommand",
            "cavra ops backup",
            "cavra ops restore",
            "cavra release verify-go-package",
            "cavra release validate-upgrade",
            "Public Boundary",
            "Operator Runbook",
            "User Stories",
            "Enterprise Challenge Solved",
            "Node 24 readiness",
            script,
        ]:
            assert required in document

    assert "docs/production-readiness-procurement-closeout.md" in readme
    assert "Production-Readiness-Procurement-Closeout.md" in wiki_home
    assert "production readiness procurement closeout" in changelog
    assert "Production readiness procurement closeout is documented" in production_roadmap
    assert "Production readiness procurement closeout:" in inventory
    assert "Node 24 readiness" in next_slice
    assert "SOC 2 Readiness Roadmap" in procurement
    assert "cavra ops backup" in operations
    assert "schema_migrations" in migrations
    assert "cavra-runtime.provenance.intoto.json" in advisory

    for workflow in workflows:
        assert f"python {script}" in workflow

    result = subprocess.run(
        [sys.executable, script],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert (
        "CAVRA production readiness procurement closeout validation passed."
        in result.stdout
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


def test_community_v013_maintenance_planning_is_linked_and_node24_ready() -> None:
    plan = Path("docs/community-v0.1.3-maintenance-planning.md").read_text(
        encoding="utf-8"
    )
    wiki_plan = Path("docs/wiki/Community-v0.1.3-Maintenance-Planning.md").read_text(
        encoding="utf-8"
    )
    readme = Path("README.md").read_text(encoding="utf-8")
    wiki_home = Path("docs/wiki/Home.md").read_text(encoding="utf-8")
    roadmap = Path("docs/production-roadmap.md").read_text(encoding="utf-8")
    inventory = Path("docs/current-feature-inventory.md").read_text(encoding="utf-8")
    changelog = Path("CHANGELOG.md").read_text(encoding="utf-8")

    required_terms = [
        "Community v0.1.3",
        "GitHub Actions Node 24 readiness",
        "actions/checkout@v6",
        "actions/setup-python@v6",
        "FORCE_JAVASCRIPT_ACTIONS_TO_NODE24",
        "current v0.1.3 release artifacts",
        "Public Boundary",
        "Implement Community v1.0.0 release-candidate hardening packet",
    ]
    for document in (plan, wiki_plan):
        for term in required_terms:
            assert term in document

    assert "docs/community-v0.1.3-maintenance-planning.md" in readme
    assert "Community-v0.1.3-Maintenance-Planning.md" in wiki_home
    assert "community-v0.1.3-maintenance-planning.md" in roadmap
    assert "Community v0.1.3 maintenance planning:" in inventory
    assert "Community v0.1.3 maintenance planning" in changelog


def test_community_v013_post_release_evidence_is_current_baseline() -> None:
    release_notes = Path("docs/releases/community-v0.1.3.md").read_text(
        encoding="utf-8"
    )
    post_release = Path(
        "docs/release-verifications/community-v0.1.3-post-release-verification.md"
    ).read_text(encoding="utf-8")
    post_release_json = json.loads(
        Path(
            "docs/release-verifications/community-v0.1.3-post-release-verification.json"
        ).read_text(encoding="utf-8")
    )
    wiki_release_notes = Path("docs/wiki/Community-v0.1.3-Release-Notes.md").read_text(
        encoding="utf-8"
    )
    wiki_post_release = Path(
        "docs/wiki/Community-v0.1.3-Post-Release-Verification.md"
    ).read_text(encoding="utf-8")
    readme = Path("README.md").read_text(encoding="utf-8")
    wiki_home = Path("docs/wiki/Home.md").read_text(encoding="utf-8")
    release_index = Path("docs/community-release-index.md").read_text(encoding="utf-8")
    dashboard = Path("docs/community-release-readiness-dashboard.md").read_text(
        encoding="utf-8"
    )
    changelog = Path("CHANGELOG.md").read_text(encoding="utf-8")

    release_url = "https://github.com/Huzefaaa2/cavra/releases/tag/community-v0.1.3"
    release_notes_path = "docs/releases/community-v0.1.3.md"
    maintenance_path = (
        "docs/release-verifications/community-v0.1.3-maintenance-verification.md"
    )
    post_release_path = (
        "docs/release-verifications/community-v0.1.3-post-release-verification.md"
    )
    wheel_sha = "843cf0c13914e4e9d95ebacd8f0a74aaf4c66969e213e8337d1c0d1c8843cb2e"
    sdist_sha = "83ddaeb4a36502bfa8a5441a15b7b089ac6d5c1dcc58692e942e3ad601d3c29f"

    for document in (release_notes, post_release, wiki_release_notes, wiki_post_release):
        assert release_url in document
        assert wheel_sha in document
        assert sdist_sha in document
        assert "cavra 0.1.3" in document

    assert maintenance_path in release_notes
    assert post_release_path in release_notes
    assert release_notes_path in readme
    assert maintenance_path in readme
    assert post_release_path in readme
    assert "Community-v0.1.3-Release-Notes.md" in wiki_home
    assert "Community-v0.1.3-Maintenance-Verification.md" in wiki_home
    assert "Community-v0.1.3-Post-Release-Verification.md" in wiki_home
    assert "| Community v0.1.3 | Published |" in release_index
    assert "| Community v0.1.3 | Published |" in dashboard
    assert post_release_path in release_index
    assert post_release_path in dashboard
    assert "Published Community v0.1.3 GitHub Release artifacts" in changelog

    assert post_release_json["tag"] == "community-v0.1.3"
    assert post_release_json["version"] == "0.1.3"
    assert post_release_json["release_target"] == (
        "5173db90af69410d27b5cd6ef4274c35e26d6a08"
    )
    assert post_release_json["install_smoke"]["output"] == "cavra 0.1.3"
    assert {artifact["sha256"] for artifact in post_release_json["artifacts"]} == {
        wheel_sha,
        sdist_sha,
    }


def test_community_v100_stabilization_plan_is_linked_and_validated() -> None:
    plan = Path("docs/community-v1.0.0-stabilization-plan.md").read_text(
        encoding="utf-8"
    )
    wiki_plan = Path("docs/wiki/Community-v1.0.0-Stabilization-Plan.md").read_text(
        encoding="utf-8"
    )
    packet = json.loads(
        Path("docs/release-verifications/community-v1.0.0-stabilization-plan.json").read_text(
            encoding="utf-8"
        )
    )
    readme = Path("README.md").read_text(encoding="utf-8")
    wiki_home = Path("docs/wiki/Home.md").read_text(encoding="utf-8")
    roadmap = Path("docs/production-roadmap.md").read_text(encoding="utf-8")
    inventory = Path("docs/current-feature-inventory.md").read_text(encoding="utf-8")
    changelog = Path("CHANGELOG.md").read_text(encoding="utf-8")
    workflows = [
        Path(".github/workflows/community-ci.yml").read_text(encoding="utf-8"),
        Path(".github/workflows/security-scan.yml").read_text(encoding="utf-8"),
        Path(".github/workflows/release-community.yml").read_text(encoding="utf-8"),
        Path(".github/workflows/cavra-governance.yml").read_text(encoding="utf-8"),
    ]
    script = "scripts/validate-community-v100-stabilization.py"
    next_recommendation = (
        "Implement Community v1.0.0 release-candidate hardening packet from the "
        "completed Node 24 readiness baseline with signed artifacts, reproducible "
        "provenance verification, GA announcement checklist, and final operator evidence."
    )

    required_terms = [
        "Community v1.0.0",
        "Node 24 readiness baseline",
        "Release signing",
        "Reproducible provenance",
        "SLSA provenance",
        "SBOM metadata",
        "GA announcement readiness",
        "Final operator evidence",
        "Evidence Console",
        "Public boundary",
        "Enterprise source code",
        "private signing keys",
        "customer records",
        script,
        next_recommendation,
    ]
    for document in (plan, wiki_plan):
        for term in required_terms:
            assert term in document

    assert "docs/community-v1.0.0-stabilization-plan.md" in readme
    assert "docs/release-verifications/community-v1.0.0-stabilization-plan.json" in readme
    assert "Community-v1.0.0-Stabilization-Plan.md" in wiki_home
    assert "docs/community-v1.0.0-stabilization-plan.md" in roadmap
    assert "Community v1.0.0 stabilization planning:" in inventory
    assert "Community v1.0.0 stabilization planning" in changelog

    assert packet["schema_version"] == "cavra.community_v100_stabilization.v1"
    assert packet["status"] == "planned"
    assert packet["target_tag"] == "community-v1.0.0"
    assert packet["baseline_release"] == "community-v0.1.3"
    assert packet["next_recommendation"] == next_recommendation
    assert {item["name"] for item in packet["required_workstreams"]} == {
        "release_signing",
        "reproducible_provenance",
        "ga_announcement_readiness",
        "final_operator_evidence",
    }
    gate_statuses = {item["name"]: item["status"] for item in packet["gates"]}
    assert gate_statuses["Node 24 readiness baseline"] == "ready"
    assert gate_statuses["Public boundary"] == "ready"

    for workflow in workflows:
        assert f"python {script}" in workflow

    result = subprocess.run(
        [sys.executable, script],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_community_v100_rc_hardening_is_linked_and_validated() -> None:
    doc = Path("docs/community-v1.0.0-release-candidate-hardening.md").read_text(
        encoding="utf-8"
    )
    wiki_doc = Path("docs/wiki/Community-v1.0.0-Release-Candidate-Hardening.md").read_text(
        encoding="utf-8"
    )
    packet = json.loads(
        Path(
            "docs/release-verifications/community-v1.0.0-release-candidate-hardening.json"
        ).read_text(encoding="utf-8")
    )
    readme = Path("README.md").read_text(encoding="utf-8")
    wiki_home = Path("docs/wiki/Home.md").read_text(encoding="utf-8")
    roadmap = Path("docs/production-roadmap.md").read_text(encoding="utf-8")
    inventory = Path("docs/current-feature-inventory.md").read_text(encoding="utf-8")
    changelog = Path("CHANGELOG.md").read_text(encoding="utf-8")
    workflows = [
        Path(".github/workflows/community-ci.yml").read_text(encoding="utf-8"),
        Path(".github/workflows/security-scan.yml").read_text(encoding="utf-8"),
        Path(".github/workflows/release-community.yml").read_text(encoding="utf-8"),
        Path(".github/workflows/cavra-governance.yml").read_text(encoding="utf-8"),
    ]
    script = "scripts/validate-community-v100-rc-hardening.py"
    next_recommendation = (
        "Prepare Community v1.0.0 release-candidate publication from the completed "
        "Node 24 readiness baseline with signed artifact verification, provenance "
        "evidence, release notes, and announcement readiness."
    )

    required_terms = [
        "Community v1.0.0",
        "release-candidate",
        "Node 24 readiness baseline",
        "Signed artifacts",
        "SHA-256",
        "detached signatures",
        "keyless attestation",
        "Reproducible provenance verification",
        "SLSA provenance",
        "SBOM",
        "GA announcement checklist",
        "Final operator evidence",
        "Evidence Console",
        "Public boundary",
        "Enterprise source code",
        "private signing keys",
        "customer records",
        script,
        next_recommendation,
    ]
    for document in (doc, wiki_doc):
        for term in required_terms:
            assert term in document

    assert "docs/community-v1.0.0-release-candidate-hardening.md" in readme
    assert (
        "docs/release-verifications/community-v1.0.0-release-candidate-hardening.json"
        in readme
    )
    assert "Community-v1.0.0-Release-Candidate-Hardening.md" in wiki_home
    assert "docs/community-v1.0.0-release-candidate-hardening.md" in roadmap
    assert "Community v1.0.0 release-candidate hardening:" in inventory
    assert "Community v1.0.0 release-candidate hardening" in changelog

    assert packet["schema_version"] == "cavra.community_v100_rc_hardening.v1"
    assert packet["status"] == "ready_for_rc_publication"
    assert packet["target_tag"] == "community-v1.0.0"
    assert packet["baseline_release"] == "community-v0.1.3"
    assert packet["next_recommendation"] == next_recommendation
    assert {item["name"] for item in packet["required_workstreams"]} == {
        "signed_artifacts",
        "reproducible_provenance_verification",
        "ga_announcement_checklist",
        "final_operator_evidence",
    }
    gate_statuses = {item["name"]: item["status"] for item in packet["gates"]}
    assert gate_statuses["Node 24 readiness baseline"] == "ready"
    assert gate_statuses["Public boundary"] == "ready"
    assert packet["decision"]["status"] == "approve_for_rc_preparation"
    assert packet["accepted_risks"][0]["id"] == "rc-artifacts-not-yet-published"

    for workflow in workflows:
        assert f"python {script}" in workflow

    result = subprocess.run(
        [sys.executable, script],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_community_v100_rc_publication_is_linked_and_validated() -> None:
    doc = Path("docs/community-v1.0.0-release-candidate-publication.md").read_text(
        encoding="utf-8"
    )
    wiki_doc = Path("docs/wiki/Community-v1.0.0-Release-Candidate-Publication.md").read_text(
        encoding="utf-8"
    )
    readiness = Path(
        "docs/release-verifications/community-v1.0.0-rc.1-publication-readiness.md"
    ).read_text(encoding="utf-8")
    wiki_readiness = Path(
        "docs/wiki/Community-v1.0.0-rc.1-Publication-Verification.md"
    ).read_text(encoding="utf-8")
    packet = json.loads(
        Path(
            "docs/release-verifications/community-v1.0.0-release-candidate-publication.json"
        ).read_text(encoding="utf-8")
    )
    readme = Path("README.md").read_text(encoding="utf-8")
    wiki_home = Path("docs/wiki/Home.md").read_text(encoding="utf-8")
    roadmap = Path("docs/production-roadmap.md").read_text(encoding="utf-8")
    inventory = Path("docs/current-feature-inventory.md").read_text(encoding="utf-8")
    changelog = Path("CHANGELOG.md").read_text(encoding="utf-8")
    workflows = [
        Path(".github/workflows/community-ci.yml").read_text(encoding="utf-8"),
        Path(".github/workflows/security-scan.yml").read_text(encoding="utf-8"),
        Path(".github/workflows/release-community.yml").read_text(encoding="utf-8"),
        Path(".github/workflows/cavra-governance.yml").read_text(encoding="utf-8"),
    ]
    script = "scripts/validate-community-v100-rc-publication.py"
    release_url = "https://github.com/Huzefaaa2/cavra/releases/tag/community-v1.0.0-rc.1"
    next_recommendation = (
        "Publish Community v1.0.0 release-candidate artifacts from the completed "
        "Node 24 readiness baseline and record signed artifact checksums, provenance, "
        "GitHub Release links, and post-publication verification evidence."
    )

    required_terms = [
        "Community v1.0.0 RC1",
        "community-v1.0.0-rc.1",
        "Node 24 readiness baseline",
        "signed artifact verification",
        "SHA-256",
        "detached signatures",
        "keyless attestation",
        "SBOM",
        "SLSA provenance",
        "dry-run",
        "Public boundary",
        "Enterprise source code",
        "private signing keys",
        "customer records",
        next_recommendation,
    ]
    for document in (doc, wiki_doc, readiness, wiki_readiness):
        for term in required_terms:
            assert term in document
        assert release_url in document

    assert "docs/community-v1.0.0-release-candidate-publication.md" in readme
    assert "docs/releases/community-v1.0.0-rc.1.md" in readme
    assert (
        "docs/release-verifications/community-v1.0.0-rc.1-publication-readiness.md"
        in readme
    )
    assert (
        "docs/release-verifications/community-v1.0.0-release-candidate-publication.json"
        in readme
    )
    assert "Community-v1.0.0-Release-Candidate-Publication.md" in wiki_home
    assert "Community-v1.0.0-rc.1-Release-Notes.md" in wiki_home
    assert "Community-v1.0.0-rc.1-Publication-Verification.md" in wiki_home
    assert "docs/community-v1.0.0-release-candidate-publication.md" in roadmap
    assert "Community v1.0.0 release-candidate publication:" in inventory
    assert "Community v1.0.0 RC1 publication preparation" in changelog

    assert packet["schema_version"] == "cavra.community_v100_rc_publication.v1"
    assert packet["status"] == "dry_run_publication_ready"
    assert packet["tag"] == "community-v1.0.0-rc.1"
    assert packet["version"] == "1.0.0rc1"
    assert packet["planned_github_release"] == release_url
    assert packet["next_recommendation"] == next_recommendation
    gate_statuses = {item["name"]: item["status"] for item in packet["gates"]}
    assert gate_statuses["Node 24 readiness baseline"] == "pass"
    assert gate_statuses["Signed artifact verification"] == "pending_real_artifacts"
    assert gate_statuses["Provenance evidence"] == "pending_real_artifacts"
    assert gate_statuses["Public boundary"] == "pass"
    assert packet["decision"]["status"] == "approve_dry_run_publication_readiness"

    for workflow in workflows:
        assert f"python {script}" in workflow

    result = subprocess.run(
        [sys.executable, script],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_community_v100_rc1_post_publication_is_linked_and_validated() -> None:
    doc = Path(
        "docs/release-verifications/community-v1.0.0-rc.1-post-publication-verification.md"
    ).read_text(encoding="utf-8")
    wiki_doc = Path(
        "docs/wiki/Community-v1.0.0-rc.1-Post-Publication-Verification.md"
    ).read_text(encoding="utf-8")
    packet = json.loads(
        Path(
            "docs/release-verifications/community-v1.0.0-rc.1-post-publication-verification.json"
        ).read_text(encoding="utf-8")
    )
    release_notes = Path("docs/releases/community-v1.0.0-rc.1.md").read_text(
        encoding="utf-8"
    )
    wiki_release_notes = Path(
        "docs/wiki/Community-v1.0.0-rc.1-Release-Notes.md"
    ).read_text(encoding="utf-8")
    readme = Path("README.md").read_text(encoding="utf-8")
    wiki_home = Path("docs/wiki/Home.md").read_text(encoding="utf-8")
    roadmap = Path("docs/production-roadmap.md").read_text(encoding="utf-8")
    inventory = Path("docs/current-feature-inventory.md").read_text(encoding="utf-8")
    changelog = Path("CHANGELOG.md").read_text(encoding="utf-8")
    release_index = Path("docs/community-release-index.md").read_text(encoding="utf-8")
    dashboard = Path("docs/community-release-readiness-dashboard.md").read_text(
        encoding="utf-8"
    )
    wiki_index = Path("docs/wiki/Community-Release-Index.md").read_text(
        encoding="utf-8"
    )
    wiki_dashboard = Path("docs/wiki/Community-Release-Readiness-Dashboard.md").read_text(
        encoding="utf-8"
    )
    workflows = [
        Path(".github/workflows/community-ci.yml").read_text(encoding="utf-8"),
        Path(".github/workflows/security-scan.yml").read_text(encoding="utf-8"),
        Path(".github/workflows/release-community.yml").read_text(encoding="utf-8"),
        Path(".github/workflows/cavra-governance.yml").read_text(encoding="utf-8"),
    ]
    script = "scripts/validate-community-v100-rc-post-publication.py"
    release_url = "https://github.com/Huzefaaa2/cavra/releases/tag/community-v1.0.0-rc.1"
    next_recommendation = (
        "Advance Community v1.0.0 RC1 feedback from the completed Node 24 "
        "readiness baseline into GA release readiness by validating upgrade notes, "
        "installer paths, announcement copy, and final GA evidence gates."
    )
    wheel_sha = "6d06bd04965d3b1340ecacf007bc39111c8a8d5d0a73ee32f44aeb06ebb1be01"
    sdist_sha = "f4312e51a4d4180387982eafa86f301c584be5af147ba09098d733d187662e0c"

    required_terms = [
        "Community v1.0.0 RC1",
        "community-v1.0.0-rc.1",
        "1.0.0rc1",
        "Node 24 readiness baseline",
        "SHA-256",
        "provenance",
        "cavra 1.0.0rc1",
        wheel_sha,
        sdist_sha,
        "detached signature",
        "keyless attestation",
        "Public boundary",
        "Enterprise source code",
        "private signing keys",
        "customer records",
        next_recommendation,
    ]
    for document in (doc, wiki_doc, release_notes, wiki_release_notes):
        for term in required_terms:
            assert term in document
        assert release_url in document

    assert "docs/releases/community-v1.0.0-rc.1.md" in readme
    assert (
        "docs/release-verifications/community-v1.0.0-rc.1-post-publication-verification.md"
        in readme
    )
    assert (
        "docs/release-verifications/community-v1.0.0-rc.1-post-publication-verification.json"
        in readme
    )
    assert "Community-v1.0.0-rc.1-Release-Notes.md" in wiki_home
    assert "Community-v1.0.0-rc.1-Post-Publication-Verification.md" in wiki_home
    assert "| Community v1.0.0 RC1 | Published |" in release_index
    assert "| Community v1.0.0 RC1 | Published |" in dashboard
    assert "| Ready |" in dashboard
    for rollup in (release_index, dashboard, wiki_index, wiki_dashboard):
        assert "docs/release-verifications/community-v1.0.0-rc.1-post-publication-verification.md" in rollup
        assert next_recommendation in rollup
    assert "Community v1.0.0 RC1 post-publication verification" in roadmap
    assert "Community v1.0.0 RC1 post-publication verification" in inventory
    assert "Community v1.0.0 RC1 post-publication verification" in changelog
    assert next_recommendation in readme
    assert next_recommendation in roadmap
    assert next_recommendation in inventory

    assert packet["schema_version"] == "cavra.community_v100_rc_post_publication.v1"
    assert packet["status"] == "published"
    assert packet["tag"] == "community-v1.0.0-rc.1"
    assert packet["version"] == "1.0.0rc1"
    assert packet["release_url"] == release_url
    assert packet["release_target"] == "e04ba0025f00b13bf05ab468669bcb3fb494eb89"
    assert packet["install_smoke"]["output"] == "cavra 1.0.0rc1"
    assert packet["node24_readiness_baseline"] == "pass"
    assert packet["next_recommendation"] == next_recommendation
    artifact_hashes = {artifact["name"]: artifact["sha256"] for artifact in packet["artifacts"]}
    assert artifact_hashes["cavra-1.0.0rc1-py3-none-any.whl"] == wheel_sha
    assert artifact_hashes["cavra-1.0.0rc1.tar.gz"] == sdist_sha
    assert packet["public_boundary"]["enterprise_source_included"] is False
    assert packet["signature_evidence"]["checksum_file_recorded"] is True
    assert packet["signature_evidence"]["provenance_file_recorded"] is True
    assert packet["signature_evidence"]["detached_signature_attached"] is False
    assert packet["signature_evidence"]["keyless_attestation_attached"] is False

    for workflow in workflows:
        assert f"python {script}" in workflow

    result = subprocess.run(
        [sys.executable, script],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
