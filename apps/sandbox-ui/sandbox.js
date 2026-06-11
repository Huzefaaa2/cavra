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

let currentAispmReplayPolicyTestsExport = null;
let currentAispmReplayPolicyDraftPacket = null;
let currentAispmReplayPolicyTestsPacket = null;
let currentAispmReplayPolicyReviewPacket = null;
let currentAispmReplayPolicyPrApprovalText = "";
let currentAispmReplayPolicyCiGateReadiness = null;
let currentAispmReplayPolicyCiGateRolloutMarkdown = "";
let currentAispmReplayPolicyCiGateAuditPacket = null;

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
  control_coverage_heatmap: {
    coverage_score: 18,
    surfaces: [
      { surface_id: "sensitive_data", label: "Sensitive Data", description: "Secrets, credentials, customer data, and protected files." },
      { surface_id: "infrastructure_iac", label: "Infrastructure", description: "Cloud, IaC, Kubernetes, and production infrastructure actions." },
      { surface_id: "mcp_tools", label: "MCP Tools", description: "External tools, MCP servers, filesystem, browser, and automation actions." },
      { surface_id: "source_control", label: "Source Control", description: "Git, branch, commit, PR, and repository mutation actions." },
      { surface_id: "runtime_commands", label: "Runtime", description: "Shell commands, scripts, package operations, and local execution." },
      { surface_id: "general_policy", label: "General", description: "Policy decisions that do not map to a more specific surface." }
    ],
    rows: [
      {
        row_id: "coverage-codex-agent-payments-api",
        agent_id: "codex-agent",
        repository: "payments/api",
        policy_packs: ["cavra-ai-agent-baseline", "cloud-iam-prod"],
        decision_count: 2,
        cells: [
          { surface_id: "sensitive_data", label: "Sensitive Data", coverage_status: "enforced", coverage_score: 100, decision_count: 1, blocked_actions: 1, approval_required_actions: 0, warned_actions: 0, evidence_confidence: "activity_evidence_refs", evidence_refs: ["sample://evidence/secret-read-block"], recommended_action: "Keep block enforcement and evidence capture active for sensitive data." },
          { surface_id: "infrastructure_iac", label: "Infrastructure", coverage_status: "approval_gated", coverage_score: 82, decision_count: 1, blocked_actions: 0, approval_required_actions: 1, warned_actions: 0, evidence_confidence: "activity_evidence_refs", evidence_refs: ["sample://evidence/iac-production-change"], recommended_action: "Validate approval routing and evidence freshness for infrastructure." },
          { surface_id: "mcp_tools", label: "MCP Tools", coverage_status: "not_observed_locally", coverage_score: 0, decision_count: 0, blocked_actions: 0, approval_required_actions: 0, warned_actions: 0, evidence_confidence: "no_local_activity", evidence_refs: [], recommended_action: "Add CAVRA policy coverage or test evidence for MCP tools." },
          { surface_id: "source_control", label: "Source Control", coverage_status: "not_observed_locally", coverage_score: 0, decision_count: 0, blocked_actions: 0, approval_required_actions: 0, warned_actions: 0, evidence_confidence: "no_local_activity", evidence_refs: [], recommended_action: "Add CAVRA policy coverage or test evidence for source control." },
          { surface_id: "runtime_commands", label: "Runtime", coverage_status: "not_observed_locally", coverage_score: 0, decision_count: 0, blocked_actions: 0, approval_required_actions: 0, warned_actions: 0, evidence_confidence: "no_local_activity", evidence_refs: [], recommended_action: "Add CAVRA policy coverage or test evidence for runtime commands." },
          { surface_id: "general_policy", label: "General", coverage_status: "not_observed_locally", coverage_score: 0, decision_count: 0, blocked_actions: 0, approval_required_actions: 0, warned_actions: 0, evidence_confidence: "no_local_activity", evidence_refs: [], recommended_action: "Add CAVRA policy coverage or test evidence for general policy." }
        ]
      },
      {
        row_id: "coverage-claude-code-agent-platform-infra",
        agent_id: "claude-code-agent",
        repository: "platform/infra",
        policy_packs: ["mcp-enterprise"],
        decision_count: 1,
        cells: [
          { surface_id: "sensitive_data", label: "Sensitive Data", coverage_status: "not_observed_locally", coverage_score: 0, decision_count: 0, blocked_actions: 0, approval_required_actions: 0, warned_actions: 0, evidence_confidence: "no_local_activity", evidence_refs: [], recommended_action: "Add CAVRA policy coverage or test evidence for sensitive data." },
          { surface_id: "infrastructure_iac", label: "Infrastructure", coverage_status: "not_observed_locally", coverage_score: 0, decision_count: 0, blocked_actions: 0, approval_required_actions: 0, warned_actions: 0, evidence_confidence: "no_local_activity", evidence_refs: [], recommended_action: "Add CAVRA policy coverage or test evidence for infrastructure." },
          { surface_id: "mcp_tools", label: "MCP Tools", coverage_status: "warning_only", coverage_score: 38, decision_count: 1, blocked_actions: 0, approval_required_actions: 0, warned_actions: 1, evidence_confidence: "activity_evidence_refs", evidence_refs: ["sample://evidence/mcp-warning"], recommended_action: "Move MCP tools from warning-only visibility to block, approval, or attestation controls where risk justifies it." },
          { surface_id: "source_control", label: "Source Control", coverage_status: "not_observed_locally", coverage_score: 0, decision_count: 0, blocked_actions: 0, approval_required_actions: 0, warned_actions: 0, evidence_confidence: "no_local_activity", evidence_refs: [], recommended_action: "Add CAVRA policy coverage or test evidence for source control." },
          { surface_id: "runtime_commands", label: "Runtime", coverage_status: "not_observed_locally", coverage_score: 0, decision_count: 0, blocked_actions: 0, approval_required_actions: 0, warned_actions: 0, evidence_confidence: "no_local_activity", evidence_refs: [], recommended_action: "Add CAVRA policy coverage or test evidence for runtime commands." },
          { surface_id: "general_policy", label: "General", coverage_status: "not_observed_locally", coverage_score: 0, decision_count: 0, blocked_actions: 0, approval_required_actions: 0, warned_actions: 0, evidence_confidence: "no_local_activity", evidence_refs: [], recommended_action: "Add CAVRA policy coverage or test evidence for general policy." }
        ]
      }
    ],
    top_gaps: [
      { gap_id: "coverage-gap-codex-agent-payments-api-mcp-tools", agent_id: "codex-agent", repository: "payments/api", surface_id: "mcp_tools", label: "MCP Tools", coverage_status: "not_observed_locally", recommended_action: "Add CAVRA policy coverage or test evidence for MCP tools.", evidence_confidence: "no_local_activity" },
      { gap_id: "coverage-gap-claude-code-agent-platform-infra-mcp-tools", agent_id: "claude-code-agent", repository: "platform/infra", surface_id: "mcp_tools", label: "MCP Tools", coverage_status: "warning_only", recommended_action: "Move MCP tools from warning-only visibility to block, approval, or attestation controls where risk justifies it.", evidence_confidence: "activity_evidence_refs" }
    ]
  },
  evidence_confidence_drilldown: {
    summary: {
      total_facts: 3,
      signed_evidence_items: 0,
      activity_evidence_items: 0,
      sample_evidence_items: 3,
      metadata_only_items: 0,
      missing_evidence_items: 0,
      evidence_score: 45,
      lowest_confidence_level: "sample_evidence_refs",
      highest_confidence_level: "sample_evidence_refs"
    },
    facts: [
      { fact_id: "evidence-sample-dec-001", fact_type: "policy_decision", source_id: "sample-dec-001", session_id: "sample-session-001", agent_id: "codex-agent", repository: "payments/api", policy_pack: "cloud-iam-prod", control_surface: "infrastructure_iac", decision: "require_approval", severity: "high", confidence_level: "sample_evidence_refs", confidence_score: 45, evidence_count: 1, signed_evidence_count: 0, evidence_refs: ["sample://evidence/iac-production-change"], metadata_fields: ["decision_id", "session_id", "agent_id", "repository", "policy_pack", "rule_id", "action_type", "target", "timestamp"], recommended_action: "Replace sample evidence with local or signed evidence before production evaluation.", timestamp: "2026-06-09T00:00:00+00:00" },
      { fact_id: "evidence-sample-dec-002", fact_type: "policy_decision", source_id: "sample-dec-002", session_id: "sample-session-001", agent_id: "codex-agent", repository: "payments/api", policy_pack: "cavra-ai-agent-baseline", control_surface: "sensitive_data", decision: "block", severity: "critical", confidence_level: "sample_evidence_refs", confidence_score: 45, evidence_count: 1, signed_evidence_count: 0, evidence_refs: ["sample://evidence/secret-read-block"], metadata_fields: ["decision_id", "session_id", "agent_id", "repository", "policy_pack", "rule_id", "action_type", "target", "timestamp"], recommended_action: "Replace sample evidence with local or signed evidence before production evaluation.", timestamp: "2026-06-09T00:01:00+00:00" },
      { fact_id: "evidence-sample-dec-003", fact_type: "policy_decision", source_id: "sample-dec-003", session_id: "sample-session-002", agent_id: "claude-code-agent", repository: "platform/infra", policy_pack: "mcp-enterprise", control_surface: "mcp_tools", decision: "warn", severity: "medium", confidence_level: "sample_evidence_refs", confidence_score: 45, evidence_count: 1, signed_evidence_count: 0, evidence_refs: ["sample://evidence/mcp-warning"], metadata_fields: ["decision_id", "session_id", "agent_id", "repository", "policy_pack", "rule_id", "action_type", "target", "timestamp"], recommended_action: "Replace sample evidence with local or signed evidence before production evaluation.", timestamp: "2026-06-09T00:02:00+00:00" }
    ]
  },
  evidence_freshness_slo: {
    slo_policy: {
      fresh_hours: 24,
      review_soon_hours: 168,
      retention_reference_patterns: ["archive://", "immutable://", "s3://", "gs://", "azblob://"],
      community_boundary: "metadata_only"
    },
    summary: {
      total_items: 3,
      fresh_items: 3,
      review_soon_items: 0,
      stale_items: 0,
      missing_timestamp_items: 0,
      retention_ready_items: 0,
      sample_retention_items: 3,
      retention_gap_items: 0,
      slo_met_items: 0,
      slo_monitor_items: 3,
      slo_breached_items: 0,
      freshness_score: 100,
      retention_score: 45,
      oldest_age_hours: 3,
      evidence_confidence: "sample_evidence_refs"
    },
    items: [
      { item_id: "freshness-sample-dec-001", item_type: "policy_decision", source_id: "sample-dec-001", session_id: "sample-session-001", agent_id: "codex-agent", repository: "payments/api", policy_pack: "cloud-iam-prod", control_surface: "infrastructure_iac", severity: "high", decision: "require_approval", observed_at: "2026-06-09T00:00:00+00:00", age_hours: 3, freshness_status: "fresh", retention_status: "sample_reference", slo_status: "monitor", evidence_refs: ["sample://evidence/iac-production-change"], recommended_action: "Replace sample evidence with retained local or signed evidence before production reliance." },
      { item_id: "freshness-sample-dec-002", item_type: "policy_decision", source_id: "sample-dec-002", session_id: "sample-session-001", agent_id: "codex-agent", repository: "payments/api", policy_pack: "cavra-ai-agent-baseline", control_surface: "sensitive_data", severity: "critical", decision: "block", observed_at: "2026-06-09T00:01:00+00:00", age_hours: 2, freshness_status: "fresh", retention_status: "sample_reference", slo_status: "monitor", evidence_refs: ["sample://evidence/secret-read-block"], recommended_action: "Replace sample evidence with retained local or signed evidence before production reliance." },
      { item_id: "freshness-sample-dec-003", item_type: "policy_decision", source_id: "sample-dec-003", session_id: "sample-session-002", agent_id: "claude-code-agent", repository: "platform/infra", policy_pack: "mcp-enterprise", control_surface: "mcp_tools", severity: "medium", decision: "warn", observed_at: "2026-06-09T00:02:00+00:00", age_hours: 1, freshness_status: "fresh", retention_status: "sample_reference", slo_status: "monitor", evidence_refs: ["sample://evidence/mcp-warning"], recommended_action: "Replace sample evidence with retained local or signed evidence before production reliance." }
    ]
  },
  executive_risk_narrative: {
    report_id: "aispm-executive-risk-narrative-community",
    narrative_type: "deterministic_public_safe_summary",
    audience: ["CSO", "CISO", "security leadership", "platform leadership"],
    time_window: "local_activity_window",
    headline: "CAVRA Community reports critical AI-agent posture from 3 local decisions, including 1 blocked action and 1 approval-gated action, with 0 evidence SLO breaches requiring operator review.",
    risk_level: "critical",
    posture_score: 12,
    key_metrics: {
      total_sessions: 2,
      total_decisions: 3,
      blocked_actions: 1,
      approval_required_actions: 1,
      risk_findings: 3,
      evidence_slo_breaches: 0,
      evidence_retention_gaps: 0,
      freshness_score: 100,
      retention_score: 45
    },
    sections: [
      { section_id: "executive-summary", title: "Executive Summary", body: "CAVRA Community reports critical AI-agent posture from 3 local decisions, including 1 blocked action and 1 approval-gated action, with 0 evidence SLO breaches requiring operator review." },
      { section_id: "risk-posture", title: "Risk Posture", body: "CAVRA observed 3 local policy decisions across 2 agent identities. The current Community posture score is 12/100 with a critical risk level." },
      { section_id: "evidence-readiness", title: "Evidence Readiness", body: "Evidence freshness has 0 breached SLO items, 3 items to monitor, and 0 retention gaps. Community validates local timestamps and reference patterns only." },
      { section_id: "operator-focus", title: "Operator Focus", body: "Focus on the highest-risk agent actions, close evidence gaps, and keep Enterprise-only live controls scoped for the next paid or trial deployment." }
    ],
    top_risks: [
      { risk_id: "finding-sample-dec-002", title: "Credential Or Sensitive Data Exposure", severity: "critical", agent_id: "codex-agent", repository: "payments/api", reason: "Sensitive production secret file access is blocked.", evidence_refs: ["sample://evidence/secret-read-block"] },
      { risk_id: "finding-sample-dec-001", title: "Infrastructure Change Risk", severity: "high", agent_id: "codex-agent", repository: "payments/api", reason: "Production-impacting infrastructure action requires approval.", evidence_refs: ["sample://evidence/iac-production-change"] }
    ],
    recommended_actions: [
      { action_id: "review-top-ai-agent-risks", priority: "high", owner: "security leadership", action: "Review the top AI-agent risks and confirm owners for remediation." },
      { action_id: "validate-approval-latency", priority: "medium", owner: "platform leadership", action: "Validate approval routes and latency for approval-gated AI-agent actions." },
      { action_id: "plan-enterprise-live-posture", priority: "medium", owner: "security architecture", action: "Plan Enterprise live ingestion for prompts, tool calls, trace history, trend reporting, and runtime controls." }
    ],
    evidence_refs: ["sample://evidence/iac-production-change", "sample://evidence/secret-read-block", "sample://evidence/mcp-warning"],
    limitations: [
      "Community narrative is deterministic and based on local/sample metadata only.",
      "Raw prompts, model reasoning, customer impact, trend history, and tenant benchmarks require CAVRA Enterprise."
    ]
  },
  near_misses: [
    { near_miss_id: "near-miss-sample-dec-001", decision_id: "sample-dec-001", session_id: "sample-session-001", agent_id: "codex-agent", repository: "payments/api", surface_id: "infrastructure_iac", severity: "high", decision: "require_approval", risk_classification: "infrastructure_change_risk", reason: "Production-impacting infrastructure action requires approval.", operator_signal: "approval_prevented_unreviewed_execution", evidence_refs: ["sample://evidence/iac-production-change"], timestamp: "2026-06-09T00:00:00+00:00" },
    { near_miss_id: "near-miss-sample-dec-003", decision_id: "sample-dec-003", session_id: "sample-session-002", agent_id: "claude-code-agent", repository: "platform/infra", surface_id: "mcp_tools", severity: "medium", decision: "warn", risk_classification: "tool_or_mcp_governance_risk", reason: "MCP tool requires registration before broad rollout.", operator_signal: "warning_allowed_with_operator_visibility", evidence_refs: ["sample://evidence/mcp-warning"], timestamp: "2026-06-09T00:02:00+00:00" }
  ],
  pre_action_risk_forecasts: [
    {
      forecast_id: "forecast-sample-dec-002",
      decision_id: "sample-dec-002",
      session_id: "sample-session-001",
      agent_id: "codex-agent",
      repository: "payments/api",
      policy_pack: "cavra-ai-agent-baseline",
      rule_id: "secrets.block-sensitive-read",
      action_type: "read_file",
      target_summary: "sensitive target redacted",
      target_redacted: true,
      decision: "block",
      severity: "critical",
      risk_classification: "credential_or_sensitive_data_exposure",
      control_surface: "sensitive_data",
      forecast_status: "block_recommended",
      projected_blast_radius: "secret_scope",
      likely_impacts: ["credential_or_sensitive_data_exposure", "data_exfiltration", "audit_scope_expansion"],
      pre_action_controls: ["block_before_execution", "require_operator_review", "capture_evidence", "redact_sensitive_target"],
      confidence: "metadata_forecast",
      evidence_refs: ["sample://evidence/secret-read-block"],
      timestamp: "2026-06-09T00:01:00+00:00"
    },
    {
      forecast_id: "forecast-sample-dec-001",
      decision_id: "sample-dec-001",
      session_id: "sample-session-001",
      agent_id: "codex-agent",
      repository: "payments/api",
      policy_pack: "cloud-iam-prod",
      rule_id: "iac.production-change",
      action_type: "execute_command",
      target_summary: "terraform apply",
      target_redacted: false,
      decision: "require_approval",
      severity: "high",
      risk_classification: "infrastructure_change_risk",
      control_surface: "infrastructure_iac",
      forecast_status: "approval_recommended",
      projected_blast_radius: "production_infrastructure",
      likely_impacts: ["production_infrastructure_change", "configuration_drift", "service_availability_impact"],
      pre_action_controls: ["require_human_approval", "verify_change_window", "attach_evidence", "require_blast_radius_context"],
      confidence: "metadata_forecast",
      evidence_refs: ["sample://evidence/iac-production-change"],
      timestamp: "2026-06-09T00:00:00+00:00"
    },
    {
      forecast_id: "forecast-sample-dec-003",
      decision_id: "sample-dec-003",
      session_id: "sample-session-002",
      agent_id: "claude-code-agent",
      repository: "platform/infra",
      policy_pack: "mcp-enterprise",
      rule_id: "mcp.untrusted-tool",
      action_type: "mcp_tool_call",
      target_summary: "filesystem.write",
      target_redacted: false,
      decision: "warn",
      severity: "medium",
      risk_classification: "tool_or_mcp_governance_risk",
      control_surface: "mcp_tools",
      forecast_status: "warn_recommended",
      projected_blast_radius: "tooling_surface",
      likely_impacts: ["untrusted_tool_write_access", "workspace_mutation", "toolchain_expansion"],
      pre_action_controls: ["warn_operator", "require_attestation", "monitor_follow_up", "verify_tool_trust_tier"],
      confidence: "metadata_forecast",
      evidence_refs: ["sample://evidence/mcp-warning"],
      timestamp: "2026-06-09T00:02:00+00:00"
    }
  ],
  intent_action_drift: [
    {
      drift_id: "intent-drift-sample-dec-002",
      decision_id: "sample-dec-002",
      session_id: "sample-session-001",
      agent_id: "codex-agent",
      repository: "payments/api",
      policy_pack: "cavra-ai-agent-baseline",
      rule_id: "secrets.block-sensitive-read",
      declared_intent: "Inspect deployment configuration",
      action_type: "read_file",
      target_summary: "sensitive target redacted",
      target_redacted: true,
      decision: "block",
      severity: "critical",
      risk_classification: "credential_or_sensitive_data_exposure",
      control_surface: "sensitive_data",
      drift_status: "high_drift",
      drift_score: 81,
      drift_signals: ["sensitive_target_not_declared", "blocked_after_declared_intent", "critical_or_high_intent_drift", "action_type_not_explicit_in_intent"],
      recommended_action: "Block or escalate until the declared intent explicitly covers sensitive-data access.",
      confidence: "metadata_intent_comparison",
      evidence_refs: ["sample://evidence/secret-read-block"],
      timestamp: "2026-06-09T00:01:00+00:00"
    },
    {
      drift_id: "intent-drift-sample-dec-001",
      decision_id: "sample-dec-001",
      session_id: "sample-session-001",
      agent_id: "codex-agent",
      repository: "payments/api",
      policy_pack: "cloud-iam-prod",
      rule_id: "iac.production-change",
      declared_intent: "Apply approved production infrastructure change",
      action_type: "execute_command",
      target_summary: "terraform apply",
      target_redacted: false,
      decision: "require_approval",
      severity: "high",
      risk_classification: "infrastructure_change_risk",
      control_surface: "infrastructure_iac",
      drift_status: "needs_review",
      drift_score: 35,
      drift_signals: ["approval_required_after_declared_intent", "critical_or_high_intent_drift", "action_type_not_explicit_in_intent"],
      recommended_action: "Verify the requested change, blast radius, approval route, and execution target before allowing the action.",
      confidence: "metadata_intent_comparison",
      evidence_refs: ["sample://evidence/iac-production-change"],
      timestamp: "2026-06-09T00:00:00+00:00"
    },
    {
      drift_id: "intent-drift-sample-dec-003",
      decision_id: "sample-dec-003",
      session_id: "sample-session-002",
      agent_id: "claude-code-agent",
      repository: "platform/infra",
      policy_pack: "mcp-enterprise",
      rule_id: "mcp.untrusted-tool",
      declared_intent: "Write generated infrastructure documentation",
      action_type: "mcp_tool_call",
      target_summary: "filesystem.write",
      target_redacted: false,
      decision: "warn",
      severity: "medium",
      risk_classification: "tool_or_mcp_governance_risk",
      control_surface: "mcp_tools",
      drift_status: "aligned",
      drift_score: 6,
      drift_signals: ["action_type_not_explicit_in_intent"],
      recommended_action: "Verify tool trust tier, write scope, and declared workflow intent before allowing broad tool use.",
      confidence: "metadata_intent_comparison",
      evidence_refs: ["sample://evidence/mcp-warning"],
      timestamp: "2026-06-09T00:02:00+00:00"
    }
  ],
  tool_chain_graph: {
    nodes: [
      { node_id: "agent-codex-agent", node_type: "agent", label: "codex-agent", risk_band: "low", risk_score: 5, decision_count: 2, metadata: { repository: "payments/api" } },
      { node_id: "agent-claude-code-agent", node_type: "agent", label: "claude-code-agent", risk_band: "observed", risk_score: 5, decision_count: 1, metadata: { repository: "platform/infra" } },
      { node_id: "tool-filesystem", node_type: "tool", label: "filesystem", risk_band: "critical", risk_score: 85, decision_count: 1, metadata: { control_surface: "sensitive_data", tool_capability: "file_read" } },
      { node_id: "tool-shell", node_type: "tool", label: "shell", risk_band: "high", risk_score: 62, decision_count: 1, metadata: { control_surface: "infrastructure_iac", tool_capability: "runtime_execution" } },
      { node_id: "tool-filesystem-write", node_type: "tool", label: "filesystem.write", risk_band: "medium", risk_score: 38, decision_count: 1, metadata: { control_surface: "mcp_tools", tool_capability: "workspace_write" } },
      { node_id: "target-sensitive-data-sensitive-target-redacted", node_type: "target", label: "sensitive target redacted", risk_band: "critical", risk_score: 85, decision_count: 1, metadata: { control_surface: "sensitive_data", target_redacted: true } },
      { node_id: "target-infrastructure-iac-terraform-apply", node_type: "target", label: "terraform apply", risk_band: "high", risk_score: 62, decision_count: 1, metadata: { control_surface: "infrastructure_iac", target_redacted: false } },
      { node_id: "policy-cavra-ai-agent-baseline", node_type: "policy", label: "cavra-ai-agent-baseline", risk_band: "observed", risk_score: 5, decision_count: 1, metadata: { rule_id: "secrets.block-sensitive-read" } }
    ],
    edges: [
      { edge_id: "tool-edge-sample-dec-002-agent-tool", source: "agent-codex-agent", target: "tool-filesystem", relationship: "invoked_tool", decision_id: "sample-dec-002", session_id: "sample-session-001", agent_id: "codex-agent", repository: "payments/api", action_type: "read_file", decision: "block", severity: "critical", risk_classification: "credential_or_sensitive_data_exposure", control_surface: "sensitive_data", risk_score: 98, risk_band: "critical", evidence_refs: ["sample://evidence/secret-read-block"], timestamp: "2026-06-09T00:01:00+00:00" },
      { edge_id: "tool-edge-sample-dec-002-tool-target", source: "tool-filesystem", target: "target-sensitive-data-sensitive-target-redacted", relationship: "requested_target", target_redacted: true, decision_id: "sample-dec-002", session_id: "sample-session-001", agent_id: "codex-agent", repository: "payments/api", action_type: "read_file", decision: "block", severity: "critical", risk_classification: "credential_or_sensitive_data_exposure", control_surface: "sensitive_data", risk_score: 98, risk_band: "critical", evidence_refs: ["sample://evidence/secret-read-block"], timestamp: "2026-06-09T00:01:00+00:00" },
      { edge_id: "tool-edge-sample-dec-001-agent-tool", source: "agent-codex-agent", target: "tool-shell", relationship: "invoked_tool", decision_id: "sample-dec-001", session_id: "sample-session-001", agent_id: "codex-agent", repository: "payments/api", action_type: "execute_command", decision: "require_approval", severity: "high", risk_classification: "infrastructure_change_risk", control_surface: "infrastructure_iac", risk_score: 52, risk_band: "high", evidence_refs: ["sample://evidence/iac-production-change"], timestamp: "2026-06-09T00:00:00+00:00" },
      { edge_id: "tool-edge-sample-dec-003-agent-tool", source: "agent-claude-code-agent", target: "tool-filesystem-write", relationship: "invoked_tool", decision_id: "sample-dec-003", session_id: "sample-session-002", agent_id: "claude-code-agent", repository: "platform/infra", action_type: "mcp_tool_call", decision: "warn", severity: "medium", risk_classification: "tool_or_mcp_governance_risk", control_surface: "mcp_tools", risk_score: 32, risk_band: "medium", evidence_refs: ["sample://evidence/mcp-warning"], timestamp: "2026-06-09T00:02:00+00:00" }
    ],
    hotspots: [
      { hotspot_id: "hotspot-codex-agent-payments-api", agent_id: "codex-agent", repository: "payments/api", decision_count: 2, blocked_edges: 1, approval_required_edges: 1, warned_edges: 0, dominant_surface: "sensitive_data", risk_score: 98, risk_band: "critical", evidence_refs: ["sample://evidence/iac-production-change", "sample://evidence/secret-read-block"] },
      { hotspot_id: "hotspot-claude-code-agent-platform-infra", agent_id: "claude-code-agent", repository: "platform/infra", decision_count: 1, blocked_edges: 0, approval_required_edges: 0, warned_edges: 1, dominant_surface: "mcp_tools", risk_score: 32, risk_band: "medium", evidence_refs: ["sample://evidence/mcp-warning"] }
    ]
  },
  agent_blast_radius: [
    {
      agent_id: "codex-agent",
      blast_radius_level: "high",
      blast_radius_score: 71,
      repository_count: 1,
      repositories: ["payments/api"],
      control_surfaces: ["infrastructure_iac", "sensitive_data"],
      policy_packs: ["cavra-ai-agent-baseline", "cloud-iam-prod"],
      tool_labels: ["filesystem", "shell"],
      target_classes: ["production_infrastructure", "sensitive_data:redacted"],
      sensitive_target_count: 1,
      production_infrastructure_count: 1,
      approval_paths: ["approval_required_unassigned"],
      decision_count: 2,
      session_count: 1,
      blocked_actions: 1,
      approval_required_actions: 1,
      warned_actions: 0,
      top_risks: ["sensitive_data_reach", "production_infrastructure_reach", "blocked_action_history", "approval_gated_actions"],
      recommended_controls: ["capture_signed_evidence", "review_agent_scope", "keep_block_enforcement_enabled", "bind_explicit_approval_route", "redact_sensitive_targets", "require_blast_radius_context"],
      evidence_refs: ["sample://evidence/iac-production-change", "sample://evidence/secret-read-block"],
      last_seen_at: "2026-06-09T00:01:30+00:00"
    },
    {
      agent_id: "claude-code-agent",
      blast_radius_level: "low",
      blast_radius_score: 10,
      repository_count: 1,
      repositories: ["platform/infra"],
      control_surfaces: ["mcp_tools"],
      policy_packs: ["mcp-enterprise"],
      tool_labels: ["filesystem.write"],
      target_classes: ["local_workspace"],
      sensitive_target_count: 0,
      production_infrastructure_count: 0,
      approval_paths: [],
      decision_count: 1,
      session_count: 1,
      blocked_actions: 0,
      approval_required_actions: 0,
      warned_actions: 1,
      top_risks: ["tooling_surface_reach"],
      recommended_controls: ["capture_signed_evidence", "review_agent_scope", "verify_tool_trust_tier"],
      evidence_refs: ["sample://evidence/mcp-warning"],
      last_seen_at: "2026-06-09T00:02:30+00:00"
    }
  ],
  policy_context_gaps: [
    {
      gap_id: "context-gap-sample-dec-001",
      decision_id: "sample-dec-001",
      session_id: "sample-session-001",
      agent_id: "codex-agent",
      repository: "payments/api",
      policy_pack: "cloud-iam-prod",
      rule_id: "iac.production-change",
      action_type: "execute_command",
      decision: "require_approval",
      severity: "high",
      risk_classification: "infrastructure_change_risk",
      control_surface: "infrastructure_iac",
      missing_context: ["environment_tier", "system_criticality", "service_owner", "change_window", "blast_radius", "approval_route"],
      present_context: [],
      gap_status: "requires_context_review",
      recommended_action: "Attach service owner, change window, and blast-radius context before execution. Missing: environment_tier, system_criticality, service_owner, change_window, blast_radius, approval_route.",
      evidence_refs: ["sample://evidence/iac-production-change"],
      timestamp: "2026-06-09T00:00:00+00:00"
    },
    {
      gap_id: "context-gap-sample-dec-002",
      decision_id: "sample-dec-002",
      session_id: "sample-session-001",
      agent_id: "codex-agent",
      repository: "payments/api",
      policy_pack: "cavra-ai-agent-baseline",
      rule_id: "secrets.block-sensitive-read",
      action_type: "read_file",
      decision: "block",
      severity: "critical",
      risk_classification: "credential_or_sensitive_data_exposure",
      control_surface: "sensitive_data",
      missing_context: ["environment_tier", "system_criticality", "data_owner", "data_classification", "customer_region", "approval_route"],
      present_context: [],
      gap_status: "requires_context_review",
      recommended_action: "Attach data-owner, classification, and regional context before relying on the decision. Missing: environment_tier, system_criticality, data_owner, data_classification, customer_region, approval_route.",
      evidence_refs: ["sample://evidence/secret-read-block"],
      timestamp: "2026-06-09T00:01:00+00:00"
    },
    {
      gap_id: "context-gap-sample-dec-003",
      decision_id: "sample-dec-003",
      session_id: "sample-session-002",
      agent_id: "claude-code-agent",
      repository: "platform/infra",
      policy_pack: "mcp-enterprise",
      rule_id: "mcp.untrusted-tool",
      action_type: "mcp_tool_call",
      decision: "warn",
      severity: "medium",
      risk_classification: "tool_or_mcp_governance_risk",
      control_surface: "mcp_tools",
      missing_context: ["environment_tier", "system_criticality", "tool_owner", "tool_trust_tier"],
      present_context: ["business_justification"],
      gap_status: "requires_context_review",
      recommended_action: "Attach tool owner, trust tier, and business justification before broad tool use. Missing: environment_tier, system_criticality, tool_owner, tool_trust_tier.",
      evidence_refs: ["sample://evidence/mcp-warning"],
      timestamp: "2026-06-09T00:02:00+00:00"
    }
  ],
  behavior_fingerprints: [
    {
      fingerprint_id: "fingerprint-codex-agent",
      agent_id: "codex-agent",
      repositories: ["payments/api"],
      session_count: 1,
      decision_count: 2,
      action_profile: [{ name: "execute_command", count: 1 }, { name: "read_file", count: 1 }],
      decision_profile: [{ name: "require_approval", count: 1 }, { name: "block", count: 1 }],
      policy_packs: ["cavra-ai-agent-baseline", "cloud-iam-prod"],
      control_surfaces: ["infrastructure_iac", "sensitive_data"],
      risk_signals: ["blocked_action", "approval_gate", "critical_or_high_decision", "sensitive_data_access", "infrastructure_change", "multiple_policy_packs"],
      drift_status: "review_required",
      drift_score: 82,
      evidence_refs: ["sample://evidence/iac-production-change", "sample://evidence/secret-read-block"],
      last_seen_at: "2026-06-09T00:01:00+00:00"
    },
    {
      fingerprint_id: "fingerprint-claude-code-agent",
      agent_id: "claude-code-agent",
      repositories: ["platform/infra"],
      session_count: 1,
      decision_count: 1,
      action_profile: [{ name: "mcp_tool_call", count: 1 }],
      decision_profile: [{ name: "warn", count: 1 }],
      policy_packs: ["mcp-enterprise"],
      control_surfaces: ["mcp_tools"],
      risk_signals: ["warned_action", "mcp_or_tool_activity"],
      drift_status: "unusual_behavior",
      drift_score: 17,
      evidence_refs: ["sample://evidence/mcp-warning"],
      last_seen_at: "2026-06-09T00:02:00+00:00"
    }
  ],
  approval_lineage: [
    {
      lineage_id: "lineage-sample-apr-001",
      approval_id: "sample-apr-001",
      decision_id: "sample-dec-001",
      session_id: "sample-session-001",
      state: "approved",
      approver_group: "Cloud Security",
      requested_by: "automation:codex-agent",
      decided_by: "role:approver",
      requested_at: "2026-06-09T00:00:10+00:00",
      decided_at: "2026-06-09T00:00:40+00:00",
      external_ref: "ticket://sample-change-42",
      break_glass: false,
      decision: {
        action_type: "execute_command",
        target_summary: "terraform apply",
        risk_classification: "infrastructure_change_risk",
        control_surface: "infrastructure_iac",
        severity: "high",
        repository: "payments/api",
        policy_pack: "cloud-iam-prod",
        rule_id: "iac.production-change"
      },
      evidence_refs: ["approval://sample-apr-001", "sample://evidence/iac-production-change"],
      redacted_fields: ["identity_provider_claims", "raw_rbac_context", "connector_payloads"]
    }
  ],
  replay_to_policy_draft: {
    summary: {
      source_scope: "sample-session-001",
      source_decisions: 3,
      authorable_decisions: 3,
      recommended_rules: 3,
      draft_valid: true,
      source_sessions: ["sample-session-001", "sample-session-002"],
      source_repositories: ["payments/api", "platform/infra"],
      rule_counts: { filesystem: 1, commands: 1, git: 0, mcp: 1, approvals: 2, evidence: 3, compliance: 3 }
    },
    recommendations: [
      { recommendation_id: "policy-rec-1-sample-dec-001", decision_id: "sample-dec-001", session_id: "sample-session-001", agent_id: "codex-agent", repository: "payments/api", control_surface: "infrastructure_iac", risk_classification: "infrastructure_change_risk", severity: "high", decision: "require_approval", action_type: "execute_command", target_summary: "terraform apply", target_redacted: false, policy_section: "commands", rule_key: "require_approval", proposed_value: "terraform apply*", rationale: "Production-impacting infrastructure action requires approval.", confidence: "metadata_derived", evidence_refs: ["sample://evidence/iac-production-change"] },
      { recommendation_id: "policy-rec-2-sample-dec-002", decision_id: "sample-dec-002", session_id: "sample-session-001", agent_id: "codex-agent", repository: "payments/api", control_surface: "sensitive_data", risk_classification: "credential_or_sensitive_data_exposure", severity: "critical", decision: "block", action_type: "read_file", target_summary: "sensitive target redacted", target_redacted: true, policy_section: "filesystem", rule_key: "block_read", proposed_value: ".env*", rationale: "Sensitive production secret file access is blocked.", confidence: "metadata_derived", evidence_refs: ["sample://evidence/secret-read-block"] },
      { recommendation_id: "policy-rec-3-sample-dec-003", decision_id: "sample-dec-003", session_id: "sample-session-002", agent_id: "claude-code-agent", repository: "platform/infra", control_surface: "mcp_tools", risk_classification: "tool_or_mcp_governance_risk", severity: "medium", decision: "warn", action_type: "mcp_tool_call", target_summary: "filesystem.write", target_redacted: false, policy_section: "mcp", rule_key: "allowlist_enabled", proposed_value: true, rationale: "MCP tool requires registration before broad rollout.", confidence: "metadata_derived", evidence_refs: ["sample://evidence/mcp-warning"] }
    ],
    policy_draft: {
      schema_version: "cavra.policy_pack.draft.v1",
      product: "CAVRA",
      valid: true,
      errors: [],
      policy_pack: {
        metadata: { id: "cavra-replay-derived-sample-session-001", title: "Replay-Derived AI Agent Controls", description: "Read-only Community draft generated from normalized AISPM replay decisions.", version: "2026.06.10", inherits: "cavra-ai-agent-baseline", mode: "enforce" },
        filesystem: { block_read: [".env*"] },
        commands: { require_approval: ["terraform apply*"] },
        mcp: { allowlist_enabled: true },
        approvals: { replay_to_policy_authoring: { approvers: ["Platform Security"], source: "aispm_replay_to_policy" } },
        evidence: { require_pr_attestation: true, require_replay_evidence: true, source: "aispm_replay_to_policy" },
        compliance: { maps_to: ["SOC 2 Change Management", "NIST SSDF RV.1.3", "Internal AI Governance"] }
      },
      summary: { policy_id: "cavra-replay-derived-sample-session-001", title: "Replay-Derived AI Agent Controls", version: "2026.06.10", inherits: "cavra-ai-agent-baseline", mode: "enforce", rule_counts: { filesystem: 1, commands: 1, git: 0, mcp: 1, approvals: 2, evidence: 3, compliance: 3 } },
      operator_notes: ["Draft generation is read-only and does not write to the policy directory.", "Commit reviewed policy YAML through repository change control before rollout."]
    },
    write_back: { status: "read_only_preview", next_step: "Review the draft, then use /policy-packs/publish-plan and the approval-bound publish flow.", approval_required: true },
    operator_notes: ["Replay-to-policy authoring is read-only in Community and does not write to policies/.", "Recommendations use normalized decision metadata only; review every generated rule before publishing.", "Use signed PR review and approval-bound policy publishing before enforcement rollout."]
  },
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

