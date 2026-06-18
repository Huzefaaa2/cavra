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
let currentAispmReports = {};
let currentAispmReportCatalogPacket = null;
let currentAispmReportSetupPacket = null;
let currentAispmReportOperationsPacket = null;
let currentAispmReportGovernancePacket = null;
let currentAispmReportAssurancePacket = null;
let currentAispmReportResponsePacket = null;
let currentAispmReportTrialOpsPacket = null;
let currentAispmTrialReadinessPacket = null;
let currentAispmTrialReadinessMarkdown = "";
let currentAispmTrialReviewPacket = null;
let currentAispmTrialPilotScopePacket = null;
let currentAispmPilotApprovalPacket = null;
let currentAispmPilotLaunchDecisionPacket = null;
let currentAispmPilotEvidenceRoomPacket = null;
let currentAispmEvidenceReviewerChecklistPacket = null;
let currentAispmPilotExceptionRegisterPacket = null;
let currentAispmPilotRiskAcceptancePacket = null;
let currentAispmPilotLaunchBoardPackPacket = null;
let currentAispmPilotControlReadinessPacket = null;
let currentAispmReleaseEvidenceIndexPacket = null;
let currentAispmHostedReleaseStatusPacket = null;

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

const aispmTrialReadinessItems = [
  [
    "Lab Notebook",
    "Ready",
    "Step-by-step Enterprise Trial walkthrough is published in the GitHub Wiki.",
    "https://github.com/Huzefaaa2/cavra/wiki/AISPM-Enterprise-Trial-Lab-Notebook"
  ],
  [
    "Access Portal",
    "Live",
    "Evaluator signup, approval intake, and trial request storage run on the trial domain.",
    "https://cavra-trial.mind-ops.cloud/"
  ],
  [
    "Operator Approval",
    "Controlled",
    "GitHub-owner operator review flow issues public-safe approval output after request review.",
    "https://github.com/Huzefaaa2/cavra/wiki/AISPM-Trial-Access-And-Operator-Approval"
  ],
  [
    "Revocation And Expiry",
    "Documented",
    "Trial closeout covers license expiry, package access removal, and blocked runtime validation.",
    "https://github.com/Huzefaaa2/cavra/wiki/AISPM-Trial-Revocation-Expiry-And-Closeout"
  ],
  [
    "Release Evidence",
    "Verified",
    "Publication readiness summary links the lab notebook to verification evidence.",
    "https://github.com/Huzefaaa2/cavra/blob/main/docs/release-verifications/aispm-trial-lab-notebook-publication-readiness-summary.md"
  ],
  [
    "Enterprise Automation",
    "Locked",
    "Live package access grants, license issuance, email delivery, and hosted telemetry remain Enterprise/private.",
    "https://github.com/Huzefaaa2/cavra/blob/main/docs/architecture/private-enterprise-repo-plan.md"
  ]
];

const aispmEvaluatorHandoffItems = [
  [
    "Trial Portal",
    "https://cavra-trial.mind-ops.cloud/",
    "Evaluator starts with the branded request and approval portal."
  ],
  [
    "Package Reference",
    "ghcr.io/huzefaaa2/cavra-enterprise-trial:2026.06.05",
    "Private GHCR image reference is provided only after approved package access."
  ],
  [
    "License Boundary",
    "CAVRA_LICENSE_KEY required",
    "Runtime validates a time-limited license; keys and signing material are never public."
  ],
  [
    "Lab Notebook",
    "AISPM Enterprise Trial Lab Notebook",
    "Step-by-step evaluation guide covers install, scenario run, evidence review, and closeout."
  ],
  [
    "Support Path",
    "hello@mind-ops.cloud",
    "Evaluator support and approval follow-up use the operator-controlled support channel."
  ],
  [
    "Closeout",
    "Expiry and revocation validation",
    "Trial end verifies blocked runtime access and private package access removal."
  ]
];

const aispmTrialJourneySteps = [
  [
    "01",
    "Request Submitted",
    "Evaluator submits the trial form on the CAVRA trial portal and receives a pending approval request ID.",
    "portal_request"
  ],
  [
    "02",
    "Operator Approved",
    "CAVRA owner reviews the request, approves access, and sends public-safe package and license instructions.",
    "operator_approval"
  ],
  [
    "03",
    "Package Pulled",
    "Evaluator authenticates to the private package registry and pulls the gated Enterprise Trial image.",
    "package_access"
  ],
  [
    "04",
    "License Validated",
    "Runtime validates CAVRA_LICENSE_KEY without exposing signing keys, license-server secrets, or customer material.",
    "license_boundary"
  ],
  [
    "05",
    "Scenario Executed",
    "Evaluator runs the lab notebook scenario and observes agent decision, policy, and evidence behavior.",
    "scenario_run"
  ],
  [
    "06",
    "Evidence Reviewed",
    "CSO/CISO or security reviewer inspects reports, readiness packet, and lab notebook evidence outputs.",
    "evidence_review"
  ],
  [
    "07",
    "Closeout Verified",
    "Trial expiry or revocation is validated, package access is removed, and blocked runtime behavior is confirmed.",
    "revocation_closeout"
  ]
];

const aispmTrialCloseoutEvidenceItems = [
  [
    "License Expiry",
    "Evidence Required",
    "Confirm the time-limited trial license reaches expiry and cannot authorize new runtime sessions.",
    "license_expiry"
  ],
  [
    "Revocation Check",
    "Evidence Required",
    "Validate that operator-triggered revocation blocks license validation before the original expiry date.",
    "license_revocation"
  ],
  [
    "Package Access Removal",
    "Evidence Required",
    "Confirm private registry/package access is removed for the evaluator identity at trial closeout.",
    "package_access_removed"
  ],
  [
    "Blocked Runtime Validation",
    "Evidence Required",
    "Run the trial container after expiry or revocation and record the expected blocked-access result.",
    "blocked_runtime_validation"
  ],
  [
    "Evidence Packet Archived",
    "Evidence Required",
    "Attach readiness packet, lab notebook outputs, report downloads, and closeout notes to the evaluation record.",
    "closeout_packet_archived"
  ],
  [
    "Evaluator Feedback",
    "Evidence Required",
    "Collect evaluator feedback, missing controls, procurement questions, and next-step disposition.",
    "evaluator_feedback"
  ]
];

const aispmTrialFeedbackCategories = [
  [
    "Setup Friction",
    "Install, registry login, environment variables, first run, and platform prerequisites.",
    "setup_friction"
  ],
  [
    "Policy Clarity",
    "Whether allow, warn, block, approval, and attestation decisions were understandable.",
    "policy_clarity"
  ],
  [
    "Dashboard Usefulness",
    "How well CSO/CISO, security, platform, and auditor views explain AI-agent posture.",
    "dashboard_usefulness"
  ],
  [
    "Report Usefulness",
    "Value of executive, audit, control, evidence, readiness, and closeout exports.",
    "report_usefulness"
  ],
  [
    "Integration Gaps",
    "Missing GitHub, GitLab, Azure DevOps, cloud, MCP, SIEM, ITSM, or identity workflow needs.",
    "integration_gaps"
  ],
  [
    "Procurement Concerns",
    "Questions about licensing, support, legal review, data handling, deployment, and renewal path.",
    "procurement_concerns"
  ],
  [
    "Go/No-Go Decision",
    "Final evaluator disposition, blockers, required proof, pilot scope, and buyer next step.",
    "go_no_go_decision"
  ]
];

const aispmTrialProcurementAreas = [
  [
    "Legal Review",
    "Terms, BUSL/open-core boundary, Enterprise source separation, trial terms, and data processing addendum questions.",
    "legal_review"
  ],
  [
    "Security Review",
    "Public boundary validation, excluded secret fields, license validation boundary, package access controls, and vulnerability response path.",
    "security_review"
  ],
  [
    "Deployment Review",
    "Trial install path, private package pull, runtime configuration, network assumptions, and future self-hosted or SaaS deployment model.",
    "deployment_review"
  ],
  [
    "Support Review",
    "Evaluator support channel, operator escalation, onboarding help, incident handling, and enterprise support expectations.",
    "support_review"
  ],
  [
    "Licensing Review",
    "Trial expiry, revocation, Business/Enterprise/SaaS license types, renewal path, and procurement approval gates.",
    "licensing_review"
  ],
  [
    "Data Handling",
    "No public customer records, no private keys, public-safe sample data only, and Enterprise tenant evidence storage boundary.",
    "data_handling"
  ],
  [
    "Pilot Scope",
    "Target repositories, AI agents, control surfaces, required checks, evidence owners, success criteria, and go/no-go date.",
    "pilot_scope"
  ]
];

const aispmTrialPilotScopeItems = [
  [
    "Target Repositories",
    "Select 2-3 protected repositories with active AI-assisted development and clear ownership.",
    "payments/api, platform/iac, security/policies"
  ],
  [
    "AI Agents",
    "Declare transparent automation identities and require CAVRA checks for their pull requests and sensitive actions.",
    "codex-agent, claude-code-agent, github-copilot-workspace"
  ],
  [
    "Required Checks",
    "Enable CAVRA policy decision, replay-to-policy review packet, boundary validation, and release evidence freshness checks.",
    "cavra-policy, cavra-review-packet, cavra-boundary, cavra-release-evidence"
  ],
  [
    "Policies",
    "Start with secrets, protected branch, production infrastructure, MCP trust, and release-governance policy packs.",
    "secrets, git, iac, mcp, release"
  ],
  [
    "Evidence Owners",
    "Assign security, platform, repo owner, GRC, and procurement reviewers for pilot evidence review.",
    "security lead, platform owner, repo owner, GRC, procurement"
  ],
  [
    "Success Criteria",
    "Measure blocked risky actions, approval latency, evidence completeness, evaluator feedback, and procurement readiness.",
    "blocked risk, approvals, reports, closeout, go/no-go"
  ],
  [
    "Go/No-Go Date",
    "Set a dated decision checkpoint after evidence review, feedback intake, and closeout validation.",
    "T+14 days from pilot start"
  ]
];

const aispmPilotApprovalChecklistItems = [
  [
    "Owner Assigned",
    "Named business, security, and platform owners approve the pilot scope and operating model.",
    "owner_assigned"
  ],
  [
    "Repos Selected",
    "Pilot repositories are protected, owned, active, and listed in the pilot scope packet.",
    "repos_selected"
  ],
  [
    "Agents Registered",
    "Transparent AI-agent identities are declared and mapped to repositories, tools, and control surfaces.",
    "agents_registered"
  ],
  [
    "Checks Enforced",
    "Required CAVRA checks are configured before agent-generated changes can merge or proceed.",
    "checks_enforced"
  ],
  [
    "Policies Selected",
    "Secrets, protected branch, infrastructure, MCP trust, and release-governance policies are in scope.",
    "policies_selected"
  ],
  [
    "Evidence Owners Assigned",
    "Security, platform, repo owner, GRC, and procurement evidence reviewers are assigned.",
    "evidence_owners_assigned"
  ],
  [
    "Support Path Confirmed",
    "Evaluator support, operator escalation, and incident-response contact paths are documented.",
    "support_path_confirmed"
  ],
  [
    "Go/No-Go Date Accepted",
    "A dated decision checkpoint is accepted by business, security, and platform owners.",
    "go_no_go_date_accepted"
  ]
];

const aispmPilotLaunchReadinessItems = [
  [
    "Scope Defined",
    "Ready",
    "Pilot scope packet identifies repositories, agents, required checks, policies, evidence owners, success criteria, and go/no-go date.",
    "cavra-aispm-trial-pilot-scope-packet.json"
  ],
  [
    "Approvals Prepared",
    "Ready",
    "Pilot approval packet lists final gates for owners, repositories, agents, checks, policies, evidence reviewers, support path, and decision date.",
    "cavra-aispm-pilot-approval-packet.json"
  ],
  [
    "Reports Available",
    "Ready",
    "CSO report center exposes executive, audit, control, evidence, and agent-risk downloads from public-safe posture data.",
    "CSO Report Center"
  ],
  [
    "Evidence Reviewed",
    "Ready",
    "Trial review packet, integrity panel, closeout evidence, and procurement readiness provide reviewer-ready evidence context.",
    "cavra-aispm-trial-review-packet.json"
  ],
  [
    "Support Confirmed",
    "Action Required",
    "Evaluator support and operator escalation path are documented; Enterprise support ownership must be confirmed before live pilot operations.",
    "hello@mind-ops.cloud"
  ],
  [
    "Go/No-Go Ready",
    "Candidate",
    "Community can show the launch decision model; signed approval, workflow write-back, and identity-bound decision evidence require Enterprise or SaaS.",
    "requires_cavra_enterprise_or_saas"
  ]
];

const aispmPilotEvidenceRoomItems = [
  [
    "CSO/CISO",
    "Launch decision packet, executive risk brief, board KPI pack, and go/no-go summary.",
    "cavra-aispm-pilot-launch-decision-packet.json",
    "signed executive approval and decision history require Enterprise"
  ],
  [
    "Security",
    "Trial review packet, policy decisions, blocked actions, near misses, control coverage, and evidence confidence.",
    "cavra-aispm-trial-review-packet.json",
    "tenant policy context and raw telemetry require Enterprise"
  ],
  [
    "Platform",
    "Pilot scope packet, required checks, CI gate readiness, rollout checklist, and integration readiness.",
    "cavra-aispm-trial-pilot-scope-packet.json",
    "workflow write-back and connector health state require Enterprise"
  ],
  [
    "Procurement",
    "Procurement readiness, licensing boundary, support path, deployment model, and commercial trial evidence.",
    "AISPM Trial Procurement Readiness",
    "commercial contract and customer records stay outside Community"
  ],
  [
    "Auditor",
    "Review packet integrity, audit summaries, control coverage export, evidence freshness export, and release packets.",
    "cavra-aispm-soc2-audit-summary.md",
    "signed evidence retention and chain-of-custody store require Enterprise"
  ],
  [
    "Operator",
    "Approval checklist, support path, launch readiness status, closeout evidence, and escalation model.",
    "cavra-aispm-pilot-approval-packet.json",
    "operator activity log and access grants require Enterprise or SaaS"
  ]
];

const aispmEvidenceReviewerChecklistItems = [
  [
    "CSO/CISO",
    "Confirm launch decision packet, executive risk brief, residual risk owner, and go/no-go recommendation are review-ready.",
    "Go/no-go owner named",
    "requires_enterprise_signed_decision"
  ],
  [
    "Security",
    "Confirm blocked-action evidence, policy coverage, near misses, control coverage, and evidence confidence are sufficient for pilot risk.",
    "Risk exceptions documented",
    "requires_enterprise_policy_context"
  ],
  [
    "Platform",
    "Confirm required checks, branch protection, CI gate rollout, agent identities, connector health, and rollback path are ready.",
    "Pilot guardrails enforceable",
    "requires_enterprise_workflow_write_back"
  ],
  [
    "Procurement",
    "Confirm license boundary, support path, deployment assumptions, data handling, and commercial evaluation terms are clear.",
    "Commercial trial path understood",
    "requires_customer_contract_record"
  ],
  [
    "Auditor",
    "Confirm review packet integrity, evidence retention expectation, control mappings, release packets, and chain-of-custody assumptions.",
    "Audit trail reviewable",
    "requires_enterprise_evidence_store"
  ],
  [
    "Operator",
    "Confirm support escalation, closeout evidence, revocation path, package access removal, and launch communication plan.",
    "Operator runbook ready",
    "requires_enterprise_operator_activity_log"
  ]
];

const aispmPilotExceptionRegisterItems = [
  [
    "EX-001",
    "Support ownership",
    "Open",
    "Operator",
    "Enterprise support owner must be confirmed before live pilot operations.",
    "Before pilot start",
    "requires_enterprise_support_assignment"
  ],
  [
    "EX-002",
    "Signed launch decision",
    "Accepted pending Enterprise",
    "CSO/CISO",
    "Community shows the model only; signed go/no-go decision evidence requires Enterprise workflow.",
    "Pilot launch gate",
    "requires_enterprise_signed_decision"
  ],
  [
    "EX-003",
    "Workflow write-back",
    "Open",
    "Platform",
    "Production pilot workflow write-back to GitHub, GitLab, or Azure DevOps remains Enterprise-only.",
    "Before enforced rollout",
    "requires_enterprise_workflow_write_back"
  ],
  [
    "EX-004",
    "Tenant evidence retention",
    "Accepted for Community demo",
    "Auditor",
    "Community exports public-safe packets; tenant retention policy enforcement requires Enterprise evidence store.",
    "Before audit reliance",
    "requires_enterprise_evidence_store"
  ],
  [
    "EX-005",
    "Policy context depth",
    "Monitor",
    "Security",
    "Private policy context and raw telemetry are excluded from Community and must be validated in Enterprise.",
    "During pilot week one",
    "requires_enterprise_policy_context"
  ],
  [
    "EX-006",
    "Commercial trial record",
    "Open",
    "Procurement",
    "Customer-specific commercial evaluation terms are tracked outside the public Community portal.",
    "Before procurement review",
    "requires_customer_contract_record"
  ]
];

const aispmPilotLaunchBoardPackItems = [
  [
    "Launch Decision",
    "cavra-aispm-pilot-launch-decision-packet.json",
    "CSO/CISO launch candidate status, readiness rows, and source artifact references.",
    "signed_launch_approval_requires_enterprise"
  ],
  [
    "Evidence Room",
    "cavra-aispm-pilot-evidence-room-packet.json",
    "Role-based evidence catalog for CSO/CISO, security, platform, procurement, auditor, and operator review.",
    "authenticated_evidence_room_requires_enterprise"
  ],
  [
    "Risk Acceptance",
    "cavra-aispm-pilot-risk-acceptance-packet.json",
    "Open exceptions, accepted risks, monitored risks, accountable owners, and launch blockers.",
    "signed_risk_acceptance_requires_enterprise"
  ],
  [
    "Exception Register",
    "cavra-aispm-pilot-exception-register-packet.json",
    "Unresolved risks, accepted exceptions, owners, status, expiry expectation, and exception lifecycle boundary.",
    "exception_lifecycle_requires_enterprise"
  ],
  [
    "Reviewer Checklist",
    "cavra-aispm-evidence-reviewer-checklist-packet.json",
    "Role-specific pre-pilot acceptance criteria for launch review records.",
    "identity_bound_reviewer_records_require_enterprise"
  ],
  [
    "Executive Reports",
    "CSO Report Center",
    "Executive risk brief, board KPI pack, audit summary, control coverage, evidence freshness, and agent risk exports.",
    "pdf_board_pack_and_delivery_require_enterprise"
  ]
];

