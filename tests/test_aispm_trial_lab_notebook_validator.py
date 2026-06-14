import json
import subprocess
import sys
from pathlib import Path


def test_aispm_trial_lab_notebook_publication_validator_passes() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate-aispm-trial-lab-notebook.py"],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    assert result.returncode == 0, result.stdout
    assert "publication validation passed" in result.stdout


def test_aispm_trial_lab_notebook_validator_is_wired_into_ci_and_release() -> None:
    command = "python scripts/validate-aispm-trial-lab-notebook.py --check-summary"

    community_ci = Path(".github/workflows/community-ci.yml").read_text(encoding="utf-8")
    release_community = Path(".github/workflows/release-community.yml").read_text(
        encoding="utf-8"
    )

    assert command in community_ci
    assert command in release_community


def test_aispm_trial_lab_notebook_publication_summary_is_fresh() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "scripts/validate-aispm-trial-lab-notebook.py",
            "--check-summary",
        ],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    assert result.returncode == 0, result.stdout
    assert "publication validation passed" in result.stdout


def test_aispm_trial_lab_notebook_publication_summary_artifacts_are_reviewer_ready() -> None:
    summary_json = Path(
        "docs/release-verifications/aispm-trial-lab-notebook-publication-readiness-summary.json"
    )
    summary_markdown = Path(
        "docs/release-verifications/aispm-trial-lab-notebook-publication-readiness-summary.md"
    )

    payload = json.loads(summary_json.read_text(encoding="utf-8"))
    markdown = summary_markdown.read_text(encoding="utf-8")

    assert payload["overall_status"] == "ready"
    assert payload["counts"]["wiki_pages"] == 3
    assert payload["counts"]["blockers"] == 0
    assert payload["counts"]["enterprise_readiness_gates"] == 9
    assert payload["counts"]["enterprise_readiness_gates_ready"] == 9
    assert payload["enterprise_readiness_sync"]["status"] == "ready"
    assert "announcement-closeout" in {
        gate["gate_id"] for gate in payload["enterprise_readiness_sync"]["gates"]
    }
    assert {page["page_id"] for page in payload["pages"]} == {
        "trial-lab-overview",
        "trial-access-flow",
        "trial-closeout",
    }
    assert "## Public Safety" in markdown
    assert "| Wiki pages | 3 | 3 |" in markdown
    assert "| Enterprise readiness gates | 9 | 9 |" in markdown
    assert "| announcement-closeout | Announcement Closeout | `ready` |" in markdown
    assert "## Enterprise Trial Readiness Sync" in markdown
    assert "- None." in markdown
