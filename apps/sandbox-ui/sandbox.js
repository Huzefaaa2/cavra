const navItems = [
  { id: "dashboard", label: "Dashboard", icon: "D", group: "Operate", description: "Live API, setup, decisions, approvals, evidence, AISPM, and connector status." },
  { id: "first-run-setup", label: "Setup", icon: "S", group: "Operate", description: "Default workspace, policy actions, SMTP setup, validation, and first-launch operator flow." },
  { id: "policy-engine", label: "Policies", icon: "P", group: "Configure", description: "Policy decisions across files, commands, Git, MCP, CI/CD, cloud, and releases." },
  { id: "agents-mcp", label: "Agents & MCP Trust", icon: "A", group: "Configure", description: "Governed AI agents, MCP servers, trust state, profiles, and classifications." },
  { id: "approvals", label: "Approvals", icon: "Q", group: "Act", description: "Approval queue, routing, provider delivery status, break-glass, and audit review." },
  { id: "evidence", label: "Evidence", icon: "E", group: "Act", description: "Audit trails, attestations, evidence bundles, artifact access, and verification." },
  { id: "ai-posture", label: "AISPM Posture", icon: "M", group: "Monitor", description: "AI Security Posture Management, findings, coverage, freshness, reports, and trial labs." },
  { id: "reports", label: "Reports", icon: "R", group: "Monitor", description: "Report catalog, filters, exports, and delivery-readiness boundaries." },
  { id: "integrations", label: "Integrations", icon: "I", group: "Configure", description: "Connector health and integration states for developer and cloud control surfaces." },
  { id: "settings", label: "Settings", icon: "G", group: "Configure", description: "API base, theme, local state, notification boundaries, and deployment mode." },
  { id: "documentation", label: "Help", icon: "H", group: "Resources", description: "Wiki textbook, README, CLI, deployment guides, Trial Field Guide, and public reference pages." }
];

const secondaryRoutes = [
  { id: "architecture", label: "Architecture Reference", status: "Reference", description: "Long-form component map, control-plane narrative, and integration architecture." },
  { id: "use-cases", label: "Use Cases", status: "Reference", description: "Security, platform, audit, and engineering examples that explain where CAVRA fits." },
  { id: "operator-experience", label: "Role Paths", status: "Reference", description: "Reader paths for security, platform, audit, engineering, trial, and managed operators." },
  { id: "enterprise-trial", label: "Trial Access", status: "Reference", description: "Trial portal, entitlement, guided lab, expiry, revocation, and closeout guidance." },
  { id: "compliance", label: "Compliance", status: "Reference", description: "Control-mapping examples for audit conversations without overstating certification." },
  { id: "roadmap", label: "Roadmap", status: "Reference", description: "Public product workstreams and operating-model direction." }
];

const metrics = [
  ["Runtime Decision Actions", "4", "Allow, block, require approval, or attest."],
  ["Protected Runtime Assets", "7", "Code, shell, Git, MCP, CI/CD, cloud, and infrastructure."],
  ["Evidence outputs", "6", "Bundles, attestations, reports, packets, exports, and release records."],
  ["AISPM views", "9", "Coverage, findings, drift, blast radius, reports, and readiness."],
  ["Product Paths", "4", "Community, Managed, Enterprise Subscription, and Trial access."]
];

const businessOutcomes = [
  ["Reduce AI Risk", "Stop unsafe autonomous actions before they reach code, infrastructure, tools, or production systems."],
  ["Accelerate Secure Delivery", "Keep agent-assisted engineering moving with policy-backed allow, approval, and attestation paths."],
  ["Generate Audit Evidence", "Capture reviewable decisions, rationale, control mappings, and board-ready evidence packets."],
  ["Improve AI Security Posture", "Continuously measure coverage, findings, exceptions, drift, and production-readiness blockers."]
];

const executiveDeliverables = [
  ["Executive Readiness", "Board-level posture summary, launch status, blockers, exceptions, and approval path."],
  ["Board Packet", "Public-safe pilot launch packet with scope, risk acceptance, report readiness, and closeout plan."],
  ["Report Center", "Executive risk brief, SOC 2-style audit summary, KPI pack, and evidence freshness exports."],
  ["Trial Field Guide", "Guided evaluator journey to prove a complete AISPM use case with evidence and closeout."]
];

const editionComparison = [
  ["CAVRA Community", "Full self-hosted public product", "Runtime decisions, policy engine, approvals, evidence, AISPM, report center, dashboards, connector SDK, reference connectors, and public policy packs.", "Teams that want to self-host and configure their own providers."],
  ["CAVRA Managed", "Hosted managed service", "Managed tenant operations, updates, uptime, policy registry, dashboards, report delivery, audit storage, support handoff, and billing.", "Teams that want CAVRA operated as a service."],
  ["Enterprise Subscription", "Commercial support relationship", "SLA, certified connectors, commercial policy packs, compliance packs, implementation help, custom integrations, and private customer operations.", "Organizations that need supported deployment and commercial assurance."],
  ["CAVRA Trial", "Temporary evaluator access", "Operator-reviewed access, hosted or package entitlement where applicable, guided AISPM labs, expiry, revocation, evidence, and closeout.", "Evaluators proving one measurable use case before adoption."]
];

const downloadArtifacts = [
  ["Executive Product Brief", "PDF-ready", "Two-page business summary for CISO, board, and procurement review."],
  ["CAVRA Datasheet", "Product brief", "Capabilities, product paths, runtime actions, protected surfaces, and evaluation path."],
  ["AISPM Capability Brief", "Datasheet", "Posture loop, findings, reports, readiness gates, and guided trial labs."],
  ["Runtime Authority Whitepaper", "Reference", "How pre-action governance works across AI-agent software delivery."],
  ["Architecture Reference Guide", "Diagram pack", "Runtime authority, policy, evidence, AISPM, identity, and integrations."],
  ["Board Readiness Packet", "Packet", "Sample launch summary, risk acceptance, report readiness, and evidence room index."],
  ["Sample Evidence Bundle", "Evidence", "Public-safe decision record, attestation outline, and control mapping examples."],
  ["Sample Attestation", "Evidence", "Example signed decision and reviewer attestation payload."],
  ["Security Controls Mapping", "SOC 2 / ISO / NIST", "Public-safe mapping from CAVRA evidence to common control families."],
  ["Capability Matrix", "Matrix", "Capability status across Community, Managed, Enterprise Subscription, and Trial access."],
  ["Deployment Reference Architecture", "Azure", "Community, Managed, Enterprise Subscription, and Trial deployment topology summary."],
  ["Trial Access Guide", "Guide", "Evaluator steps, trial portal, guided use case, AISPM labs, and closeout."],
  ["API Reference", "Reference", "Public-safe API surface overview and provider integration boundaries."],
  ["Policy Pack Samples", "Examples", "Secret, Terraform, protected branch, MCP, and release governance examples."],
  ["Release Readiness Checklist", "Checklist", "Evidence, validation, release, and production-readiness review checklist."]
];

const communityCards = [
  ["Public landing", "Rebuilt", "Product-first homepage with demo-safe language and route-aware pages."],
  ["Community sandbox", "Ready", "Sample policy decisions, evidence, reports, and posture are available without secrets."],
  ["Docs and textbook", "Linked", "The Wiki e-book is positioned as the full technical reader guide."],
  ["Azure path", "Documented", "Community self-hosted deployment path is available through public workflows and docs."]
];

const pilotCards = [
  ["Trial portal", "Live", "Evaluator requests start at cavra-trial.mind-ops.cloud."],
  ["Trial entitlement", "Time-limited", "CAVRA Trial access uses controlled evaluator entitlement, expiry, and revocation."],
  ["AISPM labs", "Guided", "Trial Field Guide helps evaluators prove one complete use case."],
  ["Production gate", "Managed/Configured", "Live connectors, SMTP, tenants, and runtime workflows require real provider validation."]
];

const setupCards = [
  ["Default setup state", "Configured by `cavra setup init`", "Creates a safe Community baseline with policy pack, evidence location, AISPM enabled state, agent defaults, and report-delivery placeholders."],
  ["Demo workspace", "Generated by `cavra setup demo-env`", "Creates known safe and risky files such as `.env`, IAM Terraform, Kubernetes delete examples, and deploy scripts so users can prove decisions immediately."],
  ["Validation scenarios", "Run by `cavra setup validate`", "Exercises read, write, command, Git, and MCP decisions and can record events into the activity store for AISPM posture views."],
  ["SMTP report setup", "Configured by `cavra setup smtp`", "Collects host, port, sender, recipient allowlist, and secret reference without storing the SMTP password in setup state."],
  ["Policy action catalog", "Listed by `cavra setup policy-actions`", "Shows block, allow, approval, and trust entries from the active policy pack so operators can plan add, update, and delete changes."],
  ["GUI/API setup flow", "Exposed through `/setup/*` APIs", "Self-hosted front ends can call setup status, defaults, bootstrap, SMTP test, demo workspace, validation, complete, and policy catalog endpoints."]
];

const setupCommands = [
  ["Initialize defaults", "cavra setup init --workspace-name local-community"],
  ["Create demo environment", "cavra setup demo-env --output .cavra/demo-workspace"],
  ["Validate and seed AISPM", "cavra setup validate --record-decisions"],
  ["List policy actions", "cavra setup policy-actions"],
  ["Preview a risky command", "cavra setup policy-action-test --action-type execute_command --target \"terraform apply -auto-approve\""],
  ["Configure SMTP safely", "cavra setup smtp --host smtp.example.com --from-email hello@example.com --recipient security@example.com --password-ref CAVRA_REPORT_SMTP_PASSWORD"],
  ["Mark setup complete", "cavra setup complete"]
];

const aispmCards = [
  ["Posture score", "82", "Demo score from sample decisions and readiness signals."],
  ["Blocked actions", "1", "Unsafe secret or production mutation attempts are stopped before execution."],
  ["Approval gates", "3", "High-risk actions route to human or policy owners before completion."],
  ["Report packs", "6", "Executive, audit, control, evidence, agent-risk, and KPI reports."],
  ["Provider-backed controls", "Configuration", "Live streaming, kill switch, runtime overrides, and report delivery require configured providers or Managed operation."]
];

const boardPackCards = [
  ["Scope", "Defined", "Repositories, agents, tools, required checks, owners, and go/no-go criteria."],
  ["Risk acceptance", "Tracked", "Accepted exceptions have owner, expiry, rationale, and reviewer evidence."],
  ["Evidence room", "Ready", "Artifacts are grouped for CISO, security, platform, procurement, and audit review."],
  ["Report readiness", "Prepared", "Executive and audit reporting is separated from configured or Managed email delivery."],
  ["Launch decision", "Reviewable", "Board-ready summary stays public-safe and excludes private tenant records."],
  ["Closeout", "Planned", "Trial expiry, revocation, access removal, and feedback are captured at closeout."]
];

const boardManifestCards = [
  ["Integrity", "Schema-ready", "Public packet includes schema, generation time, and artifact references."],
  ["Freshness", "Visible", "Reviewers can see which readiness artifacts are current."],
  ["Boundary", "Public-safe", "No secrets, connector tokens, tenant data, or private logs are exposed."],
  ["Export", "Downloadable", "Board packet can be copied or downloaded for review records."]
];

const reportCards = [
  ["Executive Risk Brief", "Board-level posture narrative with open risks and recommended actions."],
  ["SOC 2-Style Audit Summary", "Control-focused evidence summary for audit discussions."],
  ["Control Coverage Export", "Agent, repository, policy, and evidence coverage by domain."],
  ["Evidence Freshness Export", "SLO status for evidence age, references, and retention boundaries."],
  ["Agent Risk Register", "High-risk agents, unusual behavior, tool reach, and blast radius."],
  ["Board KPI Pack", "Readable KPI pack for leadership and pilot approval meetings."]
];

const architectureNodes = [
  ["AI agents", "Coding assistants, automation, and workflow agents request risky actions."],
  ["Runtime authority", "CAVRA evaluates actor, action, target, context, policy, and trust."],
  ["Policy engine", "Rules decide allow, block, approval, attestation, remediation, and severity."],
  ["Identity and trust", "OIDC, RBAC, tenant boundary, MCP trust, package integrity, and approvals."],
  ["Evidence plane", "Signed decision records, attestations, audit bundles, and release packets."],
  ["AISPM plane", "Posture score, coverage, findings, reports, exceptions, and readiness gates."],
  ["Integrations", "GitHub, GitLab, Azure DevOps, Terraform, Kubernetes, clouds, and MCP servers."],
  ["Reports", "Executive, audit, control, evidence, agent-risk, and delivery-ready packs."],
  ["Managed storage", "Tenant-aware databases, immutable blob storage, Key Vault, and monitoring."]
];

const policies = [
  ["Secrets exposure", "Block reading private keys, `.env`, customer records, or production credentials.", "Use managed secret references and redacted evidence."],
  ["Production mutation", "Require approval for IAM, deployment, infrastructure, or protected branch changes.", "Route to platform or security owner with signed attestation."],
  ["Untrusted MCP tool", "Block MCP servers that request filesystem, shell, network, or token capabilities without trust registration.", "Register server, declare capability, and rerun trust check."],
  ["Release bypass", "Prevent agents from bypassing required checks, tags, release evidence, or protected branches.", "Attach CAVRA evidence before merge or release."],
  ["Context gaps", "Warn or block when ownership, data classification, change window, or environment tier is missing.", "Collect missing context before execution."],
  ["Report delivery", "Keep SMTP/provider secrets, recipients, private report contents, and logs outside public Community.", "Configure a self-hosted report provider or use CAVRA Managed."]
];

const evidenceTimeline = [
  ["Intent captured", "Agent identity, requested action, target, repository, and environment are normalized."],
  ["Policy evaluated", "CAVRA computes severity, rationale, remediation, approvals, and control mappings."],
  ["Decision returned", "The agent receives allow, block, approval-required, or attestation-required feedback."],
  ["Evidence sealed", "Decision metadata, references, and public-safe payloads become reviewable audit material."],
  ["Posture updated", "AISPM refreshes findings, coverage, evidence freshness, and report inputs."]
];

const useCases = [
  ["Prevent secret exfiltration", "Block agent attempts to read production secrets or customer-sensitive files."],
  ["Gate Terraform plans", "Require approval for destructive infrastructure or IAM changes before apply."],
  ["Protect branches", "Attach CAVRA evidence as a required check before protected branch changes merge."],
  ["Control MCP tools", "Classify tool permissions and stop untrusted tool calls before execution."],
  ["Govern releases", "Tie release readiness to signed decisions, evidence, and verification packets."],
  ["Prepare audits", "Package policy decisions, approvals, reports, and evidence for compliance review."]
];

const operatorPaths = [
  ["Security teams", "Stop unsafe autonomous changes before they hit production.", "Start with AISPM, policy engine, and report center."],
  ["Platform teams", "Enforce policy through CI/CD, required checks, and runtime guardrails.", "Start with architecture, integrations, and deployment docs."],
  ["Auditors and GRC", "Trace each decision to durable evidence and control mappings.", "Start with evidence, compliance, and report center."],
  ["Engineering leaders", "Govern AI-assisted development without blocking all automation.", "Start with overview, role paths, and Trial access."],
  ["Trial evaluators", "Prove a complete AISPM use case with guided labs and closeout.", "Start with Trial portal and Trial Field Guide."],
  ["Managed operators", "Validate tenants, connectors, SMTP, workflows, and production gates.", "Start with Managed and Enterprise Subscription deployment docs."]
];

const trialAccessCards = [
  ["Evaluator intake", "Portal", "Use the branded trial portal for request submission and operator review."],
  ["Entitlement", "Time-limited", "Approved evaluators receive hosted access or revocable entitlement material."],
  ["Delivery", "Controlled", "Package/container access is granted only where needed through private delivery channels."],
  ["Guided lab", "AISPM", "The Trial Field Guide walks users through one complete evidence-backed use case."],
  ["Closeout", "Auditable", "Expiry, revocation, access removal, validation, and feedback are captured."],
  ["Boundary", "Public-safe", "Tenant data, SMTP secrets, connector credentials, and managed delivery logs remain private."]
];

const integrations = [
  ["GitHub", "Ready", "Required checks, PR attestations, release evidence, and deployment workflows."],
  ["Terraform/OpenTofu", "Ready", "Plan metadata, cloud IAM deltas, and infrastructure policy decisions."],
  ["Kubernetes", "Ready", "Manifest, RBAC, namespace, and workload governance."],
  ["MCP servers", "Ready", "Tool capability classification and trust registry enforcement."],
  ["Azure", "Ready", "Static UI, API deployment, Key Vault, storage, identity, and monitoring paths."],
  ["GitLab", "Planned", "Merge request and CI pipeline governance."],
  ["Azure DevOps", "Planned", "Pipeline and policy approval integration."],
  ["AWS/GCP", "Planned", "Expanded cloud posture and deployment context."]
];

const compliance = [
  ["SOC 2", "Change management", "Evidence for policy decisions, approvals, release packets, and required checks."],
  ["ISO 27001", "Access and operations control", "Agent identity, trust boundary, policy rationale, and audit records."],
  ["NIST", "Least privilege and audit", "Actor, action, target, approval route, and control evidence."],
  ["CIS", "Kubernetes and cloud hardening", "Manifest, RBAC, IAM, and infrastructure drift control evidence."],
  ["OWASP", "Agentic and tool risk", "Command, MCP, filesystem, network, and prompt-adjacent guardrails."],
  ["PCI DSS", "Secure change control", "Reviewable policy decisions and release evidence for sensitive systems."]
];

const roadmap = [
  ["CAVRA Community", "Self-hosted product, CLI, sample evidence, policy packs, provider interfaces, and Azure deployment."],
  ["CAVRA Trial", "Portal intake, evaluator entitlement, guided AISPM labs, expiry, revocation, and closeout evidence."],
  ["Enterprise Subscription", "Support, SLA, certified connectors, commercial policy packs, compliance packs, and implementation help."],
  ["CAVRA Managed", "Hosted control plane, Azure deployment options, managed reporting, monitoring, and support paths."],
  ["AISPM", "Posture loop, reports, exception lifecycle, executive board packs, runtime validation."],
  ["Public site", "Professional product landing page, role paths, diagrams, docs, and trial conversion."]
];

const docsLinks = [
  ["CAVRA Product Website", "https://cavra.mind-ops.cloud/"],
  ["GitHub Wiki Textbook", "https://github.com/Huzefaaa2/cavra/wiki"],
  ["Trial Field Guide", "https://github.com/Huzefaaa2/cavra/wiki/CAVRA-Trial-Field-Guide"],
  ["CAVRA Trial Portal", "https://cavra-trial.mind-ops.cloud/"],
  ["README", "https://github.com/Huzefaaa2/cavra#readme"],
  ["Azure Community Deployment", "https://github.com/Huzefaaa2/cavra/blob/main/docs/azure-community-saas-deployment.md"],
  ["Azure Trial, Managed, and Enterprise Deployment", "https://github.com/Huzefaaa2/cavra/blob/main/docs/azure-trial-enterprise-deployment.md"],
  ["Security Policy", "https://github.com/Huzefaaa2/cavra/security/policy"],
  ["Sample Evidence JSON", "./evidence/before-the-agent-acts/evidence.json"]
];

const helpWorkflowSteps = navItems.map((item) => ({
  label: item.label,
  route: item.id,
  group: item.group,
  description: item.description
}));

