#!/usr/bin/env python3
"""Extract and rank SIT sample candidates for a Coding bug."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import tempfile
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable

import yaml

CLAIM_NO_RE = re.compile(r"\b\d{20}\b")
CLAIM_ID_RE = re.compile(r"\bclaimId\s*[:=]\s*(\d{6,})\b", re.IGNORECASE)
TEMPLATE_RE = re.compile(r"\bT\d{3}\b")
ITEM2_RE = re.compile(
    r"\b(?:item2Id|业务大类(?:编码)?|业务类别|业务小类)\s*[:=：]?\s*(\d{6,9})\b",
    re.IGNORECASE,
)
PROCESS_STATE_RE = re.compile(
    r"\b(rootDrafterActivity|drafterActivity|accountAuditActivity|bizAccountActivity)\b",
    re.IGNORECASE,
)


@dataclass
class Candidate:
    claim_no: str
    score: int
    source: str
    reason: list[str] = field(default_factory=list)
    claim_id: str | None = None
    item_id: str | None = None
    item2_id: str | None = None
    item3_id: str | None = None
    process_state_eng: str | None = None
    status: str | None = None
    table_source: str | None = None


def read_text_if_exists(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def extract_section(text: str, heading: str) -> str:
    pattern = re.compile(
        rf"(^##\s+{re.escape(heading)}\s*$.*?)(?=^##\s+\S|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    return match.group(1) if match else ""


def add_or_merge(
    candidates: dict[str, Candidate],
    claim_no: str,
    score: int,
    source: str,
    reason: str,
    **extra: str | None,
) -> None:
    existing = candidates.get(claim_no)
    if existing is None:
        candidates[claim_no] = Candidate(
            claim_no=claim_no,
            score=score,
            source=source,
            reason=[reason],
            **extra,
        )
        return

    existing.score = max(existing.score, score)
    if reason not in existing.reason:
        existing.reason.append(reason)
    for key, value in extra.items():
        if value and not getattr(existing, key):
            setattr(existing, key, value)


def load_bug_material(args: argparse.Namespace) -> tuple[dict, dict[str, str]]:
    bug_dir = args.bug_dir
    if not bug_dir and args.bug_id:
        bug_dir = str(Path(args.prefetch_root) / str(args.bug_id))
    if not bug_dir:
        raise ValueError("Either --bug-dir or --bug-id with --prefetch-root is required.")

    bug_path = Path(bug_dir)
    if not bug_path.exists():
        raise FileNotFoundError(f"Bug directory not found: {bug_path}")

    metadata = {}
    metadata_file = bug_path / "metadata.json"
    if metadata_file.exists():
        metadata = json.loads(metadata_file.read_text(encoding="utf-8"))

    files = {
        "detail": read_text_if_exists(bug_path / "detail.txt"),
        "comments": read_text_if_exists(bug_path / "comments.txt"),
        "handoff": read_text_if_exists(bug_path / "frontend-handoff.md"),
        "manual": "",
        "sit_log": "",
    }

    bug_id = str(args.bug_id or metadata.get("id") or bug_path.name)
    if args.manual_checklist and Path(args.manual_checklist).exists():
        files["manual"] = extract_section(
            Path(args.manual_checklist).read_text(encoding="utf-8"), bug_id
        )
    if args.sit_log and Path(args.sit_log).exists():
        files["sit_log"] = extract_section(
            Path(args.sit_log).read_text(encoding="utf-8"), bug_id
        )

    return metadata, files


def collect_hints(metadata: dict, files: dict[str, str]) -> dict[str, list[str] | str | None]:
    template = str(metadata.get("template") or "")
    if not template:
        for content in files.values():
            match = TEMPLATE_RE.search(content)
            if match:
                template = match.group(0)
                break

    item2_ids: set[str] = set()
    process_states: set[str] = set()
    for content in files.values():
        item2_ids.update(ITEM2_RE.findall(content))
        process_states.update(
            match.group(1) for match in PROCESS_STATE_RE.finditer(content)
        )

    title = str(metadata.get("title") or "")
    return {
        "template": template,
        "item2_ids": sorted(item2_ids),
        "process_states": sorted(process_states),
        "title": title,
    }


def extract_explicit_candidates(files: dict[str, str], metadata: dict) -> dict[str, Candidate]:
    sources = {
        "detail": (files.get("detail", ""), 100, "Coding/offline detail explicit sample"),
        "comments": (files.get("comments", ""), 90, "Coding/offline comment explicit sample"),
        "sit_log": (files.get("sit_log", ""), 85, "SIT execution log sample"),
        "manual": (files.get("manual", ""), 80, "SIT manual checklist sample"),
        "handoff": (files.get("handoff", ""), 75, "handoff sample"),
    }

    candidates: dict[str, Candidate] = {}
    item_id = str(metadata.get("template") or "") or None

    for source_name, (content, base_score, reason) in sources.items():
        if not content:
            continue
        claim_ids = CLAIM_ID_RE.findall(content)
        for claim_no in CLAIM_NO_RE.findall(content):
            add_or_merge(
                candidates,
                claim_no,
                base_score,
                source_name,
                reason,
                item_id=item_id,
                claim_id=claim_ids[0] if claim_ids else None,
            )

    return candidates


def read_db_config(config_path: Path, env_name: str) -> dict[str, str]:
    data = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    env = (data.get("environments") or {}).get(env_name)
    if not env:
        raise KeyError(f"Environment '{env_name}' not found in {config_path}")
    required = ["host", "port", "sid", "username", "password"]
    missing = [key for key in required if not env.get(key)]
    if missing:
        raise ValueError(f"Incomplete DB config for '{env_name}': missing {', '.join(missing)}")
    return env


def build_similarity_sql(template: str, item2_ids: list[str], limit: int) -> str:
    prefix = ""
    if item2_ids:
        prefix = item2_ids[0][:3]
        quoted = ", ".join(f"'{item2_id}'" for item2_id in item2_ids)
        priority_expr = (
            f"CASE WHEN item2_id IN ({quoted}) THEN 0 "
            f"WHEN item2_id LIKE '{prefix}%' THEN 1 ELSE 2 END"
        )
        filter_expr = f"AND (item2_id IN ({quoted}) OR item2_id LIKE '{prefix}%')"
    else:
        priority_expr = "0"
        filter_expr = ""

    return f"""
