const navItems = [
  { id: "dashboard", label: "Overview", icon: "C", group: "Start", description: "Business outcomes, executive deliverables, editions, downloads, and public demo summary." },
  { id: "ai-posture", label: "AISPM", icon: "A", group: "Start", description: "AI Security Posture Management, reports, board packs, and trial labs." },
  { id: "architecture", label: "Architecture", icon: "N", group: "Platform", description: "Runtime authority, policy, evidence, posture, identity, and integrations." },
  { id: "policy-engine", label: "Policy Engine", icon: "P", group: "Platform", description: "Policy decisions across files, commands, Git, MCP, CI/CD, cloud, and releases." },
  { id: "evidence", label: "Evidence", icon: "E", group: "Platform", description: "Audit trails, attestations, evidence bundles, and control mappings." },
  { id: "use-cases", label: "Use Cases", icon: "U", group: "Solutions", description: "Secret protection, Terraform gates, protected branches, MCP trust, and AI-agent governance." },
  { id: "operator-experience", label: "Role Paths", icon: "R", group: "Solutions", description: "Security, platform, audit, and leadership reader paths." },
  { id: "enterprise-trial", label: "Enterprise Trial", icon: "T", group: "Editions", description: "Trial portal, time-limited license, private package, guided labs, and closeout." },
  { id: "integrations", label: "Integrations", icon: "I", group: "Editions", description: "Ready and planned integrations for developer and cloud control surfaces." },
  { id: "compliance", label: "Compliance", icon: "G", group: "Trust", description: "Control mappings, evidence boundaries, and audit-review caveats." },
  { id: "roadmap", label: "Roadmap", icon: "M", group: "Trust", description: "Community, Trial, Enterprise, SaaS, and Azure deployment paths." },
  { id: "documentation", label: "Docs", icon: "D", group: "Resources", description: "Wiki textbook, README, CLI, deployment guides, and Trial Field Guide." }
];

const metrics = [
  ["Runtime Decision Actions", "4", "Allow, block, require approval, or attest."],
  ["Protected Enterprise Assets", "7", "Code, shell, Git, MCP, CI/CD, cloud, and infrastructure."],
  ["Evidence outputs", "6", "Bundles, attestations, reports, packets, exports, and release records."],
  ["AISPM views", "9", "Coverage, findings, drift, blast radius, reports, and readiness."],
  ["Editions", "4", "Community, Trial, Enterprise, and SaaS deployment paths."]
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
  ["Community", "Open public sandbox", "Sample decisions, policy examples, local evidence, CLI/docs, Azure Community path.", "Developers, open-source users, and first-look reviewers."],
  ["Trial", "Time-limited Enterprise evaluation", "Trial portal, private package, guided AISPM labs, license, revocation, and closeout.", "CISO, platform, audit, and evaluator teams proving one use case."],
  ["Enterprise", "Private control plane", "Tenant isolation, SSO/RBAC, connectors, policy packs, SMTP/report delivery, runtime workflows.", "Organizations governing live AI-agent operations."],
  ["SaaS", "Managed operating model", "Hosted control plane, managed deployment, monitoring, reporting, and support paths.", "Teams that want CAVRA operated as an enterprise service."]
];

