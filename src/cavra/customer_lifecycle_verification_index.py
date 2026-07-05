from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cavra.customer_live_evidence import find_forbidden_live_evidence_fields


CUSTOMER_LIFECYCLE_VERIFICATION_INDEX_SCHEMA = "cavra.customer-lifecycle-verification-index.packet.v1"
CUSTOMER_LIFECYCLE_VERIFICATION_INDEX_RESULT_SCHEMA = "cavra.customer-lifecycle-verification-index.result.v1"

FORBIDDEN_VERIFICATION_INDEX_FIELDS = {
    "commercial_terms",
    "contract_value",
    "customer_email",
    "customer_name",
    "legal_terms",
    "private_note",
    "pricing",
    "raw_contract",
    "raw_evidence",
    "renewal_amount",
}

R7_GATE_SPECS: tuple[dict[str, str], ...] = (
    {
        "gate_id": "R7.1",
        "name": "Customer Live Evidence Intake",
        "example_path": "examples/customer-live-evidence/customer-live-evidence.live.sanitized.example.json",
        "result_path": "examples/customer-live-evidence/customer-live-evidence.live.sanitized.result.json",
        "ready_key": "ready_for_customer_live_evidence_intake",
        "validator_path": "scripts/validate_customer_live_evidence.py",
        "workflow_path": ".github/workflows/customer-live-evidence.yml",
        "test_path": "tests/test_customer_live_evidence.py",
        "doc_path": "docs/customer-live-evidence-intake.md",
        "wiki_path": "docs/wiki/Customer-Live-Evidence-Intake.md",
        "validator_command": (
            "python3 scripts/validate_customer_live_evidence.py --packet "
            "examples/customer-live-evidence/customer-live-evidence.live.sanitized.example.json --require-live"
        ),
    },
    {
        "gate_id": "R7.2",
        "name": "Customer Evidence Room Closeout",
        "example_path": "examples/customer-evidence-room/customer-evidence-room.live.sanitized.example.json",
        "result_path": "examples/customer-evidence-room/customer-evidence-room.live.sanitized.result.json",
        "ready_key": "ready_for_customer_evidence_room_closeout",
        "validator_path": "scripts/validate_customer_evidence_room.py",
        "workflow_path": ".github/workflows/customer-evidence-room.yml",
        "test_path": "tests/test_customer_evidence_room.py",
        "doc_path": "docs/customer-evidence-room-closeout.md",
        "wiki_path": "docs/wiki/Customer-Evidence-Room-Closeout.md",
        "validator_command": (
            "python3 scripts/validate_customer_evidence_room.py --index "
            "examples/customer-evidence-room/customer-evidence-room.live.sanitized.example.json --require-live"
        ),
    },
    {
        "gate_id": "R7.3",
        "name": "Customer Closeout Handoff",
        "example_path": "examples/customer-closeout-handoff/customer-closeout-handoff.live.sanitized.example.json",
        "result_path": "examples/customer-closeout-handoff/customer-closeout-handoff.live.sanitized.result.json",
        "ready_key": "ready_for_customer_closeout_handoff",
        "validator_path": "scripts/validate_customer_closeout_handoff.py",
        "workflow_path": ".github/workflows/customer-closeout-handoff.yml",
        "test_path": "tests/test_customer_closeout_handoff.py",
        "doc_path": "docs/customer-closeout-handoff.md",
        "wiki_path": "docs/wiki/Customer-Closeout-Handoff.md",
        "validator_command": (
            "python3 scripts/validate_customer_closeout_handoff.py --packet "
            "examples/customer-closeout-handoff/customer-closeout-handoff.live.sanitized.example.json --require-live"
        ),
    },
    {
        "gate_id": "R7.4",
        "name": "Customer Operating Review",
        "example_path": "examples/customer-operating-review/customer-operating-review.live.sanitized.example.json",
        "result_path": "examples/customer-operating-review/customer-operating-review.live.sanitized.result.json",
        "ready_key": "ready_for_customer_operating_review",
        "validator_path": "scripts/validate_customer_operating_review.py",
        "workflow_path": ".github/workflows/customer-operating-review.yml",
        "test_path": "tests/test_customer_operating_review.py",
        "doc_path": "docs/customer-operating-review.md",
        "wiki_path": "docs/wiki/Customer-Operating-Review.md",
        "validator_command": (
            "python3 scripts/validate_customer_operating_review.py --packet "
            "examples/customer-operating-review/customer-operating-review.live.sanitized.example.json --require-live"
        ),
    },
    {
        "gate_id": "R7.5",
        "name": "Customer Renewal And Expansion Readiness",
        "example_path": "examples/customer-renewal-expansion/customer-renewal-expansion.live.sanitized.example.json",
        "result_path": "examples/customer-renewal-expansion/customer-renewal-expansion.live.sanitized.result.json",
        "ready_key": "ready_for_customer_renewal_expansion",
        "validator_path": "scripts/validate_customer_renewal_expansion.py",
        "workflow_path": ".github/workflows/customer-renewal-expansion.yml",
        "test_path": "tests/test_customer_renewal_expansion.py",
        "doc_path": "docs/customer-renewal-expansion.md",
        "wiki_path": "docs/wiki/Customer-Renewal-And-Expansion-Readiness.md",
        "validator_command": (
            "python3 scripts/validate_customer_renewal_expansion.py --packet "
            "examples/customer-renewal-expansion/customer-renewal-expansion.live.sanitized.example.json --require-live"
        ),
    },
    {
        "gate_id": "R7.6",
        "name": "Customer Renewal Outcome Closeout",
        "example_path": "examples/customer-renewal-outcome/customer-renewal-outcome.live.sanitized.example.json",
        "result_path": "examples/customer-renewal-outcome/customer-renewal-outcome.live.sanitized.result.json",
        "ready_key": "ready_for_customer_renewal_outcome_closeout",
        "validator_path": "scripts/validate_customer_renewal_outcome.py",
        "workflow_path": ".github/workflows/customer-renewal-outcome.yml",
        "test_path": "tests/test_customer_renewal_outcome.py",
        "doc_path": "docs/customer-renewal-outcome-closeout.md",
        "wiki_path": "docs/wiki/Customer-Renewal-Outcome-Closeout.md",
        "validator_command": (
            "python3 scripts/validate_customer_renewal_outcome.py --packet "
            "examples/customer-renewal-outcome/customer-renewal-outcome.live.sanitized.example.json --require-live"
        ),
    },
    {
        "gate_id": "R7.7",
        "name": "Customer Lifecycle Executive Rollup",
        "example_path": "examples/customer-lifecycle-rollup/customer-lifecycle-rollup.live.sanitized.example.json",
        "result_path": "examples/customer-lifecycle-rollup/customer-lifecycle-rollup.live.sanitized.result.json",
        "ready_key": "ready_for_customer_lifecycle_executive_rollup",
        "validator_path": "scripts/validate_customer_lifecycle_rollup.py",
        "workflow_path": ".github/workflows/customer-lifecycle-rollup.yml",
        "test_path": "tests/test_customer_lifecycle_rollup.py",
        "doc_path": "docs/customer-lifecycle-executive-rollup.md",
        "wiki_path": "docs/wiki/Customer-Lifecycle-Executive-Rollup.md",
        "validator_command": (
            "python3 scripts/validate_customer_lifecycle_rollup.py --packet "
            "examples/customer-lifecycle-rollup/customer-lifecycle-rollup.live.sanitized.example.json --require-live"
        ),
    },
    {
        "gate_id": "R7.8",
        "name": "Customer Lifecycle Archive Manifest",
        "example_path": "examples/customer-lifecycle-archive/customer-lifecycle-archive.live.sanitized.example.json",
        "result_path": "examples/customer-lifecycle-archive/customer-lifecycle-archive.live.sanitized.result.json",
        "ready_key": "ready_for_customer_lifecycle_archive_manifest",
        "validator_path": "scripts/validate_customer_lifecycle_archive.py",
        "workflow_path": ".github/workflows/customer-lifecycle-archive.yml",
        "test_path": "tests/test_customer_lifecycle_archive.py",
        "doc_path": "docs/customer-lifecycle-archive-manifest.md",
        "wiki_path": "docs/wiki/Customer-Lifecycle-Archive-Manifest.md",
        "validator_command": (
            "python3 scripts/validate_customer_lifecycle_archive.py --packet "
            "examples/customer-lifecycle-archive/customer-lifecycle-archive.live.sanitized.example.json --require-live"
        ),
    },
    {
        "gate_id": "R7.9",
        "name": "Customer Lifecycle Public Status Summary",
        "example_path": "examples/customer-lifecycle-status/customer-lifecycle-status.live.sanitized.example.json",
        "result_path": "examples/customer-lifecycle-status/customer-lifecycle-status.live.sanitized.result.json",
        "ready_key": "ready_for_customer_lifecycle_public_status",
        "validator_path": "scripts/validate_customer_lifecycle_status.py",
        "workflow_path": ".github/workflows/customer-lifecycle-status.yml",
        "test_path": "tests/test_customer_lifecycle_status.py",
        "doc_path": "docs/customer-lifecycle-public-status.md",
        "wiki_path": "docs/wiki/Customer-Lifecycle-Public-Status.md",
        "validator_command": (
            "python3 scripts/validate_customer_lifecycle_status.py --packet "
            "examples/customer-lifecycle-status/customer-lifecycle-status.live.sanitized.example.json --require-live"
        ),
    },
    {
        "gate_id": "R7.10",
        "name": "Customer Lifecycle Final Release Seal",
        "example_path": "examples/customer-lifecycle-final-seal/customer-lifecycle-final-seal.live.sanitized.example.json",
        "result_path": "examples/customer-lifecycle-final-seal/customer-lifecycle-final-seal.live.sanitized.result.json",
        "ready_key": "ready_for_customer_lifecycle_final_release_seal",
        "validator_path": "scripts/validate_customer_lifecycle_final_seal.py",
        "workflow_path": ".github/workflows/customer-lifecycle-final-seal.yml",
        "test_path": "tests/test_customer_lifecycle_final_seal.py",
        "doc_path": "docs/customer-lifecycle-final-release-seal.md",
        "wiki_path": "docs/wiki/Customer-Lifecycle-Final-Release-Seal.md",
        "validator_command": (
            "python3 scripts/validate_customer_lifecycle_final_seal.py --packet "
            "examples/customer-lifecycle-final-seal/customer-lifecycle-final-seal.live.sanitized.example.json "
            "--require-live"
        ),
    },
)


