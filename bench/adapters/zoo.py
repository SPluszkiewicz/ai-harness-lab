from __future__ import annotations

import os

from adapters.cliutil import finish, missing, scrape_jsonl
from common import RunContext, base_url, rules_text, run_cmd

ID = "zoo"
KIND = "harness"


def available() -> tuple[bool, str]:
    return missing(
        "ZOO_BIN",
        "zoo",
        "zoo CLI not found (npm i -g @zoo-code/cli or set ZOO_BIN). Fork of Roo; CLI may lack a local base_url.",
    )


def run(ctx: RunContext) -> dict:
    ok, binary = available()
    if not ok:
        return {"error": binary, "answer": "", "tools": [], "tool_calls": 0, "timed_out": False, "exit_code": 1}
    prompt = rules_text() + "\n\n" + ctx.task["prompt"]
    env = dict(os.environ)
    env["OPENAI_BASE_URL"] = base_url()
    env["OPENAI_API_KEY"] = "none"
    env["TELEMETRY_SETTING"] = "disabled"
    cmd = [
        binary,
        "--print",
        "--output-format",
        "stream-json",
        "--ephemeral",
        "--oneshot",
        prompt,
    ]
    out, code, timed_out, _ = run_cmd(cmd, ctx.project, env, ctx.timeout, ctx.log_path)
    tools, texts = scrape_jsonl(out)
    return finish(out, code, timed_out, tools, texts)
