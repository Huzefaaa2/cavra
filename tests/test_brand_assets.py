import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path


class _HTMLSmokeParser(HTMLParser):
    pass


def test_brand_assets_exist_for_readme_sandbox_and_social_preview() -> None:
    required_assets = [
        "assets/brand/cavra-mark.svg",
        "assets/brand/favicon.svg",
        "assets/brand/cavra-logo-horizontal.svg",
        "assets/brand/cavra-logo-stacked.svg",
        "assets/brand/cavra-thumbnail.svg",
        "assets/brand/cavra-github-social-preview.svg",
        "assets/brand/png/cavra-mark-64.png",
        "assets/brand/png/cavra-mark-128.png",
        "assets/brand/png/cavra-mark-256.png",
        "assets/brand/png/cavra-mark-512.png",
        "assets/brand/png/cavra-logo-horizontal-1024.png",
        "assets/brand/png/cavra-thumbnail-1280x640.png",
        "assets/brand/png/cavra-github-social-preview-1200x630.png",
        "apps/sandbox-ui/brand/favicon.svg",
        "apps/sandbox-ui/brand/cavra-mark.svg",
        "apps/sandbox-ui/brand/cavra-logo-horizontal.svg",
    ]
    for asset in required_assets:
        assert Path(asset).is_file(), asset


def test_brand_svg_assets_are_valid_svg_documents() -> None:
    for asset in Path("assets/brand").glob("*.svg"):
        text = asset.read_text(encoding="utf-8")
        assert text.startswith("<svg"), asset
        assert "</svg>" in text, asset
        assert "<title" in text or "aria-label" in text, asset


def test_readme_and_sandbox_reference_brand_assets() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")
    html = Path("apps/sandbox-ui/index.html").read_text(encoding="utf-8")
    css = Path("apps/sandbox-ui/styles.css").read_text(encoding="utf-8")

    _HTMLSmokeParser().feed(html)
    assert "assets/brand/cavra-logo-horizontal.svg" in readme
    assert "assets/brand/png/cavra-github-social-preview-1200x630.png" in readme
    assert './brand/favicon.svg' in html
    assert './brand/cavra-mark.svg' in html
    assert 'class="brand"' not in html
    assert '<a class="brand"' not in html
    assert 'class="hero-title-block"' in html
    assert 'class="hero-wordmark">CAVRA<' in html
    assert 'class="hero-side"' in html
    assert 'class="hero-logo-lockup"' in html
    assert 'id="demoMetrics"' in html
    assert 'id="communityGaSummary"' in html
    assert 'id="communityGaChecklist"' in html
    assert 'id="communityGaCommands"' in html
    assert 'id="communityGaLinks"' in html
    assert 'id="refreshCommunityGa"' in html
    assert 'id="releaseNotes"' in html
    assert 'class="console saas-automation-console"' in html
    assert 'id="refreshSaasAutomation"' in html
    assert 'id="saasAutomationSummary"' in html
    assert 'id="saasAutomationChecks"' in html
    assert 'id="saasAutomationRequest"' in html
    assert 'id="saasAutomationResponse"' in html
    assert "hero-metrics" in css
    assert "metric-card" in css
    assert "community-ga-grid" in css
    assert "community-ga-layout" in css
    assert "release-note-grid" in css
    assert "release-note-links" in css
    assert "saas-automation-grid" in css
    assert "saas-contract-payload" in css
    assert 'class="hero-product-mark"' in html
    assert 'width="220" height="220"' in html
    assert ".hero-side { position: absolute;" in css


def test_sandbox_is_portal_style_developer_experience() -> None:
    html = Path("apps/sandbox-ui/index.html").read_text(encoding="utf-8")
    css = Path("apps/sandbox-ui/styles.css").read_text(encoding="utf-8")
    js = Path("apps/sandbox-ui/sandbox.js").read_text(encoding="utf-8")
    docs = Path("docs/sandbox-portal-redesign.md").read_text(encoding="utf-8")
    wiki_home = Path("docs/wiki/Home.md").read_text(encoding="utf-8")

    _HTMLSmokeParser().feed(html)

    required_html = [
        'class="top-shell"',
        'id="portalNav"',
        'class="sidebar"',
        'id="toc"',
        'id="commandPalette"',
        'id="mobileDrawer"',
        'class="mobile-bottom"',
        'id="architectureMap"',
        'id="nodeInspector"',
        'id="policyExplorer"',
        'id="evidenceTimeline"',
        'id="refreshAispmApprovals"',
        'id="aispmApprovalSummary"',
        'id="aispmApprovalLineage"',
        'id="refreshAispmFingerprints"',
        'id="aispmFingerprintSummary"',
        'id="aispmBehaviorFingerprints"',
        'id="aispmTraceSession"',
        'id="aispmTraceSummary"',
        'id="aispmTraceSteps"',
        'id="aispmTraceRedaction"',
        'id="aispmTracePayload"',
        'id="integrationCards"',
        'id="complianceRows"',
        'id="useCaseCards"',
        'id="operatorPathCards"',
        'id="docsNav"',
        'id="roadmapBoard"',
    ]
    for item in required_html:
        assert item in html

    for route in [
        "#dashboard",
        "#architecture",
        "#policy-engine",
        "#evidence",
        "#integrations",
        "#compliance",
        "#use-cases",
        "#operator-experience",
        "#documentation",
        "#roadmap",
    ]:
        assert route in html or route.strip("#") in js

    for feature in [
        "Ctrl+K",
        "renderCommandResults",
        "renderArchitecture",
        "renderAispmApprovalLineage",
        "renderAispmBehaviorFingerprints",
        "renderAispmTraceReplay",
        "renderCompliance",
        "renderOperatorPaths",
        "mobile-bottom",
        "CAVRA Developer Portal Redesign",
    ]:
        assert feature in html or feature in css or feature in js or feature in docs

    assert "@media (max-width: 900px)" in css
    assert "CAVRA-Developer-Portal-Redesign.md" in wiki_home
    assert "Next.js" in docs
    assert "shadcn/ui" in docs
    assert "Framer Motion" in docs
    assert "Lucide Icons" in docs