def build_customer_lifecycle_verification_index(
    repo_root: Path | None = None,
    *,
    evidence_mode: str = "sample",
) -> dict[str, Any]:
    root = repo_root or Path.cwd()
    gates = [_build_gate_entry(root, spec) for spec in R7_GATE_SPECS]
    return {
        "schema_version": CUSTOMER_LIFECYCLE_VERIFICATION_INDEX_SCHEMA,
        "product": "CAVRA",
        "phase": "R7",
        "evidence_mode": evidence_mode,
        "sanitized": evidence_mode == "live",
        "verification_index_id": f"cavra-{evidence_mode}-customer-lifecycle-verification-index",
        "gate_count": len(gates),
        "gates": gates,
        "completion_condition": (
            "All R7 customer lifecycle gates have live sanitized examples, ready result packets, validators, "
            "workflows, tests, repository docs, wiki docs, and customer-safe release commands."
        ),
    }


def validate_customer_lifecycle_verification_index(
    index: dict[str, Any],
    *,
    repo_root: Path | None = None,
    require_live: bool = False,
) -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    root = repo_root or Path.cwd()
    _add_check(
        checks,
        "schema_version",
        "pass" if index.get("schema_version") == CUSTOMER_LIFECYCLE_VERIFICATION_INDEX_SCHEMA else "blocker",
        "Customer lifecycle verification index schema is valid."
        if index.get("schema_version") == CUSTOMER_LIFECYCLE_VERIFICATION_INDEX_SCHEMA
        else f"Index must use {CUSTOMER_LIFECYCLE_VERIFICATION_INDEX_SCHEMA}.",
    )
    _check_evidence_mode(index, checks, require_live=require_live)
    _check_gate_count(index, checks)
    _check_gates(index.get("gates", []), root, checks)
    _check_completion_condition(index.get("completion_condition"), checks)
    forbidden = sorted(find_forbidden_live_evidence_fields(index) | _find_forbidden_verification_fields(index))
    _add_check(
        checks,
        "no_private_material",
        "pass" if not forbidden else "blocker",
        "Verification index contains public artifact refs and sanitized release commands only."
        if not forbidden
        else f"Forbidden private material fields detected: {', '.join(forbidden)}.",
    )
    blocker_count = sum(1 for check in checks if check["status"] == "blocker")
    warning_count = sum(1 for check in checks if check["status"] == "warn")
    ready = blocker_count == 0 and index.get("evidence_mode") == "live" and warning_count == 0
    return {
        "schema_version": CUSTOMER_LIFECYCLE_VERIFICATION_INDEX_RESULT_SCHEMA,
        "product": index.get("product", "CAVRA"),
        "phase": index.get("phase", "R7"),
        "evidence_mode": index.get("evidence_mode", "unknown"),
        "ready_for_customer_lifecycle_verification_index": ready,
        "status": "blocked" if blocker_count else ("ready_with_warnings" if warning_count else "ready"),
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "checks": checks,
    }


