from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any

from cavra.policy_engine import compile_policy, load_policy_file, validate_policy
from cavra.policy_registry import PolicyRegistry
from cavra.runtime import RuntimeGuard

OPA_REGO_BUNDLE_SCHEMA = "cavra.opa-rego-policy.bundle.v1"
OPA_REGO_READINESS_SCHEMA = "cavra.opa-rego-policy.readiness.v1"
OPA_REGO_PARITY_SCHEMA = "cavra.opa-rego-policy.parity.v1"

REQUIRED_REGO_ARTIFACTS = {
    "rego_module",
    "rego_data",
    "opa_input_fixtures",
    "parity_test_report",
    "policy_version_manifest",
}

REQUIRED_PARITY_CASES = {
    "block_env_read",
    "approval_policy_write",
    "allow_terraform_plan",
    "block_terraform_apply",
    "block_protected_branch_push",
    "block_unknown_mcp_server",
}


def load_policy_for_rego(policy_pack: str, overlays: list[Path] | None = None) -> dict[str, Any]:
    registry = PolicyRegistry()
    overlay_payloads = [load_policy_file(path) for path in overlays or []]
    policy = compile_policy(registry.load_policy(policy_pack), overlay_payloads)
    errors = validate_policy(policy)
    if errors:
        raise ValueError(f"policy pack {policy_pack} is invalid: {'; '.join(errors)}")
    return policy


def build_rego_policy_bundle(
    policy_pack: str = "cavra-ai-agent-baseline",
    *,
    overlays: list[Path] | None = None,
    package: str = "cavra.policy",
) -> dict[str, Any]:
    policy = load_policy_for_rego(policy_pack, overlays=overlays)
    rego_data = build_rego_data(policy)
    fixtures = build_default_rego_parity_fixtures()
    parity = run_rego_parity_report(policy_pack=policy_pack, fixtures=fixtures, policy=policy)
    return {
        "schema_version": OPA_REGO_BUNDLE_SCHEMA,
        "policy_pack": policy_pack,
        "package": package,
        "rego_module": policy_to_rego_module(policy, package=package),
        "rego_data": rego_data,
        "opa_input_fixtures": fixtures,
        "parity_report": parity,
        "policy_version_manifest": {
            "policy_id": str(policy.get("metadata", {}).get("id", policy_pack)),
            "policy_version": str(policy.get("metadata", {}).get("version", "unknown")),
            "source_format": "cavra-policy-yaml",
            "generated_formats": ["rego", "json-data", "opa-input-fixtures"],
        },
    }


