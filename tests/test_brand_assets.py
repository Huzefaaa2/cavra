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
        'id="integrationCards"',
        'id="complianceRows"',
        'id="useCaseCards"',
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
        "#documentation",
        "#roadmap",
    ]:
        assert route in html or route.strip("#") in js

    for feature in [
        "Ctrl+K",
        "renderCommandResults",
        "renderArchitecture",
        "renderCompliance",
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
