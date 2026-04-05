#!/usr/bin/env node

import fs from "fs";
import path from "path";
import { fileURLToPath, pathToFileURL } from "url";

function printHelp() {
  console.log(`Usage:
  node fast_page_probe.mjs --state <storageState.json> --base-url <url> --url <path-or-url> [options]

Options:
  --state <file>         Playwright storageState.
  --base-url <url>       Base origin.
  --url <path-or-url>    Page path or absolute URL.
  --wait-selector <css>  Optional selector to wait for.
  --wait-text <text>     Optional page text to wait for.
  --timeout-ms <n>       Default: 20000
  --screenshot <file>    Optional screenshot output.
  --classify-js <expr>   JS expression returning pass|sample_mismatch|auth_expired|env_blocked|fail
  --help                 Show this help.
`);
}

function parseArgs(argv) {
  const args = {
    timeoutMs: 20000,
  };
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (token === "--help" || token === "-h") {
      args.help = true;
    } else if (token === "--state") {
      args.state = argv[++i];
    } else if (token === "--base-url") {
      args.baseUrl = argv[++i];
    } else if (token === "--url") {
      args.url = argv[++i];
    } else if (token === "--wait-selector") {
      args.waitSelector = argv[++i];
    } else if (token === "--wait-text") {
      args.waitText = argv[++i];
    } else if (token === "--timeout-ms") {
      args.timeoutMs = Number(argv[++i]);
    } else if (token === "--screenshot") {
      args.screenshot = argv[++i];
    } else if (token === "--classify-js") {
      args.classifyJs = argv[++i];
    } else {
      throw new Error(`Unknown argument: ${token}`);
    }
  }
  return args;
}

async function loadPlaywright() {
  const scriptDir = path.dirname(fileURLToPath(import.meta.url));
  const candidates = [
    process.env.PLAYWRIGHT_MODULE_PATH,
    path.resolve(scriptDir, "../../../../../../fssc-web/node_modules/playwright/index.js"),
    path.resolve(process.cwd(), "node_modules/playwright/index.js"),
    "playwright",
  ].filter(Boolean);

  for (const candidate of candidates) {
    try {
      if (candidate === "playwright") {
        return await import(candidate);
      }
      if (fs.existsSync(candidate)) {
        return await import(pathToFileURL(candidate).href);
      }
    } catch {
      // Try next.
    }
  }

  throw new Error("Playwright module not found. Set PLAYWRIGHT_MODULE_PATH if needed.");
}

function detectAuthExpired(text) {
  const body = String(text || "").toLowerCase();
  return body.includes("login") || body.includes("请登录") || body.includes("统一身份认证");
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    printHelp();
    return 0;
  }

  for (const key of ["state", "baseUrl", "url"]) {
    if (!args[key]) {
      throw new Error(`--${key.replace(/[A-Z]/g, (match) => `-${match.toLowerCase()}`)} is required.`);
    }
  }

  const { chromium } = await loadPlaywright();
  const browser = await chromium.launch({
    headless: true,
    args: ["--disable-gpu", "--blink-settings=imagesEnabled=false"],
  });

  try {
    const context = await browser.newContext({
      baseURL: args.baseUrl,
      storageState: args.state,
      ignoreHTTPSErrors: true,
    });

    await context.route("**/*", (route) => {
      const type = route.request().resourceType();
      if (type === "image" || type === "media" || type === "font") {
        return route.abort();
      }
      return route.continue();
    });

    const page = await context.newPage();
    await page.goto(args.url, {
      waitUntil: "domcontentloaded",
      timeout: args.timeoutMs,
    });

    if (args.waitSelector) {
      await page.waitForSelector(args.waitSelector, { timeout: args.timeoutMs });
    }
    if (args.waitText) {
      await page.getByText(args.waitText, { exact: false }).waitFor({ timeout: args.timeoutMs });
    }

    const lastText = await page.locator("body").innerText({ timeout: args.timeoutMs });
    let status = detectAuthExpired(lastText) ? "auth_expired" : "pass";
    if (args.classifyJs) {
      const classify = new Function("lastText", `return (${args.classifyJs});`);
      status = classify(lastText);
    }

    if (args.screenshot) {
      await page.screenshot({
        path: args.screenshot,
        fullPage: true,
      });
    }

    console.log(
      JSON.stringify({
        status,
        url: page.url(),
        snippet: String(lastText || "").slice(0, 1200),
      }),
    );
    return status === "pass" ? 0 : 1;
  } catch (error) {
    console.log(
      JSON.stringify({
        status: "env_blocked",
        message: error instanceof Error ? error.message : String(error),
      }),
    );
    return 1;
  } finally {
    await browser.close();
  }
}

main()
  .then((code) => {
    process.exit(code);
  })
  .catch((error) => {
    console.log(
      JSON.stringify({
        status: "fail",
        message: error instanceof Error ? error.message : String(error),
      }),
    );
    process.exit(1);
  });
