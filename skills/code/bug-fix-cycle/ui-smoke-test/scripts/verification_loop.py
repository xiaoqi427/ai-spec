#!/usr/bin/env python3
"""Run ranked candidates against a probe command until pass or real fail."""

from __future__ import annotations

import argparse
import json
import subprocess
import time
from pathlib import Path


class SafeDict(dict):
    def __missing__(self, key: str) -> str:
        return ""


def render_command(template: str, mapping: dict[str, object]) -> str:
    rendered = template
    for key, value in mapping.items():
        rendered = rendered.replace(f"{{{key}}}", "" if value is None else str(value))
    return rendered


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Loop SIT verification candidates.")
    parser.add_argument("--bug-id", required=True, help="Coding bug id.")
    parser.add_argument("--candidates-json", required=True, help="Candidates file from bug_candidate_search.py.")
    parser.add_argument("--probe-command", required=True, help="Shell command template. Supports {claim_no}, {claim_id}, {item_id}, {item2_id}.")
    parser.add_argument("--refresh-state-command", help="Optional shell command to refresh auth state.")
    parser.add_argument("--env-retries", type=int, default=2, help="Retries for env_blocked.")
    parser.add_argument("--max-attempts", type=int, default=20, help="Hard cap for attempts.")
    parser.add_argument("--output-log", help="Optional JSON log output path.")
    return parser.parse_args()


def load_candidates(path: Path) -> list[dict]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        return list(payload.get("candidates") or [])
    if isinstance(payload, list):
        return payload
    raise ValueError("Unsupported candidates JSON structure.")


def extract_probe_json(stdout: str) -> dict:
    for line in reversed([line.strip() for line in stdout.splitlines() if line.strip()]):
        if not line.startswith("{"):
            continue
        try:
            return json.loads(line)
        except json.JSONDecodeError:
            continue
    raise ValueError("Probe stdout does not contain a JSON object.")


def run_shell(command: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
        check=False,
    )


def main() -> int:
    args = parse_args()
    candidates = load_candidates(Path(args.candidates_json))
    attempts: list[dict] = []
    state_refreshed = False
    total_attempts = 0

    for candidate in candidates:
        if total_attempts >= args.max_attempts:
            break

        env_retry = 0
        while True:
            if total_attempts >= args.max_attempts:
                break

            total_attempts += 1
            command = render_command(
                args.probe_command,
                SafeDict(
                    {
                        "bug_id": args.bug_id,
                        **candidate,
                    }
                ),
            )
            result = run_shell(command)

            try:
                probe = extract_probe_json(result.stdout)
            except Exception as exc:  # noqa: BLE001
                probe = {
                    "status": "fail",
                    "message": f"Probe output parse error: {exc}",
                    "snippet": (result.stdout or result.stderr)[-800:],
                }

            status = probe.get("status", "fail")
            attempt = {
                "candidate": candidate,
                "command": command,
                "returncode": result.returncode,
                "status": status,
                "probe": probe,
                "stdout_tail": result.stdout[-1200:],
                "stderr_tail": result.stderr[-1200:],
            }
            attempts.append(attempt)

            if status == "pass":
                summary = {
                    "bug_id": args.bug_id,
                    "status": "pass",
                    "attempts": attempts,
                    "winner": candidate,
                }
                if args.output_log:
                    Path(args.output_log).write_text(
                        f"{json.dumps(summary, ensure_ascii=False, indent=2)}\n",
                        encoding="utf-8",
                    )
                print(json.dumps(summary, ensure_ascii=False, indent=2))
                return 0

            if status == "sample_mismatch":
                break

            if status == "auth_expired" and args.refresh_state_command and not state_refreshed:
                refresh = run_shell(args.refresh_state_command)
                attempts.append(
                    {
                        "candidate": candidate,
                        "command": args.refresh_state_command,
                        "returncode": refresh.returncode,
                        "status": "auth_refresh",
                        "stdout_tail": refresh.stdout[-1200:],
                        "stderr_tail": refresh.stderr[-1200:],
                    }
                )
                state_refreshed = True
                continue

            if status == "env_blocked" and env_retry < args.env_retries:
                env_retry += 1
                time.sleep(2 if env_retry == 1 else 5 * env_retry)
                continue

            summary = {
                "bug_id": args.bug_id,
                "status": status,
                "attempts": attempts,
                "last_candidate": candidate,
            }
            if args.output_log:
                Path(args.output_log).write_text(
                    f"{json.dumps(summary, ensure_ascii=False, indent=2)}\n",
                    encoding="utf-8",
                )
            print(json.dumps(summary, ensure_ascii=False, indent=2))
            return 1

    summary = {
        "bug_id": args.bug_id,
        "status": "exhausted",
        "attempts": attempts,
        "message": "All candidates were consumed without a pass.",
    }
    if args.output_log:
        Path(args.output_log).write_text(
            f"{json.dumps(summary, ensure_ascii=False, indent=2)}\n",
            encoding="utf-8",
        )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