const aispmTraceReplayFallback = {
  schema_version: "cavra.aispm.trace_replay.v1",
  product: "CAVRA",
  edition: "community",
  mode: "local_activity",
  data_provenance: "sample_data",
  tracking: "none",
  telemetry: "disabled",
  generated_at: "2026-06-09T00:02:00+00:00",
  session: {
    session_id: "sample-session-001",
    agent_id: "codex-agent",
    actor: "codex-agent",
    repository: "payments/api",
    policy_pack: "cloud-iam-prod",
    state: "completed",
    started_at: "2026-06-09T00:00:00+00:00",
    updated_at: "2026-06-09T00:01:00+00:00"
  },
  summary: {
    step_count: 2,
    blocked_actions: 1,
    approval_required_actions: 1,
    warned_actions: 0,
    critical_or_high_steps: 2,
    evidence_confidence: "activity_evidence_refs"
  },
  steps: [
    {
      step: 1,
      event_type: "policy_decision",
      decision_id: "sample-dec-001",
      session_id: "sample-session-001",
      agent_id: "codex-agent",
      repository: "payments/api",
      action_type: "execute_command",
      target_summary: "terraform apply",
      target_redacted: false,
      decision: "require_approval",
      severity: "high",
      rule_id: "iac.production-change",
      policy_pack: "cloud-iam-prod",
      risk_classification: "infrastructure_change_risk",
      control_surface: "infrastructure_iac",
      reason: "Production-impacting infrastructure action requires approval.",
      evidence_refs: ["sample://evidence/iac-production-change"],
      timestamp: "2026-06-09T00:00:00+00:00"
    },
    {
      step: 2,
      event_type: "policy_decision",
      decision_id: "sample-dec-002",
      session_id: "sample-session-001",
      agent_id: "codex-agent",
      repository: "payments/api",
      action_type: "read_file",
      target_summary: "sensitive target redacted",
      target_redacted: true,
      decision: "block",
      severity: "critical",
      rule_id: "secrets.block-sensitive-read",
      policy_pack: "cavra-ai-agent-baseline",
      risk_classification: "credential_or_sensitive_data_exposure",
      control_surface: "sensitive_data",
      reason: "Sensitive production secret file access is blocked.",
      evidence_refs: ["sample://evidence/secret-read-block"],
      timestamp: "2026-06-09T00:01:00+00:00"
    }
  ],
  evidence_refs: ["sample://evidence/iac-production-change", "sample://evidence/secret-read-block"],
  redaction: {
    target_redaction: "sensitive targets are summarized",
    prompt_capture: "requires_cavra_enterprise",
    reasoning_trace: "requires_cavra_enterprise",
    raw_tool_output: "requires_cavra_enterprise",
    full_trace_replay: "requires_cavra_enterprise",
    customer_context: "requires_cavra_enterprise"
  },
  enterprise_unlocks: {
    status: "requires_cavra_enterprise",
    capabilities: [
      "raw prompt and response replay",
      "model reasoning trace capture",
      "tool-call graph with raw tool results",
      "approval lineage with identity-provider context",
      "immutable multi-tenant replay retention"
    ],
    private_package: "cavra_enterprise"
  }
};

