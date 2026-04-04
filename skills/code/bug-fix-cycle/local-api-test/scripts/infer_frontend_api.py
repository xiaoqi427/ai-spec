#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


HTTP_METHODS = ("get", "post", "put", "delete", "patch")
STRING_LITERAL_RE = re.compile(r"""^\s*(['"`])(?P<value>[\s\S]*)\1\s*$""")
HTTP_ALIAS_RE = re.compile(r"""const\s+(?P<alias>\w+)\s*=\s*Setaria\.getHttp\(\)\.(?P<domain>\w+)\s*;""")
EXPORT_ARROW_RE = re.compile(
    r"""export\s+const\s+(?P<name>\w+)\s*=\s*\((?P<params>[\s\S]*?)\)\s*=>\s*(?P<body>[\s\S]*?);""",
    re.MULTILINE,
)
EXPORT_FUNCTION_RE = re.compile(
    r"""export\s+function\s+(?P<name>\w+)\s*\((?P<params>[\s\S]*?)\)\s*\{(?P<body>[\s\S]*?)^\}""",
    re.MULTILINE,
)
SERVICE_IMPORT_RE = re.compile(
    r"""import\s*\{(?P<names>[\s\S]*?)\}\s*from\s*['"](?P<module>[^'"]*service[^'"]*)['"]""",
    re.MULTILINE,
)
CLASS_REQUEST_MAPPING_RE = re.compile(r"""@RequestMapping\(\s*"(?P<path>[^"]*)"\s*\)""")
METHOD_MAPPING_RE = re.compile(
    r"""@(?P<annotation>GetMapping|PostMapping|PutMapping|DeleteMapping|PatchMapping|RequestMapping)\(\s*"(?P<path>[^"]*)"\s*\)""",
    re.MULTILINE,
)
METHOD_SIGNATURE_RE = re.compile(
    r"""public\s+(?P<return_type>[^\(\n]+?)\s+(?P<name>\w+)\s*\((?P<params>[\s\S]*?)\)\s*\{""",
    re.MULTILINE,
)
REQUEST_BODY_TYPE_RE = re.compile(
    r"""@RequestBody\s+(?:@\w+(?:\([^)]*\))?\s+)*(?P<type>[A-Za-z0-9_$.]+(?:<[^>]+>)?)\s+\w+"""
)

LOCAL_SERVICE_PORTS = {
    "config": {"port": 8080, "context_path": "/"},
    "claim-base": {"port": 8081, "context_path": "/"},
    "claim-eer": {"port": 7001, "context_path": "/eer"},
    "claim-ptp": {"port": 7002, "context_path": "/ptp"},
    "claim-rtr": {"port": 7003, "context_path": "/rtr"},
    "claim-tr": {"port": 7006, "context_path": "/tr"},
    "claim-otc": {"port": 7003, "context_path": "/otc"},
    "claim-fa": {"port": 7002, "context_path": "/fa"},
    "integration": {"port": 8083, "context_path": "/"},
    "fund": {"port": 8082, "context_path": "/"},
    "invoice": {"port": 8082, "context_path": "/"},
    "bpm": {"port": 8085, "context_path": "/"},
    "image": {"port": None, "context_path": "/"},
    "aam": {"port": 7788, "context_path": "/"},
    "rule": {"port": 9013, "context_path": "/"},
}

DOMAIN_TO_MODULE = {
    "base": None,
    "claimBase": "claim-base",
    "claim": "claim-base",
    "config": "config",
    "cac": None,
    "fund": "fund",
    "pi": None,
    "re": "rule",
    "bpm": "bpm",
    "otc": "claim-otc",
    "eer": "claim-eer",
    "rtr": "claim-rtr",
    "ptp": "claim-ptp",
    "fa": "claim-fa",
    "aam": "aam",
    "voucher": None,
    "tr": "claim-tr",
    "bi": None,
    "invoice": "invoice",
    "image": "image",
}


def detect_workspace_root() -> Path:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "fssc-web").exists() and (parent / "ai-spec").exists():
            return parent
    return Path.cwd()


def normalize_rel(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path.resolve())


def normalize_target(target: str) -> str:
    text = target.strip().replace("\\", "/")
    text = re.sub(r"^@/", "src/", text)
    return text


