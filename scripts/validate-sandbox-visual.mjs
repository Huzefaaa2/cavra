#!/usr/bin/env node
import { createServer } from "node:http";
import { readFile } from "node:fs/promises";
import { existsSync, mkdirSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(__dirname, "..");
const portalRoot = path.join(repoRoot, "apps", "sandbox-ui");
const screenshotDir = path.join(repoRoot, ".cavra", "visual-smoke");

const mimeTypes = new Map([
  [".html", "text/html; charset=utf-8"],
  [".js", "text/javascript; charset=utf-8"],
  [".css", "text/css; charset=utf-8"],
  [".svg", "image/svg+xml"],
  [".json", "application/json; charset=utf-8"],
  [".png", "image/png"],
]);

function send(response, status, body, type = "text/plain; charset=utf-8") {
  response.writeHead(status, { "content-type": type });
  response.end(body);
}

function resolveStaticPath(requestUrl) {
  const url = new URL(requestUrl, "http://127.0.0.1");
  const decodedPath = decodeURIComponent(url.pathname);
  const safePath = decodedPath === "/" ? "/index.html" : decodedPath;
  const resolved = path.resolve(portalRoot, `.${safePath}`);
  if (!resolved.startsWith(portalRoot)) {
    return null;
  }
  return resolved;
}

async function startServer() {
  const server = createServer(async (request, response) => {
    const resolved = resolveStaticPath(request.url || "/");
    if (!resolved) {
      send(response, 403, "Forbidden");
      return;
    }
    try {
      const body = await readFile(resolved);
      send(response, 200, body, mimeTypes.get(path.extname(resolved)) || "application/octet-stream");
    } catch (error) {
      send(response, 404, "Not found");
    }
  });
  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  const address = server.address();
  return { server, baseUrl: `http://127.0.0.1:${address.port}` };
}

async function assertNoConsoleErrors(page, failures) {
  page.on("pageerror", (error) => failures.push(`page error: ${error.message}`));
  page.on("console", (message) => {
    if (message.type() === "error") {
      failures.push(`console error: ${message.text()}`);
    }
  });
}

async function assertVisible(page, selectors) {
  for (const selector of selectors) {
    await page.locator(selector).first().waitFor({ state: "visible", timeout: 10_000 });
  }
}

async function assertReadableAndContained(page, selector) {
  const failures = await page.locator(selector).evaluateAll((nodes) => {
    const nodeFailures = [];
    for (const node of nodes) {
      const rect = node.getBoundingClientRect();
      const style = window.getComputedStyle(node);
      if (rect.width === 0 || rect.height === 0) continue;
      if (style.visibility === "hidden" || style.display === "none") continue;
      if (Number(style.opacity) < 0.75) {
        nodeFailures.push(`${node.tagName.toLowerCase()} is too transparent`);
      }
      if (style.color === "rgba(0, 0, 0, 0)" || style.color === "transparent") {
        nodeFailures.push(`${node.tagName.toLowerCase()} has transparent text`);
      }
      if (node.scrollWidth > node.clientWidth + 3) {
        nodeFailures.push(`${node.textContent.trim().slice(0, 60)} overflows horizontally`);
      }
      if (rect.left < -2 || rect.right > window.innerWidth + 2) {
        nodeFailures.push(`${node.textContent.trim().slice(0, 60)} escapes viewport`);
      }
    }
    return nodeFailures;
  });
  if (failures.length) {
    throw new Error(`${selector} readability/containment failures:\n- ${failures.join("\n- ")}`);
  }
}

async function assertNoCardOverlap(page, containerSelector, cardSelector) {
  const failures = await page.locator(containerSelector).evaluate((container, selector) => {
    const cards = [...container.querySelectorAll(selector)]
      .map((card) => {
        const rect = card.getBoundingClientRect();
        return {
          text: card.textContent.trim().replace(/\s+/g, " ").slice(0, 80),
          left: rect.left,
          right: rect.right,
          top: rect.top,
          bottom: rect.bottom,
          width: rect.width,
          height: rect.height,
        };
      })
      .filter((rect) => rect.width > 0 && rect.height > 0);
    const overlaps = [];
    for (let index = 0; index < cards.length; index += 1) {
      for (let otherIndex = index + 1; otherIndex < cards.length; otherIndex += 1) {
        const a = cards[index];
        const b = cards[otherIndex];
        const overlapX = Math.max(0, Math.min(a.right, b.right) - Math.max(a.left, b.left));
        const overlapY = Math.max(0, Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top));
        if (overlapX > 2 && overlapY > 2) {
          overlaps.push(`${a.text} overlaps ${b.text}`);
        }
      }
    }
    return overlaps;
  }, cardSelector);
  if (failures.length) {
    throw new Error(`${containerSelector} card overlap failures:\n- ${failures.join("\n- ")}`);
  }
}

async function capture(page, name, target = null) {
  mkdirSync(screenshotDir, { recursive: true });
  const filePath = path.join(screenshotDir, name);
  if (target) {
    await page.locator(target).first().screenshot({ path: filePath });
  } else {
    await page.screenshot({ path: filePath, fullPage: true });
  }
  return filePath;
}

