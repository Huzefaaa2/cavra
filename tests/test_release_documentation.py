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
    assert "production deployment guide coverage" in next_slice
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
    assert "production deployment guide coverage" in next_slice
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
    assert "production deployment guide coverage" in next_slice

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
    assert module.DEFAULT_TAG == "community-v0.1.0"


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
    assert "production deployment guide coverage" in next_slice
    assert "release notes" in checklist
    assert "community-maintenance-release.schema.json" in template
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
    assert "production deployment guide coverage" in next_slice
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


def test_community_v011_maintenance_dry_run_is_linked_and_validated() -> None:
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
    assert "Community-v0.1.1-Release-Notes.md" in wiki_home
    assert "Community-v0.1.1-Maintenance-Verification.md" in wiki_home
    assert "dry-run release notes" in wiki_release_notes
    assert "ready_with_accepted_risk" in wiki_verification
    assert "Community v0.1.1 maintenance-release dry-run notes" in changelog
    assert "community-v0.1.1-maintenance-verification.md" in roadmap
    assert "production deployment guide coverage" in next_slice

    assert verification_json["schema_version"] == "cavra.community_maintenance_release.v1"
    assert verification_json["packet_id"] == "community-v0.1.1-maintenance-verification"
    assert verification_json["release_state"] == "ready_with_accepted_risk"
    assert verification_json["tag"] == "community-v0.1.1"
    assert verification_json["release_notes"] == release_notes_path
    assert verification_json["verification_packet"] == verification_path
    assert {gate["name"] for gate in verification_json["gates"]} == required_gates
    assert {
        gate["name"]
        for gate in verification_json["gates"]
        if gate["status"] == "warn"
    } == {"Verification workflow", "Artifact checksums", "Install smoke"}
    assert verification_json["public_boundary"]["enterprise_source_included"] is False
    assert verification_json["public_boundary"]["paid_policy_packs_included"] is False
    assert verification_json["public_boundary"]["customer_records_included"] is False
    assert verification_json["public_boundary"]["private_keys_included"] is False
    assert verification_json["accepted_risks"][0]["severity"] == "low"
    assert verification_json["decision"]["status"] == "defer"
    assert "production deployment guide coverage" in verification_json["next_recommendation"]

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
    v010_notes = "docs/releases/community-v0.1.0.md"
    v011_notes = "docs/releases/community-v0.1.1.md"
    v010_verification = (
        "docs/release-verifications/community-v0.1.0-post-release-verification.md"
    )
    v011_verification = (
        "docs/release-verifications/community-v0.1.1-maintenance-verification.md"
    )

    assert "docs/community-release-index.md" in readme
    assert "Community-Release-Index.md" in wiki_home
    assert "Community release index" in changelog
    assert "Community release index documentation" in roadmap
    assert "production deployment guide coverage" in next_slice
    assert "Community release index:" in inventory

    for document in (release_index, wiki_release_index):
        assert "Community GA v0.1.0" in document
        assert "Community v0.1.1" in document
        assert "Published" in document
        assert "Dry run" in document
        assert v010_release in document
        assert v011_release in document
        assert v010_notes in document
        assert v011_notes in document
        assert v010_verification in document
        assert v011_verification in document
        assert "scripts/validate-community-release-note-freshness.py" in document
        assert "scripts/validate-community-release-index.py" in document
        assert "production deployment guide coverage" in document


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
    assert "production deployment guide coverage" in next_slice

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
        "Dry run",
        "Ready",
        "Pending real artifacts",
        "https://github.com/Huzefaaa2/cavra/releases/tag/community-v0.1.0",
        "https://github.com/Huzefaaa2/cavra/releases/tag/community-v0.1.1",
        "docs/releases/community-v0.1.0.md",
        "docs/releases/community-v0.1.1.md",
        "docs/release-verifications/community-v0.1.0-post-release-verification.md",
        "docs/release-verifications/community-v0.1.1-maintenance-verification.md",
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
    assert "production deployment guide coverage" in next_slice

    for document in (dashboard, wiki_dashboard):
        for required_ref in required_release_refs + required_control_refs:
            assert required_ref in document
        for command in required_commands:
            assert command in document
        for workflow in required_workflows:
            assert workflow in document
        assert "Enterprise source code" in document
        assert "production deployment guide coverage" in document


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
    assert "production deployment guide coverage" in next_slice
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
    assert "production deployment guide coverage" in next_slice
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
