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
    assert '<a class="brand"' not in html
    assert 'width="34" height="34"' in html
    assert 'class="hero-side"' in html
    assert 'class="hero-product-mark"' in html
    assert 'width="220" height="220"' in html
    assert ".hero-side { position: absolute;" in css