def normalize_endpoint(path: str) -> str:
    if not path:
        return "/"
    path = path.strip()
    path = path.split("?", 1)[0]
    path = re.sub(r"\$\{[^}]+\}", "<param>", path)
    if not path.startswith("/"):
        path = "/" + path
    path = re.sub(r"/{2,}", "/", path)
    return path


def join_paths(prefix: str, path: str) -> str:
    parts = [prefix.strip("/"), path.strip("/")]
    joined = "/".join(part for part in parts if part)
    return "/" + joined if joined else "/"


def decode_string_literal(expr: str) -> str:
    match = STRING_LITERAL_RE.match(expr.strip())
    if not match:
        return expr.strip()
    return match.group("value")


def split_top_level(text: str) -> list[str]:
    items = []
    buf = []
    depth_paren = 0
    depth_brace = 0
    depth_bracket = 0
    quote = None
    escape = False

    for char in text:
        if quote:
            buf.append(char)
            if escape:
                escape = False
                continue
            if char == "\\" and quote != "`":
                escape = True
                continue
            if char == quote:
                quote = None
            continue

        if char in ("'", '"', "`"):
            quote = char
            buf.append(char)
            continue

        if char == "(":
            depth_paren += 1
        elif char == ")":
            depth_paren -= 1
        elif char == "{":
            depth_brace += 1
        elif char == "}":
            depth_brace -= 1
        elif char == "[":
            depth_bracket += 1
        elif char == "]":
            depth_bracket -= 1

        if char == "," and depth_paren == 0 and depth_brace == 0 and depth_bracket == 0:
            items.append("".join(buf).strip())
            buf = []
            continue

        buf.append(char)

    tail = "".join(buf).strip()
    if tail:
        items.append(tail)
    return items


def find_balanced_call(text: str, start_index: int) -> tuple[str, int]:
    depth = 0
    quote = None
    escape = False
    buf = []

    for index in range(start_index, len(text)):
        char = text[index]
        buf.append(char)

        if quote:
            if escape:
                escape = False
                continue
            if char == "\\" and quote != "`":
                escape = True
                continue
            if char == quote:
                quote = None
            continue

        if char in ("'", '"', "`"):
            quote = char
            continue

        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return "".join(buf), index

    return "", -1


def score_path(path: Path, target: str, root: Path) -> int:
    rel = normalize_rel(path, root)
    score = 0
    if rel == target:
        score += 100
    if rel.endswith(target):
        score += 80
    if target in rel:
        score += 40
    if path.stem == target:
        score += 30
    if path.parent.name == target:
        score += 25
    return score


def find_best_path(root: Path, target: str) -> Path | None:
    candidates = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix not in (".vue", ".js"):
            continue
        score = score_path(path, target, root)
        if score > 0:
            candidates.append((score, path))
    if not candidates:
        return None
    candidates.sort(key=lambda item: (-item[0], str(item[1])))
    return candidates[0][1]


def resolve_path(target: str, root: Path) -> Path | None:
    normalized = normalize_target(target)
    direct = Path(normalized)
    if direct.exists():
        return direct.resolve()

    prefixed = root / normalized
    if prefixed.exists():
        return prefixed.resolve()

    if not normalized.startswith("src/"):
        src_prefixed = root / "src" / normalized
        if src_prefixed.exists():
            return src_prefixed.resolve()

    if "." not in normalized:
        best = find_best_path(root, normalized)
        if best:
            return best.resolve()

    return None


def resolve_service_from_page(page_file: Path) -> Path | None:
    text = page_file.read_text(encoding="utf-8", errors="ignore")
    for match in SERVICE_IMPORT_RE.finditer(text):
        module = match.group("module").strip()
        candidate = (page_file.parent / module).resolve()
        if candidate.suffix:
            if candidate.exists():
                return candidate
        else:
            js_candidate = candidate.with_suffix(".js")
            if js_candidate.exists():
                return js_candidate
            index_candidate = candidate / "index.js"
            if index_candidate.exists():
                return index_candidate

    sibling = page_file.parent / "service.js"
    if sibling.exists():
        return sibling.resolve()
    return None


