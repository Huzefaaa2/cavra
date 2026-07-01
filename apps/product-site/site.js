const menuButton = document.querySelector("#menuButton");
const mobileNav = document.querySelector("#mobileNav");
const scenarioForm = document.querySelector("#scenarioForm");
const decisionJson = document.querySelector("#decisionJson");
const decisionBadge = document.querySelector("#decisionBadge");
const evidencePanel = document.querySelector("#evidencePanel");
const roleCard = document.querySelector("#roleCard");
const roleButtons = document.querySelector("#roleButtons");

const scenarioControls = {
  agent: document.querySelector("#agentSelect"),
  action: document.querySelector("#actionSelect"),
  environment: document.querySelector("#envSelect"),
  trust: document.querySelector("#trustSelect"),
};

const metrics = {
  blocked: document.querySelector("#metricBlocked"),
  blockers: document.querySelector("#metricBlockers"),
  mcp: document.querySelector("#metricMcp"),
  evidence: document.querySelector("#metricEvidence"),
};

const evidenceViews = {
  auditor: {
    control: "PROD_IAM_CHANGE",
    reviewer: "Security approval required",
    evidence: "signed, timestamped, hash-linked",
    finding: "Production governance blocker",
    retention: "Exportable packet for audit review",
  },
  developer: {
    action: "modify_iac",
    reason: "Production IAM escalation requires a policy-approved reviewer.",
    next_step: "Open approval request with diff and target context.",
    cli: "cavra evaluate modify_iac --target iam/admin-role.tf --env production",
  },
  executive: {
    outcome: "Unsafe autonomous production change prevented.",
    posture: "AISPM readiness remains blocked until reviewer approval.",
    value: "Developer velocity continues while high-risk actions stay governed.",
  },
  raw: {
    schema_version: "cavra.evidence.public.demo.v1",
    actor: "claude-code",
    decision: "requires_approval",
    evidence_id: "evd_public_demo_9f2a",
    controls: ["PROD_CHANGE", "IAM_ADMIN", "MCP_UNKNOWN"],
  },
};

const roleCopy = {
  ciso: {
    title: "CISO path",
    body: "See which AI-agent actions are governed, where policy coverage is weak, which exceptions remain open, and whether production readiness is blocked.",
    cta: "Start with AISPM, evidence freshness, and Enterprise Subscription controls.",
  },
  platform: {
    title: "Platform engineering path",
    body: "Connect repositories, CI/CD, MCP tools, report delivery providers, and evidence stores without forcing every control into a manual review queue.",
    cta: "Start with Community deployment, Managed architecture, and connector readiness.",
  },
  developer: {
    title: "Developer path",
    body: "Keep using AI coding agents while CAVRA evaluates the risky edges: shell commands, Git operations, IaC changes, MCP calls, and production workflows.",
    cta: "Start with the sandbox, CLI reference, and one governed workflow.",
  },
  auditor: {
    title: "Auditor path",
    body: "Review who acted, what was attempted, what policy decided, who approved it, and where signed evidence lives without reconstructing events from chat logs.",
    cta: "Start with evidence packets, report center, and Trial Field Guide labs.",
  },
  executive: {
    title: "Executive path",
    body: "Adopt AI agents with measurable operating confidence: fewer unsafe actions, stronger evidence, clearer readiness, and accountable support paths.",
    cta: "Start with Managed, Enterprise Subscription, and the buyer packet.",
  },
};

function decisionForScenario() {
  const action = scenarioControls.action.value;
  const environment = scenarioControls.environment.value;
  const trust = scenarioControls.trust.value;
  const agent = scenarioControls.agent.value;
  const highRisk = environment === "production" || action === "deploy_prod" || trust === "unknown";
  const blocked = action === "deploy_prod" && trust === "unknown";
  const decision = blocked ? "block" : highRisk ? "requires_approval" : "allow_with_attestation";
  const controls = [
    environment === "production" ? "PROD_CHANGE" : "ENVIRONMENT_CONTEXT",
    trust === "unknown" ? "MCP_UNKNOWN" : trust === "restricted" ? "MCP_RESTRICTED" : "MCP_TRUSTED",
    action === "modify_iac" ? "IAC_CHANGE" : action === "run_shell" ? "SHELL_EXECUTION" : "AGENT_ACTION",
  ];
  return {
    decision,
    reason:
      decision === "block"
        ? "Production action attempted through unknown trust context."
        : decision === "requires_approval"
          ? "High-risk action requires reviewer authority before execution."
          : "Action can proceed with signed attestation and evidence capture.",
    actor: agent,
    action,
    target: action === "modify_iac" ? "iam/admin-role.tf" : action === "call_mcp_tool" ? "ticketing.mcp/create_change" : "repository workflow",
    environment,
    controls,
    evidence_id: `evd_public_demo_${Math.random().toString(16).slice(2, 6)}`,
    aispm: {
      finding: decision === "allow_with_attestation" ? "covered_action" : "production_governance_blocker",
      readiness: decision === "block" ? "not_ready" : decision === "requires_approval" ? "approval_pending" : "ready",
    },
  };
}

function renderDecision() {
  const packet = decisionForScenario();
  decisionBadge.textContent = packet.decision.replace("_", " ");
  decisionBadge.style.background = packet.decision === "block" ? "var(--red)" : packet.decision === "requires_approval" ? "var(--amber)" : "var(--green)";
  decisionBadge.style.color = packet.decision === "requires_approval" ? "#03100b" : "#fff";
  decisionJson.textContent = JSON.stringify(packet, null, 2);
  metrics.blocked.textContent = packet.decision === "block" ? "43" : "42";
  metrics.blockers.textContent = packet.aispm.readiness === "ready" ? "0" : "1";
  metrics.mcp.textContent = packet.controls.includes("MCP_UNKNOWN") ? "71%" : "84%";
  metrics.evidence.textContent = packet.decision === "allow_with_attestation" ? "99%" : "98%";
}

function renderEvidence(view = "auditor") {
  evidencePanel.textContent = JSON.stringify(evidenceViews[view], null, 2);
}

function renderRole(role = "ciso") {
  const next = roleCopy[role];
  roleCard.innerHTML = `
    <h3>${next.title}</h3>
    <p>${next.body}</p>
    <p><strong>${next.cta}</strong></p>
  `;
}

menuButton.addEventListener("click", () => {
  const expanded = menuButton.getAttribute("aria-expanded") === "true";
  menuButton.setAttribute("aria-expanded", String(!expanded));
  mobileNav.classList.toggle("is-open", !expanded);
});

mobileNav.addEventListener("click", (event) => {
  if (event.target instanceof HTMLAnchorElement) {
    mobileNav.classList.remove("is-open");
    menuButton.setAttribute("aria-expanded", "false");
  }
});

scenarioForm.addEventListener("change", renderDecision);

document.querySelectorAll("[data-evidence-tab]").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelectorAll("[data-evidence-tab]").forEach((item) => item.classList.remove("is-active"));
    button.classList.add("is-active");
    renderEvidence(button.dataset.evidenceTab);
  });
});

roleButtons.addEventListener("click", (event) => {
  const button = event.target.closest("button[data-role]");
  if (!button) return;
  roleButtons.querySelectorAll("button").forEach((item) => item.classList.remove("is-active"));
  button.classList.add("is-active");
  renderRole(button.dataset.role);
});

renderDecision();
renderEvidence();
renderRole();
