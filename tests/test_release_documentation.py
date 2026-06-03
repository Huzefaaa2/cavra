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
