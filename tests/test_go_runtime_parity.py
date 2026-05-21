from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

from cavra.policy_engine import compile_policy
from cavra.policy_registry import PolicyRegistry
from cavra.registry import RegistryStore
from cavra.runtime import RuntimeGuard


PARITY_CASES = Path("go/cavra-runtime/testdata/parity_cases.json")
TESTDATA = PARITY_CASES.parent
RELEASE_GOVERNANCE_CASES = TESTDATA / "release_governance_records.json"
RELEASE_GOVERNANCE_CONTRACT_CASES = TESTDATA / "release_governance_contracts.json"


def _python_decision(request: dict[str, object], *, registry_store: RegistryStore | None = None) -> dict[str, object]:
    guard = RuntimeGuard(
        policy_pack=str(request.get("policy_pack") or "cavra-ai-agent-baseline"),
        session_id=str(request.get("session_id", "local")),
        agent_id=str(request.get("agent_id", "unknown-agent")),
        actor=str(request.get("actor", "ai-agent")),
        registry_store=registry_store,
    )
    action = request["action_type"]
    if action == "read_file":
        return guard.evaluate_file_access(Path(str(request["target"])), "read").to_dict()
    if action == "write_file":
        return guard.evaluate_file_access(Path(str(request["target"])), "write").to_dict()
    if action == "execute_command":
        return guard.evaluate_command(str(request["target"])).to_dict()
    if action == "git_operation":
        return guard.evaluate_git_action(str(request.get("operation", "push")), str(request.get("target", ""))).to_dict()
    if action == "mcp_tool_call":
        return guard.evaluate_mcp_tool_call(
            str(request["server"]),
            str(request["tool"]),
            str(request.get("capability", "")) or None,
        ).to_dict()
    if action == "release_governance_record":
        record = request.get("record") or request.get("release_governance")
        assert isinstance(record, dict)
        return guard.evaluate_release_governance_record(
            record,
            target=str(request.get("target", "")) or None,
            requested_operation=str(request.get("operation", request.get("requested_operation", "verify"))),
        ).to_dict()
    raise AssertionError(f"unsupported parity action: {action}")


def _registry_store(tmp_path: Path, registry_name: str | None) -> RegistryStore | None:
    if not registry_name:
        return None
    payload = json.loads((TESTDATA / registry_name).read_text(encoding="utf-8"))
    store = RegistryStore(tmp_path / f"{registry_name}.json")
    for server in payload.get("mcp_servers", []):
        store.upsert_mcp_server(server)
    return store


def test_go_parity_cases_match_python_runtime_expectations(tmp_path: Path) -> None:
    cases = json.loads(PARITY_CASES.read_text(encoding="utf-8"))
    for item in cases:
        decision = _python_decision(item["request"], registry_store=_registry_store(tmp_path, item.get("registry")))
        expected = item["expected"]
        assert decision["decision"] == expected["decision"], item["name"]
        assert decision["rule_id"] == expected["rule_id"], item["name"]
        assert decision["severity"] == expected["severity"], item["name"]
        if expected.get("approver_group"):
            assert decision["approver_group"] == expected["approver_group"], item["name"]
        if expected.get("evidence_ref_prefix"):
            assert decision["decision_id"], item["name"]
            assert decision["timestamp"], item["name"]
            assert str(decision["correlation_id"]).startswith("corr_"), item["name"]
            assert decision["evidence_refs"], item["name"]
            assert str(decision["evidence_refs"][0]).startswith(expected["evidence_ref_prefix"]), item["name"]


def test_go_release_governance_cases_match_python_runtime_expectations() -> None:
    cases = json.loads(RELEASE_GOVERNANCE_CASES.read_text(encoding="utf-8"))
    for item in cases:
        decision = _python_decision(item["request"])
        expected = item["expected"]
        assert decision["decision"] == expected["decision"], item["name"]
        assert decision["rule_id"] == expected["rule_id"], item["name"]
        assert decision["severity"] == expected["severity"], item["name"]
        if expected.get("approver_group"):
            assert decision["approver_group"] == expected["approver_group"], item["name"]
        if expected.get("evidence_ref_prefix"):
            assert decision["decision_id"], item["name"]
            assert decision["timestamp"], item["name"]
            assert str(decision["correlation_id"]).startswith("corr_"), item["name"]
            assert decision["evidence_refs"], item["name"]
            assert str(decision["evidence_refs"][0]).startswith(expected["evidence_ref_prefix"]), item["name"]


def test_go_release_governance_contract_cases_match_python_runtime_expectations() -> None:
    cases = json.loads(RELEASE_GOVERNANCE_CONTRACT_CASES.read_text(encoding="utf-8"))
    for item in cases:
        decision = _python_decision(item["request"])
        expected = item["expected"]
        assert decision["decision"] == expected["decision"], item["name"]
        assert decision["rule_id"] == expected["rule_id"], item["name"]
        assert decision["severity"] == expected["severity"], item["name"]
        if expected.get("approver_group"):
            assert decision["approver_group"] == expected["approver_group"], item["name"]


