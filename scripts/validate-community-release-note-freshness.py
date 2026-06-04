#!/usr/bin/env python3
"""Validate Community release notes are linked to matching verification evidence."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable


DEFAULT_RELEASE_NOTE_GLOB = "docs/releases/community-v*.md"
README = Path("README.md")
WIKI_HOME = Path("docs/wiki/Home.md")


def _relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _contains_any(haystack: str, needles: Iterable[str]) -> bool:
    return any(needle in haystack for needle in needles)


def validate_release_notes(root: Path, release_note_glob: str) -> list[str]:
    """Return freshness validation errors for Community release notes."""

    errors: list[str] = []
    readme_path = root / README
    wiki_home_path = root / WIKI_HOME

    if not readme_path.exists():
        return [f"{README}: missing README"]
    if not wiki_home_path.exists():
        return [f"{WIKI_HOME}: missing wiki home"]

    readme = readme_path.read_text(encoding="utf-8")
    wiki_home = wiki_home_path.read_text(encoding="utf-8")
    release_notes = sorted(root.glob(release_note_glob))

    if not release_notes:
        return [f"no Community release notes found for {release_note_glob}"]

    for release_note in release_notes:
        relative_release_note = _relative(release_note, root)
        release_text = release_note.read_text(encoding="utf-8")
        release_id = release_note.stem
        version = release_id.removeprefix("community-")
        tag = f"community-{version}"
        release_url = f"https://github.com/Huzefaaa2/cavra/releases/tag/{tag}"

        if relative_release_note not in readme:
            errors.append(f"{relative_release_note}: README is missing release notes link")
        if release_url not in release_text:
            errors.append(f"{relative_release_note}: release notes are missing GitHub Release URL")

        verification_paths = sorted(
            path
            for path in (root / "docs/release-verifications").glob(f"{tag}*.md")
            if path.name != "community-maintenance-release.schema.json"
        )
        if not verification_paths:
            errors.append(f"{relative_release_note}: missing matching verification packet")
        else:
            verification_refs = [_relative(path, root) for path in verification_paths]
            if not _contains_any(readme, verification_refs):
                errors.append(
                    f"{relative_release_note}: README is missing matching verification packet link"
                )
            if not _contains_any(release_text, verification_refs):
                errors.append(
                    f"{relative_release_note}: release notes are missing matching verification packet link"
                )

        wiki_release_candidates = sorted(
            path.name
            for path in (root / "docs/wiki").glob(f"*{version}*Release-Notes.md")
        )
        if not wiki_release_candidates:
            errors.append(f"{relative_release_note}: missing wiki release notes page")
        elif not _contains_any(wiki_home, wiki_release_candidates):
            errors.append(f"{relative_release_note}: wiki home is missing release notes entry")

        wiki_verification_candidates = sorted(
            path.name for path in (root / "docs/wiki").glob(f"*{version}*Verification.md")
        )
        if not wiki_verification_candidates:
            errors.append(f"{relative_release_note}: missing wiki verification page")
        elif not _contains_any(wiki_home, wiki_verification_candidates):
            errors.append(f"{relative_release_note}: wiki home is missing verification entry")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."), help="Repository root.")
    parser.add_argument(
        "--release-note-glob",
        default=DEFAULT_RELEASE_NOTE_GLOB,
        help="Release notes glob relative to --root.",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    errors = validate_release_notes(root, args.release_note_glob)
    if errors:
        print("CAVRA Community release note freshness validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("CAVRA Community release note freshness validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
