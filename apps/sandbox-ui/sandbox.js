const navItems = [
  { id: "dashboard", label: "Dashboard", icon: "grid", group: "Overview", description: "Mission, platform overview, risk score, and release readiness." },
  { id: "ai-posture", label: "AI Posture", icon: "posture", group: "Overview", description: "AI security posture, agent observability, findings, and execution timeline." },
  { id: "architecture", label: "Architecture", icon: "network", group: "Overview", description: "Interactive runtime, policy, evidence, and audit architecture." },
  { id: "policy-engine", label: "Policy Engine", icon: "shield", group: "Core Components", description: "Policy packs, categories, violations, remediation, and risk levels." },
  { id: "evidence", label: "Evidence Collector", icon: "archive", group: "Core Components", description: "Audit trails, attestations, and chain of custody." },
  { id: "use-cases", label: "Use Cases", icon: "layers", group: "Use Cases", description: "Terraform, Kubernetes, AI-agent, MCP, and supply-chain governance." },
  { id: "operator-experience", label: "Operator Paths", icon: "route", group: "Use Cases", description: "Persona-specific closeout journeys for prospects, auditors, platform teams, and CISOs." },
  { id: "enterprise-trial", label: "Enterprise Trial", icon: "key", group: "Platform", description: "Self-service approved access for the licensed Enterprise Trial package." },
  { id: "integrations", label: "Integrations", icon: "plug", group: "Platform", description: "GitHub, GitLab, clouds, IaC, Kubernetes, and MCP servers." },
  { id: "compliance", label: "Compliance", icon: "check", group: "Platform", description: "NIST, SOC2, ISO27001, CIS, PCI DSS, and OWASP mappings." },
  { id: "roadmap", label: "Roadmap", icon: "map", group: "Platform", description: "Interactive Community, Enterprise, SaaS, and release roadmap." },
  { id: "documentation", label: "Documentation", icon: "book", group: "Resources", description: "Quickstart, API reference, deployment, and public docs links." }
];

const icons = {
  grid: "▦",
  posture: "◉",
  network: "⌘",
  shield: "◈",
  archive: "▣",
  layers: "▤",
  route: "▥",
  key: "◐",
  plug: "◇",
  check: "✓",
  map: "◎",
  book: "▰"
};

const themes = {
  sentinel: "Sentinel",
  classic: "Classic",
  retro: "Retro",
  executive: "Executive"
};

const metrics = [
  ["Policy Packs", "14", "Community and enterprise-ready policy domains"],
  ["Evidence Types", "28", "Bundles, attestations, approvals, release packets"],
  ["Integrations", "10", "Developer, cloud, IaC, and MCP control surfaces"],
  ["Compliance", "47", "Mapped governance and audit controls"],
  ["Risk Categories", "6", "Secrets, IAM, runtime, release, MCP, drift"]
];

const communityGaCards = [
  ["Policy signing", "Ready", "Ed25519 signing workflow and public validation commands are documented."],
  ["Runtime modes", "Ready", "Audit, shadow, enforce, and break-glass behavior is visible to operators."],
  ["Golden decisions", "Ready", "Baseline decisions cover file, command, MCP, Git, and PR workflows."],
  ["Release evidence", "Ready", "Release packet, verification runbook, and post-release evidence are linked."]
];

const pilotCards = [
  ["Repositories", "Scoped", "Protected branches and required CAVRA checks define the pilot perimeter."],
  ["Agents", "Transparent", "AI agents are declared as automation with auditable identities."],
  ["CI/CD", "Blocking", "CAVRA required-check evidence can block unsafe delivery."],
  ["Handoff", "Ready", "Enterprise and SaaS handoff docs stay public-safe."]
];

