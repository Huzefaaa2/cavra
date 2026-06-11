from __future__ import annotations

import json
from importlib import resources
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

REVIEW_PACKET_SCHEMA = "aispm-replay-to-policy-review-packet.schema.json"
CI_GATE_READINESS_SCHEMA = "aispm-replay-to-policy-ci-gate-readiness.schema.json"
REVIEW_PACKET_SCHEMA_VERSION = "cavra.aispm.replay_to_policy_review_packet.v1"
CI_GATE_READINESS_SCHEMA_VERSION = "cavra.aispm.replay_to_policy_ci_gate_readiness.v1"
REVIEW_PACKET_VALIDATION_SCHEMA_VERSION = "cavra.aispm.review_packet_validation.v1"
CI_GATE_READINESS_VALIDATION_SCHEMA_VERSION = "cavra.aispm.ci_gate_readiness_validation.v1"
REQUIRED_REVIEW_PACKET_FILENAME = "cavra-replay-policy-review-packet.json"
REQUIRED_CI_GATE_CHECK = "cavra-aispm-review-packet"
EXPECTED_CI_GATES = {
    "GitHub Actions": "examples/github-actions/cavra-aispm-review-packet-validation.yml",
    "GitLab CI": "examples/gitlab-ci/cavra-aispm-review-packet-validation.gitlab-ci.yml",
    "Azure Pipelines": "examples/azure-pipelines/cavra-aispm-review-packet-validation.azure-pipelines.yml",
}


def _schema_payload(schema_name: str) -> dict[str, Any]:
    schema_text = resources.files("cavra.schemas").joinpath(schema_name).read_text(encoding="utf-8")
    payload = json.loads(schema_text)
    if not isinstance(payload, dict):  # pragma: no cover - packaged schema regression guard
        raise ValueError(f"{schema_name} is not a JSON object")
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


def _validate_ci_gate_readiness_semantics(
    packet: dict[str, Any],
    *,
    repo_root: Path | None = None,
) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    source = packet.get("source", {})
    required_packet = packet.get("required_packet", {})
    gates = packet.get("gates", [])
    validation = packet.get("validation", {})
    boundaries = packet.get("enterprise_boundaries", {})

    if isinstance(source, dict) and isinstance(required_packet, dict):
        if source.get("review_packet") != required_packet.get("filename"):
            errors.append(
                _error(
                    "$.source.review_packet",
                    "source review_packet must match required_packet filename",
                )
            )
        if source.get("review_packet") != REQUIRED_REVIEW_PACKET_FILENAME:
            errors.append(
                _error(
                    "$.source.review_packet",
                    f"source review_packet must remain {REQUIRED_REVIEW_PACKET_FILENAME}",
                )
            )
        checks_passed = source.get("checks_passed")
        checks_total = source.get("checks_total")
        if (
            isinstance(checks_passed, int)
            and isinstance(checks_total, int)
            and checks_passed > checks_total
        ):
            errors.append(_error("$.source.checks_passed", "checks_passed cannot exceed checks_total"))

    if isinstance(boundaries, dict):
        for key, value in boundaries.items():
            if value != "requires_cavra_enterprise":
                errors.append(
                    _error(
                        f"$.enterprise_boundaries.{key}",
                        "Enterprise boundary values must remain requires_cavra_enterprise",
                    )
                )

    if isinstance(validation, dict):
        expected_command = (
            "cavra aispm validate-ci-gate-readiness "
            "cavra-replay-policy-ci-gate-readiness.json --repo-root ."
        )
        if validation.get("cli_command") != expected_command:
            errors.append(
                _error(
                    "$.validation.cli_command",
                    "validation cli_command must use cavra aispm validate-ci-gate-readiness",
                )
            )
        if validation.get("api_endpoint") != "/aispm/replay-to-policy-ci-gate-readiness/validate":
            errors.append(
                _error(
                    "$.validation.api_endpoint",
                    "validation api_endpoint must remain /aispm/replay-to-policy-ci-gate-readiness/validate",
                )
            )

    gate_by_platform = {
        gate.get("platform"): gate
        for gate in gates
        if isinstance(gate, dict) and isinstance(gate.get("platform"), str)
    } if isinstance(gates, list) else {}
    for platform, expected_path in EXPECTED_CI_GATES.items():
        gate = gate_by_platform.get(platform)
        if not isinstance(gate, dict):
            errors.append(_error("$.gates", f"missing CI gate platform: {platform}"))
            continue
        if gate.get("required_check") != REQUIRED_CI_GATE_CHECK:
            errors.append(
                _error(
                    f"$.gates.{platform}.required_check",
                    f"required_check must be {REQUIRED_CI_GATE_CHECK}",
                )
            )
        if gate.get("template_path") != expected_path:
            errors.append(_error(f"$.gates.{platform}.template_path", f"template_path must be {expected_path}"))
        if repo_root is not None:
            template_path = repo_root / expected_path
            if not template_path.is_file():
                errors.append(
                    _error(
                        f"$.gates.{platform}.template_path",
                        f"template file not found under repo root: {expected_path}",
                    )
                )
                continue
            template_text = template_path.read_text(encoding="utf-8")
            if REQUIRED_CI_GATE_CHECK not in template_text:
                errors.append(
                    _error(
                        f"$.gates.{platform}.required_check",
                        f"template does not contain required check {REQUIRED_CI_GATE_CHECK}",
                    )
                )
            if "cavra aispm validate-review-packet" not in template_text:
                errors.append(
                    _error(
                        f"$.gates.{platform}.template_path",
                        "template must call cavra aispm validate-review-packet",
                    )
                )

    return errors