@pytest.mark.skipif(shutil.which("go") is None, reason="go toolchain is not installed")
def test_go_runtime_scaffold_tests_pass() -> None:
    subprocess.run(["go", "test", "./..."], cwd=Path("go/cavra-runtime"), check=True)


@pytest.mark.skipif(shutil.which("go") is None, reason="go toolchain is not installed")
def test_go_runtime_cli_accepts_compiled_policy_fixture() -> None:
    request = {
        "action_type": "read_file",
        "target": "config/prod.secret",
    }
    completed = subprocess.run(
        [
            "go",
            "run",
            "./cmd/cavra-runtime",
            "--policy",
            "testdata/compiled_policy.json",
        ],
        cwd=Path("go/cavra-runtime"),
        input=json.dumps(request),
        text=True,
        check=True,
        capture_output=True,
    )
    decision = json.loads(completed.stdout)

    assert decision["decision"] == "block"
    assert decision["rule_id"] == "filesystem.read.block"
    assert decision["policy_pack"] == "cavra-go-compiled-fixture"


@pytest.mark.skipif(shutil.which("go") is None, reason="go toolchain is not installed")
def test_go_runtime_cli_accepts_mcp_registry_fixture() -> None:
    request = {
        "session_id": "cli-registry",
        "action_type": "mcp_tool_call",
        "server": "github-mcp",
        "tool": "delete_repository",
        "capability": "repository",
        "policy_pack": "cavra-mcp-enterprise",
    }
    completed = subprocess.run(
        [
            "go",
            "run",
            "./cmd/cavra-runtime",
            "--registry",
            "testdata/mcp_registry.json",
        ],
        cwd=Path("go/cavra-runtime"),
        input=json.dumps(request),
        text=True,
        check=True,
        capture_output=True,
    )
    decision = json.loads(completed.stdout)

    assert decision["decision"] == "require_approval"
    assert decision["rule_id"] == "mcp.registry.tool_scope"
    assert decision["approver_group"] == "AI Governance"
    assert decision["evidence_refs"][0].startswith("evidence://cli-registry/")


@pytest.mark.skipif(shutil.which("go") is None, reason="go toolchain is not installed")
def test_go_runtime_accepts_all_bundled_compiled_policy_packs(tmp_path: Path) -> None:
    binary = tmp_path / "cavra-runtime"
    subprocess.run(
        ["go", "build", "-o", str(binary), "./cmd/cavra-runtime"],
        cwd=Path("go/cavra-runtime"),
        check=True,
    )
    registry = PolicyRegistry()
    for pack in registry.list_policy_packs():
        policy_pack = pack["id"]
        compiled = compile_policy(registry.load_policy(policy_pack))
        policy_path = tmp_path / f"{policy_pack}.json"
        policy_path.write_text(json.dumps(compiled), encoding="utf-8")
        for request in _representative_policy_requests(policy_pack, compiled):
            expected = _python_decision(request)
            completed = subprocess.run(
                [str(binary), "--policy", str(policy_path)],
                input=json.dumps(request),
                text=True,
                check=True,
                capture_output=True,
            )
            actual = json.loads(completed.stdout)

            case_name = f"{policy_pack} {request['action_type']} {request.get('target') or request.get('server')}"
            assert actual["decision"] == expected["decision"], case_name
            assert actual["rule_id"] == expected["rule_id"], case_name
            assert actual["severity"] == expected["severity"], case_name
            if expected.get("approver_group"):
                assert actual["approver_group"] == expected["approver_group"], case_name
            assert actual["policy_pack"] == policy_pack, case_name
            assert actual["evidence_refs"][0].startswith("evidence://"), case_name


def test_go_compiled_policy_fixture_shape_is_supported() -> None:
    fixture = json.loads(Path("go/cavra-runtime/testdata/compiled_policy.json").read_text(encoding="utf-8"))

    assert fixture["metadata"]["id"] == "cavra-go-compiled-fixture"
    assert fixture["filesystem"]["block_read"] == ["**/*.secret"]
    assert fixture["commands"]["allow"] == ["custom scan*"]
    assert fixture["mcp"]["block_unknown_servers"] is True


def test_go_mcp_registry_fixture_shape_is_supported() -> None:
    fixture = json.loads((TESTDATA / "mcp_registry.json").read_text(encoding="utf-8"))

    assert {item["server_id"] for item in fixture["mcp_servers"]} >= {"github-mcp", "filesystem-lab", "personal-drive-mcp"}
    assert next(item for item in fixture["mcp_servers"] if item["server_id"] == "github-mcp")["allowed_tools"] == ["create_pull_request"]