const aispmReplayPolicyFallback = {
  schema_version: "cavra.aispm.replay_to_policy_draft.v1",
  product: "CAVRA",
  edition: "community",
  mode: "local_activity",
  data_provenance: "sample_data",
  tracking: "none",
  telemetry: "disabled",
  generated_at: "2026-06-09T00:03:00+00:00",
  filters: { session_id: "sample-session-001", repository: null, agent_id: null, policy_pack: null, limit: 200 },
  ...aispmFallback.replay_to_policy_draft,
  redaction: {
    raw_prompts: "requires_cavra_enterprise",
    model_reasoning: "requires_cavra_enterprise",
    raw_tool_payloads: "requires_cavra_enterprise",
    ticket_or_change_context: "requires_cavra_enterprise",
    private_asset_graph: "requires_cavra_enterprise",
    customer_context: "requires_cavra_enterprise",
    private_approval_policy: "requires_cavra_enterprise"
  },
  enterprise_unlocks: {
    status: "requires_cavra_enterprise",
    capabilities: [
      "AI-assisted rule authoring from prompts, reasoning traces, and tool payloads",
      "private ticket, CMDB, asset, identity, and service criticality enrichment",
      "approval-bound policy publish workflow automation",
      "policy simulation against tenant history before rollout",
      "organization-wide policy-pack recommendation campaigns"
    ],
    private_package: "cavra_enterprise"
  }
};

const aispmReplayPolicyTestsFallback = {
  schema_version: "cavra.aispm.replay_to_policy_tests.v1",
  product: "CAVRA",
  edition: "community",
  mode: "local_activity",
  data_provenance: "sample_data",
  tracking: "none",
  telemetry: "disabled",
  generated_at: "2026-06-09T00:03:00+00:00",
  filters: { session_id: "sample-session-001", repository: null, agent_id: null, policy_pack: null, limit: 200 },
  summary: {
    source_decisions: 3,
    recommended_rules: 3,
    test_cases: 3,
    fixture_valid: true,
    source_scope: "sample-session-001",
    policy_id: "cavra-replay-derived-sample-session-001"
  },
  test_fixture: {
    schema_version: "cavra.policy_tests.replay_to_policy.v1",
    policy_id: "cavra-replay-derived-sample-session-001",
    source_scope: "sample-session-001",
    case_count: 3,
    cases: aispmFallback.replay_to_policy_draft.recommendations.map((item, index) => ({
      case_id: `replay-policy-test-${index + 1}-${item.decision_id}`,
      recommendation_id: item.recommendation_id,
      decision_id: item.decision_id,
      description: `Assert ${item.policy_section}.${item.rule_key} for ${item.control_surface}.`,
      input: {
        action_type: item.action_type,
        target: typeof item.proposed_value === "string" ? item.proposed_value : item.target_summary,
        target_summary: item.target_summary,
        target_redacted: item.target_redacted,
        agent_id: item.agent_id,
        repository: item.repository,
        policy_pack: "cavra-replay-derived-sample-session-001"
      },
      expected: {
        decision: item.decision,
        severity: item.severity,
        policy_section: item.policy_section,
        rule_key: item.rule_key,
        proposed_value: item.proposed_value,
        risk_classification: item.risk_classification
      },
      assertion_type: "metadata_derived_policy_expectation",
      public_safe: true,
      evidence_refs: item.evidence_refs
    })),
    validation: {
      community_mode: "review_only",
      recommended_commands: [
        "cavra policy validate policies/cavra-replay-derived-sample-session-001/policy.yaml",
        "cavra policy test"
      ],
      notes: [
        "Generated cases are public-safe assertions derived from normalized CAVRA decisions.",
        "Review generated cases before committing them to repository CI.",
        "Private prompt, reasoning, ticket, and tenant-history simulation requires CAVRA Enterprise."
      ]
    }
  },
  export: {
    status: "read_only_preview",
    suggested_path: "tests/fixtures/replay-to-policy/cavra-replay-derived-sample-session-001.json",
    next_step: "Review the fixture, commit it with the policy draft, and validate through repository CI before rollout.",
    approval_required: true
  },
  redaction: {
    raw_prompts: "requires_cavra_enterprise",
    model_reasoning: "requires_cavra_enterprise",
    raw_tool_payloads: "requires_cavra_enterprise",
    private_simulation_history: "requires_cavra_enterprise",
    ticket_or_change_context: "requires_cavra_enterprise",
    customer_context: "requires_cavra_enterprise"
  },
  enterprise_unlocks: {
    status: "requires_cavra_enterprise",
    capabilities: [
      "policy test generation from prompts, reasoning traces, and raw tool payloads",
      "tenant-history simulation before policy rollout",
      "CI write-back for approved policy tests"
    ],
    private_package: "cavra_enterprise"
  }
};

const aispmApprovalLineageFallback = {
  schema_version: "cavra.aispm.approval_lineage.v1",
  product: "CAVRA",
  edition: "community",
  mode: "local_activity",
  data_provenance: "sample_data",
  tracking: "none",
  telemetry: "disabled",
  generated_at: "2026-06-09T00:04:00+00:00",
  filters: { state: null, approver_group: null, session_id: null, limit: 200 },
  summary: {
    total: 1,
    pending: 0,
    approved: 1,
    denied: 0,
    expired: 0,
    break_glass: 0,
    evidence_confidence: "approval_evidence_refs"
  },
  items: aispmFallback.approval_lineage,
  redaction: {
    identity_provider_claims: "requires_cavra_enterprise",
    raw_rbac_policy: "requires_cavra_enterprise",
    private_routing_rules: "requires_cavra_enterprise",
    connector_payloads: "requires_cavra_enterprise",
    human_actor_identifiers: "role labels only"
  },
  enterprise_unlocks: {
    status: "requires_cavra_enterprise",
    capabilities: [
      "identity-provider backed approver context",
      "RBAC-scoped lineage by role and tenant",
      "approval latency SLOs and escalations",
      "immutable multi-tenant approval audit retention",
      "SIEM and ITSM approval workflow exports"
    ],
    private_package: "cavra_enterprise"
  }
};

const aispmBehaviorFingerprintFallback = {
  schema_version: "cavra.aispm.behavior_fingerprints.v1",
  product: "CAVRA",
  edition: "community",
  mode: "local_activity",
  data_provenance: "sample_data",
  tracking: "none",
  telemetry: "disabled",
  generated_at: "2026-06-09T00:04:00+00:00",
  filters: { repository: null, agent_id: null, policy_pack: null, limit: 200 },
  summary: {
    total_agents: 2,
    review_required: 1,
    unusual_behavior: 1,
    baseline: 0,
    evidence_confidence: "activity_evidence_refs"
  },
  items: aispmFallback.behavior_fingerprints,
  redaction: {
    prompt_capture: "requires_cavra_enterprise",
    reasoning_trace: "requires_cavra_enterprise",
    raw_tool_output: "requires_cavra_enterprise",
    tool_call_graph: "requires_cavra_enterprise",
    customer_context: "requires_cavra_enterprise",
    private_behavior_baselines: "requires_cavra_enterprise"
  },
  enterprise_unlocks: {
    status: "requires_cavra_enterprise",
    capabilities: [
      "organization-specific behavior baselines",
      "cross-repository anomaly detection",
      "live streaming behavior drift alerts",
      "identity and RBAC-aware agent owner mapping",
      "SIEM export for behavior drift events"
    ],
    private_package: "cavra_enterprise"
  }
};

const aispmPolicyContextGapFallback = {
  schema_version: "cavra.aispm.policy_context_gaps.v1",
  product: "CAVRA",
  edition: "community",
  mode: "local_activity",
  data_provenance: "sample_data",
  tracking: "none",
  telemetry: "disabled",
  generated_at: "2026-06-09T00:05:00+00:00",
  filters: { repository: null, agent_id: null, policy_pack: null, limit: 200 },
  summary: {
    total_gaps: 16,
    decisions_with_gaps: 3,
    requires_context_review: 3,
    monitor: 0,
    evidence_confidence: "activity_evidence_refs"
  },
  items: aispmFallback.policy_context_gaps,
  redaction: {
    private_cmdb_records: "requires_cavra_enterprise",
    data_catalog_records: "requires_cavra_enterprise",
    identity_provider_claims: "requires_cavra_enterprise",
    cloud_inventory: "requires_cavra_enterprise",
    change_calendar: "requires_cavra_enterprise",
    ticketing_metadata: "requires_cavra_enterprise"
  },
  enterprise_unlocks: {
    status: "requires_cavra_enterprise",
    capabilities: [
      "CMDB and service catalog enrichment",
      "data-owner and data-classification lookup",
      "cloud account and environment-tier enrichment",
      "change-window and ticket correlation",
      "policy decisions that require private context before execution"
    ],
    private_package: "cavra_enterprise"
  }
};

const aispmPreActionForecastFallback = {
  schema_version: "cavra.aispm.pre_action_risk_forecasts.v1",
  product: "CAVRA",
  edition: "community",
  mode: "local_activity",
  data_provenance: "sample_data",
  tracking: "none",
  telemetry: "disabled",
  generated_at: "2026-06-09T00:06:00+00:00",
  filters: { repository: null, agent_id: null, policy_pack: null, limit: 200 },
  summary: {
    total_forecasts: 3,
    critical_or_high_forecasts: 2,
    approval_recommended: 1,
    block_recommended: 1,
    warn_recommended: 1,
    evidence_confidence: "activity_evidence_refs"
  },
  items: aispmFallback.pre_action_risk_forecasts,
  redaction: {
    private_asset_graph: "requires_cavra_enterprise",
    dependency_graph: "requires_cavra_enterprise",
    cloud_resource_inventory: "requires_cavra_enterprise",
    identity_blast_radius: "requires_cavra_enterprise",
    runtime_state: "requires_cavra_enterprise",
    prompt_intent_context: "requires_cavra_enterprise"
  },
  enterprise_unlocks: {
    status: "requires_cavra_enterprise",
    capabilities: [
      "asset graph blast-radius forecasting",
      "identity and permission blast-radius analysis",
      "live dependency graph forecasting",
      "cost, performance, and SLO impact forecasts",
      "pre-action simulation against the private SaaS control plane"
    ],
    private_package: "cavra_enterprise"
  }
};

const aispmIntentActionDriftFallback = {
  schema_version: "cavra.aispm.intent_action_drift.v1",
  product: "CAVRA",
  edition: "community",
  mode: "local_activity",
  data_provenance: "sample_data",
  tracking: "none",
  telemetry: "disabled",
  generated_at: "2026-06-09T00:07:00+00:00",
  filters: { repository: null, agent_id: null, policy_pack: null, limit: 200 },
  summary: {
    total_items: 3,
    high_drift: 1,
    needs_review: 1,
    unknown_intent: 0,
    aligned: 1,
    evidence_confidence: "activity_evidence_refs"
  },
  items: aispmFallback.intent_action_drift,
  redaction: {
    raw_prompt: "requires_cavra_enterprise",
    reasoning_trace: "requires_cavra_enterprise",
    conversation_history: "requires_cavra_enterprise",
    private_ticket_context: "requires_cavra_enterprise",
    full_tool_payload: "requires_cavra_enterprise",
    semantic_intent_model: "requires_cavra_enterprise"
  },
  enterprise_unlocks: {
    status: "requires_cavra_enterprise",
    capabilities: [
      "prompt-derived semantic intent extraction",
      "task, ticket, and pull-request intent correlation",
      "private workflow and change-management context comparison",
      "live drift alerts for tool and target changes",
      "SIEM export for intent-to-action drift events"
    ],
    private_package: "cavra_enterprise"
  }
};

const aispmToolChainGraphFallback = {
  schema_version: "cavra.aispm.tool_chain_graph.v1",
  product: "CAVRA",
  edition: "community",
  mode: "local_activity",
  data_provenance: "sample_data",
  tracking: "none",
  telemetry: "disabled",
  generated_at: "2026-06-09T00:08:00+00:00",
  filters: { repository: null, agent_id: null, policy_pack: null, limit: 200 },
  summary: {
    node_count: aispmFallback.tool_chain_graph.nodes.length,
    edge_count: aispmFallback.tool_chain_graph.edges.length,
    agent_nodes: aispmFallback.tool_chain_graph.nodes.filter((node) => node.node_type === "agent").length,
    tool_nodes: aispmFallback.tool_chain_graph.nodes.filter((node) => node.node_type === "tool").length,
    target_nodes: aispmFallback.tool_chain_graph.nodes.filter((node) => node.node_type === "target").length,
    high_risk_edges: aispmFallback.tool_chain_graph.edges.filter((edge) => edge.risk_score >= 70).length,
    blocked_edges: aispmFallback.tool_chain_graph.edges.filter((edge) => edge.decision === "block").length,
    evidence_confidence: "activity_evidence_refs"
  },
  nodes: aispmFallback.tool_chain_graph.nodes,
  edges: aispmFallback.tool_chain_graph.edges,
  hotspots: aispmFallback.tool_chain_graph.hotspots,
  redaction: {
    raw_tool_payload: "requires_cavra_enterprise",
    tool_result_body: "requires_cavra_enterprise",
    prompt_context: "requires_cavra_enterprise",
    connector_spans: "requires_cavra_enterprise",
    cross_system_call_graph: "requires_cavra_enterprise",
    private_network_targets: "requires_cavra_enterprise"
  },
  enterprise_unlocks: {
    status: "requires_cavra_enterprise",
    capabilities: [
      "raw tool request and response graphing",
      "cross-system call graph from MCP, shell, Git, CI, cloud, and SaaS connectors",
      "latency and execution span correlation",
      "private network and identity-aware target mapping",
      "live tool-chain alerts and SIEM export"
    ],
    private_package: "cavra_enterprise"
  }
};

const aispmAgentBlastRadiusFallback = {
  schema_version: "cavra.aispm.agent_blast_radius.v1",
  product: "CAVRA",
  edition: "community",
  mode: "local_activity",
  data_provenance: "sample_data",
  tracking: "none",
  telemetry: "disabled",
  generated_at: "2026-06-09T00:09:00+00:00",
  filters: { repository: null, agent_id: null, policy_pack: null, limit: 200 },
  summary: {
    total_agents: aispmFallback.agent_blast_radius.length,
    critical_agents: aispmFallback.agent_blast_radius.filter((item) => item.blast_radius_level === "critical").length,
    high_agents: aispmFallback.agent_blast_radius.filter((item) => item.blast_radius_level === "high").length,
    medium_agents: aispmFallback.agent_blast_radius.filter((item) => item.blast_radius_level === "medium").length,
    low_agents: aispmFallback.agent_blast_radius.filter((item) => item.blast_radius_level === "low").length,
    affected_repositories: new Set(aispmFallback.agent_blast_radius.flatMap((item) => item.repositories || [])).size,
    approval_paths: new Set(aispmFallback.agent_blast_radius.flatMap((item) => item.approval_paths || [])).size,
    evidence_confidence: "activity_evidence_refs"
  },
  items: aispmFallback.agent_blast_radius,
  redaction: {
    private_asset_graph: "requires_cavra_enterprise",
    identity_permission_graph: "requires_cavra_enterprise",
    cloud_account_inventory: "requires_cavra_enterprise",
    dependency_graph: "requires_cavra_enterprise",
    secret_names: "requires_cavra_enterprise",
    customer_topology: "requires_cavra_enterprise"
  },
  enterprise_unlocks: {
    status: "requires_cavra_enterprise",
    capabilities: [
      "identity and permission-aware blast-radius analysis",
      "cloud account, Kubernetes, SaaS, and repository dependency graphing",
      "private asset criticality and owner enrichment",
      "secret and data-classification mapping",
      "live blast-radius alerts and executive narrative export"
    ],
    private_package: "cavra_enterprise"
  }
};

