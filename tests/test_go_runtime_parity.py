from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

from cavra.registry import RegistryStore
from cavra.runtime import RuntimeGuard


PARITY_CASES = Path("go/cavra-runtime/testdata/parity_cases.json")
TESTDATA = PARITY_CASES.parent


def _python_decision(request: dict[str, str], *, registry_store: RegistryStore | None = None) -> dict[str, object]:
    guard = RuntimeGuard(
        policy_pack=request.get("policy_pack") or "cavra-ai-agent-baseline",
        session_id=request.get("session_id", "local"),
        agent_id=request.get("agent_id", "unknown-agent"),
        actor=request.get("actor", "ai-agent"),
        registry_store=registry_store,
    )
    action = request["action_type"]
    if action == "read_file":
        return guard.evaluate_file_access(Path(request["target"]), "read").to_dict()
    if action == "write_file":
        return guard.evaluate_file_access(Path(request["target"]), "write").to_dict()
    if action == "execute_command":
        return guard.evaluate_command(request["target"]).to_dict()
    if action == "git_operation":
        return guard.evaluate_git_action(request.get("operation", "push"), request.get("target")).to_dict()
    if action == "mcp_tool_call":
        return guard.evaluate_mcp_tool_call(request["server"], request["tool"], request.get("capability")).to_dict()
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
