#!/usr/bin/env python3
"""Validate the public CAVRA sandbox portal contract."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require_file(path: str, failures: list[str]) -> None:
    if not (ROOT / path).is_file():
        failures.append(f"missing required file: {path}")


def require(text: str, needle: str, label: str, failures: list[str]) -> None:
    if needle not in text:
        failures.append(f"missing {label}: {needle}")


def require_any(texts: list[str], needle: str, label: str, failures: list[str]) -> None:
    if not any(needle in text for text in texts):
        failures.append(f"missing {label}: {needle}")


def main() -> int:
    failures: list[str] = []
    required_files = [
        "apps/sandbox-ui/index.html",
        "apps/sandbox-ui/styles.css",
        "apps/sandbox-ui/sandbox.js",
        "apps/sandbox-ui/brand/favicon.svg",
        "apps/sandbox-ui/brand/cavra-mark.svg",
        "apps/sandbox-ui/brand/cavra-logo-horizontal.svg",
        "assets/brand/cavra-logo-horizontal.svg",
        "docs/diagrams/c4-container.svg",
        ".github/workflows/deploy-sandbox.yml",
        "docs/sandbox-portal-redesign.md",
        "docs/sandbox-portal-smoke-validation.md",
        "docs/wiki/CAVRA-Developer-Portal-Redesign.md",
        "docs/wiki/CAVRA-Developer-Portal-Smoke-Validation.md",
    ]
    for path in required_files:
        require_file(path, failures)

    if failures:
        for failure in failures:
            print(failure)
        return 1

    html = read("apps/sandbox-ui/index.html")
    css = read("apps/sandbox-ui/styles.css")
    js = read("apps/sandbox-ui/sandbox.js")
    deploy = read(".github/workflows/deploy-sandbox.yml")
    readme = read("README.md")
    wiki_home = read("docs/wiki/Home.md")
    redesign_doc = read("docs/sandbox-portal-redesign.md")
    smoke_doc = read("docs/sandbox-portal-smoke-validation.md")
    wiki_smoke_doc = read("docs/wiki/CAVRA-Developer-Portal-Smoke-Validation.md")

    routes = [
        "dashboard",
        "ai-posture",
        "architecture",
        "policy-engine",
        "evidence",
        "integrations",
        "compliance",
        "use-cases",
        "operator-experience",
        "enterprise-trial",
        "documentation",
        "roadmap",
    ]
    for route in routes:
        require_any([html, js], route, "portal route", failures)

    required_html = [
        'class="top-shell"',
        'class="sidebar"',
        'class="portal-shell"',
        'class="portal-main"',
        'class="mobile-bottom"',
        'class="command-palette"',
        'class="architecture-workbench"',
        'id="portalNav"',
        'id="mobileNav"',
        'id="toc"',
        'id="commandPalette"',
        'id="commandSearch"',
        'id="commandResults"',
        'id="mobileDrawer"',
        'id="openMobileNav"',
        'id="closeMobileNav"',
        'id="mobileSearch"',
        'id="themeSelect"',
        'id="mobileThemeSelect"',
        "data-theme-select",
        'id="architectureMap"',
        'id="nodeInspector"',
        'id="aispmSourceBadge"',
        'id="refreshAispm"',
        'id="aispmOverviewCards"',
        'id="aispmAgentCards"',
        'id="aispmFindings"',
        'id="aispmControlCoverage"',
        'id="aispmNearMisses"',
        'id="refreshAispmContextGaps"',
        'id="aispmContextGapSummary"',
        'id="aispmPolicyContextGaps"',
        'id="refreshAispmForecasts"',
        'id="aispmForecastSummary"',
        'id="aispmPreActionForecasts"',
        'id="refreshAispmIntentDrift"',
        'id="aispmIntentDriftSummary"',
        'id="aispmIntentActionDrift"',
        'id="refreshAispmToolGraph"',
        'id="aispmToolGraphSummary"',
        'id="aispmToolGraphNodes"',
        'id="aispmToolGraphEdges"',
        'id="refreshAispmBlastRadius"',
        'id="aispmBlastRadiusSummary"',
        'id="aispmAgentBlastRadius"',
        'id="refreshAispmCoverageHeatmap"',
        'id="aispmCoverageHeatmapSummary"',
        'id="aispmCoverageHeatmapRows"',
        'id="refreshAispmEvidenceConfidence"',
        'id="aispmEvidenceConfidenceSummary"',
        'id="aispmEvidenceConfidenceRows"',
        'id="refreshAispmEvidenceFreshness"',
        'id="aispmEvidenceFreshnessSummary"',
        'id="aispmEvidenceFreshnessRows"',
        'id="refreshAispmExecutiveNarrative"',
        'id="aispmExecutiveNarrativeSummary"',
        'id="aispmExecutiveNarrative"',
        'id="refreshAispmReplayPolicy"',
        'id="aispmReplayPolicySummary"',
        'id="aispmReplayPolicyReviewWorkflow"',
        'id="aispmReplayPolicyRecommendations"',
        'id="aispmReplayPolicyDraft"',
        'id="aispmReplayPolicyTestStatus"',
        'id="copyAispmReplayPolicyTests"',
        'id="downloadAispmReplayPolicyTests"',
        'id="aispmReplayPolicyTests"',
        'id="refreshAispmFingerprints"',
        'id="aispmFingerprintSummary"',
        'id="aispmBehaviorFingerprints"',
        'id="aispmTimeline"',
        'id="refreshAispmApprovals"',
        'id="aispmApprovalSummary"',
        'id="aispmApprovalLineage"',
        'id="aispmTraceSession"',
        'id="aispmTraceStatus"',
        'id="aispmTraceSummary"',
        'id="aispmTraceSteps"',
        'id="aispmTraceRedaction"',
        'id="aispmTracePayload"',
        'id="aispmPayload"',
        'id="policyExplorer"',
        'id="evidenceTimeline"',
        'id="integrationCards"',
        'id="complianceFilter"',
        'id="complianceFramework"',
        'id="complianceRows"',
        'id="useCaseCards"',
        'id="operatorPathCards"',
        'id="trialAccessCards"',
        'id="docsNav"',
        'id="roadmapBoard"',
    ]
    for needle in required_html:
        require(html, needle, "portal DOM contract", failures)

    for needle in [
        "routeContent",
        "renderCommandResults",
        "openCommandPalette",
        'type: "Page"',
        'type: "Policy"',
        'type: "Integration"',
        'type: "Control"',
        'type: "Use Case"',
        'type: "Operator Path"',
        'type: "Enterprise Trial"',
        'type: "AI Posture"',
        "applyTheme",
        "normalizeTheme",
        "[data-theme-select]",
    ]:
        require(js, needle, "command palette contract", failures)
    require_any([html, js], "Ctrl K", "command palette shortcut label", failures)

    for needle in [
        "@media (max-width: 900px)",
        ".mobile-bottom",
        ".mobile-drawer",
        ".theme-picker",
        'body[data-theme="classic"]',
        'body[data-theme="retro"]',
        'body[data-theme="executive"]',
        ".fixture-export-actions",
        ".review-workflow-panel",
        ".review-checklist",
        ".action-buttons",
    ]:
        require(css, needle, "mobile portal CSS", failures)

    for needle in [
        "GitHub",
        "GitLab",
        "Terraform / OpenTofu",
        "Kubernetes",
        "CAVRA",
        "Policy Engine",
        "Evidence Engine",
        "Audit Trail",
        "AWS / Azure / GCP",
        "renderArchitecture",
        "renderNodeInspector",
        "renderAispmDashboard",
        "renderAispmApprovalLineage",
        "loadAispmApprovalLineage",
        "renderAispmBehaviorFingerprints",
        "loadAispmBehaviorFingerprints",
        "renderAispmPolicyContextGaps",
        "loadAispmPolicyContextGaps",
        "renderAispmPreActionForecasts",
        "loadAispmPreActionForecasts",
        "renderAispmIntentActionDrift",
        "loadAispmIntentActionDrift",
        "renderAispmToolChainGraph",
        "loadAispmToolChainGraph",
        "renderAispmAgentBlastRadius",
        "loadAispmAgentBlastRadius",
        "renderAispmControlCoverageHeatmap",
        "loadAispmControlCoverageHeatmap",
        "renderAispmExecutiveNarrative",
        "loadAispmExecutiveNarrative",
        "renderAispmReplayPolicy",
        "loadAispmReplayPolicy",
        "renderAispmReplayPolicyTests",
        "loadAispmReplayPolicyTests",
        "renderAispmReplayPolicyReviewWorkflow",
        "copyAispmReplayPolicyTests",
        "downloadAispmReplayPolicyTests",
        "copyTextToClipboard",
        "cavra-replay-policy-tests.json",
        "renderAispmTraceReplay",
        "loadAispmTraceReplay",
        "loadAispmDashboard",
        "/aispm/posture",
        "/aispm/replay-to-policy-draft",
        "/aispm/replay-to-policy-tests",
        "/aispm/approval-lineage",
        "/aispm/behavior-fingerprints",
        "/aispm/policy-context-gaps",
        "/aispm/pre-action-risk-forecasts",
        "/aispm/intent-action-drift",
        "/aispm/tool-chain-graph",
        "/aispm/agent-blast-radius",
        "/aispm/control-coverage-heatmap",
        "/aispm/evidence-confidence",
        "/aispm/evidence-freshness",
        "/aispm/executive-risk-narrative",
        "/aispm/trace-replay/",
        "approval_lineage",
        "behavior_fingerprints",
        "policy_context_gaps",
        "pre_action_risk_forecasts",
        "intent_action_drift",
        "tool_chain_graph",
        "agent_blast_radius",
        "control_coverage_heatmap",
        "evidence_confidence_drilldown",
        "evidence_freshness_slo",
        "executive_risk_narrative",
        "control_coverage",
        "near_misses",
        "trace_replay",
        "requires_cavra_enterprise",
    ]:
        require(js, needle, "architecture node contract", failures)

    for needle in [
        "renderCompliance",
        "NIST",
        "SOC2",
        "ISO27001",
        "CIS",
        "PCI DSS",
        "OWASP",
    ]:
        require_any([html, js], needle, "compliance filter contract", failures)

    workflow_needles = [
        "node --check apps/sandbox-ui/config.js",
        "node --check apps/sandbox-ui/sandbox.js",
        "python scripts/validate-sandbox-portal.py",
        "CAVRA_PUBLIC_TRIAL_API_URL",
        'grep -q "Evidence Console"',
        'grep -q "Community GA Control Hardening"',
        'grep -q "Production Pilot Readiness"',
        'grep -q "Enterprise Trial Access Portal"',
        'grep -q "https://cavra-trial.mind-ops.cloud/"',
        "sandbox.js",
        "styles.css",
        "brand/cavra-mark.svg",
        "assets/brand/cavra-logo-horizontal.svg",
        "c4-container.svg",
        "evidence/before-the-agent-acts/evidence.json",
        "evidence/final-closeout-trial/sample-evidence-package.json",
        "evidence/final-closeout-trial/pilot-intake-template.json",
    ]
    for needle in workflow_needles:
        require(deploy, needle, "GitHub Pages smoke workflow", failures)

    for needle in [
        "./brand/favicon.svg",
        "./brand/cavra-mark.svg",
        "class=\"hero-product-mark\"",
        "Evidence Console",
        "Community GA Control Hardening",
        "Production Pilot Readiness",
        "Enterprise Trial Access Portal",
        "https://cavra-trial.mind-ops.cloud/",
        "Open CAVRA Trial Portal",
    ]:
        require(html, needle, "brand and page signal", failures)

    for needle in [
        "trialAccessCards",
        "renderTrialAccess",
    ]:
        require(js, needle, "Enterprise Trial portal contract", failures)

    require(readme, "docs/sandbox-portal-redesign.md", "README portal redesign link", failures)
    require(
        readme,
        "docs/sandbox-portal-smoke-validation.md",
        "README portal smoke validation link",
        failures,
    )
    require(
        wiki_home,
        "CAVRA-Developer-Portal-Redesign.md",
        "wiki portal redesign link",
        failures,
    )
    require(
        wiki_home,
        "CAVRA-Developer-Portal-Smoke-Validation.md",
        "wiki portal smoke validation link",
        failures,
    )

    for doc in [redesign_doc, smoke_doc, wiki_smoke_doc]:
        require(
            doc,
            "Node 24 readiness",
            "GA path next recommendation",
            failures,
        )

    if failures:
        print("CAVRA sandbox portal smoke validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("CAVRA sandbox portal smoke validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