const aispmControlCoverageHeatmapFallback = {
  schema_version: "cavra.aispm.control_coverage_heatmap.v1",
  product: "CAVRA",
  edition: "community",
  mode: "local_activity",
  data_provenance: "sample_data",
  tracking: "none",
  telemetry: "disabled",
  generated_at: "2026-06-09T00:10:00+00:00",
  filters: { repository: null, agent_id: null, policy_pack: null, limit: 200 },
  summary: {
    row_count: aispmFallback.control_coverage_heatmap.rows.length,
    surface_count: aispmFallback.control_coverage_heatmap.surfaces.length,
    cell_count: aispmFallback.control_coverage_heatmap.rows.reduce((count, row) => count + (row.cells || []).length, 0),
    enforced_cells: aispmFallback.control_coverage_heatmap.rows.flatMap((row) => row.cells || []).filter((cell) => cell.coverage_status === "enforced").length,
    approval_gated_cells: aispmFallback.control_coverage_heatmap.rows.flatMap((row) => row.cells || []).filter((cell) => cell.coverage_status === "approval_gated").length,
    warning_only_cells: aispmFallback.control_coverage_heatmap.rows.flatMap((row) => row.cells || []).filter((cell) => cell.coverage_status === "warning_only").length,
    observed_cells: aispmFallback.control_coverage_heatmap.rows.flatMap((row) => row.cells || []).filter((cell) => ["observed", "attested"].includes(cell.coverage_status)).length,
    not_observed_cells: aispmFallback.control_coverage_heatmap.rows.flatMap((row) => row.cells || []).filter((cell) => cell.coverage_status === "not_observed_locally").length,
    coverage_score: aispmFallback.control_coverage_heatmap.coverage_score,
    evidence_confidence: "activity_evidence_refs"
  },
  surfaces: aispmFallback.control_coverage_heatmap.surfaces,
  rows: aispmFallback.control_coverage_heatmap.rows,
  top_gaps: aispmFallback.control_coverage_heatmap.top_gaps,
  redaction: {
    private_repository_owner_graph: "requires_cavra_enterprise",
    identity_provider_claims: "requires_cavra_enterprise",
    repository_permission_matrix: "requires_cavra_enterprise",
    environment_criticality: "requires_cavra_enterprise",
    cmdb_service_mapping: "requires_cavra_enterprise",
    live_org_baselines: "requires_cavra_enterprise"
  },
  enterprise_unlocks: {
    status: "requires_cavra_enterprise",
    capabilities: [
      "organization-wide live control coverage baselines",
      "repository owner, service criticality, and environment-tier enrichment",
      "identity and permission-scoped heatmap filtering",
      "policy pack rollout coverage by business unit",
      "coverage SLO alerts and executive compliance exports"
    ],
    private_package: "cavra_enterprise"
  }
};

const aispmEvidenceConfidenceFallback = {
  schema_version: "cavra.aispm.evidence_confidence.v1",
  product: "CAVRA",
  edition: "community",
  mode: "local_activity",
  data_provenance: "sample_data",
  tracking: "none",
  telemetry: "disabled",
  generated_at: "2026-06-09T00:11:00+00:00",
  filters: { repository: null, agent_id: null, policy_pack: null, limit: 200 },
  summary: aispmFallback.evidence_confidence_drilldown.summary,
  facts: aispmFallback.evidence_confidence_drilldown.facts,
  redaction: {
    raw_evidence_payload: "requires_cavra_enterprise",
    private_artifact_contents: "requires_cavra_enterprise",
    signature_trust_chain: "requires_cavra_enterprise",
    identity_provider_claims: "requires_cavra_enterprise",
    external_ticket_payloads: "requires_cavra_enterprise",
    customer_data: "requires_cavra_enterprise",
    tenant_evidence_store: "requires_cavra_enterprise"
  },
  enterprise_unlocks: {
    status: "requires_cavra_enterprise",
    capabilities: [
      "immutable evidence store verification",
      "signed artifact and provenance validation",
      "SIEM, GRC, and ticket correlation",
      "evidence freshness SLO alerts",
      "long-term retention and auditor export workflows"
    ],
    private_package: "cavra_enterprise"
  }
};

const aispmEvidenceFreshnessFallback = {
  schema_version: "cavra.aispm.evidence_freshness.v1",
  product: "CAVRA",
  edition: "community",
  mode: "local_activity",
  data_provenance: "sample_data",
  tracking: "none",
  telemetry: "disabled",
  generated_at: "2026-06-09T00:03:00+00:00",
  filters: { repository: null, agent_id: null, policy_pack: null, limit: 200 },
  slo_policy: aispmFallback.evidence_freshness_slo.slo_policy,
  summary: aispmFallback.evidence_freshness_slo.summary,
  items: aispmFallback.evidence_freshness_slo.items,
  redaction: {
    tenant_evidence_store: "requires_cavra_enterprise",
    immutable_archive_probe: "requires_cavra_enterprise",
    object_lock_status: "requires_cavra_enterprise",
    kms_key_health: "requires_cavra_enterprise",
    retention_lifecycle_policy: "requires_cavra_enterprise",
    external_archive_metadata: "requires_cavra_enterprise",
    auditor_export_manifest: "requires_cavra_enterprise"
  },
  enterprise_unlocks: {
    status: "requires_cavra_enterprise",
    capabilities: [
      "immutable evidence archive health validation",
      "object-lock, KMS, and lifecycle policy readiness checks",
      "tenant retention SLO alerts and breach escalation",
      "archive restore drills and auditor export manifests",
      "cross-system evidence freshness correlation"
    ],
    private_package: "cavra_enterprise"
  }
};

const aispmExecutiveNarrativeFallback = {
  schema_version: "cavra.aispm.executive_risk_narrative.v1",
  product: "CAVRA",
  edition: "community",
  mode: "local_activity",
  data_provenance: "sample_data",
  tracking: "none",
  telemetry: "disabled",
  generated_at: "2026-06-09T00:03:00+00:00",
  filters: { repository: null, agent_id: null, policy_pack: null, limit: 200 },
  narrative: aispmFallback.executive_risk_narrative,
  redaction: {
    raw_prompts: "requires_cavra_enterprise",
    model_reasoning: "requires_cavra_enterprise",
    private_business_context: "requires_cavra_enterprise",
    customer_impact_analysis: "requires_cavra_enterprise",
    trend_history: "requires_cavra_enterprise",
    ai_generated_board_summary: "requires_cavra_enterprise",
    tenant_benchmarking: "requires_cavra_enterprise"
  },
  enterprise_unlocks: {
    status: "requires_cavra_enterprise",
    capabilities: [
      "AI-assisted board and CSO narrative generation",
      "private trend history and tenant benchmarking",
      "business owner, service criticality, and customer-impact enrichment",
      "scheduled executive brief delivery",
      "GRC and incident packet export"
    ],
    private_package: "cavra_enterprise"
  }
};

let currentAispmPayload = aispmFallback;

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
  { type: "AI Posture", label: "Evidence Confidence", route: "ai-posture", description: "Dashboard tiles identify sample, local, or Enterprise data provenance." },
  { type: "AI Posture", label: "Evidence Confidence Drilldown", route: "ai-posture", description: "Rank policy decisions by signed, activity, sample, metadata-only, or missing evidence." },
  { type: "AI Posture", label: "Evidence Freshness SLO", route: "ai-posture", description: "Show stale evidence, retention gaps, and Enterprise archive-readiness boundaries." },
  { type: "AI Posture", label: "Executive Risk Narrative", route: "ai-posture", description: "Summarize Community-safe posture, top risks, evidence gaps, and leadership actions." },
  { type: "AI Posture", label: "Trace Replay", route: "ai-posture", description: "Community-safe replay packet with normalized steps and Enterprise redaction boundaries." },
  { type: "AI Posture", label: "Replay-To-Policy Draft", route: "ai-posture", description: "Convert replay decisions into read-only candidate policy controls." },
  { type: "AI Posture", label: "Replay-To-Policy Tests", route: "ai-posture", description: "Export public-safe policy test fixtures for replay-derived controls." },
  { type: "AI Posture", label: "Replay-To-Policy Review", route: "ai-posture", description: "Check reviewer readiness before generated controls are used in CI." },
  { type: "AI Posture", label: "Replay-To-Policy Packet", route: "ai-posture", description: "Export draft, tests, and review checklist as one public-safe PR packet." },
  { type: "AI Posture", label: "PR Attachment Guidance", route: "ai-posture", description: "Show where to attach replay-to-policy review evidence in a GitHub PR." },
  { type: "AI Posture", label: "Replay-To-Policy CI Gate", route: "ai-posture", description: "Show required check names and GitHub, GitLab, and Azure CI template paths." },
  { type: "AI Posture", label: "CI Gate Readiness Export", route: "ai-posture", description: "Copy or download the branch-protection readiness packet for GitHub, GitLab, and Azure." },
  { type: "AI Posture", label: "CI Gate Readiness Summary", route: "ai-posture", description: "Show ready or action-required status for GitHub, GitLab, and Azure gate rollout." },
  { type: "AI Posture", label: "CI Gate Rollout Checklist", route: "ai-posture", description: "Copy or download reviewer-ready Markdown for production branch-protection rollout." },
  { type: "AI Posture", label: "CI Gate Rollout Audit Packet", route: "ai-posture", description: "Bundle readiness JSON and rollout checklist metadata for auditor attachment." },
  { type: "AI Posture", label: "Approval Lineage", route: "ai-posture", description: "Public-safe who-approved-what metadata with role labels and evidence references." },
  { type: "AI Posture", label: "Behavior Fingerprinting", route: "ai-posture", description: "Baseline-vs-unusual agent behavior signals from public-safe activity metadata." },
  { type: "AI Posture", label: "Control Coverage Heatmap", route: "ai-posture", description: "Compare agent and repository coverage across CAVRA control surfaces." },
  { type: "AI Posture", label: "Policy Context Gaps", route: "ai-posture", description: "Policy-invisible risk caused by missing environment, owner, data, change-window, or criticality context." },
  { type: "AI Posture", label: "Pre-Action Risk Forecast", route: "ai-posture", description: "Projected blast radius and likely impacts before an agent action is allowed." },
  { type: "AI Posture", label: "Intent-To-Action Drift", route: "ai-posture", description: "Compare declared intent with observed action, target, and policy outcome." },
  { type: "AI Posture", label: "Tool-Chain Risk Graph", route: "ai-posture", description: "Map agents, tools, redacted targets, policy packs, and risky execution edges." },
  { type: "AI Posture", label: "Agent Blast-Radius Map", route: "ai-posture", description: "Show repository, target, tool, policy, approval, and surface reach per AI agent." }
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
  currentAispmPayload = payload;
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
  renderAispmControlCoverageHeatmap({
    ...aispmControlCoverageHeatmapFallback,
    data_provenance: payload.data_provenance || "sample_data",
    summary: summarizeControlCoverageHeatmap(payload.control_coverage_heatmap || aispmControlCoverageHeatmapFallback),
    surfaces: payload.control_coverage_heatmap?.surfaces || aispmControlCoverageHeatmapFallback.surfaces,
    rows: payload.control_coverage_heatmap?.rows || aispmControlCoverageHeatmapFallback.rows,
    top_gaps: payload.control_coverage_heatmap?.top_gaps || aispmControlCoverageHeatmapFallback.top_gaps
  }, "posture sample");
  renderAispmEvidenceConfidence({
    ...aispmEvidenceConfidenceFallback,
    data_provenance: payload.data_provenance || "sample_data",
    summary: summarizeEvidenceConfidence(payload.evidence_confidence_drilldown?.facts || aispmEvidenceConfidenceFallback.facts),
    facts: payload.evidence_confidence_drilldown?.facts || aispmEvidenceConfidenceFallback.facts
  }, "posture sample");
  renderAispmEvidenceFreshness({
    ...aispmEvidenceFreshnessFallback,
    data_provenance: payload.data_provenance || "sample_data",
    summary: summarizeEvidenceFreshness(payload.evidence_freshness_slo?.items || aispmEvidenceFreshnessFallback.items),
    items: payload.evidence_freshness_slo?.items || aispmEvidenceFreshnessFallback.items,
    slo_policy: payload.evidence_freshness_slo?.slo_policy || aispmEvidenceFreshnessFallback.slo_policy
  }, "posture sample");
  renderAispmExecutiveNarrative({
    ...aispmExecutiveNarrativeFallback,
    data_provenance: payload.data_provenance || "sample_data",
    narrative: payload.executive_risk_narrative || aispmExecutiveNarrativeFallback.narrative
  }, "posture sample");
  renderAispmReplayPolicy({
    ...aispmReplayPolicyFallback,
    data_provenance: payload.data_provenance || "sample_data",
    ...(payload.replay_to_policy_draft || aispmReplayPolicyFallback)
  }, "posture sample");
  renderAispmReplayPolicyTests({
    ...aispmReplayPolicyTestsFallback,
    data_provenance: payload.data_provenance || "sample_data"
  }, "posture sample");
  renderAispmBehaviorFingerprints({
    ...aispmBehaviorFingerprintFallback,
    data_provenance: payload.data_provenance || "sample_data",
    summary: summarizeBehaviorFingerprints(payload.behavior_fingerprints || aispmBehaviorFingerprintFallback.items),
    items: payload.behavior_fingerprints || aispmBehaviorFingerprintFallback.items
  }, "posture sample");
  renderAispmPolicyContextGaps({
    ...aispmPolicyContextGapFallback,
    data_provenance: payload.data_provenance || "sample_data",
    summary: summarizePolicyContextGaps(payload.policy_context_gaps || aispmPolicyContextGapFallback.items),
    items: payload.policy_context_gaps || aispmPolicyContextGapFallback.items
  }, "posture sample");
  renderAispmPreActionForecasts({
    ...aispmPreActionForecastFallback,
    data_provenance: payload.data_provenance || "sample_data",
    summary: summarizePreActionForecasts(payload.pre_action_risk_forecasts || aispmPreActionForecastFallback.items),
    items: payload.pre_action_risk_forecasts || aispmPreActionForecastFallback.items
  }, "posture sample");
  renderAispmIntentActionDrift({
    ...aispmIntentActionDriftFallback,
    data_provenance: payload.data_provenance || "sample_data",
    summary: summarizeIntentActionDrift(payload.intent_action_drift || aispmIntentActionDriftFallback.items),
    items: payload.intent_action_drift || aispmIntentActionDriftFallback.items
  }, "posture sample");
  renderAispmToolChainGraph({
    ...aispmToolChainGraphFallback,
    data_provenance: payload.data_provenance || "sample_data",
    summary: summarizeToolChainGraph(payload.tool_chain_graph || aispmToolChainGraphFallback),
    nodes: payload.tool_chain_graph?.nodes || aispmToolChainGraphFallback.nodes,
    edges: payload.tool_chain_graph?.edges || aispmToolChainGraphFallback.edges,
    hotspots: payload.tool_chain_graph?.hotspots || aispmToolChainGraphFallback.hotspots
  }, "posture sample");
  renderAispmAgentBlastRadius({
    ...aispmAgentBlastRadiusFallback,
    data_provenance: payload.data_provenance || "sample_data",
    summary: summarizeAgentBlastRadius(payload.agent_blast_radius || aispmAgentBlastRadiusFallback.items),
    items: payload.agent_blast_radius || aispmAgentBlastRadiusFallback.items
  }, "posture sample");
  el("#aispmTimeline").innerHTML = (payload.timeline || []).slice(0, 8).map((event) => `
    <div class="timeline-item">
      <h3>${escapeHtml(event.title || event.event_type || "timeline event")}</h3>
      <p>${escapeHtml(event.agent_id || "unknown-agent")} · ${escapeHtml(event.repository || "local")} · ${escapeHtml(event.outcome || "recorded")}</p>
    </div>
  `).join("") || `<p class="empty-state">No timeline events available.</p>`;
  renderAispmApprovalLineage({
    ...aispmApprovalLineageFallback,
    data_provenance: payload.data_provenance || "sample_data",
    summary: summarizeApprovalLineage(payload.approval_lineage || aispmApprovalLineageFallback.items),
    items: payload.approval_lineage || aispmApprovalLineageFallback.items
  }, "posture sample");
  el("#aispmPayload").textContent = JSON.stringify(payload, null, 2);
  syncTraceReplaySessions(payload);
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
    const payload = await response.json();
    renderAispmDashboard(payload, "API local activity");
  } catch (error) {
    renderAispmDashboard(aispmFallback, "API unavailable, sample shown");
  }
}

function sessionIdsFromPosture(payload) {
  const candidates = [
    ...(payload.timeline || []),
    ...(payload.findings || []),
    ...(payload.near_misses || [])
  ];
  const ids = [...new Set(candidates.map((item) => item.session_id).filter(Boolean))];
  return ids.length ? ids : [aispmTraceReplayFallback.session.session_id];
}

function syncTraceReplaySessions(payload) {
  const picker = el("#aispmTraceSession");
  if (!picker) return;
  const previous = picker.value;
  const sessions = sessionIdsFromPosture(payload);
  picker.innerHTML = sessions.map((sessionId) => `
    <option value="${escapeHtml(sessionId)}">${escapeHtml(sessionId)}</option>
  `).join("");
  picker.value = sessions.includes(previous) ? previous : sessions[0];
  loadAispmTraceReplay(picker.value);
}

function traceReplayFromPosture(payload, sessionId) {
  if (sessionId === aispmTraceReplayFallback.session.session_id) return aispmTraceReplayFallback;
  const decisions = (payload.timeline || []).filter((event) => event.session_id === sessionId);
  if (!decisions.length) {
    return {
      ...aispmTraceReplayFallback,
      data_provenance: payload.data_provenance || "sample_data",
      session: { ...aispmTraceReplayFallback.session, session_id: sessionId, state: "not_observed_locally" },
      summary: { ...aispmTraceReplayFallback.summary, step_count: 0, blocked_actions: 0, approval_required_actions: 0, warned_actions: 0, critical_or_high_steps: 0 },
      steps: [],
      evidence_refs: []
    };
  }
  const steps = decisions.slice().reverse().map((event, index) => {
    const target = String(event.target || event.title || "target not recorded");
    const targetRedacted = target.toLowerCase().includes("secret") || target.toLowerCase().includes(".env");
    return {
      step: index + 1,
      event_type: "policy_decision",
      decision_id: event.decision_id || event.event_id,
      session_id: sessionId,
      agent_id: event.agent_id || "unknown-agent",
      repository: event.repository || "local",
      action_type: String(event.title || "policy_decision").split(" ").slice(1).join(" ") || "unknown",
      target_summary: targetRedacted ? "sensitive target redacted" : target,
      target_redacted: targetRedacted,
      decision: event.outcome || "recorded",
      severity: event.severity || "low",
      rule_id: "local.timeline",
      policy_pack: "cavra-ai-agent-baseline",
      risk_classification: event.severity === "critical" ? "credential_or_sensitive_data_exposure" : "policy_decision_review",
      control_surface: event.severity === "critical" ? "sensitive_data" : "general_policy",
      reason: "Derived from the public-safe local execution timeline.",
      evidence_refs: event.evidence_refs || [],
      timestamp: event.timestamp
    };
  });
  const counts = steps.reduce((acc, step) => {
    acc[step.decision] = (acc[step.decision] || 0) + 1;
    if (["critical", "high"].includes(step.severity)) acc.criticalHigh += 1;
    return acc;
  }, { criticalHigh: 0 });
  return {
    ...aispmTraceReplayFallback,
    data_provenance: payload.data_provenance || "local_activity_store",
    session: {
      session_id: sessionId,
      agent_id: steps[0]?.agent_id || "unknown-agent",
      actor: steps[0]?.agent_id || "ai-agent",
      repository: steps[0]?.repository || "local",
      policy_pack: steps[0]?.policy_pack || "cavra-ai-agent-baseline",
      state: "derived_from_timeline",
      started_at: steps[0]?.timestamp,
      updated_at: steps.at(-1)?.timestamp
    },
    summary: {
      step_count: steps.length,
      blocked_actions: counts.block || 0,
      approval_required_actions: counts.require_approval || 0,
      warned_actions: counts.warn || 0,
      critical_or_high_steps: counts.criticalHigh,
      evidence_confidence: payload.overview?.evidence_confidence || "activity_metadata_only"
    },
    steps,
    evidence_refs: [...new Set(steps.flatMap((step) => step.evidence_refs || []))]
  };
}

async function loadAispmTraceReplay(sessionId) {
  const apiBase = (window.CAVRA_API_BASE || "").replace(/\/$/, "");
  const status = el("#aispmTraceStatus");
  status.textContent = "Loading replay packet...";
  if (apiBase) {
    try {
      const response = await fetch(`${apiBase}/aispm/trace-replay/${encodeURIComponent(sessionId)}`);
      if (!response.ok) throw new Error(`Trace replay HTTP ${response.status}`);
      renderAispmTraceReplay(await response.json(), "API local activity replay");
      return;
    } catch (error) {
      renderAispmTraceReplay(traceReplayFromPosture(currentAispmPayload, sessionId), "API unavailable, derived replay shown");
      return;
    }
  }
  renderAispmTraceReplay(traceReplayFromPosture(currentAispmPayload, sessionId), "static sample replay");
}

