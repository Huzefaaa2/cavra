import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "playwright";

const baseUrl = "http://localhost:5173/";
const outDir = path.resolve("gui-audit");
const screenshotDir = path.join(outDir, "screenshots");

const sanitize = (value) =>
  String(value || "screen")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "")
    .slice(0, 80);

const escapeSelector = (value) => String(value).replace(/([ #;?%&,.+*~':"!^$[\]()=>|/@])/g, "\\$1");

async function ensureDirs() {
  await fs.mkdir(screenshotDir, { recursive: true });
}

async function visibleText(page, selector) {
  return page.$$eval(selector, (elements) =>
    elements
      .filter((element) => {
        const style = window.getComputedStyle(element);
        const rect = element.getBoundingClientRect();
        return style.visibility !== "hidden" && style.display !== "none" && rect.width > 0 && rect.height > 0;
      })
      .map((element) => ({
        text: (element.innerText || element.textContent || "").trim().replace(/\s+/g, " "),
        href: element.getAttribute("href"),
        route: element.getAttribute("data-route-link") || element.getAttribute("data-route"),
        id: element.id || "",
        tag: element.tagName.toLowerCase(),
      }))
  );
}

async function getRouteCandidates(page) {
  const panelRoutes = await page.$$eval(".page-panel[id]", (nodes) =>
    nodes.map((node) => ({ route: node.id, label: node.getAttribute("data-title") || node.id }))
  );
  return panelRoutes;
}

async function collectScreen(page, route, label, viewportName) {
  const routeUrl = `${baseUrl}#${route}`;
  const network = [];
  const onRequest = (request) => {
    network.push({
      type: "request",
      method: request.method(),
      url: request.url(),
      resourceType: request.resourceType(),
    });
  };
  const onResponse = (response) => {
    network.push({
      type: "response",
      status: response.status(),
      url: response.url(),
    });
  };
  page.on("request", onRequest);
  page.on("response", onResponse);

  await page.goto(routeUrl, { waitUntil: "domcontentloaded" });
  await page.waitForTimeout(250);

  const screenshotPath = path.join(screenshotDir, `${sanitize(route)}-${viewportName}.png`);
  await page.screenshot({ path: screenshotPath, fullPage: true });

  const headingOutline = await page.$$eval("h1,h2,h3", (headings) =>
    headings
      .filter((heading) => {
        const rect = heading.getBoundingClientRect();
        const style = window.getComputedStyle(heading);
        return style.display !== "none" && style.visibility !== "hidden" && rect.width > 0 && rect.height > 0;
      })
      .map((heading) => ({
        level: heading.tagName.toLowerCase(),
        text: (heading.innerText || heading.textContent || "").trim().replace(/\s+/g, " "),
      }))
  );

  const staticIndicators = await page.$$eval("body *", (elements) => {
    const patterns = [
      /sample data/i,
      /public demo/i,
      /placeholder/i,
      /configured by provider/i,
      /request trial/i,
      /book a demo/i,
      /learn more/i,
      /pricing/i,
      /product paths/i,
      /before the agent acts/i,
      /marketing/i,
    ];
    return elements
      .map((element) => (element.innerText || element.textContent || "").trim().replace(/\s+/g, " "))
      .filter((text) => text && text.length < 180 && patterns.some((pattern) => pattern.test(text)))
      .slice(0, 25);
  });

  const interactiveElements = await page.$$eval(
    "a,button,input,select,textarea,[role='button'],[tabindex]",
    (elements) =>
      elements
        .filter((element) => {
          const style = window.getComputedStyle(element);
          const rect = element.getBoundingClientRect();
          return style.visibility !== "hidden" && style.display !== "none" && rect.width > 0 && rect.height > 0;
        })
        .map((element, index) => ({
          index,
          tag: element.tagName.toLowerCase(),
          role: element.getAttribute("role") || "",
          type: element.getAttribute("type") || "",
          id: element.id || "",
          label:
            element.getAttribute("aria-label") ||
            element.getAttribute("title") ||
            element.innerText ||
            element.value ||
            element.getAttribute("placeholder") ||
            element.textContent ||
            "",
          href: element.getAttribute("href") || "",
          route: element.getAttribute("data-route-link") || element.getAttribute("data-route") || "",
          action: element.getAttribute("data-setup-action") || "",
          disabled: Boolean(element.disabled) || element.getAttribute("aria-disabled") === "true",
        }))
  );

  const clickResults = interactiveElements.map((element) => {
    const label = String(element.label || element.route || element.action || element.href || element.id).trim().replace(/\s+/g, " ");
    if (element.disabled) return { label, verdict: "disabled" };
    if (element.action) return { label, verdict: "likely-functional-api-action", reason: `setup action ${element.action}` };
    if (element.route || (element.href && element.href.startsWith("#"))) return { label, verdict: "functional-navigation" };
    if (element.href && /^https?:/.test(element.href)) return { label, verdict: "external-navigation" };
    if (element.tag === "select" || element.tag === "input" || element.tag === "textarea") return { label, verdict: "input-control" };
    return { label, verdict: "needs-manual-click-verification" };
  });

  page.off("request", onRequest);
  page.off("response", onResponse);

  const apiRequests = network.filter((entry) => /localhost:8000|\/(setup|aispm|approvals|evidence|agents|mcp|console)\b/.test(entry.url));
  const websitePatternNote = staticIndicators.length || headingOutline.some((heading) => /Before the agent acts|Runtime Authority|Why Enterprises|Product paths|Trial/.test(heading.text))
    ? "Contains promotional/product-site language or static explanatory panels; needs stronger operator-console focus."
    : "Mostly application-oriented content.";

  return {
    route,
    label,
    url: routeUrl,
    viewport: viewportName,
    screenshot: path.relative(".", screenshotPath),
    headingOutline,
    interactiveElements: interactiveElements.map((element) => ({
      ...element,
      label: String(element.label || "").trim().replace(/\s+/g, " ").slice(0, 160),
      functionalVerdict:
        clickResults.find((result) => result.label === String(element.label || element.route || element.action || element.href || element.id).trim().replace(/\s+/g, " "))?.verdict ||
        (element.disabled ? "disabled" : "not-tested"),
    })),
    clickResults,
    networkRequests: network,
    apiBacked: apiRequests.length > 0,
    apiRequestSummary: [...new Set(apiRequests.map((entry) => `${entry.type}:${entry.method || entry.status}:${entry.url}`))],
    staticOrPlaceholderIndicators: staticIndicators,
    websitePatternNote,
  };
}

async function main() {
  await ensureDirs();
  const browser = await chromium.launch();
  const desktop = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  const mobile = await browser.newPage({ viewport: { width: 390, height: 900 }, isMobile: true });

  await desktop.goto(baseUrl, { waitUntil: "networkidle" });
  const routes = await getRouteCandidates(desktop);
  const uniqueRoutes = [];
  for (const route of [{ route: "dashboard", label: "Overview" }, ...routes]) {
    if (!uniqueRoutes.find((entry) => entry.route === route.route)) uniqueRoutes.push(route);
  }

  const desktopScreens = [];
  for (const { route, label } of uniqueRoutes) {
    desktopScreens.push(await collectScreen(desktop, route, label, "desktop"));
  }

  const mobileScreens = [];
  for (const routeInfo of uniqueRoutes.filter((entry) => ["dashboard", "first-run-setup", "ai-posture"].includes(entry.route))) {
    mobileScreens.push(await collectScreen(mobile, routeInfo.route, routeInfo.label, "mobile"));
  }

  const findings = {
    generatedAt: new Date().toISOString(),
    target: baseUrl,
    routeCount: uniqueRoutes.length,
    routes: uniqueRoutes,
    screens: [...desktopScreens, ...mobileScreens],
    summary: {
      apiBackedScreens: desktopScreens.filter((screen) => screen.apiBacked).map((screen) => screen.route),
      staticScreens: desktopScreens.filter((screen) => !screen.apiBacked).map((screen) => screen.route),
      routesWithMarketingPatterns: desktopScreens
        .filter((screen) => /promotional|product-site|static explanatory/.test(screen.websitePatternNote))
        .map((screen) => screen.route),
    },
  };

  await fs.writeFile(path.join(outDir, "findings.json"), JSON.stringify(findings, null, 2));
  await browser.close();
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
