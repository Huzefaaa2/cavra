#!/usr/bin/env python3
"""Validate public Community GA release packet JSON artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

from jsonschema import Draft202012Validator, FormatChecker


DEFAULT_SCHEMA = Path("docs/release-packets/community-ga-release-packet.schema.json")
DEFAULT_PACKET_GLOBS = (
    "docs/release-packets/community-ga-*.json",
    "examples/release-packets/community-ga-*.json",
)
REQUIRED_GATES = {
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


def _packet_paths(root: Path, patterns: Iterable[str]) -> list[Path]:
    paths: list[Path] = []
    for pattern in patterns:
        paths.extend(root.glob(pattern))
    return sorted(
        {
            path
            for path in paths
            if path.is_file() and path.name != "community-ga-release-packet.schema.json"
        }
    )


def validate_packets(root: Path, schema_path: Path, patterns: Iterable[str]) -> list[str]:
    """Return validation error messages for public release packet artifacts."""

    schema = json.loads((root / schema_path).read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors: list[str] = []
    paths = _packet_paths(root, patterns)

    if not paths:
        return ["no Community GA release packet JSON files found"]

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

        gate_names = {gate.get("name") for gate in packet.get("gates", []) if isinstance(gate, dict)}
        missing_gates = sorted(REQUIRED_GATES - gate_names)
        extra_gates = sorted(name for name in gate_names - REQUIRED_GATES if name)
        if missing_gates:
            errors.append(f"{relative}: missing required gates: {', '.join(missing_gates)}")
        if extra_gates:
            errors.append(f"{relative}: unexpected gates: {', '.join(extra_gates)}")

        if packet.get("release_state") == "ready_for_community_ga" and packet.get("accepted_risks"):
            errors.append(f"{relative}: ready_for_community_ga packets must not include accepted risks")

        boundary = packet.get("public_boundary_review", {})
        if isinstance(boundary, dict) and boundary.get("validation_result") == "pass":
            for field in (
                "enterprise_code_present",
                "secrets_present",
                "customer_material_present",
                "private_policy_packs_present",
            ):
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
        print("CAVRA release packet validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("CAVRA release packet validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