async function loadAispmReplayPolicy() {
  const apiBase = (window.CAVRA_API_BASE || "").replace(/\/$/, "");
  const sessionId = el("#aispmTraceSession")?.value || aispmTraceReplayFallback.session.session_id;
  if (apiBase) {
    try {
      const response = await fetch(`${apiBase}/aispm/replay-to-policy-draft?session_id=${encodeURIComponent(sessionId)}`);
      if (!response.ok) throw new Error(`Replay-to-policy HTTP ${response.status}`);
      renderAispmReplayPolicy(await response.json(), "API local activity");
      await loadAispmReplayPolicyTests(sessionId);
      return;
    } catch (error) {
      renderAispmReplayPolicy({
        ...aispmReplayPolicyFallback,
        filters: { ...aispmReplayPolicyFallback.filters, session_id: sessionId }
      }, "API unavailable, sample shown");
      renderAispmReplayPolicyTests({
        ...aispmReplayPolicyTestsFallback,
        filters: { ...aispmReplayPolicyTestsFallback.filters, session_id: sessionId }
      }, "API unavailable, sample shown");
      return;
    }
  }
  renderAispmReplayPolicy({
    ...aispmReplayPolicyFallback,
    filters: { ...aispmReplayPolicyFallback.filters, session_id: sessionId }
  }, "static sample draft");
  renderAispmReplayPolicyTests({
    ...aispmReplayPolicyTestsFallback,
    filters: { ...aispmReplayPolicyTestsFallback.filters, session_id: sessionId }
  }, "static sample tests");
}

async function loadAispmReplayPolicyTests(sessionId) {
  const apiBase = (window.CAVRA_API_BASE || "").replace(/\/$/, "");
  if (!apiBase) return;
  try {
    const response = await fetch(`${apiBase}/aispm/replay-to-policy-tests?session_id=${encodeURIComponent(sessionId)}`);
    if (!response.ok) throw new Error(`Replay-to-policy tests HTTP ${response.status}`);
    renderAispmReplayPolicyTests(await response.json(), "API local activity");
  } catch (error) {
    renderAispmReplayPolicyTests({
      ...aispmReplayPolicyTestsFallback,
      filters: { ...aispmReplayPolicyTestsFallback.filters, session_id: sessionId }
    }, "API unavailable, sample shown");
  }
}

function renderAispmReplayPolicy(packet, note = "sample draft") {
  currentAispmReplayPolicyDraftPacket = packet;
  const summary = packet.summary || {};
  const recommendations = packet.recommendations || [];
  const writeBack = packet.write_back || {};
  const writeBackStatus = String(writeBack.status || "read_only_preview").replaceAll("_", " ");
  const draft = packet.policy_draft?.policy_pack || packet.policy_draft || {};
  const summaryCards = [
    ["Recommended Rules", summary.recommended_rules ?? recommendations.length, `${packet.data_provenance || "sample_data"} · ${note}`],
    ["Draft Valid", summary.draft_valid === false ? "No" : "Yes", `Authorable: ${summary.authorable_decisions ?? recommendations.length}`],
    ["Source Decisions", summary.source_decisions ?? "0", `Session: ${packet.filters?.session_id || "current"}`],
    ["Write Back", writeBackStatus, writeBack.approval_required ? "Approval required" : "Preview only"]
  ];
  el("#aispmReplayPolicySummary").innerHTML = summaryCards.map(([label, value, detail]) => `
    <article class="trace-summary-card">
      <span>${escapeHtml(label)}</span>
      <strong>${escapeHtml(value)}</strong>
      <p>${escapeHtml(detail)}</p>
    </article>
  `).join("");
  el("#aispmReplayPolicyRecommendations").innerHTML = recommendations.slice(0, 6).map((item) => `
    <article class="replay-policy-card">
      <header>
        <div>
          <span class="replay-policy-meta">${escapeHtml(item.control_surface || "general_policy")}</span>
          <strong>${escapeHtml(item.policy_section || "policy")} · <code>${escapeHtml(item.rule_key || "rule")}</code></strong>
        </div>
        <span class="severity ${escapeHtml(item.decision || "review")}">${escapeHtml(item.decision || "review")}</span>
      </header>
      <p>${escapeHtml(item.rationale || "Review the generated control before publishing.")}</p>
      <p><b>Proposed:</b> <code>${escapeHtml(JSON.stringify(item.proposed_value))}</code></p>
      <small>${escapeHtml(item.agent_id || "unknown-agent")} · ${escapeHtml(item.repository || "local")} · ${escapeHtml(item.decision_id || item.recommendation_id || "decision")}</small>
    </article>
  `).join("") || `<p class="empty-state">No authorable replay decisions found for this session.</p>`;
  el("#aispmReplayPolicyDraft").textContent = JSON.stringify(draft, null, 2);
  renderAispmReplayPolicyReviewWorkflow();
}

function renderAispmReplayPolicyTests(packet, note = "sample tests") {
  currentAispmReplayPolicyTestsPacket = packet;
  const fixture = packet.test_fixture || {};
  const exportPacket = {
    export_status: packet.export?.status || "read_only_preview",
    suggested_path: packet.export?.suggested_path || "tests/fixtures/replay-to-policy/generated.json",
    data_provenance: `${packet.data_provenance || "sample_data"} · ${note}`,
    summary: packet.summary || {},
    test_fixture: fixture
  };
  currentAispmReplayPolicyTestsExport = exportPacket;
  el("#aispmReplayPolicyTests").textContent = JSON.stringify(exportPacket, null, 2);
  el("#aispmReplayPolicyTestStatus").textContent = `${exportPacket.export_status} · ${exportPacket.suggested_path} · ${exportPacket.summary?.test_cases ?? fixture.case_count ?? 0} cases`;
  renderAispmReplayPolicyReviewWorkflow();
}

function renderAispmReplayPolicyReviewWorkflow() {
  const draft = currentAispmReplayPolicyDraftPacket || aispmReplayPolicyFallback;
  const tests = currentAispmReplayPolicyTestsPacket || aispmReplayPolicyTestsFallback;
  const draftPolicy = draft.policy_draft?.policy_pack || draft.policy_draft || {};
  const recommendations = draft.recommendations || [];
  const fixture = tests.test_fixture || {};
  const cases = fixture.cases || [];
  const validationCommands = fixture.validation?.recommended_commands || [];
  const evidenceBacked = cases.length > 0 && cases.every((item) => (item.evidence_refs || []).length > 0);
  const checklist = [
    {
      label: "Candidate Controls",
      status: recommendations.length ? "review_required" : "not_ready",
      detail: recommendations.length ? `${recommendations.length} generated controls need owner review.` : "No generated controls are available."
    },
    {
      label: "Fixture Coverage",
      status: cases.length >= recommendations.length && recommendations.length ? "pass" : "review_required",
      detail: `${cases.length} fixture cases for ${recommendations.length} candidate controls.`
    },
    {
      label: "Evidence References",
      status: evidenceBacked ? "pass" : "review_required",
      detail: evidenceBacked ? "Each fixture case carries public-safe evidence refs." : "Review evidence refs before CI adoption."
    },
    {
      label: "Validation Commands",
      status: validationCommands.length ? "pass" : "review_required",
      detail: validationCommands.length ? validationCommands.join(" · ") : "Add validation commands before CI use."
    },
    {
      label: "Approval Gate",
      status: draft.write_back?.approval_required || tests.export?.approval_required ? "pass" : "review_required",
      detail: "Generated outputs remain review-only until approved through change control."
    },
    {
      label: "Enterprise Boundary",
      status: draft.enterprise_unlocks?.status === "requires_cavra_enterprise" && tests.enterprise_unlocks?.status === "requires_cavra_enterprise" ? "pass" : "review_required",
      detail: "Prompt, reasoning, raw tool payloads, simulation, and CI write-back remain Enterprise-only."
    }
  ];
  const readyCount = checklist.filter((item) => item.status === "pass").length;
  const overall = readyCount === checklist.length ? "Ready For Reviewer" : "Reviewer Action Required";
  currentAispmReplayPolicyReviewPacket = {
    schema_version: "cavra.aispm.replay_to_policy_review_packet.v1",
    product: "CAVRA",
    edition: "community",
    mode: "review_packet_export",
    tracking: "none",
    telemetry: "disabled",
    generated_at: new Date().toISOString(),
    data_provenance: {
      draft: draft.data_provenance || "sample_data",
      tests: tests.data_provenance || "sample_data"
    },
    source: {
      session_id: draft.filters?.session_id || tests.filters?.session_id || "current",
      draft_schema_version: draft.schema_version || "cavra.aispm.replay_to_policy_draft.v1",
      test_schema_version: tests.schema_version || "cavra.aispm.replay_to_policy_tests.v1"
    },
    review_summary: {
      status: overall,
      checks_passed: readyCount,
      checks_total: checklist.length,
      ci_adoption: "requires_human_review",
      approval_required: true
    },
    review_checklist: checklist,
    policy_draft: draftPolicy,
    test_fixture: fixture,
    export: {
      status: "review_only_packet",
      filename: "cavra-replay-policy-review-packet.json",
      intended_use: "Attach to PRs or auditor review as public-safe evidence of generated policy review readiness."
    },
    redaction: {
      raw_prompts: "requires_cavra_enterprise",
      model_reasoning: "requires_cavra_enterprise",
      raw_tool_payloads: "requires_cavra_enterprise",
      private_simulation_history: "requires_cavra_enterprise",
      customer_context: "requires_cavra_enterprise"
    }
  };
  el("#aispmReplayPolicyReviewPacketStatus").textContent = `${currentAispmReplayPolicyReviewPacket.export.status} · ${readyCount}/${checklist.length} checks passed · ${currentAispmReplayPolicyReviewPacket.export.filename}`;
  renderAispmReplayPolicyPrGuidance(currentAispmReplayPolicyReviewPacket, tests);
  renderAispmReplayPolicyCiGate(currentAispmReplayPolicyReviewPacket);
  el("#aispmReplayPolicyReviewWorkflow").innerHTML = `
    <div class="review-workflow-header">
      <div>
        <h4>Review Workflow</h4>
        <p>${escapeHtml(overall)} · ${readyCount}/${checklist.length} checks passed · CI adoption still requires human review.</p>
      </div>
      <span class="severity ${readyCount === checklist.length ? "approved" : "pending"}">${escapeHtml(overall)}</span>
    </div>
    <div class="review-checklist">
      ${checklist.map((item) => `
        <article class="review-check">
          <span>${escapeHtml(item.label)}</span>
          <strong>${escapeHtml(String(item.status).replaceAll("_", " "))}</strong>
          <p>${escapeHtml(item.detail)}</p>
        </article>
      `).join("")}
    </div>
  `;
}

function renderAispmReplayPolicyPrGuidance(reviewPacket, testsPacket) {
  const policyId = reviewPacket.policy_draft?.metadata?.id || reviewPacket.test_fixture?.policy_id || "generated-policy";
  const fixturePath = testsPacket.export?.suggested_path || `tests/fixtures/replay-to-policy/${policyId}.json`;
  const draftPath = `policies/${policyId}/policy.yaml`;
  const packetFilename = reviewPacket.export?.filename || "cavra-replay-policy-review-packet.json";
  currentAispmReplayPolicyPrApprovalText = [
    "CAVRA replay-to-policy review completed.",
    `Review packet: ${packetFilename}`,
    `Policy draft path: ${draftPath}`,
    `Test fixture path: ${fixturePath}`,
    `Checklist: ${reviewPacket.review_summary?.checks_passed ?? 0}/${reviewPacket.review_summary?.checks_total ?? 0} checks passed`,
    "Approval scope: approve these generated controls for repository CI validation only; production enforcement still requires normal CAVRA policy publishing and approval gates."
  ].join("\\n");
  const cards = [
    ["Attach To PR Conversation", "Review packet", packetFilename],
    ["Commit As Policy Draft", "Candidate policy", draftPath],
    ["Commit As Test Fixture", "Policy test fixture", fixturePath]
  ];
  el("#aispmReplayPolicyPrGuidance").innerHTML = `
    <div class="pr-guidance-header">
      <div>
        <h4>PR Attachment Guidance</h4>
        <p>Attach the packet to the PR conversation, commit reviewed files under the suggested paths, and use explicit approval language.</p>
      </div>
      <button id="copyAispmReplayPolicyPrApproval" type="button">Copy Approval Text</button>
    </div>
    <div class="pr-guidance-grid">
      ${cards.map(([label, title, value]) => `
        <article class="pr-guidance-card">
          <span>${escapeHtml(label)}</span>
          <strong>${escapeHtml(title)}</strong>
          <code>${escapeHtml(value)}</code>
        </article>
      `).join("")}
    </div>
    <article class="pr-guidance-card">
      <span>Approval Language</span>
      <pre class="pr-approval-template">${escapeHtml(currentAispmReplayPolicyPrApprovalText)}</pre>
    </article>
  `;
  el("#copyAispmReplayPolicyPrApproval").addEventListener("click", copyAispmReplayPolicyPrApproval);
}

function renderAispmReplayPolicyCiGate(reviewPacket) {
  const packetFilename = reviewPacket.export?.filename || "cavra-replay-policy-review-packet.json";
  const checksPassed = reviewPacket.review_summary?.checks_passed ?? 0;
  const checksTotal = reviewPacket.review_summary?.checks_total ?? 0;
  const gates = [
    {
      platform: "GitHub Actions",
      check: "cavra-aispm-review-packet",
      path: "examples/github-actions/cavra-aispm-review-packet-validation.yml",
      setup: "Copy into .github/workflows/ and add the check to branch protection.",
      enforcement: "Add cavra-aispm-review-packet as a required status check before merge."
    },
    {
      platform: "GitLab CI",
      check: "cavra-aispm-review-packet",
      path: "examples/gitlab-ci/cavra-aispm-review-packet-validation.gitlab-ci.yml",
      setup: "Include in merge-request pipelines and require the governance job before merge.",
      enforcement: "Require the cavra-aispm-review-packet job in merge-request approval rules."
    },
    {
      platform: "Azure Pipelines",
      check: "cavra-aispm-review-packet",
      path: "examples/azure-pipelines/cavra-aispm-review-packet-validation.azure-pipelines.yml",
      setup: "Create a Build validation policy with this pipeline as a required gate.",
      enforcement: "Configure branch policy Build validation with cavra-aispm-review-packet required."
    }
  ];
  currentAispmReplayPolicyCiGateReadiness = {
    schema_version: "cavra.aispm.replay_to_policy_ci_gate_readiness.v1",
    product: "CAVRA",
    edition: "community",
    mode: "ci_gate_readiness_export",
    tracking: "none",
    telemetry: "disabled",
    generated_at: new Date().toISOString(),
    source: {
      review_packet: packetFilename,
      review_packet_status: reviewPacket.export?.status || "review_only_packet",
      review_summary_status: reviewPacket.review_summary?.status || "Reviewer Action Required",
      checks_passed: checksPassed,
      checks_total: checksTotal
    },
    required_packet: {
      filename: packetFilename,
      purpose: "Required public-safe evidence packet for replay-derived policy or fixture changes."
    },
    gates: gates.map((gate) => ({
      platform: gate.platform,
      required_check: gate.check,
      template_path: gate.path,
      setup: gate.setup,
      enforcement: gate.enforcement
    })),
    validation: {
      cli_command: "cavra aispm validate-ci-gate-readiness cavra-replay-policy-ci-gate-readiness.json --repo-root .",
      api_endpoint: "/aispm/replay-to-policy-ci-gate-readiness/validate"
    },
    readiness_checklist: [
      "Copy the platform template into the repository CI configuration.",
      "Require the cavra-aispm-review-packet check before merge.",
      `Attach or commit ${packetFilename} with replay-derived policy and fixture changes.`,
      "Run cavra aispm validate-ci-gate-readiness cavra-replay-policy-ci-gate-readiness.json --repo-root .",
      "Verify the gate fails closed when replay-derived changes do not include a valid packet.",
      "Keep production enforcement behind normal CAVRA policy publishing and approval gates."
    ],
    enterprise_boundaries: {
      automated_ci_write_back: "requires_cavra_enterprise",
      tenant_policy_distribution: "requires_cavra_enterprise",
      private_connector_configuration: "requires_cavra_enterprise"
    }
  };
  el("#aispmReplayPolicyCiGateStatus").textContent = `ready_export · ${gates.length} platforms · ${checksPassed}/${checksTotal} review checks · cavra-replay-policy-ci-gate-readiness.json`;
  el("#aispmReplayPolicyCiGate").innerHTML = `
    <div class="ci-gate-header">
      <div>
        <h4>Replay-To-Policy CI Gate</h4>
        <p>Require a valid <code>${escapeHtml(packetFilename)}</code> before replay-derived policy drafts or fixtures merge.</p>
      </div>
      <span class="severity approved">Cross-platform</span>
    </div>
    <div class="ci-gate-grid">
      ${gates.map((gate) => `
        <article class="ci-gate-card">
          <span>${escapeHtml(gate.platform)}</span>
          <strong>${escapeHtml(gate.check)}</strong>
          <code>${escapeHtml(gate.path)}</code>
          <p>${escapeHtml(gate.setup)}</p>
        </article>
      `).join("")}
    </div>
  `;
  renderAispmReplayPolicyCiGateSummary(currentAispmReplayPolicyCiGateReadiness);
}

function renderAispmReplayPolicyCiGateSummary(readiness) {
  const gates = readiness.gates || [];
  const reviewReady = readiness.source?.checks_passed === readiness.source?.checks_total;
  const platformRows = gates.map((gate) => ({
    platform: gate.platform,
    status: reviewReady ? "ready" : "action required",
    required_check: gate.required_check,
    template_path: gate.template_path,
    outcome: reviewReady
      ? "Template and required check metadata are ready for branch protection."
      : "Complete reviewer checklist before production gate rollout."
  }));
  el("#aispmReplayPolicyCiGateSummary").innerHTML = `
    <div class="ci-gate-summary-header">
      <div>
        <h4>CI Gate Readiness Summary</h4>
        <p>${escapeHtml(readiness.source?.checks_passed ?? 0)}/${escapeHtml(readiness.source?.checks_total ?? 0)} review checks passed · validate with <code>${escapeHtml(readiness.validation?.cli_command || "cavra aispm validate-ci-gate-readiness")}</code></p>
      </div>
      <span class="severity ${reviewReady ? "approved" : "pending"}">${reviewReady ? "Ready" : "Action Required"}</span>
    </div>
    <div class="ci-gate-summary-grid">
      ${platformRows.map((row) => `
        <article class="ci-gate-summary-card">
          <span>${escapeHtml(row.platform)}</span>
          <strong>${escapeHtml(row.status)}</strong>
          <code>${escapeHtml(row.template_path)}</code>
          <p><b>Required check:</b> ${escapeHtml(row.required_check)}</p>
          <p>${escapeHtml(row.outcome)}</p>
        </article>
      `).join("")}
    </div>
  `;
  renderAispmReplayPolicyCiGateRolloutChecklist(readiness, platformRows, reviewReady);
}