SET HEADING OFF
SET FEEDBACK OFF
SET PAGESIZE 0
SET VERIFY OFF
SET LINESIZE 400
SET TRIMSPOOL ON

WITH base AS (
    SELECT 'CUR' src, claim_id, claim_no, item_id, item2_id, item3_id, process_state_eng, status, cur_receive_date
    FROM T_RMBS_CLAIM
    WHERE item_id = '{template}'
    UNION ALL
    SELECT 'HIS' src, claim_id, claim_no, item_id, item2_id, item3_id, process_state_eng, status, cur_receive_date
    FROM T_RMBS_CLAIM_HIS
    WHERE item_id = '{template}'
)
SELECT src || '|' || claim_id || '|' || claim_no || '|' || NVL(item2_id, '') || '|' ||
       NVL(item3_id, '') || '|' || NVL(process_state_eng, '') || '|' || NVL(status, '')
FROM (
    SELECT *
    FROM base
    WHERE claim_no IS NOT NULL
    {filter_expr}
    ORDER BY {priority_expr}, cur_receive_date DESC NULLS LAST
)
WHERE ROWNUM <= {int(limit)};
EXIT
"""


def query_db_candidates(
    template: str,
    item2_ids: list[str],
    db_config_path: Path,
    db_env: str,
    limit: int,
) -> list[Candidate]:
    env = read_db_config(db_config_path, db_env)
    tool = env.get("tool") or "sql"
    conn = f"{env['username']}/{env['password']}@{env['host']}:{env['port']}/{env['sid']}"
    sql_text = build_similarity_sql(template, item2_ids, limit)

    with tempfile.NamedTemporaryFile("w", suffix=".sql", delete=False, encoding="utf-8") as handle:
        handle.write(sql_text)
        sql_file = handle.name

    try:
        result = subprocess.run(
            [tool, conn, f"@{sql_file}"],
            capture_output=True,
            text=True,
            check=False,
            timeout=90,
        )
    finally:
        Path(sql_file).unlink(missing_ok=True)

    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "DB query failed")

    candidates: list[Candidate] = []
    rank = 0
    exact_item2 = set(item2_ids)
    prefix = item2_ids[0][:3] if item2_ids else ""
    for line in result.stdout.splitlines():
        if line.count("|") < 6:
            continue
        src, claim_id, claim_no, item2_id, item3_id, process_state_eng, status = [
            part.strip() for part in line.split("|", 6)
        ]
        if not claim_no:
            continue
        score = 40
        reason = "DB fallback same template"
        if item2_id and item2_id in exact_item2:
            score = 70
            reason = "DB fallback exact item2"
        elif item2_id and prefix and item2_id.startswith(prefix):
            score = 55
            reason = "DB fallback item2 prefix"
        score += max(0, 5 - rank)
        rank += 1
        candidates.append(
            Candidate(
                claim_no=claim_no,
                claim_id=claim_id or None,
                item_id=template,
                item2_id=item2_id or None,
                item3_id=item3_id or None,
                process_state_eng=process_state_eng or None,
                status=status or None,
                table_source=src,
                source="db",
                score=score,
                reason=[reason],
            )
        )

    return candidates


def sorted_candidates(candidates: Iterable[Candidate]) -> list[Candidate]:
    return sorted(
        candidates,
        key=lambda candidate: (
            -candidate.score,
            candidate.claim_no,
        ),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract and rank SIT bug candidates.")
    parser.add_argument("--bug-id", type=str, help="Coding bug id.")
    parser.add_argument("--bug-dir", type=str, help="Local bug material directory.")
    parser.add_argument(
        "--prefetch-root",
        type=str,
        default="/Users/xiaoqi/Documents/work/yili/yili-out/bug-prefetch",
        help="Default root used with --bug-id.",
    )
    parser.add_argument(
        "--manual-checklist",
        type=str,
        default="/Users/xiaoqi/Documents/work/yili/yili-out/bug-prefetch/sit-manual-checklist-20260405.md",
    )
    parser.add_argument(
        "--sit-log",
        type=str,
        default="/Users/xiaoqi/Documents/work/yili/yili-out/bug-prefetch/sit-execution-log-20260405.md",
    )
    parser.add_argument("--db-config", type=str, help="DB connection yaml.")
    parser.add_argument("--db-env", type=str, default="sit", help="DB environment name.")
    parser.add_argument("--db-limit", type=int, default=12, help="Max DB fallback rows.")
    parser.add_argument("--output", type=str, help="Optional JSON output path.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    metadata, files = load_bug_material(args)
    hints = collect_hints(metadata, files)

    candidates = extract_explicit_candidates(files, metadata)
    errors: list[str] = []

    if args.db_config and hints.get("template"):
        try:
            for candidate in query_db_candidates(
                str(hints["template"]),
                list(hints["item2_ids"]),
                Path(args.db_config),
                args.db_env,
                args.db_limit,
            ):
                add_or_merge(
                    candidates,
                    candidate.claim_no,
                    candidate.score,
                    candidate.source,
                    candidate.reason[0],
                    claim_id=candidate.claim_id,
                    item_id=candidate.item_id,
                    item2_id=candidate.item2_id,
                    item3_id=candidate.item3_id,
                    process_state_eng=candidate.process_state_eng,
                    status=candidate.status,
                    table_source=candidate.table_source,
                )
        except Exception as exc:  # noqa: BLE001
            errors.append(f"db_fallback_error: {exc}")

    output = {
        "bug_id": args.bug_id or metadata.get("id") or Path(args.bug_dir).name,
        "metadata": metadata,
        "hints": hints,
        "errors": errors,
        "candidates": [asdict(candidate) for candidate in sorted_candidates(candidates.values())],
    }

    payload = json.dumps(output, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(f"{payload}\n", encoding="utf-8")
    print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
