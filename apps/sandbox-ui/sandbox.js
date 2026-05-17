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
    attestation_targets: scenario.map((row) => row[1]),
    artifact_count: 7
  },
  {
    session_id: "docs-agent-run",
    signer: "docs-agent",
    decision_count: 4,
    blocked_count: 0,
    approval_required_count: 0,
    retention: { retention_days: 365, retain_until: "2027-05-17T00:00:00Z" },
    decisions: scenario.slice(2, 6).map(eventPayload),
    attestation_targets: scenario.slice(2, 6).map((row) => row[1]),
    artifact_count: 7
  },
  {
    session_id: "security-review",
    signer: "security-agent",
    decision_count: 5,
    blocked_count: 2,
    approval_required_count: 1,
    retention: { retention_days: 2555, retain_until: "2033-05-15T00:00:00Z" },
    decisions: scenario.slice(0, 5).map(eventPayload),
    attestation_targets: scenario.slice(0, 5).map((row) => row[1]),
    artifact_count: 7
  }
];

const evidenceArtifactCatalog = [
  ["manifest.json", "manifest", "application/json", "Manifest with checksums and signature metadata."],
  ["evidence.json", "evidence", "application/json", "Complete decision evidence for the session."],
  ["pr-attestation.md", "attestation", "text/markdown", "Reviewer-ready PR attestation."],
  ["compliance-mapping.md", "compliance", "text/markdown", "Audit control-objective mapping."],
  ["siem-event.json", "siem", "application/json", "SIEM-ready session event payload."],
  ["sandbox-run-summary.json", "summary", "application/json", "Compact session summary."],
  ["retention-policy.json", "retention", "application/json", "Retention, legal hold, and disposition policy."]
].map(([artifact, kind, media_type, description]) => ({
  artifact, kind, media_type, description, bytes: 1024, sha256: "sample"
}));

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
    coverage_percent: 95,
    evidence_refs: ["evidence://demo-session", "attestation://payments/api"]
  },
  {
    rollout_id: "platform-security-baseline",
    repository: "platform/security",
    policy_pack: "cavra-ai-agent-baseline",
    policy_version: "latest",
    mode: "enforce",
    state: "active",
    owner: "Platform Security",
    coverage_percent: 88,
    evidence_refs: ["evidence://security-review"]
  },
  {
    rollout_id: "docs-site-baseline",
    repository: "docs/site",
    policy_pack: "cavra-ai-agent-baseline",
    policy_version: "latest",
    mode: "audit_only",
    state: "planned",
    owner: "Documentation",
    coverage_percent: 20,
    evidence_refs: []
  }
];

const policyCatalog = [
  {
    id: "cavra-ai-agent-baseline",
    title: "AI Agent Baseline",
    description: "Default CAVRA controls for AI coding agents.",
    version: "latest",
    summary: { rule_counts: { filesystem: 8, commands: 6, git: 4, mcp: 5, approvals: 2, evidence: 3, compliance: 1 } }
  },
  {
    id: "cavra-banking",
    title: "Banking Baseline",
    description: "Regulated banking SDLC policy overlay.",
    version: "2026.05",
    summary: { rule_counts: { filesystem: 12, commands: 8, git: 5, mcp: 6, approvals: 4, evidence: 5, compliance: 6 } }
  }
];