const aispmPilotControlReadinessItems = [
  [
    "Exception Register",
    "Owner Review",
    "cavra-aispm-pilot-exception-register-packet.json",
    "Open, accepted, and monitored pilot exceptions have owner, expiry, and Enterprise workflow boundaries."
  ],
  [
    "Risk Acceptance",
    "CSO/CISO Decision",
    "cavra-aispm-pilot-risk-acceptance-packet.json",
    "Residual risk, launch blockers, accountable owners, and signed acceptance boundary are ready for approval review."
  ],
  [
    "Board Pack",
    "Board Ready",
    "cavra-aispm-pilot-launch-board-pack-packet.json",
    "Launch decision, evidence room, exception, risk, reviewer, and executive report artifacts are grouped for board review."
  ],
  [
    "Artifact Freshness",
    "Validated",
    "docs/release-verifications/aispm-launch-board-pack-artifact-index.json",
    "The artifact index and validator prevent launch packet drift before external pilot communication."
  ],
  [
    "Launch Rollup",
    "Release Gate",
    "docs/release-verifications/aispm-launch-readiness-rollup.json",
    "The overall launch rollup includes portal, visual, hosted, report, trial, and pilot control readiness gates."
  ]
];

const aispmReleaseEvidenceIndexItems = [
  [
    "AISPM Launch Readiness Rollup",
    "docs/release-verifications/aispm-launch-readiness-rollup.md",
    "docs/release-verifications/aispm-launch-readiness-rollup.json",
    "scripts/validate-aispm-launch-readiness.py",
    "Release candidate launch readiness, source gates, and public-safety boundaries.",
    "ready"
  ],
  [
    "Launch Board Pack Artifact Index",
    "docs/release-verifications/aispm-launch-board-pack-artifact-index.md",
    "docs/release-verifications/aispm-launch-board-pack-artifact-index.json",
    "scripts/validate-aispm-launch-artifacts.py",
    "Board/CISO launch artifacts, freshness gate, and source packet references.",
    "ready"
  ],
  [
    "AISPM Report Catalog Readiness",
    "docs/release-verifications/aispm-report-catalog-readiness.md",
    "docs/release-verifications/aispm-report-catalog-readiness.json",
    "scripts/validate-aispm-report-catalog-readiness.py",
    "Community report downloads and Enterprise report rendering, scheduling, email, and signed package boundaries.",
    "ready"
  ],
  [
    "AISPM Report Delivery Setup Readiness",
    "docs/release-verifications/aispm-report-delivery-setup-readiness.md",
    "docs/release-verifications/aispm-report-delivery-setup-readiness.json",
    "scripts/validate-aispm-report-delivery-setup-readiness.py",
    "Enterprise setup checklist for sender identity, provider mode, recipient governance, schedule, retention, and audit evidence.",
    "ready"
  ],
  [
    "AISPM Report Operations Readiness",
    "docs/release-verifications/aispm-report-operations-readiness.md",
    "docs/release-verifications/aispm-report-operations-readiness.json",
    "scripts/validate-aispm-report-operations-readiness.py",
    "Enterprise operations checklist for delivery audit events, delivery health, retention lifecycle, search/retrieval, and signed export package manifests.",
    "ready"
  ],
  [
    "AISPM Report Governance Readiness",
    "docs/release-verifications/aispm-report-governance-readiness.md",
    "docs/release-verifications/aispm-report-governance-readiness.json",
    "scripts/validate-aispm-report-governance-readiness.py",
    "Enterprise governance checklist for schedules, recipients, approvals, exceptions, and scoped evidence rooms.",
    "ready"
  ],
  [
    "AISPM Report Assurance Readiness",
    "docs/release-verifications/aispm-report-assurance-readiness.md",
    "docs/release-verifications/aispm-report-assurance-readiness.json",
    "scripts/validate-aispm-report-assurance-readiness.py",
    "Enterprise assurance checklist for evidence-room access events, incident packets, incident closure, KPI metrics, and alert escalation.",
    "ready"
  ],
  [
    "AISPM Report Response Readiness",
    "docs/release-verifications/aispm-report-response-readiness.md",
    "docs/release-verifications/aispm-report-response-readiness.json",
    "scripts/validate-aispm-report-response-readiness.py",
    "Enterprise response checklist for alert operations, drilldowns, remediation plans, remediation closure, and closure operations.",
    "ready"
  ],
  [
    "AISPM Report Trial Operations Readiness",
    "docs/release-verifications/aispm-report-trial-operations-readiness.md",
    "docs/release-verifications/aispm-report-trial-operations-readiness.json",
    "scripts/validate-aispm-report-trial-operations-readiness.py",
    "Enterprise trial operations checklist for executive digests, digest distribution, trial validation, and operator dashboard/API readiness.",
    "ready"
  ],
  [
    "AISPM Pilot Control Readiness",
    "docs/release-verifications/aispm-pilot-control-readiness.md",
    "docs/release-verifications/aispm-pilot-control-readiness.json",
    "scripts/validate-aispm-pilot-control-readiness.py",
    "Production-pilot controls for exceptions, risk acceptance, board pack, artifact freshness, and launch rollup.",
    "ready"
  ],
  [
    "AISPM v1.0 Public Release Readiness",
    "docs/release-verifications/aispm-v1.0-public-release-readiness.md",
    "docs/release-verifications/aispm-v1.0-public-release-readiness.json",
    "scripts/validate-aispm-v100-public-release.py",
    "AISPM-specific release notes, public walkthrough, lab notebook assets, final validation, and announcement readiness.",
    "ready"
  ],
  [
    "AISPM Final Announcement Readiness",
    "docs/release-verifications/aispm-final-announcement-readiness.md",
    "docs/release-verifications/aispm-final-announcement-readiness.json",
    "scripts/validate-aispm-final-announcement-readiness.py",
    "Final public-safe go/no-go packet for announcing CAVRA Community AISPM v1.0 and the CAVRA Trial Field Guide.",
    "ready"
  ],
  [
    "AISPM Visual Smoke Validation",
    "docs/release-verifications/aispm-visual-smoke-validation.md",
    "docs/release-verifications/aispm-visual-smoke-validation.json",
    "npm run validate:sandbox:visual",
    "Local browser validation for themes, AISPM board pack, report center, and command palette.",
    "pass"
  ],
  [
    "Hosted Sandbox Pages Smoke",
    "docs/release-verifications/hosted-sandbox-pages-smoke-validation.md",
    "docs/release-verifications/hosted-sandbox-pages-smoke-validation.json",
    "npm run validate:sandbox:hosted",
    "Post-deploy browser validation for the live GitHub Pages dashboard and AISPM routes.",
    "workflow_enforced"
  ],
  [
    "Hosted Sandbox Deployment Freshness",
    "docs/release-verifications/hosted-sandbox-deployment-freshness.md",
    "docs/release-verifications/hosted-sandbox-deployment-freshness.json",
    "scripts/validate-hosted-sandbox-deployment-freshness.py",
    "Build sentinel that separates local readiness from stale GitHub Pages deployment state.",
    "ready"
  ],
  [
    "Hosted Sandbox Operator Release Status",
    "docs/release-verifications/hosted-sandbox-operator-release-status.md",
    "docs/release-verifications/hosted-sandbox-operator-release-status.json",
    "scripts/validate-hosted-sandbox-operator-status.py",
    "Operator go/no-go view for local readiness, live Pages freshness, hosted smoke, and announcement state.",
    "ready"
  ],
  [
    "Hosted Sandbox Post-Deploy Evidence",
    "docs/release-verifications/hosted-sandbox-post-deploy-evidence.md",
    "docs/release-verifications/hosted-sandbox-post-deploy-evidence.json",
    "scripts/validate-hosted-sandbox-deploy-evidence.py",
    "Runtime workflow artifact contract for Pages URL, commit SHA, run URL, and hosted smoke status.",
    "workflow_enforced"
  ],
  [
    "Trial Lab Notebook Readiness",
    "docs/release-verifications/aispm-trial-lab-notebook-publication-readiness-summary.md",
    "docs/release-verifications/aispm-trial-lab-notebook-publication-readiness-summary.json",
    "scripts/validate-aispm-trial-lab-notebook.py --check-summary",
    "Wiki lab notebook navigation, screenshots, public-safety, acceptance criteria, and blockers.",
    "ready"
  ],
  [
    "Phase B Closeout Verification",
    "docs/aispm-phase-b-closeout-verification.md",
    "docs/aispm-phase-b-closeout-verification.md",
    "scripts/validate-sandbox-portal.py",
    "Community AISPM Phase B closeout evidence for the public-safe dashboard baseline.",
    "pass"
  ]
];

const aispmReportSetupReadinessItems = [
  [
    "Organization Profile",
    "Required",
    "CAVRA_REPORT_FROM_ADDRESS, CAVRA_REPORT_DEFAULT_TIMEZONE, CAVRA_REPORT_RETENTION_DAYS, CAVRA_REPORT_BRAND_PROFILE",
    "Verified sender identity, timezone, retention, and branding references for CSO reports."
  ],
  [
    "Delivery Provider",
    "Enterprise",
    "CAVRA_REPORT_DELIVERY_MODE, CAVRA_REPORT_SMTP_HOST, CAVRA_REPORT_SMTP_PORT, CAVRA_REPORT_SMTP_USERNAME_REF, CAVRA_REPORT_SMTP_PASSWORD_REF, CAVRA_REPORT_PROVIDER_TOKEN_REF",
    "SMTP, Microsoft 365, Google Workspace, SES, SendGrid, or webhook mode with secret-manager references only."
  ],
  [
    "Recipient Governance",
    "Required",
    "CAVRA_REPORT_ALLOWED_RECIPIENT_DOMAINS, CAVRA_REPORT_EXTERNAL_APPROVAL_REQUIRED, CAVRA_REPORT_ALLOWED_RBAC_ROLES",
    "Domain allowlists, RBAC roles, and optional approval gates before external report delivery."
  ],
  [
    "Schedule And Audit",
    "Required",
    "CAVRA_REPORT_DEFAULT_SCHEDULE, CAVRA_REPORT_RETRY_POLICY, CAVRA_REPORT_DELIVERY_AUDIT_RETENTION_DAYS, CAVRA_REPORT_AUDIT_EXPORT_REF",
    "Report cadence, retry policy, delivery audit retention, and immutable audit export references."
  ],
  [
    "Validation And Test Delivery",
    "Enterprise",
    "provider_validation, test_delivery, delivery_audit, retry_evidence",
    "Private Enterprise validates provider auth, sender alignment, recipient policy, test send, retry, and audit evidence."
  ]
];

const aispmReportOperationsReadinessItems = [
  [
    "Delivery Audit Events",
    "Enterprise",
    "src/cavra/schemas/aispm-report-delivery-audit-event.schema.json",
    "examples/aispm/enterprise-report-delivery-audit-event-public.example.json",
    "Immutable render, send, schedule, test-delivery, retry, approval, and failure evidence for every report operation."
  ],
  [
    "Operations Dashboard",
    "Enterprise",
    "src/cavra/schemas/aispm-report-operations-dashboard.schema.json",
    "examples/aispm/enterprise-report-operations-dashboard-public.example.json",
    "CSO and platform views for delivery health, queue depth, retries, approval latency, audit coverage, and operational blockers."
  ],
  [
    "Retention Lifecycle",
    "Enterprise",
    "src/cavra/schemas/aispm-report-retention-lifecycle.schema.json",
    "examples/aispm/enterprise-report-retention-lifecycle-public.example.json",
    "Retention policy, legal hold, immutable archive, deletion approval, purge evidence, and exception tracking for report artifacts."
  ],
  [
    "Search And Retrieval",
    "Enterprise",
    "src/cavra/schemas/aispm-report-search-retrieval.schema.json",
    "examples/aispm/enterprise-report-search-retrieval-public.example.json",
    "RBAC-scoped report lookup, retention-aware retrieval, auditor access windows, download approvals, and access audit events."
  ],
  [
    "Export Package Manifest",
    "Enterprise",
    "src/cavra/schemas/aispm-report-export-package-manifest.schema.json",
    "examples/aispm/enterprise-report-export-package-manifest-public.example.json",
    "Signed package manifests with hashes, evidence references, rendering provenance, and GRC/SIEM delivery package metadata."
  ]
];

const aispmReportGovernanceReadinessItems = [
  [
    "Schedule Policy",
    "Enterprise",
    "src/cavra/schemas/aispm-report-schedule-policy.schema.json",
    "examples/aispm/enterprise-report-schedule-policy-public.example.json",
    "Recurring report schedules, blackout windows, approval requirements, retry policy, and tenant timezone controls."
  ],
  [
    "Recipient Policy",
    "Enterprise",
    "src/cavra/schemas/aispm-report-recipient-policy.schema.json",
    "examples/aispm/enterprise-report-recipient-policy-public.example.json",
    "Domain allowlists, RBAC roles, external-send approval, channel restrictions, and delivery policy evidence."
  ],
  [
    "Approval Decisions",
    "Enterprise",
    "src/cavra/schemas/aispm-report-approval-decision.schema.json",
    "examples/aispm/enterprise-report-approval-decision-public.example.json",
    "Immutable approval, denial, expiry, escalation, and break-glass decisions for report sends and schedule changes."
  ],
  [
    "Exception Lifecycle",
    "Enterprise",
    "src/cavra/schemas/aispm-report-exception-lifecycle.schema.json",
    "examples/aispm/enterprise-report-exception-lifecycle-public.example.json",
    "Time-boxed exceptions with owner, expiry, renewal, revocation, closeout, and evidence-backed review state."
  ],
  [
    "Evidence Rooms",
    "Enterprise",
    "src/cavra/schemas/aispm-report-evidence-room.schema.json",
    "examples/aispm/enterprise-report-evidence-room-public.example.json",
    "Scoped, expiring, watermarked evidence rooms for auditors and executives with access audit and revocation boundaries."
  ]
];

const aispmReportAssuranceReadinessItems = [
  [
    "Evidence Room Access Events",
    "Enterprise",
    "src/cavra/schemas/aispm-report-evidence-room-access-event.schema.json",
    "examples/aispm/enterprise-report-evidence-room-access-event-public.example.json",
    "Immutable view, download, expiry, revocation, failed access, and watermark audit events for shared report evidence."
  ],
  [
    "Incident Packet",
    "Enterprise",
    "src/cavra/schemas/aispm-report-incident-packet.schema.json",
    "examples/aispm/enterprise-report-incident-packet-public.example.json",
    "Curated incident review packets that connect exceptions, approvals, evidence rooms, timelines, and impacted report refs."
  ],
  [
    "Incident Closure",
    "Enterprise",
    "src/cavra/schemas/aispm-report-incident-closure.schema.json",
    "examples/aispm/enterprise-report-incident-closure-public.example.json",
    "Evidence-backed closure decisions with remediation status, owner confirmation, reopen criteria, and audit signoff boundary."
  ],
  [
    "KPI Metrics",
    "Enterprise",
    "src/cavra/schemas/aispm-report-kpi-metrics.schema.json",
    "examples/aispm/enterprise-report-kpi-metrics-public.example.json",
    "Aggregate CSO metrics for report volume, delivery reliability, approval latency, exception age, and audit readiness."
  ],
  [
    "Alert Escalation",
    "Enterprise",
    "src/cavra/schemas/aispm-report-alert-escalation.schema.json",
    "examples/aispm/enterprise-report-alert-escalation-public.example.json",
    "Escalation routing for KPI breaches, risky report sharing, stale evidence, failed delivery, and suspicious access patterns."
  ]
];

const aispmReportResponseReadinessItems = [
  [
    "Alert Operations Dashboard",
    "Enterprise",
    "src/cavra/schemas/aispm-report-alert-operations-dashboard.schema.json",
    "examples/aispm/enterprise-report-alert-operations-dashboard-public.example.json",
    "CSO/SOC/GRC alert operations view for escalation health, queue pressure, assignment state, and evidence-backed triage."
  ],
  [
    "Alert Drilldown",
    "Enterprise",
    "src/cavra/schemas/aispm-report-alert-drilldown.schema.json",
    "examples/aispm/enterprise-report-alert-drilldown-public.example.json",
    "Authorized drilldown contract for alert context, related evidence, impacted report refs, and public-safe redaction guarantees."
  ],
  [
    "Alert Remediation Plan",
    "Enterprise",
    "src/cavra/schemas/aispm-report-alert-remediation-plan.schema.json",
    "examples/aispm/enterprise-report-alert-remediation-plan-public.example.json",
    "Remediation plan structure for alert findings, tasks, owners by role, due dates, approval gates, and evidence requirements."
  ],
  [
    "Alert Remediation Closure",
    "Enterprise",
    "src/cavra/schemas/aispm-report-alert-remediation-closure.schema.json",
    "examples/aispm/enterprise-report-alert-remediation-closure-public.example.json",
    "Closure proof for remediated alert findings with verification state, residual risk, reopen criteria, and audit-ready evidence refs."
  ],
  [
    "Remediation Closure Operations",
    "Enterprise",
    "src/cavra/schemas/aispm-report-remediation-closure-operations-dashboard.schema.json",
    "examples/aispm/enterprise-report-remediation-closure-operations-dashboard-public.example.json",
    "Operations dashboard contract for closure readiness, overdue remediation, due-soon work, and close-time statistics."
  ]
];

const aispmReportTrialOpsReadinessItems = [
  [
    "Remediation Closure Executive Digest",
    "Enterprise",
    "src/cavra/schemas/aispm-report-remediation-closure-executive-digest.schema.json",
    "examples/aispm/enterprise-report-remediation-closure-executive-digest-public.example.json",
    "Executive digest contract for closure metrics, residual-risk summary, board talking points, audit readiness, and evidence refs."
  ],
  [
    "Remediation Closure Digest Distribution",
    "Enterprise",
    "src/cavra/schemas/aispm-report-remediation-closure-digest-distribution.schema.json",
    "examples/aispm/enterprise-report-remediation-closure-digest-distribution-public.example.json",
    "Distribution readiness for approval-before-send, recipient governance, delivery modes, signed manifests, and immutable send evidence."
  ],
  [
    "Enterprise Trial Validation Packet",
    "Enterprise",
    "src/cavra/schemas/aispm-report-center-trial-validation-packet.schema.json",
    "examples/aispm/enterprise-report-center-trial-validation-packet-public.example.json",
    "Trial validation packet covering setup, report rendering, blocked sends, approved sends, evidence rooms, revocation, and retention."
  ],
  [
    "Trial Operator Dashboard Readiness",
    "Enterprise",
    "src/cavra/schemas/aispm-report-center-trial-operator-dashboard-readiness.schema.json",
    "examples/aispm/enterprise-report-center-trial-operator-dashboard-readiness-public.example.json",
    "Operator dashboard readiness for validation status, blockers, evidence refs, package/license state, and evaluator handoff."
  ],
  [
    "Trial Operator API View Model",
    "Enterprise",
    "src/cavra/schemas/aispm-report-center-trial-operator-api-view-model.schema.json",
    "examples/aispm/enterprise-report-center-trial-operator-api-view-model-public.example.json",
    "Public-safe API/view-model contract for private operator routes, state transitions, actions, and required audit events."
  ]
];

