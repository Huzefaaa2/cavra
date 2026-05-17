const scenario = [
  ["read_file", ".env", "block", "filesystem.read.block", "Secrets file cannot be exposed to AI-agent context."],
  ["write_file", "iam/admin-role.tf", "require_approval", "filesystem.write.require_approval", "IAM privilege change in regulated repository requires security approval."],
  ["execute_command", "terraform plan", "allow", "commands.allow", "Read-only infrastructure planning command is permitted."],
  ["execute_command", "terraform apply -auto-approve", "block", "commands.block", "Autonomous production-impacting infrastructure change is prohibited."],
  ["mcp_tool_call", "unknown filesystem MCP server", "block", "mcp.server.trust.block_unknown", "Untrusted MCP server with filesystem capability is not approved."],
  ["git_operation", "git push origin main", "block", "git.protected_branch.block_direct_push", "Direct push to protected branch is prohibited."],
  ["pull_request", "create PR", "allow_with_attestation", "git.pull_request.allow_with_attestation", "PR is allowed with CAVRA evidence and reviewer guidance."]
];

const evidenceCatalog = [
  {
    session_id: "demo-session",
    signer: "platform-security",
    decision_count: 7,
    blocked_count: 4,
    approval_required_count: 1,
    retention: { retention_days: 2555, retain_until: "2033-05-15T00:00:00Z" },
    decisions: scenario.map(eventPayload),
    attestation_targets: scenario.map((row) => row[1])
  },
  {
    session_id: "docs-agent-run",
    signer: "docs-agent",
    decision_count: 4,
    blocked_count: 0,
    approval_required_count: 0,
    retention: { retention_days: 365, retain_until: "2027-05-17T00:00:00Z" },
    decisions: scenario.slice(2, 6).map(eventPayload),
    attestation_targets: scenario.slice(2, 6).map((row) => row[1])
  },
  {
    session_id: "security-review",
    signer: "security-agent",
    decision_count: 5,
    blocked_count: 2,
    approval_required_count: 1,
    retention: { retention_days: 2555, retain_until: "2033-05-15T00:00:00Z" },
    decisions: scenario.slice(0, 5).map(eventPayload),
    attestation_targets: scenario.slice(0, 5).map((row) => row[1])
  }
];

const activitySessions = evidenceCatalog.map((item) => ({
  schema_version: "cavra.session.v1",
  session_id: item.session_id,
  agent_id: item.session_id === "docs-agent-run" ? "docs-agent" : "codex-agent",
  actor: item.signer,
  repository: item.session_id === "security-review" ? "platform/security" : "payments/api",
  policy_pack: "cavra-ai-agent-baseline",
  state: "active",
  started_at: "2026-05-18T00:00:00+00:00",
  updated_at: "2026-05-18T00:10:00+00:00",
  decision_count: item.decision_count,
  blocked_count: item.blocked_count,
  approval_required_count: item.approval_required_count,
  evidence_refs: [`evidence://${item.session_id}`]
}));

const activityDecisions = evidenceCatalog.flatMap((item) =>
  item.decisions.map((decision, index) => ({
    schema_version: "cavra.decision.v1",
    decision_id: `dec_${item.session_id}_${index + 1}`,
    session_id: item.session_id,
    agent_id: item.session_id === "docs-agent-run" ? "docs-agent" : "codex-agent",
    actor: item.signer,
    repository: item.session_id === "security-review" ? "platform/security" : "payments/api",
    policy_pack: decision.policy_pack,
    policy_id: decision.policy_id,
    action_type: decision.action_type,
    target: decision.target,
    requested_operation: decision.action_type,
    rule_id: decision.rule_id,
    decision: decision.decision,
    severity: decision.severity,
    reason: decision.reason,
    timestamp: decision.timestamp,
    correlation_id: `corr_${item.session_id}_${index + 1}`,
    evidence_refs: decision.evidence_generated || []
  }))
);

const repositoryCatalog = [
  {
    repository_id: "payments/api",
    repository: "payments/api",
    provider: "github",
    owner: "Payments Platform",
    business_unit: "payments",
    environment: "production",
    policy_pack: "cavra-banking",
    risk_tier: "high",
    status: "active",
    protected_branches: ["main", "release/*"],
    required_checks: ["cavra", "CodeQL"]
  },
  {
    repository_id: "platform/security",
    repository: "platform/security",
    provider: "github",
    owner: "Platform Security",
    business_unit: "platform",
    environment: "production",
    policy_pack: "cavra-ai-agent-baseline",
    risk_tier: "medium",
    status: "active",
    protected_branches: ["main"],
    required_checks: ["cavra"]
  },
  {
    repository_id: "docs/site",
    repository: "docs/site",
    provider: "github",
    owner: "Documentation",
    business_unit: "engineering",
    environment: "development",
    policy_pack: "cavra-ai-agent-baseline",
    risk_tier: "low",
    status: "active",
    protected_branches: ["main"],
    required_checks: []
  }
];

