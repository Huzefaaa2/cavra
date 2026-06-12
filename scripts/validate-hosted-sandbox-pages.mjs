#!/usr/bin/env node
import { mkdirSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(__dirname, "..");
const screenshotDir = path.join(repoRoot, ".cavra", "hosted-smoke");

function normalizeBaseUrl(value) {
  const base = value || "https://huzefaaa2.github.io/cavra/";
  return base.endsWith("/") ? base : `${base}/`;
}

const baseUrl = normalizeBaseUrl(process.env.CAVRA_SANDBOX_URL);

async function assertFetchOk(url, label) {
  const response = await fetch(url, { redirect: "follow" });
  if (!response.ok) {
    throw new Error(`${label} returned HTTP ${response.status}: ${url}`);
  }
  return response.text();
}

async function assertVisible(page, selectors) {
  for (const selector of selectors) {
    await page.locator(selector).first().waitFor({ state: "visible", timeout: 15_000 });
  }
}

async function assertNoConsoleErrors(page, failures) {
  page.on("pageerror", (error) => failures.push(`page error: ${error.message}`));
  page.on("console", (message) => {
    if (message.type() === "error") {
      failures.push(`console error: ${message.text()}`);
    }
  });
}

async function assertReadableAndContained(page, selector) {
  const failures = await page.locator(selector).evaluateAll((nodes) => {
    const nodeFailures = [];
    for (const node of nodes) {
      const rect = node.getBoundingClientRect();
      const style = window.getComputedStyle(node);
      if (rect.width === 0 || rect.height === 0) continue;
      if (style.visibility === "hidden" || style.display === "none") continue;
      if (node.scrollWidth > node.clientWidth + 4) {
        nodeFailures.push(`${node.textContent.trim().replace(/\s+/g, " ").slice(0, 72)} overflows horizontally`);
      }
      if (rect.left < -4 || rect.right > window.innerWidth + 4) {
        nodeFailures.push(`${node.textContent.trim().replace(/\s+/g, " ").slice(0, 72)} escapes viewport`);
      }
      if (style.color === "transparent" || style.color === "rgba(0, 0, 0, 0)") {
        nodeFailures.push(`${node.tagName.toLowerCase()} has transparent text`);
      }
    }
    return nodeFailures;
  });
  if (failures.length) {
    throw new Error(`${selector} readability/containment failures:\n- ${failures.join("\n- ")}`);
  }
}

async function capture(page, name) {
  mkdirSync(screenshotDir, { recursive: true });
  const filePath = path.join(screenshotDir, name);
  await page.screenshot({ path: filePath, fullPage: true });
  return filePath;
}

async function validateHttpAssets() {
  const index = await assertFetchOk(baseUrl, "hosted index");
  for (const needle of [
    "Evidence Console",
    "Community GA Control Hardening",
    "Production Pilot Readiness",
    "Enterprise Trial Access Portal",
    "AISPM Trial Lab Notebook Readiness",
    "Release Evidence Index",
    "Hosted Release Operator Status",
    "CSO Report Center",
    "cavra-aispm-report-catalog-packet.json",
    "Report Delivery Setup Readiness",
    "cavra-aispm-report-delivery-setup-packet.json",
    "Report Operations Readiness",
    "cavra-aispm-report-operations-readiness-packet.json",
    "Report Governance Readiness",
    "cavra-aispm-report-governance-readiness-packet.json",
    "Report Assurance Readiness",
    "cavra-aispm-report-assurance-readiness-packet.json",
    "Report Response Readiness",
    "cavra-aispm-report-response-readiness-packet.json",
    "Report Trial Operations Readiness",
    "cavra-aispm-report-trial-operations-readiness-packet.json",
    "cavra-aispm-release-evidence-index-packet.json",
    "cavra-hosted-sandbox-operator-status-packet.json",
    "community-v1.0.0-aispm-release-evidence-index",
    "sandbox.js",
  ]) {
    if (!index.includes(needle)) {
      throw new Error(`hosted index missing ${needle}`);
    }
  }

  await assertFetchOk(new URL("sandbox.js", baseUrl).toString(), "hosted sandbox.js");
  await assertFetchOk(new URL("styles.css", baseUrl).toString(), "hosted styles.css");
  await assertFetchOk(new URL("config.js", baseUrl).toString(), "hosted config.js");
  await assertFetchOk(new URL("brand/cavra-mark.svg", baseUrl).toString(), "hosted CAVRA mark");
  await assertFetchOk(new URL("assets/brand/cavra-logo-horizontal.svg", baseUrl).toString(), "hosted horizontal logo");
  await assertFetchOk(new URL("c4-container.svg", baseUrl).toString(), "hosted C4 container diagram");
  await assertFetchOk(new URL("evidence/before-the-agent-acts/evidence.json", baseUrl).toString(), "hosted evidence sample");
  await assertFetchOk(new URL("evidence/final-closeout-trial/sample-evidence-package.json", baseUrl).toString(), "hosted final closeout evidence");
}

async function validateDashboard(page) {
  await page.setViewportSize({ width: 1440, height: 1100 });
  await page.goto("about:blank");
  await page.goto(`${baseUrl}#dashboard`, { waitUntil: "networkidle" });
  await page.locator("#dashboard.is-active").waitFor({ state: "visible", timeout: 15_000 });
  await page.selectOption("#themeSelect", "classic");
  await assertVisible(page, [
    ".hero-product-mark",
    "#demoMetrics .metric-card",
    "#communityGaSummary",
    "#pilotReadinessSummary",
  ]);
  await assertReadableAndContained(page, "#dashboard .metric-card, #dashboard .community-ga-card, #dashboard .pilot-readiness-card");
  return capture(page, "hosted-dashboard-classic.png");
}

async function validateAispm(page) {
  await page.setViewportSize({ width: 1440, height: 1200 });
  await page.goto("about:blank");
  await page.goto(`${baseUrl}#ai-posture`, { waitUntil: "networkidle" });
  await page.locator("#ai-posture.is-active").waitFor({ state: "visible", timeout: 15_000 });
  await assertVisible(page, [
    "#aispmOverviewCards .posture-card",
    "#aispmPilotLaunchBoardPack .board-pack-card",
    "#aispmPilotLaunchBoardPackManifest .board-pack-manifest-card",
    "#aispmReportCenter .report-card",
    "#sendAispmReportEmail:disabled",
  ]);
  await assertReadableAndContained(page, "#ai-posture .posture-card, #ai-posture .board-pack-card, #ai-posture .board-pack-manifest-card, #ai-posture .report-card");
  await page.locator("#openSearch").click();
  await page.locator("#commandSearch").fill("Pilot Launch Board Pack Packet");
  await page.getByText("Pilot Launch Board Pack Packet").first().waitFor({ state: "visible", timeout: 10_000 });
  await page.keyboard.press("Escape");
  return capture(page, "hosted-aispm-sentinel.png");
}

async function main() {
  const failures = [];
  let browser;
  try {
    await validateHttpAssets();
    browser = await chromium.launch();
    const page = await browser.newPage();
    await assertNoConsoleErrors(page, failures);
    const screenshots = [await validateDashboard(page), await validateAispm(page)];
    if (failures.length) {
      throw new Error(failures.join("\n"));
    }
    console.log("CAVRA hosted sandbox Pages validation passed.");
    console.log(`- ${baseUrl}`);
    for (const screenshot of screenshots) {
      console.log(`- ${path.relative(repoRoot, screenshot)}`);
    }
  } catch (error) {
    console.error("CAVRA hosted sandbox Pages validation failed.");
    console.error(error.message);
    process.exitCode = 1;
  } finally {
    if (browser) await browser.close();
  }
}

await main();
