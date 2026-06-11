from __future__ import annotations

import json
from importlib import resources
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

REVIEW_PACKET_SCHEMA = "aispm-replay-to-policy-review-packet.schema.json"
REVIEW_PACKET_SCHEMA_VERSION = "cavra.aispm.replay_to_policy_review_packet.v1"
REVIEW_PACKET_VALIDATION_SCHEMA_VERSION = "cavra.aispm.review_packet_validation.v1"


def _schema_payload() -> dict[str, Any]:
    schema_text = resources.files("cavra.schemas").joinpath(REVIEW_PACKET_SCHEMA).read_text(encoding="utf-8")
    payload = json.loads(schema_text)
    if not isinstance(payload, dict):  # pragma: no cover - packaged schema regression guard
        raise ValueError(f"{REVIEW_PACKET_SCHEMA} is not a JSON object")
    return payload


def _error(path: str, message: str) -> dict[str, str]:
    return {"path": path, "message": message}


def _format_schema_path(error: Any) -> str:
    if not error.path:
        return "$"
    return "$." + ".".join(str(part) for part in error.path)


def _validate_review_packet_semantics(packet: dict[str, Any]) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    fixture = packet.get("test_fixture", {})
    cases = fixture.get("cases", []) if isinstance(fixture, dict) else []
    case_count = fixture.get("case_count") if isinstance(fixture, dict) else None
    if isinstance(cases, list) and case_count != len(cases):
        errors.append(_error("$.test_fixture.case_count", "case_count must match the number of test_fixture.cases"))

    checklist = packet.get("review_checklist", [])
    summary = packet.get("review_summary", {})
    if isinstance(checklist, list) and isinstance(summary, dict):
        checks_total = summary.get("checks_total")
        checks_passed = summary.get("checks_passed")
        actual_total = len(checklist)
        actual_passed = len([item for item in checklist if isinstance(item, dict) and item.get("status") == "pass"])
        if checks_total != actual_total:
            errors.append(_error("$.review_summary.checks_total", "checks_total must match review_checklist length"))
        if checks_passed != actual_passed:
            errors.append(_error("$.review_summary.checks_passed", "checks_passed must match checklist pass count"))

    export = packet.get("export", {})
    if isinstance(export, dict):
        if export.get("status") != "review_only_packet":
            errors.append(_error("$.export.status", "review packet export status must remain review_only_packet"))
        if export.get("filename") != "cavra-replay-policy-review-packet.json":
            errors.append(_error("$.export.filename", "review packet filename must remain cavra-replay-policy-review-packet.json"))

    if isinstance(summary, dict) and summary.get("approval_required") is not True:
        errors.append(_error("$.review_summary.approval_required", "review packets must require human approval"))

    return errors


def validate_aispm_replay_to_policy_review_packet(packet: Any, *, source: str = "inline") -> dict[str, Any]:
    """Validate a public-safe AISPM replay-to-policy review packet."""
    errors: list[dict[str, str]] = []
    schema = _schema_payload()

    if not isinstance(packet, dict):
        errors.append(_error("$", "review packet must be a JSON object"))
    else:
        validator = Draft202012Validator(schema)
        errors.extend(
            _error(_format_schema_path(error), error.message)
            for error in sorted(validator.iter_errors(packet), key=lambda item: list(item.path))
        )
        errors.extend(_validate_review_packet_semantics(packet))

    status = "valid" if not errors else "invalid"
    return {
        "schema_version": REVIEW_PACKET_VALIDATION_SCHEMA_VERSION,
        "status": status,
        "valid": status == "valid",
        "source": source,
        "packet_schema_version": REVIEW_PACKET_SCHEMA_VERSION,
        "schema_file": f"src/cavra/schemas/{REVIEW_PACKET_SCHEMA}",
        "checks": {
            "json_schema": "pass" if not errors else "review_required",
            "semantic_consistency": "pass" if not errors else "review_required",
            "enterprise_boundary": "public_safe_metadata_only",
        },
        "errors": errors,
        "message": (
            "AISPM replay-to-policy review packet is valid."
            if not errors
            else "AISPM replay-to-policy review packet failed validation."
        ),
    }


def validate_aispm_replay_to_policy_review_packet_file(path: Path) -> dict[str, Any]:
    """Load and validate an AISPM replay-to-policy review packet from disk."""
    if not path.exists():
        return {
            "schema_version": REVIEW_PACKET_VALIDATION_SCHEMA_VERSION,
            "status": "invalid",
            "valid": False,
            "source": str(path),
            "packet_schema_version": REVIEW_PACKET_SCHEMA_VERSION,
            "schema_file": f"src/cavra/schemas/{REVIEW_PACKET_SCHEMA}",
            "checks": {
                "json_schema": "review_required",
                "semantic_consistency": "not_evaluated",
                "enterprise_boundary": "public_safe_metadata_only",
            },
            "errors": [_error("$", f"review packet file not found: {path}")],
            "message": "AISPM replay-to-policy review packet failed validation.",
        }
    try:
        packet = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return {
            "schema_version": REVIEW_PACKET_VALIDATION_SCHEMA_VERSION,
            "status": "invalid",
            "valid": False,
            "source": str(path),
            "packet_schema_version": REVIEW_PACKET_SCHEMA_VERSION,
            "schema_file": f"src/cavra/schemas/{REVIEW_PACKET_SCHEMA}",
            "checks": {
                "json_schema": "review_required",
                "semantic_consistency": "not_evaluated",
                "enterprise_boundary": "public_safe_metadata_only",
            },
            "errors": [_error("$", f"invalid JSON: {exc.msg}")],
            "message": "AISPM replay-to-policy review packet failed validation.",
        }
    return validate_aispm_replay_to_policy_review_packet(packet, source=str(path))