const rolloutCatalog = [
  {
    rollout_id: "payments-api-banking",
    repository: "payments/api",
    policy_pack: "cavra-banking",
    policy_version: "2026.05",
    mode: "strict",
    state: "active",
    owner: "Platform Security",
    coverage_percent: 95
  },
  {
    rollout_id: "platform-security-baseline",
    repository: "platform/security",
    policy_pack: "cavra-ai-agent-baseline",
    policy_version: "latest",
    mode: "enforce",
    state: "active",
    owner: "Platform Security",
    coverage_percent: 88
  },
  {
    rollout_id: "docs-site-baseline",
    repository: "docs/site",
    policy_pack: "cavra-ai-agent-baseline",
    policy_version: "latest",
    mode: "audit_only",
    state: "planned",
    owner: "Documentation",
    coverage_percent: 20
  }
];

const approvalCatalog = [
  {
    approval_id: "apr_demo_iam",
    decision_id: "dec_demo_iam",
    session_id: "demo-session",
    state: "pending",
    approver_group: "IAM",
    requested_by: "developer",
    requested_at: new Date().toISOString(),
    expires_at: "2026-05-18T00:00:00Z",
    external_ref: "CHG-100",
    decision: { target: "iam/admin-role.tf", rule_id: "filesystem.write.require_approval", reason: "IAM privilege change requires review." },
    evidence_refs: ["approval://apr_demo_iam", "evidence://demo-session/dec_demo_iam"],
    history: [
      { event: "requested", actor: "developer", timestamp: new Date().toISOString(), reason: "IAM privilege change requires review." }
    ]
  },
  {
    approval_id: "apr_break_glass",
    decision_id: "dec_incident",
    session_id: "incident-session",
    state: "break_glass",
    approver_group: "Change Advisory Board",
    requested_by: "incident-commander",
    requested_at: new Date().toISOString(),
    expires_at: "2026-05-17T20:00:00Z",
    external_ref: "INC-777",
    break_glass: true,
    break_glass_reason: "Production recovery for active incident.",
    decision: { target: "terraform apply", rule_id: "commands.block", reason: "Autonomous production-impacting infrastructure change is prohibited." },
    evidence_refs: ["approval://apr_break_glass", "incident://INC-777"],
    history: [
      { event: "break_glass", actor: "incident-commander", timestamp: new Date().toISOString(), reason: "Production recovery for active incident." }
    ]
  }
];

const agentCatalog = [
  {
    agent_id: "claude-code",
    vendor: "Anthropic",
    owner: "AI Platform",
    status: "active",
    capabilities: ["code_edit", "test", "mcp_tool_call"],
    risk_tier: "high"
  },
  {
    agent_id: "codex-agent",
    vendor: "OpenAI",
    owner: "Developer Platform",
    status: "active",
    capabilities: ["code_edit", "test", "git_operation"],
    risk_tier: "high"
  },
  {
    agent_id: "docs-agent",
    vendor: "CAVRA",
    owner: "Documentation",
    status: "active",
    capabilities: ["documentation", "diagram_update"],
    risk_tier: "low"
  }
];

const mcpCatalog = [
  {
    server_id: "github-mcp",
    name: "GitHub MCP",
    trust_tier: "approved",
    approval_state: "approved",
    capabilities: ["repository", "saas"],
    allowed_tools: ["create_pull_request", "create_issue"]
  },
  {
    server_id: "filesystem-mcp",
    name: "Filesystem MCP",
    trust_tier: "experimental",
    approval_state: "pending",
    capabilities: ["filesystem"],
    allowed_tools: ["read_file"]
  },
  {
    server_id: "unknown-filesystem",
    name: "Unknown Filesystem",
    trust_tier: "blocked",
    approval_state: "denied",
    capabilities: ["filesystem"],
    allowed_tools: []
  }
];

const agentProfiles = [
  ["claude-code", "Claude Code", "Anthropic", "high", ["code_edit", "test", "shell", "mcp_tool_call"]],
  ["codex", "OpenAI Codex", "OpenAI", "high", ["code_edit", "test", "shell", "git_operation"]],
  ["github-copilot", "GitHub Copilot Agent", "GitHub", "medium", ["code_edit", "test", "pull_request"]],
  ["cursor", "Cursor Agent", "Cursor", "medium", ["code_edit", "test", "repository_search"]],
  ["gemini-cli", "Gemini CLI", "Google", "high", ["code_edit", "test", "cloud_assistance"]],
  ["aws-q-developer", "AWS Q Developer", "AWS", "high", ["code_edit", "iam_review", "cloud_assistance"]]
].map(([profile_id, display_name, vendor, risk_tier, default_capabilities]) => ({
  profile_id, display_name, vendor, risk_tier, default_capabilities
}));