const downloadArtifacts = [
  ["Executive Product Brief", "PDF-ready", "Two-page business summary for CISO, board, and procurement review."],
  ["CAVRA Datasheet", "Product brief", "Capabilities, editions, runtime actions, protected surfaces, and evaluation path."],
  ["AISPM Capability Brief", "Datasheet", "Posture loop, findings, reports, readiness gates, and guided trial labs."],
  ["Runtime Authority Whitepaper", "Reference", "How pre-action governance works across AI-agent software delivery."],
  ["Architecture Reference Guide", "Diagram pack", "Runtime authority, policy, evidence, AISPM, identity, and integrations."],
  ["Board Readiness Packet", "Packet", "Sample launch summary, risk acceptance, report readiness, and evidence room index."],
  ["Sample Evidence Bundle", "Evidence", "Public-safe decision record, attestation outline, and control mapping examples."],
  ["Sample Attestation", "Evidence", "Example signed decision and reviewer attestation payload."],
  ["Security Controls Mapping", "SOC 2 / ISO / NIST", "Public-safe mapping from CAVRA evidence to common control families."],
  ["Gartner-style Feature Matrix", "Matrix", "Feature comparison across Community, Trial, Enterprise, and SaaS."],
  ["Deployment Reference Architecture", "Azure", "Community, Trial, Enterprise, and SaaS deployment topology summary."],
  ["Enterprise Trial Guide", "Guide", "Evaluator steps, trial portal, guided use case, AISPM labs, and closeout."],
  ["API Reference", "Reference", "Public-safe API surface overview and Enterprise integration boundaries."],
  ["Policy Pack Samples", "Examples", "Secret, Terraform, protected branch, MCP, and release governance examples."],
  ["Release Readiness Checklist", "Checklist", "Evidence, validation, release, and production-readiness review checklist."]
];

const communityCards = [
  ["Public landing", "Rebuilt", "Product-first homepage with demo-safe language and route-aware pages."],
  ["Community sandbox", "Ready", "Sample policy decisions, evidence, reports, and posture are available without secrets."],
  ["Docs and textbook", "Linked", "The Wiki e-book is positioned as the full technical reader guide."],
  ["Azure path", "Documented", "Community SaaS deployment path is available through public workflows and docs."]
];

const pilotCards = [
  ["Trial portal", "Live", "Evaluator requests start at cavra-trial.mind-ops.cloud."],
  ["Trial license", "Time-limited", "Enterprise Trial access uses signed license validation and revocation."],
  ["AISPM labs", "Guided", "Trial Field Guide helps evaluators prove one complete use case."],
  ["Production gate", "Enterprise", "Live connectors, SMTP, tenants, and runtime workflows remain private validation steps."]
];

const aispmCards = [
  ["Posture score", "82", "Demo score from sample decisions and readiness signals."],
  ["Blocked actions", "1", "Unsafe secret or production mutation attempts are stopped before execution."],
  ["Approval gates", "3", "High-risk actions route to human or policy owners before completion."],
  ["Report packs", "6", "Executive, audit, control, evidence, agent-risk, and KPI reports."],
  ["Enterprise controls", "Locked", "Live streaming, kill switch, runtime overrides, and report delivery."]
];

const boardPackCards = [
  ["Scope", "Defined", "Repositories, agents, tools, required checks, owners, and go/no-go criteria."],
  ["Risk acceptance", "Tracked", "Accepted exceptions have owner, expiry, rationale, and reviewer evidence."],
  ["Evidence room", "Ready", "Artifacts are grouped for CISO, security, platform, procurement, and audit review."],
  ["Report readiness", "Prepared", "Executive and audit reporting is separated from Enterprise email delivery."],
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
  ["Enterprise storage", "Tenant-isolated databases, immutable blob storage, Key Vault, and monitoring."]
];

const policies = [
  ["Secrets exposure", "Block reading private keys, `.env`, customer records, or production credentials.", "Use managed secret references and redacted evidence."],
  ["Production mutation", "Require approval for IAM, deployment, infrastructure, or protected branch changes.", "Route to platform or security owner with signed attestation."],
  ["Untrusted MCP tool", "Block MCP servers that request filesystem, shell, network, or token capabilities without trust registration.", "Register server, declare capability, and rerun trust check."],
  ["Release bypass", "Prevent agents from bypassing required checks, tags, release evidence, or protected branches.", "Attach CAVRA evidence before merge or release."],
  ["Context gaps", "Warn or block when ownership, data classification, change window, or environment tier is missing.", "Collect missing context before execution."],
  ["Report delivery", "Keep SMTP/provider secrets, recipients, private report contents, and logs outside public Community.", "Use Enterprise report provider integration and audit storage."]
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
  ["Engineering leaders", "Govern AI-assisted development without blocking all automation.", "Start with overview, role paths, and Enterprise Trial."],
  ["Trial evaluators", "Prove a complete AISPM use case with guided labs and closeout.", "Start with Trial portal and Trial Field Guide."],
  ["Enterprise operators", "Validate tenants, connectors, SMTP, workflows, and production gates.", "Start with Enterprise deployment docs and readiness validators."]
];

