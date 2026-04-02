#!/usr/bin/env python3
import argparse
import os
import re
import sys
from pathlib import Path


ROUTE_COMPONENT_RE = re.compile(
    r"""path:\s*['"`](?P<route>[^'"`]+)['"`][\s\S]{0,400}?component:\s*\(\)\s*=>\s*import\([\s\S]{0,400}?['"`]@/(?P<component>page/[^'"`]+)['"`]""",
    re.MULTILINE,
)
MODULE_BASE_RE = re.compile(r"""MODULE_BASE_URL\s*=\s*['"`]([^'"`]+)['"`]""")


def normalize_target(target: str) -> str:
    target = target.strip()
    target = target.replace("\\", "/")
    target = re.sub(r"^/+", "", target)
    target = re.sub(r"^src/", "", target)
    target = re.sub(r"^@/", "", target)
    return target


def collect_routes(route_root: Path):
    routes = []
    for route_file in sorted(route_root.rglob("*.js")):
        text = route_file.read_text(encoding="utf-8", errors="ignore")
        module_base = ""
        module_match = MODULE_BASE_RE.search(text)
        if module_match:
            module_base = module_match.group(1).strip("/")

        for match in ROUTE_COMPONENT_RE.finditer(text):
            child_route = match.group("route").strip("/")
            component = match.group("component").strip()
            full_path = "/".join(p for p in [module_base, child_route] if p)
            routes.append(
                {
                    "route_file": str(route_file),
                    "module_base": module_base,
                    "child_route": child_route,
                    "full_path": f"/{full_path}",
                    "component": component,
                }
            )
    return routes


def score_entry(entry, target: str) -> int:
    score = 0
    component = entry["component"]
    full_path = entry["full_path"]
    child_route = entry["child_route"]

    if target == component:
        score += 100
    if target in component:
        score += 40
    if component.endswith(target):
        score += 35
    if target in full_path:
        score += 25
    if target == child_route:
        score += 30
    if component.endswith("/index.vue") and target == component[: -len("/index.vue")]:
        score += 50
    if target.endswith("/index.vue") and target[: -len("/index.vue")] == component[: -len("/index.vue")]:
        score += 50
    return score


def main():
    parser = argparse.ArgumentParser(
        description="Resolve fssc-web route URL from page path, component path, or route fragment."
    )
    parser.add_argument("target", help="Page path, component path, route fragment, or route URL suffix.")
    parser.add_argument(
        "--project-root",
        default="/Users/xiaoqi/Documents/work/yili/fssc-web",
        help="fssc-web project root",
    )
    parser.add_argument(
        "--base-url",
        default=os.environ.get("FSSC_BASE_URL", "http://localhost:8080"),
        help="Base URL for local dev server",
    )
    parser.add_argument(
        "--open",
        action="store_true",
        help="Print an agent-browser command for opening the resolved URL.",
    )
    args = parser.parse_args()

    project_root = Path(args.project_root)
    route_root = project_root / "src/config/route"
    if not route_root.exists():
        print(f"route root not found: {route_root}", file=sys.stderr)
        sys.exit(2)

    target = normalize_target(args.target)
    routes = collect_routes(route_root)
    if not routes:
        print("no route entries found", file=sys.stderr)
        sys.exit(3)

    ranked = []
    for entry in routes:
        score = score_entry(entry, target)
        if score > 0:
            ranked.append((score, entry))

    if not ranked:
        print(f"no route matched target: {target}", file=sys.stderr)
        sys.exit(4)

    ranked.sort(key=lambda item: (-item[0], item[1]["full_path"]))
    best_score, best = ranked[0]
    url = f"{args.base_url.rstrip('/')}{best['full_path']}"

    print(f"target: {target}")
    print(f"matched_component: {best['component']}")
    print(f"route_file: {best['route_file']}")
    print(f"route_path: {best['full_path']}")
    print(f"url: {url}")
    print(f"score: {best_score}")

    if args.open:
        print(f"agent-browser open {url}")


if __name__ == "__main__":
    main()