def parse_http_domain_map(http_config_file: Path) -> dict[str, str]:
    text = http_config_file.read_text(encoding="utf-8", errors="ignore")
    mapping = {}
    pattern = re.compile(
        r"""(?P<name>\w+):\s*\{[\s\S]{0,120}?baseURL:\s*['"](?P<base>[^'"]+)['"]""",
        re.MULTILINE,
    )
    for match in pattern.finditer(text):
        mapping[match.group("name")] = match.group("base")
    return mapping


def parse_service_exports(service_file: Path) -> dict[str, dict]:
    text = service_file.read_text(encoding="utf-8", errors="ignore")
    alias_map = {match.group("alias"): match.group("domain") for match in HTTP_ALIAS_RE.finditer(text)}
    exports = {}

    for match in EXPORT_ARROW_RE.finditer(text):
        name = match.group("name")
        exports[name] = {
            "name": name,
            "params": match.group("params").strip(),
            "body": match.group("body").strip(),
        }

    for match in EXPORT_FUNCTION_RE.finditer(text):
        name = match.group("name")
        exports[name] = {
            "name": name,
            "params": match.group("params").strip(),
            "body": match.group("body").strip(),
        }

    parsed = {}
    for name, info in exports.items():
        api_call = extract_request_call(info["body"], alias_map)
        if not api_call:
            continue
        parsed[name] = {
            "name": name,
            "params": [item.strip() for item in split_top_level(info["params"]) if item.strip()],
            "body": info["body"],
            **api_call,
        }
    return parsed


def extract_request_call(body: str, alias_map: dict[str, str]) -> dict | None:
    for method in HTTP_METHODS:
        direct_pattern = re.compile(rf"""Setaria\.getHttp\(\)\.(?P<domain>\w+)\.{method}\(""")
        alias_pattern = re.compile(rf"""(?P<alias>\w+)\.{method}\(""")

        for pattern, is_direct in ((direct_pattern, True), (alias_pattern, False)):
            match = pattern.search(body)
            if not match:
                continue
            call_text, end_index = find_balanced_call(body, match.end() - 1)
            if end_index == -1:
                continue
            args_text = call_text[1:-1]
            args = split_top_level(args_text)
            if not args:
                continue
            domain = match.group("domain") if is_direct else alias_map.get(match.group("alias"))
            if not domain:
                continue
            path_expr = args[0]
            payload_expr = args[1] if len(args) > 1 else None
            options_expr = args[2] if len(args) > 2 else None
            path_template = decode_string_literal(path_expr)
            return {
                "domain": domain,
                "method": method.upper(),
                "path_expr": path_expr.strip(),
                "path_template": path_template,
                "payload_expr": payload_expr.strip() if payload_expr else None,
                "options_expr": options_expr.strip() if options_expr else None,
                "endpoint_path": normalize_endpoint(path_template),
            }
    return None


def parse_page_usage(page_file: Path) -> dict:
    text = page_file.read_text(encoding="utf-8", errors="ignore")
    imports = {}
    for match in SERVICE_IMPORT_RE.finditer(text):
        names = [item.strip() for item in match.group("names").split(",") if item.strip()]
        for name in names:
            local_name = name.split(" as ")[-1].strip()
            imports[local_name] = name.strip()

    roles = {}
    for role in ("request", "load", "save", "submit", "export", "delete"):
        pattern = re.compile(
            rf"""\b{role}\s*\([^)]*\)\s*\{{(?P<body>[\s\S]{{0,600}}?)\n\s*\}}""",
            re.MULTILINE,
        )
        for match in pattern.finditer(text):
            body = match.group("body")
            for name in imports:
                if re.search(rf"""\b{name}\s*\(""", body):
                    roles.setdefault(role, [])
                    if name not in roles[role]:
                        roles[role].append(name)
    return {"imports": imports, "roles": roles}