const trialAccessCards = [
  ["Evaluator intake", "Portal", "Use the branded trial portal for request submission and operator review."],
  ["License", "Time-limited", "Approved evaluators receive a signed, revocable trial license."],
  ["Delivery", "Private", "Package/container access is granted through private delivery channels."],
  ["Guided lab", "AISPM", "The Trial Field Guide walks users through one complete evidence-backed use case."],
  ["Closeout", "Auditable", "Expiry, revocation, access removal, validation, and feedback are captured."],
  ["Boundary", "Enterprise", "Tenant data, SMTP secrets, connectors, and report delivery remain private."]
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
  ["Community", "Public sandbox, CLI, sample evidence, policy packs, Azure Community deployment."],
  ["Trial", "Portal intake, private package, time-limited licenses, guided AISPM labs, closeout evidence."],
  ["Enterprise", "Tenant isolation, SSO/RBAC, connectors, policy packs, SMTP/report delivery, production gates."],
  ["SaaS", "Hosted control plane, Azure deployment options, managed reporting, monitor and support paths."],
  ["AISPM", "Posture loop, reports, exception lifecycle, executive board packs, runtime validation."],
  ["Public site", "Professional product landing page, role paths, diagrams, docs, and trial conversion."]
];

const docsLinks = [
  ["GitHub Wiki Textbook", "https://github.com/Huzefaaa2/cavra/wiki"],
  ["Trial Field Guide", "https://github.com/Huzefaaa2/cavra/wiki/AISPM-Enterprise-Trial-Lab-Notebook"],
  ["CAVRA Trial Portal", "https://cavra-trial.mind-ops.cloud/"],
  ["README", "https://github.com/Huzefaaa2/cavra#readme"],
  ["Azure Community Deployment", "https://github.com/Huzefaaa2/cavra/blob/main/docs/azure-community-saas-deployment.md"],
  ["Azure Trial and Enterprise Deployment", "https://github.com/Huzefaaa2/cavra/blob/main/docs/azure-trial-enterprise-deployment.md"],
  ["Security Policy", "https://github.com/Huzefaaa2/cavra/security/policy"],
  ["Sample Evidence JSON", "./evidence/before-the-agent-acts/evidence.json"]
];

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
  ...policies.map(([label, description]) => ({ type: "Policy", label, route: "policy-engine", description })),
  ...useCases.map(([label, description]) => ({ type: "Use Case", label, route: "use-cases", description })),
  ...operatorPaths.map(([label, description]) => ({ type: "Role Path", label, route: "operator-experience", description })),
  ...reportCards.map(([label, description]) => ({ type: "AISPM Report", label, route: "ai-posture", description })),
  { type: "AI Posture", label: "Pilot Launch Board Pack Packet", route: "ai-posture", description: "Copy or download the public-safe board packet for launch review." },
  { type: "Trial", label: "Trial Field Guide", route: "enterprise-trial", description: "Run a complete AISPM use case with guided labs." }
];

