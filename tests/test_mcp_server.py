from cavra.mcp_server import evaluate_tool, list_tools


def test_mcp_tools_are_listed() -> None:
    names = {tool["name"] for tool in list_tools()}
    assert "cavra.check_file_read" in names
    assert "cavra.check_command" in names


def test_mcp_file_read_blocks_env() -> None:
    decision = evaluate_tool("cavra.check_file_read", {"path": ".env"})
    assert decision["decision"] == "block"


def test_mcp_command_allows_terraform_plan() -> None:
    decision = evaluate_tool("cavra.check_command", {"command": "terraform plan"})
    assert decision["decision"] == "allow"


def test_mcp_command_blocks_terraform_apply_auto_approve() -> None:
    decision = evaluate_tool("cavra.check_command", {"command": "terraform apply -auto-approve"})
    assert decision["decision"] == "block"


def test_mcp_unknown_filesystem_server_blocks() -> None:
    decision = evaluate_tool(
        "cavra.check_mcp_tool_call",
        {"server": "unknown-filesystem", "tool": "read_file", "capability": "filesystem"},
    )
    assert decision["decision"] == "block"
    assert decision["evidence_refs"]
