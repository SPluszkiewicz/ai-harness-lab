from __future__ import annotations

import os

from adapters.cliutil import finish, missing
from common import RunContext, base_url, rules_text, run_cmd

ID = "openhands"
KIND = "harness"


def available() -> tuple[bool, str]:
    return missing(
        "OPENHANDS_BIN",
        "openhands",
        "openhands CLI not found (pip install openhands-sdk / set OPENHANDS_BIN)",
    )


def run(ctx: RunContext) -> dict:
    ok, binary = available()
    if not ok:
        return {"error": binary, "answer": "", "tools": [], "tool_calls": 0, "timed_out": False, "exit_code": 1}
    prompt = rules_text() + "\n\n" + ctx.task["prompt"]
    env = dict(os.environ)
    env["LLM_MODEL"] = f"openai/{ctx.model}"
    env["LLM_BASE_URL"] = base_url()
    env["LLM_API_KEY"] = "none"
    env["OPENAI_API_KEY"] = "none"
    env["OPENAI_BASE_URL"] = base_url()
    env["AGENT_CANVAS_DISABLE_TELEMETRY"] = "1"
    env["VITE_DO_NOT_TRACK"] = "1"
    cmd = [binary, "--headless", "-t", prompt]
    out, code, timed_out, _ = run_cmd(cmd, ctx.project, env, ctx.timeout, ctx.log_path)
    tools = [w for w in ("terminal", "file_editor", "apply_patch", "grep", "glob") if w in out.lower()]
    return finish(out, code, timed_out, tools, [out[-700:]] if out.strip() else [])
