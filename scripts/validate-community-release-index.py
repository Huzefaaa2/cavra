#!/usr/bin/env python3
"""Validate public Community release index freshness.

This script intentionally validates public Community release documentation only.
It does not load Enterprise packages, contact private license services, or
inspect private release registries.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


ALLOWED_STATES = {"Published", "Dry run"}
GITHUB_RELEASE_PREFIX = "https://github.com/Huzefaaa2/cavra/releases/tag/community-v"


@dataclass(frozen=True)
class ReleaseIndexRow:
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


def _parse_release_rows(index_text: str) -> list[ReleaseIndexRow]:
    rows: list[ReleaseIndexRow] = []
    for line in index_text.splitlines():
        if not line.startswith("| Community"):
            continue
        cells = [_strip_cell(cell) for cell in line.strip().strip("|").split("|")]
        if len(cells) != 6:
            raise ValueError(f"invalid release index row shape: {line}")
        rows.append(ReleaseIndexRow(*cells))
    return rows


def _wiki_page_exists_and_is_linked(
    *, root: Path, wiki_home: str, version: str, suffix: str
) -> bool:
    wiki_dir = root / "docs" / "wiki"
    matches = sorted(wiki_dir.glob(f"*{version}*{suffix}.md"))
    return any(match.name in wiki_home for match in matches)


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    index_path = root / "docs" / "community-release-index.md"
    readme_path = root / "README.md"
    wiki_home_path = root / "docs" / "wiki" / "Home.md"

    if not index_path.exists():
        return [f"missing release index: {index_path}"]
    if not readme_path.exists():
        return [f"missing README: {readme_path}"]
    if not wiki_home_path.exists():
        return [f"missing wiki home: {wiki_home_path}"]

    index_text = index_path.read_text(encoding="utf-8")
    readme = readme_path.read_text(encoding="utf-8")
    wiki_home = wiki_home_path.read_text(encoding="utf-8")

    if "docs/community-release-index.md" not in readme:
        errors.append("README does not link docs/community-release-index.md")
    if "Community-Release-Index.md" not in wiki_home:
        errors.append("wiki home does not link Community-Release-Index.md")

    try:
        rows = _parse_release_rows(index_text)
    except ValueError as exc:
        return [str(exc)]

    if not rows:
        errors.append("release index has no Community release rows")

    for row in rows:
        if row.state not in ALLOWED_STATES:
            errors.append(
                f"{row.release}: invalid state {row.state!r}; "
                f"expected one of {sorted(ALLOWED_STATES)}"
            )
        if not row.release_url.startswith(GITHUB_RELEASE_PREFIX):
            errors.append(f"{row.release}: invalid Community GitHub Release URL")
            version = ""
        else:
            version = row.release_url.rsplit("/community-", maxsplit=1)[-1]

        if not row.next_action:
            errors.append(f"{row.release}: missing next action")

        notes_path = root / row.release_notes
        verification_path = root / row.verification_packet
        if not notes_path.exists():
            errors.append(f"{row.release}: missing release notes {row.release_notes}")
            notes = ""
        else:
            notes = notes_path.read_text(encoding="utf-8")

        if not verification_path.exists():
            errors.append(
                f"{row.release}: missing verification packet {row.verification_packet}"
            )
            verification = ""
        else:
            verification = verification_path.read_text(encoding="utf-8")

        for public_doc_path in (row.release_notes, row.verification_packet):
            if public_doc_path not in readme:
                errors.append(f"{row.release}: README does not link {public_doc_path}")

        if row.release_url not in notes:
            errors.append(f"{row.release}: release notes do not link GitHub Release")
        if row.verification_packet not in notes:
            errors.append(f"{row.release}: release notes do not link verification packet")

        if row.state == "Dry run":
            dry_run_text = f"{notes}\n{verification}".lower()
            if "dry-run" not in dry_run_text and "dry run" not in dry_run_text:
                errors.append(f"{row.release}: dry-run record is not marked as dry run")

        if version:
            if not _wiki_page_exists_and_is_linked(
                root=root, wiki_home=wiki_home, version=version, suffix="Release-Notes"
            ):
                errors.append(
                    f"{row.release}: wiki home does not link release notes for {version}"
                )
            if not _wiki_page_exists_and_is_linked(
                root=root, wiki_home=wiki_home, version=version, suffix="Verification"
            ):
                errors.append(
                    f"{row.release}: wiki home does not link verification for {version}"
                )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate CAVRA Community release index freshness."
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
        print("CAVRA Community release index validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("CAVRA Community release index validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