const architectureNodes = [
  {
    id: "github",
    title: "GitHub",
    subtitle: "Pull requests, Actions, branch protection",
    purpose: "Routes source, pull request, and workflow events into CAVRA decisions.",
    inputs: "PR metadata, workflow context, commit, actor, repository rules.",
    outputs: "Required check status, evidence artifact, PR attestation.",
    responsibilities: "Prevent direct bypasses by enforcing CAVRA as a protected required check."
  },
  {
    id: "gitlab",
    title: "GitLab",
    subtitle: "Merge requests and CI pipelines",
    purpose: "Extends the same governance model to GitLab repositories and runners.",
    inputs: "MR metadata, job token claims, pipeline state.",
    outputs: "Pipeline pass/warn/block result and evidence bundle.",
    responsibilities: "Keep agent automation transparent across non-GitHub platforms."
  },
  {
    id: "iac",
    title: "Terraform / OpenTofu",
    subtitle: "Infrastructure plan metadata",
    purpose: "Evaluates infrastructure changes before execution.",
    inputs: "Plan summaries, resource changes, cloud IAM deltas.",
    outputs: "Policy decision, risk score, approval route, remediation text.",
    responsibilities: "Stop production-impacting changes from bypassing review."
  },
  {
    id: "kubernetes",
    title: "Kubernetes",
    subtitle: "Manifests, RBAC, runtime policy",
    purpose: "Checks cluster-facing changes for privilege and deployment risk.",
    inputs: "Manifest diffs, RBAC bindings, namespace and workload metadata.",
    outputs: "Risk category, severity, and evidence reference.",
    responsibilities: "Protect platform runtime surfaces from autonomous drift."
  },
  {
    id: "cavra",
    title: "CAVRA",
    subtitle: "Runtime Guard",
    purpose: "Central decision point before an AI agent acts.",
    inputs: "Actor, action, target, context, policy pack, trust registry.",
    outputs: "Allow, block, require approval, or allow with attestation.",
    responsibilities: "Normalize decisions across repositories, tools, and release workflows."
  },
  {
    id: "policy",
    title: "Policy Engine",
    subtitle: "Rules, packs, severity, remediation",
    purpose: "Compiles enterprise policies into deterministic decision logic.",
    inputs: "Policy packs, repository scope, actor claims, resource metadata.",
    outputs: "Decision, severity, rationale, remediation, controls mapping.",
    responsibilities: "Make governance explainable and testable."
  },
  {
    id: "evidence-engine",
    title: "Evidence Engine",
    subtitle: "Bundles, attestations, chain of custody",
    purpose: "Captures decision evidence for audit, compliance, and release review.",
    inputs: "Decision payloads, approvals, runtime metadata, release packets.",
    outputs: "Signed bundles, PR attestations, audit exports.",
    responsibilities: "Turn enforcement into durable audit artifacts."
  },
  {
    id: "audit",
    title: "Audit Trail",
    subtitle: "Search, export, compliance mapping",
    purpose: "Presents evidence records to auditors, security, platform, and release owners.",
    inputs: "Evidence metadata, bundles, control mappings, release verification.",
    outputs: "Audit packets, compliance reports, release readiness views.",
    responsibilities: "Show who did what, why it was allowed, and which controls were met."
  },
  {
    id: "cloud",
    title: "AWS / Azure / GCP",
    subtitle: "Cloud risk and deployment context",
    purpose: "Provides target-environment context for cloud-impacting actions.",
    inputs: "IAM, storage, network, runtime, and deployment metadata.",
    outputs: "Risk categories, compliance evidence, and drift signals.",
    responsibilities: "Connect agent intent to enterprise cloud control outcomes."
  }
];

const policies = [
  ["Critical", "Secrets exposure", "Block reading `.env`, private keys, or customer records.", "Use managed secret references and scoped evidence redaction."],
  ["High", "Production mutation", "Require approval for deployment, IAM, or protected branch changes.", "Route to security or platform owner with attestation."],
  ["Medium", "Untrusted MCP server", "Block unapproved MCP tools with filesystem, shell, or network capability.", "Register server, declare permissions, and rerun trust check."],
  ["Low", "Documentation update", "Allow low-risk docs edits with release-note freshness checks.", "Attach public boundary validation evidence."]
];

const integrations = [
  ["GitHub", "Required checks, PR attestations, release evidence", "Ready"],
  ["GitLab", "Pipeline checks and merge-request governance", "Planned"],
  ["Azure DevOps", "Pipeline and policy approval integration", "Planned"],
  ["Terraform", "Plan metadata and infrastructure risk", "Ready"],
  ["OpenTofu", "IaC plan parity and policy packs", "Ready"],
  ["Kubernetes", "RBAC and manifest governance", "Ready"],
  ["AWS", "IAM, storage, network, and evidence targets", "Ready"],
  ["Azure", "Identity, storage, and deployment checks", "Ready"],
  ["GCP", "Cloud resource and policy context", "Planned"],
  ["MCP Servers", "Trust registry and tool capability classification", "Ready"]
];

const complianceRows = [
  ["NIST", "AC-6 Least Privilege", "cloud-iam-prod", "PR attestation and approval evidence", "Mapped"],
  ["SOC2", "Change Management", "release-governance", "Release packet and required-check evidence", "Mapped"],
  ["ISO27001", "A.8 Asset and access control", "mcp-enterprise", "Trust registry decision evidence", "Mapped"],
  ["CIS", "Kubernetes RBAC", "kubernetes-prod", "Manifest evaluation evidence", "Mapped"],
  ["PCI DSS", "Secure change control", "pci-dss", "Policy decision and audit export", "Mapped"],
  ["OWASP", "Command injection", "owasp-agentic", "Blocked command evidence", "Mapped"]
];