async function validateThemes(page, baseUrl) {
  await page.setViewportSize({ width: 1440, height: 1100 });
  await page.goto("about:blank");
  await page.goto(`${baseUrl}/index.html#dashboard`, { waitUntil: "networkidle" });
  await page.locator("#dashboard.is-active").waitFor({ state: "visible" });
  for (const theme of ["sentinel", "classic", "retro", "executive"]) {
    await page.selectOption("#themeSelect", theme);
    await page.locator(`body[data-theme="${theme}"]`).waitFor({ state: "attached" });
    await assertReadableAndContained(page, ".top-shell, #operatorStatusStrip, .operator-dashboard");
  }
}

async function validateDashboard(page, baseUrl) {
  await page.setViewportSize({ width: 1440, height: 1100 });
  await page.goto("about:blank");
  await page.goto(`${baseUrl}/index.html#dashboard`, { waitUntil: "networkidle" });
  await page.locator("#dashboard.is-active").waitFor({ state: "visible" });
  await page.selectOption("#themeSelect", "classic");
  await assertVisible(page, [
    ".operator-dashboard",
    "#operatorStatusStrip",
    ".operator-empty-state:not([hidden]), .operator-configured-state:not([hidden])",
  ]);
  await assertReadableAndContained(page, "#operatorStatusStrip, .operator-dashboard");
  return capture(page, "dashboard-desktop-classic.png");
}

async function validateAispmDesktop(page, baseUrl) {
  await page.setViewportSize({ width: 1440, height: 1200 });
  await page.goto("about:blank");
  await page.goto(`${baseUrl}/index.html#ai-posture`, { waitUntil: "networkidle" });
  await page.locator("#ai-posture.is-active").waitFor({ state: "visible" });
  await page.selectOption("#themeSelect", "sentinel");
  await assertVisible(page, [
    ".aispm-live-workstation",
    "#aispmLiveStatusStrip",
    "#aispmLiveMetricCards .operator-metric-card",
    "#aispmOverviewCards .posture-card",
    "#aispmPilotLaunchBoardPack .board-pack-card",
    "#aispmPilotLaunchBoardPackManifest .board-pack-manifest-card",
    "#copyAispmPilotLaunchBoardPackPacket",
    "#downloadAispmPilotLaunchBoardPackPacket",
    "#aispmReportCenter .report-card",
    "#sendAispmReportEmail:disabled",
  ]);
  await assertReadableAndContained(page, ".aispm-live-workstation, #aispmLiveMetricCards .operator-metric-card");
  await assertReadableAndContained(page, "#ai-posture .board-pack-card, #ai-posture .board-pack-manifest-card, #ai-posture .report-card");
  await assertNoCardOverlap(page, "#aispmPilotLaunchBoardPack", ".board-pack-card");
  await assertNoCardOverlap(page, "#aispmPilotLaunchBoardPackManifest", ".board-pack-manifest-card");
  await assertNoCardOverlap(page, "#aispmReportCenter", ".report-card");
  await page.locator("#openSearch").click();
  await page.locator("#commandSearch").fill("Board Pack Packet");
  await page.getByText("Pilot Launch Board Pack Packet").first().waitFor({ state: "visible" });
  await page.keyboard.press("Escape");
  const full = await capture(page, "aispm-desktop-sentinel.png");
  await page.locator(".aispm-board-pack-panel").scrollIntoViewIfNeeded();
  const board = await capture(page, "aispm-board-pack-panel.png", ".aispm-board-pack-panel");
  await page.locator(".aispm-report-center-panel").scrollIntoViewIfNeeded();
  const reports = await capture(page, "aispm-report-center-panel.png", ".aispm-report-center-panel");
  return [full, board, reports];
}

async function validateAispmMobile(page, baseUrl) {
  await page.setViewportSize({ width: 390, height: 1100 });
  await page.goto("about:blank");
  await page.goto(`${baseUrl}/index.html#ai-posture`, { waitUntil: "networkidle" });
  await page.locator("#ai-posture.is-active").waitFor({ state: "visible" });
  await assertVisible(page, [
    ".mobile-bottom",
    ".aispm-live-workstation",
    "#aispmLiveMetricCards .operator-metric-card",
    "#aispmPilotLaunchBoardPack .board-pack-card",
    "#aispmPilotLaunchBoardPackManifest .board-pack-manifest-card",
    "#aispmReportCenter .report-card",
  ]);
  await assertReadableAndContained(page, "#ai-posture .board-pack-card, #ai-posture .board-pack-manifest-card, #ai-posture .report-card, .mobile-bottom");
  return capture(page, "aispm-mobile-sentinel.png");
}

async function main() {
  const failures = [];
  const { server, baseUrl } = await startServer();
  let browser;
  try {
    browser = await chromium.launch();
    const page = await browser.newPage();
    await assertNoConsoleErrors(page, failures);
    await validateThemes(page, baseUrl);
    const screenshots = [
      await validateDashboard(page, baseUrl),
      ...(await validateAispmDesktop(page, baseUrl)),
      await validateAispmMobile(page, baseUrl),
    ];
    if (failures.length) {
      throw new Error(failures.join("\n"));
    }
    console.log("CAVRA sandbox visual validation passed.");
    for (const screenshot of screenshots) {
      console.log(`- ${path.relative(repoRoot, screenshot)}`);
    }
  } catch (error) {
    console.error("CAVRA sandbox visual validation failed.");
    console.error(error.message);
    process.exitCode = 1;
  } finally {
    if (browser) await browser.close();
    await new Promise((resolve) => server.close(resolve));
  }
}

if (!existsSync(portalRoot)) {
  console.error(`Missing sandbox portal root: ${portalRoot}`);
  process.exit(1);
}

await main();