def write_customer_lifecycle_verification_index_artifacts(output_dir: Path, repo_root: Path | None = None) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    root = repo_root or Path.cwd()
    sample = build_customer_lifecycle_verification_index(root, evidence_mode="sample")
    live = build_customer_lifecycle_verification_index(root, evidence_mode="live")
    sample_result = validate_customer_lifecycle_verification_index(sample, repo_root=root)
    live_result = validate_customer_lifecycle_verification_index(live, repo_root=root, require_live=True)
    written = {
        "sample": output_dir / "customer-lifecycle-verification-index.sample.json",
        "live_sanitized_example": output_dir / "customer-lifecycle-verification-index.live.sanitized.example.json",
        "sample_result": output_dir / "customer-lifecycle-verification-index.sample.result.json",
        "live_result": output_dir / "customer-lifecycle-verification-index.live.sanitized.result.json",
    }
    payloads = {
        "sample": sample,
        "live_sanitized_example": live,
        "sample_result": sample_result,
        "live_result": live_result,
    }
    for key, path in written.items():
        path.write_text(json.dumps(payloads[key], indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "schema_version": "cavra.customer-lifecycle-verification-index.export.v1",
        "written": {key: str(path) for key, path in written.items()},
        "ready_for_customer_lifecycle_verification_index": live_result[
            "ready_for_customer_lifecycle_verification_index"
        ],
    }


def _build_gate_entry(repo_root: Path, spec: dict[str, str]) -> dict[str, Any]:
    result_payload = _read_json(repo_root / spec["result_path"])
    example_payload = _read_json(repo_root / spec["example_path"])
    artifact_paths = {
        "live_sanitized_example": spec["example_path"],
        "live_result": spec["result_path"],
        "validator": spec["validator_path"],
        "workflow": spec["workflow_path"],
        "test": spec["test_path"],
        "docs": spec["doc_path"],
        "wiki": spec["wiki_path"],
    }
    return {
        "gate_id": spec["gate_id"],
        "name": spec["name"],
        "ready_key": spec["ready_key"],
        "ready": result_payload.get(spec["ready_key"]) is True,
        "blocker_count": int(result_payload.get("blocker_count", 1)),
        "warning_count": int(result_payload.get("warning_count", 0)),
        "example_evidence_mode": example_payload.get("evidence_mode", "unknown"),
        "example_sanitized": example_payload.get("sanitized") is True,
        "artifact_paths": artifact_paths,
        "artifact_presence": {key: (repo_root / value).exists() for key, value in artifact_paths.items()},
        "validator_command": spec["validator_command"],
    }


def _check_evidence_mode(index: dict[str, Any], checks: list[dict[str, str]], *, require_live: bool) -> None:
    mode = index.get("evidence_mode")
    sanitized = index.get("sanitized") is True
    if mode == "live" and sanitized:
        _add_check(checks, "evidence_mode", "pass", "Live sanitized verification index supplied.")
    elif mode == "sample" and not require_live:
        _add_check(checks, "evidence_mode", "warn", "Sample verification index validates shape only.")
    else:
        _add_check(checks, "evidence_mode", "blocker", "Verification index requires evidence_mode=live and sanitized=true.")


def _check_gate_count(index: dict[str, Any], checks: list[dict[str, str]]) -> None:
    gate_count = index.get("gate_count")
    gates = index.get("gates")
    expected = len(R7_GATE_SPECS)
    actual = len(gates) if isinstance(gates, list) else 0
    _add_check(
        checks,
        "gate_count",
        "pass" if gate_count == expected and actual == expected else "blocker",
        f"Verification index contains all {expected} R7 gates."
        if gate_count == expected and actual == expected
        else f"Verification index must contain {expected} R7 gates; found gate_count={gate_count}, gates={actual}.",
    )


def _check_gates(gates: Any, repo_root: Path, checks: list[dict[str, str]]) -> None:
    if not isinstance(gates, list):
        _add_check(checks, "gates", "blocker", "gates must be a list.")
        return
    specs_by_id = {spec["gate_id"]: spec for spec in R7_GATE_SPECS}
    gates_by_id = {str(gate.get("gate_id")): gate for gate in gates if isinstance(gate, dict)}
    missing = sorted(set(specs_by_id) - set(gates_by_id))
    unexpected = sorted(set(gates_by_id) - set(specs_by_id))
    not_ready: list[str] = []
    bad_examples: list[str] = []
    missing_artifacts: list[str] = []
    bad_commands: list[str] = []
    for gate_id, spec in specs_by_id.items():
        gate = gates_by_id.get(gate_id)
        if not gate:
            continue
        if gate.get("ready") is not True or int(gate.get("blocker_count", 1)) != 0:
            not_ready.append(gate_id)
        if gate.get("example_evidence_mode") != "live" or gate.get("example_sanitized") is not True:
            bad_examples.append(gate_id)
        artifact_paths = gate.get("artifact_paths", {})
        artifact_presence = gate.get("artifact_presence", {})
        for key in ("live_sanitized_example", "live_result", "validator", "workflow", "test", "docs", "wiki"):
            path = artifact_paths.get(key)
            if path != _expected_artifact_path(spec, key):
                missing_artifacts.append(f"{gate_id}:{key}")
                continue
            if artifact_presence.get(key) is not True or not (repo_root / str(path)).exists():
                missing_artifacts.append(f"{gate_id}:{key}")
        if gate.get("validator_command") != spec["validator_command"]:
            bad_commands.append(gate_id)
    if not missing and not unexpected and not not_ready and not bad_examples and not missing_artifacts and not bad_commands:
        _add_check(checks, "gates", "pass", "All R7 gates are present, ready, documented, tested, and wired to CI.")
    else:
        problems = []
        if missing:
            problems.append(f"missing gates: {', '.join(missing)}")
        if unexpected:
            problems.append(f"unexpected gates: {', '.join(unexpected)}")
        if not_ready:
            problems.append(f"not ready: {', '.join(not_ready)}")
        if bad_examples:
            problems.append(f"bad live examples: {', '.join(bad_examples)}")
        if missing_artifacts:
            problems.append(f"missing artifacts: {', '.join(sorted(missing_artifacts))}")
        if bad_commands:
            problems.append(f"bad validator commands: {', '.join(bad_commands)}")
        _add_check(checks, "gates", "blocker", f"R7 gate verification failed: {'; '.join(problems)}.")


def _expected_artifact_path(spec: dict[str, str], key: str) -> str:
    mapping = {
        "live_sanitized_example": "example_path",
        "live_result": "result_path",
        "validator": "validator_path",
        "workflow": "workflow_path",
        "test": "test_path",
        "docs": "doc_path",
        "wiki": "wiki_path",
    }
    return spec[mapping[key]]


def _check_completion_condition(value: Any, checks: list[dict[str, str]]) -> None:
    text = str(value or "").strip()
    _add_check(
        checks,
        "completion_condition",
        "pass" if len(text) >= 60 else "blocker",
        "Completion condition is explicit."
        if len(text) >= 60
        else "completion_condition must be an explicit summary of at least 60 characters.",
    )


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _find_forbidden_verification_fields(value: Any, *, prefix: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_VERIFICATION_INDEX_FIELDS:
                found.add(path)
            found.update(_find_forbidden_verification_fields(item, prefix=path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.update(_find_forbidden_verification_fields(item, prefix=f"{prefix}[{index}]"))
    return found


def _add_check(checks: list[dict[str, str]], name: str, status: str, message: str) -> None:
    checks.append({"name": name, "status": status, "message": message})