const useCases = [
  ["Terraform Governance", "Evaluate infrastructure plans before AI agents execute destructive changes."],
  ["Infrastructure Drift", "Compare desired state, endpoint inventory, and release channel evidence."],
  ["Kubernetes Security", "Catch privilege and workload changes before runtime impact."],
  ["AI Agent Governance", "Make agent identities, actions, and approvals transparent."],
  ["MCP Governance", "Classify MCP server capabilities and block untrusted tools."],
  ["Software Supply Chain", "Require CAVRA evidence for protected branches and release workflows."],
  ["Audit Automation", "Package decisions, approvals, and release packets for compliance review."]
];

const operatorPaths = [
  [
    "Prospect",
    "Can CAVRA explain its value without private access?",
    "Dashboard, Architecture, Use Cases, Documentation",
    "Risk posture, before-the-agent-acts flow, supported integrations, and trial handoff links."
  ],
  [
    "Auditor",
    "Can I trace a decision to durable evidence?",
    "Evidence, Compliance, Release Readiness Dashboard, Release Index",
    "Decision payload, compliance mapping, release packet, verification packet, and public boundary statement."
  ],
  [
    "Platform Team",
    "Can this be enforced in CI and developer workflows?",
    "Architecture, Integrations, Policy Engine, Documentation",
    "Required checks, policy packs, GitHub/GitLab/Azure DevOps paths, CLI commands, and deployment references."
  ],
  [
    "CISO",
    "Can I govern AI agents without exposing Enterprise source?",
    "Dashboard, Compliance, Operator Paths, Enterprise Trial",
    "Blocked-risk narrative, control coverage, open-core boundary, and Enterprise/SaaS handoff documentation."
  ]
];

const trialAccessCards = [
  ["Package", "2026.06.05", "ghcr.io/huzefaaa2/cavra-enterprise-trial:2026.06.05"],
  ["Integrity", "Verified", "Digest sha256:2d5f0d338a5528205f11674917d1526db7aa9732ef2af6ca3bd957b6230b4b47"],
  ["Access", "Gated", "Private GHCR access plus a time-limited trial license."],
  ["Controls", "Enforced", "Signed license, revocation, expiry, registry pull, and runtime checks."]
];

const timeline = [
  ["Intent captured", "Agent action is normalized with actor, target, repository, tool, and context."],
  ["Policy evaluated", "Policy Engine returns allow, block, approval, or attestation decision."],
  ["Evidence sealed", "Evidence Collector records rationale, severity, controls, and chain-of-custody metadata."],
  ["Audit mapped", "Compliance mapping links the decision to NIST, SOC2, ISO27001, CIS, PCI, or OWASP."],
  ["Review exported", "Release, audit, or PR evidence is attached to the delivery workflow."]
];

const docsLinks = [
  ["Quickstart", "README.md"],
  ["Community Release Index", "docs/community-release-index.md"],
  ["Release Readiness Dashboard", "docs/community-release-readiness-dashboard.md"],
  ["Community GA Path", "docs/community-ga-user-verifiable-path.md"],
  ["API Reference", "docs/api.md"],
  ["Deployment", "docs/deployment.md"],
  ["Open-Core Model", "docs/architecture/open-core-model.md"],
  ["Enterprise Trial", "docs/enterprise/trial.md"],
  ["Self-Service Trial Access", "docs/enterprise/trial-self-service-access.md"]
];

const roadmap = [
  ["Community", ["AISPM public contract", "AI Posture demo route", "Release readiness dashboard"]],
  ["Enterprise", ["Live AISPM ingestion", "SSO/RBAC", "Kill switch and runtime overrides"]],
  ["SaaS", ["Tenant control plane", "Billing and license service", "Compliance reporting"]],
  ["Ecosystem", ["GitLab and Azure DevOps", "Policy/plugin marketplace", "Managed evidence storage"]]
];

