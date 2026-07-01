#!/usr/bin/env node
import { mkdirSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(__dirname, "..");
const screenshotDir = path.join(repoRoot, ".cavra", "product-site-smoke");

function normalizeBaseUrl(value) {
  const base = value || "https://cavra.mind-ops.cloud/";
  return base.endsWith("/") ? base : `${base}/`;
}

const baseUrl = normalizeBaseUrl(process.env.CAVRA_PRODUCT_SITE_URL);

async function assertFetchOk(url, label) {
  const response = await fetch(url, { redirect: "follow" });
  if (!response.ok) throw new Error(`${label} returned HTTP ${response.status}: ${url}`);
  return response.text();
}

async function assertIndexMarkers() {
  const index = await assertFetchOk(baseUrl, "product site index");
  for (const marker of [
    "Before the agent acts, CAVRA decides.",
    "The runtime authority layer for AI agents.",
    "Run Interactive Demo",
    "CAVRA Managed",
    "Enterprise Subscription",
    "Trial Access",
    "Open CAVRA Textbook",
    "Product Video Script",
    "https://cavra-trial.mind-ops.cloud/",
    "https://github.com/Huzefaaa2/cavra/wiki",
  ]) {
    if (!index.includes(marker)) throw new Error(`product site index missing ${marker}`);
  }
  await assertFetchOk(new URL("styles.css", baseUrl).toString(), "product site styles");
  await assertFetchOk(new URL("site.js", baseUrl).toString(), "product site JavaScript");
  await assertFetchOk(new URL("video-script.html", baseUrl).toString(), "product video script page");
  await assertFetchOk(new URL("assets/brand/cavra-mark.svg", baseUrl).toString(), "CAVRA mark");
  await assertFetchOk(new URL("assets/brand/product/cavra-command-center-preview.svg", baseUrl).toString(), "product preview asset");
}

async function assertReadable(page, selector) {
  const failures = await page.locator(selector).evaluateAll((nodes) => {
    const results = [];
    for (const node of nodes) {
      const rect = node.getBoundingClientRect();
      const style = window.getComputedStyle(node);
      if (rect.width === 0 || rect.height === 0) continue;
      if (style.visibility === "hidden" || style.display === "none") continue;
      if (node.scrollWidth > node.clientWidth + 4) {
        results.push(`${node.textContent.trim().replace(/\s+/g, " ").slice(0, 80)} overflows horizontally`);
      }
      if (rect.left < -4 || rect.right > window.innerWidth + 4) {
        results.push(`${node.tagName.toLowerCase()} escapes viewport`);
      }
    }
    return results;
  });
  if (failures.length) throw new Error(`${selector} layout failures:\n- ${failures.join("\n- ")}`);
}

async function capture(page, name) {
  mkdirSync(screenshotDir, { recursive: true });
  const filePath = path.join(screenshotDir, name);
  await page.screenshot({ path: filePath, fullPage: true });
  return filePath;
}

async function validatePage() {
  const failures = [];
  const browser = await chromium.launch();
  try {
    const page = await browser.newPage();
    page.on("pageerror", (error) => failures.push(`page error: ${error.message}`));
    page.on("console", (message) => {
      if (message.type() === "error") failures.push(`console error: ${message.text()}`);
    });

    await page.setViewportSize({ width: 1440, height: 1100 });
    await page.goto(baseUrl, { waitUntil: "networkidle" });
    await page.getByText("The runtime authority layer for AI agents.").waitFor({ state: "visible" });
    await page.getByText("CAVRA Managed").first().waitFor({ state: "visible" });
    await page.getByText("Enterprise Subscription").first().waitFor({ state: "visible" });
    await page.getByText("Open CAVRA Textbook").first().waitFor({ state: "visible" });
    await page.selectOption("#actionSelect", "deploy_prod");
    await page.selectOption("#trustSelect", "unknown");
    await page.getByText('"decision": "block"').waitFor({ state: "visible" });
    await page.getByLabel("Role-specific buyer paths").getByRole("button", { name: "Executive" }).click();
    await page.getByText("Executive path").waitFor({ state: "visible" });
    await page.getByRole("button", { name: "Raw JSON" }).click();
    await page.getByText("cavra.evidence.public.demo.v1").waitFor({ state: "visible" });
    await assertReadable(page, "h1, h2, h3, p, a, button, article, pre");
    const desktop = await capture(page, "product-site-desktop.png");

    await page.setViewportSize({ width: 390, height: 920 });
    await page.goto(baseUrl, { waitUntil: "networkidle" });
    await page.getByRole("button", { name: "Menu" }).click();
    await page.locator("#mobileNav.is-open").waitFor({ state: "visible" });
    await assertReadable(page, "h1, h2, h3, p, a, button, article, pre");
    const mobile = await capture(page, "product-site-mobile.png");

    if (failures.length) throw new Error(failures.join("\n"));
    console.log("CAVRA product site validation passed.");
    console.log(`- ${baseUrl}`);
    console.log(`- ${path.relative(repoRoot, desktop)}`);
    console.log(`- ${path.relative(repoRoot, mobile)}`);
  } finally {
    await browser.close();
  }
}

try {
  await assertIndexMarkers();
  await validatePage();
} catch (error) {
  console.error("CAVRA product site validation failed.");
  console.error(error.message);
  process.exitCode = 1;
}