def test_go_release_governance_record_fixture_shape_is_supported() -> None:
    cases = json.loads(RELEASE_GOVERNANCE_CASES.read_text(encoding="utf-8"))
    metadata_kinds = {item["request"]["record"]["metadata_kind"] for item in cases}
    rule_ids = {item["expected"]["rule_id"] for item in cases}

    assert metadata_kinds >= {
        "release-channel-promotion-request",
        "rollout-promotion-execution",
        "rollout-rollback-execution",
        "endpoint-drift-remediation-request",
        "endpoint-management-publication-delivery",
        "release-connector-delivery",
        "endpoint-inventory-freshness-report",
        "managed-endpoint-reconciliation",
        "endpoint-remediation-sla-report",
        "endpoint-remediation-handoff-status",
        "endpoint-remediation-handoff",
        "rollout-evidence-verification",
        "rollout-artifact-integrity",
    }
    assert rule_ids >= {
        "release_governance.approval.pending",
        "release_governance.approval.approved",
        "release_governance.approval.missing",
        "release_governance.approval.denied",
        "release_governance.delivery.failed",
        "release_governance.signal.critical",
        "release_governance.record.verified",
    }


def _representative_policy_requests(policy_pack: str, compiled: dict[str, object]) -> list[dict[str, str]]:
    filesystem = compiled.get("filesystem") if isinstance(compiled.get("filesystem"), dict) else {}
    commands = compiled.get("commands") if isinstance(compiled.get("commands"), dict) else {}
    mcp = compiled.get("mcp") if isinstance(compiled.get("mcp"), dict) else {}
    requests: list[dict[str, str]] = []
    if filesystem.get("block_read"):
        requests.append(
            {
                "session_id": f"{policy_pack}-block-read",
                "action_type": "read_file",
                "target": _target_for_pattern(str(filesystem["block_read"][0])),
                "policy_pack": policy_pack,
            }
        )
    if filesystem.get("block_write"):
        requests.append(
            {
                "session_id": f"{policy_pack}-block-write",
                "action_type": "write_file",
                "target": _target_for_pattern(str(filesystem["block_write"][0])),
                "policy_pack": policy_pack,
            }
        )
    if filesystem.get("require_approval_write"):
        requests.append(
            {
                "session_id": f"{policy_pack}-approval-write",
                "action_type": "write_file",
                "target": _target_for_pattern(str(filesystem["require_approval_write"][0])),
                "policy_pack": policy_pack,
            }
        )
    if commands.get("block"):
        command = _command_for_pattern(str(commands["block"][0]))
        requests.append(
            {
                "session_id": f"{policy_pack}-block-command",
                "action_type": "execute_command",
                "target": command,
                "policy_pack": policy_pack,
            }
        )
    if commands.get("allow"):
        command = _command_for_pattern(str(commands["allow"][0]))
        requests.append(
            {
                "session_id": f"{policy_pack}-allow-command",
                "action_type": "execute_command",
                "target": command,
                "policy_pack": policy_pack,
            }
        )
    if mcp.get("allowed_servers"):
        requests.append(
            {
                "session_id": f"{policy_pack}-mcp-allow",
                "action_type": "mcp_tool_call",
                "server": str(mcp["allowed_servers"][0]),
                "tool": "read_file",
                "capability": "filesystem",
                "policy_pack": policy_pack,
            }
        )
    if mcp.get("blocked_servers"):
        requests.append(
            {
                "session_id": f"{policy_pack}-mcp-block",
                "action_type": "mcp_tool_call",
                "server": str(mcp["blocked_servers"][0]),
                "tool": "read_file",
                "capability": "filesystem",
                "policy_pack": policy_pack,
            }
        )
    return requests


def _target_for_pattern(pattern: str) -> str:
    if pattern == ".env":
        return ".env"
    if pattern.startswith(".github/"):
        return pattern.replace("**", "cavra-required-check.yml").replace("*", "security")
    if pattern.startswith(".gitlab"):
        return pattern.replace("**", "ci.yml").replace("*", "security")
    cleaned = pattern
    cleaned = cleaned.replace("**/", "src/")
    cleaned = cleaned.replace("/**", "/policy.yaml")
    cleaned = cleaned.replace("**", "src")
    cleaned = cleaned.replace("*", "sample")
    if cleaned.endswith("/"):
        cleaned += "file.txt"
    if "." not in Path(cleaned).name:
        cleaned += "/file.txt" if cleaned.endswith("src") else ""
    return cleaned


def _command_for_pattern(pattern: str) -> str:
    if pattern.endswith("*"):
        prefix = pattern[:-1].strip()
        suffixes = {
            "aws iam": " create-role",
            "az role": " assignment create",
            "gcloud projects add-iam-policy-binding": " cavra-prod",
            "kubectl delete": " pod cavra-prod",
            "terraform apply": " -auto-approve",
            "gitlab project-settings update": " --protected-branches=false",
            "gh api repos": "/owner/repo/actions/secrets",
        }
        return prefix + suffixes.get(prefix, " --check")
    return pattern
