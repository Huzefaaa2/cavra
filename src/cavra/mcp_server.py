from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from cavra.runtime import RuntimeGuard

TOOLS = [
    "cavra.evaluate_action",
    "cavra.check_file_read",
    "cavra.check_file_write",
    "cavra.check_command",
    "cavra.check_git_operation",
    "cavra.check_mcp_tool_call",
    "cavra.explain_decision",
    "cavra.generate_pr_attestation",
    "cavra.export_evidence",
    "cavra.policy_list",
    "cavra.policy_validate",
    "cavra.session_start",
    "cavra.session_summary",
]


def list_tools() -> list[dict[str, Any]]:
    return [{"name": name, "description": f"{name} CAVRA governance tool"} for name in TOOLS]


def evaluate_tool(name: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
    args = arguments or {}
    guard = RuntimeGuard(policy_pack=args.get("policy_pack") or "cavra-ai-agent-baseline")
    if name in {"cavra.check_file_read", "cavra.evaluate_action"} and args.get("action_type", "read_file") == "read_file":
        return guard.evaluate_file_access(Path(args.get("path") or args.get("target") or ".env"), "read").to_dict()
    if name == "cavra.check_file_write" or args.get("action_type") == "write_file":
        return guard.evaluate_file_access(Path(args.get("path") or args.get("target") or "iam/admin-role.tf"), "write").to_dict()
    if name == "cavra.check_command" or args.get("action_type") == "execute_command":
        return guard.evaluate_command(args.get("command") or args.get("target") or "terraform plan").to_dict()
    if name == "cavra.check_git_operation" or args.get("action_type") == "git_operation":
        return guard.evaluate_git_action(args.get("operation", "push"), args.get("target", "origin/main")).to_dict()
    if name == "cavra.check_mcp_tool_call" or args.get("action_type") == "mcp_tool_call":
        return guard.evaluate_mcp_tool_call(args.get("server", "unknown-filesystem"), args.get("tool", "read_file"), args.get("capability", "filesystem")).to_dict()
    if name == "cavra.generate_pr_attestation":
        return guard.generate_pr_attestation_decision(args.get("target", "create PR")).to_dict()
    return {"status": "ok", "tool": name, "product": "CAVRA"}


def handle_json_rpc(message: dict[str, Any]) -> dict[str, Any] | None:
    method = message.get("method")
    msg_id = message.get("id")
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": list_tools()}}
    if method == "tools/call":
        params = message.get("params", {})
        result = evaluate_tool(params.get("name", ""), params.get("arguments", {}))
        return {"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(result)}]}}
    if method == "initialize":
        return {"jsonrpc": "2.0", "id": msg_id, "result": {"protocolVersion": "2024-11-05", "serverInfo": {"name": "cavra-mcp-server", "version": "0.1.0"}, "capabilities": {"tools": {}}}}
    if method == "notifications/initialized":
        return None
    return {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Unknown method: {method}"}}


def main() -> None:
    parser = argparse.ArgumentParser(description="CAVRA MCP server for AI-agent runtime governance.")
    parser.add_argument("--list-tools", action="store_true", help="Print available CAVRA MCP tools and exit.")
    parser.add_argument("--check-command", help="Evaluate a command and exit.")
    args = parser.parse_args()
    if args.list_tools:
        print(json.dumps({"tools": list_tools()}, indent=2))
        return
    if args.check_command:
        print(json.dumps(evaluate_tool("cavra.check_command", {"command": args.check_command}), indent=2))
        return
    for line in sys.stdin:
        if not line.strip():
            continue
        response = handle_json_rpc(json.loads(line))
        if response is not None:
            print(json.dumps(response), flush=True)


if __name__ == "__main__":
    main()
