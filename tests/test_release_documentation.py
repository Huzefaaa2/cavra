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
