const scenario = [
  ["read_file", ".env", "block", "filesystem.read.block", "Secrets file cannot be exposed to AI-agent context."],
  ["write_file", "iam/admin-role.tf", "require_approval", "filesystem.write.require_approval", "IAM privilege change in regulated repository requires security approval."],
  ["execute_command", "terraform plan", "allow", "commands.allow", "Read-only infrastructure planning command is permitted."],
  ["execute_command", "terraform apply -auto-approve", "block", "commands.block", "Autonomous production-impacting infrastructure change is prohibited."],
  ["mcp_tool_call", "unknown filesystem MCP server", "block", "mcp.server.trust.block_unknown", "Untrusted MCP server with filesystem capability is not approved."],
  ["git_operation", "git push origin main", "block", "git.protected_branch.block_direct_push", "Direct push to protected branch is prohibited."],
  ["pull_request", "create PR", "allow_with_attestation", "git.pull_request.allow_with_attestation", "PR is allowed with CAVRA evidence and reviewer guidance."]
];

function eventPayload(row, index) {
  const [action_type, target, decision, rule_id, reason] = row;
  return {
    event_id: `evt_${index + 1}`,
    timestamp: new Date().toISOString(),
    agent: "Simulated AI-agent scenario using real CAVRA policy decisions.",
    action_type, target, decision, rule_id, reason,
    policy_pack: "cavra-ai-agent-baseline",
    policy_id: "cavra-ai-agent-baseline",
    severity: decision === "allow" ? "low" : "high",
    business_impact: "Pre-action runtime governance with audit evidence.",
    evidence_generated: [`evidence://sandbox/evt_${index + 1}`],
    remediation: decision === "block" ? "Use an approved workflow or request a policy exception." : "Continue with recorded evidence."
  };
}

async function runScenario() {
  const actions = document.querySelector("#actions");
  const decisions = document.querySelector("#decisions");
  const evidence = document.querySelector("#evidence");
  actions.innerHTML = "";
  decisions.innerHTML = "";
  const events = scenario.map(eventPayload);
  evidence.textContent = "Running...";
  for (const event of events) {
    await new Promise((resolve) => setTimeout(resolve, 280));
    actions.insertAdjacentHTML("beforeend", `<li><strong>${event.action_type}</strong><br>${event.target}</li>`);
    decisions.insertAdjacentHTML("beforeend", `<li class="${event.decision}"><strong>${event.decision}</strong><br>${event.reason}<br><small>${event.rule_id}</small></li>`);
  }
  evidence.textContent = JSON.stringify({ product: "CAVRA", tagline: "Before the agent acts, CAVRA decides.", events }, null, 2);
}

document.querySelector("#runScenario").addEventListener("click", runScenario);
document.querySelector("#copyInstall").addEventListener("click", async () => {
  await navigator.clipboard.writeText("claude mcp add cavra -- cavra-mcp-server");
});