def _validation_report(
    *,
    validation_schema_version: str,
    status: str,
    source: str,
    packet_schema_version: str,
    schema_file: str,
    errors: list[dict[str, str]],
    valid_message: str,
    invalid_message: str,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    valid = status == "valid"
    checks = {
        "json_schema": "pass" if not errors else "review_required",
        "semantic_consistency": "pass" if not errors else "review_required",
        "enterprise_boundary": "public_safe_metadata_only",
    }
    if repo_root is not None:
        checks["repository_templates"] = "pass" if not errors else "review_required"
        checks["repo_root"] = str(repo_root)
    return {
        "schema_version": validation_schema_version,
        "status": status,
        "valid": valid,
        "source": source,
        "packet_schema_version": packet_schema_version,
        "schema_file": schema_file,
        "checks": checks,
        "errors": errors,
        "message": valid_message if valid else invalid_message,
    }


def validate_aispm_replay_to_policy_review_packet(packet: Any, *, source: str = "inline") -> dict[str, Any]:
    """Validate a public-safe AISPM replay-to-policy review packet."""
    errors: list[dict[str, str]] = []
    schema = _schema_payload(REVIEW_PACKET_SCHEMA)

    if not isinstance(packet, dict):
        errors.append(_error("$", "review packet must be a JSON object"))
    else:
        validator = Draft202012Validator(schema)
        errors.extend(
            _error(_format_schema_path(error), error.message)
            for error in sorted(validator.iter_errors(packet), key=lambda item: list(item.path))
        )
        errors.extend(_validate_review_packet_semantics(packet))

    return _validation_report(
        validation_schema_version=REVIEW_PACKET_VALIDATION_SCHEMA_VERSION,
        status="valid" if not errors else "invalid",
        source=source,
        packet_schema_version=REVIEW_PACKET_SCHEMA_VERSION,
        schema_file=f"src/cavra/schemas/{REVIEW_PACKET_SCHEMA}",
        errors=errors,
        valid_message="AISPM replay-to-policy review packet is valid.",
        invalid_message="AISPM replay-to-policy review packet failed validation.",
    )


def validate_aispm_replay_to_policy_ci_gate_readiness(
    packet: Any,
    *,
    source: str = "inline",
    repo_root: Path | None = None,
) -> dict[str, Any]:
    """Validate a public-safe AISPM replay-to-policy CI gate readiness packet."""
    errors: list[dict[str, str]] = []
    schema = _schema_payload(CI_GATE_READINESS_SCHEMA)

    if not isinstance(packet, dict):
        errors.append(_error("$", "CI gate readiness packet must be a JSON object"))
    else:
        validator = Draft202012Validator(schema)
        errors.extend(
            _error(_format_schema_path(error), error.message)
            for error in sorted(validator.iter_errors(packet), key=lambda item: list(item.path))
        )
        errors.extend(_validate_ci_gate_readiness_semantics(packet, repo_root=repo_root))

    return _validation_report(
        validation_schema_version=CI_GATE_READINESS_VALIDATION_SCHEMA_VERSION,
        status="valid" if not errors else "invalid",
        source=source,
        packet_schema_version=CI_GATE_READINESS_SCHEMA_VERSION,
        schema_file=f"src/cavra/schemas/{CI_GATE_READINESS_SCHEMA}",
        errors=errors,
        valid_message="AISPM replay-to-policy CI gate readiness packet is valid.",
        invalid_message="AISPM replay-to-policy CI gate readiness packet failed validation.",
        repo_root=repo_root,
    )


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


def validate_aispm_replay_to_policy_ci_gate_readiness_file(
    path: Path,
    *,
    repo_root: Path | None = None,
) -> dict[str, Any]:
    """Load and validate an AISPM replay-to-policy CI gate readiness packet."""
    if not path.exists():
        return _validation_report(
            validation_schema_version=CI_GATE_READINESS_VALIDATION_SCHEMA_VERSION,
            status="invalid",
            source=str(path),
            packet_schema_version=CI_GATE_READINESS_SCHEMA_VERSION,
            schema_file=f"src/cavra/schemas/{CI_GATE_READINESS_SCHEMA}",
            errors=[_error("$", f"CI gate readiness file not found: {path}")],
            valid_message="AISPM replay-to-policy CI gate readiness packet is valid.",
            invalid_message="AISPM replay-to-policy CI gate readiness packet failed validation.",
            repo_root=repo_root,
        )
    try:
        packet = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return _validation_report(
            validation_schema_version=CI_GATE_READINESS_VALIDATION_SCHEMA_VERSION,
            status="invalid",
            source=str(path),
            packet_schema_version=CI_GATE_READINESS_SCHEMA_VERSION,
            schema_file=f"src/cavra/schemas/{CI_GATE_READINESS_SCHEMA}",
            errors=[_error("$", f"invalid JSON: {exc.msg}")],
            valid_message="AISPM replay-to-policy CI gate readiness packet is valid.",
            invalid_message="AISPM replay-to-policy CI gate readiness packet failed validation.",
            repo_root=repo_root,
        )
    return validate_aispm_replay_to_policy_ci_gate_readiness(
        packet,
        source=str(path),
        repo_root=repo_root,
    )
