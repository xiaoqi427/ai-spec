#!/usr/bin/env node

import fs from "fs";
import os from "os";
import path from "path";
import { spawnSync } from "child_process";

function printHelp() {
  console.log(`Usage:
  node build_playwright_state.mjs --source-json <cookies.json> --output <state.json>
  node build_playwright_state.mjs --from-live-chrome --output <state.json>

Options:
  --source-json <file>     Chrome-exported cookies JSON array.
  --output <file>          Playwright storageState output file.
  --from-live-chrome       Save state from an already logged-in Chrome session.
  --agent-browser-helper   Optional helper script for agent-browser.
  --merge                  Merge with an existing storageState file.
  --help                   Show this help.
`);
}

function parseArgs(argv) {
  const args = {
    merge: false,
  };
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (token === "--help" || token === "-h") {
      args.help = true;
    } else if (token === "--source-json") {
      args.sourceJson = argv[++i];
    } else if (token === "--output") {
      args.output = argv[++i];
    } else if (token === "--from-live-chrome") {
      args.fromLiveChrome = true;
    } else if (token === "--agent-browser-helper") {
      args.agentBrowserHelper = argv[++i];
    } else if (token === "--merge") {
      args.merge = true;
    } else {
      throw new Error(`Unknown argument: ${token}`);
    }
  }
  return args;
}

function ensureParentDir(filePath) {
  fs.mkdirSync(path.dirname(path.resolve(filePath)), { recursive: true });
}

function normalizeSameSite(value) {
  if (!value) {
    return "Lax";
  }
  const text = String(value).toLowerCase();
  if (text === "strict") {
    return "Strict";
  }
  if (text === "none") {
    return "None";
  }
  return "Lax";
}

function normalizeCookie(cookie) {
  const normalized = {
    name: String(cookie.name ?? ""),
    value: String(cookie.value ?? ""),
    domain: String(cookie.domain ?? ""),
    path: String(cookie.path ?? "/"),
    secure: Boolean(cookie.secure),
    httpOnly: Boolean(cookie.httpOnly),
    sameSite: normalizeSameSite(cookie.sameSite),
  };

  if (Number.isFinite(cookie.expires) && Number(cookie.expires) > 0) {
    normalized.expires = Number(cookie.expires);
  }

  return normalized;
}

function mergeCookies(existing, incoming) {
  const map = new Map();
  for (const cookie of [...existing, ...incoming]) {
    const key = [
      cookie.name,
      cookie.domain,
      cookie.path,
      cookie.secure ? "1" : "0",
    ].join("|");
    map.set(key, cookie);
  }
  return Array.from(map.values()).sort((a, b) => {
    return `${a.domain}${a.path}${a.name}`.localeCompare(
      `${b.domain}${b.path}${b.name}`,
    );
  });
}

function buildStateFromCookieJson(cookieJsonPath, outputPath, merge) {
  const raw = JSON.parse(fs.readFileSync(cookieJsonPath, "utf8"));
  if (!Array.isArray(raw)) {
    throw new Error("Cookie JSON must be an array.");
  }

  let existing = { cookies: [], origins: [] };
  if (merge && fs.existsSync(outputPath)) {
    existing = JSON.parse(fs.readFileSync(outputPath, "utf8"));
  }

  const cookies = mergeCookies(
    Array.isArray(existing.cookies) ? existing.cookies : [],
    raw.map(normalizeCookie),
  );

  const state = {
    cookies,
    origins: Array.isArray(existing.origins) ? existing.origins : [],
  };

  ensureParentDir(outputPath);
  fs.writeFileSync(outputPath, `${JSON.stringify(state, null, 2)}\n`, "utf8");
  console.log(
    JSON.stringify(
      {
        mode: "cookie-json",
        output: path.resolve(outputPath),
        cookieCount: cookies.length,
      },
      null,
      2,
    ),
  );
}

function saveStateFromLiveChrome(outputPath, helperPath) {
  ensureParentDir(outputPath);
  const defaultHelper = path.join(
    os.homedir(),
    ".agents/skills/agent-browser/scripts/agent-browser-codex.sh",
  );
  const helper = helperPath || process.env.AGENT_BROWSER_CODEX_HELPER || defaultHelper;

  let result;
  if (fs.existsSync(helper)) {
    result = spawnSync(
      "bash",
      [helper, "--auto-connect", "state", "save", outputPath],
      { stdio: "inherit" },
    );
  } else {
    result = spawnSync(
      "npx",
      ["-y", "agent-browser", "--auto-connect", "state", "save", outputPath],
      { stdio: "inherit" },
    );
  }

  if ((result.status ?? 1) !== 0) {
    process.exit(result.status ?? 1);
  }

  console.log(
    JSON.stringify(
      {
        mode: "live-chrome",
        output: path.resolve(outputPath),
      },
      null,
      2,
    ),
  );
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    printHelp();
    return;
  }

  if (!args.output) {
    throw new Error("--output is required.");
  }

  if (args.fromLiveChrome) {
    saveStateFromLiveChrome(args.output, args.agentBrowserHelper);
    return;
  }

  if (!args.sourceJson) {
    throw new Error("Either --source-json or --from-live-chrome is required.");
  }

  buildStateFromCookieJson(args.sourceJson, args.output, args.merge);
}

try {
  main();
} catch (error) {
  console.error(
    JSON.stringify(
      {
        status: "error",
        message: error instanceof Error ? error.message : String(error),
      },
      null,
      2,
    ),
  );
  process.exit(1);
}