const aispmFallback = {
  schema_version: "cavra.aispm.dashboard.v1",
  product: "CAVRA",
  edition: "community",
  mode: "sample",
  data_provenance: "sample_data",
  tracking: "none",
  telemetry: "disabled",
  overview: {
    posture_score: 12,
    risk_level: "critical",
    total_sessions: 2,
    total_decisions: 3,
    blocked_actions: 1,
    approval_required_actions: 1,
    warned_actions: 1,
    risk_findings: 3,
    evidence_confidence: "activity_evidence_refs"
  },
  agents: [
    { agent_id: "codex-agent", repository_count: 1, session_count: 1, decision_count: 2, blocked_actions: 1, approval_required_actions: 1, warned_actions: 0, coverage_status: "observed", drift_status: "review_required" },
    { agent_id: "claude-code-agent", repository_count: 1, session_count: 1, decision_count: 1, blocked_actions: 0, approval_required_actions: 0, warned_actions: 1, coverage_status: "observed", drift_status: "baseline" }
  ],
  findings: [
    { finding_id: "finding-sample-dec-002", decision_id: "sample-dec-002", session_id: "sample-session-001", agent_id: "codex-agent", repository: "payments/api", severity: "critical", risk_classification: "credential_or_sensitive_data_exposure", decision: "block", rule_id: "secrets.block-sensitive-read", reason: "Sensitive production secret file access is blocked.", evidence_refs: ["sample://evidence/secret-read-block"], timestamp: "2026-06-09T00:01:00+00:00" },
    { finding_id: "finding-sample-dec-001", decision_id: "sample-dec-001", session_id: "sample-session-001", agent_id: "codex-agent", repository: "payments/api", severity: "high", risk_classification: "infrastructure_change_risk", decision: "require_approval", rule_id: "iac.production-change", reason: "Production-impacting infrastructure action requires approval.", evidence_refs: ["sample://evidence/iac-production-change"], timestamp: "2026-06-09T00:00:00+00:00" }
  ],
  timeline: [
    { event_id: "decision-sample-dec-002", event_type: "policy_decision", decision_id: "sample-dec-002", session_id: "sample-session-001", agent_id: "codex-agent", repository: "payments/api", title: "block read_file", outcome: "block", severity: "critical", target: ".env.production", timestamp: "2026-06-09T00:01:00+00:00", evidence_refs: ["sample://evidence/secret-read-block"] },
    { event_id: "decision-sample-dec-001", event_type: "policy_decision", decision_id: "sample-dec-001", session_id: "sample-session-001", agent_id: "codex-agent", repository: "payments/api", title: "require_approval execute_command", outcome: "require_approval", severity: "high", target: "terraform apply", timestamp: "2026-06-09T00:00:00+00:00", evidence_refs: ["sample://evidence/iac-production-change"] }
  ],
  control_coverage: [
    { surface_id: "sensitive_data", label: "Secrets and sensitive data", description: "Reads or writes that could expose credentials, tokens, customer data, or protected files.", coverage_status: "enforced", decision_count: 1, blocked_actions: 1, approval_required_actions: 0, warned_actions: 0, evidence_confidence: "activity_evidence_refs", evidence_refs: ["sample://evidence/secret-read-block"] },
    { surface_id: "infrastructure_iac", label: "Infrastructure and IaC", description: "Cloud, Terraform/OpenTofu, Kubernetes, and production infrastructure actions.", coverage_status: "approval_gated", decision_count: 1, blocked_actions: 0, approval_required_actions: 1, warned_actions: 0, evidence_confidence: "activity_evidence_refs", evidence_refs: ["sample://evidence/iac-production-change"] },
    { surface_id: "mcp_tools", label: "MCP and tool calls", description: "External tool, MCP server, filesystem, browser, and automation actions.", coverage_status: "warning_only", decision_count: 1, blocked_actions: 0, approval_required_actions: 0, warned_actions: 1, evidence_confidence: "activity_evidence_refs", evidence_refs: ["sample://evidence/mcp-warning"] }
  ],
  near_misses: [
    { near_miss_id: "near-miss-sample-dec-001", decision_id: "sample-dec-001", session_id: "sample-session-001", agent_id: "codex-agent", repository: "payments/api", surface_id: "infrastructure_iac", severity: "high", decision: "require_approval", risk_classification: "infrastructure_change_risk", reason: "Production-impacting infrastructure action requires approval.", operator_signal: "approval_prevented_unreviewed_execution", evidence_refs: ["sample://evidence/iac-production-change"], timestamp: "2026-06-09T00:00:00+00:00" },
    { near_miss_id: "near-miss-sample-dec-003", decision_id: "sample-dec-003", session_id: "sample-session-002", agent_id: "claude-code-agent", repository: "platform/infra", surface_id: "mcp_tools", severity: "medium", decision: "warn", risk_classification: "tool_or_mcp_governance_risk", reason: "MCP tool requires registration before broad rollout.", operator_signal: "warning_allowed_with_operator_visibility", evidence_refs: ["sample://evidence/mcp-warning"], timestamp: "2026-06-09T00:02:00+00:00" }
  ],
  control_plane: {
    community_status: "local_activity_ready",
    enterprise_status: "requires_cavra_enterprise",
    live_streaming: "requires_cavra_enterprise",
    kill_switch: "requires_cavra_enterprise",
    runtime_overrides: "requires_cavra_enterprise",
    policy_distribution: "requires_cavra_enterprise",
    trace_replay: "local_timeline_available",
    data_provenance_required: true
  }
};