def parse_controller_file(controller_file: Path) -> list[dict]:
    text = controller_file.read_text(encoding="utf-8", errors="ignore")
    class_pos = text.find("class ")
    prefix = ""
    if class_pos != -1:
        matches = list(CLASS_REQUEST_MAPPING_RE.finditer(text[:class_pos]))
        if matches:
            prefix = matches[-1].group("path")

    endpoints = []
    search_index = 0
    while True:
        mapping_match = METHOD_MAPPING_RE.search(text, search_index)
        if not mapping_match:
            break
        signature_match = METHOD_SIGNATURE_RE.search(text, mapping_match.end())
        if not signature_match:
            search_index = mapping_match.end()
            continue

        annotation = mapping_match.group("annotation")
        method_path = mapping_match.group("path")
        params = " ".join(signature_match.group("params").split())
        body_type_match = REQUEST_BODY_TYPE_RE.search(params)
        request_type = body_type_match.group("type") if body_type_match else None
        http_method = annotation.replace("Mapping", "").upper()
        if http_method == "REQUEST":
            http_method = "ANY"

        endpoints.append(
            {
                "controller_file": str(controller_file),
                "class_prefix": normalize_endpoint(prefix),
                "method_path": normalize_endpoint(method_path),
                "endpoint_path": join_paths(prefix, method_path),
                "http_method": http_method,
                "method_name": signature_match.group("name"),
                "request_type": request_type,
            }
        )
        search_index = signature_match.end()
    return endpoints


def controller_module_name(controller_file: Path) -> str | None:
    text = str(controller_file)
    mapping = {
        "fssc-config-service": "config",
        "claim-base/claim-base-web": "claim-base",
        "claim-eer/claim-eer-web": "claim-eer",
        "claim-ptp/claim-ptp-web": "claim-ptp",
        "claim-rtr/claim-rtr-web": "claim-rtr",
        "claim-tr/claim-tr-web": "claim-tr",
        "claim-otc/claim-otc-web": "claim-otc",
        "claim-fa/claim-fa-web": "claim-fa",
        "fssc-integration-service": "integration",
        "fssc-fund-service": "fund",
        "fssc-invoice-service": "invoice",
        "fssc-bpm-service": "bpm",
        "fssc-aam-service": "aam",
        "fssc-rule-service": "rule",
        "fssc-image-service": "image",
    }
    for marker, module in mapping.items():
        if marker in text:
            return module
    return None


def load_controller_matches(workspace_root: Path, endpoint_path: str, http_method: str) -> list[dict]:
    controller_matches = []
    backend_roots = [path for path in workspace_root.glob("fssc-*-service") if path.is_dir()]
    for backend_root in backend_roots:
        for controller_file in backend_root.rglob("*Controller.java"):
            entries = parse_controller_file(controller_file)
            for entry in entries:
                if entry["endpoint_path"] != endpoint_path:
                    continue
                if entry["http_method"] not in ("ANY", http_method):
                    continue
                module_name = controller_module_name(controller_file)
                if module_name:
                    entry["module_name"] = module_name
                controller_matches.append(entry)
    return controller_matches


def load_schema_definition(schema_dir: Path, type_name: str) -> tuple[dict | None, Path | None]:
    if not type_name:
        return None, None
    for schema_file in sorted(schema_dir.glob("*.json")):
        text = schema_file.read_text(encoding="utf-8", errors="ignore")
        if f'"{type_name}"' not in text:
            continue
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            continue
        if type_name in data:
            return data[type_name], schema_file
        components = data.get("components", {}).get("schemas", {})
        if type_name in components:
            return components[type_name], schema_file
    return None, None


def build_value_from_schema(schema: dict) -> object:
    schema_type = schema.get("type")
    if schema_type == "string":
        return ""
    if schema_type == "number":
        return 0
    if schema_type == "integer":
        return 1
    if schema_type == "boolean":
        return False
    if schema_type == "array":
        return []
    if schema_type == "object":
        props = schema.get("properties", {})
        return {name: build_value_from_schema(prop) for name, prop in props.items()}
    return None


def parse_request_type(raw_type: str | None) -> dict:
    result = {
        "raw_type": raw_type,
        "is_page_param": False,
        "schema_type": None,
    }
    if not raw_type:
        return result
    match = re.match(r"""PageParam<\s*(?P<query>[^,>]+)\s*,\s*[^>]+>""", raw_type)
    if match:
        result["is_page_param"] = True
        result["schema_type"] = match.group("query").strip()
    else:
        result["schema_type"] = raw_type.strip()
    return result


def build_request_examples(request_type_info: dict, schema_definition: dict | None) -> tuple[dict, dict | None]:
    if request_type_info["is_page_param"]:
        example = {
            "pageNum": 1,
            "pageSize": 10,
            "params": {},
        }
        params_example = build_value_from_schema(schema_definition) if schema_definition else None
        return example, params_example
    if schema_definition:
        return build_value_from_schema(schema_definition), None
    return {}, None


