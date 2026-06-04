import json
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
    assert "Community-GA-Release-Packet-Template.md" in wiki_home
    assert "Community GA release packet" in release_policy
    assert "Community GA release packet template" in checklist
    assert "community-ga-release-packet.schema.json" in template
    assert "community-ga-release-packet.example.json" in template
    assert "Public Boundary Review" in template
    assert "Public Boundary Review" in wiki_template

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
    assert "JSON schema validation" in next_slice
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
        "Add automated JSON schema validation for Community GA release packets in CI."
    )