const mcpClassifications = [
  ["filesystem", "local_resource", "high", "Prevent unapproved file and secret access."],
  ["shell", "execution", "critical", "Route command execution through policy and approval gates."],
  ["network", "egress", "medium", "Control data egress and supply-chain downloads."],
  ["database", "data_access", "high", "Protect regulated data stores from autonomous reads and writes."],
  ["saas", "enterprise_workflow", "medium", "Keep workflow automation scoped to approved tools."],
  ["cloud", "infrastructure", "critical", "Prevent unapproved IAM and production changes."],
  ["repository", "source_control", "medium", "Govern source-control automation and workflow changes."]
].map(([capability, category, risk_tier, control_objective]) => ({
  capability, category, risk_tier, control_objective
}));

let consoleConfig = null;

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

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, (char) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    "\"": "&quot;",
    "'": "&#39;"
  })[char]);
}

function apiUrl(path, params = {}) {
  const configuredBase = window.CAVRA_API_BASE || consoleConfig?.api_base_url || "";
  const base = configuredBase || window.location.origin;
  const url = new URL(path, base);
  for (const [key, value] of Object.entries(params)) {
    if (value !== undefined && value !== null && value !== "") {
      url.searchParams.set(key, value);
    }
  }
  return url.toString();
}

async function loadConsoleConfig() {
  if (consoleConfig) return consoleConfig;
  try {
    const response = await fetch(apiUrl("/console/config"));
    if (!response.ok) throw new Error("config unavailable");
    consoleConfig = await response.json();
  } catch {
    consoleConfig = {
      product: "CAVRA",
      api_base_url: window.CAVRA_API_BASE || "",
      metadata_mode: "sample",
      cors_origins: []
    };
  }
  const status = document.querySelector("#apiStatus");
  if (status) {
    const mode = consoleConfig.metadata_mode || "sample";
    status.textContent = `API: ${mode}`;
  }
  return consoleConfig;
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

async function loadEvidenceMetadata() {
  await loadConsoleConfig();
  try {
    const params = {
      signer: document.querySelector("#filterSigner")?.value.trim(),
      min_blocked: document.querySelector("#filterBlocked")?.value || 0,
      has_approvals: document.querySelector("#filterApprovals")?.value,
      limit: document.querySelector("#filterLimit")?.value || 10
    };
    const response = await fetch(apiUrl("/evidence", params));
    if (!response.ok) throw new Error("API unavailable");
    const payload = await response.json();
    return Array.isArray(payload) ? payload : payload.items || [];
  } catch {
    return evidenceCatalog;
  }
}

async function loadSessions() {
  await loadConsoleConfig();
  try {
    const params = {
      repository: document.querySelector("#filterActivityRepository")?.value.trim(),
      agent_id: document.querySelector("#filterActivityAgent")?.value.trim(),
      policy_pack: document.querySelector("#filterActivityPolicy")?.value.trim(),
      limit: 25
    };
    const response = await fetch(apiUrl("/sessions", params));
    if (!response.ok) throw new Error("Session API unavailable");
    const payload = await response.json();
    return Array.isArray(payload) ? payload : payload.items || [];
  } catch {
    return activitySessions;
  }
}

async function loadDecisions() {
  await loadConsoleConfig();
  try {
    const params = {
      repository: document.querySelector("#filterActivityRepository")?.value.trim(),
      agent_id: document.querySelector("#filterActivityAgent")?.value.trim(),
      policy_pack: document.querySelector("#filterActivityPolicy")?.value.trim(),
      decision: document.querySelector("#filterDecisionState")?.value,
      severity: document.querySelector("#filterDecisionSeverity")?.value,
      limit: 25
    };
    const response = await fetch(apiUrl("/decisions", params));
    if (!response.ok) throw new Error("Decision API unavailable");
    const payload = await response.json();
    return Array.isArray(payload) ? payload : payload.items || [];
  } catch {
    return activityDecisions;
  }
}

async function loadRepositories() {
  await loadConsoleConfig();
  try {
    const params = {
      owner: document.querySelector("#filterRepositoryOwner")?.value.trim(),
      policy_pack: document.querySelector("#filterRepositoryPolicy")?.value.trim(),
      risk_tier: document.querySelector("#filterRepositoryRisk")?.value
    };
    const response = await fetch(apiUrl("/repositories", params));
    if (!response.ok) throw new Error("Repository API unavailable");
    const payload = await response.json();
    return Array.isArray(payload) ? payload : payload.items || [];
  } catch {
    return repositoryCatalog;
  }
}

async function loadPolicyRollouts() {
  await loadConsoleConfig();
  try {
    const params = {
      policy_pack: document.querySelector("#filterRepositoryPolicy")?.value.trim(),
      state: document.querySelector("#filterRolloutState")?.value,
      mode: document.querySelector("#filterRolloutMode")?.value
    };
    const response = await fetch(apiUrl("/policy-rollouts", params));
    if (!response.ok) throw new Error("Policy rollout API unavailable");
    const payload = await response.json();
    return Array.isArray(payload) ? payload : payload.items || [];
  } catch {
    return rolloutCatalog;
  }
}

async function loadApprovals() {
  await loadConsoleConfig();
  try {
    const params = {
      state: document.querySelector("#filterApprovalState")?.value,
      approver_group: document.querySelector("#filterApprovalGroup")?.value.trim(),
      limit: 25
    };
    const response = await fetch(apiUrl("/approvals", params));
    if (!response.ok) throw new Error("Approval API unavailable");
    const payload = await response.json();
    return Array.isArray(payload) ? payload : payload.items || [];
  } catch {
    return approvalCatalog;
  }
}

async function loadAgents() {
  await loadConsoleConfig();
  try {
    const params = {
      status: document.querySelector("#filterAgentStatus")?.value,
      owner: document.querySelector("#filterAgentOwner")?.value.trim()
    };
    const response = await fetch(apiUrl("/agents", params));
    if (!response.ok) throw new Error("Agent registry API unavailable");
    const payload = await response.json();
    return Array.isArray(payload) ? payload : payload.items || [];
  } catch {
    return agentCatalog;
  }
}

async function loadMcpServers() {
  await loadConsoleConfig();
  try {
    const params = {
      trust_tier: document.querySelector("#filterMcpTrust")?.value,
      capability: document.querySelector("#filterMcpCapability")?.value
    };
    const response = await fetch(apiUrl("/mcp/servers", params));
    if (!response.ok) throw new Error("MCP registry API unavailable");
    const payload = await response.json();
    return Array.isArray(payload) ? payload : payload.items || [];
  } catch {
    return mcpCatalog;
  }
}

async function loadAgentProfiles() {
  await loadConsoleConfig();
  try {
    const response = await fetch(apiUrl("/agents/profiles"));
    if (!response.ok) throw new Error("Agent profile API unavailable");
    const payload = await response.json();
    return Array.isArray(payload) ? payload : payload.items || [];
  } catch {
    return agentProfiles;
  }
}

async function loadMcpClassifications() {
  await loadConsoleConfig();
  try {
    const response = await fetch(apiUrl("/mcp/tool-classifications"));
    if (!response.ok) throw new Error("MCP classification API unavailable");
    const payload = await response.json();
    return Array.isArray(payload) ? payload : payload.items || [];
  } catch {
    return mcpClassifications;
  }
}

function filterEvidence(items) {
  const signer = document.querySelector("#filterSigner").value.trim().toLowerCase();
  const minBlocked = Number(document.querySelector("#filterBlocked").value || 0);
  const approvalValue = document.querySelector("#filterApprovals").value;
  const limit = Number(document.querySelector("#filterLimit").value || 10);
  return items
    .filter((item) => !signer || String(item.signer || "").toLowerCase().includes(signer))
    .filter((item) => Number(item.blocked_count || 0) >= minBlocked)
    .filter((item) => approvalValue === "" || (Number(item.approval_required_count || 0) > 0) === (approvalValue === "true"))
    .slice(0, limit);
}

function filterSessions(items) {
  const repository = document.querySelector("#filterActivityRepository").value.trim().toLowerCase();
  const agent = document.querySelector("#filterActivityAgent").value.trim().toLowerCase();
  const policy = document.querySelector("#filterActivityPolicy").value.trim().toLowerCase();
  return items
    .filter((item) => !repository || String(item.repository || "").toLowerCase().includes(repository))
    .filter((item) => !agent || String(item.agent_id || "").toLowerCase().includes(agent))
    .filter((item) => !policy || String(item.policy_pack || "").toLowerCase().includes(policy));
}

function filterDecisions(items) {
  const repository = document.querySelector("#filterActivityRepository").value.trim().toLowerCase();
  const agent = document.querySelector("#filterActivityAgent").value.trim().toLowerCase();
  const policy = document.querySelector("#filterActivityPolicy").value.trim().toLowerCase();
  const decision = document.querySelector("#filterDecisionState").value;
  const severity = document.querySelector("#filterDecisionSeverity").value;
  return items
    .filter((item) => !repository || String(item.repository || "").toLowerCase().includes(repository))
    .filter((item) => !agent || String(item.agent_id || "").toLowerCase().includes(agent))
    .filter((item) => !policy || String(item.policy_pack || "").toLowerCase().includes(policy))
    .filter((item) => !decision || item.decision === decision)
    .filter((item) => !severity || item.severity === severity);
}

function filterRepositories(items) {
  const owner = document.querySelector("#filterRepositoryOwner").value.trim().toLowerCase();
  const policy = document.querySelector("#filterRepositoryPolicy").value.trim().toLowerCase();
  const risk = document.querySelector("#filterRepositoryRisk").value;
  return items
    .filter((item) => !owner || String(item.owner || "").toLowerCase().includes(owner))
    .filter((item) => !policy || String(item.policy_pack || "").toLowerCase().includes(policy))
    .filter((item) => !risk || item.risk_tier === risk);
}

function filterPolicyRollouts(items) {
  const policy = document.querySelector("#filterRepositoryPolicy").value.trim().toLowerCase();
  const state = document.querySelector("#filterRolloutState").value;
  const mode = document.querySelector("#filterRolloutMode").value;
  return items
    .filter((item) => !policy || String(item.policy_pack || "").toLowerCase().includes(policy))
    .filter((item) => !state || item.state === state)
    .filter((item) => !mode || item.mode === mode);
}

function filterApprovals(items) {
  const state = document.querySelector("#filterApprovalState").value;
  const group = document.querySelector("#filterApprovalGroup").value.trim().toLowerCase();
  return items
    .filter((item) => !state || item.state === state)
    .filter((item) => !group || String(item.approver_group || "").toLowerCase().includes(group));
}

function filterAgents(items) {
  const status = document.querySelector("#filterAgentStatus").value;
  const owner = document.querySelector("#filterAgentOwner").value.trim().toLowerCase();
  return items
    .filter((item) => !status || item.status === status)
    .filter((item) => !owner || String(item.owner || "").toLowerCase().includes(owner));
}

function filterMcpServers(items) {
  const trust = document.querySelector("#filterMcpTrust").value;
  const capability = document.querySelector("#filterMcpCapability").value;
  return items
    .filter((item) => !trust || item.trust_tier === trust)
    .filter((item) => !capability || (item.capabilities || []).includes(capability));
}

function renderEvidenceRows(items) {
  const rows = document.querySelector("#evidenceRows");
  const sessionSelect = document.querySelector("#attestationSession");
  rows.innerHTML = "";
  sessionSelect.innerHTML = "";
  for (const item of items) {
    rows.insertAdjacentHTML("beforeend", `
      <tr>
        <td>${escapeHtml(item.session_id || "unknown")}</td>
        <td>${escapeHtml(item.signer || "local")}</td>
        <td>${item.decision_count || 0}</td>
        <td class="${Number(item.blocked_count || 0) > 0 ? "block" : "allow"}">${item.blocked_count || 0}</td>
        <td class="${Number(item.approval_required_count || 0) > 0 ? "require_approval" : "allow"}">${item.approval_required_count || 0}</td>
        <td>${item.retention?.retention_days || "n/a"} days</td>
      </tr>
    `);
    sessionSelect.insertAdjacentHTML("beforeend", `<option value="${escapeHtml(item.session_id)}">${escapeHtml(item.session_id)}</option>`);
  }
}

function renderActivityRows(sessions, decisions) {
  const sessionRows = document.querySelector("#sessionRows");
  const decisionRows = document.querySelector("#decisionRows");
  sessionRows.innerHTML = "";
  decisionRows.innerHTML = "";
  for (const item of sessions) {
    sessionRows.insertAdjacentHTML("beforeend", `
      <tr>
        <td>${escapeHtml(item.session_id || "unknown")}</td>
        <td>${escapeHtml(item.repository || "local")}</td>
        <td>${escapeHtml(item.agent_id || "unknown-agent")}</td>
        <td>${item.decision_count || 0}</td>
        <td class="${Number(item.blocked_count || 0) > 0 ? "block" : "allow"}">${item.blocked_count || 0}</td>
        <td class="${Number(item.approval_required_count || 0) > 0 ? "require_approval" : "allow"}">${item.approval_required_count || 0}</td>
        <td>${escapeHtml(String(item.updated_at || "").slice(0, 19))}</td>
      </tr>
    `);
  }
  for (const item of decisions) {
    decisionRows.insertAdjacentHTML("beforeend", `
      <tr>
        <td>${escapeHtml(item.decision_id || "unknown")}</td>
        <td class="${riskClass(item.decision)}">${escapeHtml(item.decision || "audit_only")}</td>
        <td>${escapeHtml(item.action_type || "unknown")}</td>
        <td>${escapeHtml(item.target || "n/a")}</td>
        <td>${escapeHtml(item.rule_id || "runtime.default")}</td>
        <td class="${riskClass(item.severity)}">${escapeHtml(item.severity || "low")}</td>
      </tr>
    `);
  }
}

function renderInventoryRows(repositories, rollouts) {
  const repositoryRows = document.querySelector("#repositoryRows");
  const rolloutRows = document.querySelector("#rolloutRows");
  repositoryRows.innerHTML = "";
  rolloutRows.innerHTML = "";
  for (const item of repositories) {
    const checks = Array.isArray(item.required_checks) && item.required_checks.length ? item.required_checks.join(", ") : "not configured";
    repositoryRows.insertAdjacentHTML("beforeend", `
      <tr>
        <td>${escapeHtml(item.repository || item.repository_id || "unknown")}</td>
        <td>${escapeHtml(item.owner || "unassigned")}</td>
        <td>${escapeHtml(item.policy_pack || "cavra-ai-agent-baseline")}</td>
        <td class="${riskClass(item.risk_tier)}">${escapeHtml(item.risk_tier || "medium")}</td>
        <td class="${riskClass(item.status)}">${escapeHtml(item.status || "active")}</td>
        <td>${escapeHtml(checks)}</td>
      </tr>
    `);
  }
  for (const item of rollouts) {
    rolloutRows.insertAdjacentHTML("beforeend", `
      <tr>
        <td>${escapeHtml(item.repository || "unknown")}</td>
        <td>${escapeHtml(item.policy_pack || "n/a")}</td>
        <td class="${riskClass(item.mode)}">${escapeHtml(item.mode || "enforce")}</td>
        <td class="${riskClass(item.state)}">${escapeHtml(item.state || "planned")}</td>
        <td>${Number(item.coverage_percent || 0)}%</td>
        <td>${escapeHtml(item.owner || "platform-security")}</td>
      </tr>
    `);
  }
}

function riskClass(value) {
  if (value === "critical" || value === "high" || value === "blocked" || value === "denied" || value === "strict") return "block";
  if (value === "medium" || value === "experimental" || value === "pending" || value === "planned" || value === "audit_only") return "require_approval";
  return "allow";
}

function renderRegistryRows(agents, mcpServers, profiles, classifications) {
  const agentRows = document.querySelector("#agentRows");
  const mcpRows = document.querySelector("#mcpRows");
  const profileRows = document.querySelector("#agentProfileRows");
  const classificationRows = document.querySelector("#mcpClassificationRows");
  agentRows.innerHTML = "";
  mcpRows.innerHTML = "";
  profileRows.innerHTML = "";
  classificationRows.innerHTML = "";
  for (const item of agents) {
    const capabilities = Array.isArray(item.capabilities) ? item.capabilities.join(", ") : "";
    agentRows.insertAdjacentHTML("beforeend", `
      <tr>
        <td>${escapeHtml(item.agent_id || "unknown")}</td>
        <td>${escapeHtml(item.vendor || "unknown")}</td>
        <td>${escapeHtml(item.owner || "unassigned")}</td>
        <td class="${riskClass(item.status)}">${escapeHtml(item.status || "active")}</td>
        <td>${escapeHtml(capabilities || "n/a")}</td>
        <td class="${riskClass(item.risk_tier)}">${escapeHtml(item.risk_tier || "medium")}</td>
      </tr>
    `);
  }
  for (const item of mcpServers) {
    const capabilities = Array.isArray(item.capabilities) ? item.capabilities.join(", ") : "";
    const tools = Array.isArray(item.allowed_tools) && item.allowed_tools.length ? item.allowed_tools.join(", ") : "approval required";
    mcpRows.insertAdjacentHTML("beforeend", `
      <tr>
        <td>${escapeHtml(item.name || item.server_id || "unknown")}</td>
        <td class="${riskClass(item.trust_tier)}">${escapeHtml(item.trust_tier || "unknown")}</td>
        <td class="${riskClass(item.approval_state)}">${escapeHtml(item.approval_state || "pending")}</td>
        <td>${escapeHtml(capabilities || "n/a")}</td>
        <td>${escapeHtml(tools)}</td>
      </tr>
    `);
  }
  for (const item of profiles.slice(0, 6)) {
    const capabilities = item.default_capabilities || [];
    profileRows.insertAdjacentHTML("beforeend", `
      <article class="profile-item">
        <strong>${escapeHtml(item.display_name || item.profile_id)}</strong>
        <span>${escapeHtml(item.vendor || "unknown")} · <span class="${riskClass(item.risk_tier)}">${escapeHtml(item.risk_tier || "medium")}</span></span>
        <small>${escapeHtml(capabilities.slice(0, 4).join(", "))}</small>
      </article>
    `);
  }
  for (const item of classifications) {
    classificationRows.insertAdjacentHTML("beforeend", `
      <article class="profile-item">
        <strong>${escapeHtml(item.capability)}</strong>
        <span>${escapeHtml(item.category || "tool")} · <span class="${riskClass(item.risk_tier)}">${escapeHtml(item.risk_tier)}</span></span>
        <small>${escapeHtml(item.control_objective || "")}</small>
      </article>
    `);
  }
}

function renderApprovalRows(items) {
  const rows = document.querySelector("#approvalRows");
  rows.innerHTML = "";
  for (const item of items) {
    const stateClass = item.state === "break_glass" ? "warn" : item.state === "denied" ? "block" : "allow";
    const detailAction = `<button class="approvalDetailAction secondary" data-id="${escapeHtml(item.approval_id)}">Details</button>`;
    const actions = item.state === "pending"
      ? `<button class="approvalAction" data-action="approve" data-id="${escapeHtml(item.approval_id)}">Approve</button>
         <button class="approvalAction secondary" data-action="deny" data-id="${escapeHtml(item.approval_id)}">Deny</button>
         <button class="approvalAction secondary" data-action="expire" data-id="${escapeHtml(item.approval_id)}">Expire</button>
         ${detailAction}`
      : detailAction;
    rows.insertAdjacentHTML("beforeend", `
      <tr>
        <td>${escapeHtml(item.approval_id || "unknown")}</td>
        <td class="${stateClass}">${escapeHtml(item.state || "pending")}</td>
        <td>${escapeHtml(item.approver_group || "Repository Owners")}</td>
        <td>${escapeHtml(item.requested_by || "ai-agent")}</td>
        <td>${escapeHtml(item.decision?.target || item.decision_id || "unknown")}</td>
        <td>${escapeHtml(item.external_ref || "n/a")}</td>
        <td class="row-actions">${actions}</td>
      </tr>
    `);
  }
}

function renderApprovalDetail(item) {
  const panel = document.querySelector("#approvalDetail");
  if (!item) {
    panel.textContent = "Approval record not found.";
    return;
  }
  const history = Array.isArray(item.history) ? item.history : [];
  const evidenceRefs = Array.isArray(item.evidence_refs) ? item.evidence_refs : [];
  panel.innerHTML = `
    <dl>
      <dt>Approval</dt><dd>${escapeHtml(item.approval_id || "unknown")}</dd>
      <dt>State</dt><dd>${escapeHtml(item.state || "pending")}</dd>
      <dt>Approver group</dt><dd>${escapeHtml(item.approver_group || "Repository Owners")}</dd>
      <dt>Requested by</dt><dd>${escapeHtml(item.requested_by || "ai-agent")}</dd>
      <dt>Decided by</dt><dd>${escapeHtml(item.decided_by || "n/a")}</dd>
      <dt>External ref</dt><dd>${escapeHtml(item.external_ref || "n/a")}</dd>
      <dt>Decision target</dt><dd>${escapeHtml(item.decision?.target || item.decision_id || "unknown")}</dd>
      <dt>Rule</dt><dd>${escapeHtml(item.decision?.rule_id || "n/a")}</dd>
      <dt>Reason</dt><dd>${escapeHtml(item.decision_reason || item.break_glass_reason || item.decision?.reason || "n/a")}</dd>
    </dl>
    <h3>Evidence</h3>
    <ul>${evidenceRefs.length ? evidenceRefs.map((ref) => `<li>${escapeHtml(ref)}</li>`).join("") : "<li>n/a</li>"}</ul>
    <h3>History</h3>
    <ul>${history.length ? history.map((event) => `<li><strong>${escapeHtml(event.event || "event")}</strong> ${escapeHtml(event.actor || "unknown")}<br><small>${escapeHtml(event.timestamp || "")}</small><br>${escapeHtml(event.reason || "")}</li>`).join("") : "<li>n/a</li>"}</ul>
  `;
}

async function refreshEvidence() {
  const items = filterEvidence(await loadEvidenceMetadata());
  renderEvidenceRows(items);
}

async function refreshActivity() {
  const [sessions, decisions] = await Promise.all([loadSessions(), loadDecisions()]);
  renderActivityRows(filterSessions(sessions), filterDecisions(decisions));
}

async function refreshInventory() {
  const [repositories, rollouts] = await Promise.all([loadRepositories(), loadPolicyRollouts()]);
  renderInventoryRows(filterRepositories(repositories), filterPolicyRollouts(rollouts));
}

async function refreshApprovals() {
  const items = filterApprovals(await loadApprovals());
  renderApprovalRows(items);
}

async function refreshRegistry() {
  const [agents, mcpServers, profiles, classifications] = await Promise.all([
    loadAgents(),
    loadMcpServers(),
    loadAgentProfiles(),
    loadMcpClassifications()
  ]);
  renderRegistryRows(filterAgents(agents), filterMcpServers(mcpServers), profiles, classifications);
}

async function submitApprovalAction(approvalId, action) {
  const reason = action === "expire" ? "approval expired from console" : window.prompt(`${action} reason`);
  if (!reason) return;
  try {
    const response = await fetch(apiUrl(`/approvals/${approvalId}/${action}`), {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ actor: "console-user", reason })
    });
    if (!response.ok) throw new Error("Approval API unavailable");
  } catch {
    const item = approvalCatalog.find((approval) => approval.approval_id === approvalId);
    if (item) {
      item.state = action === "approve" ? "approved" : action === "deny" ? "denied" : "expired";
      item.decided_by = "console-user";
      item.decision_reason = reason;
      item.history = [
        ...(Array.isArray(item.history) ? item.history : []),
        { event: item.state, actor: "console-user", timestamp: new Date().toISOString(), reason }
      ];
    }
  }
  await refreshApprovals();
}