def build_local_url(module_name: str | None, endpoint_path: str) -> str | None:
    if not module_name:
        return None
    service_info = LOCAL_SERVICE_PORTS.get(module_name)
    if not service_info or not service_info.get("port"):
        return None
    context_path = service_info["context_path"]
    base = f"http://127.0.0.1:{service_info['port']}"
    if context_path and context_path != "/":
        return base + join_paths(context_path, endpoint_path)
    return base + endpoint_path


def build_curl_template(local_url: str | None, method: str, example_body: dict, cookie_file: str) -> str | None:
    if not local_url:
        return None
    if method == "GET":
        return (
            f"curl -s -X GET '{local_url}' "
            f"-b {cookie_file} -H 'Content-Type: application/json' | python3 -m json.tool"
        )

    json_body = json.dumps(example_body, ensure_ascii=False)
    return (
        f"curl -s -X {method} '{local_url}' "
        f"-b {cookie_file} -H 'Content-Type: application/json' "
        f"-d '{json_body}' | python3 -m json.tool"
    )


def choose_selected_api(apis: dict, page_usage: dict, explicit_name: str | None) -> str | None:
    if explicit_name and explicit_name in apis:
        return explicit_name
    for preferred_role in ("request", "load", "save", "submit", "export", "delete"):
        names = page_usage.get("roles", {}).get(preferred_role, [])
        for name in names:
            if name in apis:
                return name
    return next(iter(apis), None)


def print_report(report: dict):
    print(f"target: {report['target']}")
    print(f"page_file: {report.get('page_file') or '-'}")
    print(f"service_file: {report.get('service_file') or '-'}")
    print(f"selected_api: {report.get('selected_api') or '-'}")

    roles = report.get("page_roles") or {}
    if roles:
        print("page_roles:")
        for role, names in roles.items():
            print(f"  {role}: {', '.join(names)}")

    print("apis:")
    for api in report["apis"]:
        print(f"  - name: {api['name']}")
        print(f"    method: {api['method']}")
        print(f"    domain: {api['domain']}")
        print(f"    frontend_base_url: {api.get('frontend_base_url') or '-'}")
        print(f"    endpoint_path: {api['endpoint_path']}")
        print(f"    local_module: {api.get('local_module') or '-'}")
        print(f"    local_url: {api.get('local_url') or '-'}")
        print(f"    request_type: {api.get('request_type') or '-'}")
        print(f"    schema_type: {api.get('schema_type') or '-'}")
        print(f"    schema_file: {api.get('schema_file') or '-'}")
        if api.get("controller_matches"):
            print("    controllers:")
            for match in api["controller_matches"]:
                print(
                    f"      {match['http_method']} {match['endpoint_path']} -> "
                    f"{match['controller_file']}"
                )
        if api.get("mock_matches"):
            print("    mocks:")
            for match in api["mock_matches"]:
                print(f"      {match}")
        print("    request_example:")
        print(json.dumps(api["request_example"], ensure_ascii=False, indent=6))
        if api.get("params_example") is not None:
            print("    params_example:")
            print(json.dumps(api["params_example"], ensure_ascii=False, indent=6))
        if api.get("curl_template"):
            print("    curl_template:")
            print(f"      {api['curl_template']}")


def find_mock_matches(mock_root: Path, endpoint_path: str) -> list[str]:
    matches = []
    target = endpoint_path.strip("/")
    for mock_file in mock_root.rglob("*.js"):
        text = mock_file.read_text(encoding="utf-8", errors="ignore")
        if target and target in text:
            matches.append(str(mock_file))
    return matches[:5]


