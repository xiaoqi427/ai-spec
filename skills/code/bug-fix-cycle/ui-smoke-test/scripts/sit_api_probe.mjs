#!/usr/bin/env node

import fs from "fs";
import path from "path";
import { fileURLToPath, pathToFileURL } from "url";

function printHelp() {
  console.log(`Usage:
  node sit_api_probe.mjs --state <storageState.json> --base-url <url> --flow <flow> [options]

Flows:
  resolve-load
  resolve-new-claim-line
  resolve-load-submit

Options:
  --state <file>             Playwright storageState.
  --base-url <url>           SIT base url, such as https://pri-fssc-web-sit.digitalyili.com
  --flow <name>              One of the flows above.
  --claim-no <value>         Claim number used by the resolve step.
  --resolve-endpoint <path>  Default: /api/claim/rmbs-claim/getClaimIdByClaimNo
  --target-endpoint <path>   Used by resolve-load or resolve-new-claim-line.
  --load-endpoint <path>     Used by resolve-load-submit.
  --submit-endpoint <path>   Used by resolve-load-submit.
  --classify-js <expr>       JS expression returning pass|sample_mismatch|auth_expired|env_blocked|fail
  --timeout-ms <n>           Default: 20000
  --help                     Show this help.
`);
}

function parseArgs(argv) {
  const args = {
    resolveEndpoint: "/api/claim/rmbs-claim/getClaimIdByClaimNo",
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
    } else if (token === "--flow") {
      args.flow = argv[++i];
    } else if (token === "--claim-no") {
      args.claimNo = argv[++i];
    } else if (token === "--resolve-endpoint") {
      args.resolveEndpoint = argv[++i];
    } else if (token === "--target-endpoint") {
      args.targetEndpoint = argv[++i];
    } else if (token === "--load-endpoint") {
      args.loadEndpoint = argv[++i];
    } else if (token === "--submit-endpoint") {
      args.submitEndpoint = argv[++i];
    } else if (token === "--classify-js") {
      args.classifyJs = argv[++i];
    } else if (token === "--timeout-ms") {
      args.timeoutMs = Number(argv[++i]);
    } else {
      throw new Error(`Unknown argument: ${token}`);
    }
  }
  return args;
}

async function loadPlaywrightRequest() {
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
        const mod = await import(candidate);
        return mod.default ?? mod;
      }
      if (fs.existsSync(candidate)) {
        const mod = await import(pathToFileURL(candidate).href);
        return mod.default ?? mod;
      }
    } catch {
      // Try the next candidate.
    }
  }

  throw new Error("Playwright module not found. Set PLAYWRIGHT_MODULE_PATH if needed.");
}

async function safeJson(response) {
  const text = await response.text();
  try {
    return { json: JSON.parse(text), text };
  } catch {
    return { json: null, text };
  }
}

function detectAuthExpired(statusCode, lastText) {
  if (statusCode === 401 || statusCode === 403) {
    return true;
  }
  const text = String(lastText || "").toLowerCase();
  return (
    text.includes("login") ||
    text.includes("请登录") ||
    text.includes("统一身份认证")
  );
}

