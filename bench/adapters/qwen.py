from __future__ import annotations

import json
import os

from common import BENCH, RunContext, base_url, find_bin, rules_text, run_cmd

ID = "qwen"
KIND = "harness"


def available() -> tuple[bool, str]:
    path = find_bin("QWEN_BIN", BENCH / "qwen")
    if path:
        return True, str(path)
    return False, "qwen CLI not found (set QWEN_BIN)"


def run(ctx: RunContext) -> dict:
    ok, binary = available()
    if not ok:
        return {"error": binary, "answer": "", "tools": [], "tool_calls": 0, "timed_out": False, "exit_code": 1}
    prompt = rules_text() + "\n\n" + ctx.task["prompt"]
    env = dict(os.environ)
    env["QWEN_USAGE_STATISTICS_ENABLED"] = "0"
    env["OPENAI_BASE_URL"] = base_url()
    env["OPENAI_API_KEY"] = "none"
    cmd = [
        binary,
        "-p",
        prompt,
        "--output-format",
        "stream-json",
        "--approval-mode",
        "yolo",
        "-m",
        ctx.model,
    ]
    out, code, timed_out, _ = run_cmd(cmd, ctx.project, env, ctx.timeout, ctx.log_path)
    tools: list[str] = []
    texts: list[str] = []
    for line in out.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        t = str(event.get("type") or event.get("kind") or "")
        if "tool" in t.lower():
            tools.append(str(event.get("name") or event.get("tool") or "tool"))
        if event.get("content") or event.get("text"):
            texts.append(str(event.get("content") or event.get("text")))
    return {
        "answer": (texts[-1] if texts else out[-700:]),
        "tools": tools,
        "tool_calls": len(tools),
        "timed_out": timed_out,
        "exit_code": code,
        "error": None,
        "raw_tail": out[-700:],
    }
