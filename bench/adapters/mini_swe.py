from __future__ import annotations

import os

from common import BENCH, RunContext, base_url, find_bin, rules_text, run_cmd, which

ID = "mini_swe"
KIND = "harness"


def available() -> tuple[bool, str]:
    path = find_bin("MINI_SWE_BIN", BENCH / "mini-swe")
    if path:
        return True, str(path)
    found = which("mini")
    if found:
        return True, str(found)
    return False, "mini-swe-agent not found (pip install mini-swe-agent, set MINI_SWE_BIN)"


def run(ctx: RunContext) -> dict:
    ok, binary = available()
    if not ok:
        return {"error": binary, "answer": "", "tools": [], "tool_calls": 0, "timed_out": False, "exit_code": 1}
    prompt = rules_text() + "\n\n" + ctx.task["prompt"]
    env = dict(os.environ)
    env["MSWEA_CONFIGURED"] = "1"
    env["MSWEA_COST_TRACKING"] = "ignore_errors"
    env["OPENAI_API_BASE"] = base_url()
    env["OPENAI_API_KEY"] = "none"
    cmd = [
        binary,
        "-t",
        prompt,
        "-y",
        "--exit-immediately",
        "-m",
        f"openai/{ctx.model}",
        "-o",
        str(ctx.log_path.with_suffix(".traj.json")),
    ]
    out, code, timed_out, _ = run_cmd(cmd, ctx.project, env, ctx.timeout, ctx.log_path)
    tools = ["bash"] if "bash" in out.lower() or "docker" in out.lower() else []
    return {
        "answer": out[-700:],
        "tools": tools,
        "tool_calls": out.lower().count("tool"),
        "timed_out": timed_out,
        "exit_code": code,
        "error": None,
        "raw_tail": out[-700:],
    }