def policy_to_rego_module(policy: dict[str, Any], *, package: str = "cavra.policy") -> str:
    policy_id = str(policy.get("metadata", {}).get("id", "cavra-policy"))
    title = str(policy.get("metadata", {}).get("title", policy_id))
    return "\n".join(
        [
            f"package {package}",
            "",
            "import future.keywords.if",
            "import future.keywords.in",
            "",
            f"# Generated from CAVRA policy pack: {policy_id}",
            f"# Policy title: {title}",
            "",
            'default decision := {"decision": "require_approval", "rule_id": "runtime.default.require_approval", "severity": "medium", "reason": "No Rego rule matched; review required."}',
            "",
            'decision := {"decision": "block", "rule_id": "filesystem.read.block", "severity": "high", "reason": sprintf("Matched sensitive path policy: %s", [pattern])} if {',
            '  input.action_type == "read_file"',
            "  pattern := data.cavra.policy.filesystem.block_read[_]",
            "  glob.match(pattern, [], input.target)",
            "}",
            "",
            'decision := {"decision": "block", "rule_id": "filesystem.write.block", "severity": "high", "reason": sprintf("Matched sensitive path policy: %s", [pattern])} if {',
            '  input.action_type == "write_file"',
            "  pattern := data.cavra.policy.filesystem.block_write[_]",
            "  glob.match(pattern, [], input.target)",
            "}",
            "",
            'decision := {"decision": "require_approval", "rule_id": "filesystem.write.require_approval", "severity": "high", "approver_group": "Platform Security", "reason": sprintf("Matched approval-required path policy: %s", [pattern])} if {',
            '  input.action_type == "write_file"',
            "  pattern := data.cavra.policy.filesystem.require_approval_write[_]",
            "  glob.match(pattern, [], input.target)",
            "}",
            "",
            'decision := {"decision": "block", "rule_id": "commands.block", "severity": command_severity, "reason": sprintf("Matched blocked command policy: %s", [pattern])} if {',
            '  input.action_type == "execute_command"',
            "  pattern := data.cavra.policy.commands.block[_]",
            "  glob.match(pattern, [], input.requested_operation)",
            "}",
            "",
            'decision := {"decision": "allow", "rule_id": "commands.allow", "severity": "low", "reason": sprintf("Matched allowed command policy: %s", [pattern])} if {',
            '  input.action_type == "execute_command"',
            "  pattern := data.cavra.policy.commands.allow[_]",
            "  glob.match(pattern, [], input.requested_operation)",
            "}",
            "",
            'decision := {"decision": "block", "rule_id": "git.protected_branch.block_direct_push", "severity": "high", "reason": "Direct push to protected branch is prohibited."} if {',
            '  input.action_type == "git_operation"',
            '  input.requested_operation == "push"',
            '  endswith(input.target, "main")',
            "}",
            "",
            'decision := {"decision": "block", "rule_id": "git.protected_branch.block_direct_push", "severity": "high", "reason": "Direct push to protected branch is prohibited."} if {',
            '  input.action_type == "git_operation"',
            '  input.requested_operation == "push"',
            '  endswith(input.target, "master")',
            "}",
            "",
            'decision := {"decision": "block", "rule_id": "mcp.server.trust.block_unknown", "severity": "high", "reason": "Untrusted MCP server with filesystem/tool capability is not approved."} if {',
            '  input.action_type == "mcp_tool_call"',
            "  data.cavra.policy.mcp.block_unknown_servers",
            "  not input.server in data.cavra.policy.mcp.allowed_servers",
            "}",
            "",
            'decision := {"decision": "block", "rule_id": "mcp.server.trust.block_unknown", "severity": "high", "reason": "Untrusted MCP server with filesystem/tool capability is not approved."} if {',
            '  input.action_type == "mcp_tool_call"',
            "  input.server in data.cavra.policy.mcp.blocked_servers",
            "}",
            "",
            'decision := {"decision": "allow", "rule_id": "mcp.server.trust.allow", "severity": "low", "reason": "MCP server is trusted for this tool call."} if {',
            '  input.action_type == "mcp_tool_call"',
            "  input.server in data.cavra.policy.mcp.allowed_servers",
            "  not input.server in data.cavra.policy.mcp.blocked_servers",
            "}",
            "",
            'command_severity := "critical" if {',
            '  contains(input.requested_operation, "apply")',
            "}",
            "",
            'command_severity := "critical" if {',
            '  contains(input.requested_operation, "delete")',
            "}",
            "",
            'command_severity := "high" if {',
            '  not contains(input.requested_operation, "apply")',
            '  not contains(input.requested_operation, "delete")',
            "}",
            "",
        ]
    )


def build_rego_data(policy: dict[str, Any]) -> dict[str, Any]:
    normalized = deepcopy(policy)
    commands = normalized.setdefault("commands", {})
    command_block = _string_list(commands.get("block"))
    command_allow = _string_list(commands.get("allow"))
    return {
        "cavra": {
            "policy": {
                "metadata": normalized.get("metadata", {}),
                "filesystem": {
                    "block_read": _string_list(normalized.get("filesystem", {}).get("block_read")),
                    "block_write": _string_list(normalized.get("filesystem", {}).get("block_write")),
                    "require_approval_write": _string_list(
                        normalized.get("filesystem", {}).get("require_approval_write")
                    ),
                },
                "commands": {
                    "block": command_block,
                    "allow": command_allow,
                    "block_regex": {pattern: pattern_to_regex(pattern) for pattern in command_block},
                    "allow_regex": {pattern: pattern_to_regex(pattern) for pattern in command_allow},
                },
                "git": normalized.get("git", {}),
                "mcp": {
                    "block_unknown_servers": bool(normalized.get("mcp", {}).get("block_unknown_servers", True)),
                    "allowed_servers": _string_list(normalized.get("mcp", {}).get("allowed_servers")),
                    "blocked_servers": _string_list(normalized.get("mcp", {}).get("blocked_servers")),
                },
            }
        }
    }


def pattern_to_regex(pattern: str) -> str:
    return "^" + re.escape(pattern).replace("\\*\\*", ".*").replace("\\*", ".*") + "$"


