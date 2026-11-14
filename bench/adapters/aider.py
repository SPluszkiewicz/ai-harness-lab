from __future__ import annotations

import os
import sys

from common import BENCH, RunContext, base_url, materialize_rules, run_cmd, which

ID = "aider"
KIND = "harness"


def available() -> tuple[bool, str]:
    if (BENCH / "aider" / "site").exists():
        return True, sys.executable
    if which("aider"):
        return True, "aider"
    return False, "aider not found (uv tool install aider-chat, or site under bench/aider/site)"


def run(ctx: RunContext) -> dict:
    ok, binary = available()
    if not ok:
        return {"error": binary, "answer": "", "tools": [], "tool_calls": 0, "timed_out": False, "exit_code": 1}
    prompt = ctx.task["prompt"]
    env = dict(os.environ)
    site = BENCH / "aider" / "site"
    if site.exists():
        env["PYTHONPATH"] = str(site)
    env["OPENAI_API_BASE"] = base_url()
    env["OPENAI_API_KEY"] = "none"
    env["AIDER_ANALYTICS"] = "false"
    if binary == sys.executable:
        cmd = [sys.executable, "-m", "aider.main"]
    else:
        cmd = [binary]
    cmd += [
        "--model",
        f"openai/{ctx.model}",
        "--openai-api-base",
        base_url(),
        "--openai-api-key",
        "none",
        "--no-auto-commits",
        "--no-dirty-commits",
        "--yes-always",
        "--no-pretty",
        "--no-stream",
        "--no-gitignore",
        "--no-show-model-warnings",
        "--map-tokens",
        "1024",
        "--read",
        str(materialize_rules()),
        "--message",
        prompt,
    ]
    for rel in ctx.task.get("chat_files") or []:
        if (ctx.project / rel).is_file():
            cmd += ["--file", rel]
    out, code, timed_out, _ = run_cmd(cmd, ctx.project, env, ctx.timeout, ctx.log_path)
    blocks = [b.strip() for b in out.split("\n\n") if len(b.strip()) > 40]
    answer = blocks[-1][:700] if blocks else out[-700:]
    return {
        "answer": answer,
        "tools": ["edit"] if ctx.task.get("kind") == "edit" else [],
        "tool_calls": 1 if ctx.task.get("kind") == "edit" else 0,
        "timed_out": timed_out,
        "exit_code": code,
        "error": None,
        "raw_tail": out[-700:],
    }