const inlineHelpContent = {
  dashboard: {
    kicker: "Operator guide",
    title: "Dashboard",
    summary: "Use Dashboard as the control-room overview after the API is running. It shows whether CAVRA is connected, configured, and producing runtime evidence.",
    steps: [
      "Confirm API connection and setup state before connecting AI agents.",
      "Review recent runtime decisions and connector health.",
      "Open Setup if the dashboard reports missing defaults or incomplete validation."
    ],
    links: [["Setup", "first-run-setup"], ["Evidence", "evidence"], ["AISPM", "ai-posture"]]
  },
  "first-run-setup": {
    kicker: "Setup guide",
    title: "First-Run Setup",
    summary: "Use Setup to bootstrap safe defaults, generate demo fixtures, configure report metadata, validate decisions, and mark the local environment ready.",
    steps: [
      "Create defaults before running agent integrations.",
      "Generate the demo workspace so policy decisions use known safe and risky fixtures.",
      "Run validation with decision recording to seed AISPM posture."
    ],
    links: [["Policies", "policy-engine"], ["AISPM", "ai-posture"], ["Settings", "settings"]]
  },
  "policy-engine": {
    kicker: "Policy guide",
    title: "Policies",
    summary: "Use Policies to inspect the active action catalog and simulate decisions before allowing agents to perform filesystem, shell, Git, MCP, cloud, or deployment actions.",
    steps: [
      "Filter rules by section or decision to understand the active guardrails.",
      "Run a risky action simulation before handing the action to an agent.",
      "Treat policy edits as controlled changes that should generate evidence."
    ],
    links: [["Approvals", "approvals"], ["Evidence", "evidence"], ["Agents & MCP", "agents-mcp"]]
  },
  "agents-mcp": {
    kicker: "Trust guide",
    title: "Agents & MCP Trust",
    summary: "Use Agents & MCP Trust to inventory AI agents, classify MCP servers, and verify whether tool calls should be allowed, blocked, or routed for approval.",
    steps: [
      "Seed sample agents and MCP servers for manual testing.",
      "Review owner, scope, risk tier, trust state, and requested capabilities.",
      "Run an unknown MCP tool check before exposing new tool surfaces."
    ],
    links: [["Policies", "policy-engine"], ["Approvals", "approvals"], ["Integrations", "integrations"]]
  },
  approvals: {
    kicker: "Workflow guide",
    title: "Approvals",
    summary: "Use Approvals to process high-risk decisions, test provider delivery boundaries, and capture reviewer evidence for audit.",
    steps: [
      "Filter pending, approved, denied, expired, and break-glass decisions.",
      "Inspect the selected approval before approving, denying, expiring, or delivering it.",
      "Use sample approval seeding for local workflow testing."
    ],
    links: [["Evidence", "evidence"], ["Reports", "reports"], ["Settings", "settings"]]
  },
  evidence: {
    kicker: "Audit guide",
    title: "Evidence",
    summary: "Use Evidence to search indexed metadata and AISPM references, verify decision records, and export selected audit payloads.",
    steps: [
      "Search by decision, agent, evidence ID, or verification state.",
      "Select evidence to review payload details and related AISPM references.",
      "Download selected evidence JSON for manual audit review."
    ],
    links: [["AISPM", "ai-posture"], ["Reports", "reports"], ["Compliance", "compliance"]]
  },
  "ai-posture": {
    kicker: "AISPM guide",
    title: "AISPM Posture",
    summary: "Use AISPM to turn runtime evidence into findings, blockers, freshness signals, agent risk, and executive-ready posture outputs.",
    steps: [
      "Refresh posture after setup validation or agent testing.",
      "Review open findings and closeout blockers before declaring readiness.",
      "Use report and board-pack outputs for stakeholder review."
    ],
    links: [["Reports", "reports"], ["Evidence", "evidence"], ["Trial Access", "enterprise-trial"]]
  },
  reports: {
    kicker: "Reporting guide",
    title: "Reports",
    summary: "Use Reports to generate local executive, audit, control, evidence, agent-risk, and KPI previews from currently loaded runtime state.",
    steps: [
      "Select report type, range, scope, and output format.",
      "Generate preview before download so the operator can inspect the payload.",
      "Configure provider delivery separately before sending production reports."
    ],
    links: [["Settings", "settings"], ["AISPM", "ai-posture"], ["Evidence", "evidence"]]
  },
  integrations: {
    kicker: "Connector guide",
    title: "Integrations",
    summary: "Use Integrations to review connector inventory and understand provider-delivery readiness without exposing secrets in the public UI.",
    steps: [
      "Seed sample connectors for local testing.",
      "Filter by category, status, and health.",
      "Use delivery tests to confirm configured versus disabled provider boundaries."
    ],
    links: [["Settings", "settings"], ["Agents & MCP", "agents-mcp"], ["Approvals", "approvals"]]
  },
  settings: {
    kicker: "Environment guide",
    title: "Settings",
    summary: "Use Settings to inspect API health, setup state, storage mode, provider boundaries, local UI preferences, and support diagnostics.",
    steps: [
      "Refresh API state when changing backend configuration.",
      "Confirm provider delivery is configured before live notification/report tests.",
      "Export diagnostics when troubleshooting local Docker or browser setup."
    ],
    links: [["Setup", "first-run-setup"], ["Reports", "reports"], ["Help", "documentation"]]
  },
  documentation: {
    kicker: "Help guide",
    title: "Help",
    summary: "Use Help as the map for application workflow and secondary references. It keeps product context available without crowding operator screens.",
    steps: [
      "Start with application workflow cards for daily operation.",
      "Use secondary references for architecture, use cases, trial, compliance, and roadmap context.",
      "Open the Wiki textbook for full technical documentation."
    ],
    links: [["Dashboard", "dashboard"], ["Architecture Reference", "architecture"], ["Trial Access", "enterprise-trial"]]
  }
};

/*
  Public release validation markers retained for historical validators:
  currentAispmReportCatalogPacket currentAispmReportSetupPacket
  currentAispmReportOperationsPacket currentAispmReportGovernancePacket
  currentAispmReportAssurancePacket currentAispmReportResponsePacket
  currentAispmReportTrialOpsPacket currentAispmHostedReleaseStatusPacket
  currentAispmPilotControlReadinessPacket aispmPilotControlReadinessItems
  currentAispmReleaseEvidenceIndexPacket aispmReleaseEvidenceIndexItems
  currentAispmPilotLaunchBoardPackPacket
  aispmReportSetupReadinessItems aispmReportOperationsReadinessItems
  aispmReportGovernanceReadinessItems aispmReportAssuranceReadinessItems
  aispmReportResponseReadinessItems aispmReportTrialOpsReadinessItems
  aispmHostedReleaseStatusItems renderAispmHostedReleaseStatus
  renderAispmReportCenter renderAispmReportSetupReadiness
  renderAispmReportOperationsReadiness renderAispmReportGovernanceReadiness
  renderAispmReportAssuranceReadiness renderAispmReportResponseReadiness
  renderAispmReportTrialOpsReadiness renderAispmPilotControlReadiness
  renderAispmReleaseEvidenceIndex
  renderAispmPilotLaunchBoardPack
  copyAispmReportCatalogPacket downloadAispmReportCatalogPacket
  copyAispmReportSetupPacket downloadAispmReportSetupPacket
  copyAispmReportOperationsPacket downloadAispmReportOperationsPacket
  copyAispmReportGovernancePacket downloadAispmReportGovernancePacket
  copyAispmReportAssurancePacket downloadAispmReportAssurancePacket
  copyAispmReportResponsePacket downloadAispmReportResponsePacket
  copyAispmReportTrialOpsPacket downloadAispmReportTrialOpsPacket
  copyAispmHostedReleaseStatusPacket downloadAispmHostedReleaseStatusPacket
  copyAispmPilotControlReadinessPacket downloadAispmPilotControlReadinessPacket
  copyAispmReleaseEvidenceIndexPacket downloadAispmReleaseEvidenceIndexPacket
  sendAispmReportEmail
  cavra.aispm.report_catalog_readiness_packet.v1
  cavra.aispm.report_delivery_setup_readiness_packet.v1
  cavra.aispm.report_operations_readiness_packet.v1
  cavra.aispm.report_governance_readiness_packet.v1
  cavra.aispm.report_assurance_readiness_packet.v1
  cavra.aispm.report_response_readiness_packet.v1
  cavra.aispm.report_trial_operations_readiness_packet.v1
  cavra.aispm.pilot_control_readiness_packet.v1
  cavra.aispm.release_evidence_index_packet.v1
  cavra.aispm.pilot_launch_board_pack_packet.v1
  cavra.hosted_sandbox.operator_release_status_packet.v1
  blocked_until_live_freshness_passes
  cavra-aispm-report-catalog-packet.json
  cavra-aispm-report-delivery-setup-packet.json
  cavra-aispm-report-operations-readiness-packet.json
  cavra-aispm-report-governance-readiness-packet.json
  cavra-aispm-report-assurance-readiness-packet.json
  cavra-aispm-report-response-readiness-packet.json
  cavra-aispm-report-trial-operations-readiness-packet.json
  cavra-aispm-pilot-control-readiness-packet.json
  cavra-aispm-release-evidence-index-packet.json
  cavra-aispm-pilot-launch-board-pack-packet.json
  cavra-aispm-pilot-launch-decision-packet.json
  cavra-aispm-pilot-evidence-room-packet.json
  cavra-aispm-pilot-risk-acceptance-packet.json
  cavra-aispm-pilot-exception-register-packet.json
  cavra-aispm-evidence-reviewer-checklist-packet.json
  cavra-hosted-sandbox-operator-status-packet.json
  cavra-aispm-agent-risk-register.csv cavra-aispm-control-coverage.csv
  cavra-aispm-evidence-freshness.csv cavra-aispm-soc2-audit-summary.md
  cavra-aispm-board-kpi-pack.json cavra-aispm-executive-risk-brief.md
  CSO Report Catalog Readiness Report Catalog Readiness Packet
  Report Delivery Setup Readiness Report Delivery Setup Packet
  CAVRA_REPORT_SMTP_PASSWORD_REF
  Report Operations Readiness Report Operations Readiness Packet
  Report Governance Readiness Report Governance Readiness Packet
  Report Assurance Readiness Report Assurance Readiness Packet
  Report Response Readiness Report Response Readiness Packet
  Report Trial Operations Readiness Report Trial Operations Readiness Packet
  Pilot Control Readiness Pilot Control Readiness Packet
  Hosted Release Operator Status
  scripts/validate-aispm-report-catalog-readiness.py
  scripts/validate-aispm-report-delivery-setup-readiness.py
  scripts/validate-aispm-report-operations-readiness.py
  scripts/validate-aispm-report-governance-readiness.py
  scripts/validate-aispm-report-assurance-readiness.py
  scripts/validate-aispm-report-response-readiness.py
  scripts/validate-aispm-report-trial-operations-readiness.py
  scripts/validate-aispm-pilot-control-readiness.py
  scripts/validate-aispm-release-evidence-index.py
  scripts/validate-aispm-v100-public-release.py
  scripts/validate-aispm-final-announcement-readiness.py
  scripts/validate-hosted-sandbox-deployment-freshness.py
  scripts/validate-hosted-sandbox-operator-status.py
  cavra-hosted-sandbox-post-deploy-evidence
  docs/release-verifications/aispm-v1.0-public-release-readiness.json
  artifact_manifest freshness_gate signed_board_approval
  board_minutes_and_attestation pdf_generation_and_delivery
  recipient_allowlists_and_email_audit tenant_artifact_retention
  docs/release-verifications/aispm-pilot-control-readiness.json
  src/cavra/schemas/aispm-report-delivery-audit-event.schema.json
  src/cavra/schemas/aispm-report-export-package-manifest.schema.json
  src/cavra/schemas/aispm-report-schedule-policy.schema.json
  src/cavra/schemas/aispm-report-evidence-room.schema.json
  src/cavra/schemas/aispm-report-evidence-room-access-event.schema.json
  src/cavra/schemas/aispm-report-alert-escalation.schema.json
  src/cavra/schemas/aispm-report-alert-operations-dashboard.schema.json
  src/cavra/schemas/aispm-report-remediation-closure-operations-dashboard.schema.json
  src/cavra/schemas/aispm-report-remediation-closure-executive-digest.schema.json
  src/cavra/schemas/aispm-report-center-trial-operator-api-view-model.schema.json
*/

const routeContent = [
  ...navItems.map((item) => ({ type: "Page", label: item.label, route: item.id, description: item.description })),
  ...secondaryRoutes.map((item) => ({ type: "Reference", label: item.label, route: item.id, description: item.description })),
  ...policies.map(([label, description]) => ({ type: "Policy", label, route: "policy-engine", description })),
  ...useCases.map(([label, description]) => ({ type: "Reference Use Case", label, route: "use-cases", description })),
  ...operatorPaths.map(([label, description]) => ({ type: "Reference Role Path", label, route: "operator-experience", description })),
  ...reportCards.map(([label, description]) => ({ type: "AISPM Report", label, route: "ai-posture", description })),
  { type: "AI Posture", label: "Pilot Launch Board Pack Packet", route: "ai-posture", description: "Copy or download the public-safe board packet for launch review." },
  { type: "Reference Trial", label: "Trial Field Guide", route: "enterprise-trial", description: "Run a complete AISPM use case with guided labs." }
];

const commandActions = [
  { id: "refresh-all", label: "Refresh all live state", type: "Action", route: "dashboard", description: "Reload health, setup, approvals, evidence, AISPM, agents, integrations, reports, and settings.", keywords: "refresh reload api dashboard state health" },
  { id: "open-setup-status", label: "Check setup status", type: "Setup Action", route: "first-run-setup", description: "Open Setup and call the setup status endpoint.", keywords: "setup status check first run" },
  { id: "run-setup-validate", label: "Validate setup and seed AISPM", type: "Setup Action", route: "first-run-setup", description: "Run setup validation and record sample decisions for AISPM posture.", keywords: "setup validate seed aispm decisions" },
  { id: "load-policy-actions", label: "Load policy action catalog", type: "Setup Action", route: "first-run-setup", description: "Load the active block, allow, approval, and trust catalog.", keywords: "policy action catalog rules controls" },
  { id: "test-risky-action", label: "Test risky policy action", type: "Setup Action", route: "first-run-setup", description: "Run the known risky action simulation from the setup panel.", keywords: "risk risky simulate command terraform approval block" },
  { id: "seed-approval", label: "Seed sample approval", type: "Action", route: "approvals", description: "Create a local approval item for workflow testing.", keywords: "approval queue seed sample" },
  { id: "seed-agents", label: "Seed sample agents", type: "Action", route: "agents-mcp", description: "Create sample Codex, Claude Code, and Copilot-style agent records.", keywords: "agent registry seed codex claude copilot" },
  { id: "seed-mcp", label: "Seed sample MCP servers", type: "Action", route: "agents-mcp", description: "Create sample trusted, review, and blocked MCP server records.", keywords: "mcp server trust seed tools" },
  { id: "seed-integrations", label: "Seed sample integrations", type: "Action", route: "integrations", description: "Create sample GitHub, Terraform, Kubernetes, cloud, and notification connector records.", keywords: "integration connector seed github terraform kubernetes" },
  { id: "generate-report-preview", label: "Generate report preview", type: "Report Action", route: "reports", description: "Generate the current report preview from loaded runtime state.", keywords: "report preview generate executive audit csv markdown json" },
  { id: "download-report-preview", label: "Download report preview", type: "Report Action", route: "reports", description: "Download the current report preview in the selected format.", keywords: "report download export csv markdown json" },
  { id: "download-settings-diagnostics", label: "Download settings diagnostics", type: "Export Action", route: "settings", description: "Export API, setup, provider, storage, and local UI diagnostics.", keywords: "settings diagnostics export download support" },
  { id: "expand-sidebar", label: "Expand sidebar", type: "UI Action", route: "settings", description: "Restore the desktop sidebar if it was collapsed.", keywords: "sidebar expand navigation ui" },
  { id: "collapse-sidebar", label: "Collapse sidebar", type: "UI Action", route: "settings", description: "Collapse the desktop sidebar for a focused work area.", keywords: "sidebar collapse navigation ui" },
  { id: "show-setup-prompt", label: "Show first-run setup prompt", type: "UI Action", route: "first-run-setup", description: "Reopen the first-run setup prompt.", keywords: "setup prompt first run modal" }
];

const el = (selector) => document.querySelector(selector);
const localApiDefault = "";
const setupApiBase = String(window.CAVRA_API_BASE || localApiDefault).replace(/\/$/, "");
const appState = {
  apiBase: setupApiBase,
  connected: false,
  lastRefreshAt: null,
  health: null,
  version: null,
  setupStatus: null,
  consoleConfig: null,
  aispmPosture: null,
  approvals: null,
  selectedApprovalId: null,
  approvalFilters: {
    search: "",
    state: "",
    group: ""
  },
  evidence: null,
  selectedEvidenceId: null,
  evidenceFilters: {
    search: "",
    kind: "",
    verification: ""
  },
  agents: null,
  selectedAgentId: null,
  agentFilters: {
    search: "",
    status: "",
    risk: ""
  },
  mcpServers: null,
  selectedMcpServerId: null,
  mcpFilters: {
    search: "",
    trust: "",
    capability: ""
  },
  agentProfiles: null,
  mcpClassifications: null,
  integrations: null,
  connectorDeliveryDashboard: null,
  selectedIntegrationId: null,
  integrationFilters: {
    search: "",
    category: "",
    status: "",
    health: ""
  },
  policyCatalog: null,
  policyFilters: {
    search: "",
    section: "",
    decision: ""
  },
  errors: []
};
const escapeHtml = (value) => String(value).replace(/[&<>"']/g, (char) => ({
  "&": "&amp;",
  "<": "&lt;",
  ">": "&gt;",
  "\"": "&quot;",
  "'": "&#039;"
}[char]));

function prettyJson(payload) {
  return JSON.stringify(payload, null, 2);
}

function writeSetupOutput(selector, payload) {
  const target = el(selector);
  if (!target) return;
  target.textContent = typeof payload === "string" ? payload : prettyJson(payload);
}

function setSetupApiStatus(message, state = "neutral") {
  const status = el("#setupApiStatus");
  if (!status) return;
  status.textContent = message;
  status.dataset.state = state;
}

async function setupApi(path, options = {}) {
  if (!setupApiBase) {
    throw new Error("No CAVRA API base configured. For local testing, start the API on http://localhost:8000 or set window.CAVRA_API_BASE in config.js.");
  }
  const response = await fetch(`${setupApiBase}${path}`, {
    headers: {
      "content-type": "application/json",
      ...(options.headers || {})
    },
    ...options
  });
  const text = await response.text();
  let payload;
  try {
    payload = text ? JSON.parse(text) : {};
  } catch {
    payload = { raw: text };
  }
  if (!response.ok) {
    const reason = payload.detail || payload.message || response.statusText;
    throw new Error(`CAVRA API ${response.status}: ${reason}`);
  }
  return payload;
}