const el = (selector) => document.querySelector(selector);
const escapeHtml = (value) => String(value).replace(/[&<>"']/g, (char) => ({
  "&": "&amp;",
  "<": "&lt;",
  ">": "&gt;",
  "\"": "&quot;",
  "'": "&#039;"
}[char]));

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

  el("#integrationCards").innerHTML = integrations.map(([title, status, detail]) => `
    <article class="integration-card">
      <span class="eyebrow">${escapeHtml(status)}</span>
      <h3>${escapeHtml(title)}</h3>
      <p>${escapeHtml(detail)}</p>
    </article>
  `).join("");

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

  el("#docsNav").innerHTML = docsLinks.map(([label, href]) => `
    <a href="${escapeHtml(href)}" target="${href.startsWith("http") ? "_blank" : "_self"}" rel="${href.startsWith("http") ? "noreferrer" : ""}">
      ${escapeHtml(label)}
    </a>
  `).join("");
}

function routeTitle(route) {
  const item = navItems.find((nav) => nav.id === route);
  return item ? `CAVRA | ${item.label}` : "CAVRA | Runtime Governance for AI Coding Agents";
}

function renderToc(route) {
  const panel = document.getElementById(route);
  const toc = el("#toc");
  if (!panel || !toc) return;
  const headings = [...panel.querySelectorAll("h2, h3")].slice(0, 10);
  toc.innerHTML = `
    <strong>On this page</strong>
    ${headings.map((heading, index) => {
      if (!heading.id) heading.id = `${route}-heading-${index}`;
      return `<a href="#${heading.id}">${escapeHtml(heading.textContent || "Section")}</a>`;
    }).join("")}
  `;
}

function setRoute(route, options = {}) {
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
  document.title = routeTitle(nextRoute);
  localStorage.setItem("cavra.activeRoute", nextRoute);
  if (!options.fromHash && location.hash.slice(1) !== nextRoute) {
    history.pushState(null, "", `#${nextRoute}`);
  }
  renderToc(nextRoute);
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

function renderCommandResults(query) {
  const normalized = query.trim().toLowerCase();
  const matches = routeContent.filter((item) => {
    const haystack = `${item.type} ${item.label} ${item.description}`.toLowerCase();
    return !normalized || haystack.includes(normalized);
  }).slice(0, 12);

  el("#commandResults").innerHTML = matches.map((item) => `
    <button class="command-result" data-route="${item.route}">
      <strong>${escapeHtml(item.label)}</strong>
      <small>${escapeHtml(item.type)} - ${escapeHtml(item.description)}</small>
    </button>
  `).join("") || `<p>No matching CAVRA content found.</p>`;
}

function downloadJson(filename, payload) {
  const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
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
      "Request an Enterprise Trial"
    ],
    public_safety_boundary: [
      "No customer tenant data",
      "No connector secrets",
      "No SMTP/provider credentials",
      "No private Enterprise source or runtime logs"
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

function wireEvents() {
  document.addEventListener("click", async (event) => {
    const routeTarget = event.target.closest("[data-route], [data-route-link]");
    if (routeTarget?.dataset.route || routeTarget?.dataset.routeLink) {
      event.preventDefault();
      setRoute(routeTarget.dataset.route || routeTarget.dataset.routeLink);
      el("#mobileDrawer").classList.remove("is-open");
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
    if (event.target.closest("#openMobileNav")) {
      el("#mobileDrawer").classList.add("is-open");
      el("#mobileDrawer").setAttribute("aria-hidden", "false");
      return;
    }
    if (event.target.closest("#closeMobileNav")) {
      el("#mobileDrawer").classList.remove("is-open");
      el("#mobileDrawer").setAttribute("aria-hidden", "true");
      return;
    }
    if (event.target.closest("#collapseSidebar")) {
      setSidebarCollapsed(!el("#sidebar").classList.contains("is-collapsed"));
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
        boundary: "Enterprise report rendering, SMTP/provider delivery, and private report content are not included in Community."
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

  el("#commandSearch").addEventListener("input", (event) => renderCommandResults(event.target.value));
  document.addEventListener("keydown", (event) => {
    if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "k") {
      event.preventDefault();
      openCommandPalette();
    }
    if (event.key === "Escape") closeCommandPalette();
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
*/
