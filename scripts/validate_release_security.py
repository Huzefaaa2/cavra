from __future__ import annotations

from pathlib import Path


REQUIRED_TEXT = {
    "SECURITY.md": [
        "Reporting a Vulnerability",
        "Release Advisory Process",
        "cavra release verify-go-package",
    ],
    "docs/vulnerability-disclosure.md": [
        "Reporter Workflow",
        "Maintainer Workflow",
        "Enterprise Value",
    ],
    "docs/release-security-advisories.md": [
        "Advisory Content",
        "Go Runtime Release Gate",
        "cavra-runtime.provenance.intoto.json",
        "gh attestation verify",
    ],
    "scripts/package_go_release.py": [
        "https://in-toto.io/Statement/v1",
        "https://slsa.dev/provenance/v1",
        "cavra-runtime.provenance.intoto.json",
    ],
    "src/cavra/release.py": [
        "verify_go_release_provenance",
        "https://slsa.dev/provenance/v1",
    ],
    "src/cavra/cli.py": [
        "--allow-missing-provenance",
    ],
    ".github/workflows/go-release.yml": [
        "id-token: write",
        "attestations: write",
        "artifact-metadata: write",
        "actions/attest@v4",
        "github-keyless-attestation.json",
    ],
}


def main() -> None:
    failures: list[str] = []
    for relative_path, required_fragments in REQUIRED_TEXT.items():
        path = Path(relative_path)
        if not path.exists():
            failures.append(f"missing {relative_path}")
            continue
        text = path.read_text(encoding="utf-8")
        for fragment in required_fragments:
            if fragment not in text:
                failures.append(f"{relative_path} is missing required text: {fragment}")
    if failures:
        raise SystemExit("\n".join(failures))
    print("release security controls validated")


if __name__ == "__main__":
    main()
