#!/usr/bin/env python3
"""Validate public Community release readiness dashboard freshness."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


ALLOWED_STATES = {"Published", "Dry run"}
ALLOWED_READINESS = {"Ready", "Pending real artifacts"}
REQUIRED_CONTROL_EVIDENCE = {
    "docs/community-release-index.md",
    "docs/community-release-note-freshness.md",
    "docs/community-release-index-freshness.md",
    "docs/community-maintenance-release-checklist.md",
    "docs/community-ga-release-packet-validation.md",
    "scripts/validate-boundaries.sh",
    "scripts/validate-community-release-readiness-dashboard.py",
}
REQUIRED_COMMANDS = {
    "python3 scripts/validate-release-packets.py",
    "python3 scripts/validate-maintenance-release-evidence.py",
    "python3 scripts/validate-community-release-note-freshness.py",
    "python3 scripts/validate-community-release-index.py",
    "python3 scripts/validate-community-release-readiness-dashboard.py",
    "python3 scripts/validate-community-v100-rc-post-publication.py",
    "python3 scripts/validate-community-v100-ga-readiness.py",
    "python3 scripts/validate-community-v100-ga-publication-package.py",
    "bash scripts/validate-boundaries.sh .",
    "python3 -m pytest tests/test_release_documentation.py -q",
}
REQUIRED_WORKFLOWS = {
    ".github/workflows/community-ci.yml",
    ".github/workflows/security-scan.yml",
    ".github/workflows/release-community.yml",
    ".github/workflows/cavra-governance.yml",
    ".github/workflows/verify-community-release.yml",
}


@dataclass(frozen=True)
class DashboardRow:
    release: str
    state: str
    release_url: str
    release_evidence: str
    verification: str
    readiness: str
    next_action: str


@dataclass(frozen=True)
class IndexRow:
    release: str
    state: str
    release_url: str
    release_notes: str
    verification_packet: str
    next_action: str


def _strip_cell(value: str) -> str:
    value = value.strip()
    if value.startswith("<") and value.endswith(">"):
        return value[1:-1]
    if value.startswith("`") and value.endswith("`"):
        return value[1:-1]
    return value


def _parse_dashboard_rows(text: str) -> list[DashboardRow]:
    rows: list[DashboardRow] = []
    for line in text.splitlines():
        if not line.startswith("| Community"):
            continue
        cells = [_strip_cell(cell) for cell in line.strip().strip("|").split("|")]
        if len(cells) != 7:
            raise ValueError(f"invalid dashboard row shape: {line}")
        rows.append(DashboardRow(*cells))
    return rows


def _parse_index_rows(text: str) -> list[IndexRow]:
    rows: list[IndexRow] = []
    for line in text.splitlines():
        if not line.startswith("| Community"):
            continue
        cells = [_strip_cell(cell) for cell in line.strip().strip("|").split("|")]
        if len(cells) != 6:
            raise ValueError(f"invalid release index row shape: {line}")
        rows.append(IndexRow(*cells))
    return rows


def _validate_dashboard_document(
    *, root: Path, text: str, dashboard_name: str, index_rows: dict[str, IndexRow]
) -> list[str]:
    errors: list[str] = []
    normalized_text = " ".join(text.split())

    try:
        rows = _parse_dashboard_rows(text)
    except ValueError as exc:
        return [f"{dashboard_name}: {exc}"]

    if not rows:
        errors.append(f"{dashboard_name}: no Community release readiness rows found")

    dashboard_rows = {row.release: row for row in rows}
    for release, index_row in index_rows.items():
        row = dashboard_rows.get(release)
        if row is None:
            errors.append(f"{dashboard_name}: missing indexed release {release}")
            continue
        if row.state != index_row.state:
            errors.append(
                f"{dashboard_name}: {release} state {row.state!r} does not match index "
                f"{index_row.state!r}"
            )
        if row.release_url != index_row.release_url:
            errors.append(f"{dashboard_name}: {release} release URL does not match index")
        if row.release_evidence != index_row.release_notes:
            errors.append(f"{dashboard_name}: {release} release evidence does not match index")
        if row.verification != index_row.verification_packet:
            errors.append(f"{dashboard_name}: {release} verification does not match index")
        if row.next_action != index_row.next_action:
            errors.append(f"{dashboard_name}: {release} next action does not match index")
        if row.state not in ALLOWED_STATES:
            errors.append(f"{dashboard_name}: {release} has invalid state {row.state!r}")
        if row.readiness not in ALLOWED_READINESS:
            errors.append(
                f"{dashboard_name}: {release} has invalid readiness {row.readiness!r}"
            )
        for public_path in (row.release_evidence, row.verification):
            if not (root / public_path).exists():
                errors.append(f"{dashboard_name}: {release} missing path {public_path}")

    for evidence in REQUIRED_CONTROL_EVIDENCE:
        if evidence not in text:
            errors.append(f"{dashboard_name}: missing control evidence {evidence}")
    for command in REQUIRED_COMMANDS:
        if command not in text:
            errors.append(f"{dashboard_name}: missing verification command {command}")
    for workflow in REQUIRED_WORKFLOWS:
        if workflow not in text:
            errors.append(f"{dashboard_name}: missing CI workflow {workflow}")

    boundary_terms = (
        "Enterprise source code",
        "paid policy packs",
        "SaaS backend implementation",
        "private keys",
        "customer records",
    )
    for term in boundary_terms:
        if term not in normalized_text:
            errors.append(f"{dashboard_name}: missing boundary term {term}")

    return errors


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    dashboard_path = root / "docs" / "community-release-readiness-dashboard.md"
    wiki_dashboard_path = (
        root / "docs" / "wiki" / "Community-Release-Readiness-Dashboard.md"
    )
    index_path = root / "docs" / "community-release-index.md"
    readme_path = root / "README.md"
    wiki_home_path = root / "docs" / "wiki" / "Home.md"

    for path in (
        dashboard_path,
        wiki_dashboard_path,
        index_path,
        readme_path,
        wiki_home_path,
    ):
        if not path.exists():
            errors.append(f"missing required file: {path}")
    if errors:
        return errors

    try:
        index_rows = {
            row.release: row
            for row in _parse_index_rows(index_path.read_text(encoding="utf-8"))
        }
    except ValueError as exc:
        return [str(exc)]

    if not index_rows:
        errors.append("release index has no Community release rows")

    readme = readme_path.read_text(encoding="utf-8")
    wiki_home = wiki_home_path.read_text(encoding="utf-8")
    if "docs/community-release-readiness-dashboard.md" not in readme:
        errors.append("README does not link docs/community-release-readiness-dashboard.md")
    if "Community-Release-Readiness-Dashboard.md" not in wiki_home:
        errors.append("wiki home does not link Community-Release-Readiness-Dashboard.md")

    for dashboard_file in (dashboard_path, wiki_dashboard_path):
        errors.extend(
            _validate_dashboard_document(
                root=root,
                text=dashboard_file.read_text(encoding="utf-8"),
                dashboard_name=str(dashboard_file.relative_to(root)),
                index_rows=index_rows,
            )
        )

    workflows_to_check = {
        root / ".github" / "workflows" / "community-ci.yml",
        root / ".github" / "workflows" / "security-scan.yml",
        root / ".github" / "workflows" / "release-community.yml",
        root / ".github" / "workflows" / "cavra-governance.yml",
    }
    script_ref = "scripts/validate-community-release-readiness-dashboard.py"
    for workflow in workflows_to_check:
        if script_ref not in workflow.read_text(encoding="utf-8"):
            errors.append(f"{workflow.relative_to(root)} does not run {script_ref}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate CAVRA Community release readiness dashboard freshness."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("."),
        help="Repository root to validate.",
    )
    args = parser.parse_args()

    errors = validate(args.root.resolve())
    if errors:
        print("CAVRA Community release readiness dashboard validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("CAVRA Community release readiness dashboard validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
