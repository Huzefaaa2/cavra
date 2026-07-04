package cavra.policy

import future.keywords.if
import future.keywords.in

# Generated from CAVRA policy pack: cavra-ai-agent-baseline
# Policy title: CAVRA AI Agent Baseline

default decision := {"decision": "require_approval", "rule_id": "runtime.default.require_approval", "severity": "medium", "reason": "No Rego rule matched; review required."}

decision := {"decision": "block", "rule_id": "filesystem.read.block", "severity": "high", "reason": sprintf("Matched sensitive path policy: %s", [pattern])} if {
  input.action_type == "read_file"
  pattern := data.cavra.policy.filesystem.block_read[_]
  glob.match(pattern, [], input.target)
}

decision := {"decision": "block", "rule_id": "filesystem.write.block", "severity": "high", "reason": sprintf("Matched sensitive path policy: %s", [pattern])} if {
  input.action_type == "write_file"
  pattern := data.cavra.policy.filesystem.block_write[_]
  glob.match(pattern, [], input.target)
}

decision := {"decision": "require_approval", "rule_id": "filesystem.write.require_approval", "severity": "high", "approver_group": "Platform Security", "reason": sprintf("Matched approval-required path policy: %s", [pattern])} if {
  input.action_type == "write_file"
  pattern := data.cavra.policy.filesystem.require_approval_write[_]
  glob.match(pattern, [], input.target)
}

decision := {"decision": "block", "rule_id": "commands.block", "severity": command_severity, "reason": sprintf("Matched blocked command policy: %s", [pattern])} if {
  input.action_type == "execute_command"
  pattern := data.cavra.policy.commands.block[_]
  glob.match(pattern, [], input.requested_operation)
}

decision := {"decision": "allow", "rule_id": "commands.allow", "severity": "low", "reason": sprintf("Matched allowed command policy: %s", [pattern])} if {
  input.action_type == "execute_command"
  pattern := data.cavra.policy.commands.allow[_]
  glob.match(pattern, [], input.requested_operation)
}

decision := {"decision": "block", "rule_id": "git.protected_branch.block_direct_push", "severity": "high", "reason": "Direct push to protected branch is prohibited."} if {
  input.action_type == "git_operation"
  input.requested_operation == "push"
  endswith(input.target, "main")
}

decision := {"decision": "block", "rule_id": "git.protected_branch.block_direct_push", "severity": "high", "reason": "Direct push to protected branch is prohibited."} if {
  input.action_type == "git_operation"
  input.requested_operation == "push"
  endswith(input.target, "master")
}

decision := {"decision": "block", "rule_id": "mcp.server.trust.block_unknown", "severity": "high", "reason": "Untrusted MCP server with filesystem/tool capability is not approved."} if {
  input.action_type == "mcp_tool_call"
  data.cavra.policy.mcp.block_unknown_servers
  not input.server in data.cavra.policy.mcp.allowed_servers
}

decision := {"decision": "block", "rule_id": "mcp.server.trust.block_unknown", "severity": "high", "reason": "Untrusted MCP server with filesystem/tool capability is not approved."} if {
  input.action_type == "mcp_tool_call"
  input.server in data.cavra.policy.mcp.blocked_servers
}

decision := {"decision": "allow", "rule_id": "mcp.server.trust.allow", "severity": "low", "reason": "MCP server is trusted for this tool call."} if {
  input.action_type == "mcp_tool_call"
  input.server in data.cavra.policy.mcp.allowed_servers
  not input.server in data.cavra.policy.mcp.blocked_servers
}

command_severity := "critical" if {
  contains(input.requested_operation, "apply")
}

command_severity := "critical" if {
  contains(input.requested_operation, "delete")
}

command_severity := "high" if {
  not contains(input.requested_operation, "apply")
  not contains(input.requested_operation, "delete")
}