def test_sandbox_portal_smoke_validator_is_linked_and_enforced() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")
    changelog = Path("CHANGELOG.md").read_text(encoding="utf-8")
    wiki_home = Path("docs/wiki/Home.md").read_text(encoding="utf-8")
    docs = Path("docs/sandbox-portal-smoke-validation.md").read_text(encoding="utf-8")
    wiki_docs = Path("docs/wiki/CAVRA-Developer-Portal-Smoke-Validation.md").read_text(
        encoding="utf-8"
    )
    production_roadmap = Path("docs/production-roadmap.md").read_text(encoding="utf-8")
    next_slice = Path("docs/roadmap-status-next-slice.md").read_text(encoding="utf-8")
    workflows = {
        "community-ci": Path(".github/workflows/community-ci.yml").read_text(
            encoding="utf-8"
        ),
        "security-scan": Path(".github/workflows/security-scan.yml").read_text(
            encoding="utf-8"
        ),
        "release-community": Path(".github/workflows/release-community.yml").read_text(
            encoding="utf-8"
        ),
        "governance": Path(".github/workflows/cavra-governance.yml").read_text(
            encoding="utf-8"
        ),
        "deploy-sandbox": Path(".github/workflows/deploy-sandbox.yml").read_text(
            encoding="utf-8"
        ),
    }

    assert "docs/sandbox-portal-smoke-validation.md" in readme
    assert "CAVRA-Developer-Portal-Smoke-Validation.md" in wiki_home
    assert "developer portal smoke validation" in changelog
    assert "scripts/validate-sandbox-portal.py" in docs
    assert "scripts/validate-sandbox-portal.py" in wiki_docs
    assert "scripts/validate-sandbox-portal.py" in production_roadmap
    assert "Node 24 readiness" in next_slice

    for workflow in workflows.values():
        assert "python scripts/validate-sandbox-portal.py" in workflow

    result = subprocess.run(
        [sys.executable, "scripts/validate-sandbox-portal.py"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "CAVRA sandbox portal smoke validation passed." in result.stdout


def test_console_closeout_operator_experience_is_linked_and_enforced() -> None:
    html = Path("apps/sandbox-ui/index.html").read_text(encoding="utf-8")
    css = Path("apps/sandbox-ui/styles.css").read_text(encoding="utf-8")
    js = Path("apps/sandbox-ui/sandbox.js").read_text(encoding="utf-8")
    readme = Path("README.md").read_text(encoding="utf-8")
    changelog = Path("CHANGELOG.md").read_text(encoding="utf-8")
    wiki_home = Path("docs/wiki/Home.md").read_text(encoding="utf-8")
    docs = Path("docs/console-closeout-operator-experience.md").read_text(
        encoding="utf-8"
    )
    wiki_docs = Path("docs/wiki/Console-Closeout-Operator-Experience.md").read_text(
        encoding="utf-8"
    )
    production_roadmap = Path("docs/production-roadmap.md").read_text(encoding="utf-8")
    workflows = [
        Path(".github/workflows/community-ci.yml").read_text(encoding="utf-8"),
        Path(".github/workflows/security-scan.yml").read_text(encoding="utf-8"),
        Path(".github/workflows/release-community.yml").read_text(encoding="utf-8"),
        Path(".github/workflows/cavra-governance.yml").read_text(encoding="utf-8"),
        Path(".github/workflows/deploy-sandbox.yml").read_text(encoding="utf-8"),
    ]

    assert 'id="operator-experience"' in html
    assert 'id="operatorPathCards"' in html
    assert ".operator-path-grid" in css
    assert "operatorPaths" in js
    assert "renderOperatorPaths" in js
    assert 'type: "Operator Path"' in js

    for persona in ["Prospect", "Auditor", "Platform Team", "CISO"]:
        assert persona in js
        assert persona in docs
        assert persona in wiki_docs

    assert "docs/console-closeout-operator-experience.md" in readme
    assert "Console-Closeout-Operator-Experience.md" in wiki_home
    assert "console closeout operator experience" in changelog
    assert "scripts/validate-console-closeout.py" in production_roadmap

    for workflow in workflows:
        assert "python scripts/validate-console-closeout.py" in workflow

    result = subprocess.run(
        [sys.executable, "scripts/validate-console-closeout.py"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "CAVRA console closeout validation passed." in result.stdout