def main():
    parser = argparse.ArgumentParser(
        description="Infer local API test information from fssc-web page/service code."
    )
    parser.add_argument("target", help="Page path, service path, or page/service name fragment.")
    parser.add_argument("--api-name", help="Select a specific exported API function from service.js.")
    parser.add_argument("--json", action="store_true", help="Print JSON output.")
    parser.add_argument("--primary-only", action="store_true", help="Only print the primary API.")
    parser.add_argument(
        "--workspace-root",
        default=str(detect_workspace_root()),
        help="Workspace root that contains fssc-web and backend projects.",
    )
    parser.add_argument(
        "--cookie-file",
        default="/tmp/fssc-cookies.txt",
        help="Cookie file path used to render curl templates.",
    )
    args = parser.parse_args()

    workspace_root = Path(args.workspace_root).resolve()
    frontend_root = workspace_root / "fssc-web"
    framework_root = workspace_root / "fssc-web-framework"
    schema_dir = frontend_root / "src/json-schema"
    mock_root = frontend_root / "mock"
    http_config_file = framework_root / "src/config/http/index.js"

    if not frontend_root.exists():
        print(f"frontend root not found: {frontend_root}", file=sys.stderr)
        sys.exit(2)
    if not http_config_file.exists():
        print(f"http config not found: {http_config_file}", file=sys.stderr)
        sys.exit(3)

    target_path = resolve_path(args.target, frontend_root)
    if not target_path:
        print(f"target not found: {args.target}", file=sys.stderr)
        sys.exit(4)

    page_file = None
    service_file = None
    if target_path.suffix == ".vue":
        page_file = target_path
        service_file = resolve_service_from_page(page_file)
    elif target_path.name == "service.js":
        service_file = target_path
        sibling_page = service_file.parent / "index.vue"
        if sibling_page.exists():
            page_file = sibling_page.resolve()
    else:
        service_candidate = target_path.parent / "service.js"
        if service_candidate.exists():
            service_file = service_candidate.resolve()
        if target_path.suffix == ".js":
            service_file = target_path

    if not service_file or not service_file.exists():
        print(f"service.js not found for target: {target_path}", file=sys.stderr)
        sys.exit(5)

    domain_map = parse_http_domain_map(http_config_file)
    api_defs = parse_service_exports(service_file)
    if not api_defs:
        print(f"no exported API calls parsed from: {service_file}", file=sys.stderr)
        sys.exit(6)
    if args.api_name and args.api_name not in api_defs:
        print(f"api name not found in service file: {args.api_name}", file=sys.stderr)
        sys.exit(7)

    page_usage = parse_page_usage(page_file) if page_file and page_file.exists() else {"imports": {}, "roles": {}}
    selected_api = choose_selected_api(api_defs, page_usage, args.api_name)

    results = []
    for api_name, api_def in api_defs.items():
        if args.api_name and api_name != args.api_name:
            continue
        if args.primary_only and selected_api and api_name != selected_api:
            continue

        frontend_base_url = domain_map.get(api_def["domain"])
        local_module = DOMAIN_TO_MODULE.get(api_def["domain"])

        controller_matches = load_controller_matches(
            workspace_root,
            api_def["endpoint_path"],
            api_def["method"],
        )
        if controller_matches:
            local_module = controller_matches[0].get("module_name") or local_module

        request_type = controller_matches[0].get("request_type") if controller_matches else None
        request_type_info = parse_request_type(request_type)
        schema_definition, schema_file = load_schema_definition(schema_dir, request_type_info["schema_type"])
        request_example, params_example = build_request_examples(request_type_info, schema_definition)
        local_url = build_local_url(local_module, api_def["endpoint_path"])
        curl_template = build_curl_template(local_url, api_def["method"], request_example, args.cookie_file)
        mock_matches = find_mock_matches(mock_root, api_def["endpoint_path"])

        results.append(
            {
                "name": api_name,
                "method": api_def["method"],
                "domain": api_def["domain"],
                "frontend_base_url": frontend_base_url,
                "path_expr": api_def["path_expr"],
                "endpoint_path": api_def["endpoint_path"],
                "payload_expr": api_def["payload_expr"],
                "options_expr": api_def["options_expr"],
                "local_module": local_module,
                "local_url": local_url,
                "controller_matches": controller_matches,
                "request_type": request_type_info["raw_type"],
                "schema_type": request_type_info["schema_type"],
                "schema_file": str(schema_file) if schema_file else None,
                "request_example": request_example,
                "params_example": params_example,
                "curl_template": curl_template,
                "mock_matches": mock_matches,
            }
        )

    report = {
        "target": args.target,
        "page_file": normalize_rel(page_file, workspace_root) if page_file else None,
        "service_file": normalize_rel(service_file, workspace_root) if service_file else None,
        "selected_api": selected_api,
        "page_roles": page_usage.get("roles", {}),
        "apis": results,
    }

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return

    print_report(report)


if __name__ == "__main__":
    main()