function defaultStatus(statusCode, lastText) {
  if (detectAuthExpired(statusCode, lastText)) {
    return "auth_expired";
  }
  if (statusCode >= 500) {
    return "env_blocked";
  }
  return "fail";
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    printHelp();
    return 0;
  }

  for (const required of ["state", "baseUrl", "flow", "claimNo"]) {
    if (!args[required]) {
      throw new Error(`--${required.replace(/[A-Z]/g, (match) => `-${match.toLowerCase()}`)} is required.`);
    }
  }

  const playwright = await loadPlaywrightRequest();
  const { request } = playwright;
  const api = await request.newContext({
    baseURL: args.baseUrl,
    storageState: args.state,
    ignoreHTTPSErrors: true,
    extraHTTPHeaders: {
      Accept: "application/json, text/plain, */*",
      "Content-Type": "application/json;charset=UTF-8",
    },
  });

  const responses = [];
  const vars = {
    claim_no: args.claimNo,
  };

  try {
    const resolveResponse = await api.post(args.resolveEndpoint, {
      data: {
        claimNo: args.claimNo,
      },
      timeout: args.timeoutMs,
    });
    const resolveBody = await safeJson(resolveResponse);
    responses.push({
      step: "resolve",
      status: resolveResponse.status(),
      body: resolveBody.json,
      text: resolveBody.text,
    });

    const claimInfo = resolveBody.json?.data || resolveBody.json || {};
    vars.claim_id = claimInfo.claimId ?? claimInfo.id ?? null;
    vars.item_id = claimInfo.itemId ?? null;

    if (!vars.claim_id) {
      const payload = {
        status: defaultStatus(resolveResponse.status(), resolveBody.text),
        response_status: resolveResponse.status(),
        claim_no: args.claimNo,
        snippet: resolveBody.text.slice(0, 1200),
      };
      console.log(JSON.stringify(payload));
      return payload.status === "pass" ? 0 : 1;
    }

    let lastResponse = resolveResponse;
    let lastJson = resolveBody.json;
    let lastText = resolveBody.text;

    if (args.flow === "resolve-load") {
      if (!args.targetEndpoint) {
        throw new Error("--target-endpoint is required for resolve-load.");
      }
      lastResponse = await api.post(args.targetEndpoint, {
        data: { claimId: vars.claim_id },
        timeout: args.timeoutMs,
      });
      ({ json: lastJson, text: lastText } = await safeJson(lastResponse));
      responses.push({
        step: "target",
        status: lastResponse.status(),
        body: lastJson,
        text: lastText,
      });
    } else if (args.flow === "resolve-new-claim-line") {
      if (!args.targetEndpoint) {
        throw new Error("--target-endpoint is required for resolve-new-claim-line.");
      }
      lastResponse = await api.post(
        `${args.targetEndpoint}?claimId=${encodeURIComponent(String(vars.claim_id))}`,
        {
          timeout: args.timeoutMs,
        },
      );
      ({ json: lastJson, text: lastText } = await safeJson(lastResponse));
      responses.push({
        step: "target",
        status: lastResponse.status(),
        body: lastJson,
        text: lastText,
      });
    } else if (args.flow === "resolve-load-submit") {
      if (!args.loadEndpoint || !args.submitEndpoint) {
        throw new Error("--load-endpoint and --submit-endpoint are required for resolve-load-submit.");
      }
      const loadResponse = await api.post(args.loadEndpoint, {
        data: { claimId: vars.claim_id },
        timeout: args.timeoutMs,
      });
      const loadBody = await safeJson(loadResponse);
      responses.push({
        step: "load",
        status: loadResponse.status(),
        body: loadBody.json,
        text: loadBody.text,
      });
      const claimPayload = loadBody.json?.data?.claim ?? loadBody.json?.data ?? loadBody.json;
      lastResponse = await api.post(args.submitEndpoint, {
        data: claimPayload,
        timeout: args.timeoutMs,
      });
      ({ json: lastJson, text: lastText } = await safeJson(lastResponse));
      responses.push({
        step: "submit",
        status: lastResponse.status(),
        body: lastJson,
        text: lastText,
      });
    } else {
      throw new Error(`Unsupported flow: ${args.flow}`);
    }

    let status = defaultStatus(lastResponse.status(), lastText);
    if (args.classifyJs) {
      const classify = new Function(
        "vars",
        "responses",
        "lastJson",
        "lastText",
        "statusCode",
        `return (${args.classifyJs});`,
      );
      status = classify(vars, responses, lastJson, lastText, lastResponse.status());
    }

    const payload = {
      status,
      claim_no: args.claimNo,
      claim_id: vars.claim_id,
      item_id: vars.item_id,
      response_status: lastResponse.status(),
      snippet: String(lastText || "").slice(0, 1200),
    };
    console.log(JSON.stringify(payload));
    return status === "pass" ? 0 : 1;
  } catch (error) {
    const payload = {
      status: "env_blocked",
      claim_no: args.claimNo,
      message: error instanceof Error ? error.message : String(error),
    };
    console.log(JSON.stringify(payload));
    return 1;
  } finally {
    await api.dispose();
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