const integrationCatalog = [
  {
    integration_id: "github-enterprise",
    provider: "github",
    name: "GitHub Enterprise",
    category: "source_control",
    status: "active",
    health_status: "healthy",
    owner: "Developer Platform",
    environment: "production",
    auth_mode: "github_app",
    capabilities: ["required_check", "pull_request", "branch_protection"]
  },
  {
    integration_id: "splunk-soc",
    provider: "splunk",
    name: "Splunk SOC",
    category: "siem",
    status: "configured",
    health_status: "not_checked",
    owner: "SOC",
    environment: "production",
    auth_mode: "hec_token",
    capabilities: ["decision_events", "blocked_action_alerts"]
  },
  {
    integration_id: "jira-change",
    provider: "jira",
    name: "Jira Change",
    category: "itsm",
    status: "planned",
    health_status: "unknown",
    owner: "Change Management",
    environment: "production",
    auth_mode: "oauth",
    capabilities: ["approval_ticket", "change_reference"]
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
let consoleAuthToken = window.sessionStorage?.getItem("cavraConsoleToken") || "";

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

function apiHeaders(json = false) {
  const headers = {};
  if (json) headers["content-type"] = "application/json";
  if (consoleAuthToken) headers.authorization = `Bearer ${consoleAuthToken}`;
  return headers;
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

async function loadEvidenceArtifacts(sessionId) {
  await loadConsoleConfig();
  try {
    const response = await fetch(apiUrl(`/evidence/${encodeURIComponent(sessionId)}/artifacts`));
    if (!response.ok) throw new Error("Evidence artifact API unavailable");
    return await response.json();
  } catch {
    return {
      schema_version: "cavra.evidence.artifacts.v1",
      product: "CAVRA",
      session_id: sessionId,
      artifact_root_configured: false,
      artifact_count: evidenceArtifactCatalog.length,
      artifacts: evidenceArtifactCatalog.map((item) => ({ ...item, download_url: "" })),
      bundle_download_url: ""
    };
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

async function loadPolicyRolloutDetail(rolloutId) {
  await loadConsoleConfig();
  try {
    const response = await fetch(apiUrl(`/policy-rollout-details/${encodeURIComponent(rolloutId)}`));
    if (!response.ok) throw new Error("Policy rollout detail API unavailable");
    return await response.json();
  } catch {
    const rollout = rolloutCatalog.find((item) => item.rollout_id === rolloutId);
    if (!rollout) return null;
    const repository = repositoryCatalog.find((item) => item.repository === rollout.repository);
    const decisions = activityDecisions.filter((item) => item.repository === rollout.repository && item.policy_pack === rollout.policy_pack);
    return {
      schema_version: "cavra.policy_rollout.detail.v1",
      product: "CAVRA",
      rollout,
      repository,
      policy_pack: {
        id: rollout.policy_pack,
        title: rollout.policy_pack,
        version: rollout.policy_version,
        rule_summary: { filesystem: 8, commands: 6, git: 2, mcp: 3, approvals: 2, evidence: 3 }
      },
      activity_summary: {
        total: decisions.length,
        outcomes: decisions.reduce((acc, item) => ({ ...acc, [item.decision]: (acc[item.decision] || 0) + 1 }), {}),
        severities: decisions.reduce((acc, item) => ({ ...acc, [item.severity]: (acc[item.severity] || 0) + 1 }), {}),
        recent_decisions: decisions.slice(0, 5)
      },
      integration_summary: {
        total: integrationCatalog.length,
        by_category: integrationCatalog.reduce((acc, item) => ({ ...acc, [item.category]: (acc[item.category] || 0) + 1 }), {}),
        by_health: integrationCatalog.reduce((acc, item) => ({ ...acc, [item.health_status]: (acc[item.health_status] || 0) + 1 }), {})
      },
      readiness: {
        status: Number(rollout.coverage_percent || 0) >= 80 ? "ready" : "needs_attention",
        checks: [
          { id: "repository_registered", status: repository ? "pass" : "warn", message: repository ? "Repository inventory record is present." : "Repository inventory record is missing." },
          { id: "policy_coverage", status: Number(rollout.coverage_percent || 0) >= 80 ? "pass" : "warn", message: `Coverage is ${Number(rollout.coverage_percent || 0)}%.` }
        ]
      }
    };
  }
}

async function loadPolicyCatalog() {
  await loadConsoleConfig();
  try {
    const response = await fetch(apiUrl("/policy-pack-catalog"));
    if (!response.ok) throw new Error("Policy catalog API unavailable");
    const payload = await response.json();
    return Array.isArray(payload) ? payload : payload.items || [];
  } catch {
    return policyCatalog;
  }
}

function draftPolicyPayload() {
  return {
    id: document.querySelector("#draftPolicyId").value.trim(),
    title: document.querySelector("#draftPolicyTitle").value.trim(),
    description: "Platform-authored policy draft from the CAVRA console.",
    version: document.querySelector("#draftPolicyVersion").value.trim(),
    inherits: document.querySelector("#draftPolicyInherits").value.trim(),
    commands: { block: ["terraform apply -auto-approve", "kubectl delete namespace"] },
    filesystem: { block_read: [".env", "secrets/"], require_approval_write: ["iam/"] },
    git: { require_ai_attestation: true, require_pull_request: true }
  };
}

function rolloutChangePayload() {
  return {
    rollout_id: document.querySelector("#changeRolloutId").value.trim(),
    repository: document.querySelector("#changeRepository").value.trim(),
    policy_pack: document.querySelector("#changePolicyPack").value.trim(),
    mode: document.querySelector("#changeMode").value,
    state: document.querySelector("#changeState").value,
    coverage_percent: Number(document.querySelector("#changeCoverage").value || 0)
  };
}

async function previewPolicyDraft() {
  await loadConsoleConfig();
  try {
    const response = await fetch(apiUrl("/policy-packs/draft"), {
      method: "POST",
      headers: apiHeaders(true),
      body: JSON.stringify(draftPolicyPayload())
    });
    if (!response.ok) throw new Error("Policy draft API unavailable");
    renderPolicyDraft(await response.json());
  } catch {
    const payload = draftPolicyPayload();
    renderPolicyDraft({
      schema_version: "cavra.policy_pack.draft.v1",
      product: "CAVRA",
      valid: payload.id.startsWith("cavra-"),
      errors: payload.id.startsWith("cavra-") ? [] : ["metadata.id must start with cavra-"],
      policy_pack: { metadata: { id: payload.id, title: payload.title, version: payload.version, inherits: payload.inherits } },
      summary: { policy_id: payload.id, title: payload.title, version: payload.version, inherits: payload.inherits, rule_counts: { filesystem: 3, commands: 2, git: 2 } },
      operator_notes: ["Sample draft preview; connect the API for schema validation."]
    });
  }
}

async function planRolloutChange() {
  await loadConsoleConfig();
  const payload = rolloutChangePayload();
  try {
    const response = await fetch(apiUrl("/policy-rollouts/change-plan"), {
      method: "POST",
      headers: apiHeaders(true),
      body: JSON.stringify(payload)
    });
    if (!response.ok) throw new Error("Rollout plan API unavailable");
    renderRolloutChangePlan(await response.json(), false);
  } catch {
    const before = rolloutCatalog.find((item) => item.rollout_id === payload.rollout_id);
    renderRolloutChangePlan({
      schema_version: "cavra.policy_rollout.change_plan.v1",
      product: "CAVRA",
      operation: before ? "update" : "create",
      risk: payload.mode === "strict" ? "high" : "medium",
      approval_required: payload.mode === "strict" || payload.mode === "break_glass",
      before,
      after: { ...(before || {}), ...payload },
      changes: Object.entries(payload).map(([field, value]) => ({ field, before: before?.[field], after: value })),
      operator_notes: ["Sample rollout plan; connect the API to persist changes."]
    }, false);
  }
}

async function applyRolloutChange() {
  await loadConsoleConfig();
  const payload = rolloutChangePayload();
  try {
    const response = await fetch(apiUrl("/policy-rollouts/apply-change"), {
      method: "POST",
      headers: apiHeaders(true),
      body: JSON.stringify(payload)
    });
    if (!response.ok) throw new Error("Rollout apply API unavailable");
    const result = await response.json();
    renderRolloutChangePlan(result.plan, true);
    await refreshInventory();
  } catch {
    const index = rolloutCatalog.findIndex((item) => item.rollout_id === payload.rollout_id);
    if (index >= 0) rolloutCatalog[index] = { ...rolloutCatalog[index], ...payload };
    else rolloutCatalog.push({ owner: "platform-security", policy_version: "latest", evidence_refs: [], ...payload });
    renderRolloutChangePlan({
      schema_version: "cavra.policy_rollout.change_plan.v1",
      product: "CAVRA",
      operation: index >= 0 ? "update" : "create",
      risk: payload.mode === "strict" ? "high" : "medium",
      approval_required: payload.mode === "strict",
      before: null,
      after: payload,
      changes: Object.entries(payload).map(([field, value]) => ({ field, before: null, after: value })),
      operator_notes: ["Applied locally because the API was unavailable."]
    }, true);
    await refreshInventory();
  }
}

async function loadDeploymentReadiness() {
  await loadConsoleConfig();
  try {
    const response = await fetch(apiUrl("/deployment/production-readiness"));
    if (!response.ok) throw new Error("Deployment readiness API unavailable");
    return await response.json();
  } catch {
    return {
      schema_version: "cavra.deployment.production_readiness.v1",
      product: "CAVRA",
      status: "needs_attention",
      checks: [
        { id: "oidc_configured", status: consoleConfig?.approval_oidc === "configured" ? "pass" : "warn", message: "Console and approval actions validate signed OIDC tokens." },
        { id: "rbac_configured", status: consoleConfig?.approval_rbac === "configured" ? "pass" : "warn", message: "Repository-scoped RBAC policy is configured." },
        { id: "cors_restricted", status: (consoleConfig?.cors_origins || []).length ? "pass" : "warn", message: "Allowed console origins are explicit." }
      ],
      operator_notes: ["Connect to the API for full persistent-store and evidence-artifact readiness checks."]
    };
  }
}

async function loadSecurityBoundary() {
  await loadConsoleConfig();
  try {
    const response = await fetch(apiUrl("/console/security-boundary"));
    if (!response.ok) throw new Error("Security boundary API unavailable");
    return await response.json();
  } catch {
    return {
      schema_version: "cavra.console.security_boundary.v1",
      product: "CAVRA",
      mode: "local_or_demo",
      oidc: { configured: false, config_env: "CAVRA_APPROVAL_OIDC_CONFIG", supported_algorithms: ["RS256"], validated_claims: ["iss", "aud", "exp", "nbf", "groups", "roles"] },
      rbac: { configured: false, config_env: "CAVRA_APPROVAL_RBAC_FILE", boundaries: ["approval_group", "repository_permissions", "group_mappings"] },
      cors: { configured: Array.isArray(consoleConfig?.cors_origins) && consoleConfig.cors_origins.length > 0, origins: consoleConfig?.cors_origins || [] },
      console_permissions: ["read_activity", "read_inventory", "read_integrations", "read_evidence_metadata", "approval_decision_requires_actor_claims_or_token_when_configured"],
      operator_notes: ["Host the console behind enterprise identity before production use."]
    };
  }
}

async function loadConsoleSession() {
  await loadConsoleConfig();
  try {
    const response = await fetch(apiUrl("/console/session"), { headers: apiHeaders() });
    if (!response.ok) throw new Error("Console session API unavailable");
    return await response.json();
  } catch {
    return {
      schema_version: "cavra.console.session.v1",
      product: "CAVRA",
      mode: consoleAuthToken ? "token_not_verified" : "local_or_demo",
      authenticated: false,
      auth_required: consoleConfig?.approval_oidc === "configured",
      actor: null,
      repository_permissions: [],
      permissions: {
        read_activity: true,
        read_inventory: true,
        read_integrations: true,
        read_evidence_metadata: true,
        decide_approvals: false,
        create_break_glass: false
      },
      operator_notes: ["Connect to the API to validate signed console tokens."]
    };
  }
}

async function loadIntegrations() {
  await loadConsoleConfig();
  try {
    const params = {
      category: document.querySelector("#filterIntegrationCategory")?.value,
      status: document.querySelector("#filterIntegrationStatus")?.value,
      health_status: document.querySelector("#filterIntegrationHealth")?.value,
      owner: document.querySelector("#filterIntegrationOwner")?.value.trim()
    };
    const response = await fetch(apiUrl("/integrations", params));
    if (!response.ok) throw new Error("Integration API unavailable");
    const payload = await response.json();
    return Array.isArray(payload) ? payload : payload.items || [];
  } catch {
    return integrationCatalog;
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

function filterIntegrations(items) {
  const category = document.querySelector("#filterIntegrationCategory").value;
  const status = document.querySelector("#filterIntegrationStatus").value;
  const health = document.querySelector("#filterIntegrationHealth").value;
  const owner = document.querySelector("#filterIntegrationOwner").value.trim().toLowerCase();
  return items
    .filter((item) => !category || item.category === category)
    .filter((item) => !status || item.status === status)
    .filter((item) => !health || item.health_status === health)
    .filter((item) => !owner || String(item.owner || "").toLowerCase().includes(owner));
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
        <td><button class="evidenceArtifactAction secondary" data-session="${escapeHtml(item.session_id || "")}">Artifacts</button></td>
      </tr>
    `);
    sessionSelect.insertAdjacentHTML("beforeend", `<option value="${escapeHtml(item.session_id)}">${escapeHtml(item.session_id)}</option>`);
  }
}

function renderEvidenceArtifacts(payload) {
  const panel = document.querySelector("#evidenceArtifacts");
  const artifacts = Array.isArray(payload.artifacts) ? payload.artifacts : [];
  const bundleHref = payload.bundle_download_url ? apiUrl(payload.bundle_download_url) : "";
  panel.innerHTML = `
    <dl>
      <dt>Session</dt><dd>${escapeHtml(payload.session_id || "unknown")}</dd>
      <dt>Artifact root</dt><dd class="${payload.artifact_root_configured ? "allow" : "require_approval"}">${payload.artifact_root_configured ? "configured" : "sample or disabled"}</dd>
      <dt>Artifacts</dt><dd>${Number(payload.artifact_count || artifacts.length || 0)}</dd>
      <dt>Bundle</dt><dd>${bundleHref ? `<a href="${escapeHtml(bundleHref)}">Download bundle</a>` : "not available from sample data"}</dd>
    </dl>
    <h3>Bundle Files</h3>
    <ul>${artifacts.map((item) => {
      const href = item.download_url ? apiUrl(item.download_url) : "";
      const label = `${item.artifact} (${item.kind || item.media_type || "artifact"})`;
      const suffix = item.bytes ? ` - ${Number(item.bytes)} bytes` : "";
      return `<li>${href ? `<a href="${escapeHtml(href)}">${escapeHtml(label)}</a>` : escapeHtml(label)}${escapeHtml(suffix)}<br><small>${escapeHtml(item.description || "")}</small></li>`;
    }).join("") || "<li>n/a</li>"}</ul>
  `;
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
        <td><button class="rolloutDetailAction secondary" data-id="${escapeHtml(item.rollout_id || "")}">Details</button></td>
      </tr>
    `);
  }
}

function renderPolicyRolloutDetail(detail) {
  const panel = document.querySelector("#rolloutDetail");
  if (!detail) {
    panel.textContent = "Policy rollout detail is not available.";
    return;
  }
  const rollout = detail.rollout || {};
  const repository = detail.repository || {};
  const policy = detail.policy_pack || {};
  const activity = detail.activity_summary || {};
  const integrations = detail.integration_summary || {};
  const readiness = detail.readiness || {};
  const checks = Array.isArray(readiness.checks) ? readiness.checks : [];
  const recent = Array.isArray(activity.recent_decisions) ? activity.recent_decisions : [];
  panel.innerHTML = `
    <dl>
      <dt>Rollout</dt><dd>${escapeHtml(rollout.rollout_id || "unknown")}</dd>
      <dt>Repository</dt><dd>${escapeHtml(rollout.repository || repository.repository || "unknown")}</dd>
      <dt>Policy</dt><dd>${escapeHtml(policy.title || rollout.policy_pack || "unknown")} ${escapeHtml(policy.version || rollout.policy_version || "")}</dd>
      <dt>Mode</dt><dd class="${riskClass(rollout.mode)}">${escapeHtml(rollout.mode || "enforce")}</dd>
      <dt>State</dt><dd class="${riskClass(rollout.state)}">${escapeHtml(rollout.state || "planned")}</dd>
      <dt>Coverage</dt><dd>${Number(rollout.coverage_percent || 0)}%</dd>
      <dt>Repository owner</dt><dd>${escapeHtml(repository.owner || rollout.owner || "unassigned")}</dd>
      <dt>Activity</dt><dd>${Number(activity.total || 0)} matching decisions</dd>
      <dt>Integrations</dt><dd>${Number(integrations.total || 0)} inventoried</dd>
      <dt>Readiness</dt><dd class="${readiness.status === "ready" ? "allow" : "require_approval"}">${escapeHtml(readiness.status || "needs_attention")}</dd>
    </dl>
    <h3>Rule Summary</h3>
    <ul>${Object.entries(policy.rule_summary || {}).map(([key, value]) => `<li>${escapeHtml(key)}: ${Number(value || 0)}</li>`).join("") || "<li>n/a</li>"}</ul>
    <h3>Readiness Checks</h3>
    <ul>${checks.map((item) => `<li><strong class="${item.status === "pass" ? "allow" : "require_approval"}">${escapeHtml(item.status)}</strong> ${escapeHtml(item.message || item.id)}</li>`).join("") || "<li>n/a</li>"}</ul>
    <h3>Recent Decisions</h3>
    <ul>${recent.map((item) => `<li><strong class="${riskClass(item.decision)}">${escapeHtml(item.decision)}</strong> ${escapeHtml(item.target || item.decision_id || "unknown")}</li>`).join("") || "<li>n/a</li>"}</ul>
  `;
}

function renderPolicyCatalog(items) {
  const panel = document.querySelector("#policyCatalog");
  panel.innerHTML = `
    <h3>Policy Catalog</h3>
    <ul>${items.map((item) => `<li><strong>${escapeHtml(item.id)}</strong> ${escapeHtml(item.version || "latest")}<br><small>${escapeHtml(item.title || item.description || "")}</small></li>`).join("") || "<li>n/a</li>"}</ul>
  `;
}

function renderPolicyDraft(draft) {
  const panel = document.querySelector("#policyDraft");
  const counts = draft.summary?.rule_counts || {};
  const errors = Array.isArray(draft.errors) ? draft.errors : [];
  panel.innerHTML = `
    <dl>
      <dt>Status</dt><dd class="${draft.valid ? "allow" : "block"}">${draft.valid ? "valid" : "invalid"}</dd>
      <dt>Policy</dt><dd>${escapeHtml(draft.summary?.policy_id || draft.policy_pack?.metadata?.id || "unknown")}</dd>
      <dt>Version</dt><dd>${escapeHtml(draft.summary?.version || "n/a")}</dd>
      <dt>Inherits</dt><dd>${escapeHtml(draft.summary?.inherits || "none")}</dd>
    </dl>
    <h3>Rule Counts</h3>
    <ul>${Object.entries(counts).map(([key, value]) => `<li>${escapeHtml(key)}: ${Number(value || 0)}</li>`).join("") || "<li>n/a</li>"}</ul>
    <h3>Validation</h3>
    <ul>${errors.map((item) => `<li class="block">${escapeHtml(item)}</li>`).join("") || "<li class=\"allow\">No schema errors</li>"}</ul>
  `;
}

function renderRolloutChangePlan(plan, applied) {
  const panel = document.querySelector("#rolloutChangePlan");
  const changes = Array.isArray(plan.changes) ? plan.changes : [];
  const notes = Array.isArray(plan.operator_notes) ? plan.operator_notes : [];
  panel.innerHTML = `
    <dl>
      <dt>Status</dt><dd class="${applied ? "allow" : "require_approval"}">${applied ? "applied" : "planned"}</dd>
      <dt>Operation</dt><dd>${escapeHtml(plan.operation || "update")}</dd>
      <dt>Risk</dt><dd class="${riskClass(plan.risk)}">${escapeHtml(plan.risk || "medium")}</dd>
      <dt>Approval</dt><dd class="${plan.approval_required ? "require_approval" : "allow"}">${plan.approval_required ? "required" : "not required"}</dd>
      <dt>Repository</dt><dd>${escapeHtml(plan.after?.repository || "unknown")}</dd>
      <dt>Policy</dt><dd>${escapeHtml(plan.after?.policy_pack || "unknown")}</dd>
    </dl>
    <h3>Changes</h3>
    <ul>${changes.map((item) => `<li>${escapeHtml(item.field)}: ${escapeHtml(item.before ?? "n/a")} -> ${escapeHtml(item.after ?? "n/a")}</li>`).join("") || "<li>n/a</li>"}</ul>
    <h3>Operator Notes</h3>
    <ul>${notes.map((item) => `<li>${escapeHtml(item)}</li>`).join("") || "<li>n/a</li>"}</ul>
  `;
}

function renderIntegrationRows(integrations) {
  const integrationRows = document.querySelector("#integrationRows");
  integrationRows.innerHTML = "";
  for (const item of integrations) {
    const capabilities = Array.isArray(item.capabilities) && item.capabilities.length ? item.capabilities.join(", ") : "not configured";
    integrationRows.insertAdjacentHTML("beforeend", `
      <tr>
        <td>${escapeHtml(item.name || item.integration_id || item.provider || "unknown")}</td>
        <td>${escapeHtml(item.category || "security")}</td>
        <td class="${riskClass(item.status)}">${escapeHtml(item.status || "planned")}</td>
        <td class="${riskClass(item.health_status)}">${escapeHtml(item.health_status || "not_checked")}</td>
        <td>${escapeHtml(item.owner || "platform-security")}</td>
        <td>${escapeHtml(item.environment || "global")}</td>
        <td>${escapeHtml(capabilities)}</td>
      </tr>
    `);
  }
}

function riskClass(value) {
  if (value === "critical" || value === "high" || value === "blocked" || value === "denied" || value === "strict" || value === "failed" || value === "disabled") return "block";
  if (value === "medium" || value === "experimental" || value === "pending" || value === "planned" || value === "audit_only" || value === "degraded" || value === "not_checked" || value === "configured") return "require_approval";
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

function renderSecurityBoundary(boundary) {
  const panel = document.querySelector("#securityBoundary");
  const oidc = boundary.oidc || {};
  const rbac = boundary.rbac || {};
  const cors = boundary.cors || {};
  const permissions = Array.isArray(boundary.console_permissions) ? boundary.console_permissions : [];
  const notes = Array.isArray(boundary.operator_notes) ? boundary.operator_notes : [];
  panel.innerHTML = `
    <dl>
      <dt>Mode</dt><dd class="${boundary.mode === "oidc_rbac_ready" ? "allow" : "require_approval"}">${escapeHtml(boundary.mode || "local_or_demo")}</dd>
      <dt>OIDC</dt><dd class="${oidc.configured ? "allow" : "require_approval"}">${oidc.configured ? "configured" : "disabled"}</dd>
      <dt>RBAC</dt><dd class="${rbac.configured ? "allow" : "require_approval"}">${rbac.configured ? "configured" : "disabled"}</dd>
      <dt>CORS</dt><dd>${cors.configured ? escapeHtml((cors.origins || []).join(", ")) : "same-origin or local demo"}</dd>
      <dt>OIDC env</dt><dd>${escapeHtml(oidc.config_env || "CAVRA_APPROVAL_OIDC_CONFIG")}</dd>
      <dt>RBAC env</dt><dd>${escapeHtml(rbac.config_env || "CAVRA_APPROVAL_RBAC_FILE")}</dd>
    </dl>
    <h3>Console Permissions</h3>
    <ul>${permissions.map((item) => `<li>${escapeHtml(item)}</li>`).join("") || "<li>n/a</li>"}</ul>
    <h3>Operator Notes</h3>
    <ul>${notes.map((item) => `<li>${escapeHtml(item)}</li>`).join("") || "<li>n/a</li>"}</ul>
  `;
}

function renderConsoleSession(session) {
  const panel = document.querySelector("#consoleSession");
  const actor = session.actor || {};
  const permissions = session.permissions || {};
  const repositoryPermissions = Array.isArray(session.repository_permissions) ? session.repository_permissions : [];
  const notes = Array.isArray(session.operator_notes) ? session.operator_notes : [];
  panel.innerHTML = `
    <dl>
      <dt>Mode</dt><dd class="${session.authenticated ? "allow" : "require_approval"}">${escapeHtml(session.mode || "local_or_demo")}</dd>
      <dt>Authenticated</dt><dd class="${session.authenticated ? "allow" : "require_approval"}">${session.authenticated ? "yes" : "no"}</dd>
      <dt>Actor</dt><dd>${escapeHtml(actor.actor || "not verified")}</dd>
      <dt>Issuer</dt><dd>${escapeHtml(actor.issuer || "n/a")}</dd>
      <dt>Groups</dt><dd>${escapeHtml((actor.groups || []).join(", ") || "n/a")}</dd>
    </dl>
    <h3>Permissions</h3>
    <ul>${Object.entries(permissions).map(([key, value]) => `<li><strong class="${value ? "allow" : "require_approval"}">${escapeHtml(value ? "allow" : "not allowed")}</strong> ${escapeHtml(key)}</li>`).join("") || "<li>n/a</li>"}</ul>
    <h3>Repository Scope</h3>
    <ul>${repositoryPermissions.map((item) => `<li>${escapeHtml(item.repository || "*")} / ${escapeHtml(item.approver_group || "*")} / ${escapeHtml((item.actions || []).join(", "))}</li>`).join("") || "<li>n/a</li>"}</ul>
    <h3>Operator Notes</h3>
    <ul>${notes.map((item) => `<li>${escapeHtml(item)}</li>`).join("") || "<li>n/a</li>"}</ul>
  `;
}

function renderDeploymentReadiness(report) {
  const panel = document.querySelector("#deploymentReadiness");
  const checks = Array.isArray(report.checks) ? report.checks : [];
  const notes = Array.isArray(report.operator_notes) ? report.operator_notes : [];
  panel.innerHTML = `
    <dl>
      <dt>Status</dt><dd class="${report.status === "ready" ? "allow" : "require_approval"}">${escapeHtml(report.status || "needs_attention")}</dd>
      <dt>Stores</dt><dd>${Number(report.store_summary?.total || 0)} checked</dd>
      <dt>Missing stores</dt><dd>${escapeHtml((report.store_summary?.missing || []).join(", ") || "none")}</dd>
    </dl>
    <h3>Checks</h3>
    <ul>${checks.map((item) => `<li><strong class="${item.status === "pass" ? "allow" : "require_approval"}">${escapeHtml(item.status)}</strong> ${escapeHtml(item.id)}<br><small>${escapeHtml(item.message || "")}</small></li>`).join("") || "<li>n/a</li>"}</ul>
    <h3>Operator Notes</h3>
    <ul>${notes.map((item) => `<li>${escapeHtml(item)}</li>`).join("") || "<li>n/a</li>"}</ul>
  `;
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

async function showEvidenceArtifacts(sessionId) {
  renderEvidenceArtifacts(await loadEvidenceArtifacts(sessionId));
}

async function refreshActivity() {
  const [sessions, decisions] = await Promise.all([loadSessions(), loadDecisions()]);
  renderActivityRows(filterSessions(sessions), filterDecisions(decisions));
}

async function refreshInventory() {
  const [repositories, rollouts] = await Promise.all([loadRepositories(), loadPolicyRollouts()]);
  renderInventoryRows(filterRepositories(repositories), filterPolicyRollouts(rollouts));
}

async function refreshPolicyCatalog() {
  renderPolicyCatalog(await loadPolicyCatalog());
}

async function showPolicyRolloutDetail(rolloutId) {
  renderPolicyRolloutDetail(await loadPolicyRolloutDetail(rolloutId));
}

async function refreshIntegrations() {
  const items = filterIntegrations(await loadIntegrations());
  renderIntegrationRows(items);
}

async function refreshSecurityBoundary() {
  renderSecurityBoundary(await loadSecurityBoundary());
}

async function refreshDeploymentReadiness() {
  renderDeploymentReadiness(await loadDeploymentReadiness());
}

async function refreshConsoleSession() {
  renderConsoleSession(await loadConsoleSession());
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
      headers: apiHeaders(true),
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
      headers: apiHeaders(true),
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
document.querySelector("#refreshPolicyCatalog").addEventListener("click", refreshPolicyCatalog);
document.querySelector("#previewPolicyDraft").addEventListener("click", previewPolicyDraft);
document.querySelector("#planRolloutChange").addEventListener("click", planRolloutChange);
document.querySelector("#applyRolloutChange").addEventListener("click", applyRolloutChange);
document.querySelector("#refreshIntegrations").addEventListener("click", refreshIntegrations);
document.querySelector("#refreshSecurityBoundary").addEventListener("click", refreshSecurityBoundary);
document.querySelector("#refreshDeploymentReadiness").addEventListener("click", refreshDeploymentReadiness);
document.querySelector("#refreshConsoleSession").addEventListener("click", refreshConsoleSession);
document.querySelector("#saveConsoleToken").addEventListener("click", async () => {
  consoleAuthToken = document.querySelector("#consoleToken").value.trim();
  window.sessionStorage?.setItem("cavraConsoleToken", consoleAuthToken);
  await refreshConsoleSession();
});
document.querySelector("#clearConsoleToken").addEventListener("click", async () => {
  consoleAuthToken = "";
  document.querySelector("#consoleToken").value = "";
  window.sessionStorage?.removeItem("cavraConsoleToken");
  await refreshConsoleSession();
});
document.querySelector("#refreshApprovals").addEventListener("click", refreshApprovals);
document.querySelector("#refreshRegistry").addEventListener("click", refreshRegistry);
document.querySelector("#createBreakGlass").addEventListener("click", createBreakGlassApproval);
document.querySelector("#evidenceRows").addEventListener("click", async (event) => {
  if (!(event.target instanceof Element)) return;
  const artifactButton = event.target.closest(".evidenceArtifactAction");
  if (!artifactButton) return;
  await showEvidenceArtifacts(artifactButton.dataset.session);
});
document.querySelector("#rolloutRows").addEventListener("click", async (event) => {
  if (!(event.target instanceof Element)) return;
  const detailButton = event.target.closest(".rolloutDetailAction");
  if (!detailButton) return;
  await showPolicyRolloutDetail(detailButton.dataset.id);
});
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
refreshPolicyCatalog();
refreshIntegrations();
refreshSecurityBoundary();
refreshDeploymentReadiness();
document.querySelector("#consoleToken").value = consoleAuthToken;
refreshConsoleSession();
refreshApprovals();
refreshRegistry();
