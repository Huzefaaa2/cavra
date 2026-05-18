from pathlib import Path

import yaml


def _load_yaml(path: str) -> dict[str, object]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def test_live_github_governance_workflow_is_required_check_candidate() -> None:
    workflow_path = ".github/workflows/cavra-governance.yml"
    workflow = _load_yaml(workflow_path)
    text = Path(workflow_path).read_text(encoding="utf-8")

    assert workflow["jobs"]["cavra"]["name"] == "cavra-required-check"
    assert "cavra policy validate" in text
    assert "ruff check src/ tests/" in text
    assert "pytest -q" in text
    assert "cavra evidence verify .cavra/evidence/required-check" in text
    assert "cavra evidence verify-attestation" in text
    assert "cavra-required-check-evidence" in text


def test_github_required_check_templates_parse_and_verify_evidence() -> None:
    for workflow_path in [
        "examples/github-actions/cavra-required-check.yml",
        "examples/github-actions/cavra-enterprise-enforcement.yml",
    ]:
        workflow = _load_yaml(workflow_path)
        text = Path(workflow_path).read_text(encoding="utf-8")

        assert workflow["jobs"]["cavra"]["name"].startswith("cavra-")
        assert "cavra policy validate" in text
        assert "cavra evidence verify" in text
        assert "cavra evidence verify-attestation" in text


def test_gitlab_required_check_template_parses_and_exports_artifacts() -> None:
    pipeline_path = "examples/gitlab-ci/cavra-required-check.gitlab-ci.yml"
    pipeline = _load_yaml(pipeline_path)
    text = Path(pipeline_path).read_text(encoding="utf-8")

    job = pipeline["cavra-required-check"]
    assert job["stage"] == "governance"
    assert "cavra evidence verify" in text
    assert "cavra evidence verify-attestation" in text
    assert ".cavra/evidence/attestation/" in job["artifacts"]["paths"]
