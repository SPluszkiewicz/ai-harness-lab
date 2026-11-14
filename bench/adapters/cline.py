from __future__ import annotations

import json
import os

from common import BENCH, RunContext, base_url, find_bin, rules_text, run_cmd

ID = "cline"
KIND = "harness"


def available() -> tuple[bool, str]:
    path = find_bin("CLINE_BIN", BENCH / "cline")
    if path:
        return True, str(path)
    return False, "cline CLI not found (npm i -g cline, set CLINE_BIN)"


def run(ctx: RunContext) -> dict:
    ok, binary = available()
    if not ok:
        return {"error": binary, "answer": "", "tools": [], "tool_calls": 0, "timed_out": False, "exit_code": 1}
    prompt = rules_text() + "\n\n" + ctx.task["prompt"]
    env = dict(os.environ)
    env["OPENAI_BASE_URL"] = base_url()
    env["OPENAI_API_KEY"] = "none"
    cmd = [
        binary,
        "--json",
        "-c",
        str(ctx.project),
        "-t",
        str(ctx.timeout),
        prompt,
    ]
    out, code, timed_out, _ = run_cmd(cmd, ctx.project, env, ctx.timeout, ctx.log_path)
    tools: list[str] = []
    texts: list[str] = []
    for line in out.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        kind = str(event.get("type") or event.get("event") or "")
        if "tool" in kind.lower() or event.get("tool"):
            tools.append(str(event.get("tool") or event.get("name") or "tool"))
        if event.get("text") or event.get("content"):
            texts.append(str(event.get("text") or event.get("content")))
    return {
        "answer": texts[-1] if texts else out[-700:],
        "tools": tools,
        "tool_calls": len(tools),
        "timed_out": timed_out,
        "exit_code": code,
        "error": None,
        "raw_tail": out[-700:],
    }