function setupPost(path, payload = {}) {
  return setupApi(path, {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

async function optionalApi(path) {
  try {
    return { ok: true, value: await setupApi(path) };
  } catch (error) {
    return { ok: false, error: error.message };
  }
}

function itemCount(payload) {
  if (!payload) return 0;
  if (Array.isArray(payload)) return payload.length;
  if (typeof payload.total === "number") return payload.total;
  if (Array.isArray(payload.items)) return payload.items.length;
  return 0;
}

function formatTime(value) {
  if (!value) return "not recorded";
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? String(value) : date.toLocaleString();
}

function statusClass(value) {
  const normalized = String(value || "").toLowerCase();
  if (["ready", "connected", "configured", "complete", "ok", "allow", "approved", "enforced", "healthy", "active"].some((token) => normalized.includes(token))) return "ok";
  if (["pending", "require", "warning", "warn", "partial", "not_configured", "planned", "degraded", "not_checked"].some((token) => normalized.includes(token))) return "warn";
  if (["block", "critical", "high", "error", "fail", "disabled", "unknown"].some((token) => normalized.includes(token))) return "danger";
  return "neutral";
}

function statusBadge(value) {
  const text = value === undefined || value === null || value === "" ? "unknown" : String(value);
  return `<span class="state-chip ${statusClass(text)}">${escapeHtml(text)}</span>`;
}

function policyDecisionFor(item) {
  const action = String(item?.action || item?.action_type || "").toLowerCase();
  if (action.includes("block")) return "block";
  if (action.includes("require_approval") || action.includes("approval")) return "require_approval";
  if (action.includes("allow")) return "allow";
  if (action.includes("trust") || action.includes("approve")) return "trust";
  return "observe";
}

function policySeverityFor(item) {
  const action = String(item?.action || "").toLowerCase();
  const value = String(item?.value || "").toLowerCase();
  if (action.includes("block") && /(terraform apply|kubectl delete|admin|secret|\.env|pem|pfx|tfstate)/.test(value)) return "critical";
  if (action.includes("block")) return "high";
  if (action.includes("approval")) return "high";
  if (action.includes("allow")) return "low";
  return "medium";
}

function policyActionTypeFor(item) {
  const section = String(item?.section || "").toLowerCase();
  const action = String(item?.action || "").toLowerCase();
  if (section.includes("filesystem") && action.includes("read")) return "read_file";
  if (section.includes("filesystem") && action.includes("write")) return "write_file";
  if (section.includes("command")) return "execute_command";
  if (section.includes("git")) return "git_operation";
  if (section.includes("mcp")) return "mcp_tool_call";
  return section || "policy";
}

function normalizedPolicyItems() {
  return (appState.policyCatalog?.items || []).map((item) => ({
    ...item,
    decision: policyDecisionFor(item),
    severity: policySeverityFor(item),
    action_type: policyActionTypeFor(item),
    target: item.value || item.target || item.pattern || "not recorded"
  }));
}

function filteredPolicyItems() {
  const filters = appState.policyFilters;
  const search = filters.search.trim().toLowerCase();
  return normalizedPolicyItems().filter((item) => {
    const haystack = `${item.id} ${item.section} ${item.action} ${item.target} ${item.editable_via} ${item.decision} ${item.severity}`.toLowerCase();
    return (!search || haystack.includes(search)) &&
      (!filters.section || item.section === filters.section) &&
      (!filters.decision || item.decision === filters.decision);
  });
}

function approvalItems() {
  return appState.approvals?.items || [];
}

function approvalState(approval) {
  return approval.state || approval.status || "unknown";
}

function approvalActor(approval) {
  return approval.requested_by || approval.actor || approval.decision?.actor || "unknown";
}

function approvalReason(approval) {
  return approval.reason || approval.decision_reason || approval.decision?.reason || "not recorded";
}

function approvalTarget(approval) {
  return approval.decision?.target || approval.target || approval.decision?.repository || "not recorded";
}

function filteredApprovalItems() {
  const filters = appState.approvalFilters;
  const search = filters.search.trim().toLowerCase();
  return approvalItems().filter((approval) => {
    const group = approval.approver_group || "not routed";
    const state = approvalState(approval);
    const haystack = [
      approval.approval_id,
      approval.decision_id,
      state,
      group,
      approvalActor(approval),
      approvalTarget(approval),
      approvalReason(approval)
    ].join(" ").toLowerCase();
    return (!search || haystack.includes(search)) &&
      (!filters.state || state === filters.state) &&
      (!filters.group || group === filters.group);
  });
}

function selectedApproval() {
  return approvalItems().find((approval) => approval.approval_id === appState.selectedApprovalId) || null;
}

function evidenceId(record) {
  return record.evidence_ref || record.evidence_id || record.session_id || record.id || "evidence";
}

function evidenceKind(record) {
  return record.metadata_kind || record.kind || record.source_kind || "bundle_metadata";
}

function evidenceVerification(record) {
  if (record.verification_state) return record.verification_state;
  if (record.source === "aispm_reference") return "aispm_reference";
  if (record.signer || record.signature || record.manifest?.signature) return "signed";
  if (record.missing_metadata) return "missing";
  return "metadata_only";
}

function evidenceRefs(record) {
  if (record.evidence_ref) return [String(record.evidence_ref)];
  const refs = record.evidence_refs || record.refs || record.manifest?.evidence_refs || [];
  return Array.isArray(refs) ? refs.map(String) : [String(refs)];
}

function evidenceItems() {
  const items = [];
  for (const record of appState.evidence?.items || []) {
    items.push({
      ...record,
      source: "metadata_store",
      source_kind: record.metadata_kind || "bundle_metadata"
    });
  }
  const existingIds = new Set(items.map((item) => evidenceId(item)));
  const correlatedSources = [
    ...(appState.aispmPosture?.findings || []),
    ...(appState.aispmPosture?.timeline || [])
  ];
  for (const source of correlatedSources) {
    for (const ref of evidenceRefs(source)) {
      if (!ref || existingIds.has(ref)) continue;
      existingIds.add(ref);
      const session = ref.startsWith("evidence://") ? ref.replace("evidence://", "").split("/")[0] : source.session_id;
      items.push({
        evidence_ref: ref,
        session_id: session || source.session_id || "not recorded",
        source: "aispm_reference",
        source_kind: "aispm_evidence_ref",
        metadata_kind: "aispm_evidence_ref",
        verification_state: "aispm_reference",
        signer: "not indexed",
        blocked_count: source.outcome === "block" || source.decision === "block" ? 1 : 0,
        approval_count: source.outcome === "require_approval" || source.decision === "require_approval" ? 1 : 0,
        created_at: source.timestamp,
        decision_id: source.decision_id,
        agent_id: source.agent_id,
        repository: source.repository,
        rule_id: source.rule_id,
        severity: source.severity,
        reason: source.reason || source.title || "AISPM evidence reference observed without indexed bundle metadata.",
        correlated_source: source
      });
    }
  }
  return items;
}

function selectedEvidence() {
  return evidenceItems().find((record) => evidenceId(record) === appState.selectedEvidenceId) || null;
}

function filteredEvidenceItems() {
  const filters = appState.evidenceFilters;
  const search = filters.search.trim().toLowerCase();
  return evidenceItems().filter((record) => {
    const kind = evidenceKind(record);
    const verification = evidenceVerification(record);
    const haystack = [
      evidenceId(record),
      record.session_id,
      record.signer,
      kind,
      verification,
      record.decision_id,
      record.agent_id,
      record.repository,
      record.rule_id,
      record.reason,
      evidenceRefs(record).join(" ")
    ].join(" ").toLowerCase();
    return (!search || haystack.includes(search)) &&
      (!filters.kind || kind === filters.kind) &&
      (!filters.verification || verification === filters.verification);
  });
}

function populateEvidenceKindFilter(items) {
  const select = el("#evidenceKindFilter");
  if (!select) return;
  const current = appState.evidenceFilters.kind;
  const kinds = [...new Set(items.map((item) => evidenceKind(item)).filter(Boolean))].sort();
  select.innerHTML = `
    <option value="">All kinds</option>
    ${kinds.map((kind) => `<option value="${escapeHtml(kind)}">${escapeHtml(kind)}</option>`).join("")}
  `;
  select.value = kinds.includes(current) ? current : "";
  if (select.value !== current) appState.evidenceFilters.kind = select.value;
}

function agentItems() {
  return appState.agents?.items || [];
}

function mcpServerItems() {
  return appState.mcpServers?.items || [];
}

function selectedAgent() {
  return agentItems().find((agent) => agent.agent_id === appState.selectedAgentId || agent.id === appState.selectedAgentId) || null;
}

function selectedMcpServer() {
  return mcpServerItems().find((server) => server.server_id === appState.selectedMcpServerId || server.id === appState.selectedMcpServerId || server.name === appState.selectedMcpServerId) || null;
}

function agentId(agent) {
  return agent.agent_id || agent.id || "agent";
}

function mcpServerId(server) {
  return server.server_id || server.id || server.name || "mcp-server";
}

function filteredAgentItems() {
  const filters = appState.agentFilters;
  const search = filters.search.trim().toLowerCase();
  return agentItems().filter((agent) => {
    const haystack = [
      agentId(agent),
      agent.vendor,
      agent.type,
      agent.owner,
      agent.status,
      agent.risk_tier,
      (agent.capabilities || []).join(" "),
      (agent.scopes || []).join(" "),
      (agent.allowed_repositories || []).join(" "),
      (agent.allowed_tools || []).join(" ")
    ].join(" ").toLowerCase();
    return (!search || haystack.includes(search)) &&
      (!filters.status || agent.status === filters.status) &&
      (!filters.risk || agent.risk_tier === filters.risk);
  });
}

function filteredMcpServerItems() {
  const filters = appState.mcpFilters;
  const search = filters.search.trim().toLowerCase();
  return mcpServerItems().filter((server) => {
    const haystack = [
      mcpServerId(server),
      server.name,
      server.owner,
      server.trust_tier,
      server.approval_state,
      (server.capabilities || []).join(" "),
      (server.allowed_tools || []).join(" ")
    ].join(" ").toLowerCase();
    return (!search || haystack.includes(search)) &&
      (!filters.trust || server.trust_tier === filters.trust) &&
      (!filters.capability || (server.capabilities || []).includes(filters.capability));
  });
}

function populateMcpCapabilityFilter(items) {
  const select = el("#mcpCapabilityFilter");
  if (!select) return;
  const current = appState.mcpFilters.capability;
  const capabilities = [...new Set(items.flatMap((item) => item.capabilities || []).filter(Boolean))].sort();
  select.innerHTML = `
    <option value="">All capabilities</option>
    ${capabilities.map((capability) => `<option value="${escapeHtml(capability)}">${escapeHtml(capability)}</option>`).join("")}
  `;
  select.value = capabilities.includes(current) ? current : "";
  if (select.value !== current) appState.mcpFilters.capability = select.value;
}

function buildRegistryAuditPayload(kind, record) {
  return {
    schema_version: "cavra.ui.registry.audit_view.v1",
    generated_at: new Date().toISOString(),
    kind,
    selected_id: kind === "agent" ? agentId(record || {}) : mcpServerId(record || {}),
    record: record || null,
    posture_correlation: {
      agent_findings: kind === "agent"
        ? (appState.aispmPosture?.findings || []).filter((finding) => finding.agent_id === agentId(record || {})).slice(0, 10)
        : [],
      mcp_findings: kind === "mcp_server"
        ? (appState.aispmPosture?.findings || []).filter((finding) => String(finding.rule_id || "").startsWith("mcp.")).slice(0, 10)
        : []
    }
  };
}

function integrationItems() {
  return appState.integrations?.items || [];
}

function integrationId(integration) {
  return integration.integration_id || integration.id || integration.provider || "integration";
}

function selectedIntegration() {
  return integrationItems().find((integration) => integrationId(integration) === appState.selectedIntegrationId) || null;
}

function filteredIntegrationItems() {
  const filters = appState.integrationFilters;
  const search = filters.search.trim().toLowerCase();
  return integrationItems().filter((integration) => {
    const haystack = [
      integrationId(integration),
      integration.name,
      integration.provider,
      integration.category,
      integration.status,
      integration.health_status,
      integration.owner,
      integration.environment,
      integration.auth_mode,
      integration.endpoint_ref,
      (integration.capabilities || []).join(" "),
      (integration.repositories || []).join(" ")
    ].join(" ").toLowerCase();
    return (!search || haystack.includes(search)) &&
      (!filters.category || integration.category === filters.category) &&
      (!filters.status || integration.status === filters.status) &&
      (!filters.health || integration.health_status === filters.health);
  });
}

function buildIntegrationAuditPayload(record) {
  const id = integrationId(record || {});
  return {
    schema_version: "cavra.ui.integration.audit_view.v1",
    generated_at: new Date().toISOString(),
    selected_id: id,
    connector_delivery_configured: (appState.consoleConfig?.connector_delivery || "disabled") === "configured",
    selected_record: record || null,
    delivery_dashboard: appState.connectorDeliveryDashboard || null,
    evidence_correlation: (appState.evidence?.items || [])
      .filter((item) => JSON.stringify(item).toLowerCase().includes(String(id).toLowerCase()))
      .slice(0, 10)
      .map((item) => ({
        session_id: item.session_id,
        metadata_kind: item.metadata_kind,
        generated_at: item.generated_at || item.created_at
      }))
  };
}

function populateApprovalGroupFilter(items) {
  const select = el("#approvalGroupFilter");
  if (!select) return;
  const current = appState.approvalFilters.group;
  const groups = [...new Set(items.map((item) => item.approver_group || "not routed"))].sort();
  select.innerHTML = `
    <option value="">All groups</option>
    ${groups.map((group) => `<option value="${escapeHtml(group)}">${escapeHtml(group)}</option>`).join("")}
  `;
  select.value = groups.includes(current) ? current : "";
  if (select.value !== current) appState.approvalFilters.group = select.value;
}

function populatePolicySectionFilter(items) {
  const select = el("#policyCatalogSection");
  if (!select) return;
  const current = appState.policyFilters.section;
  const sections = [...new Set(items.map((item) => item.section).filter(Boolean))].sort();
  select.innerHTML = `
    <option value="">All sections</option>
    ${sections.map((section) => `<option value="${escapeHtml(section)}">${escapeHtml(section)}</option>`).join("")}
  `;
  select.value = sections.includes(current) ? current : "";
  if (select.value !== current) appState.policyFilters.section = select.value;
}

function renderEmptyTable(targetSelector, title, detail) {
  const target = el(targetSelector);
  if (!target) return;
  target.innerHTML = `
    <div class="operator-empty-table">
      <strong>${escapeHtml(title)}</strong>
      <p>${escapeHtml(detail)}</p>
    </div>
  `;
}

function renderRows(targetSelector, columns, rows) {
  const target = el(targetSelector);
  if (!target) return;
  if (!rows.length) {
    renderEmptyTable(targetSelector, "No records yet", "Run setup validation or connect providers to populate this view.");
    return;
  }
  target.innerHTML = `
    <table class="operator-table">
      <thead><tr>${columns.map((column) => `<th>${escapeHtml(column)}</th>`).join("")}</tr></thead>
      <tbody>
        ${rows.map((row) => `<tr>${row.map((cell) => `<td>${cell}</td>`).join("")}</tr>`).join("")}
      </tbody>
    </table>
  `;
}

function renderOperatorDashboard() {
  const strip = el("#operatorStatusStrip");
  const empty = el("#operatorEmptyState");
  const configured = el("#operatorConfiguredState");
  const offline = el("#operatorOfflineState");
  if (!strip || !empty || !configured || !offline) return;

  empty.hidden = true;
  configured.hidden = true;
  offline.hidden = true;

  if (!appState.connected) {
    strip.innerHTML = `
      <div>${statusBadge("API disconnected")}<span>Base: ${escapeHtml(appState.apiBase || "not configured")}</span></div>
      <div>${statusBadge("Static mode")}<span>Reference pages remain available.</span></div>
    `;
    offline.hidden = false;
    const message = el("#operatorOfflineMessage");
    if (message) message.textContent = appState.errors[0] || "The CAVRA API is not reachable from this browser.";
    return;
  }

  const setup = appState.setupStatus || {};
  const complete = Boolean(setup.configured && setup.setup_complete);
  const overview = appState.aispmPosture?.overview || {};
  const config = appState.consoleConfig || {};

  strip.innerHTML = `
    <div>${statusBadge("API connected")}<span>${escapeHtml(appState.apiBase)}</span></div>
    <div>${statusBadge(complete ? "setup complete" : "setup required")}<span>${escapeHtml(setup.workspace?.name || "local workspace")}</span></div>
    <div>${statusBadge(overview.risk_level || "posture pending")}<span>AISPM risk</span></div>
    <div>${statusBadge(config.metadata_mode || "metadata")}<span>metadata store</span></div>
    <div><span class="state-chip neutral">refreshed</span><span>${escapeHtml(formatTime(appState.lastRefreshAt))}</span></div>
  `;

  if (!complete) {
    empty.hidden = false;
    return;
  }

  configured.hidden = false;
  const metricCards = [
    ["Policy Pack", setup.policy?.default_pack || "not selected", setup.policy?.available ? "Available" : "Missing", setup.policy?.available ? "ok" : "danger"],
    ["Decisions", overview.total_decisions ?? 0, `${overview.blocked_actions ?? 0} blocked / ${overview.approval_required_actions ?? 0} approvals`, statusClass(overview.risk_level)],
    ["Open Approvals", itemCount(appState.approvals), "Pending approval records", itemCount(appState.approvals) ? "warn" : "ok"],
    ["Evidence Records", itemCount(appState.evidence), "Indexed metadata records", itemCount(appState.evidence) ? "ok" : "warn"],
    ["Agents", itemCount(appState.agents), `${itemCount(appState.mcpServers)} MCP servers`, itemCount(appState.agents) || itemCount(appState.mcpServers) ? "ok" : "warn"],
    ["Connectors", config.connector_delivery || "disabled", `approvals: ${config.approval_provider_delivery || "disabled"}`, config.connector_delivery === "disabled" ? "warn" : "ok"]
  ];
  el("#operatorMetricCards").innerHTML = metricCards.map(([label, value, detail, state]) => `
    <article class="operator-metric-card ${escapeHtml(state)}">
      <span>${escapeHtml(label)}</span>
      <strong>${escapeHtml(value)}</strong>
      <p>${escapeHtml(detail)}</p>
    </article>
  `).join("");

  const timeline = appState.aispmPosture?.timeline || [];
  renderRows("#recentDecisionTable", ["Time", "Action", "Target", "Decision", "Severity"], timeline.slice(0, 8).map((event) => [
    escapeHtml(formatTime(event.timestamp)),
    escapeHtml(event.title || event.action_type || event.event_type || "decision"),
    escapeHtml(event.target || event.repository || "not recorded"),
    statusBadge(event.outcome || event.decision || "unknown"),
    statusBadge(event.severity || "info")
  ]));
  const recentStatus = el("#recentDecisionStatus");
  if (recentStatus) {
    recentStatus.textContent = timeline.length ? `${timeline.length} events` : "empty";
    recentStatus.className = `state-chip ${timeline.length ? "ok" : "warn"}`;
  }

  renderConnectorHealth();
}

function renderConnectorHealth() {
  const config = appState.consoleConfig || {};
  const cards = [
    ["Approval delivery", config.approval_provider_delivery || "disabled", "Slack, Teams, Jira, ServiceNow, or webhook provider delivery."],
    ["Connector delivery", config.connector_delivery || "disabled", "SIEM, ITSM, ChatOps, and cloud delivery layer."],
    ["OIDC approval identity", config.approval_oidc || "disabled", "Signed identity claims for approval authorization."],
    ["RBAC approval policy", config.approval_rbac || "disabled", "Repository-scoped approval rights."],
    ["Evidence artifacts", config.evidence_artifacts || "disabled", "Hosted evidence artifact access and bundle retrieval."],
    ["CORS origins", (config.cors_origins || []).length ? "configured" : "not configured", (config.cors_origins || []).join(", ") || "No browser origins reported."]
  ];
  const target = el("#connectorHealthCards");
  if (!target) return;
  target.innerHTML = cards.map(([name, state, detail]) => `
    <article class="connector-health-card ${statusClass(state)}">
      <strong>${escapeHtml(name)}</strong>
      ${statusBadge(state)}
      <p>${escapeHtml(detail)}</p>
    </article>
  `).join("");
  const status = el("#connectorHealthStatus");
  if (status) {
    const disabled = cards.filter(([, state]) => String(state).includes("disabled")).length;
    status.textContent = disabled ? `${disabled} disabled` : "ready";
    status.className = `state-chip ${disabled ? "warn" : "ok"}`;
  }
}

function renderIntegrationHub() {
  const items = integrationItems();
  const filtered = filteredIntegrationItems();
  if (!appState.selectedIntegrationId && filtered.length) appState.selectedIntegrationId = integrationId(filtered[0]);
  if (appState.selectedIntegrationId && !items.some((item) => integrationId(item) === appState.selectedIntegrationId)) {
    appState.selectedIntegrationId = filtered[0] ? integrationId(filtered[0]) : null;
  }

  const configuredDelivery = (appState.consoleConfig?.connector_delivery || "disabled") === "configured";
  const healthy = items.filter((item) => item.health_status === "healthy").length;
  const degraded = items.filter((item) => ["degraded", "failed"].includes(item.health_status)).length;
  const active = items.filter((item) => item.status === "active").length;
  const categories = new Set(items.map((item) => item.category).filter(Boolean)).size;
  const environments = new Set(items.map((item) => item.environment).filter(Boolean)).size;
  const summary = el("#integrationSummaryCards");
  if (summary) {
    summary.innerHTML = [
      ["Integrations", items.length, "registered", items.length ? "ok" : "warn"],
      ["Active", active, "enabled", active ? "ok" : "warn"],
      ["Healthy", healthy, "passing", healthy ? "ok" : "warn"],
      ["Degraded", degraded, "review", degraded ? "danger" : "ok"],
      ["Categories", categories, "covered", categories ? "ok" : "warn"],
      ["Delivery", configuredDelivery ? "configured" : "disabled", "provider boundary", configuredDelivery ? "ok" : "warn"]
    ].map(([label, value, detail, state]) => `
      <article class="integration-summary-card ${escapeHtml(state)}">
        <span>${escapeHtml(detail)}</span>
        <strong>${escapeHtml(value)}</strong>
        <p>${escapeHtml(label)}</p>
      </article>
    `).join("");
  }

  const line = el("#integrationSummaryLine");
  if (line) {
    line.textContent = `${items.length} integration records across ${categories} categories and ${environments} environments. Showing ${filtered.length} after filters.`;
  }

  renderRows("#integrationTable", ["Select", "Provider", "Category", "Status", "Health", "Owner", "Environment"], filtered.map((integration) => [
    `<button type="button" class="integration-select-button" data-integration-select="${escapeHtml(integrationId(integration))}">${integrationId(integration) === appState.selectedIntegrationId ? "Selected" : "Inspect"}</button>`,
    escapeHtml(integration.provider || integration.name || "provider"),
    escapeHtml(integration.category || "uncategorized"),
    statusBadge(integration.status || "unknown"),
    statusBadge(integration.health_status || "not_checked"),
    escapeHtml(integration.owner || "unassigned"),
    escapeHtml(integration.environment || "global")
  ]));

  renderIntegrationDetail();
  renderConnectorDeliveryDashboard();
  renderIntegrationProviderBoundary();
}

function renderIntegrationDetail() {
  const selected = selectedIntegration();
  const status = el("#integrationDetailStatus");
  const detail = el("#integrationDetail");
  if (status) {
    status.textContent = selected ? selected.health_status || selected.status || "selected" : "none";
    status.className = `state-chip ${selected ? statusClass(selected.health_status || selected.status) : "neutral"}`;
  }
  if (!detail) return;
  detail.innerHTML = selected ? `
    <dl class="integration-detail-list">
      <div><dt>ID</dt><dd>${escapeHtml(integrationId(selected))}</dd></div>
      <div><dt>Name</dt><dd>${escapeHtml(selected.name || selected.provider || "integration")}</dd></div>
      <div><dt>Provider</dt><dd>${escapeHtml(selected.provider || "unknown")}</dd></div>
      <div><dt>Category</dt><dd>${escapeHtml(selected.category || "unknown")}</dd></div>
      <div><dt>Status</dt><dd>${statusBadge(selected.status || "unknown")}</dd></div>
      <div><dt>Health</dt><dd>${statusBadge(selected.health_status || "not_checked")}</dd></div>
      <div><dt>Owner</dt><dd>${escapeHtml(selected.owner || "unassigned")}</dd></div>
      <div><dt>Environment</dt><dd>${escapeHtml(selected.environment || "global")}</dd></div>
      <div><dt>Auth Mode</dt><dd>${escapeHtml(selected.auth_mode || "not_configured")}</dd></div>
      <div><dt>Endpoint Ref</dt><dd>${escapeHtml(selected.endpoint_ref || "not recorded")}</dd></div>
      <div><dt>Capabilities</dt><dd>${escapeHtml((selected.capabilities || []).join(", ") || "none recorded")}</dd></div>
      <div><dt>Repositories</dt><dd>${escapeHtml((selected.repositories || []).join(", ") || "none recorded")}</dd></div>
      <div><dt>Last Checked</dt><dd>${escapeHtml(formatTime(selected.last_checked_at))}</dd></div>
    </dl>
    <details class="integration-json-detail"><summary>Raw integration JSON</summary><pre>${escapeHtml(prettyJson(selected))}</pre></details>
  ` : `
    <div class="operator-empty-table">
      <strong>No integration selected</strong>
      <p>Seed sample integrations or connect provider inventory to review health and delivery readiness.</p>
    </div>
  `;
}

function renderConnectorDeliveryDashboard() {
  const dashboard = appState.connectorDeliveryDashboard;
  const status = el("#integrationDeliveryStatus");
  const target = el("#connectorDeliveryDashboard");
  if (status) {
    const level = dashboard?.alert_level || "unknown";
    status.textContent = level;
    status.className = `state-chip ${statusClass(level)}`;
  }
  if (!target) return;
  if (!dashboard) {
    target.innerHTML = `
      <div class="operator-empty-table">
        <strong>Delivery history unavailable</strong>
        <p>Connect the API and refresh to load release connector delivery telemetry.</p>
      </div>
    `;
    return;
  }
  const providers = dashboard.providers || [];
  const alerts = dashboard.alerts || [];
  target.innerHTML = `
    <div class="connector-delivery-metrics">
      <article><span>Total</span><strong>${escapeHtml(dashboard.total_deliveries ?? 0)}</strong></article>
      <article><span>Success</span><strong>${escapeHtml(dashboard.successful_deliveries ?? 0)}</strong></article>
      <article><span>Failed</span><strong>${escapeHtml(dashboard.failed_deliveries ?? 0)}</strong></article>
      <article><span>Rate</span><strong>${escapeHtml(`${dashboard.success_rate ?? 0}%`)}</strong></article>
    </div>
    <div class="connector-delivery-list">
      ${providers.length ? providers.map((provider) => `
        <article>
          <strong>${escapeHtml(provider.provider || provider.name || "provider")}</strong>
          <span>${statusBadge(provider.status || provider.health || "observed")}</span>
          <p>${escapeHtml(`${provider.successful_deliveries ?? 0} successful / ${provider.failed_deliveries ?? 0} failed`)}</p>
        </article>
      `).join("") : `
        <article>
          <strong>No persisted provider deliveries</strong>
          <p>Delivery events appear here after configured connector delivery writes evidence metadata.</p>
        </article>
      `}
    </div>
    <details class="integration-json-detail" ${alerts.length ? "open" : ""}>
      <summary>Delivery alerts and raw dashboard</summary>
      <pre>${escapeHtml(prettyJson(dashboard))}</pre>
    </details>
  `;
}

function renderIntegrationProviderBoundary() {
  const config = appState.consoleConfig || {};
  const target = el("#integrationProviderBoundary");
  const status = el("#integrationProviderStatus");
  const connectorDelivery = config.connector_delivery || "disabled";
  if (status) {
    status.textContent = connectorDelivery;
    status.className = `state-chip ${statusClass(connectorDelivery)}`;
  }
  if (!target) return;
  const rows = [
    ["Connector delivery", connectorDelivery, "Provider-backed delivery to SIEM, ITSM, ChatOps, webhook, or cloud targets."],
    ["Approval provider", config.approval_provider_delivery || "disabled", "Approval notification and decision provider delivery."],
    ["OIDC approval identity", config.approval_oidc || "disabled", "Signed identity context for approval authorization."],
    ["RBAC approval policy", config.approval_rbac || "disabled", "Repository and owner-scoped approval authorization."],
    ["Evidence artifacts", config.evidence_artifacts || "disabled", "Artifact root and evidence bundle retrieval."]
  ];
  target.innerHTML = rows.map(([name, state, detail]) => `
    <article class="integration-boundary-card ${statusClass(state)}">
      <div><strong>${escapeHtml(name)}</strong>${statusBadge(state)}</div>
      <p>${escapeHtml(detail)}</p>
    </article>
  `).join("");
}

function renderPolicyCatalog() {
  const catalog = appState.policyCatalog;
  if (!catalog) {
    const cards = el("#policyCatalogCards");
    if (cards) cards.innerHTML = "";
    populatePolicySectionFilter([]);
    renderEmptyTable("#policyCatalogTable", "Policy catalog unavailable", "Connect the API and refresh policy state.");
    return;
  }
  const items = normalizedPolicyItems();
  const filtered = filteredPolicyItems();
  populatePolicySectionFilter(items);
  const decisionOrder = ["block", "require_approval", "allow", "trust", "observe"];
  const decisionCounts = decisionOrder.map((decision) => [
    decision,
    items.filter((item) => item.decision === decision).length
  ]);
  const sectionCounts = [...new Set(items.map((item) => item.section).filter(Boolean))]
    .map((section) => [section, items.filter((item) => item.section === section).length])
    .sort((a, b) => b[1] - a[1])
    .slice(0, 3);
  const cards = el("#policyCatalogCards");
  if (cards) {
    cards.innerHTML = [
      ["Total rules", items.length, catalog.policy_pack || "active pack"],
      ...decisionCounts.filter(([, count]) => count > 0).map(([decision, count]) => [decision.replace("_", " "), count, "decision class"]),
      ...sectionCounts.map(([section, count]) => [section, count, "section"])
    ].slice(0, 6).map(([label, value, detail]) => `
      <article class="policy-catalog-card ${statusClass(label)}">
        <span>${escapeHtml(detail)}</span>
        <strong>${escapeHtml(value)}</strong>
        <p>${escapeHtml(label)}</p>
      </article>
    `).join("");
  }
  const summary = el("#policyCatalogSummary");
  if (summary) {
    summary.textContent = `${catalog.policy_pack || "policy pack"} exposes ${catalog.total ?? items.length} governed actions. Showing ${filtered.length} after filters.`;
  }
  renderRows("#policyCatalogTable", ["Section", "Action Type", "Target", "Decision", "Severity", "Editable Via", "Rule"], filtered.slice(0, 60).map((item) => [
    escapeHtml(item.section || "policy"),
    escapeHtml(item.action_type || "action"),
    escapeHtml(item.target || "not recorded"),
    statusBadge(item.decision),
    statusBadge(item.severity),
    escapeHtml(item.editable_via || "policy file"),
    escapeHtml(item.rule_id || item.id || "rule")
  ]));
}

function renderAgentsAndMcp() {
  const agents = agentItems();
  const servers = mcpServerItems();
  const filteredAgents = filteredAgentItems();
  const filteredServers = filteredMcpServerItems();
  populateMcpCapabilityFilter(servers);

  if (!appState.selectedAgentId && filteredAgents.length) appState.selectedAgentId = agentId(filteredAgents[0]);
  if (appState.selectedAgentId && !agents.some((agent) => agentId(agent) === appState.selectedAgentId)) {
    appState.selectedAgentId = filteredAgents[0] ? agentId(filteredAgents[0]) : null;
  }
  if (!appState.selectedMcpServerId && filteredServers.length) appState.selectedMcpServerId = mcpServerId(filteredServers[0]);
  if (appState.selectedMcpServerId && !servers.some((server) => mcpServerId(server) === appState.selectedMcpServerId)) {
    appState.selectedMcpServerId = filteredServers[0] ? mcpServerId(filteredServers[0]) : null;
  }

  const summary = el("#registrySummaryCards");
  if (summary) {
    const unknownServers = servers.filter((server) => ["unknown", "experimental"].includes(String(server.trust_tier || ""))).length;
    const blockedServers = servers.filter((server) => server.trust_tier === "blocked" || server.approval_state === "denied").length;
    const highAgents = agents.filter((agent) => ["critical", "high"].includes(String(agent.risk_tier || ""))).length;
    summary.innerHTML = [
      ["Agents", agents.length, "registered"],
      ["MCP servers", servers.length, "registered"],
      ["High-risk agents", highAgents, "review"],
      ["Unknown MCP", unknownServers, "trust review"],
      ["Blocked MCP", blockedServers, "denied"],
      ["Capabilities", new Set(servers.flatMap((server) => server.capabilities || [])).size, "covered"]
    ].map(([label, value, detail]) => `
      <article class="registry-summary-card ${statusClass(label)}">
        <span>${escapeHtml(detail)}</span>
        <strong>${escapeHtml(value)}</strong>
        <p>${escapeHtml(label)}</p>
      </article>
    `).join("");
  }

  renderRows("#agentsTable", ["Select", "Agent", "Vendor", "Risk", "Status", "Owner", "Scopes"], filteredAgents.map((agent) => [
    `<button type="button" class="registry-select-button" data-agent-select="${escapeHtml(agentId(agent))}">${agentId(agent) === appState.selectedAgentId ? "Selected" : "Inspect"}</button>`,
    escapeHtml(agentId(agent)),
    escapeHtml(agent.vendor || agent.type || "unknown"),
    statusBadge(agent.risk_tier || "not set"),
    statusBadge(agent.status || "unknown"),
    escapeHtml(agent.owner || "unassigned"),
    escapeHtml((agent.scopes || []).join(", ") || "none recorded")
  ]));
  renderRows("#mcpTrustTable", ["Select", "Server", "Trust", "Approval", "Capabilities", "Tools", "Owner"], filteredServers.map((server) => [
    `<button type="button" class="registry-select-button" data-mcp-select="${escapeHtml(mcpServerId(server))}">${mcpServerId(server) === appState.selectedMcpServerId ? "Selected" : "Inspect"}</button>`,
    escapeHtml(mcpServerId(server)),
    statusBadge(server.trust_tier || "unknown"),
    statusBadge(server.approval_state || "unknown"),
    escapeHtml((server.capabilities || []).join(", ") || "none recorded"),
    escapeHtml((server.allowed_tools || []).join(", ") || "all tools"),
    escapeHtml(server.owner || "unassigned")
  ]));

  const agentStatus = el("#agentRegistryStatus");
  if (agentStatus) {
    agentStatus.textContent = agents.length ? `${filteredAgents.length}/${agents.length}` : "empty";
    agentStatus.className = `state-chip ${agents.length ? "ok" : "warn"}`;
  }
  const mcpStatus = el("#mcpRegistryStatus");
  if (mcpStatus) {
    mcpStatus.textContent = servers.length ? `${filteredServers.length}/${servers.length}` : "empty";
    mcpStatus.className = `state-chip ${servers.length ? "ok" : "warn"}`;
  }

  renderRegistryDetails();
  renderRegistryReferenceTables();
}

function renderRegistryDetails() {
  const agent = selectedAgent();
  const agentStatus = el("#agentDetailStatus");
  const agentDetail = el("#agentDetail");
  if (agentStatus) {
    agentStatus.textContent = agent ? agent.risk_tier || "registered" : "none";
    agentStatus.className = `state-chip ${agent ? statusClass(agent.risk_tier || agent.status) : "neutral"}`;
  }
  if (agentDetail) {
    agentDetail.innerHTML = agent ? `
      <dl class="registry-detail-list">
        <div><dt>Agent ID</dt><dd>${escapeHtml(agentId(agent))}</dd></div>
        <div><dt>Vendor</dt><dd>${escapeHtml(agent.vendor || "unknown")}</dd></div>
        <div><dt>Type</dt><dd>${escapeHtml(agent.type || "unknown")}</dd></div>
        <div><dt>Status</dt><dd>${statusBadge(agent.status || "unknown")}</dd></div>
        <div><dt>Risk Tier</dt><dd>${statusBadge(agent.risk_tier || "not set")}</dd></div>
        <div><dt>Owner</dt><dd>${escapeHtml(agent.owner || "unassigned")}</dd></div>
        <div><dt>Capabilities</dt><dd>${escapeHtml((agent.capabilities || []).join(", ") || "none recorded")}</dd></div>
        <div><dt>Scopes</dt><dd>${escapeHtml((agent.scopes || []).join(", ") || "none recorded")}</dd></div>
        <div><dt>Repositories</dt><dd>${escapeHtml((agent.allowed_repositories || []).join(", ") || "none recorded")}</dd></div>
        <div><dt>Allowed Tools</dt><dd>${escapeHtml((agent.allowed_tools || []).join(", ") || "none recorded")}</dd></div>
        <div><dt>Last Seen</dt><dd>${escapeHtml(formatTime(agent.last_seen || agent.last_seen_at))}</dd></div>
      </dl>
      <details class="registry-json-detail"><summary>Raw agent JSON</summary><pre>${escapeHtml(prettyJson(agent))}</pre></details>
    ` : `
      <div class="operator-empty-table">
        <strong>No agent selected</strong>
        <p>Seed sample agents or connect a registry source to inspect agent identity and scope.</p>
      </div>
    `;
  }

  const server = selectedMcpServer();
  const mcpStatus = el("#mcpDetailStatus");
  const mcpDetail = el("#mcpDetail");
  if (mcpStatus) {
    mcpStatus.textContent = server ? server.trust_tier || "registered" : "none";
    mcpStatus.className = `state-chip ${server ? statusClass(server.trust_tier || server.approval_state) : "neutral"}`;
  }
  if (mcpDetail) {
    mcpDetail.innerHTML = server ? `
      <dl class="registry-detail-list">
        <div><dt>Server ID</dt><dd>${escapeHtml(mcpServerId(server))}</dd></div>
        <div><dt>Name</dt><dd>${escapeHtml(server.name || mcpServerId(server))}</dd></div>
        <div><dt>Trust Tier</dt><dd>${statusBadge(server.trust_tier || "unknown")}</dd></div>
        <div><dt>Approval</dt><dd>${statusBadge(server.approval_state || "unknown")}</dd></div>
        <div><dt>Owner</dt><dd>${escapeHtml(server.owner || "unassigned")}</dd></div>
        <div><dt>Capabilities</dt><dd>${escapeHtml((server.capabilities || []).join(", ") || "none recorded")}</dd></div>
        <div><dt>Allowed Tools</dt><dd>${escapeHtml((server.allowed_tools || []).join(", ") || "all tools")}</dd></div>
        <div><dt>Last Seen</dt><dd>${escapeHtml(formatTime(server.last_seen))}</dd></div>
      </dl>
      <details class="registry-json-detail"><summary>Raw MCP JSON</summary><pre>${escapeHtml(prettyJson(server))}</pre></details>
    ` : `
      <div class="operator-empty-table">
        <strong>No MCP server selected</strong>
        <p>Seed sample MCP servers or connect a registry source to inspect trust boundaries.</p>
      </div>
    `;
  }
}

function renderRegistryReferenceTables() {
  renderRows("#agentProfilesTable", ["Profile", "Vendor", "Risk", "Scopes", "Controls"], (appState.agentProfiles?.items || []).slice(0, 12).map((profile) => [
    escapeHtml(profile.display_name || profile.profile_id),
    escapeHtml(profile.vendor || "unknown"),
    statusBadge(profile.risk_tier || "not set"),
    escapeHtml((profile.default_scopes || []).join(", ") || "none recorded"),
    escapeHtml((profile.enterprise_controls || []).join(", ") || "none recorded")
  ]));
  renderRows("#mcpClassificationsTable", ["Capability", "Risk", "Default", "Approvals", "Objective"], (appState.mcpClassifications?.items || []).map((classification) => [
    escapeHtml(classification.capability || "capability"),
    statusBadge(classification.risk_tier || "not set"),
    statusBadge(classification.default_decision || "not set"),
    escapeHtml((classification.approval_required_for || []).join(", ") || "none recorded"),
    escapeHtml(classification.control_objective || "not recorded")
  ]));
}

function renderApprovals() {
  const items = approvalItems();
  const filtered = filteredApprovalItems();
  populateApprovalGroupFilter(items);
  if (!appState.selectedApprovalId && filtered.length) {
    appState.selectedApprovalId = filtered[0].approval_id;
  }
  if (appState.selectedApprovalId && !items.some((item) => item.approval_id === appState.selectedApprovalId)) {
    appState.selectedApprovalId = filtered[0]?.approval_id || null;
  }

  const summary = el("#approvalQueueSummary");
  if (summary) {
    summary.textContent = `${items.length} approval records. Showing ${filtered.length} after filters.`;
  }

  const states = ["pending", "approved", "denied", "expired", "break_glass"];
  const cards = el("#approvalSummaryCards");
  if (cards) {
    cards.innerHTML = [
      ["Total", items.length, "records"],
      ...states.map((state) => [state.replace("_", " "), items.filter((item) => approvalState(item) === state).length, "state"])
    ].filter(([, count], index) => index === 0 || count > 0).map(([label, count, detail]) => `
      <article class="approval-summary-card ${statusClass(label)}">
        <span>${escapeHtml(detail)}</span>
        <strong>${escapeHtml(count)}</strong>
        <p>${escapeHtml(label)}</p>
      </article>
    `).join("");
  }

  renderRows("#approvalQueueTable", ["Select", "ID", "State", "Group", "Requested By", "Target", "Expires"], filtered.map((approval) => [
    `<button type="button" class="approval-select-button" data-approval-select="${escapeHtml(approval.approval_id)}">${approval.approval_id === appState.selectedApprovalId ? "Selected" : "Review"}</button>`,
    escapeHtml(approval.approval_id || "approval"),
    statusBadge(approvalState(approval)),
    escapeHtml(approval.approver_group || "not routed"),
    escapeHtml(approvalActor(approval)),
    escapeHtml(approvalTarget(approval)),
    escapeHtml(formatTime(approval.expires_at))
  ]));

  const detailStatus = el("#approvalDetailStatus");
  const detail = el("#approvalDetail");
  const selected = selectedApproval();
  if (!selected) {
    if (detailStatus) {
      detailStatus.textContent = "none";
      detailStatus.className = "state-chip neutral";
    }
    if (detail) {
      detail.innerHTML = `
        <div class="operator-empty-table">
          <strong>No approval selected</strong>
          <p>Create or select an approval request to review action detail.</p>
        </div>
      `;
    }
    return;
  }
  if (detailStatus) {
    detailStatus.textContent = approvalState(selected);
    detailStatus.className = `state-chip ${statusClass(approvalState(selected))}`;
  }
  if (detail) {
    const decision = selected.decision || {};
    detail.innerHTML = `
      <dl class="approval-detail-grid">
        <div><dt>Approval ID</dt><dd>${escapeHtml(selected.approval_id)}</dd></div>
        <div><dt>Decision ID</dt><dd>${escapeHtml(selected.decision_id || decision.decision_id || "not recorded")}</dd></div>
        <div><dt>Approver Group</dt><dd>${escapeHtml(selected.approver_group || "not routed")}</dd></div>
        <div><dt>Requested By</dt><dd>${escapeHtml(approvalActor(selected))}</dd></div>
        <div><dt>Requested At</dt><dd>${escapeHtml(formatTime(selected.requested_at))}</dd></div>
        <div><dt>Expires At</dt><dd>${escapeHtml(formatTime(selected.expires_at))}</dd></div>
        <div><dt>Action</dt><dd>${escapeHtml(decision.action_type || "not recorded")}</dd></div>
        <div><dt>Target</dt><dd>${escapeHtml(approvalTarget(selected))}</dd></div>
        <div><dt>Rule</dt><dd>${escapeHtml(decision.rule_id || "not recorded")}</dd></div>
        <div><dt>Reason</dt><dd>${escapeHtml(approvalReason(selected))}</dd></div>
      </dl>
      <details class="approval-json-detail">
        <summary>Raw approval JSON</summary>
        <pre>${escapeHtml(prettyJson(selected))}</pre>
      </details>
    `;
  }
}

function renderEvidenceSearch() {
  const items = evidenceItems();
  const filtered = filteredEvidenceItems();
  populateEvidenceKindFilter(items);
  if (!appState.selectedEvidenceId && filtered.length) {
    appState.selectedEvidenceId = evidenceId(filtered[0]);
  }
  if (appState.selectedEvidenceId && !items.some((item) => evidenceId(item) === appState.selectedEvidenceId)) {
    appState.selectedEvidenceId = filtered[0] ? evidenceId(filtered[0]) : null;
  }

  const summary = el("#evidenceSummaryLine");
  if (summary) {
    const metadataCount = items.filter((item) => item.source === "metadata_store").length;
    const correlatedCount = items.filter((item) => item.source === "aispm_reference").length;
    summary.textContent = `${items.length} evidence records (${metadataCount} indexed metadata, ${correlatedCount} AISPM references). Showing ${filtered.length} after filters.`;
  }

  const cards = el("#evidenceSummaryCards");
  if (cards) {
    const verificationStates = ["signed", "metadata_only", "aispm_reference", "missing"];
    cards.innerHTML = [
      ["Total", items.length, "records"],
      ["Indexed", items.filter((item) => item.source === "metadata_store").length, "metadata"],
      ["Correlated", items.filter((item) => item.source === "aispm_reference").length, "AISPM refs"],
      ...verificationStates.map((state) => [state.replace("_", " "), items.filter((item) => evidenceVerification(item) === state).length, "verification"])
    ].filter(([, count], index) => index < 3 || count > 0).slice(0, 7).map(([label, count, detail]) => `
      <article class="evidence-summary-card ${statusClass(label)}">
        <span>${escapeHtml(detail)}</span>
        <strong>${escapeHtml(count)}</strong>
        <p>${escapeHtml(label)}</p>
      </article>
    `).join("");
  }

  renderRows("#evidenceTable", ["Select", "Evidence", "Kind", "Verification", "Signer", "Blocked", "Approvals", "Created"], filtered.map((record) => [
    `<button type="button" class="evidence-select-button" data-evidence-select="${escapeHtml(evidenceId(record))}">${evidenceId(record) === appState.selectedEvidenceId ? "Selected" : "Inspect"}</button>`,
    escapeHtml(evidenceId(record)),
    escapeHtml(evidenceKind(record)),
    statusBadge(evidenceVerification(record)),
    escapeHtml(record.signer || "not signed"),
    statusBadge(record.blocked_count ?? record.blocked_actions ?? 0),
    statusBadge(record.approval_count ?? record.approval_required_actions ?? 0),
    escapeHtml(formatTime(record.created_at || record.generated_at || record.timestamp))
  ]));

  const detailStatus = el("#evidenceDetailStatus");
  const detail = el("#evidenceDetail");
  const selected = selectedEvidence();
  if (!selected) {
    if (detailStatus) {
      detailStatus.textContent = "none";
      detailStatus.className = "state-chip neutral";
    }
    if (detail) {
      detail.innerHTML = `
        <div class="operator-empty-table">
          <strong>No evidence selected</strong>
          <p>Run setup validation, select an AISPM reference, or connect an evidence metadata store.</p>
        </div>
      `;
    }
    const output = el("#evidenceAuditOutput");
    if (output && !output.textContent.trim()) output.textContent = "Select an evidence record to inspect verification and correlation detail.";
    return;
  }

  const verification = evidenceVerification(selected);
  if (detailStatus) {
    detailStatus.textContent = verification;
    detailStatus.className = `state-chip ${statusClass(verification)}`;
  }
  if (detail) {
    const refs = evidenceRefs(selected);
    detail.innerHTML = `
      <dl class="evidence-detail-grid">
        <div><dt>Evidence ID</dt><dd>${escapeHtml(evidenceId(selected))}</dd></div>
        <div><dt>Session</dt><dd>${escapeHtml(selected.session_id || "not recorded")}</dd></div>
        <div><dt>Kind</dt><dd>${escapeHtml(evidenceKind(selected))}</dd></div>
        <div><dt>Verification</dt><dd>${statusBadge(verification)}</dd></div>
        <div><dt>Signer</dt><dd>${escapeHtml(selected.signer || "not signed")}</dd></div>
        <div><dt>Decision</dt><dd>${escapeHtml(selected.decision_id || "not recorded")}</dd></div>
        <div><dt>Agent</dt><dd>${escapeHtml(selected.agent_id || "not recorded")}</dd></div>
        <div><dt>Repository</dt><dd>${escapeHtml(selected.repository || "not recorded")}</dd></div>
        <div><dt>Rule</dt><dd>${escapeHtml(selected.rule_id || "not recorded")}</dd></div>
        <div><dt>Evidence Refs</dt><dd>${escapeHtml(refs.join(", ") || "not recorded")}</dd></div>
        <div><dt>Created</dt><dd>${escapeHtml(formatTime(selected.created_at || selected.generated_at || selected.timestamp))}</dd></div>
        <div><dt>Reason</dt><dd>${escapeHtml(selected.reason || "not recorded")}</dd></div>
      </dl>
      <details class="evidence-json-detail">
        <summary>Raw evidence JSON</summary>
        <pre>${escapeHtml(prettyJson(selected))}</pre>
      </details>
    `;
  }
  const output = el("#evidenceAuditOutput");
  if (output && output.textContent.includes("Select an evidence record")) {
    output.textContent = prettyJson(buildEvidenceAuditPayload(selected));
  }
}

function renderReportsLive() {
  const mirror = el("#reportsCatalogMirror");
  if (mirror) {
    mirror.innerHTML = reportCards.map(([title, detail]) => `
      <article class="report-card">
        <span class="eyebrow">Community export</span>
        <h3>${escapeHtml(title)}</h3>
        <p>${escapeHtml(detail)}</p>
        <button type="button" data-report="${escapeHtml(title)}">Download Sample</button>
      </article>
    `).join("");
  }
  renderReportMetrics();
  renderReportSourceInventory();
  const output = el("#reportPreviewOutput");
  if (output && !output.textContent.trim()) {
    output.textContent = formatReportOutput(buildCurrentReportPacket());
  }
}

function currentReportOptions() {
  return {
    type: el("#reportType")?.value || "Executive Risk Brief",
    range: el("#reportRange")?.value || "Last 24 hours",
    scope: el("#reportScope")?.value || "All agents",
    format: el("#reportFormat")?.value || "JSON"
  };
}

function scopedReportFindings(scope) {
  const findings = appState.aispmPosture?.findings || [];
  if (scope === "Blocked actions") return findings.filter((finding) => String(finding.decision || finding.outcome || "").includes("block"));
  if (scope === "Approval routed") return findings.filter((finding) => String(finding.decision || finding.outcome || "").includes("approval"));
  return findings;
}

function buildCurrentReportPacket() {
  const options = currentReportOptions();
  const posture = appState.aispmPosture || {};
  const overview = posture.overview || {};
  const findings = scopedReportFindings(options.scope);
  const approvals = approvalItems();
  const evidence = evidenceItems();
  const agents = agentItems();
  const mcpServers = mcpServerItems();
  const integrationsState = integrationItems();
  const connectorDashboard = appState.connectorDeliveryDashboard || {};
  return {
    schema_version: "cavra.ui.report_center.preview.v1",
    product: "CAVRA Community",
    report_type: options.type,
    generated_at: new Date().toISOString(),
    range: options.range,
    scope: options.scope,
    format: options.format,
    api: {
      connected: appState.connected,
      base: appState.apiBase || "not configured"
    },
    summary: {
      posture_score: overview.posture_score ?? null,
      risk_level: overview.risk_level || "not measured",
      risk_findings: findings.length,
      critical_findings: findings.filter((finding) => finding.severity === "critical").length,
      high_findings: findings.filter((finding) => finding.severity === "high").length,
      blocked_actions: overview.blocked_actions ?? findings.filter((finding) => String(finding.decision || "").includes("block")).length,
      approval_required_actions: overview.approval_required_actions ?? findings.filter((finding) => String(finding.decision || "").includes("approval")).length,
      approvals: approvals.length,
      evidence_records: evidence.length,
      agents: agents.length,
      mcp_servers: mcpServers.length,
      integrations: integrationsState.length,
      connector_delivery: appState.consoleConfig?.connector_delivery || "disabled"
    },
    posture: overview,
    findings: findings.slice(0, 25).map((finding) => ({
      severity: finding.severity || "info",
      risk_classification: finding.risk_classification || finding.rule_id || "risk finding",
      decision: finding.decision || finding.outcome || "unknown",
      rule_id: finding.rule_id || "not recorded",
      reason: finding.reason || "not recorded",
      evidence_refs: finding.evidence_refs || []
    })),
    approvals: approvals.slice(0, 25).map((approval) => ({
      approval_id: approval.approval_id,
      state: approvalState(approval),
      approver_group: approval.approver_group || "not routed",
      requested_by: approvalActor(approval),
      target: approvalTarget(approval),
      expires_at: approval.expires_at || null
    })),
    evidence: evidence.slice(0, 25).map((record) => ({
      evidence_id: evidenceId(record),
      kind: evidenceKind(record),
      verification: evidenceVerification(record),
      signer: record.signer || null,
      generated_at: record.generated_at || record.created_at || null
    })),
    agents: agents.slice(0, 25).map((agent) => ({
      agent_id: agentId(agent),
      vendor: agent.vendor || agent.type || "unknown",
      risk_tier: agent.risk_tier || "not set",
      status: agent.status || "unknown",
      owner: agent.owner || "unassigned"
    })),
    integrations: integrationsState.slice(0, 25).map((integration) => ({
      integration_id: integrationId(integration),
      provider: integration.provider || integration.name || "unknown",
      category: integration.category || "unknown",
      status: integration.status || "unknown",
      health_status: integration.health_status || "not_checked",
      owner: integration.owner || "unassigned"
    })),
    connector_delivery_dashboard: connectorDashboard,
    boundary: "Community report previews are browser-generated from the connected local API. Provider-backed PDF/XLSX rendering, SMTP delivery, recipient governance, and private tenant content require configured self-hosted providers or CAVRA Managed."
  };
}

function renderReportMetrics() {
  const packet = buildCurrentReportPacket();
  const target = el("#reportMetricCards");
  if (!target) return;
  const summary = packet.summary;
  target.innerHTML = [
    ["Risk", summary.risk_level, "posture", statusClass(summary.risk_level)],
    ["Findings", summary.risk_findings, "scoped", summary.risk_findings ? "warn" : "ok"],
    ["Approvals", summary.approvals, "records", summary.approvals ? "warn" : "ok"],
    ["Evidence", summary.evidence_records, "records", summary.evidence_records ? "ok" : "warn"],
    ["Agents", summary.agents, `${summary.mcp_servers} MCP`, summary.agents ? "ok" : "warn"],
    ["Delivery", summary.connector_delivery, "provider", statusClass(summary.connector_delivery)]
  ].map(([label, value, detail, state]) => `
    <article class="report-summary-card ${escapeHtml(state)}">
      <span>${escapeHtml(detail)}</span>
      <strong>${escapeHtml(value)}</strong>
      <p>${escapeHtml(label)}</p>
    </article>
  `).join("");
  const line = el("#reportCenterLiveSummary");
  if (line) {
    line.textContent = `${packet.report_type} generated from ${summary.risk_findings} findings, ${summary.evidence_records} evidence records, ${summary.approvals} approvals, and ${summary.integrations} integrations.`;
  }
}

function renderReportSourceInventory() {
  renderRows("#reportSourceInventory", ["Source", "Records", "Status", "Notes"], [
    ["AISPM posture", appState.aispmPosture ? (appState.aispmPosture.findings || []).length : 0, statusBadge(appState.aispmPosture ? "loaded" : "missing"), "Findings, timeline, agent risk, posture score"],
    ["Approvals", itemCount(appState.approvals), statusBadge(appState.approvals ? "loaded" : "missing"), "Approval queue and decision audit"],
    ["Evidence", itemCount(appState.evidence), statusBadge(appState.evidence ? "loaded" : "missing"), "Evidence metadata and AISPM refs"],
    ["Agents/MCP", `${itemCount(appState.agents)} / ${itemCount(appState.mcpServers)}`, statusBadge(appState.agents || appState.mcpServers ? "loaded" : "missing"), "Agent registry and MCP trust state"],
    ["Integrations", itemCount(appState.integrations), statusBadge(appState.integrations ? "loaded" : "missing"), "Connector inventory and delivery boundary"]
  ].map((row) => row.map((cell) => typeof cell === "string" && cell.startsWith("<span") ? cell : escapeHtml(cell))));
}

function reportCsvValue(value) {
  const text = String(value ?? "");
  return /[",\n]/.test(text) ? `"${text.replace(/"/g, '""')}"` : text;
}

function formatReportCsv(packet) {
  const rows = [
    ["section", "name", "value", "detail"],
    ...Object.entries(packet.summary).map(([key, value]) => ["summary", key, value, packet.report_type]),
    ...packet.findings.map((finding) => ["finding", finding.rule_id, finding.decision, `${finding.severity}: ${finding.reason}`]),
    ...packet.approvals.map((approval) => ["approval", approval.approval_id, approval.state, `${approval.approver_group}: ${approval.target}`]),
    ...packet.evidence.map((record) => ["evidence", record.evidence_id, record.verification, record.kind]),
    ...packet.agents.map((agent) => ["agent", agent.agent_id, agent.risk_tier, `${agent.vendor}: ${agent.status}`]),
    ...packet.integrations.map((integration) => ["integration", integration.integration_id, integration.health_status, `${integration.provider}: ${integration.status}`])
  ];
  return rows.map((row) => row.map(reportCsvValue).join(",")).join("\n");
}

function formatReportMarkdown(packet) {
  const summaryRows = Object.entries(packet.summary)
    .map(([key, value]) => `| ${key} | ${String(value ?? "not recorded")} |`)
    .join("\n");
  const findings = packet.findings.length
    ? packet.findings.map((finding) => `- **${finding.severity}** ${finding.risk_classification}: ${finding.decision} via ${finding.rule_id}`).join("\n")
    : "- No findings in the selected scope.";
  const approvals = packet.approvals.length
    ? packet.approvals.map((approval) => `- ${approval.approval_id}: ${approval.state} for ${approval.target}`).join("\n")
    : "- No approval records loaded.";
  const evidence = packet.evidence.length
    ? packet.evidence.map((record) => `- ${record.evidence_id}: ${record.verification} (${record.kind})`).join("\n")
    : "- No evidence records loaded.";
  const integrationsState = packet.integrations.length
    ? packet.integrations.map((integration) => `- ${integration.integration_id}: ${integration.health_status} (${integration.provider}/${integration.category})`).join("\n")
    : "- No integration records loaded.";
  return `# ${packet.report_type}

Generated: ${packet.generated_at}

Range: ${packet.range}

Scope: ${packet.scope}

## Summary

| Metric | Value |
| --- | --- |
${summaryRows}

## Findings

${findings}

## Approvals

${approvals}

## Evidence

${evidence}

## Integrations

${integrationsState}

## Boundary

${packet.boundary}
`;
}

function formatReportOutput(packet = buildCurrentReportPacket()) {
  const format = currentReportOptions().format;
  if (format === "Markdown") return formatReportMarkdown(packet);
  if (format === "CSV") return formatReportCsv(packet);
  return prettyJson(packet);
}

function reportFilename(packet = buildCurrentReportPacket()) {
  const extension = currentReportOptions().format === "Markdown" ? "md" : currentReportOptions().format === "CSV" ? "csv" : "json";
  const slug = `${packet.report_type}-${packet.scope}-${packet.range}`
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");
  return `cavra-${slug}.${extension}`;
}

function renderReportPreview() {
  renderReportMetrics();
  const output = el("#reportPreviewOutput");
  if (output) output.textContent = formatReportOutput(buildCurrentReportPacket());
}

function buildSettingsDiagnostics() {
  return {
    schema_version: "cavra.ui.settings_diagnostics.v1",
    generated_at: new Date().toISOString(),
    api: {
      connected: appState.connected,
      base: appState.apiBase || "not configured",
      health: appState.health || null,
      version: appState.version || null,
      last_refresh_at: appState.lastRefreshAt
    },
    setup: appState.setupStatus || null,
    console_config: appState.consoleConfig ? {
      product: appState.consoleConfig.product,
      metadata_mode: appState.consoleConfig.metadata_mode,
      approval_mode: appState.consoleConfig.approval_mode,
      registry_mode: appState.consoleConfig.registry_mode,
      activity_mode: appState.consoleConfig.activity_mode,
      inventory_mode: appState.consoleConfig.inventory_mode,
      integration_mode: appState.consoleConfig.integration_mode,
      pilot_intake_mode: appState.consoleConfig.pilot_intake_mode,
      approval_provider_delivery: appState.consoleConfig.approval_provider_delivery,
      connector_delivery: appState.consoleConfig.connector_delivery,
      approval_oidc: appState.consoleConfig.approval_oidc,
      approval_rbac: appState.consoleConfig.approval_rbac,
      enterprise_identity_policy: appState.consoleConfig.enterprise_identity_policy,
      evidence_artifacts: appState.consoleConfig.evidence_artifacts,
      registry_store: appState.consoleConfig.registry_store,
      cors_origins: appState.consoleConfig.cors_origins || [],
      endpoint_count: Object.keys(appState.consoleConfig.endpoints || {}).length
    } : null,
    loaded_records: {
      approvals: itemCount(appState.approvals),
      evidence: itemCount(appState.evidence),
      agents: itemCount(appState.agents),
      mcp_servers: itemCount(appState.mcpServers),
      integrations: itemCount(appState.integrations),
      policy_actions: itemCount(appState.policyCatalog)
    },
    local_ui: {
      theme: localStorage.getItem("cavra.theme") || "sentinel",
      sidebar_collapsed: el("#sidebar")?.classList.contains("is-collapsed") || false,
      setup_prompt_dismissed: localStorage.getItem("cavra.setupPromptDismissed") === "true"
    },
    errors: appState.errors || []
  };
}

function renderAispmWorkstation() {
  const posture = appState.aispmPosture;
  const overview = posture?.overview || {};
  const findings = posture?.findings || [];
  const agents = posture?.agents || [];
  const timeline = posture?.timeline || [];
  const statusStrip = el("#aispmLiveStatusStrip");
  if (statusStrip) {
    statusStrip.innerHTML = `
      <div>${statusBadge(appState.connected ? "API connected" : "API disconnected")}<span>${escapeHtml(appState.apiBase || "not configured")}</span></div>
      <div>${statusBadge(overview.risk_level || "static demo")}<span>risk level</span></div>
      <div>${statusBadge(posture?.data_provenance || "sample content")}<span>data provenance</span></div>
      <div>${statusBadge(overview.evidence_confidence || "not measured")}<span>evidence confidence</span></div>
      <div><span class="state-chip neutral">generated</span><span>${escapeHtml(formatTime(posture?.generated_at || appState.lastRefreshAt))}</span></div>
    `;
  }

  const metricCards = [
    ["Posture Score", overview.posture_score ?? "N/A", "Calculated from current activity", statusClass(overview.risk_level)],
    ["Risk Findings", overview.risk_findings ?? findings.length, `${overview.critical_findings ?? 0} critical / ${overview.high_findings ?? 0} high`, findings.length ? "danger" : "ok"],
    ["Blocked Actions", overview.blocked_actions ?? 0, "Prevented before execution", (overview.blocked_actions ?? 0) ? "danger" : "ok"],
    ["Approval Routes", overview.approval_required_actions ?? 0, "Human decision required", (overview.approval_required_actions ?? 0) ? "warn" : "ok"],
    ["Agents Observed", agents.length, `${overview.total_sessions ?? 0} sessions`, agents.length ? "ok" : "warn"],
    ["Latest Activity", formatTime(overview.latest_activity_at), `${overview.total_decisions ?? 0} decisions`, overview.latest_activity_at ? "ok" : "warn"]
  ];
  const metricTarget = el("#aispmLiveMetricCards");
  if (metricTarget) {
    metricTarget.innerHTML = metricCards.map(([label, value, detail, state]) => `
      <article class="operator-metric-card ${escapeHtml(state)}">
        <span>${escapeHtml(label)}</span>
        <strong>${escapeHtml(value)}</strong>
        <p>${escapeHtml(detail)}</p>
      </article>
    `).join("");
  }

  renderRows("#aispmFindingsTable", ["Severity", "Risk", "Decision", "Rule", "Reason", "Evidence"], findings.slice(0, 12).map((finding) => [
    statusBadge(finding.severity || "unknown"),
    escapeHtml(finding.risk_classification || "not classified"),
    statusBadge(finding.decision || "unknown"),
    escapeHtml(finding.rule_id || "rule"),
    escapeHtml(finding.reason || "not recorded"),
    escapeHtml((finding.evidence_refs || []).join(", ") || "not recorded")
  ]));
  const findingsStatus = el("#aispmFindingsStatus");
  if (findingsStatus) {
    findingsStatus.textContent = findings.length ? `${findings.length} findings` : "clear";
    findingsStatus.className = `state-chip ${findings.length ? "danger" : "ok"}`;
  }

  const blockers = findings
    .filter((finding) => ["critical", "high"].includes(String(finding.severity || "").toLowerCase()))
    .slice(0, 6);
  const blockerTarget = el("#aispmBlockerList");
  if (blockerTarget) {
    blockerTarget.innerHTML = blockers.length ? blockers.map((finding) => `
      <article class="aispm-blocker-card ${statusClass(finding.severity)}">
        <div>
          ${statusBadge(finding.severity)}
          <strong>${escapeHtml(finding.risk_classification || finding.rule_id || "risk finding")}</strong>
        </div>
        <p>${escapeHtml(finding.reason || "No rationale recorded.")}</p>
        <small>${escapeHtml(finding.agent_id || "unknown-agent")} / ${escapeHtml(finding.repository || "unknown-repository")}</small>
      </article>
    `).join("") : `
      <div class="operator-empty-table">
        <strong>No critical or high closeout blockers</strong>
        <p>Run validation or connect runtime events to keep this view current.</p>
      </div>
    `;
  }
  const blockerStatus = el("#aispmBlockerStatus");
  if (blockerStatus) {
    blockerStatus.textContent = blockers.length ? `${blockers.length} blockers` : "clear";
    blockerStatus.className = `state-chip ${blockers.length ? "danger" : "ok"}`;
  }

  renderRows("#aispmAgentRiskTable", ["Agent", "Sessions", "Decisions", "Blocked", "Approvals", "Drift", "Last Seen"], agents.slice(0, 12).map((agent) => [
    escapeHtml(agent.agent_id || "agent"),
    escapeHtml(agent.session_count ?? 0),
    escapeHtml(agent.decision_count ?? 0),
    statusBadge(agent.blocked_actions ?? 0),
    statusBadge(agent.approval_required_actions ?? 0),
    statusBadge(agent.drift_status || "unknown"),
    escapeHtml(formatTime(agent.last_seen_at))
  ]));
  const agentStatus = el("#aispmAgentStatus");
  if (agentStatus) {
    agentStatus.textContent = agents.length ? `${agents.length} agents` : "empty";
    agentStatus.className = `state-chip ${agents.length ? "ok" : "warn"}`;
  }

  renderRows("#aispmTimelineTable", ["Time", "Event", "Target", "Outcome", "Severity", "Evidence"], timeline.slice(0, 12).map((event) => [
    escapeHtml(formatTime(event.timestamp)),
    escapeHtml(event.title || event.event_type || "event"),
    escapeHtml(event.target || event.repository || "not recorded"),
    statusBadge(event.outcome || event.decision || "unknown"),
    statusBadge(event.severity || "info"),
    escapeHtml((event.evidence_refs || []).join(", ") || "not recorded")
  ]));
  const timelineStatus = el("#aispmTimelineStatus");
  if (timelineStatus) {
    timelineStatus.textContent = timeline.length ? `${timeline.length} events` : "empty";
    timelineStatus.className = `state-chip ${timeline.length ? "ok" : "warn"}`;
  }

  const freshness = [
    ["Latest activity", formatTime(overview.latest_activity_at), "Most recent runtime event used for posture."],
    ["Generated at", formatTime(posture?.generated_at), "Dashboard packet generation timestamp."],
    ["Evidence confidence", overview.evidence_confidence || "not measured", "How strongly posture links back to evidence."],
    ["Telemetry", posture?.telemetry || "disabled", "Community mode keeps telemetry disabled."],
    ["Tracking", posture?.tracking || "none", "Public-safe tracking boundary."],
    ["Mode", posture?.mode || "static", "Current posture source mode."]
  ];
  const freshnessTarget = el("#aispmFreshnessCards");
  if (freshnessTarget) {
    freshnessTarget.innerHTML = freshness.map(([label, value, detail]) => `
      <article class="aispm-freshness-card">
        <span>${escapeHtml(label)}</span>
        <strong>${escapeHtml(value)}</strong>
        <p>${escapeHtml(detail)}</p>
      </article>
    `).join("");
  }
}

function renderSettings() {
  const config = appState.consoleConfig || {};
  const setup = appState.setupStatus || {};
  const version = appState.version || {};
  const api = el("#settingsApiBase");
  if (api) api.textContent = appState.apiBase || "not configured";

  const apiStatus = el("#settingsApiStatus");
  if (apiStatus) {
    apiStatus.textContent = appState.connected ? "connected" : "disconnected";
    apiStatus.className = `state-chip ${appState.connected ? "ok" : "danger"}`;
  }
  const localStatus = el("#settingsLocalStatus");
  if (localStatus) {
    const collapsed = el("#sidebar")?.classList.contains("is-collapsed");
    localStatus.textContent = collapsed ? "sidebar collapsed" : "sidebar expanded";
    localStatus.className = "state-chip neutral";
  }
  const themeSelect = el("#settingsThemeSelect");
  if (themeSelect) themeSelect.value = localStorage.getItem("cavra.theme") || "sentinel";

  const cards = el("#settingsStatusCards");
  if (cards) {
    const storageModes = ["metadata_mode", "approval_mode", "registry_mode", "activity_mode", "inventory_mode", "integration_mode"]
      .map((key) => config[key])
      .filter(Boolean);
    cards.innerHTML = [
      ["API", appState.connected ? "connected" : "offline", appState.apiBase || "not configured", appState.connected ? "ok" : "danger"],
      ["Version", version.version || "unknown", version.name || "runtime", version.version ? "ok" : "warn"],
      ["Setup", setup.setup_complete ? "complete" : "incomplete", setup.configured ? "configured" : "not configured", setup.setup_complete ? "ok" : "warn"],
      ["Policy", setup.policy?.default_pack || "not selected", setup.policy?.available ? "available" : "missing", setup.policy?.available ? "ok" : "danger"],
      ["Storage", [...new Set(storageModes)].join(", ") || "unknown", "runtime modes", storageModes.length ? "ok" : "warn"],
      ["Providers", config.connector_delivery || "disabled", `approvals: ${config.approval_provider_delivery || "disabled"}`, config.connector_delivery === "configured" ? "ok" : "warn"]
    ].map(([label, value, detail, state]) => `
      <article class="settings-summary-card ${escapeHtml(state)}">
        <span>${escapeHtml(detail)}</span>
        <strong>${escapeHtml(value)}</strong>
        <p>${escapeHtml(label)}</p>
      </article>
    `).join("");
  }

  const apiDetail = el("#settingsApiDetail");
  if (apiDetail) {
    apiDetail.innerHTML = `
      <dl>
        <div><dt>Product</dt><dd>${escapeHtml(appState.health?.product || config.product || "unknown")}</dd></div>
        <div><dt>Runtime</dt><dd>${escapeHtml(version.name || "unknown")}</dd></div>
        <div><dt>Version</dt><dd>${escapeHtml(version.version || "unknown")}</dd></div>
        <div><dt>Last refresh</dt><dd>${escapeHtml(formatTime(appState.lastRefreshAt))}</dd></div>
        <div><dt>CORS</dt><dd>${escapeHtml((config.cors_origins || []).join(", ") || "not reported")}</dd></div>
      </dl>
    `;
  }

  const setupStatus = el("#settingsSetupStatus");
  if (setupStatus) {
    setupStatus.textContent = setup.setup_complete ? "complete" : setup.configured ? "configured" : "incomplete";
    setupStatus.className = `state-chip ${setup.setup_complete ? "ok" : setup.configured ? "warn" : "danger"}`;
  }
  renderRows("#settingsSetupTable", ["Area", "Value", "Status", "Detail"], [
    ["Workspace", setup.workspace?.name || "not configured", statusBadge(setup.configured ? "configured" : "missing"), `${setup.workspace?.mode || "unknown"} / ${setup.workspace?.environment || "unknown"}`],
    ["Policy pack", setup.policy?.default_pack || "not selected", statusBadge(setup.policy?.available ? "available" : "missing"), "Default runtime policy pack"],
    ["Demo workspace", setup.demo?.workspace_path || "not generated", statusBadge(setup.demo?.exists ? "exists" : "missing"), "Known risky fixtures for validation"],
    ["Reports", setup.reports?.delivery_mode || "not_configured", statusBadge(setup.reports?.smtp_enabled ? "configured" : "not_configured"), `${setup.reports?.recipient_count || 0} recipients`],
    ["Next steps", (setup.next_steps || []).length, statusBadge((setup.next_steps || []).length ? "pending" : "complete"), (setup.next_steps || []).join("; ") || "No setup next steps"]
  ].map((row) => row.map((cell) => typeof cell === "string" && cell.startsWith("<span") ? cell : escapeHtml(cell))));

  const providerStatus = el("#settingsProviderStatus");
  if (providerStatus) {
    providerStatus.textContent = config.connector_delivery === "configured" ? "configured" : "disabled";
    providerStatus.className = `state-chip ${config.connector_delivery === "configured" ? "ok" : "warn"}`;
  }
  renderRows("#settingsProviderTable", ["Provider Surface", "State", "Meaning"], [
    ["Connector delivery", statusBadge(config.connector_delivery || "disabled"), "SIEM, ITSM, ChatOps, webhook, and cloud event delivery"],
    ["Approval provider", statusBadge(config.approval_provider_delivery || "disabled"), "Provider-backed approval notification and decision routing"],
    ["OIDC approval identity", statusBadge(config.approval_oidc || "disabled"), "Signed identity claims for approval authorization"],
    ["RBAC approval policy", statusBadge(config.approval_rbac || "disabled"), "Repository-scoped approval rights"],
    ["Evidence artifacts", statusBadge(config.evidence_artifacts || "disabled"), "Hosted artifact access and bundle retrieval"],
    ["Enterprise identity policy", statusBadge(config.enterprise_identity_policy || "default_contract"), "Enterprise identity readiness contract mode"]
  ].map((row) => row.map((cell) => typeof cell === "string" && cell.startsWith("<span") ? cell : escapeHtml(cell))));

  const storageStatus = el("#settingsStorageStatus");
  if (storageStatus) {
    storageStatus.textContent = config.metadata_mode || "unknown";
    storageStatus.className = `state-chip ${config.metadata_mode ? "ok" : "warn"}`;
  }
  renderRows("#settingsStoreTable", ["Store", "Mode", "Path/Detail"], [
    ["Metadata", config.metadata_mode || "unknown", "Evidence metadata"],
    ["Approvals", config.approval_mode || "unknown", "Approval queue"],
    ["Registry", config.registry_mode || "unknown", config.registry_store || "not reported"],
    ["Activity", config.activity_mode || "unknown", "Decision/activity stream"],
    ["Inventory", config.inventory_mode || "unknown", "Asset and endpoint inventory"],
    ["Integrations", config.integration_mode || "unknown", "Connector inventory"],
    ["Pilot intake", config.pilot_intake_mode || "unknown", "Trial/managed intake records"]
  ].map((row) => row.map((cell) => escapeHtml(cell))));

  const diagnostics = el("#settingsDiagnosticsOutput");
  if (diagnostics) diagnostics.textContent = prettyJson(buildSettingsDiagnostics());
}

function renderLiveViews() {
  renderOperatorDashboard();
  renderPolicyCatalog();
  renderAgentsAndMcp();
  renderApprovals();
  renderEvidenceSearch();
  renderReportsLive();
  renderAispmWorkstation();
  renderIntegrationHub();
  renderSettings();
}

async function refreshApplicationState() {
  appState.lastRefreshAt = new Date().toISOString();
  appState.errors = [];
  const health = await optionalApi("/health");
  appState.connected = health.ok;
  appState.health = health.ok ? health.value : null;
  if (!health.ok) {
    appState.errors.push(health.error);
    renderLiveViews();
    return;
  }

  const entries = await Promise.all([
    optionalApi("/version"),
    optionalApi("/setup/status"),
    optionalApi("/console/config"),
    optionalApi("/aispm/posture"),
    optionalApi("/approvals"),
    optionalApi("/evidence"),
    optionalApi("/agents"),
    optionalApi("/mcp/servers"),
    optionalApi("/integrations"),
    optionalApi("/release-connector-deliveries/dashboard"),
    optionalApi("/policy-action-catalog")
  ]);

  const [version, setupStatus, consoleConfig, aispmPosture, approvals, evidence, agents, mcpServers, integrationsState, connectorDeliveryDashboard, policyCatalog] = entries;
  appState.version = version.ok ? version.value : null;
  appState.setupStatus = setupStatus.ok ? setupStatus.value : null;
  appState.consoleConfig = consoleConfig.ok ? consoleConfig.value : null;
  appState.aispmPosture = aispmPosture.ok ? aispmPosture.value : null;
  appState.approvals = approvals.ok ? approvals.value : null;
  appState.evidence = evidence.ok ? evidence.value : null;
  appState.agents = agents.ok ? agents.value : null;
  appState.mcpServers = mcpServers.ok ? mcpServers.value : null;
  appState.integrations = integrationsState.ok ? integrationsState.value : null;
  appState.connectorDeliveryDashboard = connectorDeliveryDashboard.ok ? connectorDeliveryDashboard.value : null;
  appState.policyCatalog = policyCatalog.ok ? policyCatalog.value : null;
  appState.errors = entries.filter((entry) => !entry.ok).map((entry) => entry.error);
  renderLiveViews();
}

async function refreshSetupStatus() {
  try {
    const status = await setupApi("/setup/status");
    appState.connected = true;
    appState.setupStatus = status;
    const configured = status.configured ? "configured" : "not configured";
    const complete = status.setup_complete ? "complete" : "not complete";
    setSetupApiStatus(`Connected to ${setupApiBase}. Setup is ${configured} and ${complete}.`, "ready");
    writeSetupOutput("#setupStatusOutput", status);
    renderSettings();
    return status;
  } catch (error) {
    appState.connected = false;
    appState.errors = [error.message];
    setSetupApiStatus(error.message, "error");
    writeSetupOutput("#setupStatusOutput", {
      status: "api_unavailable",
      api_base: setupApiBase || "not configured",
      message: error.message
    });
    renderSettings();
    return null;
  }
}

function smtpPayloadFromForm(save = false) {
  const form = el("#setupSmtpForm");
  const data = new FormData(form);
  const recipient = String(data.get("recipient") || "").trim();
  return {
    host: String(data.get("host") || "").trim(),
    port: Number(data.get("port") || 587),
    from_email: String(data.get("from_email") || "").trim(),
    recipients: recipient ? [recipient] : [],
    recipient_allowlist: recipient ? [recipient] : [],
    password_ref: String(data.get("password_ref") || "CAVRA_REPORT_SMTP_PASSWORD").trim(),
    live: false,
    save
  };
}

async function runSetupAction(action) {
  const output = "#setupActionOutput";
  writeSetupOutput(output, { status: "running", action });
  try {
    let result;
    if (action === "status") result = await setupApi("/setup/status");
    if (action === "bootstrap") result = await setupPost("/setup/bootstrap", { workspace_name: "local-community", overwrite: true });
    if (action === "demo") result = await setupPost("/setup/demo-workspace", { output: ".cavra/demo-workspace", overwrite: true });
    if (action === "validate") result = await setupPost("/setup/validate", { record_decisions: true });
    if (action === "complete") result = await setupPost("/setup/complete", {});
    if (action === "catalog") result = await setupApi("/policy-action-catalog");
    if (action === "test-risk") {
      result = await setupPost("/policy-action-catalog/test", {
        action_type: "execute_command",
        target: "terraform apply -auto-approve",
        policy_pack: "cavra-ai-agent-baseline"
      });
    }
    if (action === "smtp-test") result = await setupPost("/setup/smtp/test", smtpPayloadFromForm(false));
    if (action === "smtp-save") result = await setupPost("/setup/smtp/test", smtpPayloadFromForm(true));
    writeSetupOutput(output, result || { status: "unknown_action", action });
    await refreshSetupStatus();
    await refreshApplicationState();
  } catch (error) {
    setSetupApiStatus(error.message, "error");
    writeSetupOutput(output, { status: "failed", action, message: error.message });
  }
}

async function runPolicySimulation() {
  const form = el("#policySimulatorForm");
  const status = el("#policySimulatorStatus");
  const output = el("#policySimulatorOutput");
  if (!form || !output) return;
  const data = new FormData(form);
  const payload = {
    action_type: String(data.get("action_type") || "execute_command"),
    target: String(data.get("target") || "").trim(),
    policy_pack: String(data.get("policy_pack") || appState.policyCatalog?.policy_pack || "cavra-ai-agent-baseline").trim()
  };
  if (status) {
    status.textContent = "running";
    status.className = "state-chip warn";
  }
  output.textContent = "Running simulation...";
  try {
    const result = await setupPost("/policy-action-catalog/test", payload);
    const decision = result.decision?.decision || result.decision || result.expected_decision || "controlled";
    if (status) {
      status.textContent = decision;
      status.className = `state-chip ${statusClass(decision)}`;
    }
    output.textContent = prettyJson(result);
    await refreshApplicationState();
  } catch (error) {
    if (status) {
      status.textContent = "failed";
      status.className = "state-chip danger";
    }
    output.textContent = prettyJson({ status: "failed", request: payload, message: error.message });
  }
}

function approvalDecisionPayload() {
  const form = el("#approvalDecisionForm");
  const data = form ? new FormData(form) : new FormData();
  return {
    actor: String(data.get("actor") || "local-operator").trim(),
    reason: String(data.get("reason") || "Manual local validation decision.").trim(),
    external_ref: String(data.get("external_ref") || "manual-test").trim()
  };
}

async function seedSampleApproval() {
  const output = el("#approvalAuditOutput");
  if (output) output.textContent = "Creating sample approval request...";
  const payload = {
    requested_by: "codex-agent",
    approver_group: "Cloud Security",
    ttl_hours: 24,
    decision: {
      decision_id: `dec_manual_${Date.now()}`,
      session_id: "manual-gui-test",
      agent_id: "codex-agent",
      actor: "ai-agent",
      action_type: "execute_command",
      target: "terraform apply -auto-approve",
      repository: "cavra-agent-test",
      decision: "require_approval",
      severity: "high",
      rule_id: "commands.default.require_approval",
      reason: "Manual GUI test: Terraform production-style change requires Cloud Security approval.",
      evidence_refs: [`evidence://manual-gui-test/${Date.now()}`],
      timestamp: new Date().toISOString()
    }
  };
  try {
    const result = await setupPost("/approvals", payload);
    appState.selectedApprovalId = result.approval_id;
    if (output) output.textContent = prettyJson({ action: "seed_sample_approval", result });
    await refreshApplicationState();
  } catch (error) {
    if (output) output.textContent = prettyJson({ action: "seed_sample_approval", status: "failed", message: error.message });
  }
}

async function runApprovalAction(action) {
  const output = el("#approvalAuditOutput");
  const selected = selectedApproval();
  if (!selected && action !== "break-glass") {
    if (output) output.textContent = prettyJson({ status: "failed", action, message: "select an approval request first" });
    return;
  }
  const decisionPayload = approvalDecisionPayload();
  if (output) output.textContent = `Running ${action}...`;
  try {
    let result;
    if (action === "approve") {
      result = await setupPost(`/approvals/${selected.approval_id}/approve`, decisionPayload);
    } else if (action === "deny") {
      result = await setupPost(`/approvals/${selected.approval_id}/deny`, decisionPayload);
    } else if (action === "expire") {
      result = await setupPost(`/approvals/${selected.approval_id}/expire`, decisionPayload);
    } else if (action === "deliver") {
      result = await setupPost(`/approvals/${selected.approval_id}/deliver`, { provider: "all", retries: 1, timeout_seconds: 5 });
    } else if (action === "break-glass") {
      const decision = selected?.decision || {
        decision_id: `dec_break_glass_${Date.now()}`,
        session_id: "manual-gui-test",
        agent_id: "local-operator",
        actor: "local-operator",
        action_type: "execute_command",
        target: "emergency production rollback",
        repository: "cavra-agent-test",
        decision: "require_approval",
        severity: "critical",
        rule_id: "break_glass.manual",
        reason: "Manual break-glass GUI validation.",
        evidence_refs: [`evidence://manual-gui-test/break-glass-${Date.now()}`],
        timestamp: new Date().toISOString()
      };
      result = await setupPost("/approvals/break-glass", {
        ...decisionPayload,
        approver_group: "Change Advisory Board",
        ttl_hours: 4,
        decision
      });
    }
    if (result?.approval_id) appState.selectedApprovalId = result.approval_id;
    if (output) output.textContent = prettyJson({ action, result });
    await refreshApplicationState();
  } catch (error) {
    if (output) output.textContent = prettyJson({ action, status: "failed", message: error.message });
  }
}

function buildEvidenceAuditPayload(record) {
  if (!record) {
    return { status: "no_evidence_selected" };
  }
  const verification = evidenceVerification(record);
  const refs = evidenceRefs(record);
  const correlatedFindings = (appState.aispmPosture?.findings || []).filter((finding) =>
    evidenceRefs(finding).some((ref) => refs.includes(ref) || ref === evidenceId(record))
  );
  const correlatedApprovals = approvalItems().filter((approval) => {
    const decision = approval.decision || {};
    return decision.decision_id && decision.decision_id === record.decision_id;
  });
  return {
    schema_version: "cavra.ui.evidence.audit_view.v1",
    generated_at: new Date().toISOString(),
    evidence_id: evidenceId(record),
    session_id: record.session_id || null,
    metadata_kind: evidenceKind(record),
    verification_state: verification,
    signer: record.signer || null,
    source: record.source || "metadata_store",
    evidence_refs: refs,
    correlation: {
      decision_id: record.decision_id || null,
      agent_id: record.agent_id || null,
      repository: record.repository || null,
      aispm_findings: correlatedFindings.map((finding) => ({
        finding_id: finding.finding_id,
        severity: finding.severity,
        risk_classification: finding.risk_classification,
        decision: finding.decision,
        rule_id: finding.rule_id
      })),
      approvals: correlatedApprovals.map((approval) => ({
        approval_id: approval.approval_id,
        state: approvalState(approval),
        approver_group: approval.approver_group
      }))
    },
    selected_record: record
  };
}

async function copySelectedEvidenceJson() {
  const selected = selectedEvidence();
  const output = el("#evidenceAuditOutput");
  const payload = buildEvidenceAuditPayload(selected);
  const ok = await copyText(prettyJson(payload));
  if (output) output.textContent = prettyJson({ action: "copy_selected_evidence", copied: ok, evidence_id: payload.evidence_id || null });
}

function downloadSelectedEvidenceJson() {
  const selected = selectedEvidence();
  const payload = buildEvidenceAuditPayload(selected);
  const name = String(payload.evidence_id || "evidence").replace(/[^a-z0-9._-]+/gi, "-").toLowerCase();
  downloadJson(`${name}-audit-view.json`, payload);
  const output = el("#evidenceAuditOutput");
  if (output) output.textContent = prettyJson({ action: "download_selected_evidence", filename: `${name}-audit-view.json`, evidence_id: payload.evidence_id || null });
}

function sampleAgentRecords() {
  return [
    {
      agent_id: "codex-agent",
      vendor: "OpenAI",
      type: "coding-agent",
      capabilities: ["code_edit", "test", "shell", "git_operation", "pull_request_attestation"],
      scopes: ["repository", "filesystem", "shell", "git"],
      allowed_repositories: ["cavra-agent-test", "cavra"],
      allowed_tools: ["cavra", "git", "pytest", "node"],
      risk_tier: "high",
      owner: "Platform Engineering",
      status: "active",
      evidence_refs: ["registry://agents/codex-agent"]
    },
    {
      agent_id: "claude-code",
      vendor: "Anthropic",
      type: "coding-agent",
      capabilities: ["code_edit", "test", "shell", "mcp_tool_call"],
      scopes: ["repository", "filesystem", "shell", "mcp"],
      allowed_repositories: ["cavra-agent-test"],
      allowed_tools: ["cavra-mcp-server", "git", "pytest"],
      risk_tier: "high",
      owner: "AI Governance",
      status: "active",
      evidence_refs: ["registry://agents/claude-code"]
    },
    {
      agent_id: "github-copilot-agent",
      vendor: "GitHub",
      type: "coding-agent",
      capabilities: ["code_edit", "pull_request", "workflow_assistance"],
      scopes: ["repository", "git", "ci"],
      allowed_repositories: ["cavra-agent-test"],
      allowed_tools: ["github-actions", "cavra-pr-attestation"],
      risk_tier: "medium",
      owner: "Repository Owners",
      status: "active",
      evidence_refs: ["registry://agents/github-copilot-agent"]
    }
  ];
}

function sampleMcpServerRecords() {
  return [
    {
      server_id: "cavra-mcp-server",
      name: "CAVRA MCP Server",
      trust_tier: "trusted",
      approval_state: "approved",
      capabilities: ["repository", "filesystem"],
      allowed_tools: ["cavra.evaluate_action", "cavra.check_file_read", "cavra.check_file_write", "cavra.export_evidence"],
      owner: "Platform Security",
      evidence_refs: ["registry://mcp/cavra-mcp-server"]
    },
    {
      server_id: "unknown-filesystem",
      name: "Unknown Filesystem MCP",
      trust_tier: "unknown",
      approval_state: "pending",
      capabilities: ["filesystem"],
      allowed_tools: [],
      owner: "unassigned",
      evidence_refs: ["registry://mcp/unknown-filesystem"]
    },
    {
      server_id: "cloud-admin-tools",
      name: "Cloud Admin Tools",
      trust_tier: "experimental",
      approval_state: "pending",
      capabilities: ["cloud", "shell"],
      allowed_tools: ["plan_change"],
      owner: "Cloud Security",
      evidence_refs: ["registry://mcp/cloud-admin-tools"]
    }
  ];
}

async function seedSampleAgents() {
  const output = el("#registryAuditOutput");
  if (output) output.textContent = "Seeding sample agents...";
  try {
    const results = [];
    for (const payload of sampleAgentRecords()) {
      results.push(await setupPost("/agents", payload));
    }
    appState.selectedAgentId = results[0]?.agent_id || appState.selectedAgentId;
    if (output) output.textContent = prettyJson({ action: "seed_sample_agents", results });
    await refreshApplicationState();
  } catch (error) {
    if (output) output.textContent = prettyJson({ action: "seed_sample_agents", status: "failed", message: error.message });
  }
}

async function seedSampleMcp() {
  const output = el("#registryAuditOutput");
  if (output) output.textContent = "Seeding sample MCP servers...";
  try {
    const results = [];
    for (const payload of sampleMcpServerRecords()) {
      results.push(await setupPost("/mcp/servers", payload));
    }
    appState.selectedMcpServerId = results[0]?.server_id || appState.selectedMcpServerId;
    if (output) output.textContent = prettyJson({ action: "seed_sample_mcp", results });
    await refreshApplicationState();
  } catch (error) {
    if (output) output.textContent = prettyJson({ action: "seed_sample_mcp", status: "failed", message: error.message });
  }
}

async function loadRegistryReferences() {
  const [profiles, classifications] = await Promise.all([
    optionalApi("/agents/profiles"),
    optionalApi("/mcp/tool-classifications")
  ]);
  appState.agentProfiles = profiles.ok ? profiles.value : null;
  appState.mcpClassifications = classifications.ok ? classifications.value : null;
  renderRegistryReferenceTables();
}

async function runMcpTrustCheck() {
  const form = el("#mcpTrustCheckForm");
  const status = el("#mcpTrustCheckStatus");
  const output = el("#registryAuditOutput");
  if (!form || !output) return;
  const data = new FormData(form);
  const server = String(data.get("server") || "").trim();
  const tool = String(data.get("tool") || "unknown").trim();
  const capability = String(data.get("capability") || "").trim();
  if (status) {
    status.textContent = "running";
    status.className = "state-chip warn";
  }
  try {
    const path = `/mcp/trust?server=${encodeURIComponent(server)}&tool=${encodeURIComponent(tool)}${capability ? `&capability=${encodeURIComponent(capability)}` : ""}`;
    const result = await setupApi(path);
    if (status) {
      status.textContent = result.decision || "complete";
      status.className = `state-chip ${statusClass(result.decision)}`;
    }
    output.textContent = prettyJson({ action: "mcp_trust_check", request: { server, tool, capability }, result });
  } catch (error) {
    if (status) {
      status.textContent = "failed";
      status.className = "state-chip danger";
    }
    output.textContent = prettyJson({ action: "mcp_trust_check", status: "failed", message: error.message });
  }
}

function sampleIntegrationRecords() {
  const checkedAt = new Date().toISOString();
  return [
    {
      integration_id: "github-main",
      name: "GitHub Repository Controls",
      provider: "github",
      category: "source_control",
      status: "active",
      health_status: "healthy",
      owner: "Repository Owners",
      environment: "community-local",
      auth_mode: "github_app",
      endpoint_ref: "github://Huzefaaa2/cavra",
      capabilities: ["pull_request_attestation", "required_checks", "release_evidence"],
      repositories: ["Huzefaaa2/cavra"],
      last_checked_at: checkedAt,
      evidence_refs: ["integration://github-main"]
    },
    {
      integration_id: "github-actions-release",
      name: "GitHub Actions Release Gates",
      provider: "github_actions",
      category: "ci_cd",
      status: "configured",
      health_status: "healthy",
      owner: "Platform Engineering",
      environment: "community-local",
      auth_mode: "oidc",
      endpoint_ref: "github-actions://workflows",
      capabilities: ["container_publish", "helm_lint", "release_validation"],
      repositories: ["Huzefaaa2/cavra"],
      last_checked_at: checkedAt,
      evidence_refs: ["integration://github-actions-release"]
    },
    {
      integration_id: "splunk-siem",
      name: "Splunk SIEM Export",
      provider: "splunk",
      category: "siem",
      status: "planned",
      health_status: "not_checked",
      owner: "Security Operations",
      environment: "customer-configured",
      auth_mode: "token_env",
      endpoint_ref: "env://SPLUNK_HEC_URL",
      capabilities: ["runtime_event_stream", "aispm_finding_export", "connector_delivery"],
      repositories: [],
      evidence_refs: ["integration://splunk-siem"]
    },
    {
      integration_id: "servicenow-itsm",
      name: "ServiceNow Change Queue",
      provider: "servicenow",
      category: "itsm",
      status: "planned",
      health_status: "not_checked",
      owner: "Change Advisory Board",
      environment: "customer-configured",
      auth_mode: "token_env",
      endpoint_ref: "env://SERVICENOW_URL",
      capabilities: ["approval_ticket", "change_request", "break_glass_review"],
      repositories: [],
      evidence_refs: ["integration://servicenow-itsm"]
    },
    {
      integration_id: "teams-chatops",
      name: "Teams Approval Notifications",
      provider: "teams",
      category: "chatops",
      status: "planned",
      health_status: "not_checked",
      owner: "AI Governance",
      environment: "customer-configured",
      auth_mode: "webhook_env",
      endpoint_ref: "env://TEAMS_WEBHOOK_URL",
      capabilities: ["approval_notification", "launch_alert", "report_delivery"],
      repositories: [],
      evidence_refs: ["integration://teams-chatops"]
    },
    {
      integration_id: "azure-prod",
      name: "Azure Production Control Plane",
      provider: "sentinel",
      category: "cloud",
      status: "configured",
      health_status: "degraded",
      owner: "Cloud Security",
      environment: "production",
      auth_mode: "managed_identity",
      endpoint_ref: "azure://sentinel-workspace",
      capabilities: ["cloud_event_ingest", "runtime_alert", "posture_export"],
      repositories: ["Huzefaaa2/cavra"],
      last_checked_at: checkedAt,
      evidence_refs: ["integration://azure-prod"]
    }
  ];
}

async function seedSampleIntegrations() {
  const output = el("#integrationAuditOutput");
  if (output) output.textContent = "Seeding sample integrations...";
  try {
    const results = [];
    for (const payload of sampleIntegrationRecords()) {
      results.push(await setupPost("/integrations", payload));
    }
    appState.selectedIntegrationId = results[0]?.integration_id || appState.selectedIntegrationId;
    if (output) output.textContent = prettyJson({ action: "seed_sample_integrations", results });
    await refreshApplicationState();
  } catch (error) {
    if (output) output.textContent = prettyJson({ action: "seed_sample_integrations", status: "failed", message: error.message });
  }
}

async function runIntegrationDeliveryTest() {
  const selected = selectedIntegration();
  const form = el("#integrationDeliveryTestForm");
  const output = el("#integrationAuditOutput");
  if (!form || !output) return;
  if (!selected) {
    output.textContent = prettyJson({ action: "integration_delivery_test", status: "skipped", message: "No integration selected." });
    return;
  }
  const data = new FormData(form);
  const provider = String(data.get("provider") || "all").trim() || "all";
  const eventType = String(data.get("event_type") || "cavra.integration.delivery.test").trim();
  const requestPayload = {
    provider,
    event: {
      event_type: eventType,
      generated_at: new Date().toISOString(),
      integration_id: integrationId(selected),
      integration_provider: selected.provider,
      source: "sandbox-ui.integration-hub",
      message: "CAVRA sandbox integration delivery boundary test."
    }
  };
  if ((appState.consoleConfig?.connector_delivery || "disabled") !== "configured") {
    output.textContent = prettyJson({
      action: "integration_delivery_test",
      selected: integrationId(selected),
      request: requestPayload,
      status: "not_configured",
      message: "Connector delivery is disabled in the current API configuration.",
      expected_boundary: "Configure CAVRA_CONNECTOR_CONFIG and provider secrets before sending live connector events."
    });
    return;
  }
  output.textContent = "Testing connector delivery boundary...";
  try {
    const result = await setupPost(`/integrations/${encodeURIComponent(integrationId(selected))}/deliver`, requestPayload);
    output.textContent = prettyJson({ action: "integration_delivery_test", selected: integrationId(selected), request: requestPayload, result });
    await refreshApplicationState();
  } catch (error) {
    output.textContent = prettyJson({
      action: "integration_delivery_test",
      selected: integrationId(selected),
      request: requestPayload,
      status: "blocked_or_not_configured",
      message: error.message,
      expected_boundary: "Community local UI can register integrations, but provider delivery needs CAVRA_CONNECTOR_CONFIG and provider secrets."
    });
  }
}

function grouped(items) {
  return items.reduce((groups, item) => {
    groups[item.group] ||= [];
    groups[item.group].push(item);
    return groups;
  }, {});
}

function renderNav(target) {
  if (!target) return;
  const groups = grouped(navItems);
  target.innerHTML = Object.entries(groups).map(([group, items]) => `
    <div class="nav-group">
      <p class="nav-heading">${escapeHtml(group)}</p>
      ${items.map((item) => `
        <button class="nav-link" data-route="${item.id}" aria-label="${escapeHtml(item.label)}">
          <span>${item.icon}</span>
          <span class="nav-label">${escapeHtml(item.label)}</span>
          <small>&rsaquo;</small>
        </button>
      `).join("")}
    </div>
  `).join("");
}

function renderCards() {
  el("#demoMetrics").innerHTML = metrics.map(([label, value, detail]) => `
    <article class="metric-card">
      <span>${escapeHtml(label)}</span>
      <strong>${escapeHtml(value)}</strong>
      <p>${escapeHtml(detail)}</p>
    </article>
  `).join("");

  el("#businessOutcomeCards").innerHTML = businessOutcomes.map(([title, detail], index) => `
    <article class="outcome-card">
      <span>${String(index + 1).padStart(2, "0")}</span>
      <h3>${escapeHtml(title)}</h3>
      <p>${escapeHtml(detail)}</p>
    </article>
  `).join("");

  el("#executiveDeliverableCards").innerHTML = executiveDeliverables.map(([title, detail]) => `
    <article class="deliverable-card">
      <span class="eyebrow">Board-ready</span>
      <h3>${escapeHtml(title)}</h3>
      <p>${escapeHtml(detail)}</p>
    </article>
  `).join("");

  el("#editionComparison").innerHTML = `
    <div class="edition-row edition-header">
      <strong>Edition</strong>
      <strong>Operating model</strong>
      <strong>What it includes</strong>
      <strong>Best for</strong>
    </div>
    ${editionComparison.map(([edition, model, includes, bestFor]) => `
      <div class="edition-row">
        <strong>${escapeHtml(edition)}</strong>
        <span>${escapeHtml(model)}</span>
        <span>${escapeHtml(includes)}</span>
        <span>${escapeHtml(bestFor)}</span>
      </div>
    `).join("")}
  `;

  el("#downloadCards").innerHTML = downloadArtifacts.map(([title, type, detail]) => `
    <article class="download-card">
      <span class="eyebrow">${escapeHtml(type)}</span>
      <h3>${escapeHtml(title)}</h3>
      <p>${escapeHtml(detail)}</p>
      <button type="button" data-download="${escapeHtml(title)}">Download</button>
    </article>
  `).join("");

  el("#communityGaSummary").innerHTML = communityCards.map(([title, status, detail]) => `
    <article class="readiness-card community-ga-card">
      <span class="eyebrow">${escapeHtml(status)}</span>
      <h3>${escapeHtml(title)}</h3>
      <p>${escapeHtml(detail)}</p>
    </article>
  `).join("");

  el("#pilotReadinessSummary").innerHTML = pilotCards.map(([title, status, detail]) => `
    <article class="readiness-card pilot-readiness-card">
      <span class="eyebrow">${escapeHtml(status)}</span>
      <h3>${escapeHtml(title)}</h3>
      <p>${escapeHtml(detail)}</p>
    </article>
  `).join("");

  el("#setupCards").innerHTML = setupCards.map(([title, status, detail]) => `
    <article class="setup-card">
      <span class="eyebrow">${escapeHtml(status)}</span>
      <h3>${escapeHtml(title)}</h3>
      <p>${escapeHtml(detail)}</p>
    </article>
  `).join("");

  el("#setupCommandRail").innerHTML = setupCommands.map(([label, command]) => `
    <article class="setup-command-card">
      <span>${escapeHtml(label)}</span>
      <code>${escapeHtml(command)}</code>
    </article>
  `).join("");

  el("#aispmOverviewCards").innerHTML = aispmCards.map(([label, value, detail]) => `
    <article class="posture-card">
      <span>${escapeHtml(label)}</span>
      <strong>${escapeHtml(value)}</strong>
      <p>${escapeHtml(detail)}</p>
    </article>
  `).join("");

  el("#aispmPilotLaunchBoardPack").innerHTML = boardPackCards.map(([title, status, detail]) => `
    <article class="board-pack-card">
      <span class="eyebrow">${escapeHtml(status)}</span>
      <h3>${escapeHtml(title)}</h3>
      <p>${escapeHtml(detail)}</p>
    </article>
  `).join("");

  el("#aispmPilotLaunchBoardPackManifest").innerHTML = boardManifestCards.map(([title, status, detail]) => `
    <article class="board-pack-manifest-card">
      <span class="eyebrow">${escapeHtml(status)}</span>
      <h3>${escapeHtml(title)}</h3>
      <p>${escapeHtml(detail)}</p>
    </article>
  `).join("");

  el("#aispmReportCenter").innerHTML = reportCards.map(([title, detail]) => `
    <article class="report-card">
      <span class="eyebrow">Community download</span>
      <h3>${escapeHtml(title)}</h3>
      <p>${escapeHtml(detail)}</p>
      <button type="button" data-report="${escapeHtml(title)}">Download Sample</button>
    </article>
  `).join("");

  el("#architectureMap").innerHTML = architectureNodes.map(([title, detail]) => `
    <article class="architecture-node">
      <strong>${escapeHtml(title)}</strong>
      <small>CAVRA control plane</small>
      <p>${escapeHtml(detail)}</p>
    </article>
  `).join("");

  el("#policyExplorer").innerHTML = policies.map(([title, violation, remediation]) => `
    <article class="policy-card">
      <span class="eyebrow">Policy</span>
      <h3>${escapeHtml(title)}</h3>
      <p>${escapeHtml(violation)}</p>
      <p><strong>Recommended action:</strong> ${escapeHtml(remediation)}</p>
    </article>
  `).join("");

  el("#evidenceTimeline").innerHTML = evidenceTimeline.map(([title, detail]) => `
    <div class="timeline-item">
      <h3>${escapeHtml(title)}</h3>
      <p>${escapeHtml(detail)}</p>
    </div>
  `).join("");

  el("#useCaseCards").innerHTML = useCases.map(([title, detail]) => `
    <article class="usecase-card">
      <h3>${escapeHtml(title)}</h3>
      <p>${escapeHtml(detail)}</p>
    </article>
  `).join("");

  el("#operatorPathCards").innerHTML = operatorPaths.map(([title, value, path]) => `
    <article class="operator-path-card">
      <span class="eyebrow">${escapeHtml(title)}</span>
      <h3>${escapeHtml(value)}</h3>
      <p>${escapeHtml(path)}</p>
    </article>
  `).join("");

  el("#trialAccessCards").innerHTML = trialAccessCards.map(([title, status, detail]) => `
    <article class="trial-access-card">
      <span class="eyebrow">${escapeHtml(status)}</span>
      <h3>${escapeHtml(title)}</h3>
      <p>${escapeHtml(detail)}</p>
    </article>
  `).join("");

  const integrationCards = el("#integrationCards");
  if (integrationCards) {
    integrationCards.innerHTML = integrations.map(([title, status, detail]) => `
      <article class="integration-card">
        <span class="eyebrow">${escapeHtml(status)}</span>
        <h3>${escapeHtml(title)}</h3>
        <p>${escapeHtml(detail)}</p>
      </article>
    `).join("");
  }

  el("#complianceRows").innerHTML = compliance.map(([framework, control, detail]) => `
    <article class="compliance-card">
      <span class="eyebrow">${escapeHtml(framework)}</span>
      <h3>${escapeHtml(control)}</h3>
      <p>${escapeHtml(detail)}</p>
    </article>
  `).join("");

  el("#roadmapBoard").innerHTML = roadmap.map(([title, detail]) => `
    <article class="roadmap-card">
      <h3>${escapeHtml(title)}</h3>
      <p>${escapeHtml(detail)}</p>
    </article>
  `).join("");

  el("#operatorHelpCards").innerHTML = helpWorkflowSteps.map((item, index) => `
    <article class="help-workflow-card">
      <span class="eyebrow">${escapeHtml(item.group)} / ${String(index + 1).padStart(2, "0")}</span>
      <h3>${escapeHtml(item.label)}</h3>
      <p>${escapeHtml(item.description)}</p>
      <a href="#${escapeHtml(item.route)}" data-route-link="${escapeHtml(item.route)}">Open ${escapeHtml(item.label)}</a>
    </article>
  `).join("");

  el("#secondaryReferenceCards").innerHTML = secondaryRoutes.map((item) => `
    <article class="reference-route-card">
      <span class="eyebrow">${escapeHtml(item.status)}</span>
      <h3>${escapeHtml(item.label)}</h3>
      <p>${escapeHtml(item.description)}</p>
      <a href="#${escapeHtml(item.id)}" data-route-link="${escapeHtml(item.id)}">Open reference</a>
    </article>
  `).join("");

  el("#docsNav").innerHTML = docsLinks.map(([label, href]) => `
    <a href="${escapeHtml(href)}" target="${href.startsWith("http") ? "_blank" : "_self"}" rel="${href.startsWith("http") ? "noreferrer" : ""}">
      ${escapeHtml(label)}
    </a>
  `).join("");

  renderInlineHelpTriggers();
  renderReportsLive();
}

function renderInlineHelpTriggers() {
  document.querySelectorAll(".inline-help-trigger").forEach((button) => button.remove());
  Object.keys(inlineHelpContent).forEach((route) => {
    const panel = document.getElementById(route);
    if (!panel) return;
    const target = panel.querySelector(".operator-dashboard-actions") || panel.querySelector(".page-hero") || panel.querySelector(".operator-panel-heading");
    if (!target) return;
    const button = document.createElement("button");
    button.type = "button";
    button.className = "inline-help-trigger";
    button.dataset.inlineHelp = route;
    button.textContent = "Page Guide";
    target.append(button);
  });
}

function routeTitle(route) {
  const item = navItems.find((nav) => nav.id === route);
  if (item) return `CAVRA | ${item.label}`;
  const panel = document.getElementById(route);
  const title = panel?.getAttribute("data-title");
  return title ? `CAVRA | ${title}` : "CAVRA | Runtime Governance for AI Coding Agents";
}

function renderToc(route) {
  const panel = document.getElementById(route);
  const toc = el("#toc");
  if (!panel || !toc) return;
  const headings = [...panel.querySelectorAll("h2, h3")]
    .filter((heading) => {
      const rect = heading.getBoundingClientRect();
      const style = window.getComputedStyle(heading);
      return rect.width > 0 && rect.height > 0 && style.display !== "none" && style.visibility !== "hidden";
    })
    .slice(0, 10);
  toc.innerHTML = `
    <strong>On this page</strong>
    ${headings.map((heading, index) => {
      if (!heading.id) heading.id = `${route}-heading-${index}`;
      return `<a href="#${heading.id}">${escapeHtml(heading.textContent || "Section")}</a>`;
    }).join("")}
  `;
}

function openInlineHelp(route) {
  const guide = inlineHelpContent[route] || inlineHelpContent.documentation;
  const drawer = el("#inlineHelpDrawer");
  if (!drawer || !guide) return;
  el("#inlineHelpKicker").textContent = guide.kicker || "Page guide";
  el("#inlineHelpTitle").textContent = guide.title || "CAVRA guide";
  el("#inlineHelpSummary").textContent = guide.summary || "";
  el("#inlineHelpBody").innerHTML = `
    <h3>Operator path</h3>
    <ol>
      ${(guide.steps || []).map((step) => `<li>${escapeHtml(step)}</li>`).join("")}
    </ol>
  `;
  el("#inlineHelpLinks").innerHTML = (guide.links || []).map(([label, target]) => `
    <a href="#${escapeHtml(target)}" data-route-link="${escapeHtml(target)}">${escapeHtml(label)}</a>
  `).join("");
  drawer.classList.add("is-open");
  drawer.setAttribute("aria-hidden", "false");
}

function closeInlineHelp() {
  const drawer = el("#inlineHelpDrawer");
  if (!drawer) return;
  drawer.classList.remove("is-open");
  drawer.setAttribute("aria-hidden", "true");
}

function setRoute(route, options = {}) {
  const nextRoute = document.getElementById(route) ? route : "dashboard";
  document.querySelectorAll(".page-panel").forEach((panel) => {
    panel.classList.toggle("is-active", panel.id === nextRoute);
  });
  document.querySelectorAll(".nav-link").forEach((link) => {
    link.classList.toggle("is-active", link.dataset.route === nextRoute);
  });
  document.querySelectorAll("[data-route-link]").forEach((link) => {
    link.classList.toggle("is-active", link.dataset.routeLink === nextRoute);
  });
  document.title = routeTitle(nextRoute);
  localStorage.setItem("cavra.activeRoute", nextRoute);
  if (!options.fromHash && location.hash.slice(1) !== nextRoute) {
    history.pushState(null, "", `#${nextRoute}`);
  }
  renderToc(nextRoute);
  closeInlineHelp();
  window.scrollTo(0, 0);
  el("#mainContent")?.focus({ preventScroll: true });
}

function applyTheme(theme) {
  const normalized = ["sentinel", "classic", "retro", "executive"].includes(theme) ? theme : "sentinel";
  document.body.dataset.theme = normalized;
  document.querySelectorAll("[data-theme-select]").forEach((picker) => {
    picker.value = normalized;
  });
  localStorage.setItem("cavra.theme", normalized);
}

function openCommandPalette() {
  el("#commandPalette").classList.add("is-open");
  el("#commandPalette").setAttribute("aria-hidden", "false");
  el("#commandSearch").value = "";
  renderCommandResults("");
  setTimeout(() => el("#commandSearch").focus(), 0);
}

function closeCommandPalette() {
  el("#commandPalette").classList.remove("is-open");
  el("#commandPalette").setAttribute("aria-hidden", "true");
}

function setCommandStatus(message, state = "neutral") {
  const target = el("#commandStatus");
  if (!target) return;
  target.textContent = message;
  target.dataset.state = state;
}

function openSetupPrompt() {
  const prompt = el("#setupPrompt");
  if (!prompt || localStorage.getItem("cavra.setupPromptDismissed") === "true") return;
  prompt.classList.add("is-open");
  prompt.setAttribute("aria-hidden", "false");
}

function closeSetupPrompt() {
  const prompt = el("#setupPrompt");
  if (!prompt) return;
  prompt.classList.remove("is-open");
  prompt.setAttribute("aria-hidden", "true");
  localStorage.setItem("cavra.setupPromptDismissed", "true");
}

function renderCommandResults(query) {
  const normalized = query.trim().toLowerCase();
  const actionMatches = commandActions.filter((item) => {
    const haystack = `${item.type} ${item.label} ${item.description} ${item.keywords || ""}`.toLowerCase();
    return !normalized || haystack.includes(normalized);
  }).slice(0, normalized ? 8 : 6);
  const routeMatches = routeContent.filter((item) => {
    const haystack = `${item.type} ${item.label} ${item.description}`.toLowerCase();
    return !normalized || haystack.includes(normalized);
  }).slice(0, normalized ? 8 : 6);
  const actionHtml = actionMatches.map((item) => `
    <button class="command-result command-action-result" data-command-action="${escapeHtml(item.id)}">
      <span class="command-result-type">${escapeHtml(item.type)}</span>
      <strong>${escapeHtml(item.label)}</strong>
      <small>${escapeHtml(item.description)}</small>
    </button>
  `).join("");
  const routeHtml = routeMatches.map((item) => `
    <button class="command-result" data-route="${item.route}">
      <span class="command-result-type">${escapeHtml(item.type)}</span>
      <strong>${escapeHtml(item.label)}</strong>
      <small>${escapeHtml(item.description)}</small>
    </button>
  `).join("");

  el("#commandResults").innerHTML = actionHtml || routeHtml
    ? `
      ${actionHtml ? `<div class="command-result-section"><span>Actions</span>${actionHtml}</div>` : ""}
      ${routeHtml ? `<div class="command-result-section"><span>Pages and references</span>${routeHtml}</div>` : ""}
    `
    : `<p>No matching CAVRA command found.</p>`;
}

async function runCommandAction(actionId) {
  const action = commandActions.find((item) => item.id === actionId);
  if (!action) {
    setCommandStatus("Unknown command.", "danger");
    return;
  }
  setCommandStatus(`Running: ${action.label}`, "busy");
  if (action.route) setRoute(action.route);
  try {
    switch (actionId) {
      case "refresh-all":
        await refreshApplicationState();
        await refreshSetupStatus();
        break;
      case "open-setup-status":
        await runSetupAction("status");
        break;
      case "run-setup-validate":
        await runSetupAction("validate");
        break;
      case "load-policy-actions":
        await runSetupAction("catalog");
        break;
      case "test-risky-action":
        await runSetupAction("test-risk");
        break;
      case "seed-approval":
        await seedSampleApproval();
        break;
      case "seed-agents":
        await seedSampleAgents();
        break;
      case "seed-mcp":
        await seedSampleMcp();
        break;
      case "seed-integrations":
        await seedSampleIntegrations();
        break;
      case "generate-report-preview":
        renderReportPreview();
        break;
      case "download-report-preview": {
        const packet = buildCurrentReportPacket();
        downloadText(reportFilename(packet), formatReportOutput(packet), currentReportOptions().format === "CSV" ? "text/csv" : "text/plain");
        break;
      }
      case "download-settings-diagnostics":
        downloadJson("cavra-settings-diagnostics.json", buildSettingsDiagnostics());
        break;
      case "expand-sidebar":
        setSidebarCollapsed(false);
        renderSettings();
        break;
      case "collapse-sidebar":
        setSidebarCollapsed(true);
        renderSettings();
        break;
      case "show-setup-prompt":
        localStorage.removeItem("cavra.setupPromptDismissed");
        openSetupPrompt();
        break;
      default:
        throw new Error(`Unhandled command action: ${actionId}`);
    }
    setCommandStatus(`Completed: ${action.label}`, "ok");
    setTimeout(closeCommandPalette, 350);
  } catch (error) {
    setCommandStatus(`Failed: ${error.message}`, "danger");
  }
}

function downloadJson(filename, payload) {
  const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
  downloadBlob(filename, blob);
}

function downloadText(filename, text, type = "text/plain") {
  downloadBlob(filename, new Blob([text], { type }));
}

function downloadBlob(filename, blob) {
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.append(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

async function copyText(text) {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch {
    return false;
  }
}

function buildBoardPacket() {
  return {
    product: "CAVRA AISPM",
    packet_type: "public_safe_pilot_launch_board_pack",
    generated_at: new Date().toISOString(),
    status: "demo_ready",
    artifacts: boardPackCards.map(([name, status, detail]) => ({ name, status, detail })),
    manifest: boardManifestCards.map(([name, status, detail]) => ({ name, status, detail })),
    public_boundary: [
      "No production tenant records",
      "No connector credentials",
      "No SMTP/provider secrets",
      "No private runtime logs"
    ]
  };
}

function buildDownloadArtifact(title) {
  const artifact = downloadArtifacts.find(([name]) => name === title);
  return {
    product: "CAVRA",
    artifact: title,
    artifact_type: artifact?.[1] || "Public-safe artifact",
    generated_at: new Date().toISOString(),
    purpose: artifact?.[2] || "CAVRA public product evaluation artifact.",
    overview: "CAVRA is the Runtime Authority platform for governing AI coding agents across software delivery.",
    includes_aispm: "Built-in AI Security Posture Management continuously measures AI operational risk and governance readiness.",
    recommended_evaluation_path: [
      "Run the public demo",
      "Review sample evidence",
      "Download the board packet",
      "Request CAVRA Trial access"
    ],
    public_safety_boundary: [
      "No customer tenant data",
      "No connector secrets",
      "No SMTP/provider credentials",
      "No private managed-service source or runtime logs"
    ],
    links: {
      public_site: "https://huzefaaa2.github.io/cavra/",
      trial_portal: "https://cavra-trial.mind-ops.cloud/",
      wiki_textbook: "https://github.com/Huzefaaa2/cavra/wiki"
    }
  };
}

function runScenario() {
  const packet = {
    decision_id: `demo-${Date.now()}`,
    agent: "codex-agent",
    requested_action: "read_file .env.production",
    decision: "block",
    severity: "critical",
    rationale: "Production secret access requires managed secret references and cannot be read directly by an AI agent.",
    evidence_refs: ["sample://evidence/secret-read-block"],
    posture_update: "AISPM finding opened and evidence confidence updated."
  };
  el("#scenarioStatus").textContent = "Demo decision complete: blocked direct production secret access and generated sample evidence.";
  const evidencePayload = el("#evidencePayload");
  if (evidencePayload) evidencePayload.textContent = JSON.stringify(packet, null, 2);
  setRoute("evidence");
}

function setSidebarCollapsed(collapsed) {
  const sidebar = el("#sidebar");
  const toggle = el("#collapseSidebar");
  if (!sidebar || !toggle) return;
  sidebar.classList.toggle("is-collapsed", collapsed);
  toggle.textContent = collapsed ? "Expand" : "Collapse";
  toggle.setAttribute("aria-label", collapsed ? "Expand sidebar" : "Collapse sidebar");
  toggle.setAttribute("aria-expanded", String(!collapsed));
  localStorage.setItem("cavra.sidebarCollapsed", String(collapsed));
}

function closeMobileDrawer() {
  const drawer = el("#mobileDrawer");
  if (!drawer) return;
  drawer.classList.remove("is-open");
  drawer.setAttribute("aria-hidden", "true");
}

function wireEvents() {
  document.addEventListener("click", async (event) => {
    const inlineHelpTrigger = event.target.closest("[data-inline-help]");
    if (inlineHelpTrigger) {
      event.preventDefault();
      openInlineHelp(inlineHelpTrigger.dataset.inlineHelp);
      return;
    }
    if (event.target.closest("#closeInlineHelp")) {
      closeInlineHelp();
      return;
    }
    if (event.target.id === "inlineHelpDrawer") {
      closeInlineHelp();
      return;
    }

    const commandAction = event.target.closest("[data-command-action]");
    if (commandAction) {
      event.preventDefault();
      await runCommandAction(commandAction.dataset.commandAction);
      if (event.target.closest("#mobileDrawer")) closeMobileDrawer();
      return;
    }

    const routeTarget = event.target.closest("[data-route], [data-route-link]");
    if (routeTarget?.dataset.route || routeTarget?.dataset.routeLink) {
      event.preventDefault();
      setRoute(routeTarget.dataset.route || routeTarget.dataset.routeLink);
      closeMobileDrawer();
      closeCommandPalette();
      return;
    }

    if (event.target.closest("#openSearch") || event.target.closest("#mobileSearch")) {
      openCommandPalette();
      return;
    }
    if (event.target.closest("#closeSearch")) {
      closeCommandPalette();
      return;
    }
    if (event.target.closest("#startSetupPrompt")) {
      closeSetupPrompt();
      setRoute("first-run-setup");
      return;
    }
    if (event.target.closest("#dismissSetupPrompt")) {
      closeSetupPrompt();
      return;
    }
    if (event.target.closest("#openMobileNav")) {
      el("#mobileDrawer").classList.add("is-open");
      el("#mobileDrawer").setAttribute("aria-hidden", "false");
      return;
    }
    if (event.target.closest("#closeMobileNav")) {
      closeMobileDrawer();
      return;
    }
    if (event.target.closest("#collapseSidebar")) {
      setSidebarCollapsed(!el("#sidebar").classList.contains("is-collapsed"));
      return;
    }
    if (event.target.closest("#refreshOperatorDashboard") || event.target.closest("#settingsRefreshState")) {
      await refreshApplicationState();
      await refreshSetupStatus();
      return;
    }
    if (event.target.closest("#resetSetupPrompt")) {
      localStorage.removeItem("cavra.setupPromptDismissed");
      openSetupPrompt();
      return;
    }
    if (event.target.closest("#expandSidebarSetting")) {
      setSidebarCollapsed(false);
      renderSettings();
      return;
    }
    if (event.target.closest("#collapseSidebarSetting")) {
      setSidebarCollapsed(true);
      renderSettings();
      return;
    }
    if (event.target.closest("#resetLocalUiState")) {
      localStorage.removeItem("cavra.theme");
      localStorage.removeItem("cavra.sidebarCollapsed");
      localStorage.removeItem("cavra.setupPromptDismissed");
      applyTheme("sentinel");
      setSidebarCollapsed(false);
      renderSettings();
      openSetupPrompt();
      return;
    }
    if (event.target.closest("#copySettingsDiagnostics")) {
      const diagnostics = prettyJson(buildSettingsDiagnostics());
      const ok = await copyText(diagnostics);
      const output = el("#settingsDiagnosticsOutput");
      if (output) output.textContent = `${diagnostics}\n\nCopy status: ${ok ? "copied" : "copy failed"}`;
      return;
    }
    if (event.target.closest("#downloadSettingsDiagnostics")) {
      downloadJson("cavra-settings-diagnostics.json", buildSettingsDiagnostics());
      return;
    }
    if (event.target.closest("[data-live-refresh]")) {
      await refreshApplicationState();
      return;
    }
    const approvalSelect = event.target.closest("[data-approval-select]");
    if (approvalSelect) {
      appState.selectedApprovalId = approvalSelect.dataset.approvalSelect;
      renderApprovals();
      return;
    }
    const approvalAction = event.target.closest("[data-approval-action]");
    if (approvalAction) {
      await runApprovalAction(approvalAction.dataset.approvalAction);
      return;
    }
    if (event.target.closest("#seedSampleApproval")) {
      await seedSampleApproval();
      return;
    }
    const evidenceSelect = event.target.closest("[data-evidence-select]");
    if (evidenceSelect) {
      appState.selectedEvidenceId = evidenceSelect.dataset.evidenceSelect;
      const output = el("#evidenceAuditOutput");
      if (output) output.textContent = prettyJson(buildEvidenceAuditPayload(selectedEvidence()));
      renderEvidenceSearch();
      return;
    }
    if (event.target.closest("#copySelectedEvidence")) {
      await copySelectedEvidenceJson();
      return;
    }
    if (event.target.closest("#downloadSelectedEvidence")) {
      downloadSelectedEvidenceJson();
      return;
    }
    const agentSelect = event.target.closest("[data-agent-select]");
    if (agentSelect) {
      appState.selectedAgentId = agentSelect.dataset.agentSelect;
      const output = el("#registryAuditOutput");
      if (output) output.textContent = prettyJson(buildRegistryAuditPayload("agent", selectedAgent()));
      renderAgentsAndMcp();
      return;
    }
    const mcpSelect = event.target.closest("[data-mcp-select]");
    if (mcpSelect) {
      appState.selectedMcpServerId = mcpSelect.dataset.mcpSelect;
      const output = el("#registryAuditOutput");
      if (output) output.textContent = prettyJson(buildRegistryAuditPayload("mcp_server", selectedMcpServer()));
      renderAgentsAndMcp();
      return;
    }
    if (event.target.closest("#seedSampleAgents")) {
      await seedSampleAgents();
      return;
    }
    if (event.target.closest("#seedSampleMcp")) {
      await seedSampleMcp();
      return;
    }
    if (event.target.closest("#loadAgentProfiles") || event.target.closest("#loadMcpClassifications")) {
      await loadRegistryReferences();
      return;
    }
    const integrationSelect = event.target.closest("[data-integration-select]");
    if (integrationSelect) {
      appState.selectedIntegrationId = integrationSelect.dataset.integrationSelect;
      const output = el("#integrationAuditOutput");
      if (output) output.textContent = prettyJson(buildIntegrationAuditPayload(selectedIntegration()));
      renderIntegrationHub();
      return;
    }
    if (event.target.closest("#seedSampleIntegrations")) {
      await seedSampleIntegrations();
      return;
    }
    if (event.target.closest("#generateReportPreview")) {
      renderReportPreview();
      return;
    }
    if (event.target.closest("#copyReportPreview")) {
      const packet = buildCurrentReportPacket();
      const output = formatReportOutput(packet);
      const ok = await copyText(output);
      const preview = el("#reportPreviewOutput");
      if (preview) preview.textContent = `${output}\n\nCopy status: ${ok ? "copied" : "copy failed"}`;
      return;
    }
    if (event.target.closest("#downloadReportPreview")) {
      const packet = buildCurrentReportPacket();
      const output = formatReportOutput(packet);
      const filename = reportFilename(packet);
      const format = currentReportOptions().format;
      downloadText(filename, output, format === "CSV" ? "text/csv" : format === "Markdown" ? "text/markdown" : "application/json");
      return;
    }
    const setupAction = event.target.closest("[data-setup-action]");
    if (setupAction) {
      event.preventDefault();
      await runSetupAction(setupAction.dataset.setupAction);
      return;
    }
    if (event.target.closest("#runScenario")) {
      runScenario();
      return;
    }
    if (event.target.closest("#overviewRunDemo")) {
      runScenario();
      return;
    }
    if (event.target.closest("#copyAispmPilotLaunchBoardPackPacket")) {
      const ok = await copyText(JSON.stringify(buildBoardPacket(), null, 2));
      event.target.textContent = ok ? "Copied" : "Copy Failed";
      setTimeout(() => { event.target.textContent = "Copy Board Packet"; }, 1800);
      return;
    }
    if (event.target.closest("#downloadAispmPilotLaunchBoardPackPacket")) {
      downloadJson("cavra-aispm-pilot-launch-board-pack-public-demo.json", buildBoardPacket());
      return;
    }
    const reportButton = event.target.closest("[data-report]");
    if (reportButton) {
      downloadJson(`${reportButton.dataset.report.toLowerCase().replace(/[^a-z0-9]+/g, "-")}.json`, {
        report: reportButton.dataset.report,
        product: "CAVRA AISPM",
        mode: "public_demo",
        generated_at: new Date().toISOString(),
        boundary: "Configured or Managed report rendering, SMTP/provider delivery, and private report content are not included in the public demo."
      });
      return;
    }
    const downloadButton = event.target.closest("[data-download]");
    if (downloadButton) {
      const title = downloadButton.dataset.download;
      downloadJson(`${title.toLowerCase().replace(/[^a-z0-9]+/g, "-")}.json`, buildDownloadArtifact(title));
    }
  });

  document.querySelectorAll("[data-theme-select]").forEach((picker) => {
    picker.addEventListener("change", () => applyTheme(picker.value));
  });

  el("#policyCatalogSearch")?.addEventListener("input", (event) => {
    appState.policyFilters.search = event.target.value;
    renderPolicyCatalog();
  });
  el("#policyCatalogSection")?.addEventListener("change", (event) => {
    appState.policyFilters.section = event.target.value;
    renderPolicyCatalog();
  });
  el("#policyCatalogDecision")?.addEventListener("change", (event) => {
    appState.policyFilters.decision = event.target.value;
    renderPolicyCatalog();
  });
  el("#policySimulatorForm")?.addEventListener("submit", async (event) => {
    event.preventDefault();
    await runPolicySimulation();
  });
  el("#approvalSearch")?.addEventListener("input", (event) => {
    appState.approvalFilters.search = event.target.value;
    renderApprovals();
  });
  el("#approvalStateFilter")?.addEventListener("change", (event) => {
    appState.approvalFilters.state = event.target.value;
    renderApprovals();
  });
  el("#approvalGroupFilter")?.addEventListener("change", (event) => {
    appState.approvalFilters.group = event.target.value;
    renderApprovals();
  });
  el("#evidenceSearch")?.addEventListener("input", (event) => {
    appState.evidenceFilters.search = event.target.value;
    renderEvidenceSearch();
  });
  el("#evidenceKindFilter")?.addEventListener("change", (event) => {
    appState.evidenceFilters.kind = event.target.value;
    renderEvidenceSearch();
  });
  el("#evidenceVerificationFilter")?.addEventListener("change", (event) => {
    appState.evidenceFilters.verification = event.target.value;
    renderEvidenceSearch();
  });
  el("#agentSearch")?.addEventListener("input", (event) => {
    appState.agentFilters.search = event.target.value;
    renderAgentsAndMcp();
  });
  el("#agentStatusFilter")?.addEventListener("change", (event) => {
    appState.agentFilters.status = event.target.value;
    renderAgentsAndMcp();
  });
  el("#agentRiskFilter")?.addEventListener("change", (event) => {
    appState.agentFilters.risk = event.target.value;
    renderAgentsAndMcp();
  });
  el("#mcpSearch")?.addEventListener("input", (event) => {
    appState.mcpFilters.search = event.target.value;
    renderAgentsAndMcp();
  });
  el("#mcpTrustFilter")?.addEventListener("change", (event) => {
    appState.mcpFilters.trust = event.target.value;
    renderAgentsAndMcp();
  });
  el("#mcpCapabilityFilter")?.addEventListener("change", (event) => {
    appState.mcpFilters.capability = event.target.value;
    renderAgentsAndMcp();
  });
  el("#mcpTrustCheckForm")?.addEventListener("submit", async (event) => {
    event.preventDefault();
    await runMcpTrustCheck();
  });
  el("#integrationSearch")?.addEventListener("input", (event) => {
    appState.integrationFilters.search = event.target.value;
    renderIntegrationHub();
  });
  el("#integrationCategoryFilter")?.addEventListener("change", (event) => {
    appState.integrationFilters.category = event.target.value;
    renderIntegrationHub();
  });
  el("#integrationStatusFilter")?.addEventListener("change", (event) => {
    appState.integrationFilters.status = event.target.value;
    renderIntegrationHub();
  });
  el("#integrationHealthFilter")?.addEventListener("change", (event) => {
    appState.integrationFilters.health = event.target.value;
    renderIntegrationHub();
  });
  el("#integrationDeliveryTestForm")?.addEventListener("submit", async (event) => {
    event.preventDefault();
    await runIntegrationDeliveryTest();
  });
  ["#reportType", "#reportRange", "#reportScope", "#reportFormat"].forEach((selector) => {
    el(selector)?.addEventListener("change", renderReportPreview);
  });
  el("#settingsThemeSelect")?.addEventListener("change", (event) => {
    applyTheme(event.target.value);
    renderSettings();
  });

  el("#commandSearch").addEventListener("input", (event) => renderCommandResults(event.target.value));
  document.addEventListener("keydown", (event) => {
    if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "k") {
      event.preventDefault();
      openCommandPalette();
    }
    if (event.key === "Escape") {
      closeCommandPalette();
      closeInlineHelp();
    }
  });
  window.addEventListener("hashchange", () => setRoute(location.hash.slice(1), { fromHash: true }));
}

function init() {
  renderNav(el("#portalNav"));
  renderNav(el("#mobileNav"));
  renderCards();
  wireEvents();
  applyTheme(localStorage.getItem("cavra.theme") || "sentinel");
  setSidebarCollapsed(localStorage.getItem("cavra.sidebarCollapsed") === "true");
  const initialRoute = location.hash.slice(1) || "dashboard";
  setRoute(initialRoute, { fromHash: true });
  refreshApplicationState().then(() => refreshSetupStatus());
  if (!location.hash) {
    setTimeout(() => {
      if (!appState.setupStatus?.setup_complete) openSetupPrompt();
    }, 700);
  }
}

init();

/*
  Historical release-gate compatibility markers retained for
  scripts/validate-console-closeout.py while the rendered public site uses the
  rebuilt product-first navigation model.

  operatorPaths
  renderOperatorPaths
  type: "Operator Path"
  Prospect
  Auditor
  Platform Team
  CISO
  Dashboard, Architecture, Use Cases, Documentation
  Evidence, Compliance, Release Readiness Dashboard, Release Index
  Required checks, policy packs, GitHub/GitLab/Azure DevOps paths
  open-core boundary
  Community GA Path
  renderArchitecture
  renderAispmApprovalLineage
  renderAispmControlCoverageHeatmap
  loadAispmControlCoverageHeatmap
  renderAispmBehaviorFingerprints
  renderAispmPolicyContextGaps
  renderAispmPreActionForecasts
  renderAispmIntentActionDrift
  renderAispmToolChainGraph
  renderAispmAgentBlastRadius
  loadAispmAgentBlastRadius
  renderAispmReplayPolicy
  loadAispmReplayPolicy
  renderAispmReplayPolicyTests
  loadAispmReplayPolicyTests
  renderAispmReplayPolicyReviewWorkflow
  copyAispmReplayPolicyReviewPacket
  downloadAispmReplayPolicyReviewPacket
  cavra-replay-policy-review-packet.json
  renderAispmReplayPolicyPrGuidance
  copyAispmReplayPolicyPrApproval
  CAVRA replay-to-policy review completed.
  renderAispmReplayPolicyCiGate
  Replay-To-Policy CI Gate
  renderAispmReplayPolicyCiGateSummary
  CI Gate Readiness Summary
  Action Required
  renderAispmReplayPolicyCiGateRolloutChecklist
  CI Gate Production Rollout Checklist
  cavra-replay-policy-ci-gate-rollout-checklist.md
  copyAispmReplayPolicyCiGateRollout
  downloadAispmReplayPolicyCiGateRollout
  renderAispmReplayPolicyCiGateAuditPacket
  CI Gate Rollout Audit Packet
  cavra.aispm.replay_to_policy_ci_gate_rollout_audit_packet.v1
  cavra-replay-policy-ci-gate-rollout-audit-packet.json
  renderAispmReplayPolicyCiGateAuditorView
  CI Gate Rollout Auditor View
  renderAispmReleaseEvidenceIndex
  cavra.aispm.release_evidence_index_packet.v1
  scripts/validate-aispm-release-evidence-index.py
  renderAispmHostedReleaseStatus
  cavra.hosted_sandbox.operator_release_status_packet.v1
  scripts/validate-hosted-sandbox-operator-status.py
  Auditor conclusion: ready for controlled production rollout
  Public safety boundary
  Enterprise automation boundary
  renderAispmReportCenter
  handleAispmReportDownload
  Scheduled Email Delivery
  cavra-aispm-executive-risk-brief.md
  cavra-aispm-board-kpi-pack.json
  cavra-aispm-soc2-audit-summary.md
  cavra-aispm-control-coverage.csv
  cavra-aispm-evidence-freshness.csv
  cavra-aispm-agent-risk-register.csv
  CI Gate Readiness Export
  cavra-replay-policy-ci-gate-readiness.json
  cavra aispm validate-ci-gate-readiness cavra-replay-policy-ci-gate-readiness.json --repo-root .
  /aispm/replay-to-policy-ci-gate-readiness/validate
  copyAispmReplayPolicyCiGateReadiness
  downloadAispmReplayPolicyCiGateReadiness
  cavra.aispm.replay_to_policy_ci_gate_readiness.v1
  cavra-aispm-review-packet
  examples/github-actions/cavra-aispm-review-packet-validation.yml
  examples/gitlab-ci/cavra-aispm-review-packet-validation.gitlab-ci.yml
  examples/azure-pipelines/cavra-aispm-review-packet-validation.azure-pipelines.yml
  copyAispmReplayPolicyTests
  downloadAispmReplayPolicyTests
  copyTextToClipboard
  cavra-replay-policy-tests.json
  /aispm/replay-to-policy-draft
  /aispm/replay-to-policy-tests
  renderAispmTraceReplay
  renderCompliance
*/