const aispmHostedReleaseStatusItems = [
  [
    "Local portal freshness",
    "ready",
    "python scripts/validate-hosted-sandbox-deployment-freshness.py",
    "Local static portal contains AISPM trial lab notebook, release evidence index, packet filename, and build sentinel markers."
  ],
  [
    "Live Pages freshness",
    "requires_deploy",
    "CAVRA_CHECK_LIVE_SANDBOX=true python scripts/validate-hosted-sandbox-deployment-freshness.py",
    "Live GitHub Pages must match the build sentinel before external announcement or evaluator handoff."
  ],
  [
    "Hosted browser smoke",
    "workflow_enforced",
    "npm run validate:sandbox:hosted",
    "Post-deploy browser validation checks dashboard and AISPM routes, command palette, report center, and board pack visibility."
  ],
  [
    "Post-deploy artifact",
    "workflow_enforced",
    "cavra-hosted-sandbox-post-deploy-evidence",
    "Deploy workflow uploads public-safe Pages URL, commit SHA, run URL, ref, and hosted smoke status evidence."
  ],
  [
    "Announcement gate",
    "blocked_until_live_fresh",
    "Hosted Release Operator Status",
    "Announce only after local validation, live freshness, hosted smoke, and post-deploy evidence all pass for the same deployment."
  ]
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
  ["Self-Service Trial Access", "docs/enterprise/trial-self-service-access.md"],
  [
    "AISPM Trial Lab Notebook Readiness",
    "docs/release-verifications/aispm-trial-lab-notebook-publication-readiness-summary.md"
  ],
  [
    "AISPM Final Announcement Readiness",
    "docs/release-verifications/aispm-final-announcement-readiness.md"
  ]
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
  { type: "Enterprise Trial", label: "AISPM Trial Lab Notebook Readiness", route: "enterprise-trial", description: "Open reviewer-facing publication readiness links for the Enterprise Trial lab notebook." },
  { type: "Enterprise Trial", label: "Trial Lab Notebook Readiness Summary", route: "enterprise-trial", description: "Review the Markdown readiness summary for pages, navigation, public-safety status, and blockers." },
  { type: "Enterprise Trial", label: "Trial Lab Notebook Readiness JSON", route: "enterprise-trial", description: "Review the machine-readable AISPM trial lab notebook readiness summary packet." },
  { type: "Enterprise Trial", label: "Enterprise Trial Lab Notebook Wiki", route: "enterprise-trial", description: "Open the GitHub Wiki trial lab notebook for approved evaluator walkthroughs." },
  { type: "AI Posture", label: "Agent Observability", route: "ai-posture", description: "Live-ready agent coverage, risk findings, and execution timeline." },
  { type: "AI Posture", label: "Kill Switch", route: "ai-posture", description: "Enterprise runtime control plane capability marked as locked in Community." },
  { type: "AI Posture", label: "Evidence Confidence", route: "ai-posture", description: "Dashboard tiles identify sample, local, or Enterprise data provenance." },
  { type: "AI Posture", label: "Evidence Confidence Drilldown", route: "ai-posture", description: "Rank policy decisions by signed, activity, sample, metadata-only, or missing evidence." },
  { type: "AI Posture", label: "Evidence Freshness SLO", route: "ai-posture", description: "Show stale evidence, retention gaps, and Enterprise archive-readiness boundaries." },
  { type: "AI Posture", label: "Executive Risk Narrative", route: "ai-posture", description: "Summarize Community-safe posture, top risks, evidence gaps, and leadership actions." },
  { type: "AI Posture", label: "AISPM Enterprise Trial Readiness Checklist", route: "ai-posture", description: "Review lab notebook, access portal, operator approval, revocation, and release evidence status in one CSO view." },
  { type: "AI Posture", label: "Release Evidence Index", route: "ai-posture", description: "Open reviewer-friendly links to AISPM launch, visual, hosted Pages, post-deploy, and lab notebook evidence." },
  { type: "AI Posture", label: "Release Evidence Index Packet", route: "ai-posture", description: "Copy or download the public-safe release evidence index packet for reviewers and auditors." },
  { type: "AI Posture", label: "Hosted Release Operator Status", route: "ai-posture", description: "Review local freshness, live Pages freshness, hosted smoke, post-deploy evidence, and announcement go/no-go status." },
  { type: "AI Posture", label: "Hosted Release Operator Status Packet", route: "ai-posture", description: "Copy or download the public-safe hosted release operator packet for release reviewers." },
  { type: "AI Posture", label: "CSO Report Catalog Readiness", route: "ai-posture", description: "Review Community report downloads and Enterprise-only report rendering, scheduling, email, and signed package boundaries." },
  { type: "AI Posture", label: "Report Catalog Readiness Packet", route: "ai-posture", description: "Copy or download the public-safe AISPM report catalog packet for CSO, audit, procurement, and release reviewers." },
  { type: "AI Posture", label: "Report Delivery Setup Readiness", route: "ai-posture", description: "Review Enterprise setup requirements for sender identity, provider mode, recipients, schedule, retention, and audit evidence." },
  { type: "AI Posture", label: "Report Delivery Setup Packet", route: "ai-posture", description: "Copy or download the public-safe report delivery setup packet for tenant onboarding and trial operator handoff." },
  { type: "AI Posture", label: "Report Operations Readiness", route: "ai-posture", description: "Review Enterprise report delivery audit, operations dashboard, retention, search, retrieval, and signed package manifest readiness." },
  { type: "AI Posture", label: "Report Operations Readiness Packet", route: "ai-posture", description: "Copy or download the public-safe report operations readiness packet for Enterprise delivery operations review." },
  { type: "AI Posture", label: "Report Governance Readiness", route: "ai-posture", description: "Review Enterprise report schedule, recipient, approval, exception, and evidence-room governance readiness." },
  { type: "AI Posture", label: "Report Governance Readiness Packet", route: "ai-posture", description: "Copy or download the public-safe report governance readiness packet for Enterprise governance review." },
  { type: "AI Posture", label: "Report Assurance Readiness", route: "ai-posture", description: "Review Enterprise evidence-room access, incident, closure, KPI, and alert escalation assurance readiness." },
  { type: "AI Posture", label: "Report Assurance Readiness Packet", route: "ai-posture", description: "Copy or download the public-safe report assurance readiness packet for audit and CSO review." },
  { type: "AI Posture", label: "Report Response Readiness", route: "ai-posture", description: "Review Enterprise alert operations, drilldowns, remediation plans, remediation closure, and closure operations readiness." },
  { type: "AI Posture", label: "Report Response Readiness Packet", route: "ai-posture", description: "Copy or download the public-safe report response readiness packet for SOC, CSO, and audit review." },
  { type: "AI Posture", label: "Report Trial Operations Readiness", route: "ai-posture", description: "Review Enterprise executive digest, distribution, trial validation, and operator dashboard/API readiness." },
  { type: "AI Posture", label: "Report Trial Operations Readiness Packet", route: "ai-posture", description: "Copy or download the public-safe report trial operations readiness packet for trial operator review." },
  { type: "AI Posture", label: "Trial readiness export", route: "ai-posture", description: "Copy a Markdown readiness summary or download a public-safe Enterprise Trial readiness packet." },
  { type: "AI Posture", label: "Enterprise Trial Evaluator Handoff", route: "ai-posture", description: "Show what approved evaluators receive after operator approval: portal, package, license boundary, lab notebook, and support path." },
  { type: "AI Posture", label: "Enterprise Trial Evaluation Journey", route: "ai-posture", description: "Follow the trial flow from request submission to approval, package pull, license validation, scenario execution, evidence review, and closeout." },
  { type: "AI Posture", label: "AISPM Trial Closeout Evidence", route: "ai-posture", description: "Verify expiry, revocation, package access removal, blocked runtime validation, archived evidence, and evaluator feedback." },
  { type: "AI Posture", label: "AISPM Trial Feedback Intake", route: "ai-posture", description: "Show evaluator feedback categories for setup friction, policy clarity, dashboard usefulness, reports, integrations, procurement, and go/no-go decision." },
  { type: "AI Posture", label: "AISPM Trial Outcome Summary", route: "ai-posture", description: "Roll up readiness, handoff, journey, closeout evidence, and feedback coverage into a CSO/CISO go/no-go view." },
  { type: "AI Posture", label: "AISPM Trial Review Packet Export", route: "ai-posture", description: "Copy or download the public-safe trial review packet for CSO/CISO or procurement review." },
  { type: "AI Posture", label: "AISPM Trial Review Packet Integrity", route: "ai-posture", description: "Show review packet schema, generated timestamp, expected filename, public-safety boundary, and excluded private fields." },
  { type: "AI Posture", label: "AISPM Trial Procurement Readiness", route: "ai-posture", description: "Map trial outcomes to buyer review areas: legal, security, deployment, support, licensing, data handling, and pilot scope." },
  { type: "AI Posture", label: "AISPM Trial Pilot Scope Builder", route: "ai-posture", description: "Draft target repositories, AI agents, required checks, policies, evidence owners, success criteria, and go/no-go date for a controlled pilot." },
  { type: "AI Posture", label: "AISPM Trial Pilot Scope Packet", route: "ai-posture", description: "Copy or download the public-safe pilot scope packet for an internal pilot approval ticket." },
  { type: "AI Posture", label: "AISPM Pilot Approval Checklist", route: "ai-posture", description: "Show final approval gates before a production pilot starts." },
  { type: "AI Posture", label: "AISPM Pilot Approval Packet", route: "ai-posture", description: "Copy or download a public-safe packet that bundles pilot scope and approval gates." },
  { type: "AI Posture", label: "AISPM Pilot Launch Readiness Summary", route: "ai-posture", description: "Roll up scope, approvals, reports, evidence, support, and go/no-go readiness for production pilot launch." },
  { type: "AI Posture", label: "AISPM Pilot Launch Decision Packet", route: "ai-posture", description: "Copy or download a public-safe launch decision packet for CSO/CISO approval records." },
  { type: "AI Posture", label: "Production Pilot Evidence Room", route: "ai-posture", description: "Group pilot artifacts by CSO/CISO, security, platform, procurement, auditor, and operator review needs." },
  { type: "AI Posture", label: "Production Pilot Evidence Room Packet", route: "ai-posture", description: "Copy or download the public-safe role-based evidence catalog for reviewer handoff." },
  { type: "AI Posture", label: "Evidence Room Reviewer Checklist", route: "ai-posture", description: "Show pre-pilot acceptance criteria by CSO/CISO, security, platform, procurement, auditor, and operator role." },
  { type: "AI Posture", label: "Evidence Room Reviewer Checklist Packet", route: "ai-posture", description: "Copy or download public-safe reviewer acceptance criteria for launch review records." },
  { type: "AI Posture", label: "Pilot Exception Register", route: "ai-posture", description: "Show unresolved risks and accepted exceptions before production pilot launch." },
  { type: "AI Posture", label: "Pilot Exception Register Packet", route: "ai-posture", description: "Copy or download public-safe unresolved risks and accepted exceptions for launch approval records." },
  { type: "AI Posture", label: "Pilot Risk Acceptance Summary", route: "ai-posture", description: "Roll up open exceptions, accepted risks, accountable owners, and launch blockers for CSO/CISO review." },
  { type: "AI Posture", label: "Pilot Risk Acceptance Packet", route: "ai-posture", description: "Copy or download the public-safe CSO/CISO risk acceptance roll-up for launch approval records." },
  { type: "AI Posture", label: "Pilot Launch Board Pack", route: "ai-posture", description: "Group launch decision, evidence room, risk acceptance, and exception register artifacts into one board-ready view." },
  { type: "AI Posture", label: "Pilot Launch Board Pack Packet", route: "ai-posture", description: "Copy or download the public-safe board/CISO artifact index with freshness and integrity metadata." },
  { type: "AI Posture", label: "Pilot Control Readiness", route: "ai-posture", description: "Review production-pilot exception, risk, board, artifact freshness, and launch-rollup controls." },
  { type: "AI Posture", label: "Pilot Control Readiness Packet", route: "ai-posture", description: "Copy or download the public-safe production-pilot control readiness packet." },
  { type: "AI Posture", label: "CSO Report Center", route: "ai-posture", description: "Download executive, audit, control, evidence, and agent-risk reports from public-safe posture data." },
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
  { type: "AI Posture", label: "CI Gate Rollout Auditor View", route: "ai-posture", description: "Summarize audit packet status, evidence attachments, and public-safe rollout findings." },
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

function csvCell(value) {
  const text = String(value ?? "");
  return `"${text.replace(/"/g, '""')}"`;
}

function toCsv(headers, rows) {
  return [
    headers.map(csvCell).join(","),
    ...rows.map((row) => headers.map((header) => csvCell(row[header])).join(","))
  ].join("\n");
}

function downloadTextFile(filename, content, type = "text/plain") {
  const blob = new Blob([content], { type });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = filename;
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  URL.revokeObjectURL(url);
}

function buildAispmReportCatalog(payload) {
  const generatedAt = new Date().toISOString();
  const overview = payload.overview || {};
  const agents = payload.agents || [];
  const findings = payload.findings || [];
  const controlCoverage = payload.control_coverage || [];
  const evidenceFreshness = payload.evidence_freshness_slo?.items || aispmEvidenceFreshnessFallback.items || [];
  const narrative = payload.executive_risk_narrative || aispmExecutiveNarrativeFallback.narrative || {};
  const source = payload.data_provenance || "sample_data";
  const topFindings = findings.slice(0, 8).map((finding) => `- ${finding.severity || "unknown"}: ${finding.risk_classification || "policy finding"} (${finding.agent_id || "unknown-agent"} / ${finding.repository || "local"})`).join("\n") || "- No current findings.";
  const executiveMarkdown = [
    "# CAVRA AISPM Executive Risk Brief",
    "",
    `Generated: ${generatedAt}`,
    `Data provenance: ${source}`,
    "",
    "## Summary",
    "",
    `Posture score: ${overview.posture_score ?? "n/a"}`,
    `Risk level: ${overview.risk_level || "unknown"}`,
    `Total sessions: ${overview.total_sessions ?? 0}`,
    `Total decisions: ${overview.total_decisions ?? 0}`,
    `Blocked actions: ${overview.blocked_actions ?? 0}`,
    `Approval-gated actions: ${overview.approval_required_actions ?? 0}`,
    `Risk findings: ${overview.risk_findings ?? findings.length}`,
    "",
    "## Executive Narrative",
    "",
    narrative.headline || narrative.summary || "CAVRA generated this public-safe summary from local or sample posture metadata.",
    "",
    "## Top Findings",
    "",
    topFindings,
    "",
    "## Community Boundary",
    "",
    "This Community report excludes raw prompts, model reasoning, raw tool output, tenant secrets, private connector payloads, and customer data. Enterprise adds authenticated live ingestion, scheduled delivery, PDF/XLSX packs, and delivery evidence.",
    ""
  ].join("\n");
  const boardJson = JSON.stringify({
    schema_version: "cavra.aispm.board_kpi_pack.v1",
    product: "CAVRA",
    edition: "community",
    generated_at: generatedAt,
    data_provenance: source,
    tracking: "none",
    telemetry: "disabled",
    overview: {
      posture_score: overview.posture_score ?? 0,
      risk_level: overview.risk_level || "unknown",
      total_sessions: overview.total_sessions ?? 0,
      total_decisions: overview.total_decisions ?? 0,
      blocked_actions: overview.blocked_actions ?? 0,
      approval_required_actions: overview.approval_required_actions ?? 0,
      risk_findings: overview.risk_findings ?? findings.length,
      evidence_confidence: overview.evidence_confidence || "unknown"
    },
    agent_count: agents.length,
    control_surface_count: controlCoverage.length,
    top_risks: findings.slice(0, 5).map((finding) => ({
      severity: finding.severity || "unknown",
      risk_classification: finding.risk_classification || "policy_finding",
      decision: finding.decision || "review",
      agent_id: finding.agent_id || "unknown-agent",
      repository: finding.repository || "local"
    })),
    enterprise_expansion: {
      pdf_pack: "requires_cavra_enterprise",
      xlsx_pack: "requires_cavra_enterprise",
      scheduled_email_delivery: "requires_cavra_enterprise",
      recipient_allowlists: "requires_cavra_enterprise"
    }
  }, null, 2);
  const soc2Markdown = [
    "# CAVRA AISPM SOC 2-Style Audit Summary",
    "",
    `Generated: ${generatedAt}`,
    `Data provenance: ${source}`,
    "",
    "| Control Area | Public-Safe Evidence | Current Signal |",
    "| --- | --- | --- |",
    `| Change management | Policy decisions, approval gates, PR/replay packets | ${overview.approval_required_actions ?? 0} approval-gated actions |`,
    `| Logical access | Agent identity and control coverage metadata | ${agents.length} observed agents |`,
    `| Monitoring | Findings, near misses, timeline, evidence freshness | ${overview.risk_findings ?? findings.length} findings |`,
    `| Evidence integrity | Evidence refs and confidence labels | ${overview.evidence_confidence || "unknown"} |`,
    `| Incident response | Blocked and high-risk action queue | ${overview.blocked_actions ?? 0} blocked actions |`,
    "",
    "## Auditor Notes",
    "",
    "- This Community artifact is suitable for demo, design review, and public-safe audit walkthroughs.",
    "- Enterprise should attach immutable evidence, tenant-scoped trace replay, approver identity context, and scheduled delivery logs.",
    ""
  ].join("\n");
  const controlCsv = toCsv(
    ["surface", "coverage_status", "decision_count", "blocked_actions", "approval_required_actions", "warned_actions", "evidence_confidence"],
    controlCoverage.map((control) => ({
      surface: control.label || control.surface_id || "unknown",
      coverage_status: control.coverage_status || "unknown",
      decision_count: control.decision_count ?? 0,
      blocked_actions: control.blocked_actions ?? 0,
      approval_required_actions: control.approval_required_actions ?? 0,
      warned_actions: control.warned_actions ?? 0,
      evidence_confidence: control.evidence_confidence || "unknown"
    }))
  );
  const freshnessCsv = toCsv(
    ["item_id", "item_type", "freshness_status", "age_hours", "retention_status", "recommended_action"],
    evidenceFreshness.map((item) => ({
      item_id: item.item_id || item.decision_id || item.session_id || "unknown",
      item_type: item.item_type || "evidence",
      freshness_status: item.freshness_status || item.status || "unknown",
      age_hours: item.age_hours ?? "",
      retention_status: item.retention_status || "unknown",
      recommended_action: item.recommended_action || item.action || "review"
    }))
  );
  const agentCsv = toCsv(
    ["agent_id", "coverage_status", "drift_status", "session_count", "decision_count", "blocked_actions", "approval_required_actions", "warned_actions"],
    agents.map((agent) => ({
      agent_id: agent.agent_id || "unknown-agent",
      coverage_status: agent.coverage_status || "unknown",
      drift_status: agent.drift_status || "unknown",
      session_count: agent.session_count ?? 0,
      decision_count: agent.decision_count ?? 0,
      blocked_actions: agent.blocked_actions ?? 0,
      approval_required_actions: agent.approval_required_actions ?? 0,
      warned_actions: agent.warned_actions ?? 0
    }))
  );
  return {
    executive_brief_md: {
      title: "Executive Risk Brief",
      format: "Markdown",
      audience: "CSO/CISO",
      filename: "cavra-aispm-executive-risk-brief.md",
      type: "text/markdown",
      content: executiveMarkdown
    },
    board_kpi_json: {
      title: "Board KPI Pack",
      format: "JSON",
      audience: "Leadership",
      filename: "cavra-aispm-board-kpi-pack.json",
      type: "application/json",
      content: boardJson
    },
    soc2_audit_md: {
      title: "SOC 2-Style Audit Summary",
      format: "Markdown",
      audience: "Audit",
      filename: "cavra-aispm-soc2-audit-summary.md",
      type: "text/markdown",
      content: soc2Markdown
    },
    control_coverage_csv: {
      title: "Control Coverage Export",
      format: "CSV",
      audience: "Security Engineering",
      filename: "cavra-aispm-control-coverage.csv",
      type: "text/csv",
      content: controlCsv
    },
    evidence_freshness_csv: {
      title: "Evidence Freshness Export",
      format: "CSV",
      audience: "GRC / Audit",
      filename: "cavra-aispm-evidence-freshness.csv",
      type: "text/csv",
      content: freshnessCsv
    },
    agent_risk_csv: {
      title: "Agent Risk Register",
      format: "CSV",
      audience: "Platform Security",
      filename: "cavra-aispm-agent-risk-register.csv",
      type: "text/csv",
      content: agentCsv
    }
  };
}

function renderAispmReportCenter(payload) {
  currentAispmReports = buildAispmReportCatalog(payload);
  const enterpriseReports = [
    {
      report_id: "pdf_board_pack",
      title: "PDF Board Pack",
      formats: ["pdf"],
      detail: "Board-ready PDF with charts, trend lines, and sign-off"
    },
    {
      report_id: "xlsx_evidence_workbook",
      title: "XLSX Evidence Workbook",
      formats: ["xlsx"],
      detail: "Multi-sheet control, evidence, owner, and exception workbook"
    },
    {
      report_id: "scheduled_email_delivery",
      title: "Scheduled Email Delivery",
      formats: ["email"],
      detail: "SMTP, Microsoft 365, Google Workspace, SES, or SendGrid delivery"
    },
    {
      report_id: "recipient_governance",
      title: "Recipient Governance",
      formats: ["policy"],
      detail: "Allowlisted domains, RBAC, approval gates, delivery evidence"
    }
  ];
  currentAispmReportCatalogPacket = {
    schema_version: "cavra.aispm.report_catalog_readiness_packet.v1",
    product: "CAVRA",
    edition: "community",
    mode: "public_safe_report_catalog",
    generated_at: new Date().toISOString(),
    portal_panel: "apps/sandbox-ui/index.html#ai-posture",
    expected_filename: "cavra-aispm-report-catalog-packet.json",
    community_reports: Object.entries(currentAispmReports).map(([reportId, report]) => ({
      report_id: reportId,
      title: report.title,
      format: report.format,
      audience: report.audience,
      filename: report.filename,
      source: "sample_or_local_activity_metadata",
      availability: "community"
    })),
    enterprise_reports: enterpriseReports.map((report) => ({
      ...report,
      availability: "requires_cavra_enterprise"
    })),
    enterprise_delivery_boundary: {
      pdf_xlsx_docx_rendering: "requires_cavra_enterprise",
      signed_json_and_grc_packages: "requires_cavra_enterprise",
      scheduled_email_delivery: "requires_cavra_enterprise",
      recipient_allowlists_rbac_and_approval_gates: "requires_cavra_enterprise",
      delivery_audit_and_retry_evidence: "requires_cavra_enterprise"
    },
    public_safety_boundary: {
      excludes_raw_prompts: true,
      excludes_model_reasoning: true,
      excludes_recipient_addresses: true,
      excludes_smtp_credentials: true,
      excludes_customer_records: true,
      excludes_enterprise_source_code: true
    },
    verification: {
      validator: "scripts/validate-aispm-report-catalog-readiness.py",
      release_verification_markdown: "docs/release-verifications/aispm-report-catalog-readiness.md",
      release_verification_json: "docs/release-verifications/aispm-report-catalog-readiness.json"
    }
  };
  const cards = Object.entries(currentAispmReports).map(([reportId, report]) => `
    <article class="report-card">
      <span>${escapeHtml(report.format)}</span>
      <strong>${escapeHtml(report.title)}</strong>
      <p>${escapeHtml(report.audience)} · ${escapeHtml(report.filename)}</p>
      <button type="button" data-report-download="${escapeHtml(reportId)}">Download</button>
    </article>
  `).join("");
  const enterpriseCards = enterpriseReports.map(({ title, detail }) => `
    <article class="report-card is-locked">
      <span>Enterprise</span>
      <strong>${escapeHtml(title)}</strong>
      <p>${escapeHtml(detail)}</p>
      <button type="button" disabled>Requires Enterprise</button>
    </article>
  `).join("");
  el("#aispmReportCenter").innerHTML = cards + enterpriseCards;
  el("#aispmReportStatus").textContent = `${Object.keys(currentAispmReports).length} Community reports ready · ${enterpriseReports.length} Enterprise report capabilities locked · catalog packet ready.`;
}

function renderAispmReportSetupReadiness() {
  const generatedAt = new Date().toISOString();
  const setupItems = aispmReportSetupReadinessItems.map(([step, status, fields, detail]) => ({
    step,
    status,
    fields: fields.split(", "),
    detail,
    public_safe: true
  }));
  currentAispmReportSetupPacket = {
    schema_version: "cavra.aispm.report_delivery_setup_readiness_packet.v1",
    product: "CAVRA",
    edition: "community",
    mode: "public_safe_enterprise_setup_checklist",
    generated_at: generatedAt,
    portal_panel: "apps/sandbox-ui/index.html#ai-posture",
    expected_filename: "cavra-aispm-report-delivery-setup-packet.json",
    setup_items: setupItems,
    required_public_settings: [
      "CAVRA_REPORT_DELIVERY_MODE",
      "CAVRA_REPORT_FROM_ADDRESS",
      "CAVRA_REPORT_ALLOWED_RECIPIENT_DOMAINS",
      "CAVRA_REPORT_DEFAULT_TIMEZONE",
      "CAVRA_REPORT_RETENTION_DAYS"
    ],
    optional_public_settings: [
      "CAVRA_REPORT_REPLY_TO",
      "CAVRA_REPORT_BRAND_PROFILE",
      "CAVRA_REPORT_DEFAULT_SCHEDULE",
      "CAVRA_REPORT_EXTERNAL_APPROVAL_REQUIRED",
      "CAVRA_REPORT_ALLOWED_RBAC_ROLES"
    ],
    secret_reference_settings: [
      "CAVRA_REPORT_SMTP_USERNAME_REF",
      "CAVRA_REPORT_SMTP_PASSWORD_REF",
      "CAVRA_REPORT_PROVIDER_TOKEN_REF"
    ],
    validation_rules: [
      "sender-address-required",
      "recipient-domain-allowlist-required",
      "secret-values-not-accepted",
      "external-delivery-approval",
      "test-delivery-audit-required"
    ],
    enterprise_boundaries: {
      wizard_ui: "requires_cavra_enterprise",
      settings_persistence: "requires_cavra_enterprise",
      secret_resolution: "requires_cavra_enterprise",
      provider_validation: "requires_cavra_enterprise",
      test_delivery: "requires_cavra_enterprise",
      delivery_audit_and_retry_evidence: "requires_cavra_enterprise"
    },
    public_safety_boundary: {
      secret_values_allowed: false,
      recipient_addresses_included: false,
      provider_tokens_included: false,
      smtp_passwords_included: false,
      raw_report_content_included: false,
      customer_records_included: false,
      enterprise_source_code_included: false
    },
    verification: {
      validator: "scripts/validate-aispm-report-delivery-setup-readiness.py",
      release_verification_markdown: "docs/release-verifications/aispm-report-delivery-setup-readiness.md",
      release_verification_json: "docs/release-verifications/aispm-report-delivery-setup-readiness.json"
    }
  };
  el("#aispmReportSetupReadiness").innerHTML = setupItems.map((item) => `
    <article class="report-setup-card">
      <span class="severity ${item.status === "Required" ? "approved" : "controlled"}">${escapeHtml(item.status)}</span>
      <strong>${escapeHtml(item.step)}</strong>
      <p>${escapeHtml(item.detail)}</p>
      <code>${escapeHtml(item.fields.join(" · "))}</code>
    </article>
  `).join("");
  el("#aispmReportSetupStatus").textContent = `${setupItems.length} setup areas mapped · raw credentials and recipient addresses remain Enterprise-only.`;
}

function renderAispmReportOperationsReadiness() {
  const generatedAt = new Date().toISOString();
  const operationsItems = aispmReportOperationsReadinessItems.map(([area, status, schema, example, detail]) => ({
    area,
    status,
    schema,
    example,
    detail,
    availability: "requires_cavra_enterprise",
    public_safe: true
  }));
  currentAispmReportOperationsPacket = {
    schema_version: "cavra.aispm.report_operations_readiness_packet.v1",
    product: "CAVRA",
    edition: "community",
    mode: "public_safe_enterprise_report_operations_checklist",
    generated_at: generatedAt,
    portal_panel: "apps/sandbox-ui/index.html#ai-posture",
    expected_filename: "cavra-aispm-report-operations-readiness-packet.json",
    operations_items: operationsItems,
    source_contracts: operationsItems.map((item) => ({
      area: item.area,
      schema: item.schema,
      example: item.example
    })),
    enterprise_boundaries: {
      immutable_delivery_audit_store: "requires_cavra_enterprise",
      operations_dashboard_persistence: "requires_cavra_enterprise",
      retention_lifecycle_enforcement: "requires_cavra_enterprise",
      rbac_scoped_search_and_retrieval: "requires_cavra_enterprise",
      signed_export_package_manifest_service: "requires_cavra_enterprise"
    },
    public_safety_boundary: {
      raw_reports_included: false,
      provider_responses_included: false,
      recipient_addresses_included: false,
      customer_identities_included: false,
      signed_download_urls_included: false,
      tenant_telemetry_included: false,
      enterprise_source_code_included: false
    },
    verification: {
      validator: "scripts/validate-aispm-report-operations-readiness.py",
      release_verification_markdown: "docs/release-verifications/aispm-report-operations-readiness.md",
      release_verification_json: "docs/release-verifications/aispm-report-operations-readiness.json"
    }
  };
  el("#aispmReportOperationsReadiness").innerHTML = operationsItems.map((item) => `
    <article class="report-operations-card">
      <span class="severity controlled">${escapeHtml(item.status)}</span>
      <strong>${escapeHtml(item.area)}</strong>
      <p>${escapeHtml(item.detail)}</p>
      <code>${escapeHtml(item.schema)} · ${escapeHtml(item.example)}</code>
    </article>
  `).join("");
  el("#aispmReportOperationsStatus").textContent = `${operationsItems.length} operations areas mapped · report payloads, recipients, provider responses, and signed URLs remain Enterprise-only.`;
}

function renderAispmReportGovernanceReadiness() {
  const generatedAt = new Date().toISOString();
  const governanceItems = aispmReportGovernanceReadinessItems.map(([area, status, schema, example, detail]) => ({
    area,
    status,
    schema,
    example,
    detail,
    availability: "requires_cavra_enterprise",
    public_safe: true
  }));
  currentAispmReportGovernancePacket = {
    schema_version: "cavra.aispm.report_governance_readiness_packet.v1",
    product: "CAVRA",
    edition: "community",
    mode: "public_safe_enterprise_report_governance_checklist",
    generated_at: generatedAt,
    portal_panel: "apps/sandbox-ui/index.html#ai-posture",
    expected_filename: "cavra-aispm-report-governance-readiness-packet.json",
    governance_items: governanceItems,
    source_contracts: governanceItems.map((item) => ({
      area: item.area,
      schema: item.schema,
      example: item.example
    })),
    enterprise_boundaries: {
      governed_schedule_workers: "requires_cavra_enterprise",
      recipient_directory_and_policy_enforcement: "requires_cavra_enterprise",
      approval_workflow_execution: "requires_cavra_enterprise",
      exception_lifecycle_workflow: "requires_cavra_enterprise",
      authenticated_evidence_room_portal: "requires_cavra_enterprise"
    },
    public_safety_boundary: {
      recipient_addresses_included: false,
      approver_identities_included: false,
      auditor_identities_included: false,
      private_justifications_included: false,
      raw_reports_included: false,
      signed_download_urls_included: false,
      customer_records_included: false,
      enterprise_source_code_included: false
    },
    verification: {
      validator: "scripts/validate-aispm-report-governance-readiness.py",
      release_verification_markdown: "docs/release-verifications/aispm-report-governance-readiness.md",
      release_verification_json: "docs/release-verifications/aispm-report-governance-readiness.json"
    }
  };
  el("#aispmReportGovernanceReadiness").innerHTML = governanceItems.map((item) => `
    <article class="report-governance-card">
      <span class="severity controlled">${escapeHtml(item.status)}</span>
      <strong>${escapeHtml(item.area)}</strong>
      <p>${escapeHtml(item.detail)}</p>
      <code>${escapeHtml(item.schema)} · ${escapeHtml(item.example)}</code>
    </article>
  `).join("");
  el("#aispmReportGovernanceStatus").textContent = `${governanceItems.length} governance areas mapped · identities, recipient addresses, private justifications, raw reports, and signed URLs remain Enterprise-only.`;
}

function renderAispmReportAssuranceReadiness() {
  const generatedAt = new Date().toISOString();
  const assuranceItems = aispmReportAssuranceReadinessItems.map(([area, status, schema, example, detail]) => ({
    area,
    status,
    schema,
    example,
    detail,
    availability: "requires_cavra_enterprise",
    public_safe: true
  }));
  currentAispmReportAssurancePacket = {
    schema_version: "cavra.aispm.report_assurance_readiness_packet.v1",
    product: "CAVRA",
    edition: "community",
    mode: "public_safe_enterprise_report_assurance_checklist",
    generated_at: generatedAt,
    portal_panel: "apps/sandbox-ui/index.html#ai-posture",
    expected_filename: "cavra-aispm-report-assurance-readiness-packet.json",
    assurance_items: assuranceItems,
    source_contracts: assuranceItems.map((item) => ({
      area: item.area,
      schema: item.schema,
      example: item.example
    })),
    enterprise_boundaries: {
      evidence_room_access_audit_store: "requires_cavra_enterprise",
      incident_packet_builder: "requires_cavra_enterprise",
      incident_closure_workflow: "requires_cavra_enterprise",
      tenant_kpi_metrics_store: "requires_cavra_enterprise",
      alert_escalation_workflow: "requires_cavra_enterprise"
    },
    public_safety_boundary: {
      auditor_identities_included: false,
      approver_identities_included: false,
      ip_addresses_included: false,
      raw_reports_included: false,
      private_remediation_details_included: false,
      tenant_drilldown_records_included: false,
      signed_download_urls_included: false,
      customer_records_included: false,
      enterprise_source_code_included: false
    },
    verification: {
      validator: "scripts/validate-aispm-report-assurance-readiness.py",
      release_verification_markdown: "docs/release-verifications/aispm-report-assurance-readiness.md",
      release_verification_json: "docs/release-verifications/aispm-report-assurance-readiness.json"
    }
  };
  el("#aispmReportAssuranceReadiness").innerHTML = assuranceItems.map((item) => `
    <article class="report-assurance-card">
      <span class="severity controlled">${escapeHtml(item.status)}</span>
      <strong>${escapeHtml(item.area)}</strong>
      <p>${escapeHtml(item.detail)}</p>
      <code>${escapeHtml(item.schema)} · ${escapeHtml(item.example)}</code>
    </article>
  `).join("");
  el("#aispmReportAssuranceStatus").textContent = `${assuranceItems.length} assurance areas mapped · identities, IP addresses, raw reports, private remediation, drilldowns, and signed URLs remain Enterprise-only.`;
}

function renderAispmReportResponseReadiness() {
  const generatedAt = new Date().toISOString();
  const responseItems = aispmReportResponseReadinessItems.map(([area, status, schema, example, detail]) => ({
    area,
    status,
    schema,
    example,
    detail,
    availability: "requires_cavra_enterprise",
    public_safe: true
  }));
  currentAispmReportResponsePacket = {
    schema_version: "cavra.aispm.report_response_readiness_packet.v1",
    product: "CAVRA",
    edition: "community",
    mode: "public_safe_enterprise_report_response_checklist",
    generated_at: generatedAt,
    portal_panel: "apps/sandbox-ui/index.html#ai-posture",
    expected_filename: "cavra-aispm-report-response-readiness-packet.json",
    response_items: responseItems,
    source_contracts: responseItems.map((item) => ({
      area: item.area,
      schema: item.schema,
      example: item.example
    })),
    enterprise_boundaries: {
      alert_operations_dashboard_persistence: "requires_cavra_enterprise",
      alert_drilldown_authorization: "requires_cavra_enterprise",
      remediation_plan_workflow: "requires_cavra_enterprise",
      remediation_closure_workflow: "requires_cavra_enterprise",
      closure_operations_dashboard: "requires_cavra_enterprise"
    },
    public_safety_boundary: {
      assignee_identities_included: false,
      tenant_alert_records_included: false,
      raw_report_content_included: false,
      private_remediation_tasks_included: false,
      customer_records_included: false,
      signed_download_urls_included: false,
      provider_responses_included: false,
      enterprise_source_code_included: false
    },
    verification: {
      validator: "scripts/validate-aispm-report-response-readiness.py",
      release_verification_markdown: "docs/release-verifications/aispm-report-response-readiness.md",
      release_verification_json: "docs/release-verifications/aispm-report-response-readiness.json"
    }
  };
  el("#aispmReportResponseReadiness").innerHTML = responseItems.map((item) => `
    <article class="report-response-card">
      <span class="severity controlled">${escapeHtml(item.status)}</span>
      <strong>${escapeHtml(item.area)}</strong>
      <p>${escapeHtml(item.detail)}</p>
      <code>${escapeHtml(item.schema)} · ${escapeHtml(item.example)}</code>
    </article>
  `).join("");
  el("#aispmReportResponseStatus").textContent = `${responseItems.length} response areas mapped · identities, tenant alert records, raw reports, private remediation, and provider responses remain Enterprise-only.`;
}

function renderAispmReportTrialOpsReadiness() {
  const generatedAt = new Date().toISOString();
  const trialOpsItems = aispmReportTrialOpsReadinessItems.map(([area, status, schema, example, detail]) => ({
    area,
    status,
    schema,
    example,
    detail,
    availability: "requires_cavra_enterprise",
    public_safe: true
  }));
  currentAispmReportTrialOpsPacket = {
    schema_version: "cavra.aispm.report_trial_operations_readiness_packet.v1",
    product: "CAVRA",
    edition: "community",
    mode: "public_safe_enterprise_report_trial_operations_checklist",
    generated_at: generatedAt,
    portal_panel: "apps/sandbox-ui/index.html#ai-posture",
    expected_filename: "cavra-aispm-report-trial-operations-readiness-packet.json",
    trial_operations_items: trialOpsItems,
    source_contracts: trialOpsItems.map((item) => ({
      area: item.area,
      schema: item.schema,
      example: item.example
    })),
    enterprise_boundaries: {
      executive_digest_rendering: "requires_cavra_enterprise",
      digest_distribution_workflow: "requires_cavra_enterprise",
      trial_validation_runtime: "requires_cavra_enterprise",
      operator_dashboard_api: "requires_cavra_enterprise",
      operator_session_and_audit_store: "requires_cavra_enterprise"
    },
    public_safety_boundary: {
      evaluator_identities_included: false,
      operator_identities_included: false,
      recipient_addresses_included: false,
      package_tokens_included: false,
      license_keys_included: false,
      raw_prompt_or_reasoning_included: false,
      raw_report_content_included: false,
      customer_records_included: false,
      enterprise_source_code_included: false
    },
    verification: {
      validator: "scripts/validate-aispm-report-trial-operations-readiness.py",
      release_verification_markdown: "docs/release-verifications/aispm-report-trial-operations-readiness.md",
      release_verification_json: "docs/release-verifications/aispm-report-trial-operations-readiness.json"
    }
  };
  el("#aispmReportTrialOpsReadiness").innerHTML = trialOpsItems.map((item) => `
    <article class="report-trialops-card">
      <span class="severity controlled">${escapeHtml(item.status)}</span>
      <strong>${escapeHtml(item.area)}</strong>
      <p>${escapeHtml(item.detail)}</p>
      <code>${escapeHtml(item.schema)} · ${escapeHtml(item.example)}</code>
    </article>
  `).join("");
  el("#aispmReportTrialOpsStatus").textContent = `${trialOpsItems.length} trial operations areas mapped · evaluator identities, package tokens, license keys, raw content, and Enterprise source remain private.`;
}

function renderAispmTrialReadinessChecklist() {
  const generatedAt = new Date().toISOString();
  const checklist = aispmTrialReadinessItems.map(([label, status, detail, href]) => ({
    label,
    status,
    detail,
    href,
    public_safe: true
  }));
  currentAispmTrialReadinessPacket = {
    schema_version: "cavra.aispm.enterprise_trial_readiness_packet.v1",
    product: "CAVRA",
    edition: "community",
    mode: "public_safe_export",
    generated_at: generatedAt,
    audience: ["CSO", "CISO", "Security Engineering", "Procurement", "Trial Evaluator"],
    summary: {
      checklist_items: checklist.length,
      ready_items: checklist.filter((item) => ["Ready", "Live", "Controlled", "Documented", "Verified"].includes(item.status)).length,
      locked_items: checklist.filter((item) => item.status === "Locked").length,
      external_trial_domain: "https://cavra-trial.mind-ops.cloud/",
      public_safety_boundary: "No Enterprise source code, secrets, customer data, license signing keys, or private package credentials are included."
    },
    checklist,
    enterprise_boundary: {
      private_package_access_grants: "requires_cavra_enterprise_private_service",
      license_issuance: "requires_cavra_enterprise_private_service",
      evaluator_email_delivery: "requires_cavra_enterprise_private_service",
      hosted_telemetry: "requires_cavra_enterprise_or_saas"
    }
  };
  currentAispmTrialReadinessMarkdown = [
    "# CAVRA AISPM Enterprise Trial Readiness Summary",
    "",
    `Generated: ${generatedAt}`,
    "",
    "## Summary",
    "",
    `- Checklist items: ${currentAispmTrialReadinessPacket.summary.checklist_items}`,
    `- Ready or controlled items: ${currentAispmTrialReadinessPacket.summary.ready_items}`,
    `- Enterprise-locked automation items: ${currentAispmTrialReadinessPacket.summary.locked_items}`,
    `- Trial domain: ${currentAispmTrialReadinessPacket.summary.external_trial_domain}`,
    "",
    "## Checklist",
    "",
    ...checklist.map((item) => `- **${item.label}**: ${item.status} - ${item.detail} (${item.href})`),
    "",
    "## Public Safety Boundary",
    "",
    currentAispmTrialReadinessPacket.summary.public_safety_boundary
  ].join("\n");
  el("#aispmTrialReadinessChecklist").innerHTML = aispmTrialReadinessItems.map(([label, status, detail, href]) => {
    const statusClass = status.toLowerCase().replaceAll(" ", "-");
    return `
      <article class="trial-readiness-item">
        <div>
          <span class="severity ${escapeHtml(statusClass)}">${escapeHtml(status)}</span>
          <strong>${escapeHtml(label)}</strong>
          <p>${escapeHtml(detail)}</p>
        </div>
        <a href="${escapeHtml(href)}" target="_blank" rel="noreferrer">Open</a>
      </article>
    `;
  }).join("");
  el("#aispmTrialReadinessStatus").textContent = `${checklist.length} readiness items prepared for public-safe CSO/CISO export.`;
}

function renderAispmEvaluatorHandoff() {
  el("#aispmEvaluatorHandoff").innerHTML = aispmEvaluatorHandoffItems.map(([label, value, detail]) => `
    <article class="evaluator-handoff-card">
      <span>${escapeHtml(label)}</span>
      <strong>${escapeHtml(value)}</strong>
      <p>${escapeHtml(detail)}</p>
    </article>
  `).join("");
}

function renderAispmTrialJourney() {
  el("#aispmTrialJourney").innerHTML = aispmTrialJourneySteps.map(([step, title, detail, evidenceType]) => `
    <article class="trial-journey-step">
      <span>${escapeHtml(step)}</span>
      <div>
        <strong>${escapeHtml(title)}</strong>
        <p>${escapeHtml(detail)}</p>
        <small>Evidence signal: ${escapeHtml(evidenceType)}</small>
      </div>
    </article>
  `).join("");
}

function renderAispmTrialCloseoutEvidence() {
  el("#aispmTrialCloseoutEvidence").innerHTML = aispmTrialCloseoutEvidenceItems.map(([label, status, detail, evidenceType]) => `
    <article class="trial-closeout-card">
      <span class="severity controlled">${escapeHtml(status)}</span>
      <strong>${escapeHtml(label)}</strong>
      <p>${escapeHtml(detail)}</p>
      <small>Evidence signal: ${escapeHtml(evidenceType)}</small>
    </article>
  `).join("");
}

function renderAispmTrialFeedbackIntake() {
  el("#aispmTrialFeedbackIntake").innerHTML = aispmTrialFeedbackCategories.map(([label, detail, fieldId]) => `
    <article class="trial-feedback-card">
      <span>${escapeHtml(fieldId)}</span>
      <strong>${escapeHtml(label)}</strong>
      <p>${escapeHtml(detail)}</p>
      <small>Enterprise capture: governed tenant feedback record</small>
    </article>
  `).join("");
}

function buildAispmTrialReviewPacket(outcomeCards, generatedAt) {
  return {
    schema_version: "cavra.aispm.trial_review_packet.v1",
    product: "CAVRA",
    edition: "community",
    mode: "public_safe_export",
    generated_at: generatedAt,
    audience: ["CSO", "CISO", "Security Engineering", "Procurement", "Trial Evaluator"],
    public_safety_boundary: "No Enterprise source code, secrets, customer data, private license keys, package credentials, or tenant records are included.",
    readiness: currentAispmTrialReadinessPacket || null,
    evaluator_handoff: aispmEvaluatorHandoffItems.map(([label, value, detail]) => ({ label, value, detail })),
    evaluation_journey: aispmTrialJourneySteps.map(([step, title, detail, evidence_signal]) => ({ step, title, detail, evidence_signal })),
    closeout_evidence: aispmTrialCloseoutEvidenceItems.map(([label, status, detail, evidence_signal]) => ({ label, status, detail, evidence_signal })),
    feedback_intake: aispmTrialFeedbackCategories.map(([label, detail, field_id]) => ({ label, detail, field_id, enterprise_capture: "governed_tenant_feedback_record" })),
    outcome_summary: outcomeCards.map(([label, value, detail]) => ({ label, value, detail })),
    enterprise_boundary: {
      private_package_access_grants: "requires_cavra_enterprise_private_service",
      license_issuance: "requires_cavra_enterprise_private_service",
      evaluator_email_delivery: "requires_cavra_enterprise_private_service",
      tenant_feedback_storage: "requires_cavra_enterprise_or_saas",
      hosted_telemetry: "requires_cavra_enterprise_or_saas"
    }
  };
}

function renderAispmTrialOutcomeSummary() {
  const generatedAt = new Date().toISOString();
  const readinessReady = aispmTrialReadinessItems.filter((item) => item[1] !== "Locked").length;
  const outcomeCards = [
    [
      "Readiness",
      `${readinessReady}/${aispmTrialReadinessItems.length}`,
      "Lab notebook, portal, approval, revocation, release evidence, and Enterprise boundary are visible."
    ],
    [
      "Evaluator Handoff",
      `${aispmEvaluatorHandoffItems.length} signals`,
      "Approved evaluator receives portal, package reference, license boundary, notebook, support, and closeout path."
    ],
    [
      "Journey Coverage",
      `${aispmTrialJourneySteps.length} milestones`,
      "Request, approval, pull, license validation, scenario execution, evidence review, and closeout are traceable."
    ],
    [
      "Closeout Evidence",
      `${aispmTrialCloseoutEvidenceItems.length} controls`,
      "Expiry, revocation, package removal, blocked runtime, evidence archive, and feedback collection are required."
    ],
    [
      "Feedback Intake",
      `${aispmTrialFeedbackCategories.length} categories`,
      "Setup, policy, dashboard, reports, integrations, procurement, and go/no-go feedback are modeled."
    ],
    [
      "CSO/CISO Outcome",
      "Go candidate",
      "Public-safe evidence is ready for a controlled evaluator trial; Enterprise automation remains private."
    ]
  ];
  el("#aispmTrialOutcomeSummary").innerHTML = outcomeCards.map(([label, value, detail]) => `
    <article class="trial-outcome-card">
      <span>${escapeHtml(label)}</span>
      <strong>${escapeHtml(value)}</strong>
      <p>${escapeHtml(detail)}</p>
    </article>
  `).join("");
  currentAispmTrialReviewPacket = buildAispmTrialReviewPacket(outcomeCards, generatedAt);
  el("#aispmTrialReviewPacketStatus").textContent = `Trial review packet ready with ${outcomeCards.length} outcome sections.`;
}

function renderAispmTrialReviewPacketIntegrity() {
  const packet = currentAispmTrialReviewPacket || {};
  const excludedFields = [
    "license_signing_key",
    "private_registry_credentials",
    "customer_records",
    "tenant_feedback_records",
    "enterprise_source_code",
    "hosted_telemetry_events"
  ];
  const integrityCards = [
    ["Schema", packet.schema_version || "not_generated", "Expected public-safe review packet contract."],
    ["Generated", packet.generated_at || "not_generated", "Timestamp is generated locally when the dashboard renders."],
    ["Filename", "cavra-aispm-trial-review-packet.json", "Expected downloadable review artifact name."],
    ["Boundary", "Public safe", packet.public_safety_boundary || "No private fields are included."],
    ["Excluded Fields", `${excludedFields.length}`, excludedFields.join(", ")],
    ["Enterprise Boundary", "Private", "Access grants, license issuance, email delivery, tenant feedback, and telemetry require Enterprise or SaaS."]
  ];
  el("#aispmTrialReviewPacketIntegrity").innerHTML = integrityCards.map(([label, value, detail]) => `
    <article class="trial-integrity-card">
      <span>${escapeHtml(label)}</span>
      <strong>${escapeHtml(value)}</strong>
      <p>${escapeHtml(detail)}</p>
    </article>
  `).join("");
}

function renderAispmTrialProcurementReadiness() {
  el("#aispmTrialProcurementReadiness").innerHTML = aispmTrialProcurementAreas.map(([label, detail, reviewArea]) => `
    <article class="procurement-readiness-card">
      <span>${escapeHtml(reviewArea)}</span>
      <strong>${escapeHtml(label)}</strong>
      <p>${escapeHtml(detail)}</p>
      <small>Review source: AISPM Trial review packet</small>
    </article>
  `).join("");
}

function renderAispmTrialPilotScope() {
  const generatedAt = new Date().toISOString();
  const scope = aispmTrialPilotScopeItems.map(([label, detail, example]) => ({
    label,
    detail,
    example,
    public_safe: true
  }));
  currentAispmTrialPilotScopePacket = {
    schema_version: "cavra.aispm.trial_pilot_scope_packet.v1",
    product: "CAVRA",
    edition: "community",
    mode: "public_safe_export",
    generated_at: generatedAt,
    audience: ["CSO", "CISO", "Security Engineering", "Platform Engineering", "Procurement"],
    source: "AISPM Trial Pilot Scope Builder",
    scope,
    approval_ticket_use: "Attach this packet to an internal pilot approval ticket after replacing sample values with organization-approved scope.",
    public_safety_boundary: "No customer records, private registry credentials, license keys, Enterprise source code, or tenant telemetry are included.",
    enterprise_boundary: {
      pilot_workflow_write_back: "requires_cavra_enterprise_or_saas",
      tenant_owner_assignment: "requires_cavra_enterprise_or_saas",
      private_connector_configuration: "requires_cavra_enterprise_private_service"
    }
  };
  el("#aispmTrialPilotScope").innerHTML = scope.map(({ label, detail, example }) => `
    <article class="pilot-scope-card">
      <span>${escapeHtml(label)}</span>
      <strong>${escapeHtml(example)}</strong>
      <p>${escapeHtml(detail)}</p>
    </article>
  `).join("");
  el("#aispmTrialPilotScopeStatus").textContent = `${scope.length} pilot scope fields prepared for public-safe export.`;
}

function renderAispmPilotApprovalChecklist() {
  const generatedAt = new Date().toISOString();
  const approvalGates = aispmPilotApprovalChecklistItems.map(([label, detail, gateId]) => ({
    gate_id: gateId,
    label,
    detail,
    required_before_pilot_start: true,
    public_safe: true
  }));
  currentAispmPilotApprovalPacket = {
    schema_version: "cavra.aispm.pilot_approval_packet.v1",
    product: "CAVRA",
    edition: "community",
    mode: "public_safe_export",
    generated_at: generatedAt,
    audience: ["CSO", "CISO", "Security Engineering", "Platform Engineering", "Procurement"],
    source: "AISPM Pilot Approval Checklist",
    linked_scope_packet_schema: currentAispmTrialPilotScopePacket?.schema_version || "cavra.aispm.trial_pilot_scope_packet.v1",
    linked_scope_packet_filename: "cavra-aispm-trial-pilot-scope-packet.json",
    approval_gates: approvalGates,
    approval_record_use: "Attach this packet with the pilot scope packet to the internal production-pilot approval record.",
    public_safety_boundary: "No customer records, private registry credentials, license keys, Enterprise source code, tenant telemetry, or signed approvals are included.",
    enterprise_boundary: {
      signed_approval_workflow: "requires_cavra_enterprise_or_saas",
      workflow_write_back: "requires_cavra_enterprise_or_saas",
      identity_bound_approvals: "requires_enterprise_identity_integration"
    }
  };
  el("#aispmPilotApprovalChecklist").innerHTML = approvalGates.map(({ label, detail, gate_id }) => `
    <article class="pilot-approval-card">
      <span class="severity controlled">Gate</span>
      <strong>${escapeHtml(label)}</strong>
      <p>${escapeHtml(detail)}</p>
      <small>${escapeHtml(gate_id)}</small>
    </article>
  `).join("");
  el("#aispmPilotApprovalStatus").textContent = `${approvalGates.length} approval gates prepared for public-safe export.`;
}

function renderAispmPilotLaunchReadiness() {
  const generatedAt = new Date().toISOString();
  const readyCount = aispmPilotLaunchReadinessItems.filter(([, status]) => status === "Ready").length;
  const readiness = aispmPilotLaunchReadinessItems.map(([label, status, detail, source]) => ({
    label,
    status,
    detail,
    source,
    public_safe: true
  }));
  currentAispmPilotLaunchDecisionPacket = {
    schema_version: "cavra.aispm.pilot_launch_decision_packet.v1",
    product: "CAVRA",
    edition: "community",
    mode: "public_safe_export",
    generated_at: generatedAt,
    audience: ["CSO", "CISO", "Security Engineering", "Platform Engineering", "Procurement"],
    source: "AISPM Pilot Launch Readiness Summary",
    launch_decision_status: "launch_candidate_pending_enterprise_signed_approval",
    readiness,
    source_artifacts: [
      "cavra-aispm-trial-pilot-scope-packet.json",
      "cavra-aispm-pilot-approval-packet.json",
      "cavra-aispm-trial-review-packet.json",
      "CSO Report Center"
    ],
    decision_record_use: "Attach this packet to the CSO/CISO production-pilot launch approval record after confirming Enterprise signed approval workflow.",
    public_safety_boundary: "No signed approvals, customer records, private registry credentials, license keys, Enterprise source code, tenant telemetry, or workflow write-back state are included.",
    enterprise_boundary: {
      signed_launch_approval: "requires_cavra_enterprise_or_saas",
      identity_bound_decision_evidence: "requires_enterprise_identity_integration",
      approval_workflow_write_back: "requires_cavra_enterprise_or_saas",
      tenant_live_readiness_state: "requires_enterprise_tenant_store"
    }
  };
  el("#aispmPilotLaunchReadiness").innerHTML = readiness.map(({ label, status, detail, source }) => {
    const severity = status === "Ready" ? "approved" : status === "Candidate" ? "controlled" : "medium";
    return `
      <article class="pilot-launch-card">
        <span class="severity ${severity}">${escapeHtml(status)}</span>
        <strong>${escapeHtml(label)}</strong>
        <p>${escapeHtml(detail)}</p>
        <small>${escapeHtml(source)}</small>
      </article>
    `;
  }).join("");
  el("#aispmPilotLaunchStatus").textContent = `${readyCount} of ${readiness.length} launch readiness areas are ready in the public-safe model; decision packet is ready for CSO/CISO approval records.`;
}

function renderAispmPilotEvidenceRoom() {
  const generatedAt = new Date().toISOString();
  const reviewerCatalog = aispmPilotEvidenceRoomItems.map(([role, artifacts, publicReference, enterpriseBoundary]) => ({
    role,
    artifacts,
    public_reference: publicReference,
    enterprise_boundary: enterpriseBoundary,
    public_safe: true
  }));
  currentAispmPilotEvidenceRoomPacket = {
    schema_version: "cavra.aispm.pilot_evidence_room_packet.v1",
    product: "CAVRA",
    edition: "community",
    mode: "public_safe_export",
    generated_at: generatedAt,
    audience: ["CSO", "CISO", "Security Engineering", "Platform Engineering", "Procurement", "Auditor", "Operator"],
    source: "Production Pilot Evidence Room",
    reviewer_catalog: reviewerCatalog,
    source_artifacts: [
      "cavra-aispm-pilot-launch-decision-packet.json",
      "cavra-aispm-pilot-approval-packet.json",
      "cavra-aispm-trial-pilot-scope-packet.json",
      "cavra-aispm-trial-review-packet.json",
      "CSO Report Center"
    ],
    evidence_room_use: "Attach this packet to reviewer handoff records as a public-safe index of pilot evidence artifacts.",
    public_safety_boundary: "No customer records, private registry credentials, license keys, Enterprise source code, tenant telemetry, signed evidence, access grants, or reviewer activity logs are included.",
    enterprise_boundary: {
      authenticated_evidence_room_access: "requires_cavra_enterprise_or_saas",
      signed_reviewer_activity_logs: "requires_cavra_enterprise_or_saas",
      evidence_retention_policy_enforcement: "requires_enterprise_evidence_store",
      tenant_artifact_permissions: "requires_enterprise_identity_integration"
    },
    enterprise_boundary_summary: "Enterprise is required for authenticated evidence-room access, retention, signed activity logs, and tenant artifact permissions."
  };
  el("#aispmPilotEvidenceRoom").innerHTML = reviewerCatalog.map(({ role, artifacts, public_reference, enterprise_boundary }) => `
    <article class="pilot-evidence-room-card">
      <span class="severity controlled">${escapeHtml(role)}</span>
      <strong>${escapeHtml(public_reference)}</strong>
      <p>${escapeHtml(artifacts)}</p>
      <small>${escapeHtml(enterprise_boundary)}</small>
    </article>
  `).join("");
  el("#aispmPilotEvidenceRoomStatus").textContent = `${reviewerCatalog.length} reviewer evidence catalogs prepared for public-safe export.`;
}

function renderAispmEvidenceReviewerChecklist() {
  const generatedAt = new Date().toISOString();
  const acceptanceCriteria = aispmEvidenceReviewerChecklistItems.map(([role, criterion, acceptanceSignal, enterpriseBoundary]) => ({
    role,
    criterion,
    acceptance_signal: acceptanceSignal,
    enterprise_boundary: enterpriseBoundary,
    public_safe: true
  }));
  currentAispmEvidenceReviewerChecklistPacket = {
    schema_version: "cavra.aispm.evidence_reviewer_checklist_packet.v1",
    product: "CAVRA",
    edition: "community",
    mode: "public_safe_export",
    generated_at: generatedAt,
    audience: ["CSO", "CISO", "Security Engineering", "Platform Engineering", "Procurement", "Auditor", "Operator"],
    source: "Evidence Room Reviewer Checklist",
    acceptance_criteria: acceptanceCriteria,
    source_artifacts: [
      "cavra-aispm-pilot-evidence-room-packet.json",
      "cavra-aispm-pilot-launch-decision-packet.json",
      "cavra-aispm-pilot-approval-packet.json",
      "cavra-aispm-trial-review-packet.json"
    ],
    checklist_use: "Attach this packet to launch review records as a public-safe checklist of reviewer acceptance criteria.",
    public_safety_boundary: "No signed decisions, reviewer identity records, customer records, private policy context, Enterprise source code, tenant telemetry, or workflow write-back state are included.",
    enterprise_boundary: {
      signed_reviewer_acceptance: "requires_cavra_enterprise_or_saas",
      identity_bound_reviewer_records: "requires_enterprise_identity_integration",
      checklist_workflow_write_back: "requires_cavra_enterprise_or_saas",
      tenant_exception_records: "requires_enterprise_tenant_store"
    },
    enterprise_boundary_summary: "Enterprise is required for signed reviewer acceptance, identity-bound reviewer records, workflow write-back, and tenant exception records."
  };
  el("#aispmEvidenceReviewerChecklist").innerHTML = acceptanceCriteria.map(({ role, criterion, acceptance_signal, enterprise_boundary }) => `
    <article class="evidence-reviewer-checklist-card">
      <span class="severity approved">${escapeHtml(role)}</span>
      <strong>${escapeHtml(acceptance_signal)}</strong>
      <p>${escapeHtml(criterion)}</p>
      <small>${escapeHtml(enterprise_boundary)}</small>
    </article>
  `).join("");
  el("#aispmEvidenceReviewerChecklistStatus").textContent = `${acceptanceCriteria.length} reviewer roles have public-safe pre-pilot acceptance criteria prepared for export.`;
}

function renderAispmPilotExceptionRegister() {
  const generatedAt = new Date().toISOString();
  const exceptions = aispmPilotExceptionRegisterItems.map(([exceptionId, riskArea, status, owner, summary, expiry, enterpriseBoundary]) => ({
    exception_id: exceptionId,
    risk_area: riskArea,
    status,
    owner,
    summary,
    expiry_expectation: expiry,
    enterprise_boundary: enterpriseBoundary,
    public_safe: true
  }));
  const openCount = exceptions.filter(({ status }) => status === "Open").length;
  currentAispmPilotExceptionRegisterPacket = {
    schema_version: "cavra.aispm.pilot_exception_register_packet.v1",
    product: "CAVRA",
    edition: "community",
    mode: "public_safe_export",
    generated_at: generatedAt,
    audience: ["CSO", "CISO", "Security Engineering", "Platform Engineering", "Procurement", "Auditor", "Operator"],
    source: "Pilot Exception Register",
    exceptions,
    source_artifacts: [
      "cavra-aispm-evidence-reviewer-checklist-packet.json",
      "cavra-aispm-pilot-evidence-room-packet.json",
      "cavra-aispm-pilot-launch-decision-packet.json",
      "cavra-aispm-trial-review-packet.json"
    ],
    register_use: "Attach this packet to launch approval records as a public-safe register of unresolved risks and accepted exceptions.",
    public_safety_boundary: "No signed exception acceptance, customer records, reviewer identity records, private policy context, Enterprise source code, tenant telemetry, or exception workflow state are included.",
    enterprise_boundary: {
      signed_exception_acceptance: "requires_cavra_enterprise_or_saas",
      exception_owner_assignment: "requires_enterprise_identity_integration",
      exception_expiry_enforcement: "requires_cavra_enterprise_or_saas",
      exception_closure_workflow: "requires_cavra_enterprise_or_saas",
      tenant_exception_history: "requires_enterprise_tenant_store"
    },
    enterprise_boundary_summary: "Enterprise is required for signed exception acceptance, owner assignment, expiry enforcement, closure workflow, and tenant exception history."
  };
  el("#aispmPilotExceptionRegister").innerHTML = exceptions.map(({ exception_id, risk_area, status, owner, summary, expiry_expectation, enterprise_boundary }) => {
    const severity = status === "Open" ? "high" : status === "Monitor" ? "medium" : "controlled";
    return `
      <article class="pilot-exception-card">
        <div class="exception-card-heading">
          <span class="severity ${severity}">${escapeHtml(status)}</span>
          <code>${escapeHtml(exception_id)}</code>
        </div>
        <strong>${escapeHtml(risk_area)}</strong>
        <p>${escapeHtml(summary)}</p>
        <small>${escapeHtml(owner)} · ${escapeHtml(expiry_expectation)} · ${escapeHtml(enterprise_boundary)}</small>
      </article>
    `;
  }).join("");
  el("#aispmPilotExceptionStatus").textContent = `${openCount} open exception areas require owner review before production pilot launch; exception register packet is ready for public-safe export.`;
}

function renderAispmPilotRiskAcceptanceSummary() {
  const generatedAt = new Date().toISOString();
  const exceptions = aispmPilotExceptionRegisterItems.map(([exceptionId, riskArea, status, owner, summary, expiry, enterpriseBoundary]) => ({
    exception_id: exceptionId,
    risk_area: riskArea,
    status,
    owner,
    summary,
    expiry_expectation: expiry,
    enterprise_boundary: enterpriseBoundary
  }));
  const openExceptions = exceptions.filter(({ status }) => status === "Open");
  const acceptedRisks = exceptions.filter(({ status }) => status.startsWith("Accepted"));
  const monitoredRisks = exceptions.filter(({ status }) => status === "Monitor");
  const ownerSet = [...new Set(exceptions.map(({ owner }) => owner))];
  const launchBlockers = openExceptions.map(({ risk_area, owner }) => `${risk_area} (${owner})`);
  currentAispmPilotRiskAcceptancePacket = {
    schema_version: "cavra.aispm.pilot_risk_acceptance_packet.v1",
    product: "CAVRA",
    edition: "community",
    mode: "public_safe_export",
    generated_at: generatedAt,
    audience: ["CSO", "CISO", "Security Engineering", "Platform Engineering", "Procurement", "Auditor", "Operator"],
    source: "Pilot Risk Acceptance Summary",
    summary: {
      open_exceptions: openExceptions.length,
      accepted_risks: acceptedRisks.length,
      monitored_risks: monitoredRisks.length,
      accountable_owners: ownerSet,
      launch_blocking_items: launchBlockers,
      launch_disposition: openExceptions.length ? "action_required_before_pilot_launch" : "public_safe_model_clear"
    },
    source_artifacts: [
      "cavra-aispm-pilot-exception-register-packet.json",
      "cavra-aispm-evidence-reviewer-checklist-packet.json",
      "cavra-aispm-pilot-launch-decision-packet.json",
      "cavra-aispm-pilot-evidence-room-packet.json"
    ],
    risk_acceptance_use: "Attach this packet to CSO/CISO launch approval records as a public-safe risk acceptance summary.",
    public_safety_boundary: "No signed risk acceptance, reviewer identity records, customer records, private policy context, Enterprise source code, tenant telemetry, or workflow write-back state are included.",
    enterprise_boundary: {
      signed_risk_acceptance: "requires_cavra_enterprise_or_saas",
      identity_bound_risk_owner_records: "requires_enterprise_identity_integration",
      exception_expiry_enforcement: "requires_cavra_enterprise_or_saas",
      risk_acceptance_workflow_write_back: "requires_cavra_enterprise_or_saas",
      tenant_risk_acceptance_history: "requires_enterprise_tenant_store"
    },
    enterprise_boundary_summary: "Enterprise is required for signed risk acceptance, identity-bound risk owner records, exception expiry enforcement, workflow write-back, and tenant risk acceptance history."
  };
  const summaryCards = [
    ["Open Exceptions", String(openExceptions.length), launchBlockers.join(", ") || "None"],
    ["Accepted Risks", String(acceptedRisks.length), acceptedRisks.map(({ risk_area }) => risk_area).join(", ") || "None"],
    ["Monitored Risks", String(monitoredRisks.length), monitoredRisks.map(({ risk_area }) => risk_area).join(", ") || "None"],
    ["Accountable Owners", String(ownerSet.length), ownerSet.join(", ")],
    ["Launch Blocking", openExceptions.length ? "Action Required" : "Clear", openExceptions.length ? "Resolve or accept open exceptions before pilot launch." : "No open exception blockers in public-safe model."],
    ["Enterprise Boundary", "Required", "Signed risk acceptance, exception expiry enforcement, and tenant exception history require CAVRA Enterprise or SaaS."]
  ];
  el("#aispmPilotRiskAcceptanceSummary").innerHTML = summaryCards.map(([label, value, detail]) => {
    const severity = label === "Launch Blocking" && value === "Action Required" ? "high" : label === "Enterprise Boundary" ? "controlled" : "approved";
    return `
      <article class="risk-acceptance-card">
        <span class="severity ${severity}">${escapeHtml(label)}</span>
        <strong>${escapeHtml(value)}</strong>
        <p>${escapeHtml(detail)}</p>
      </article>
    `;
  }).join("");
  el("#aispmPilotRiskAcceptanceStatus").textContent = `${openExceptions.length} launch-blocking exception areas need CSO/CISO disposition; signed risk acceptance remains Enterprise-only.`;
}

function renderAispmPilotLaunchBoardPack() {
  const generatedAt = new Date().toISOString();
  const boardPackItems = aispmPilotLaunchBoardPackItems.map(([label, artifact, detail, enterpriseBoundary]) => ({
    label,
    artifact,
    detail,
    enterprise_boundary: enterpriseBoundary,
    public_safe: true
  }));
  const artifactManifest = [
    {
      artifact_id: "launch_decision",
      filename: "cavra-aispm-pilot-launch-decision-packet.json",
      schema_version: currentAispmPilotLaunchDecisionPacket?.schema_version || "cavra.aispm.pilot_launch_decision_packet.v1",
      source_panel: "AISPM Pilot Launch Readiness Summary",
      freshness_status: currentAispmPilotLaunchDecisionPacket ? "current_session" : "expected",
      required_for: "CSO/CISO launch decision review"
    },
    {
      artifact_id: "evidence_room",
      filename: "cavra-aispm-pilot-evidence-room-packet.json",
      schema_version: currentAispmPilotEvidenceRoomPacket?.schema_version || "cavra.aispm.pilot_evidence_room_packet.v1",
      source_panel: "Production Pilot Evidence Room",
      freshness_status: currentAispmPilotEvidenceRoomPacket ? "current_session" : "expected",
      required_for: "Role-based reviewer evidence catalog"
    },
    {
      artifact_id: "risk_acceptance",
      filename: "cavra-aispm-pilot-risk-acceptance-packet.json",
      schema_version: currentAispmPilotRiskAcceptancePacket?.schema_version || "cavra.aispm.pilot_risk_acceptance_packet.v1",
      source_panel: "Pilot Risk Acceptance Summary",
      freshness_status: currentAispmPilotRiskAcceptancePacket ? "current_session" : "expected",
      required_for: "Residual risk and launch-blocker disposition"
    },
    {
      artifact_id: "exception_register",
      filename: "cavra-aispm-pilot-exception-register-packet.json",
      schema_version: currentAispmPilotExceptionRegisterPacket?.schema_version || "cavra.aispm.pilot_exception_register_packet.v1",
      source_panel: "Pilot Exception Register",
      freshness_status: currentAispmPilotExceptionRegisterPacket ? "current_session" : "expected",
      required_for: "Exception owner and expiry review"
    },
    {
      artifact_id: "reviewer_checklist",
      filename: "cavra-aispm-evidence-reviewer-checklist-packet.json",
      schema_version: currentAispmEvidenceReviewerChecklistPacket?.schema_version || "cavra.aispm.evidence_reviewer_checklist_packet.v1",
      source_panel: "Evidence Room Reviewer Checklist",
      freshness_status: currentAispmEvidenceReviewerChecklistPacket ? "current_session" : "expected",
      required_for: "Role-specific acceptance criteria"
    },
    {
      artifact_id: "executive_reports",
      filename: "CSO Report Center",
      schema_version: "cavra.aispm.community_report_center.v1",
      source_panel: "CSO Report Center",
      freshness_status: Object.keys(currentAispmReports || {}).length ? "current_session" : "expected",
      required_for: "Executive risk brief, board KPI pack, audit summary, control, evidence, and agent-risk exports"
    }
  ];
  const generatedArtifacts = artifactManifest.filter(({ freshness_status }) => freshness_status === "current_session").length;
  const missingPublicArtifacts = artifactManifest
    .filter(({ freshness_status }) => freshness_status !== "current_session")
    .map(({ artifact_id, filename }) => ({ artifact_id, filename }));
  currentAispmPilotLaunchBoardPackPacket = {
    schema_version: "cavra.aispm.pilot_launch_board_pack_packet.v1",
    product: "CAVRA",
    edition: "community",
    mode: "public_safe_export",
    generated_at: generatedAt,
    audience: ["Board", "CSO", "CISO", "Security Engineering", "Platform Engineering", "Procurement", "Auditor"],
    source: "Pilot Launch Board Pack",
    packet_label: "Pilot Launch Board Pack Packet",
    launch_disposition: "board_ready_public_safe_packet_pending_enterprise_signed_approval",
    board_pack_items: boardPackItems,
    artifact_manifest: artifactManifest,
    freshness_gate: {
      status: missingPublicArtifacts.length ? "action_required" : "pass",
      generated_artifacts: generatedArtifacts,
      expected_artifacts: artifactManifest.length,
      validator: "scripts/validate-aispm-launch-artifacts.py",
      required_docs: [
        "docs/ai-security-posture-dashboard-roadmap.md",
        "docs/sandbox-portal-redesign.md",
        "docs/sandbox-portal-smoke-validation.md",
        "docs/wiki/AISPM-Dashboard-Roadmap.md",
        "docs/wiki/CAVRA-Developer-Portal-Redesign.md",
        "docs/wiki/CAVRA-Developer-Portal-Smoke-Validation.md"
      ],
      missing_public_artifacts: missingPublicArtifacts
    },
    integrity: {
      public_safety_status: "pass",
      manifest_artifacts: artifactManifest.length,
      source_packet_count: 5,
      report_artifact_count: Object.keys(currentAispmReports || {}).length,
      excluded_private_fields: [
        "signed_board_approval",
        "board_minutes",
        "recipient_email_addresses",
        "private_telemetry_events",
        "customer_identity_records",
        "license_keys",
        "enterprise_source_code"
      ],
      package_use: "Attach this packet to board, CSO/CISO, procurement, or pilot launch records as a public-safe artifact index and freshness gate."
    },
    public_safety_boundary: "No signed approvals, board minutes, email recipients, private telemetry, customer identity records, license keys, Enterprise source code, or delivery workflow state are included.",
    enterprise_boundary: {
      signed_board_approval: "requires_cavra_enterprise_or_saas",
      board_minutes_and_attestation: "requires_cavra_enterprise_or_saas",
      pdf_generation_and_delivery: "requires_cavra_enterprise_report_service",
      recipient_allowlists_and_email_audit: "requires_cavra_enterprise_report_service",
      tenant_artifact_retention: "requires_enterprise_evidence_store"
    },
    enterprise_boundary_summary: "Enterprise is required for signed board approval, minutes, PDF generation, scheduled delivery, recipient controls, and tenant artifact retention."
  };
  el("#aispmPilotLaunchBoardPack").innerHTML = aispmPilotLaunchBoardPackItems.map(([label, artifact, detail, enterpriseBoundary]) => `
    <article class="board-pack-card">
      <span class="severity approved">${escapeHtml(label)}</span>
      <strong>${escapeHtml(artifact)}</strong>
      <p>${escapeHtml(detail)}</p>
      <small>${escapeHtml(enterpriseBoundary)}</small>
    </article>
  `).join("");
  const manifestCards = [
    ["Freshness Gate", currentAispmPilotLaunchBoardPackPacket.freshness_gate.status, `${generatedArtifacts}/${artifactManifest.length} artifacts generated in this session`],
    ["Manifest", String(artifactManifest.length), "Launch decision, evidence room, risk, exceptions, checklist, and reports"],
    ["Integrity", "Public safe", "Private approvals, minutes, recipients, telemetry, license data, and source code excluded"],
    ["Enterprise Boundary", "Required", "Signed board approval, PDF board pack, email delivery, and retention remain Enterprise-only"]
  ];
  el("#aispmPilotLaunchBoardPackManifest").innerHTML = manifestCards.map(([label, value, detail]) => {
    const severity = value === "action_required" ? "medium" : "approved";
    return `
      <article class="board-pack-manifest-card">
        <span class="severity ${severity}">${escapeHtml(label)}</span>
        <strong>${escapeHtml(value)}</strong>
        <p>${escapeHtml(detail)}</p>
      </article>
    `;
  }).join("");
  el("#aispmPilotLaunchBoardPackStatus").textContent = `${aispmPilotLaunchBoardPackItems.length} board pack artifacts prepared; ${generatedArtifacts}/${artifactManifest.length} manifest entries are current-session artifacts; signed board approval, minutes, PDF generation, and delivery workflow require Enterprise.`;
}

function renderAispmPilotControlReadiness() {
  const generatedAt = new Date().toISOString();
  const readinessItems = aispmPilotControlReadinessItems.map(([control, status, artifact, detail]) => ({
    control,
    status,
    artifact,
    detail,
    public_safe: true
  }));
  currentAispmPilotControlReadinessPacket = {
    schema_version: "cavra.aispm.pilot_control_readiness_packet.v1",
    product: "CAVRA",
    edition: "community",
    mode: "public_safe_export",
    generated_at: generatedAt,
    packet_label: "AISPM Pilot Control Readiness Packet",
    source: "Pilot Control Readiness",
    audience: ["CSO", "CISO", "Platform Engineering", "Security Engineering", "Procurement", "Auditor"],
    readiness_items: readinessItems,
    source_packets: [
      currentAispmPilotExceptionRegisterPacket?.schema_version || "cavra.aispm.pilot_exception_register_packet.v1",
      currentAispmPilotRiskAcceptancePacket?.schema_version || "cavra.aispm.pilot_risk_acceptance_packet.v1",
      currentAispmPilotLaunchBoardPackPacket?.schema_version || "cavra.aispm.pilot_launch_board_pack_packet.v1"
    ],
    release_verification_sources: [
      "docs/release-verifications/aispm-launch-board-pack-artifact-index.json",
      "docs/release-verifications/aispm-launch-readiness-rollup.json",
      "docs/release-verifications/aispm-release-evidence-index.json"
    ],
    verification: {
      validator: "scripts/validate-aispm-pilot-control-readiness.py",
      portal_packet: "cavra-aispm-pilot-control-readiness-packet.json",
      release_index: "docs/release-verifications/aispm-release-evidence-index.json",
      launch_rollup: "docs/release-verifications/aispm-launch-readiness-rollup.json",
      expected_control_count: readinessItems.length
    },
    public_safety_boundary: "No signed risk acceptance, named approvers, board minutes, private telemetry, customer records, license keys, private package tokens, Enterprise source code, or tenant workflow state are included.",
    enterprise_boundary: {
      signed_exception_acceptance: "requires_cavra_enterprise_or_saas",
      signed_risk_acceptance: "requires_cavra_enterprise_or_saas",
      board_minutes_and_pdf_delivery: "requires_cavra_enterprise_report_service",
      tenant_artifact_retention: "requires_enterprise_evidence_store",
      workflow_write_back: "requires_cavra_enterprise_or_saas"
    },
    enterprise_boundary_summary: "Enterprise is required for signed exception and risk acceptance, board minutes, PDF delivery, tenant retention, and workflow write-back."
  };
  el("#aispmPilotControlReadiness").innerHTML = readinessItems.map(({ control, status, artifact, detail }) => `
    <article class="pilot-control-card">
      <span class="severity approved">${escapeHtml(status)}</span>
      <strong>${escapeHtml(control)}</strong>
      <p>${escapeHtml(detail)}</p>
      <code>${escapeHtml(artifact)}</code>
    </article>
  `).join("");
  el("#aispmPilotControlStatus").textContent = `${readinessItems.length} production-pilot control areas are ready for public-safe export; signed approvals, board minutes, and workflow write-back remain Enterprise-only.`;
}

function renderAispmReleaseEvidenceIndex() {
  const generatedAt = new Date().toISOString();
  const evidenceItems = aispmReleaseEvidenceIndexItems.map(([title, markdown, jsonPath, validator, detail, status]) => ({
    title,
    markdown,
    machine_readable: jsonPath,
    validator,
    detail,
    status,
    public_safe: true
  }));
  currentAispmReleaseEvidenceIndexPacket = {
    schema_version: "cavra.aispm.release_evidence_index_packet.v1",
    product: "CAVRA",
    edition: "community",
    mode: "public_safe_export",
    generated_at: generatedAt,
    packet_label: "AISPM Release Evidence Index Packet",
    source: "Release Evidence Index",
    audience: ["Release Reviewer", "CSO", "CISO", "Auditor", "Platform Engineering", "Security Engineering"],
    evidence_items: evidenceItems,
    freshness_gate: {
      status: "ready",
      evidence_count: evidenceItems.length,
      validator: "scripts/validate-aispm-release-evidence-index.py",
      workflow_artifact: "cavra-hosted-sandbox-post-deploy-evidence",
      hosted_pages_smoke: "npm run validate:sandbox:hosted",
      local_visual_smoke: "npm run validate:sandbox:visual"
    },
    public_safety_boundary: "No customer records, raw prompts, private trial package tokens, license signing keys, private registry credentials, Enterprise source code, or tenant telemetry are included.",
    enterprise_boundary: {
      signed_release_approval: "requires_cavra_enterprise_or_saas",
      tenant_evidence_room: "requires_enterprise_evidence_store",
      private_trial_package_validation: "requires_private_enterprise_pipeline",
      licensed_report_delivery: "requires_cavra_enterprise"
    }
  };
  el("#aispmReleaseEvidenceIndex").innerHTML = evidenceItems.map(({ title, markdown, machine_readable, validator, detail, status }) => `
    <article class="release-evidence-card">
      <span class="severity ${status === "workflow_enforced" ? "controlled" : "approved"}">${escapeHtml(status)}</span>
      <strong>${escapeHtml(title)}</strong>
      <p>${escapeHtml(detail)}</p>
      <div class="release-evidence-links">
        <a href="https://github.com/Huzefaaa2/cavra/blob/main/${escapeHtml(markdown)}" target="_blank" rel="noreferrer">Markdown</a>
        <a href="https://github.com/Huzefaaa2/cavra/blob/main/${escapeHtml(machine_readable)}" target="_blank" rel="noreferrer">Packet</a>
      </div>
      <small>${escapeHtml(validator)}</small>
    </article>
  `).join("");
  const manifestCards = [
    ["Evidence Packets", String(evidenceItems.length), "Launch, visual, hosted, post-deploy, lab notebook, and closeout evidence"],
    ["Freshness Gate", "Ready", "Index is validator-backed and wired into Community CI, release, and Pages workflows"],
    ["Workflow Artifact", "Uploaded", "cavra-hosted-sandbox-post-deploy-evidence records live Pages run metadata"],
    ["Public Boundary", "Clean", "Secrets, customer data, private registries, telemetry, and Enterprise source are excluded"]
  ];
  el("#aispmReleaseEvidenceManifest").innerHTML = manifestCards.map(([label, value, detail]) => `
    <article class="release-evidence-manifest-card">
      <span class="severity approved">${escapeHtml(label)}</span>
      <strong>${escapeHtml(value)}</strong>
      <p>${escapeHtml(detail)}</p>
    </article>
  `).join("");
  el("#aispmReleaseEvidenceStatus").textContent = `${evidenceItems.length} release evidence records indexed for reviewers; signed release approval and tenant evidence room remain Enterprise-only.`;
}

function renderAispmHostedReleaseStatus() {
  const generatedAt = new Date().toISOString();
  const checks = aispmHostedReleaseStatusItems.map(([label, status, validator, detail]) => ({
    label,
    status,
    validator,
    detail,
    public_safe: true
  }));
  const readyCount = checks.filter((item) => ["ready", "workflow_enforced"].includes(item.status)).length;
  const actionCount = checks.length - readyCount;
  currentAispmHostedReleaseStatusPacket = {
    schema_version: "cavra.hosted_sandbox.operator_release_status_packet.v1",
    product: "CAVRA",
    edition: "community",
    mode: "public_safe_operator_export",
    generated_at: generatedAt,
    packet_label: "Hosted Release Operator Status Packet",
    source: "Hosted Release Operator Status",
    hosted_target: "https://huzefaaa2.github.io/cavra/",
    build_sentinel: "community-v1.0.0-aispm-release-evidence-index",
    checks,
    status_summary: {
      local_repository_status: "ready",
      hosted_pages_status: "requires_deploy_validation",
      ready_or_enforced_checks: readyCount,
      operator_action_checks: actionCount,
      announcement_state: "blocked_until_live_freshness_passes"
    },
    release_evidence_refs: [
      "docs/release-verifications/hosted-sandbox-deployment-freshness.md",
      "docs/release-verifications/hosted-sandbox-deployment-freshness.json",
      "scripts/validate-hosted-sandbox-operator-status.py",
      "docs/release-verifications/hosted-sandbox-post-deploy-evidence.md",
      "docs/release-verifications/aispm-release-evidence-index.md"
    ],
    public_safety_boundary: "Includes public static deployment readiness markers only. Excludes customer data, raw prompts, private package credentials, license secrets, Enterprise source code, and tenant telemetry.",
    enterprise_boundary: {
      signed_announcement_approval: "requires_cavra_enterprise_or_saas",
      tenant_release_room: "requires_enterprise_evidence_store",
      evaluator_access_grants: "requires_private_trial_operator_flow"
    }
  };
  el("#aispmHostedReleaseStatus").innerHTML = [
    ["Local Repository", "Ready", "Local validators and static portal markers pass before deployment."],
    ["Hosted Pages", "Needs deploy", "Live freshness remains blocked until GitHub Pages publishes this build."],
    ["Announcement", "Hold", "Share externally after live freshness, browser smoke, and post-deploy artifact pass."],
    ["Sentinel", "v1.0.0 AISPM", "community-v1.0.0-aispm-release-evidence-index"]
  ].map(([label, value, detail]) => `
    <article class="hosted-release-status-card">
      <span class="severity ${value === "Ready" ? "approved" : "controlled"}">${escapeHtml(label)}</span>
      <strong>${escapeHtml(value)}</strong>
      <p>${escapeHtml(detail)}</p>
    </article>
  `).join("");
  el("#aispmHostedReleaseChecklist").innerHTML = checks.map(({ label, status, validator, detail }) => `
    <article class="hosted-release-check-card">
      <div>
        <span class="severity ${status === "blocked_until_live_fresh" ? "high" : status === "requires_deploy" ? "medium" : "approved"}">${escapeHtml(status)}</span>
        <strong>${escapeHtml(label)}</strong>
      </div>
      <p>${escapeHtml(detail)}</p>
      <code>${escapeHtml(validator)}</code>
    </article>
  `).join("");
  el("#aispmHostedReleaseStatusLine").textContent = `${checks.length} hosted release checks indexed; external announcement remains blocked until live freshness passes after GitHub Pages deployment.`;
}

function handleAispmReportDownload(event) {
  const button = event.target.closest("[data-report-download]");
  if (!button) return;
  const report = currentAispmReports[button.dataset.reportDownload];
  if (!report) return;
  downloadTextFile(report.filename, report.content, report.type);
  el("#aispmReportStatus").textContent = `Downloaded ${report.filename}.`;
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
  renderAispmReportCenter(payload);
  renderAispmReportSetupReadiness();
  renderAispmReportOperationsReadiness();
  renderAispmReportGovernanceReadiness();
  renderAispmReportAssuranceReadiness();
  renderAispmReportResponseReadiness();
  renderAispmReportTrialOpsReadiness();
  renderAispmTrialReadinessChecklist();
  renderAispmEvaluatorHandoff();
  renderAispmTrialJourney();
  renderAispmTrialCloseoutEvidence();
  renderAispmTrialFeedbackIntake();
  renderAispmTrialOutcomeSummary();
  renderAispmTrialReviewPacketIntegrity();
  renderAispmTrialProcurementReadiness();
  renderAispmTrialPilotScope();
  renderAispmPilotApprovalChecklist();
  renderAispmPilotLaunchReadiness();
  renderAispmPilotEvidenceRoom();
  renderAispmEvidenceReviewerChecklist();
  renderAispmPilotExceptionRegister();
  renderAispmPilotRiskAcceptanceSummary();
  renderAispmPilotLaunchBoardPack();
  renderAispmPilotControlReadiness();
  renderAispmReleaseEvidenceIndex();
  renderAispmHostedReleaseStatus();
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
  renderAispmReplayPolicyCiGateAuditorView(currentAispmReplayPolicyCiGateAuditPacket);
}

function renderAispmReplayPolicyCiGateAuditorView(packet) {
  const attachments = packet.evidence_attachments || [];
  const platformOutcomes = packet.platform_outcomes || [];
  const requiredCheck = packet.rollout_checklist?.required_check || "cavra-aispm-review-packet";
  const status = packet.status === "ready" ? "ready" : "action_required";
  const findingRows = [
    {
      control: "Review packet attached",
      status: attachments.includes("cavra-replay-policy-review-packet.json") ? "pass" : "action required",
      evidence: "cavra-replay-policy-review-packet.json",
      auditor_note: "Replay-derived policy changes have a public-safe review packet."
    },
    {
      control: "Readiness packet attached",
      status: attachments.includes("cavra-replay-policy-ci-gate-readiness.json") ? "pass" : "action required",
      evidence: "cavra-replay-policy-ci-gate-readiness.json",
      auditor_note: "Branch-protection readiness metadata is available for validation."
    },
    {
      control: "Rollout checklist attached",
      status: attachments.includes("cavra-replay-policy-ci-gate-rollout-checklist.md") ? "pass" : "action required",
      evidence: "cavra-replay-policy-ci-gate-rollout-checklist.md",
      auditor_note: "Manual rollout steps are documented for reviewer sign-off."
    },
    {
      control: "Required check named",
      status: requiredCheck === "cavra-aispm-review-packet" ? "pass" : "action required",
      evidence: requiredCheck,
      auditor_note: "The same required check name is used across supported CI platforms."
    },
    {
      control: "Public safety boundary",
      status: packet.public_safety?.raw_prompts === "not_included" && packet.public_safety?.model_reasoning === "not_included" ? "pass" : "action required",
      evidence: "raw_prompts/model_reasoning/customer_context not included",
      auditor_note: "Community audit packets do not expose prompts, reasoning, or customer context."
    },
    {
      control: "Enterprise automation boundary",
      status: packet.public_safety?.branch_protection_write_back === "requires_cavra_enterprise" ? "pass" : "action required",
      evidence: "branch protection write-back requires CAVRA Enterprise",
      auditor_note: "Community provides evidence guidance; automated write-back remains an Enterprise control."
    }
  ];
  const passedFindings = findingRows.filter((row) => row.status === "pass").length;
  const auditorConclusion = status === "ready" && passedFindings === findingRows.length
    ? "Auditor conclusion: ready for controlled production rollout after branch protection is configured and evidence attachments are preserved with the rollout ticket or PR."
    : "Auditor conclusion: action required before production rollout. Resolve missing attachments or inconsistent gate metadata first.";
  el("#aispmReplayPolicyCiGateAuditorView").innerHTML = `
    <div class="ci-gate-auditor-header">
      <div>
        <h4>CI Gate Rollout Auditor View</h4>
        <p>Human-readable rollup of rollout evidence, required checks, platform outcomes, and public-safe boundaries.</p>
      </div>
      <span class="severity ${status === "ready" ? "approved" : "pending"}">${status === "ready" ? "Ready" : "Action Required"}</span>
    </div>
    <div class="ci-gate-auditor-grid">
      <article>
        <span>Audit status</span>
        <strong>${escapeHtml(status)}</strong>
        <p>${escapeHtml(passedFindings)}/${escapeHtml(findingRows.length)} auditor findings pass.</p>
      </article>
      <article>
        <span>Platforms</span>
        <strong>${escapeHtml(platformOutcomes.length)}</strong>
        <p>${escapeHtml(platformOutcomes.map((row) => row.platform).join(", "))}</p>
      </article>
      <article>
        <span>Required check</span>
        <strong>${escapeHtml(requiredCheck)}</strong>
        <p>Must be required before replay-derived policy or fixture changes merge.</p>
      </article>
      <article>
        <span>Evidence attachments</span>
        <strong>${escapeHtml(attachments.length)}</strong>
        <p>${escapeHtml(attachments.join(", "))}</p>
      </article>
    </div>
    <div class="ci-gate-auditor-findings">
      ${findingRows.map((row) => `
        <article class="ci-gate-auditor-finding">
          <div>
            <span>${escapeHtml(row.control)}</span>
            <strong>${escapeHtml(row.status)}</strong>
          </div>
          <code>${escapeHtml(row.evidence)}</code>
          <p>${escapeHtml(row.auditor_note)}</p>
        </article>
      `).join("")}
    </div>
    <div class="ci-gate-auditor-conclusion">${escapeHtml(auditorConclusion)}</div>
  `;
}

async function copyAispmReplayPolicyCiGateReadiness() {
  const payload = JSON.stringify(currentAispmReplayPolicyCiGateReadiness || {}, null, 2);
  const copied = await copyTextToClipboard(payload);
  el("#aispmReplayPolicyCiGateStatus").textContent = copied
    ? "Copied public-safe CI gate readiness JSON."
    : "Copy was blocked by the browser. Use Download Readiness or select the JSON from exported artifacts.";
}

async function copyAispmTrialReadinessSummary() {
  const copied = await copyTextToClipboard(currentAispmTrialReadinessMarkdown);
  el("#aispmTrialReadinessStatus").textContent = copied
    ? "Copied public-safe AISPM Enterprise Trial readiness summary Markdown."
    : "Copy was blocked by the browser. Use Download Packet or select the readiness links manually.";
}

function downloadAispmTrialReadinessPacket() {
  const payload = JSON.stringify(currentAispmTrialReadinessPacket || {}, null, 2);
  downloadTextFile(
    "cavra-aispm-enterprise-trial-readiness-packet.json",
    payload,
    "application/json"
  );
  el("#aispmTrialReadinessStatus").textContent = "Downloaded public-safe AISPM Enterprise Trial readiness packet JSON.";
}

async function copyAispmTrialReviewPacket() {
  const payload = JSON.stringify(currentAispmTrialReviewPacket || {}, null, 2);
  const copied = await copyTextToClipboard(payload);
  el("#aispmTrialReviewPacketStatus").textContent = copied
    ? "Copied public-safe AISPM Trial review packet JSON."
    : "Copy was blocked by the browser. Use Download Review Packet or select the visible section details.";
}

function downloadAispmTrialReviewPacket() {
  const payload = JSON.stringify(currentAispmTrialReviewPacket || {}, null, 2);
  downloadTextFile(
    "cavra-aispm-trial-review-packet.json",
    payload,
    "application/json"
  );
  el("#aispmTrialReviewPacketStatus").textContent = "Downloaded public-safe AISPM Trial review packet JSON.";
}

async function copyAispmTrialPilotScopePacket() {
  const payload = JSON.stringify(currentAispmTrialPilotScopePacket || {}, null, 2);
  const copied = await copyTextToClipboard(payload);
  el("#aispmTrialPilotScopeStatus").textContent = copied
    ? "Copied public-safe AISPM Trial pilot scope packet JSON."
    : "Copy was blocked by the browser. Use Download Pilot Packet or select the visible scope details.";
}

function downloadAispmTrialPilotScopePacket() {
  const payload = JSON.stringify(currentAispmTrialPilotScopePacket || {}, null, 2);
  downloadTextFile(
    "cavra-aispm-trial-pilot-scope-packet.json",
    payload,
    "application/json"
  );
  el("#aispmTrialPilotScopeStatus").textContent = "Downloaded public-safe AISPM Trial pilot scope packet JSON.";
}

async function copyAispmPilotApprovalPacket() {
  const payload = JSON.stringify(currentAispmPilotApprovalPacket || {}, null, 2);
  const copied = await copyTextToClipboard(payload);
  el("#aispmPilotApprovalStatus").textContent = copied
    ? "Copied public-safe AISPM Pilot approval packet JSON."
    : "Copy was blocked by the browser. Use Download Approval Packet or select the visible gate details.";
}

function downloadAispmPilotApprovalPacket() {
  const payload = JSON.stringify(currentAispmPilotApprovalPacket || {}, null, 2);
  downloadTextFile(
    "cavra-aispm-pilot-approval-packet.json",
    payload,
    "application/json"
  );
  el("#aispmPilotApprovalStatus").textContent = "Downloaded public-safe AISPM Pilot approval packet JSON.";
}

async function copyAispmPilotLaunchDecisionPacket() {
  const payload = JSON.stringify(currentAispmPilotLaunchDecisionPacket || {}, null, 2);
  const copied = await copyTextToClipboard(payload);
  el("#aispmPilotLaunchStatus").textContent = copied
    ? "Copied public-safe AISPM Pilot launch decision packet JSON."
    : "Copy was blocked by the browser. Use Download Decision Packet or select the visible readiness details.";
}

function downloadAispmPilotLaunchDecisionPacket() {
  const payload = JSON.stringify(currentAispmPilotLaunchDecisionPacket || {}, null, 2);
  downloadTextFile(
    "cavra-aispm-pilot-launch-decision-packet.json",
    payload,
    "application/json"
  );
  el("#aispmPilotLaunchStatus").textContent = "Downloaded public-safe AISPM Pilot launch decision packet JSON.";
}

async function copyAispmPilotEvidenceRoomPacket() {
  const payload = JSON.stringify(currentAispmPilotEvidenceRoomPacket || {}, null, 2);
  const copied = await copyTextToClipboard(payload);
  el("#aispmPilotEvidenceRoomStatus").textContent = copied
    ? "Copied public-safe AISPM Production Pilot evidence room packet JSON."
    : "Copy was blocked by the browser. Use Download Evidence Packet or select the visible role catalog.";
}

function downloadAispmPilotEvidenceRoomPacket() {
  const payload = JSON.stringify(currentAispmPilotEvidenceRoomPacket || {}, null, 2);
  downloadTextFile(
    "cavra-aispm-pilot-evidence-room-packet.json",
    payload,
    "application/json"
  );
  el("#aispmPilotEvidenceRoomStatus").textContent = "Downloaded public-safe AISPM Production Pilot evidence room packet JSON.";
}

async function copyAispmEvidenceReviewerChecklistPacket() {
  const payload = JSON.stringify(currentAispmEvidenceReviewerChecklistPacket || {}, null, 2);
  const copied = await copyTextToClipboard(payload);
  el("#aispmEvidenceReviewerChecklistStatus").textContent = copied
    ? "Copied public-safe AISPM Evidence Room reviewer checklist packet JSON."
    : "Copy was blocked by the browser. Use Download Checklist Packet or select the visible criteria.";
}

function downloadAispmEvidenceReviewerChecklistPacket() {
  const payload = JSON.stringify(currentAispmEvidenceReviewerChecklistPacket || {}, null, 2);
  downloadTextFile(
    "cavra-aispm-evidence-reviewer-checklist-packet.json",
    payload,
    "application/json"
  );
  el("#aispmEvidenceReviewerChecklistStatus").textContent = "Downloaded public-safe AISPM Evidence Room reviewer checklist packet JSON.";
}

async function copyAispmPilotExceptionRegisterPacket() {
  const payload = JSON.stringify(currentAispmPilotExceptionRegisterPacket || {}, null, 2);
  const copied = await copyTextToClipboard(payload);
  el("#aispmPilotExceptionStatus").textContent = copied
    ? "Copied public-safe AISPM Pilot exception register packet JSON."
    : "Copy was blocked by the browser. Use Download Exception Packet or select the visible register.";
}

function downloadAispmPilotExceptionRegisterPacket() {
  const payload = JSON.stringify(currentAispmPilotExceptionRegisterPacket || {}, null, 2);
  downloadTextFile(
    "cavra-aispm-pilot-exception-register-packet.json",
    payload,
    "application/json"
  );
  el("#aispmPilotExceptionStatus").textContent = "Downloaded public-safe AISPM Pilot exception register packet JSON.";
}

async function copyAispmPilotRiskAcceptancePacket() {
  const payload = JSON.stringify(currentAispmPilotRiskAcceptancePacket || {}, null, 2);
  const copied = await copyTextToClipboard(payload);
  el("#aispmPilotRiskAcceptanceStatus").textContent = copied
    ? "Copied public-safe AISPM Pilot risk acceptance packet JSON."
    : "Copy was blocked by the browser. Use Download Risk Packet or select the visible summary.";
}

function downloadAispmPilotRiskAcceptancePacket() {
  const payload = JSON.stringify(currentAispmPilotRiskAcceptancePacket || {}, null, 2);
  downloadTextFile(
    "cavra-aispm-pilot-risk-acceptance-packet.json",
    payload,
    "application/json"
  );
  el("#aispmPilotRiskAcceptanceStatus").textContent = "Downloaded public-safe AISPM Pilot risk acceptance packet JSON.";
}

async function copyAispmPilotLaunchBoardPackPacket() {
  const payload = JSON.stringify(currentAispmPilotLaunchBoardPackPacket || {}, null, 2);
  const copied = await copyTextToClipboard(payload);
  el("#aispmPilotLaunchBoardPackStatus").textContent = copied
    ? "Copied public-safe AISPM Pilot launch board pack packet JSON."
    : "Copy was blocked by the browser. Use Download Board Packet or select the visible board pack details.";
}

function downloadAispmPilotLaunchBoardPackPacket() {
  const payload = JSON.stringify(currentAispmPilotLaunchBoardPackPacket || {}, null, 2);
  downloadTextFile(
    "cavra-aispm-pilot-launch-board-pack-packet.json",
    payload,
    "application/json"
  );
  el("#aispmPilotLaunchBoardPackStatus").textContent = "Downloaded public-safe AISPM Pilot launch board pack packet JSON.";
}

async function copyAispmPilotControlReadinessPacket() {
  const payload = JSON.stringify(currentAispmPilotControlReadinessPacket || {}, null, 2);
  const copied = await copyTextToClipboard(payload);
  el("#aispmPilotControlStatus").textContent = copied
    ? "Copied public-safe AISPM Pilot control readiness packet JSON."
    : "Copy was blocked by the browser. Use Download Control Packet or select the visible control readiness details.";
}

function downloadAispmPilotControlReadinessPacket() {
  const payload = JSON.stringify(currentAispmPilotControlReadinessPacket || {}, null, 2);
  downloadTextFile(
    "cavra-aispm-pilot-control-readiness-packet.json",
    payload,
    "application/json"
  );
  el("#aispmPilotControlStatus").textContent = "Downloaded public-safe AISPM Pilot control readiness packet JSON.";
}

async function copyAispmReleaseEvidenceIndexPacket() {
  const payload = JSON.stringify(currentAispmReleaseEvidenceIndexPacket || {}, null, 2);
  const copied = await copyTextToClipboard(payload);
  el("#aispmReleaseEvidenceStatus").textContent = copied
    ? "Copied public-safe AISPM release evidence index packet JSON."
    : "Copy was blocked by the browser. Use Download Evidence Index or select the visible release evidence details.";
}

function downloadAispmReleaseEvidenceIndexPacket() {
  const payload = JSON.stringify(currentAispmReleaseEvidenceIndexPacket || {}, null, 2);
  downloadTextFile(
    "cavra-aispm-release-evidence-index-packet.json",
    payload,
    "application/json"
  );
  el("#aispmReleaseEvidenceStatus").textContent = "Downloaded public-safe AISPM release evidence index packet JSON.";
}

async function copyAispmHostedReleaseStatusPacket() {
  const payload = JSON.stringify(currentAispmHostedReleaseStatusPacket || {}, null, 2);
  const copied = await copyTextToClipboard(payload);
  el("#aispmHostedReleaseStatusLine").textContent = copied
    ? "Copied public-safe hosted release operator status packet JSON."
    : "Copy was blocked by the browser. Use Download Status Packet or select the visible status details.";
}

function downloadAispmHostedReleaseStatusPacket() {
  const payload = JSON.stringify(currentAispmHostedReleaseStatusPacket || {}, null, 2);
  downloadTextFile(
    "cavra-hosted-sandbox-operator-status-packet.json",
    payload,
    "application/json"
  );
  el("#aispmHostedReleaseStatusLine").textContent = "Downloaded public-safe hosted release operator status packet JSON.";
}

async function copyAispmReportCatalogPacket() {
  const payload = JSON.stringify(currentAispmReportCatalogPacket || {}, null, 2);
  const copied = await copyTextToClipboard(payload);
  el("#aispmReportStatus").textContent = copied
    ? "Copied public-safe AISPM report catalog readiness packet JSON."
    : "Copy was blocked by the browser. Use Download Catalog Packet or select the visible report details.";
}

function downloadAispmReportCatalogPacket() {
  const payload = JSON.stringify(currentAispmReportCatalogPacket || {}, null, 2);
  downloadTextFile(
    "cavra-aispm-report-catalog-packet.json",
    payload,
    "application/json"
  );
  el("#aispmReportStatus").textContent = "Downloaded public-safe AISPM report catalog readiness packet JSON.";
}

async function copyAispmReportSetupPacket() {
  const payload = JSON.stringify(currentAispmReportSetupPacket || {}, null, 2);
  const copied = await copyTextToClipboard(payload);
  el("#aispmReportSetupStatus").textContent = copied
    ? "Copied public-safe AISPM report delivery setup readiness packet JSON."
    : "Copy was blocked by the browser. Use Download Setup Packet or select the visible setup details.";
}

function downloadAispmReportSetupPacket() {
  const payload = JSON.stringify(currentAispmReportSetupPacket || {}, null, 2);
  downloadTextFile(
    "cavra-aispm-report-delivery-setup-packet.json",
    payload,
    "application/json"
  );
  el("#aispmReportSetupStatus").textContent = "Downloaded public-safe AISPM report delivery setup readiness packet JSON.";
}

async function copyAispmReportOperationsPacket() {
  const payload = JSON.stringify(currentAispmReportOperationsPacket || {}, null, 2);
  const copied = await copyTextToClipboard(payload);
  el("#aispmReportOperationsStatus").textContent = copied
    ? "Copied public-safe AISPM report operations readiness packet JSON."
    : "Copy was blocked by the browser. Use Download Operations Packet or select the visible operations details.";
}

function downloadAispmReportOperationsPacket() {
  const payload = JSON.stringify(currentAispmReportOperationsPacket || {}, null, 2);
  downloadTextFile(
    "cavra-aispm-report-operations-readiness-packet.json",
    payload,
    "application/json"
  );
  el("#aispmReportOperationsStatus").textContent = "Downloaded public-safe AISPM report operations readiness packet JSON.";
}

async function copyAispmReportGovernancePacket() {
  const payload = JSON.stringify(currentAispmReportGovernancePacket || {}, null, 2);
  const copied = await copyTextToClipboard(payload);
  el("#aispmReportGovernanceStatus").textContent = copied
    ? "Copied public-safe AISPM report governance readiness packet JSON."
    : "Copy was blocked by the browser. Use Download Governance Packet or select the visible governance details.";
}

function downloadAispmReportGovernancePacket() {
  const payload = JSON.stringify(currentAispmReportGovernancePacket || {}, null, 2);
  downloadTextFile(
    "cavra-aispm-report-governance-readiness-packet.json",
    payload,
    "application/json"
  );
  el("#aispmReportGovernanceStatus").textContent = "Downloaded public-safe AISPM report governance readiness packet JSON.";
}

async function copyAispmReportAssurancePacket() {
  const payload = JSON.stringify(currentAispmReportAssurancePacket || {}, null, 2);
  const copied = await copyTextToClipboard(payload);
  el("#aispmReportAssuranceStatus").textContent = copied
    ? "Copied public-safe AISPM report assurance readiness packet JSON."
    : "Copy was blocked by the browser. Use Download Assurance Packet or select the visible assurance details.";
}

function downloadAispmReportAssurancePacket() {
  const payload = JSON.stringify(currentAispmReportAssurancePacket || {}, null, 2);
  downloadTextFile(
    "cavra-aispm-report-assurance-readiness-packet.json",
    payload,
    "application/json"
  );
  el("#aispmReportAssuranceStatus").textContent = "Downloaded public-safe AISPM report assurance readiness packet JSON.";
}

async function copyAispmReportResponsePacket() {
  const payload = JSON.stringify(currentAispmReportResponsePacket || {}, null, 2);
  const copied = await copyTextToClipboard(payload);
  el("#aispmReportResponseStatus").textContent = copied
    ? "Copied public-safe AISPM report response readiness packet JSON."
    : "Copy was blocked by the browser. Use Download Response Packet or select the visible response details.";
}

function downloadAispmReportResponsePacket() {
  const payload = JSON.stringify(currentAispmReportResponsePacket || {}, null, 2);
  downloadTextFile(
    "cavra-aispm-report-response-readiness-packet.json",
    payload,
    "application/json"
  );
  el("#aispmReportResponseStatus").textContent = "Downloaded public-safe AISPM report response readiness packet JSON.";
}

async function copyAispmReportTrialOpsPacket() {
  const payload = JSON.stringify(currentAispmReportTrialOpsPacket || {}, null, 2);
  const copied = await copyTextToClipboard(payload);
  el("#aispmReportTrialOpsStatus").textContent = copied
    ? "Copied public-safe AISPM report trial operations readiness packet JSON."
    : "Copy was blocked by the browser. Use Download Trial Ops Packet or select the visible trial operations details.";
}

function downloadAispmReportTrialOpsPacket() {
  const payload = JSON.stringify(currentAispmReportTrialOpsPacket || {}, null, 2);
  downloadTextFile(
    "cavra-aispm-report-trial-operations-readiness-packet.json",
    payload,
    "application/json"
  );
  el("#aispmReportTrialOpsStatus").textContent = "Downloaded public-safe AISPM report trial operations readiness packet JSON.";
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
  el("#aispmReportCenter").addEventListener("click", handleAispmReportDownload);
  el("#copyAispmTrialReadinessSummary").addEventListener("click", copyAispmTrialReadinessSummary);
  el("#downloadAispmTrialReadinessPacket").addEventListener("click", downloadAispmTrialReadinessPacket);
  el("#copyAispmTrialReviewPacket").addEventListener("click", copyAispmTrialReviewPacket);
  el("#downloadAispmTrialReviewPacket").addEventListener("click", downloadAispmTrialReviewPacket);
  el("#copyAispmTrialPilotScopePacket").addEventListener("click", copyAispmTrialPilotScopePacket);
  el("#downloadAispmTrialPilotScopePacket").addEventListener("click", downloadAispmTrialPilotScopePacket);
  el("#copyAispmPilotApprovalPacket").addEventListener("click", copyAispmPilotApprovalPacket);
  el("#downloadAispmPilotApprovalPacket").addEventListener("click", downloadAispmPilotApprovalPacket);
  el("#copyAispmPilotLaunchDecisionPacket").addEventListener("click", copyAispmPilotLaunchDecisionPacket);
  el("#downloadAispmPilotLaunchDecisionPacket").addEventListener("click", downloadAispmPilotLaunchDecisionPacket);
  el("#copyAispmPilotEvidenceRoomPacket").addEventListener("click", copyAispmPilotEvidenceRoomPacket);
  el("#downloadAispmPilotEvidenceRoomPacket").addEventListener("click", downloadAispmPilotEvidenceRoomPacket);
  el("#copyAispmEvidenceReviewerChecklistPacket").addEventListener("click", copyAispmEvidenceReviewerChecklistPacket);
  el("#downloadAispmEvidenceReviewerChecklistPacket").addEventListener("click", downloadAispmEvidenceReviewerChecklistPacket);
  el("#copyAispmPilotExceptionRegisterPacket").addEventListener("click", copyAispmPilotExceptionRegisterPacket);
  el("#downloadAispmPilotExceptionRegisterPacket").addEventListener("click", downloadAispmPilotExceptionRegisterPacket);
  el("#copyAispmPilotRiskAcceptancePacket").addEventListener("click", copyAispmPilotRiskAcceptancePacket);
  el("#downloadAispmPilotRiskAcceptancePacket").addEventListener("click", downloadAispmPilotRiskAcceptancePacket);
  el("#copyAispmPilotLaunchBoardPackPacket").addEventListener("click", copyAispmPilotLaunchBoardPackPacket);
  el("#downloadAispmPilotLaunchBoardPackPacket").addEventListener("click", downloadAispmPilotLaunchBoardPackPacket);
  el("#copyAispmPilotControlReadinessPacket").addEventListener("click", copyAispmPilotControlReadinessPacket);
  el("#downloadAispmPilotControlReadinessPacket").addEventListener("click", downloadAispmPilotControlReadinessPacket);
  el("#copyAispmReleaseEvidenceIndexPacket").addEventListener("click", copyAispmReleaseEvidenceIndexPacket);
  el("#downloadAispmReleaseEvidenceIndexPacket").addEventListener("click", downloadAispmReleaseEvidenceIndexPacket);
  el("#copyAispmHostedReleaseStatusPacket").addEventListener("click", copyAispmHostedReleaseStatusPacket);
  el("#downloadAispmHostedReleaseStatusPacket").addEventListener("click", downloadAispmHostedReleaseStatusPacket);
  el("#copyAispmReportCatalogPacket").addEventListener("click", copyAispmReportCatalogPacket);
  el("#downloadAispmReportCatalogPacket").addEventListener("click", downloadAispmReportCatalogPacket);
  el("#copyAispmReportSetupPacket").addEventListener("click", copyAispmReportSetupPacket);
  el("#downloadAispmReportSetupPacket").addEventListener("click", downloadAispmReportSetupPacket);
  el("#copyAispmReportOperationsPacket").addEventListener("click", copyAispmReportOperationsPacket);
  el("#downloadAispmReportOperationsPacket").addEventListener("click", downloadAispmReportOperationsPacket);
  el("#copyAispmReportGovernancePacket").addEventListener("click", copyAispmReportGovernancePacket);
  el("#downloadAispmReportGovernancePacket").addEventListener("click", downloadAispmReportGovernancePacket);
  el("#copyAispmReportAssurancePacket").addEventListener("click", copyAispmReportAssurancePacket);
  el("#downloadAispmReportAssurancePacket").addEventListener("click", downloadAispmReportAssurancePacket);
  el("#copyAispmReportResponsePacket").addEventListener("click", copyAispmReportResponsePacket);
  el("#downloadAispmReportResponsePacket").addEventListener("click", downloadAispmReportResponsePacket);
  el("#copyAispmReportTrialOpsPacket").addEventListener("click", copyAispmReportTrialOpsPacket);
  el("#downloadAispmReportTrialOpsPacket").addEventListener("click", downloadAispmReportTrialOpsPacket);
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