function renderAispmReplayPolicyCiGateRolloutChecklist(readiness, platformRows, reviewReady) {
  const packetFilename = readiness.required_packet?.filename || "cavra-replay-policy-review-packet.json";
  const readinessFilename = "cavra-replay-policy-ci-gate-readiness.json";
  const lines = [
    "# CAVRA Replay-To-Policy CI Gate Production Rollout Checklist",
    "",
    `Status: ${reviewReady ? "Ready" : "Action Required"}`,
    `Review checks: ${readiness.source?.checks_passed ?? 0}/${readiness.source?.checks_total ?? 0}`,
    `Required review packet: ${packetFilename}`,
    `Readiness packet: ${readinessFilename}`,
    "",
    "## Validator",
    "",
    "```bash",
    readiness.validation?.cli_command || `cavra aispm validate-ci-gate-readiness ${readinessFilename} --repo-root .`,
    "```",
    "",
    `API endpoint: \`${readiness.validation?.api_endpoint || "/aispm/replay-to-policy-ci-gate-readiness/validate"}\``,
    "",
    "## Platform Gates",
    "",
    ...platformRows.flatMap((row) => [
      `### ${row.platform}`,
      "",
      `- Status: ${row.status}`,
      `- Required check: \`${row.required_check}\``,
      `- Template path: \`${row.template_path}\``,
      `- Outcome: ${row.outcome}`,
      ""
    ]),
    "## Manual Rollout Steps",
    "",
    ...(readiness.readiness_checklist || []).map((item) => `- [ ] ${item}`),
    "- [ ] Confirm branch protection or merge policy requires `cavra-aispm-review-packet`.",
    "- [ ] Attach this checklist and the readiness JSON to the rollout ticket or PR.",
    "",
    "## Enterprise Boundary",
    "",
    "- Community exports this checklist as reviewer guidance only.",
    "- Automated branch-protection write-back, tenant policy distribution, and private connector configuration require CAVRA Enterprise.",
    ""
  ];
  currentAispmReplayPolicyCiGateRolloutMarkdown = lines.join("\n");
  el("#aispmReplayPolicyCiGateRollout").textContent = currentAispmReplayPolicyCiGateRolloutMarkdown;
  el("#aispmReplayPolicyCiGateRolloutStatus").textContent = `${reviewReady ? "ready" : "action_required"} · ${platformRows.length} platforms · cavra-replay-policy-ci-gate-rollout-checklist.md`;
  renderAispmReplayPolicyCiGateAuditPacket(readiness, platformRows, reviewReady);
}

function renderAispmReplayPolicyCiGateAuditPacket(readiness, platformRows, reviewReady) {
  currentAispmReplayPolicyCiGateAuditPacket = {
    schema_version: "cavra.aispm.replay_to_policy_ci_gate_rollout_audit_packet.v1",
    product: "CAVRA",
    edition: "community",
    mode: "ci_gate_rollout_audit_packet",
    tracking: "none",
    telemetry: "disabled",
    generated_at: new Date().toISOString(),
    status: reviewReady ? "ready" : "action_required",
    readiness_packet: {
      filename: "cavra-replay-policy-ci-gate-readiness.json",
      schema_version: readiness.schema_version,
      source: readiness.source,
      required_packet: readiness.required_packet,
      validation: readiness.validation,
      gates: readiness.gates
    },
    rollout_checklist: {
      filename: "cavra-replay-policy-ci-gate-rollout-checklist.md",
      format: "markdown",
      status: reviewReady ? "ready" : "action_required",
      manual_steps: readiness.readiness_checklist || [],
      required_check: "cavra-aispm-review-packet",
      platform_count: platformRows.length
    },
    platform_outcomes: platformRows.map((row) => ({
      platform: row.platform,
      status: row.status,
      required_check: row.required_check,
      template_path: row.template_path,
      outcome: row.outcome
    })),
    evidence_attachments: [
      "cavra-replay-policy-review-packet.json",
      "cavra-replay-policy-ci-gate-readiness.json",
      "cavra-replay-policy-ci-gate-rollout-checklist.md"
    ],
    enterprise_boundaries: readiness.enterprise_boundaries || {},
    public_safety: {
      raw_prompts: "not_included",
      model_reasoning: "not_included",
      customer_context: "not_included",
      branch_protection_write_back: "requires_cavra_enterprise"
    }
  };
  el("#aispmReplayPolicyCiGateAuditPacket").textContent = JSON.stringify(currentAispmReplayPolicyCiGateAuditPacket, null, 2);
  el("#aispmReplayPolicyCiGateAuditStatus").textContent = `${currentAispmReplayPolicyCiGateAuditPacket.status} · ${platformRows.length} platforms · cavra-replay-policy-ci-gate-rollout-audit-packet.json`;
}

async function copyAispmReplayPolicyCiGateReadiness() {
  const payload = JSON.stringify(currentAispmReplayPolicyCiGateReadiness || {}, null, 2);
  const copied = await copyTextToClipboard(payload);
  el("#aispmReplayPolicyCiGateStatus").textContent = copied
    ? "Copied public-safe CI gate readiness JSON."
    : "Copy was blocked by the browser. Use Download Readiness or select the JSON from exported artifacts.";
}

