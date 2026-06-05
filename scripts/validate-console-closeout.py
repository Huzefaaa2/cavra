#!/usr/bin/env python3
"""Validate the public console closeout operator experience."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NEXT_RECOMMENDATION = (
    "Implement Community v1.0.0 release-candidate hardening packet from the "
    "completed Node 24 readiness baseline with signed artifacts, reproducible "
    "provenance verification, GA announcement checklist, and final operator evidence."
)


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require_file(path: str, failures: list[str]) -> None:
    if not (ROOT / path).is_file():
        failures.append(f"missing required file: {path}")


def require(text: str, needle: str, label: str, failures: list[str]) -> None:
    if needle not in text:
        failures.append(f"missing {label}: {needle}")


def require_phrase(text: str, phrase: str, label: str, failures: list[str]) -> None:
    normalized_phrase = " ".join(phrase.lower().split())
    normalized_text = " ".join(text.lower().split())
    if normalized_phrase not in normalized_text:
        failures.append(f"missing {label}: {phrase}")


def main() -> int:
    failures: list[str] = []
    required_files = [
        "apps/sandbox-ui/index.html",
        "apps/sandbox-ui/styles.css",
        "apps/sandbox-ui/sandbox.js",
        "docs/console-closeout-operator-experience.md",
        "docs/wiki/Console-Closeout-Operator-Experience.md",
        "docs/roadmap-status-next-slice.md",
        "docs/wiki/Roadmap-Status-And-Next-Slice.md",
    ]
    for path in required_files:
        require_file(path, failures)

    if failures:
        for failure in failures:
            print(failure)
        return 1

    html = read("apps/sandbox-ui/index.html")
    css = read("apps/sandbox-ui/styles.css")
    js = read("apps/sandbox-ui/sandbox.js")
    readme = read("README.md")
    changelog = read("CHANGELOG.md")
    wiki_home = read("docs/wiki/Home.md")
    closeout_doc = read("docs/console-closeout-operator-experience.md")
    wiki_closeout_doc = read("docs/wiki/Console-Closeout-Operator-Experience.md")
    roadmap = read("docs/production-roadmap.md")
    next_slice = read("docs/roadmap-status-next-slice.md")
    wiki_next_slice = read("docs/wiki/Roadmap-Status-And-Next-Slice.md")

    for needle in [
        'id="operator-experience"',
        'data-title="Operator Paths"',
        'id="operatorPathCards"',
        "operator-path-grid",
    ]:
        require(html, needle, "operator route DOM", failures)

    for needle in [
        "operatorPaths",
        "renderOperatorPaths",
        'type: "Operator Path"',
        "Prospect",
        "Auditor",
        "Platform Team",
        "CISO",
        "Dashboard, Architecture, Use Cases, Documentation",
        "Evidence, Compliance, Release Readiness Dashboard, Release Index",
        "Required checks, policy packs, GitHub/GitLab/Azure DevOps paths",
        "open-core boundary",
    ]:
        require(js, needle, "operator journey content", failures)

    for needle in [
        ".operator-path-grid",
        ".operator-path-card",
        "@media (max-width: 900px)",
    ]:
        require(css, needle, "operator route styling", failures)

    for path in [
        "docs/console-closeout-operator-experience.md",
        "docs/sandbox-portal-smoke-validation.md",
    ]:
        require(readme, path, "README console navigation", failures)

    require(
        wiki_home,
        "Console-Closeout-Operator-Experience.md",
        "wiki console closeout link",
        failures,
    )
    require(changelog, "console closeout operator experience", "changelog entry", failures)

    for doc in [closeout_doc, wiki_closeout_doc]:
        for needle in [
            "Prospect",
            "Auditor",
            "Platform Team",
            "CISO",
            "Public Boundary",
            "Validation Command",
            "scripts/validate-console-closeout.py",
        ]:
            require(doc, needle, "console closeout documentation", failures)
        require_phrase(doc, NEXT_RECOMMENDATION, "console closeout next recommendation", failures)

    for doc in [roadmap, next_slice, wiki_next_slice]:
        require(
            doc,
            "Console closeout operator experience is documented",
            "roadmap delivered console closeout statement",
            failures,
        )
        require_phrase(doc, NEXT_RECOMMENDATION, "roadmap next recommendation", failures)

    for workflow_path in [
        ".github/workflows/community-ci.yml",
        ".github/workflows/security-scan.yml",
        ".github/workflows/release-community.yml",
        ".github/workflows/cavra-governance.yml",
        ".github/workflows/deploy-sandbox.yml",
    ]:
        require(
            read(workflow_path),
            "python scripts/validate-console-closeout.py",
            f"{workflow_path} validator wiring",
            failures,
        )

    if failures:
        print("CAVRA console closeout validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("CAVRA console closeout validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