const routeContent = [
  ...navItems.map((item) => ({ type: "Page", label: item.label, route: item.id, description: item.description })),
  ...policies.map((item) => ({ type: "Policy", label: item[1], route: "policy-engine", description: item[2] })),
  ...integrations.map((item) => ({ type: "Integration", label: item[0], route: "integrations", description: item[1] })),
  ...complianceRows.map((item) => ({ type: "Control", label: `${item[0]} ${item[1]}`, route: "compliance", description: item[3] })),
  ...useCases.map((item) => ({ type: "Use Case", label: item[0], route: "use-cases", description: item[1] })),
  ...operatorPaths.map((item) => ({ type: "Operator Path", label: item[0], route: "operator-experience", description: item[1] })),
  ...trialAccessCards.map((item) => ({ type: "Enterprise Trial", label: item[0], route: "enterprise-trial", description: item[2] })),
  { type: "AI Posture", label: "Agent Observability", route: "ai-posture", description: "Live-ready agent coverage, risk findings, and execution timeline." },
  { type: "AI Posture", label: "Kill Switch", route: "ai-posture", description: "Enterprise runtime control plane capability marked as locked in Community." },
  { type: "AI Posture", label: "Evidence Confidence", route: "ai-posture", description: "Dashboard tiles identify sample, local, or Enterprise data provenance." }
];