async function showApprovalDetail(approvalId) {
  await loadConsoleConfig();
  try {
    const response = await fetch(apiUrl(`/approvals/${approvalId}`));
    if (!response.ok) throw new Error("Approval API unavailable");
    renderApprovalDetail(await response.json());
  } catch {
    renderApprovalDetail(approvalCatalog.find((approval) => approval.approval_id === approvalId));
  }
}

async function createBreakGlassApproval() {
  const target = document.querySelector("#breakGlassTarget").value.trim();
  const rule = document.querySelector("#breakGlassRule").value.trim();
  const actor = document.querySelector("#breakGlassActor").value.trim();
  const group = document.querySelector("#breakGlassGroup").value.trim();
  const externalRef = document.querySelector("#breakGlassRef").value.trim();
  const reason = document.querySelector("#breakGlassReason").value.trim();
  const ttlHours = Number(document.querySelector("#breakGlassTtl").value || 4);
  const status = document.querySelector("#breakGlassStatus");
  if (!target || !actor || !group || !reason) {
    status.textContent = "Target, actor, group, and reason are required.";
    status.className = "status-line warn";
    return;
  }
  const payload = {
    decision: {
      decision_id: `dec_console_${Date.now()}`,
      session_id: "console-break-glass",
      action_type: "execute_command",
      target,
      rule_id: rule || "commands.block",
      decision: "block",
      severity: "critical",
      reason: "Emergency override requested from console.",
      evidence_refs: [`console://break-glass/${Date.now()}`]
    },
    actor,
    reason,
    approver_group: group,
    external_ref: externalRef || undefined,
    ttl_hours: ttlHours
  };
  try {
    const response = await fetch(apiUrl("/approvals/break-glass"), {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(payload)
    });
    if (!response.ok) throw new Error("Approval API unavailable");
    const created = await response.json();
    status.textContent = `Break-glass approval created: ${created.approval_id}`;
    status.className = "status-line ok";
    renderApprovalDetail(created);
  } catch {
    const created = {
      schema_version: "cavra.approval.v1",
      product: "CAVRA",
      approval_id: `apr_console_${Date.now()}`,
      decision_id: payload.decision.decision_id,
      session_id: payload.decision.session_id,
      state: "break_glass",
      approver_group: group,
      requested_by: actor,
      requested_at: new Date().toISOString(),
      expires_at: new Date(Date.now() + ttlHours * 60 * 60 * 1000).toISOString(),
      external_ref: externalRef || undefined,
      break_glass: true,
      break_glass_reason: reason,
      decision: payload.decision,
      evidence_refs: [`approval://console/${Date.now()}`, ...payload.decision.evidence_refs],
      history: [{ event: "break_glass", actor, timestamp: new Date().toISOString(), reason }]
    };
    approvalCatalog.unshift(created);
    status.textContent = `Break-glass approval created locally: ${created.approval_id}`;
    status.className = "status-line ok";
    renderApprovalDetail(created);
  }
  await refreshApprovals();
}

