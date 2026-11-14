from __future__ import annotations

import os

from adapters.cliutil import finish, missing
from common import RunContext, base_url, rules_text, run_cmd

ID = "refact"
KIND = "harness"


def available() -> tuple[bool, str]:
    return missing("REFACT_BIN", "refact", "refact CLI not found (set REFACT_BIN)")


def run(ctx: RunContext) -> dict:
    ok, binary = available()
    if not ok:
        return {"error": binary, "answer": "", "tools": [], "tool_calls": 0, "timed_out": False, "exit_code": 1}
    prompt = rules_text() + "\n\n" + ctx.task["prompt"]
    env = dict(os.environ)
    env["OPENAI_BASE_URL"] = base_url()
    env["OPENAI_API_KEY"] = "none"
    # Headless agent; if the installed CLI uses another subcommand, the trial is ERR not SKIP.
    cmd = [binary, "agent", "--yes", "--project", str(ctx.project), prompt]
    out, code, timed_out, _ = run_cmd(cmd, ctx.project, env, ctx.timeout, ctx.log_path)
    tools = [w for w in ("shell", "apply_patch", "cat", "tree") if w in out.lower()]
    return finish(out, code, timed_out, tools, [out[-700:]] if out.strip() else [])
