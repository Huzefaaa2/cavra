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
    decision: { target: "iam/admin-role.tf", rule_id: "filesystem.write.require_approval" }
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
    decision: { target: "terraform apply", rule_id: "commands.block" }
  }
];

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

function filterApprovals(items) {
  const state = document.querySelector("#filterApprovalState").value;
  const group = document.querySelector("#filterApprovalGroup").value.trim().toLowerCase();
  return items
    .filter((item) => !state || item.state === state)
    .filter((item) => !group || String(item.approver_group || "").toLowerCase().includes(group));
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

function renderApprovalRows(items) {
  const rows = document.querySelector("#approvalRows");
  rows.innerHTML = "";
  for (const item of items) {
    const stateClass = item.state === "break_glass" ? "warn" : item.state === "denied" ? "block" : "allow";
    rows.insertAdjacentHTML("beforeend", `
      <tr>
        <td>${escapeHtml(item.approval_id || "unknown")}</td>
        <td class="${stateClass}">${escapeHtml(item.state || "pending")}</td>
        <td>${escapeHtml(item.approver_group || "Repository Owners")}</td>
        <td>${escapeHtml(item.requested_by || "ai-agent")}</td>
        <td>${escapeHtml(item.decision?.target || item.decision_id || "unknown")}</td>
        <td>${escapeHtml(item.external_ref || "n/a")}</td>
      </tr>
    `);
  }
}

async function refreshEvidence() {
  const items = filterEvidence(await loadEvidenceMetadata());
  renderEvidenceRows(items);
}

async function refreshApprovals() {
  const items = filterApprovals(await loadApprovals());
  renderApprovalRows(items);
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
document.querySelector("#refreshApprovals").addEventListener("click", refreshApprovals);
document.querySelector("#verifyAttestation").addEventListener("click", verifyAttestation);
document.querySelector("#copyInstall").addEventListener("click", async () => {
  await navigator.clipboard.writeText("claude mcp add cavra -- cavra-mcp-server");
});
refreshEvidence();
refreshApprovals();