async function verifyAttestation() {
  const selected = document.querySelector("#attestationSession").value;
  const result = document.querySelector("#attestationResult");
  const items = await loadEvidenceMetadata();
  const item = items.find((entry) => entry.session_id === selected) || evidenceCatalog.find((entry) => entry.session_id === selected);
  const decisions = item?.decisions || evidenceCatalog[0].decisions;
  const targets = item?.attestation_targets || decisions.map((decision) => decision.target);
  const missing = targets.filter((target) => !JSON.stringify(decisions).includes(target));
  result.innerHTML = "";
  result.insertAdjacentHTML("beforeend", `<li class="${missing.length ? "warn" : "ok"}">${missing.length ? "Verification needs review" : "Attestation coverage verified"}</li>`);
  result.insertAdjacentHTML("beforeend", `<li>Session: ${selected}</li>`);
  result.insertAdjacentHTML("beforeend", `<li>Decision targets checked: ${targets.length}</li>`);
  result.insertAdjacentHTML("beforeend", `<li>Missing targets: ${missing.length}</li>`);
}

document.querySelector("#runScenario").addEventListener("click", runScenario);
document.querySelector("#refreshEvidence").addEventListener("click", refreshEvidence);
document.querySelector("#refreshActivity").addEventListener("click", refreshActivity);
document.querySelector("#refreshInventory").addEventListener("click", refreshInventory);
document.querySelector("#refreshApprovals").addEventListener("click", refreshApprovals);
document.querySelector("#refreshRegistry").addEventListener("click", refreshRegistry);
document.querySelector("#createBreakGlass").addEventListener("click", createBreakGlassApproval);
document.querySelector("#approvalRows").addEventListener("click", async (event) => {
  if (!(event.target instanceof Element)) return;
  const detailButton = event.target.closest(".approvalDetailAction");
  if (detailButton) {
    await showApprovalDetail(detailButton.dataset.id);
    return;
  }
  const actionButton = event.target.closest(".approvalAction");
  if (!actionButton) return;
  await submitApprovalAction(actionButton.dataset.id, actionButton.dataset.action);
});
document.querySelector("#verifyAttestation").addEventListener("click", verifyAttestation);
document.querySelector("#copyInstall").addEventListener("click", async () => {
  await navigator.clipboard.writeText("claude mcp add cavra -- cavra-mcp-server");
});
refreshEvidence();
refreshActivity();
refreshInventory();
refreshApprovals();
refreshRegistry();
