#!/usr/bin/env python3
"""Validate public Community maintenance release evidence packets."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

from jsonschema import Draft202012Validator, FormatChecker


DEFAULT_SCHEMA = Path("docs/release-verifications/community-maintenance-release.schema.json")
DEFAULT_PACKET_GLOBS = (
    "docs/release-verifications/community-*-maintenance-verification.json",
    "examples/release-verifications/community-maintenance-release.example.json",
)
REQUIRED_GATES = {
    "Release notes",
    "Changelog",
    "README link",
    "Wiki link",
    "Verification workflow",
    "Artifact checksums",
    "Install smoke",
    "Public boundary",
    "CI evidence",
}
BOUNDARY_FIELDS = (
    "enterprise_source_included",
    "paid_policy_packs_included",
    "customer_records_included",
    "private_keys_included",
    "private_registry_credentials_included",
)


def _packet_paths(root: Path, patterns: Iterable[str]) -> list[Path]:
    paths: list[Path] = []
    for pattern in patterns:
        paths.extend(root.glob(pattern))
    return sorted({path for path in paths if path.is_file()})


def validate_packets(root: Path, schema_path: Path, patterns: Iterable[str]) -> list[str]:
    """Return validation errors for Community maintenance-release evidence."""

    schema = json.loads((root / schema_path).read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors: list[str] = []
    paths = _packet_paths(root, patterns)

    if not paths:
        return ["no Community maintenance release evidence JSON files found"]

    for path in paths:
        relative = path.relative_to(root)
        try:
            packet = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{relative}: invalid JSON: {exc}")
            continue

        for error in sorted(validator.iter_errors(packet), key=lambda item: item.path):
            location = ".".join(str(part) for part in error.path) or "<root>"
            errors.append(f"{relative}: {location}: {error.message}")

        gate_names = {
            gate.get("name") for gate in packet.get("gates", []) if isinstance(gate, dict)
        }
        missing_gates = sorted(REQUIRED_GATES - gate_names)
        extra_gates = sorted(name for name in gate_names - REQUIRED_GATES if name)
        if missing_gates:
            errors.append(f"{relative}: missing required gates: {', '.join(missing_gates)}")
        if extra_gates:
            errors.append(f"{relative}: unexpected gates: {', '.join(extra_gates)}")

        state = packet.get("release_state")
        gates = packet.get("gates", [])
        gate_statuses = {
            gate.get("name"): gate.get("status")
            for gate in gates
            if isinstance(gate, dict) and gate.get("name")
        }
        if state == "ready_for_publication":
            failed_or_warned = sorted(
                name for name, status in gate_statuses.items() if status != "pass"
            )
            if failed_or_warned:
                errors.append(
                    f"{relative}: ready_for_publication requires passing gates: "
                    + ", ".join(failed_or_warned)
                )
            if packet.get("accepted_risks"):
                errors.append(
                    f"{relative}: ready_for_publication packets must not include accepted risks"
                )

        boundary = packet.get("public_boundary", {})
        if isinstance(boundary, dict) and boundary.get("validation_result") == "pass":
            for field in BOUNDARY_FIELDS:
                if boundary.get(field) is not False:
                    errors.append(f"{relative}: {field} must be false when boundary validation passes")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."), help="Repository root.")
    parser.add_argument(
        "--schema",
        type=Path,
        default=DEFAULT_SCHEMA,
        help="Schema path relative to --root.",
    )
    parser.add_argument(
        "--pattern",
        action="append",
        dest="patterns",
        help="Packet glob relative to --root. Can be repeated.",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    patterns = tuple(args.patterns or DEFAULT_PACKET_GLOBS)
    errors = validate_packets(root, args.schema, patterns)
    if errors:
        print("CAVRA maintenance release evidence validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("CAVRA maintenance release evidence validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