def build_rego_input(
    action_type: str,
    target: str,
    *,
    requested_operation: str | None = None,
    server: str | None = None,
    tool: str | None = None,
    capability: str | None = None,
) -> dict[str, Any]:
    payload = {
        "schema_version": "cavra.opa-rego-policy.input.v1",
        "action_type": action_type,
        "target": target,
        "requested_operation": requested_operation or target,
    }
    if server is not None:
        payload["server"] = server
    if tool is not None:
        payload["tool"] = tool
    if capability is not None:
        payload["capability"] = capability
    return payload


def build_default_rego_parity_fixtures() -> list[dict[str, Any]]:
    return [
        {
            "case_id": "block_env_read",
            "input": build_rego_input("read_file", ".env", requested_operation="read"),
            "expected_decision": "block",
        },
        {
            "case_id": "approval_policy_write",
            "input": build_rego_input("write_file", "policies/cavra-ai-agent-baseline/policy.yaml", requested_operation="write"),
            "expected_decision": "require_approval",
        },
        {
            "case_id": "allow_terraform_plan",
            "input": build_rego_input("execute_command", "terraform plan", requested_operation="terraform plan"),
            "expected_decision": "allow",
        },
        {
            "case_id": "block_terraform_apply",
            "input": build_rego_input(
                "execute_command",
                "terraform apply -auto-approve",
                requested_operation="terraform apply -auto-approve",
            ),
            "expected_decision": "block",
        },
        {
            "case_id": "block_protected_branch_push",
            "input": build_rego_input("git_operation", "origin/main", requested_operation="push"),
            "expected_decision": "block",
        },
        {
            "case_id": "block_unknown_mcp_server",
            "input": build_rego_input(
                "mcp_tool_call",
                "unknown-filesystem:read_file",
                requested_operation="filesystem",
                server="unknown-filesystem",
                tool="read_file",
                capability="filesystem",
            ),
            "expected_decision": "block",
        },
    ]


def evaluate_rego_compatible_policy(policy: dict[str, Any], rego_input: dict[str, Any]) -> dict[str, Any]:
    data = build_rego_data(policy)["cavra"]["policy"]
    action_type = str(rego_input.get("action_type", ""))
    target = str(rego_input.get("target", ""))
    requested_operation = str(rego_input.get("requested_operation", target)).strip()

    if action_type == "read_file":
        for pattern in data["filesystem"]["block_read"]:
            if _match_pattern(target, pattern):
                return _rego_decision("block", "filesystem.read.block", "high", f"Matched sensitive path policy: {pattern}")
        return _rego_decision("allow", "filesystem.read.allow", "low", "No sensitive path policy matched.")

    if action_type == "write_file":
        for pattern in data["filesystem"]["block_write"]:
            if _match_pattern(target, pattern):
                return _rego_decision("block", "filesystem.write.block", "high", f"Matched sensitive path policy: {pattern}")
        for pattern in data["filesystem"]["require_approval_write"]:
            if _match_pattern(target, pattern):
                return _rego_decision(
                    "require_approval",
                    "filesystem.write.require_approval",
                    "high",
                    f"Matched approval-required path policy: {pattern}",
                    approver_group="Platform Security",
                )
        return _rego_decision("allow", "filesystem.write.allow", "low", "No sensitive path policy matched.")

    if action_type == "execute_command":
        for pattern in data["commands"]["block"]:
            if re.fullmatch(data["commands"]["block_regex"][pattern], requested_operation):
                severity = "critical" if "apply" in requested_operation or "delete" in requested_operation else "high"
                return _rego_decision("block", "commands.block", severity, f"Matched blocked command policy: {pattern}")
        for pattern in data["commands"]["allow"]:
            if re.fullmatch(data["commands"]["allow_regex"][pattern], requested_operation):
                return _rego_decision("allow", "commands.allow", "low", f"Matched allowed command policy: {pattern}")
        return _rego_decision(
            "require_approval",
            "commands.default.require_approval",
            "medium",
            "No allow rule matched; review required.",
            approver_group="Repository Owners",
        )

    if action_type == "git_operation":
        if requested_operation == "push" and (target.endswith("main") or target.endswith("master")):
            return _rego_decision(
                "block",
                "git.protected_branch.block_direct_push",
                "high",
                "Direct push to protected branch is prohibited.",
            )
        return _rego_decision("allow", "git.allow", "low", "Git operation is allowed by policy.")

    if action_type == "mcp_tool_call":
        server = str(rego_input.get("server", target.split(":", 1)[0]))
        allowed = set(data["mcp"]["allowed_servers"])
        blocked = set(data["mcp"]["blocked_servers"])
        if server in blocked or (data["mcp"]["block_unknown_servers"] and server not in allowed):
            return _rego_decision(
                "block",
                "mcp.server.trust.block_unknown",
                "high",
                "Untrusted MCP server with filesystem/tool capability is not approved.",
            )
        return _rego_decision("allow", "mcp.server.trust.allow", "low", "MCP server is trusted for this tool call.")

    return _rego_decision(
        "require_approval",
        "runtime.default.require_approval",
        "medium",
        "No Rego rule matched; review required.",
        approver_group="Repository Owners",
    )