function el(selector) {
  return document.querySelector(selector);
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function renderNav(target) {
  const groups = navItems.reduce((acc, item) => {
    acc[item.group] = acc[item.group] || [];
    acc[item.group].push(item);
    return acc;
  }, {});
  target.innerHTML = Object.entries(groups).map(([group, items]) => `
    <div class="nav-group">
      <p class="nav-heading">${group}</p>
      ${items.map((item) => `
        <button class="nav-link" data-route="${item.id}" aria-label="${item.label}">
          <span>${icons[item.icon]}</span>
          <span class="nav-label">${item.label}</span>
          <small>›</small>
        </button>
      `).join("")}
    </div>
  `).join("");
}

function setRoute(route) {
  const nextRoute = navItems.some((item) => item.id === route) ? route : "dashboard";
  document.querySelectorAll(".page-panel").forEach((panel) => {
    panel.classList.toggle("is-active", panel.id === nextRoute);
  });
  document.querySelectorAll(".nav-link").forEach((link) => {
    link.classList.toggle("is-active", link.dataset.route === nextRoute);
  });
  document.querySelectorAll("[data-route-link]").forEach((link) => {
    link.classList.toggle("is-active", link.dataset.routeLink === nextRoute);
  });
  localStorage.setItem("cavra.activeRoute", nextRoute);
  if (location.hash.slice(1) !== nextRoute) history.replaceState(null, "", `#${nextRoute}`);
  window.scrollTo(0, 0);
  renderToc(nextRoute);
  el("#mainContent")?.focus({ preventScroll: true });
}

function renderToc(route) {
  const panel = document.getElementById(route);
  const toc = el("#toc");
  if (!panel || !toc) return;
  const headings = [...panel.querySelectorAll("h2, h3")].slice(0, 8);
  toc.innerHTML = `<h2>On this page</h2>${headings.map((heading, index) => {
    if (!heading.id) heading.id = `${route}-heading-${index}`;
    return `<a href="#${heading.id}">${escapeHtml(heading.textContent)}</a>`;
  }).join("")}`;
}

function renderMetrics() {
  el("#demoMetrics").innerHTML = metrics.map(([label, value, detail]) => `
    <div class="metric-card"><span>${label}</span><strong>${value}</strong><small>${detail}</small></div>
  `).join("");
  el("#communityGaSummary").innerHTML = communityGaCards.map(([label, value, detail]) => `
    <article class="community-ga-card"><span>${label}</span><strong>${value}</strong><p>${detail}</p></article>
  `).join("");
  el("#pilotReadinessSummary").innerHTML = pilotCards.map(([label, value, detail]) => `
    <article class="pilot-readiness-card"><span>${label}</span><strong>${value}</strong><p>${detail}</p></article>
  `).join("");
}

function renderArchitecture(selectedId = "cavra") {
  const map = el("#architectureMap");
  map.innerHTML = architectureNodes.map((node) => `
    <button class="arch-node ${node.id === selectedId ? "is-selected" : ""}" data-node="${node.id}">
      <strong>${node.title}</strong>
      <small>${node.subtitle}</small>
    </button>
  `).join("");
  renderNodeInspector(selectedId);
}

function renderNodeInspector(nodeId) {
  const node = architectureNodes.find((item) => item.id === nodeId) || architectureNodes[4];
  el("#nodeInspector").innerHTML = `
    <h3>${node.title}</h3>
    <p>${node.subtitle}</p>
    <dl>
      <dt>Purpose</dt><dd>${node.purpose}</dd>
      <dt>Inputs</dt><dd>${node.inputs}</dd>
      <dt>Outputs</dt><dd>${node.outputs}</dd>
      <dt>Responsibilities</dt><dd>${node.responsibilities}</dd>
    </dl>
  `;
}

function renderPolicies() {
  el("#policyExplorer").innerHTML = policies.map(([severity, title, violation, remediation]) => `
    <article class="policy-card">
      <span class="severity ${severity.toLowerCase()}">${severity}</span>
      <h3>${title}</h3>
      <p><strong>Violation:</strong> ${violation}</p>
      <p><strong>Remediation:</strong> ${remediation}</p>
    </article>
  `).join("");
}

function renderEvidence() {
  el("#evidenceTimeline").innerHTML = timeline.map(([title, detail]) => `
    <div class="timeline-item"><h3>${title}</h3><p>${detail}</p></div>
  `).join("");
}

function renderAispmDashboard(payload, note = "sample fallback") {
  const overview = payload.overview || {};
  const controlPlane = payload.control_plane || {};
  el("#aispmSourceBadge").textContent = `${payload.data_provenance || "sample_data"} · ${note}`;
  const overviewCards = [
    ["Posture Score", overview.posture_score ?? "0", `Risk level: ${overview.risk_level || "unknown"}`],
    ["Blocked Actions", overview.blocked_actions ?? "0", "Policy decisions stopped before execution"],
    ["Approval Gates", overview.approval_required_actions ?? "0", "Actions requiring human approval"],
    ["Risk Findings", overview.risk_findings ?? "0", `Evidence: ${overview.evidence_confidence || "unknown"}`],
    ["Enterprise Controls", "Locked", `Kill switch: ${controlPlane.kill_switch || "requires_cavra_enterprise"}`]
  ];
  el("#aispmOverviewCards").innerHTML = overviewCards.map(([label, value, detail]) => `
    <article class="posture-card">
      <span>${escapeHtml(label)}</span>
      <strong>${escapeHtml(value)}</strong>
      <p>${escapeHtml(detail)}</p>
    </article>
  `).join("");
  el("#aispmAgentCards").innerHTML = (payload.agents || []).map((agent) => `
    <article class="posture-card">
      <span>${escapeHtml(agent.coverage_status || "unknown")}</span>
      <strong>${escapeHtml(agent.agent_id || "unknown-agent")}</strong>
      <p>${escapeHtml(agent.decision_count || 0)} decisions · ${escapeHtml(agent.blocked_actions || 0)} blocked · ${escapeHtml(agent.approval_required_actions || 0)} approvals</p>
      <p>Drift: <b>${escapeHtml(agent.drift_status || "unknown")}</b></p>
    </article>
  `).join("") || `<p class="empty-state">No local agent activity found. Sample or Enterprise ingestion is required.</p>`;
  el("#aispmFindings").innerHTML = (payload.findings || []).map((finding) => `
    <article class="finding-row">
      <span class="severity ${escapeHtml(finding.severity || "low")}">${escapeHtml(finding.severity || "low")}</span>
      <div>
        <strong>${escapeHtml(finding.risk_classification || "policy_violation")}</strong>
        <p>${escapeHtml(finding.reason || "Policy finding requires review.")}</p>
        <small>${escapeHtml(finding.agent_id || "unknown-agent")} · ${escapeHtml(finding.repository || "local")} · ${escapeHtml(finding.decision || "review")}</small>
      </div>
    </article>
  `).join("") || `<p class="empty-state">No findings in the current local activity window.</p>`;
  el("#aispmControlCoverage").innerHTML = (payload.control_coverage || []).map((control) => `
    <article class="posture-card">
      <span>${escapeHtml(control.coverage_status || "unknown")}</span>
      <strong>${escapeHtml(control.label || control.surface_id || "Control surface")}</strong>
      <p>${escapeHtml(control.description || "Observed local control activity.")}</p>
      <p>${escapeHtml(control.decision_count || 0)} decisions · ${escapeHtml(control.blocked_actions || 0)} blocked · ${escapeHtml(control.approval_required_actions || 0)} approvals</p>
      <p>Evidence: <b>${escapeHtml(control.evidence_confidence || "unknown")}</b></p>
    </article>
  `).join("") || `<p class="empty-state">No local control coverage data found.</p>`;
  el("#aispmNearMisses").innerHTML = (payload.near_misses || []).slice(0, 8).map((item) => `
    <article class="finding-row">
      <span class="severity ${escapeHtml(item.severity || "low")}">${escapeHtml(item.decision || "review")}</span>
      <div>
        <strong>${escapeHtml(item.operator_signal || "review_recommended")}</strong>
        <p>${escapeHtml(item.reason || "Near-miss event requires operator review.")}</p>
        <small>${escapeHtml(item.agent_id || "unknown-agent")} · ${escapeHtml(item.repository || "local")} · ${escapeHtml(item.surface_id || "general_policy")}</small>
      </div>
    </article>
  `).join("") || `<p class="empty-state">No near misses in the current local activity window.</p>`;
  el("#aispmTimeline").innerHTML = (payload.timeline || []).slice(0, 8).map((event) => `
    <div class="timeline-item">
      <h3>${escapeHtml(event.title || event.event_type || "timeline event")}</h3>
      <p>${escapeHtml(event.agent_id || "unknown-agent")} · ${escapeHtml(event.repository || "local")} · ${escapeHtml(event.outcome || "recorded")}</p>
    </div>
  `).join("") || `<p class="empty-state">No timeline events available.</p>`;
  el("#aispmPayload").textContent = JSON.stringify(payload, null, 2);
}

async function loadAispmDashboard() {
  const apiBase = (window.CAVRA_API_BASE || "").replace(/\/$/, "");
  if (!apiBase) {
    renderAispmDashboard(aispmFallback, "static sample");
    return;
  }
  try {
    const response = await fetch(`${apiBase}/aispm/posture`);
    if (!response.ok) throw new Error(`AISPM posture HTTP ${response.status}`);
    renderAispmDashboard(await response.json(), "API local activity");
  } catch (error) {
    renderAispmDashboard(aispmFallback, "API unavailable, sample shown");
  }
}

function renderIntegrations() {
  el("#integrationCards").innerHTML = integrations.map(([name, capability, status]) => `
    <article class="integration-card">
      <span>${status}</span>
      <h3>${name}</h3>
      <p>${capability}</p>
      <a href="#documentation" data-route-link="documentation">Documentation</a>
    </article>
  `).join("");
}

function renderCompliance() {
  const query = el("#complianceFilter").value.trim().toLowerCase();
  const framework = el("#complianceFramework").value;
  const rows = complianceRows.filter((row) => {
    const textMatch = row.join(" ").toLowerCase().includes(query);
    const frameworkMatch = framework === "all" || row[0] === framework;
    return textMatch && frameworkMatch;
  });
  el("#complianceRows").innerHTML = rows.map(([frameworkName, control, policy, evidence, status]) => `
    <tr>
      <td>${frameworkName}: ${control}</td>
      <td>${policy}</td>
      <td>${evidence}</td>
      <td><span class="severity low">${status}</span></td>
    </tr>
  `).join("");
}

function renderUseCases() {
  el("#useCaseCards").innerHTML = useCases.map(([title, detail]) => `
    <article class="usecase-card"><h3>${title}</h3><p>${detail}</p><button data-route="architecture">View flow</button></article>
  `).join("");
}

function renderOperatorPaths() {
  el("#operatorPathCards").innerHTML = operatorPaths.map(([persona, question, path, evidence]) => `
    <article class="operator-path-card">
      <span>${persona}</span>
      <h3>${question}</h3>
      <dl>
        <dt>Inspect</dt><dd>${path}</dd>
        <dt>Verify</dt><dd>${evidence}</dd>
      </dl>
      <button data-route="documentation">Open docs</button>
    </article>
  `).join("");
}

function renderTrialAccess() {
  el("#trialAccessCards").innerHTML = trialAccessCards.map(([label, value, detail]) => `
    <article class="trial-access-card">
      <span>${label}</span>
      <strong>${value}</strong>
      <p>${detail}</p>
    </article>
  `).join("");
}

function renderDocs() {
  el("#docsNav").innerHTML = docsLinks.map(([label, path]) => `
    <a href="https://github.com/Huzefaaa2/cavra/blob/main/${path}" target="_blank" rel="noreferrer">${label}<span>${path}</span></a>
  `).join("");
}

function renderRoadmap() {
  el("#roadmapBoard").innerHTML = roadmap.map(([column, items]) => `
    <section class="roadmap-column">
      <h3>${column}</h3>
      <ol>${items.map((item) => `<li>${item}</li>`).join("")}</ol>
    </section>
  `).join("");
}

function openCommandPalette() {
  el("#commandPalette").classList.add("is-open");
  el("#commandPalette").setAttribute("aria-hidden", "false");
  el("#commandSearch").focus();
  renderCommandResults("");
}

function closeCommandPalette() {
  el("#commandPalette").classList.remove("is-open");
  el("#commandPalette").setAttribute("aria-hidden", "true");
}

function renderCommandResults(query) {
  const normalized = query.trim().toLowerCase();
  const results = routeContent.filter((item) => {
    const haystack = `${item.type} ${item.label} ${item.description}`.toLowerCase();
    return !normalized || haystack.includes(normalized);
  }).slice(0, 16);
  el("#commandResults").innerHTML = results.map((item) => `
    <button class="command-result" data-route="${item.route}">
      ${item.label}
      <span>${item.type} - ${item.description}</span>
    </button>
  `).join("");
}

function runScenario() {
  const payload = {
    scenario: "before-the-agent-acts",
    decision: "block",
    reason: "Autonomous production-impacting infrastructure changes require approval.",
    evidence: "PR attestation, policy decision, and audit bundle generated.",
    timestamp: new Date().toISOString()
  };
  el("#scenarioStatus").textContent = "Scenario complete: one high-risk action blocked and evidence generated.";
  el("#evidencePayload").textContent = JSON.stringify(payload, null, 2);
  setRoute("evidence");
}

function normalizeTheme(theme) {
  if (theme === "light") return "classic";
  if (theme === "dark") return "sentinel";
  return themes[theme] ? theme : "sentinel";
}

function applyTheme(theme) {
  const normalized = normalizeTheme(theme);
  document.body.dataset.theme = normalized;
  document.querySelectorAll("[data-theme-select]").forEach((picker) => {
    picker.value = normalized;
  });
  localStorage.setItem("cavra.theme", normalized);
}

function wireEvents() {
  document.addEventListener("click", async (event) => {
    const target = event.target.closest("[data-route], [data-route-link]");
    if (target?.dataset.route || target?.dataset.routeLink) {
      event.preventDefault();
      setRoute(target.dataset.route || target.dataset.routeLink);
      el("#mobileDrawer").classList.remove("is-open");
      closeCommandPalette();
      return;
    }
    const nodeButton = event.target.closest("[data-node]");
    if (nodeButton) {
      renderArchitecture(nodeButton.dataset.node);
      return;
    }
  });
  el("#openSearch").addEventListener("click", openCommandPalette);
  el("#mobileSearch").addEventListener("click", openCommandPalette);
  el("#closeSearch").addEventListener("click", closeCommandPalette);
  el("#commandSearch").addEventListener("input", (event) => renderCommandResults(event.target.value));
  el("#commandPalette").addEventListener("click", (event) => {
    if (event.target === el("#commandPalette")) closeCommandPalette();
  });
  document.addEventListener("keydown", (event) => {
    if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "k") {
      event.preventDefault();
      openCommandPalette();
    }
    if (event.key === "Escape") closeCommandPalette();
  });
  el("#collapseSidebar").addEventListener("click", () => {
    el("#sidebar").classList.toggle("is-collapsed");
    localStorage.setItem("cavra.sidebarCollapsed", String(el("#sidebar").classList.contains("is-collapsed")));
  });
  el("#openMobileNav").addEventListener("click", () => el("#mobileDrawer").classList.add("is-open"));
  el("#closeMobileNav").addEventListener("click", () => el("#mobileDrawer").classList.remove("is-open"));
  document.querySelectorAll("[data-theme-select]").forEach((picker) => {
    picker.addEventListener("change", (event) => applyTheme(event.target.value));
  });
  el("#runScenario").addEventListener("click", runScenario);
  el("#refreshAispm").addEventListener("click", loadAispmDashboard);
  el("#refreshCommunityGa").addEventListener("click", renderMetrics);
  el("#savePilotIntake").addEventListener("click", () => {
    el("#scenarioStatus").textContent = "Pilot intake snapshot saved locally for this static demo.";
  });
  el("#copyInstall").addEventListener("click", async () => {
    await navigator.clipboard?.writeText("claude mcp add cavra -- cavra-mcp-server");
    el("#scenarioStatus").textContent = "Install command copied.";
  });
  el("#complianceFilter").addEventListener("input", renderCompliance);
  el("#complianceFramework").addEventListener("change", renderCompliance);
  document.querySelectorAll(".copy-code").forEach((button) => {
    button.addEventListener("click", async () => navigator.clipboard?.writeText(button.dataset.copy));
  });
}

function init() {
  applyTheme(localStorage.getItem("cavra.theme") || "sentinel");
  renderNav(el("#portalNav"));
  renderNav(el("#mobileNav"));
  renderMetrics();
  renderArchitecture();
  renderPolicies();
  renderEvidence();
  renderAispmDashboard(aispmFallback, "static sample");
  renderIntegrations();
  renderCompliance();
  renderUseCases();
  renderOperatorPaths();
  renderTrialAccess();
  renderDocs();
  renderRoadmap();
  wireEvents();
  loadAispmDashboard();
  if (localStorage.getItem("cavra.sidebarCollapsed") === "true") el("#sidebar").classList.add("is-collapsed");
  setRoute(location.hash.slice(1) || localStorage.getItem("cavra.activeRoute") || "dashboard");
}

init();
