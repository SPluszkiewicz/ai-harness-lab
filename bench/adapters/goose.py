from __future__ import annotations

import json
import os

from common import BENCH, RunContext, base_url, ctx_limit, find_bin, rules_text, run_cmd

ID = "goose"
KIND = "harness"


def available() -> tuple[bool, str]:
    path = find_bin("GOOSE_BIN", BENCH / "goose")
    if path:
        return True, str(path)
    return False, "goose.exe not found (set GOOSE_BIN or place under bench/goose/)"


def run(ctx: RunContext) -> dict:
    ok, binary = available()
    if not ok:
        return {"error": binary, "answer": "", "tools": [], "tool_calls": 0, "timed_out": False, "exit_code": 1}
    prompt = ctx.task["prompt"]
    host = base_url()
    if host.endswith("/v1"):
        host = host[: -3]
    env = dict(os.environ)
    env.update(
        {
            "GOOSE_PROVIDER": "openai",
            "GOOSE_MODEL": ctx.model,
            "GOOSE_MODE": "auto",
            "OPENAI_HOST": host,
            "OPENAI_BASE_PATH": "v1/chat/completions",
            "OPENAI_API_KEY": "none",
            "GOOSE_DISABLE_KEYRING": "1",
            "GOOSE_TELEMETRY": "false",
            "GOOSE_CONTEXT_LIMIT": str(ctx_limit()),
        }
    )
    cmd = [
        binary,
        "run",
        "--no-session",
        "-q",
        "--output-format",
        "stream-json",
        "--max-turns",
        "24",
        "--system",
        rules_text(),
        "-t",
        prompt,
    ]
    out, code, timed_out, _ = run_cmd(cmd, ctx.project, env, ctx.timeout, ctx.log_path)
    tools: list[str] = []
    answers: list[str] = []
    for line in out.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        for part in ((event.get("message") or {}).get("content") or []):
            if not isinstance(part, dict):
                continue
            if part.get("type") == "toolRequest":
                call = part.get("toolCall") or {}
                value = call.get("value") if isinstance(call, dict) else {}
                tools.append(str((value or {}).get("name") or part.get("name") or "?"))
            elif part.get("type") == "text" and part.get("text"):
                answers.append(part["text"])
    answer = "".join(answers).strip() or out[-700:]
    return {
        "answer": answer,
        "tools": tools,
        "tool_calls": len(tools),
        "timed_out": timed_out,
        "exit_code": code,
        "error": None,
        "raw_tail": out[-700:],
    }