function downloadAispmReplayPolicyCiGateReadiness() {
  const payload = JSON.stringify(currentAispmReplayPolicyCiGateReadiness || {}, null, 2);
  const blob = new Blob([payload], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = "cavra-replay-policy-ci-gate-readiness.json";
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  URL.revokeObjectURL(url);
  el("#aispmReplayPolicyCiGateStatus").textContent = "Downloaded public-safe CI gate readiness JSON.";
}

async function copyAispmReplayPolicyCiGateRollout() {
  const copied = await copyTextToClipboard(currentAispmReplayPolicyCiGateRolloutMarkdown);
  el("#aispmReplayPolicyCiGateRolloutStatus").textContent = copied
    ? "Copied CI gate production rollout checklist Markdown."
    : "Copy was blocked by the browser. Use Download Checklist or select the Markdown preview.";
}

function downloadAispmReplayPolicyCiGateRollout() {
  const blob = new Blob([currentAispmReplayPolicyCiGateRolloutMarkdown], { type: "text/markdown" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = "cavra-replay-policy-ci-gate-rollout-checklist.md";
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  URL.revokeObjectURL(url);
  el("#aispmReplayPolicyCiGateRolloutStatus").textContent = "Downloaded CI gate production rollout checklist Markdown.";
}

async function copyAispmReplayPolicyCiGateAuditPacket() {
  const payload = JSON.stringify(currentAispmReplayPolicyCiGateAuditPacket || {}, null, 2);
  const copied = await copyTextToClipboard(payload);
  el("#aispmReplayPolicyCiGateAuditStatus").textContent = copied
    ? "Copied public-safe CI gate rollout audit packet JSON."
    : "Copy was blocked by the browser. Use Download Audit Packet or select the JSON preview.";
}

function downloadAispmReplayPolicyCiGateAuditPacket() {
  const payload = JSON.stringify(currentAispmReplayPolicyCiGateAuditPacket || {}, null, 2);
  const blob = new Blob([payload], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = "cavra-replay-policy-ci-gate-rollout-audit-packet.json";
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  URL.revokeObjectURL(url);
  el("#aispmReplayPolicyCiGateAuditStatus").textContent = "Downloaded public-safe CI gate rollout audit packet JSON.";
}

async function copyAispmReplayPolicyPrApproval() {
  const copied = await copyTextToClipboard(currentAispmReplayPolicyPrApprovalText);
  el("#aispmReplayPolicyReviewPacketStatus").textContent = copied
    ? "Copied replay-to-policy PR approval text."
    : "Copy was blocked by the browser. Select the approval text manually.";
}

async function copyAispmReplayPolicyReviewPacket() {
  const payload = JSON.stringify(currentAispmReplayPolicyReviewPacket || {}, null, 2);
  const copied = await copyTextToClipboard(payload);
  el("#aispmReplayPolicyReviewPacketStatus").textContent = copied
    ? "Copied public-safe replay-to-policy review packet JSON."
    : "Copy was blocked by the browser. Use Download Packet or select the JSON from exported artifacts.";
}

function downloadAispmReplayPolicyReviewPacket() {
  const payload = JSON.stringify(currentAispmReplayPolicyReviewPacket || {}, null, 2);
  const blob = new Blob([payload], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = "cavra-replay-policy-review-packet.json";
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  URL.revokeObjectURL(url);
  el("#aispmReplayPolicyReviewPacketStatus").textContent = "Downloaded public-safe replay-to-policy review packet JSON.";
}

async function copyAispmReplayPolicyTests() {
  const payload = JSON.stringify(currentAispmReplayPolicyTestsExport || {}, null, 2);
  const copied = await copyTextToClipboard(payload);
  el("#aispmReplayPolicyTestStatus").textContent = copied
    ? "Copied review-only replay-to-policy test fixture JSON."
    : "Copy was blocked by the browser. Select the JSON preview or use Download JSON.";
}

function downloadAispmReplayPolicyTests() {
  const payload = JSON.stringify(currentAispmReplayPolicyTestsExport || {}, null, 2);
  const blob = new Blob([payload], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = "cavra-replay-policy-tests.json";
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  URL.revokeObjectURL(url);
  el("#aispmReplayPolicyTestStatus").textContent = "Downloaded review-only replay-to-policy test fixture JSON.";
}

async function copyTextToClipboard(text) {
  try {
    if (navigator.clipboard?.writeText) {
      await navigator.clipboard.writeText(text);
      return true;
    }
  } catch (error) {
    // Fall through to the selection-based copy path for restricted browsers.
  }
  const textarea = document.createElement("textarea");
  textarea.value = text;
  textarea.setAttribute("readonly", "");
  textarea.style.position = "fixed";
  textarea.style.left = "-9999px";
  textarea.style.top = "0";
  document.body.appendChild(textarea);
  textarea.select();
  let copied = false;
  try {
    copied = document.execCommand("copy");
  } catch (error) {
    copied = false;
  }
  textarea.remove();
  return copied;
}

function summarizeApprovalLineage(items) {
  const counts = (items || []).reduce((acc, item) => {
    acc[item.state] = (acc[item.state] || 0) + 1;
    return acc;
  }, {});
  return {
    total: (items || []).length,
    pending: counts.pending || 0,
    approved: counts.approved || 0,
    denied: counts.denied || 0,
    expired: counts.expired || 0,
    break_glass: counts.break_glass || 0,
    evidence_confidence: (items || []).every((item) => (item.evidence_refs || []).length) ? "approval_evidence_refs" : "approval_metadata_only"
  };
}

async function loadAispmApprovalLineage() {
  const apiBase = (window.CAVRA_API_BASE || "").replace(/\/$/, "");
  if (apiBase) {
    try {
      const response = await fetch(`${apiBase}/aispm/approval-lineage`);
      if (!response.ok) throw new Error(`Approval lineage HTTP ${response.status}`);
      renderAispmApprovalLineage(await response.json(), "API local approval store");
      return;
    } catch (error) {
      renderAispmApprovalLineage(aispmApprovalLineageFallback, "API unavailable, sample shown");
      return;
    }
  }
  renderAispmApprovalLineage(aispmApprovalLineageFallback, "static sample lineage");
}

function renderAispmApprovalLineage(packet, note = "sample lineage") {
  const summary = packet.summary || {};
  const items = packet.items || [];
  const summaryCards = [
    ["Lineage", summary.total ?? items.length, `${packet.data_provenance || "sample_data"} · ${note}`],
    ["Approved", summary.approved ?? 0, `Pending: ${summary.pending ?? 0}`],
    ["Denied/Expired", (summary.denied ?? 0) + (summary.expired ?? 0), `Break-glass: ${summary.break_glass ?? 0}`],
    ["Evidence", summary.evidence_confidence || "unknown", "Public-safe metadata"]
  ];
  el("#aispmApprovalSummary").innerHTML = summaryCards.map(([label, value, detail]) => `
    <article class="trace-summary-card">
      <span>${escapeHtml(label)}</span>
      <strong>${escapeHtml(value)}</strong>
      <p>${escapeHtml(detail)}</p>
    </article>
  `).join("");
  el("#aispmApprovalLineage").innerHTML = items.slice(0, 8).map((item) => `
    <article class="approval-lineage-row">
      <span class="severity ${escapeHtml(item.state || "pending")}">${escapeHtml(item.state || "pending")}</span>
      <div>
        <strong>${escapeHtml(item.approver_group || "Unassigned")} approved ${escapeHtml(item.decision?.action_type || "action")}</strong>
        <p>${escapeHtml(item.decision?.target_summary || "target not recorded")} · ${escapeHtml(item.decision?.risk_classification || "policy_decision_review")}</p>
        <small>${escapeHtml(item.requested_by || "unknown requester")} → ${escapeHtml(item.decided_by || "pending")} · ${escapeHtml(item.external_ref || item.approval_id || "approval record")}</small>
      </div>
      <small>${escapeHtml((item.evidence_refs || []).join(", ") || "no evidence refs")}</small>
    </article>
  `).join("") || `<p class="empty-state">No approval lineage records available.</p>`;
}

function summarizeControlCoverageHeatmap(packet) {
  const rows = packet?.rows || [];
  const cells = rows.flatMap((row) => row.cells || []);
  return {
    row_count: rows.length,
    surface_count: (packet?.surfaces || []).length,
    cell_count: cells.length,
    enforced_cells: cells.filter((cell) => cell.coverage_status === "enforced").length,
    approval_gated_cells: cells.filter((cell) => cell.coverage_status === "approval_gated").length,
    warning_only_cells: cells.filter((cell) => cell.coverage_status === "warning_only").length,
    observed_cells: cells.filter((cell) => ["observed", "attested"].includes(cell.coverage_status)).length,
    not_observed_cells: cells.filter((cell) => cell.coverage_status === "not_observed_locally").length,
    coverage_score: cells.length ? Math.round(cells.reduce((sum, cell) => sum + Number(cell.coverage_score || 0), 0) / cells.length) : 0,
    evidence_confidence: cells.some((cell) => (cell.evidence_refs || []).length) ? "activity_evidence_refs" : "activity_metadata_only"
  };
}

async function loadAispmControlCoverageHeatmap() {
  const apiBase = (window.CAVRA_API_BASE || "").replace(/\/$/, "");
  if (apiBase) {
    try {
      const response = await fetch(`${apiBase}/aispm/control-coverage-heatmap`);
      if (!response.ok) throw new Error(`Control heatmap HTTP ${response.status}`);
      renderAispmControlCoverageHeatmap(await response.json(), "API local activity");
      return;
    } catch (error) {
      renderAispmControlCoverageHeatmap(aispmControlCoverageHeatmapFallback, "API unavailable, sample shown");
      return;
    }
  }
  renderAispmControlCoverageHeatmap(aispmControlCoverageHeatmapFallback, "static sample heatmap");
}

function renderAispmControlCoverageHeatmap(packet, note = "sample heatmap") {
  const summary = packet.summary || summarizeControlCoverageHeatmap(packet);
  const rows = packet.rows || [];
  const summaryCards = [
    ["Coverage Score", summary.coverage_score ?? 0, `${packet.data_provenance || "sample_data"} · ${note}`],
    ["Rows", summary.row_count ?? rows.length, `Surfaces: ${summary.surface_count ?? 0}`],
    ["Enforced/Approval", (summary.enforced_cells ?? 0) + (summary.approval_gated_cells ?? 0), `Warn-only: ${summary.warning_only_cells ?? 0}`],
    ["Gaps", summary.not_observed_cells ?? 0, `Evidence: ${summary.evidence_confidence || "unknown"}`]
  ];
  el("#aispmCoverageHeatmapSummary").innerHTML = summaryCards.map(([label, value, detail]) => `
    <article class="trace-summary-card">
      <span>${escapeHtml(label)}</span>
      <strong>${escapeHtml(value)}</strong>
      <p>${escapeHtml(detail)}</p>
    </article>
  `).join("");
  el("#aispmCoverageHeatmapRows").innerHTML = rows.slice(0, 6).map((row) => `
    <article class="coverage-heatmap-row">
      <header>
        <div>
          <span>${escapeHtml(row.agent_id || "unknown-agent")}</span>
          <strong>${escapeHtml(row.repository || "local")}</strong>
        </div>
        <span>${escapeHtml(row.decision_count ?? 0)} decisions · ${escapeHtml((row.policy_packs || []).join(", ") || "no policy pack")}</span>
      </header>
      <div class="coverage-cell-grid">
        ${(row.cells || []).map((cell) => {
          const status = cell.coverage_status || "not_observed_locally";
          return `
          <div class="coverage-cell coverage-${escapeHtml(status)}">
            <span>${escapeHtml(status.replaceAll("_", " "))}</span>
            <strong>${escapeHtml(cell.label || cell.surface_id || "Control")}</strong>
            <p>${escapeHtml(cell.decision_count ?? 0)} decisions · ${escapeHtml(cell.blocked_actions ?? 0)} block · ${escapeHtml(cell.approval_required_actions ?? 0)} approval · ${escapeHtml(cell.warned_actions ?? 0)} warn</p>
            <p>${escapeHtml(cell.recommended_action || "Review coverage status.")}</p>
          </div>
        `}).join("")}
      </div>
    </article>
  `).join("") || `<p class="empty-state">No control coverage heatmap rows available.</p>`;
}

function summarizeEvidenceConfidence(facts) {
  const items = facts || [];
  const counts = items.reduce((acc, item) => {
    acc[item.confidence_level] = (acc[item.confidence_level] || 0) + 1;
    return acc;
  }, {});
  return {
    total_facts: items.length,
    signed_evidence_items: counts.signed_evidence || 0,
    activity_evidence_items: counts.activity_evidence_refs || 0,
    sample_evidence_items: counts.sample_evidence_refs || 0,
    metadata_only_items: counts.activity_metadata_only || 0,
    missing_evidence_items: counts.missing_evidence || 0,
    evidence_score: items.length ? Math.round(items.reduce((sum, item) => sum + Number(item.confidence_score || 0), 0) / items.length) : 0,
    lowest_confidence_level: [...items].sort((a, b) => Number(a.confidence_score || 0) - Number(b.confidence_score || 0))[0]?.confidence_level || "no_local_activity",
    highest_confidence_level: [...items].sort((a, b) => Number(b.confidence_score || 0) - Number(a.confidence_score || 0))[0]?.confidence_level || "no_local_activity"
  };
}

async function loadAispmEvidenceConfidence() {
  const apiBase = (window.CAVRA_API_BASE || "").replace(/\/$/, "");
  if (apiBase) {
    try {
      const response = await fetch(`${apiBase}/aispm/evidence-confidence`);
      if (!response.ok) throw new Error(`Evidence confidence HTTP ${response.status}`);
      renderAispmEvidenceConfidence(await response.json(), "API local activity");
      return;
    } catch (error) {
      renderAispmEvidenceConfidence(aispmEvidenceConfidenceFallback, "API unavailable, sample shown");
      return;
    }
  }
  renderAispmEvidenceConfidence(aispmEvidenceConfidenceFallback, "static sample evidence");
}

function renderAispmEvidenceConfidence(packet, note = "sample evidence") {
  const facts = packet.facts || [];
  const summary = packet.summary || summarizeEvidenceConfidence(facts);
  const summaryCards = [
    ["Evidence Score", summary.evidence_score ?? 0, `${packet.data_provenance || "sample_data"} · ${note}`],
    ["Signed", summary.signed_evidence_items ?? 0, `Activity refs: ${summary.activity_evidence_items ?? 0}`],
    ["Sample/Metadata", (summary.sample_evidence_items ?? 0) + (summary.metadata_only_items ?? 0), `Missing: ${summary.missing_evidence_items ?? 0}`],
    ["Facts", summary.total_facts ?? facts.length, `Lowest: ${summary.lowest_confidence_level || "unknown"}`]
  ];
  el("#aispmEvidenceConfidenceSummary").innerHTML = summaryCards.map(([label, value, detail]) => `
    <article class="trace-summary-card">
      <span>${escapeHtml(label)}</span>
      <strong>${escapeHtml(value)}</strong>
      <p>${escapeHtml(detail)}</p>
    </article>
  `).join("");
  const orderedFacts = [...facts].sort((a, b) => Number(a.confidence_score || 0) - Number(b.confidence_score || 0));
  el("#aispmEvidenceConfidenceRows").innerHTML = orderedFacts.slice(0, 8).map((fact) => `
    <article class="evidence-confidence-row">
      <div class="evidence-confidence-score">${escapeHtml(fact.confidence_score ?? 0)}</div>
      <div>
        <span class="evidence-confidence-level">${escapeHtml((fact.confidence_level || "unknown").replaceAll("_", " "))}</span>
        <strong>${escapeHtml(fact.agent_id || "unknown-agent")} · ${escapeHtml(fact.repository || "local")}</strong>
        <p>${escapeHtml(fact.decision || fact.fact_type || "evidence fact")} · ${escapeHtml(fact.control_surface || "general_policy")} · ${escapeHtml(fact.severity || "low")}</p>
        <p>${escapeHtml(fact.recommended_action || "Review evidence confidence before audit reliance.")}</p>
      </div>
      <small>${escapeHtml((fact.evidence_refs || []).join(", ") || "metadata only")}</small>
    </article>
  `).join("") || `<p class="empty-state">No evidence confidence facts available.</p>`;
}

function summarizeEvidenceFreshness(items) {
  const rows = items || [];
  const count = (field, value) => rows.filter((item) => item[field] === value).length;
  const avg = (values) => values.length ? Math.round(values.reduce((sum, value) => sum + Number(value || 0), 0) / values.length) : 0;
  const freshnessScores = rows.map((item) => ({
    fresh: 100,
    review_soon: 68,
    stale: 18,
    timestamp_missing: 0
  }[item.freshness_status] ?? 0));
  const retentionScores = rows.map((item) => ({
    retained_reference: 100,
    sample_reference: 45,
    evidence_ref_only: 38,
    metadata_only: 0,
    retention_missing: 0
  }[item.retention_status] ?? 0));
  return {
    total_items: rows.length,
    fresh_items: count("freshness_status", "fresh"),
    review_soon_items: count("freshness_status", "review_soon"),
    stale_items: count("freshness_status", "stale"),
    missing_timestamp_items: count("freshness_status", "timestamp_missing"),
    retention_ready_items: count("retention_status", "retained_reference"),
    sample_retention_items: count("retention_status", "sample_reference"),
    retention_gap_items: rows.filter((item) => ["evidence_ref_only", "metadata_only", "retention_missing"].includes(item.retention_status)).length,
    slo_met_items: count("slo_status", "met"),
    slo_monitor_items: count("slo_status", "monitor"),
    slo_breached_items: count("slo_status", "breached"),
    freshness_score: avg(freshnessScores),
    retention_score: avg(retentionScores),
    oldest_age_hours: Math.max(...rows.map((item) => Number(item.age_hours || 0)), 0),
    evidence_confidence: rows.some((item) => (item.evidence_refs || []).length) ? "activity_evidence_refs" : "activity_metadata_only"
  };
}

async function loadAispmEvidenceFreshness() {
  const apiBase = (window.CAVRA_API_BASE || "").replace(/\/$/, "");
  if (apiBase) {
    try {
      const response = await fetch(`${apiBase}/aispm/evidence-freshness`);
      if (!response.ok) throw new Error(`Evidence freshness HTTP ${response.status}`);
      renderAispmEvidenceFreshness(await response.json(), "API local activity");
      return;
    } catch (error) {
      renderAispmEvidenceFreshness(aispmEvidenceFreshnessFallback, "API unavailable, sample shown");
      return;
    }
  }
  renderAispmEvidenceFreshness(aispmEvidenceFreshnessFallback, "static sample SLO");
}

function renderAispmEvidenceFreshness(packet, note = "sample SLO") {
  const items = packet.items || [];
  const summary = packet.summary || summarizeEvidenceFreshness(items);
  const policy = packet.slo_policy || {};
  const summaryCards = [
    ["Freshness Score", summary.freshness_score ?? 0, `${packet.data_provenance || "sample_data"} · ${note}`],
    ["Retention Score", summary.retention_score ?? 0, `Ready: ${summary.retention_ready_items ?? 0}`],
    ["SLO Breaches", summary.slo_breached_items ?? 0, `Monitor: ${summary.slo_monitor_items ?? 0}`],
    ["Oldest Evidence", summary.oldest_age_hours ?? "n/a", `Fresh <= ${policy.fresh_hours || 24}h`]
  ];
  el("#aispmEvidenceFreshnessSummary").innerHTML = summaryCards.map(([label, value, detail]) => `
    <article class="trace-summary-card">
      <span>${escapeHtml(label)}</span>
      <strong>${escapeHtml(value)}</strong>
      <p>${escapeHtml(detail)}</p>
    </article>
  `).join("");
  const ordered = [...items].sort((a, b) => {
    const statusWeight = { breached: 3, monitor: 2, met: 1 };
    return (statusWeight[b.slo_status] || 0) - (statusWeight[a.slo_status] || 0)
      || Number(b.age_hours || 0) - Number(a.age_hours || 0);
  });
  el("#aispmEvidenceFreshnessRows").innerHTML = ordered.slice(0, 8).map((item) => `
    <article class="evidence-freshness-row">
      <div class="evidence-freshness-meter">
        <strong>${escapeHtml(item.age_hours ?? "n/a")}h</strong>
        <span>${escapeHtml(item.slo_status || "review")}</span>
      </div>
      <div>
        <strong>${escapeHtml(item.agent_id || "unknown-agent")} · ${escapeHtml(item.repository || "local")}</strong>
        <p>${escapeHtml(item.decision || item.item_type || "evidence item")} · ${escapeHtml(item.control_surface || "general_policy")} · ${escapeHtml(item.severity || "low")}</p>
        <div class="evidence-freshness-badges">
          <span>${escapeHtml((item.freshness_status || "unknown").replaceAll("_", " "))}</span>
          <span>${escapeHtml((item.retention_status || "unknown").replaceAll("_", " "))}</span>
        </div>
        <p>${escapeHtml(item.recommended_action || "Review evidence freshness and retention before audit reliance.")}</p>
      </div>
      <small>${escapeHtml((item.evidence_refs || []).join(", ") || "metadata only")}</small>
    </article>
  `).join("") || `<p class="empty-state">No evidence freshness SLO records available.</p>`;
}

async function loadAispmExecutiveNarrative() {
  const apiBase = (window.CAVRA_API_BASE || "").replace(/\/$/, "");
  if (apiBase) {
    try {
      const response = await fetch(`${apiBase}/aispm/executive-risk-narrative`);
      if (!response.ok) throw new Error(`Executive narrative HTTP ${response.status}`);
      renderAispmExecutiveNarrative(await response.json(), "API local activity");
      return;
    } catch (error) {
      renderAispmExecutiveNarrative(aispmExecutiveNarrativeFallback, "API unavailable, sample shown");
      return;
    }
  }
  renderAispmExecutiveNarrative(aispmExecutiveNarrativeFallback, "static sample narrative");
}

function renderAispmExecutiveNarrative(packet, note = "sample narrative") {
  const narrative = packet.narrative || aispmExecutiveNarrativeFallback.narrative;
  const metrics = narrative.key_metrics || {};
  const summaryCards = [
    ["Risk Level", narrative.risk_level || "unknown", `${packet.data_provenance || "sample_data"} · ${note}`],
    ["Posture Score", narrative.posture_score ?? 0, `${metrics.risk_findings ?? 0} findings`],
    ["Blocked/Approval", (metrics.blocked_actions ?? 0) + (metrics.approval_required_actions ?? 0), "Controlled before execution"],
    ["Evidence SLO", metrics.evidence_slo_breaches ?? 0, `${metrics.evidence_retention_gaps ?? 0} retention gaps`]
  ];
  el("#aispmExecutiveNarrativeSummary").innerHTML = summaryCards.map(([label, value, detail]) => `
    <article class="trace-summary-card">
      <span>${escapeHtml(label)}</span>
      <strong>${escapeHtml(value)}</strong>
      <p>${escapeHtml(detail)}</p>
    </article>
  `).join("");
  el("#aispmExecutiveNarrative").innerHTML = `
    <div class="executive-narrative-headline">
      <strong>${escapeHtml(narrative.headline || "No executive narrative available yet.")}</strong>
    </div>
    <div class="executive-narrative-grid">
      <section class="executive-narrative-card">
        <h4>Brief</h4>
        <div class="executive-narrative-list">
          ${(narrative.sections || []).map((section) => `
            <article>
              <strong>${escapeHtml(section.title || "Section")}</strong>
              <p>${escapeHtml(section.body || "")}</p>
            </article>
          `).join("")}
        </div>
      </section>
      <section class="executive-narrative-card">
        <h4>Top Risks</h4>
        <div class="executive-narrative-list">
          ${(narrative.top_risks || []).slice(0, 5).map((risk) => `
            <article>
              <strong>${escapeHtml(risk.title || "Risk")}</strong>
              <small>${escapeHtml(risk.severity || "low")} · ${escapeHtml(risk.agent_id || "unknown-agent")} · ${escapeHtml(risk.repository || "local")}</small>
              <p>${escapeHtml(risk.reason || "Review recommended.")}</p>
            </article>
          `).join("") || `<p class="empty-state">No top risks in the current local activity window.</p>`}
        </div>
      </section>
      <section class="executive-narrative-card">
        <h4>Recommended Actions</h4>
        <div class="executive-narrative-list">
          ${(narrative.recommended_actions || []).map((action) => `
            <article>
              <strong>${escapeHtml(action.action || "Action")}</strong>
              <small>${escapeHtml(action.priority || "medium")} · ${escapeHtml(action.owner || "owner")}</small>
            </article>
          `).join("")}
        </div>
      </section>
      <section class="executive-narrative-card">
        <h4>Boundaries</h4>
        <div class="executive-narrative-list">
          ${(narrative.limitations || []).map((item) => `
            <article><p>${escapeHtml(item)}</p></article>
          `).join("")}
        </div>
      </section>
    </div>
  `;
}

function summarizeBehaviorFingerprints(items) {
  const counts = (items || []).reduce((acc, item) => {
    acc[item.drift_status] = (acc[item.drift_status] || 0) + 1;
    return acc;
  }, {});
  return {
    total_agents: (items || []).length,
    review_required: counts.review_required || 0,
    unusual_behavior: counts.unusual_behavior || 0,
    baseline: counts.baseline || 0,
    evidence_confidence: (items || []).some((item) => (item.evidence_refs || []).length) ? "activity_evidence_refs" : "activity_metadata_only"
  };
}

async function loadAispmBehaviorFingerprints() {
  const apiBase = (window.CAVRA_API_BASE || "").replace(/\/$/, "");
  if (apiBase) {
    try {
      const response = await fetch(`${apiBase}/aispm/behavior-fingerprints`);
      if (!response.ok) throw new Error(`Behavior fingerprints HTTP ${response.status}`);
      renderAispmBehaviorFingerprints(await response.json(), "API local activity");
      return;
    } catch (error) {
      renderAispmBehaviorFingerprints(aispmBehaviorFingerprintFallback, "API unavailable, sample shown");
      return;
    }
  }
  renderAispmBehaviorFingerprints(aispmBehaviorFingerprintFallback, "static sample fingerprints");
}

function renderAispmBehaviorFingerprints(packet, note = "sample fingerprints") {
  const summary = packet.summary || {};
  const items = packet.items || [];
  const summaryCards = [
    ["Fingerprints", summary.total_agents ?? items.length, `${packet.data_provenance || "sample_data"} · ${note}`],
    ["Review Required", summary.review_required ?? 0, "Blocked, approval-gated, or high-risk drift"],
    ["Unusual Behavior", summary.unusual_behavior ?? 0, `Baseline: ${summary.baseline ?? 0}`],
    ["Evidence", summary.evidence_confidence || "unknown", "Public-safe metadata only"]
  ];
  el("#aispmFingerprintSummary").innerHTML = summaryCards.map(([label, value, detail]) => `
    <article class="trace-summary-card">
      <span>${escapeHtml(label)}</span>
      <strong>${escapeHtml(value)}</strong>
      <p>${escapeHtml(detail)}</p>
    </article>
  `).join("");
  el("#aispmBehaviorFingerprints").innerHTML = items.slice(0, 6).map((item) => {
    const actions = (item.action_profile || []).slice(0, 3).map((entry) => `${entry.name}:${entry.count}`).join(" · ") || "no actions";
    const decisions = (item.decision_profile || []).slice(0, 3).map((entry) => `${entry.name}:${entry.count}`).join(" · ") || "no decisions";
    const signals = (item.risk_signals || []).slice(0, 6).map((signal) => `<span>${escapeHtml(signal.replaceAll("_", " "))}</span>`).join("");
    return `
      <article class="fingerprint-card">
        <div class="fingerprint-card-header">
          <div>
            <span>${escapeHtml(item.drift_status || "baseline")}</span>
            <strong>${escapeHtml(item.agent_id || "unknown-agent")}</strong>
          </div>
          <b>${escapeHtml(item.drift_score ?? 0)}</b>
        </div>
        <p>${escapeHtml((item.repositories || []).join(", ") || "local")} · ${escapeHtml(item.decision_count || 0)} decisions · ${escapeHtml(item.session_count || 0)} sessions</p>
        <dl>
          <dt>Actions</dt><dd>${escapeHtml(actions)}</dd>
          <dt>Decisions</dt><dd>${escapeHtml(decisions)}</dd>
          <dt>Surfaces</dt><dd>${escapeHtml((item.control_surfaces || []).join(", ") || "none observed")}</dd>
        </dl>
        <div class="risk-signal-list">${signals || "<span>baseline</span>"}</div>
      </article>
    `;
  }).join("") || `<p class="empty-state">No behavior fingerprints available for this activity window.</p>`;
}

function summarizePolicyContextGaps(items) {
  const counts = (items || []).reduce((acc, item) => {
    acc[item.gap_status] = (acc[item.gap_status] || 0) + 1;
    acc.totalGaps += (item.missing_context || []).length;
    return acc;
  }, { totalGaps: 0 });
  return {
    total_gaps: counts.totalGaps,
    decisions_with_gaps: (items || []).length,
    requires_context_review: counts.requires_context_review || 0,
    monitor: counts.monitor || 0,
    evidence_confidence: (items || []).some((item) => (item.evidence_refs || []).length) ? "activity_evidence_refs" : "activity_metadata_only"
  };
}

async function loadAispmPolicyContextGaps() {
  const apiBase = (window.CAVRA_API_BASE || "").replace(/\/$/, "");
  if (apiBase) {
    try {
      const response = await fetch(`${apiBase}/aispm/policy-context-gaps`);
      if (!response.ok) throw new Error(`Policy context gaps HTTP ${response.status}`);
      renderAispmPolicyContextGaps(await response.json(), "API local activity");
      return;
    } catch (error) {
      renderAispmPolicyContextGaps(aispmPolicyContextGapFallback, "API unavailable, sample shown");
      return;
    }
  }
  renderAispmPolicyContextGaps(aispmPolicyContextGapFallback, "static sample gaps");
}

function renderAispmPolicyContextGaps(packet, note = "sample context gaps") {
  const summary = packet.summary || {};
  const items = packet.items || [];
  const summaryCards = [
    ["Context Gaps", summary.total_gaps ?? 0, `${packet.data_provenance || "sample_data"} · ${note}`],
    ["Decisions", summary.decisions_with_gaps ?? items.length, "Decisions missing required business context"],
    ["Review Required", summary.requires_context_review ?? 0, `Monitor: ${summary.monitor ?? 0}`],
    ["Evidence", summary.evidence_confidence || "unknown", "Private enrichment stays Enterprise"]
  ];
  el("#aispmContextGapSummary").innerHTML = summaryCards.map(([label, value, detail]) => `
    <article class="trace-summary-card">
      <span>${escapeHtml(label)}</span>
      <strong>${escapeHtml(value)}</strong>
      <p>${escapeHtml(detail)}</p>
    </article>
  `).join("");
  el("#aispmPolicyContextGaps").innerHTML = items.slice(0, 8).map((item) => {
    const missing = (item.missing_context || []).slice(0, 8).map((field) => `<span>${escapeHtml(field.replaceAll("_", " "))}</span>`).join("");
    return `
      <article class="context-gap-row">
        <span class="severity ${escapeHtml(item.gap_status === "requires_context_review" ? "high" : "medium")}">${escapeHtml(item.gap_status || "monitor")}</span>
        <div>
          <strong>${escapeHtml(item.risk_classification || "policy_context_gap")}</strong>
          <p>${escapeHtml(item.recommended_action || "Attach missing business context before relying on the decision.")}</p>
          <small>${escapeHtml(item.agent_id || "unknown-agent")} · ${escapeHtml(item.repository || "local")} · ${escapeHtml(item.control_surface || "general_policy")}</small>
          <div class="risk-signal-list">${missing || "<span>context complete</span>"}</div>
        </div>
        <small>${escapeHtml((item.evidence_refs || []).join(", ") || "no evidence refs")}</small>
      </article>
    `;
  }).join("") || `<p class="empty-state">No policy context gaps detected in this activity window.</p>`;
}

function summarizePreActionForecasts(items) {
  const counts = (items || []).reduce((acc, item) => {
    acc[item.forecast_status] = (acc[item.forecast_status] || 0) + 1;
    if (["critical", "high"].includes(item.severity)) acc.criticalHigh += 1;
    return acc;
  }, { criticalHigh: 0 });
  return {
    total_forecasts: (items || []).length,
    critical_or_high_forecasts: counts.criticalHigh,
    approval_recommended: counts.approval_recommended || 0,
    block_recommended: counts.block_recommended || 0,
    warn_recommended: counts.warn_recommended || 0,
    evidence_confidence: (items || []).some((item) => (item.evidence_refs || []).length) ? "activity_evidence_refs" : "activity_metadata_only"
  };
}

async function loadAispmPreActionForecasts() {
  const apiBase = (window.CAVRA_API_BASE || "").replace(/\/$/, "");
  if (apiBase) {
    try {
      const response = await fetch(`${apiBase}/aispm/pre-action-risk-forecasts`);
      if (!response.ok) throw new Error(`Pre-action forecasts HTTP ${response.status}`);
      renderAispmPreActionForecasts(await response.json(), "API local activity");
      return;
    } catch (error) {
      renderAispmPreActionForecasts(aispmPreActionForecastFallback, "API unavailable, sample shown");
      return;
    }
  }
  renderAispmPreActionForecasts(aispmPreActionForecastFallback, "static sample forecasts");
}

function renderAispmPreActionForecasts(packet, note = "sample forecasts") {
  const summary = packet.summary || {};
  const items = packet.items || [];
  const summaryCards = [
    ["Forecasts", summary.total_forecasts ?? items.length, `${packet.data_provenance || "sample_data"} · ${note}`],
    ["Block", summary.block_recommended ?? 0, "Stop before execution"],
    ["Approval", summary.approval_recommended ?? 0, `Warn: ${summary.warn_recommended ?? 0}`],
    ["Critical/High", summary.critical_or_high_forecasts ?? 0, `Evidence: ${summary.evidence_confidence || "unknown"}`]
  ];
  el("#aispmForecastSummary").innerHTML = summaryCards.map(([label, value, detail]) => `
    <article class="trace-summary-card">
      <span>${escapeHtml(label)}</span>
      <strong>${escapeHtml(value)}</strong>
      <p>${escapeHtml(detail)}</p>
    </article>
  `).join("");
  el("#aispmPreActionForecasts").innerHTML = items.slice(0, 6).map((item) => {
    const impacts = (item.likely_impacts || []).slice(0, 4).map((impact) => `<span>${escapeHtml(impact.replaceAll("_", " "))}</span>`).join("");
    const controls = (item.pre_action_controls || []).slice(0, 4).map((control) => control.replaceAll("_", " ")).join(" · ");
    const status = String(item.forecast_status || "monitor").replaceAll("_", " ");
    const blastRadius = String(item.projected_blast_radius || "local_policy_scope").replaceAll("_", " ");
    const risk = String(item.risk_classification || "policy_decision_review").replaceAll("_", " ");
    return `
      <article class="forecast-card">
        <header>
          <div>
            <span>${escapeHtml(status)}</span>
            <strong>${escapeHtml(blastRadius)}</strong>
          </div>
          <span class="severity ${escapeHtml(item.severity || "low")}">${escapeHtml(item.severity || "low")}</span>
        </header>
        <p>${escapeHtml(item.target_summary || "target not recorded")} · ${escapeHtml(risk)}</p>
        <dl>
          <dt>Agent</dt><dd>${escapeHtml(item.agent_id || "unknown-agent")}</dd>
          <dt>Repo</dt><dd>${escapeHtml(item.repository || "local")}</dd>
          <dt>Control</dt><dd>${escapeHtml(controls || "record decision")}</dd>
        </dl>
        <div class="risk-signal-list">${impacts || "<span>policy visibility</span>"}</div>
      </article>
    `;
  }).join("") || `<p class="empty-state">No pre-action forecasts available for this activity window.</p>`;
}

function summarizeIntentActionDrift(items) {
  const counts = (items || []).reduce((acc, item) => {
    acc[item.drift_status] = (acc[item.drift_status] || 0) + 1;
    return acc;
  }, {});
  return {
    total_items: (items || []).length,
    high_drift: counts.high_drift || 0,
    needs_review: counts.needs_review || 0,
    unknown_intent: counts.unknown_intent || 0,
    aligned: counts.aligned || 0,
    evidence_confidence: (items || []).some((item) => (item.evidence_refs || []).length) ? "activity_evidence_refs" : "activity_metadata_only"
  };
}

async function loadAispmIntentActionDrift() {
  const apiBase = (window.CAVRA_API_BASE || "").replace(/\/$/, "");
  if (apiBase) {
    try {
      const response = await fetch(`${apiBase}/aispm/intent-action-drift`);
      if (!response.ok) throw new Error(`Intent drift HTTP ${response.status}`);
      renderAispmIntentActionDrift(await response.json(), "API local activity");
      return;
    } catch (error) {
      renderAispmIntentActionDrift(aispmIntentActionDriftFallback, "API unavailable, sample shown");
      return;
    }
  }
  renderAispmIntentActionDrift(aispmIntentActionDriftFallback, "static sample drift");
}

function renderAispmIntentActionDrift(packet, note = "sample drift") {
  const summary = packet.summary || {};
  const items = packet.items || [];
  const summaryCards = [
    ["Intent Rows", summary.total_items ?? items.length, `${packet.data_provenance || "sample_data"} · ${note}`],
    ["High Drift", summary.high_drift ?? 0, `Needs review: ${summary.needs_review ?? 0}`],
    ["Unknown Intent", summary.unknown_intent ?? 0, `Aligned: ${summary.aligned ?? 0}`],
    ["Evidence", summary.evidence_confidence || "unknown", "Raw prompt intent stays Enterprise"]
  ];
  el("#aispmIntentDriftSummary").innerHTML = summaryCards.map(([label, value, detail]) => `
    <article class="trace-summary-card">
      <span>${escapeHtml(label)}</span>
      <strong>${escapeHtml(value)}</strong>
      <p>${escapeHtml(detail)}</p>
    </article>
  `).join("");
  el("#aispmIntentActionDrift").innerHTML = items.slice(0, 8).map((item) => {
    const status = String(item.drift_status || "aligned").replaceAll("_", " ");
    const signals = (item.drift_signals || []).slice(0, 6).map((signal) => `<span>${escapeHtml(signal.replaceAll("_", " "))}</span>`).join("");
    const risk = String(item.risk_classification || "policy_decision_review").replaceAll("_", " ");
    return `
      <article class="intent-drift-row">
        <span class="intent-score">${escapeHtml(item.drift_score ?? 0)}</span>
        <div>
          <strong>${escapeHtml(status)} · ${escapeHtml(item.declared_intent || "intent not recorded")}</strong>
          <p>${escapeHtml(item.action_type || "unknown action")} → ${escapeHtml(item.target_summary || "target not recorded")} · ${escapeHtml(risk)}</p>
          <small>${escapeHtml(item.agent_id || "unknown-agent")} · ${escapeHtml(item.repository || "local")} · ${escapeHtml(item.decision || "recorded")}</small>
          <div class="risk-signal-list">${signals || "<span>aligned</span>"}</div>
        </div>
        <small>${escapeHtml(item.recommended_action || "Compare declared intent with observed action before allowing execution.")}</small>
      </article>
    `;
  }).join("") || `<p class="empty-state">No intent-to-action drift records available for this activity window.</p>`;
}

function summarizeToolChainGraph(graph) {
  const nodes = graph?.nodes || [];
  const edges = graph?.edges || [];
  return {
    node_count: nodes.length,
    edge_count: edges.length,
    agent_nodes: nodes.filter((node) => node.node_type === "agent").length,
    tool_nodes: nodes.filter((node) => node.node_type === "tool").length,
    target_nodes: nodes.filter((node) => node.node_type === "target").length,
    high_risk_edges: edges.filter((edge) => Number(edge.risk_score || 0) >= 70).length,
    blocked_edges: edges.filter((edge) => edge.decision === "block").length,
    evidence_confidence: edges.some((edge) => (edge.evidence_refs || []).length) ? "activity_evidence_refs" : "activity_metadata_only"
  };
}

async function loadAispmToolChainGraph() {
  const apiBase = (window.CAVRA_API_BASE || "").replace(/\/$/, "");
  if (apiBase) {
    try {
      const response = await fetch(`${apiBase}/aispm/tool-chain-graph`);
      if (!response.ok) throw new Error(`Tool graph HTTP ${response.status}`);
      renderAispmToolChainGraph(await response.json(), "API local activity");
      return;
    } catch (error) {
      renderAispmToolChainGraph(aispmToolChainGraphFallback, "API unavailable, sample shown");
      return;
    }
  }
  renderAispmToolChainGraph(aispmToolChainGraphFallback, "static sample graph");
}

function renderAispmToolChainGraph(packet, note = "sample graph") {
  const summary = packet.summary || summarizeToolChainGraph(packet);
  const nodes = packet.nodes || [];
  const edges = packet.edges || [];
  const hotspots = packet.hotspots || [];
  const summaryCards = [
    ["Graph", `${summary.node_count ?? nodes.length} nodes`, `${summary.edge_count ?? edges.length} edges · ${note}`],
    ["High-Risk Edges", summary.high_risk_edges ?? 0, `Blocked: ${summary.blocked_edges ?? 0}`],
    ["Tools/Targets", `${summary.tool_nodes ?? 0}/${summary.target_nodes ?? 0}`, `Agents: ${summary.agent_nodes ?? 0}`],
    ["Evidence", summary.evidence_confidence || "unknown", "Raw payloads stay Enterprise"]
  ];
  el("#aispmToolGraphSummary").innerHTML = summaryCards.map(([label, value, detail]) => `
    <article class="trace-summary-card">
      <span>${escapeHtml(label)}</span>
      <strong>${escapeHtml(value)}</strong>
      <p>${escapeHtml(detail)}</p>
    </article>
  `).join("");
  el("#aispmToolGraphNodes").innerHTML = hotspots.slice(0, 4).map((hotspot) => `
    <article class="tool-node-card">
      <span class="severity ${escapeHtml(hotspot.risk_band || "low")}">${escapeHtml(hotspot.risk_band || "low")}</span>
      <strong>${escapeHtml(hotspot.agent_id || "unknown-agent")} · ${escapeHtml(hotspot.repository || "local")}</strong>
      <p>${escapeHtml(String(hotspot.dominant_surface || "general_policy").replaceAll("_", " "))} · ${escapeHtml(hotspot.decision_count ?? 0)} decisions</p>
      <small>${escapeHtml((hotspot.evidence_refs || []).join(", ") || "no evidence refs")}</small>
    </article>
  `).join("") || nodes.slice(0, 6).map((node) => `
    <article class="tool-node-card">
      <span class="severity ${escapeHtml(node.risk_band || "low")}">${escapeHtml(node.node_type || "node")}</span>
      <strong>${escapeHtml(node.label || node.node_id || "unknown")}</strong>
      <p>${escapeHtml(node.risk_band || "observed")} · ${escapeHtml(node.decision_count ?? 0)} decisions</p>
    </article>
  `).join("") || `<p class="empty-state">No tool graph nodes available.</p>`;
  el("#aispmToolGraphEdges").innerHTML = edges.slice(0, 8).map((edge) => {
    const relationship = String(edge.relationship || "observed").replaceAll("_", " ");
    const risk = String(edge.risk_classification || "policy_decision_review").replaceAll("_", " ");
    return `
      <article class="tool-edge-row">
        <span class="tool-risk-score">${escapeHtml(edge.risk_score ?? 0)}</span>
        <div>
          <strong>${escapeHtml(relationship)} · ${escapeHtml(edge.decision || "recorded")}</strong>
          <p>${escapeHtml(edge.source || "source")} → ${escapeHtml(edge.target || "target")} · ${escapeHtml(risk)}</p>
          <small>${escapeHtml(edge.agent_id || "unknown-agent")} · ${escapeHtml(edge.repository || "local")} · ${escapeHtml(edge.control_surface || "general_policy")}</small>
        </div>
        <small>${escapeHtml((edge.evidence_refs || []).join(", ") || "metadata only")}</small>
      </article>
    `;
  }).join("") || `<p class="empty-state">No tool-chain edges available for this activity window.</p>`;
}

function summarizeAgentBlastRadius(items) {
  const rows = items || [];
  const counts = rows.reduce((acc, item) => {
    const level = item.blast_radius_level || "low";
    acc[level] = (acc[level] || 0) + 1;
    for (const repository of item.repositories || []) acc.repositories.add(repository);
    for (const path of item.approval_paths || []) acc.approvalPaths.add(path);
    return acc;
  }, { repositories: new Set(), approvalPaths: new Set() });
  return {
    total_agents: rows.length,
    critical_agents: counts.critical || 0,
    high_agents: counts.high || 0,
    medium_agents: counts.medium || 0,
    low_agents: counts.low || 0,
    affected_repositories: counts.repositories.size,
    approval_paths: counts.approvalPaths.size,
    evidence_confidence: rows.some((item) => (item.evidence_refs || []).length) ? "activity_evidence_refs" : "activity_metadata_only"
  };
}

async function loadAispmAgentBlastRadius() {
  const apiBase = (window.CAVRA_API_BASE || "").replace(/\/$/, "");
  if (apiBase) {
    try {
      const response = await fetch(`${apiBase}/aispm/agent-blast-radius`);
      if (!response.ok) throw new Error(`Agent blast-radius HTTP ${response.status}`);
      renderAispmAgentBlastRadius(await response.json(), "API local activity");
      return;
    } catch (error) {
      renderAispmAgentBlastRadius(aispmAgentBlastRadiusFallback, "API unavailable, sample shown");
      return;
    }
  }
  renderAispmAgentBlastRadius(aispmAgentBlastRadiusFallback, "static sample map");
}

function renderAispmAgentBlastRadius(packet, note = "sample blast radius") {
  const items = packet.items || [];
  const summary = packet.summary || summarizeAgentBlastRadius(items);
  const summaryCards = [
    ["Agents", summary.total_agents ?? items.length, `${packet.data_provenance || "sample_data"} · ${note}`],
    ["Critical/High", (summary.critical_agents ?? 0) + (summary.high_agents ?? 0), `Medium: ${summary.medium_agents ?? 0}`],
    ["Repositories", summary.affected_repositories ?? 0, `Approval paths: ${summary.approval_paths ?? 0}`],
    ["Evidence", summary.evidence_confidence || "unknown", "Private topology stays Enterprise"]
  ];
  el("#aispmBlastRadiusSummary").innerHTML = summaryCards.map(([label, value, detail]) => `
    <article class="trace-summary-card">
      <span>${escapeHtml(label)}</span>
      <strong>${escapeHtml(value)}</strong>
      <p>${escapeHtml(detail)}</p>
    </article>
  `).join("");
  el("#aispmAgentBlastRadius").innerHTML = items.slice(0, 6).map((item) => {
    const surfaces = (item.control_surfaces || []).map((surface) => surface.replaceAll("_", " ")).join(", ") || "general policy";
    const risks = (item.top_risks || []).slice(0, 5).map((risk) => `<span>${escapeHtml(risk.replaceAll("_", " "))}</span>`).join("");
    const controls = (item.recommended_controls || []).slice(0, 5).map((control) => `<span>${escapeHtml(control.replaceAll("_", " "))}</span>`).join("");
    return `
      <article class="blast-radius-card">
        <header>
          <div>
            <span class="severity ${escapeHtml(item.blast_radius_level || "low")}">${escapeHtml(item.blast_radius_level || "low")}</span>
            <strong>${escapeHtml(item.agent_id || "unknown-agent")}</strong>
          </div>
          <b class="blast-radius-score">${escapeHtml(item.blast_radius_score ?? 0)}</b>
        </header>
        <p>${escapeHtml((item.repositories || []).join(", ") || "local")} · ${escapeHtml(surfaces)}</p>
        <dl>
          <dt>Targets</dt><dd>${escapeHtml((item.target_classes || []).map((target) => target.replaceAll("_", " ")).join(", ") || "not observed")}</dd>
          <dt>Tools</dt><dd>${escapeHtml((item.tool_labels || []).join(", ") || "not observed")}</dd>
          <dt>Policy Packs</dt><dd>${escapeHtml((item.policy_packs || []).join(", ") || "not observed")}</dd>
          <dt>Actions</dt><dd>${escapeHtml(item.decision_count ?? 0)} decisions · ${escapeHtml(item.blocked_actions ?? 0)} blocked · ${escapeHtml(item.approval_required_actions ?? 0)} approval-gated</dd>
        </dl>
        <div class="risk-signal-list">${risks || "<span>local policy scope</span>"}</div>
        <div class="risk-signal-list">${controls || "<span>capture signed evidence</span>"}</div>
      </article>
    `;
  }).join("") || `<p class="empty-state">No agent blast-radius records available for this activity window.</p>`;
}

function renderAispmTraceReplay(packet, note = "sample replay") {
  const summary = packet.summary || {};
  const session = packet.session || {};
  el("#aispmTraceStatus").textContent = `${packet.data_provenance || "sample_data"} · ${note}`;
  const summaryCards = [
    ["Session", session.session_id || "unknown", `${session.agent_id || "unknown-agent"} · ${session.repository || "local"}`],
    ["Replay Steps", summary.step_count ?? 0, `Critical/high: ${summary.critical_or_high_steps ?? 0}`],
    ["Blocked", summary.blocked_actions ?? 0, `Approval gates: ${summary.approval_required_actions ?? 0}`],
    ["Evidence", summary.evidence_confidence || "unknown", `${(packet.evidence_refs || []).length} references`]
  ];
  el("#aispmTraceSummary").innerHTML = summaryCards.map(([label, value, detail]) => `
    <article class="trace-summary-card">
      <span>${escapeHtml(label)}</span>
      <strong>${escapeHtml(value)}</strong>
      <p>${escapeHtml(detail)}</p>
    </article>
  `).join("");
  el("#aispmTraceSteps").innerHTML = (packet.steps || []).map((step) => `
    <article class="trace-step">
      <span class="trace-step-number">${escapeHtml(step.step || "-")}</span>
      <div>
        <strong>${escapeHtml(step.decision || "recorded")} · ${escapeHtml(step.action_type || "unknown")}</strong>
        <p>${escapeHtml(step.reason || "CAVRA policy decision recorded.")}</p>
        <small>${escapeHtml(step.target_summary || "target not recorded")} · ${escapeHtml(step.risk_classification || "policy_decision_review")}</small>
      </div>
      <span class="severity ${escapeHtml(step.severity || "low")}">${escapeHtml(step.severity || "low")}</span>
    </article>
  `).join("") || `<p class="empty-state">No replay steps available for this session.</p>`;
  const redaction = packet.redaction || {};
  el("#aispmTraceRedaction").innerHTML = Object.entries(redaction).map(([key, value]) => `
    <div>
      <span>${escapeHtml(key.replaceAll("_", " "))}</span>
      <strong>${escapeHtml(value)}</strong>
    </div>
  `).join("");
  el("#aispmTracePayload").textContent = JSON.stringify(packet, null, 2);
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
  el("#refreshAispmApprovals").addEventListener("click", loadAispmApprovalLineage);
  el("#refreshAispmCoverageHeatmap").addEventListener("click", loadAispmControlCoverageHeatmap);
  el("#refreshAispmEvidenceConfidence").addEventListener("click", loadAispmEvidenceConfidence);
  el("#refreshAispmEvidenceFreshness").addEventListener("click", loadAispmEvidenceFreshness);
  el("#refreshAispmExecutiveNarrative").addEventListener("click", loadAispmExecutiveNarrative);
  el("#refreshAispmReplayPolicy").addEventListener("click", loadAispmReplayPolicy);
  el("#copyAispmReplayPolicyTests").addEventListener("click", copyAispmReplayPolicyTests);
  el("#downloadAispmReplayPolicyTests").addEventListener("click", downloadAispmReplayPolicyTests);
  el("#copyAispmReplayPolicyReviewPacket").addEventListener("click", copyAispmReplayPolicyReviewPacket);
  el("#downloadAispmReplayPolicyReviewPacket").addEventListener("click", downloadAispmReplayPolicyReviewPacket);
  el("#copyAispmReplayPolicyCiGateReadiness").addEventListener("click", copyAispmReplayPolicyCiGateReadiness);
  el("#downloadAispmReplayPolicyCiGateReadiness").addEventListener("click", downloadAispmReplayPolicyCiGateReadiness);
  el("#copyAispmReplayPolicyCiGateRollout").addEventListener("click", copyAispmReplayPolicyCiGateRollout);
  el("#downloadAispmReplayPolicyCiGateRollout").addEventListener("click", downloadAispmReplayPolicyCiGateRollout);
  el("#copyAispmReplayPolicyCiGateAuditPacket").addEventListener("click", copyAispmReplayPolicyCiGateAuditPacket);
  el("#downloadAispmReplayPolicyCiGateAuditPacket").addEventListener("click", downloadAispmReplayPolicyCiGateAuditPacket);
  el("#refreshAispmFingerprints").addEventListener("click", loadAispmBehaviorFingerprints);
  el("#refreshAispmContextGaps").addEventListener("click", loadAispmPolicyContextGaps);
  el("#refreshAispmForecasts").addEventListener("click", loadAispmPreActionForecasts);
  el("#refreshAispmIntentDrift").addEventListener("click", loadAispmIntentActionDrift);
  el("#refreshAispmToolGraph").addEventListener("click", loadAispmToolChainGraph);
  el("#refreshAispmBlastRadius").addEventListener("click", loadAispmAgentBlastRadius);
  el("#aispmTraceSession").addEventListener("change", (event) => {
    loadAispmTraceReplay(event.target.value);
    loadAispmReplayPolicy();
  });
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
  loadAispmApprovalLineage();
  loadAispmControlCoverageHeatmap();
  loadAispmBehaviorFingerprints();
  loadAispmPolicyContextGaps();
  loadAispmPreActionForecasts();
  loadAispmIntentActionDrift();
  loadAispmToolChainGraph();
  loadAispmAgentBlastRadius();
  if (localStorage.getItem("cavra.sidebarCollapsed") === "true") el("#sidebar").classList.add("is-collapsed");
  setRoute(location.hash.slice(1) || localStorage.getItem("cavra.activeRoute") || "dashboard");
}

init();