def run_rego_parity_report(
    policy_pack: str = "cavra-ai-agent-baseline",
    *,
    fixtures: list[dict[str, Any]] | None = None,
    policy: dict[str, Any] | None = None,
) -> dict[str, Any]:
    loaded_policy = policy or load_policy_for_rego(policy_pack)
    guard = RuntimeGuard(policy_pack=policy_pack)
    results: list[dict[str, Any]] = []
    for fixture in fixtures or build_default_rego_parity_fixtures():
        rego_input = fixture["input"]
        rego_decision = evaluate_rego_compatible_policy(loaded_policy, rego_input)
        python_decision = _evaluate_python_guard(guard, rego_input)
        passed = (
            rego_decision["decision"] == python_decision["decision"]
            and rego_decision["rule_id"] == python_decision["rule_id"]
            and rego_decision["severity"] == python_decision["severity"]
            and rego_decision["decision"] == fixture.get("expected_decision")
        )
        results.append(
            {
                "case_id": fixture["case_id"],
                "input": rego_input,
                "expected_decision": fixture.get("expected_decision"),
                "rego_decision": rego_decision,
                "python_decision": {
                    "decision": python_decision["decision"],
                    "rule_id": python_decision["rule_id"],
                    "severity": python_decision["severity"],
                    "reason": python_decision["reason"],
                },
                "passed": passed,
            }
        )
    failed = [item for item in results if not item["passed"]]
    return {
        "schema_version": OPA_REGO_PARITY_SCHEMA,
        "policy_pack": policy_pack,
        "case_count": len(results),
        "passed_count": len(results) - len(failed),
        "failed_count": len(failed),
        "required_cases_present": REQUIRED_PARITY_CASES <= {item["case_id"] for item in results},
        "passed": not failed and REQUIRED_PARITY_CASES <= {item["case_id"] for item in results},
        "results": results,
    }


def validate_opa_rego_policy_packet(packet: dict[str, Any], *, require_live: bool = False) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    blockers = 0
    warnings = 0

    blockers += _check(checks, packet.get("schema_version") == OPA_REGO_READINESS_SCHEMA, "schema_version", "OPA/Rego policy evidence packet schema is valid.")
    evidence_mode = str(packet.get("evidence_mode", "sample"))
    if evidence_mode == "live":
        _check(checks, True, "evidence_mode", "Live OPA/Rego policy evidence packet supplied.")
    elif require_live:
        blockers += _check(checks, False, "evidence_mode", "Live OPA/Rego policy evidence is required for this gate.")
    else:
        warnings += _warn(checks, "evidence_mode", "Sample OPA/Rego policy packet validates contract shape only.")

    artifacts = packet.get("rego_artifacts", {})
    artifact_ids = set(artifacts.get("artifact_ids", [])) if isinstance(artifacts, dict) else set()
    blockers += _check(
        checks,
        REQUIRED_REGO_ARTIFACTS <= artifact_ids and bool(artifacts.get("git_versioned")) and bool(artifacts.get("signed_or_reviewed")),
        "rego_artifacts",
        "OPA/Rego artifacts are generated, Git-versioned, and reviewed.",
    )

    parity = packet.get("parity_tests", {})
    case_ids = set(parity.get("case_ids", [])) if isinstance(parity, dict) else set()
    blockers += _check(
        checks,
        REQUIRED_PARITY_CASES <= case_ids
        and int(parity.get("failed_count", 1)) == 0
        and int(parity.get("passed_count", 0)) >= len(REQUIRED_PARITY_CASES),
        "parity_tests",
        "Rego parity tests cover required runtime decisions.",
    )

    lifecycle = packet.get("policy_lifecycle", {})
    blockers += _check(
        checks,
        bool(lifecycle.get("source_policy_yaml"))
        and bool(lifecycle.get("generated_rego_module"))
        and bool(lifecycle.get("review_workflow_ref"))
        and bool(lifecycle.get("rollback_ref")),
        "policy_lifecycle",
        "Policy source, generated Rego, review workflow, and rollback references are present.",
    )

    operating = packet.get("operating_evidence", {})
    blockers += _check(
        checks,
        bool(operating.get("ci_run_ref"))
        and bool(operating.get("parity_report_ref"))
        and bool(operating.get("policy_review_ref")),
        "operating_evidence",
        "OPA/Rego operating evidence references are present.",
    )

    ready_contract = blockers == 0
    ready_live = ready_contract and evidence_mode == "live"
    return {
        "schema_version": "cavra.opa-rego-policy.readiness-result.v1",
        "product": "CAVRA",
        "evidence_mode": evidence_mode,
        "ready_for_opa_rego_policy_contract": ready_contract,
        "ready_for_live_opa_rego_policy_path": ready_live,
        "status": "blocked" if blockers else ("ready_with_warnings" if warnings else "ready"),
        "blocker_count": blockers,
        "warning_count": warnings,
        "checks": checks,
    }


def write_rego_bundle(bundle: dict[str, Any], output_dir: Path) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    module_path = output_dir / "cavra_policy.rego"
    data_path = output_dir / "data.json"
    fixtures_path = output_dir / "opa-input-fixtures.json"
    parity_path = output_dir / "rego-parity-report.json"
    manifest_path = output_dir / "policy-version-manifest.json"
    module_path.write_text(bundle["rego_module"], encoding="utf-8")
    data_path.write_text(json.dumps(bundle["rego_data"], indent=2) + "\n", encoding="utf-8")
    fixtures_path.write_text(json.dumps(bundle["opa_input_fixtures"], indent=2) + "\n", encoding="utf-8")
    parity_path.write_text(json.dumps(bundle["parity_report"], indent=2) + "\n", encoding="utf-8")
    manifest_path.write_text(json.dumps(bundle["policy_version_manifest"], indent=2) + "\n", encoding="utf-8")
    return {
        "schema_version": "cavra.opa-rego-policy.export.v1",
        "output_dir": str(output_dir),
        "artifacts": {
            "rego_module": str(module_path),
            "rego_data": str(data_path),
            "opa_input_fixtures": str(fixtures_path),
            "parity_report": str(parity_path),
            "policy_version_manifest": str(manifest_path),
        },
    }


def _evaluate_python_guard(guard: RuntimeGuard, rego_input: dict[str, Any]) -> dict[str, Any]:
    action_type = str(rego_input.get("action_type", ""))
    target = str(rego_input.get("target", ""))
    requested = str(rego_input.get("requested_operation", target))
    if action_type == "read_file":
        return guard.evaluate_file_access(Path(target), "read").to_dict()
    if action_type == "write_file":
        return guard.evaluate_file_access(Path(target), "write").to_dict()
    if action_type == "execute_command":
        return guard.evaluate_command(requested).to_dict()
    if action_type == "git_operation":
        return guard.evaluate_git_action(requested, target).to_dict()
    if action_type == "mcp_tool_call":
        return guard.evaluate_mcp_tool_call(
            str(rego_input.get("server", target.split(":", 1)[0])),
            str(rego_input.get("tool", "unknown")),
            str(rego_input.get("capability", requested)),
        ).to_dict()
    return guard.evaluate_mcp_tool_call(target, "unknown", action_type).to_dict()


def _match_pattern(value: str, pattern: str) -> bool:
    return re.fullmatch(pattern_to_regex(pattern), value) is not None


def _rego_decision(
    decision: str,
    rule_id: str,
    severity: str,
    reason: str,
    *,
    approver_group: str | None = None,
) -> dict[str, Any]:
    result = {
        "decision": decision,
        "rule_id": rule_id,
        "severity": severity,
        "reason": reason,
    }
    if approver_group:
        result["approver_group"] = approver_group
    return result


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if item is not None]


def _check(checks: list[dict[str, Any]], ok: bool, name: str, message: str) -> int:
    checks.append({"name": name, "status": "pass" if ok else "blocker", "message": message})
    return 0 if ok else 1


def _warn(checks: list[dict[str, Any]], name: str, message: str) -> int:
    checks.append({"name": name, "status": "warn", "message": message})
    return 1
