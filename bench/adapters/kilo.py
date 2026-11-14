from __future__ import annotations

import json
import os

from adapters import opencode as oc
from common import BENCH, RunContext, find_bin, run_cmd

ID = "kilo"
KIND = "harness"


def available() -> tuple[bool, str]:
    path = find_bin("KILO_BIN", BENCH / "kilo")
    if path:
        return True, str(path)
    return False, "kilo CLI not found (set KILO_BIN)"


def run(ctx: RunContext) -> dict:
    ok, binary = available()
    if not ok:
        return {"error": binary, "answer": "", "tools": [], "tool_calls": 0, "timed_out": False, "exit_code": 1}
    edit = ctx.task.get("kind") in {"edit", "policy"}
    cfg = oc._config(ctx.model, edit=edit)
    prompt = ctx.task["prompt"]
    env = dict(os.environ)
    env["KILO_CONFIG"] = str(cfg)
    env["KILO_TELEMETRY_LEVEL"] = "off"
    env["KILO_DISABLE_LSP_DOWNLOAD"] = "1"
    env["OPENCODE_CONFIG"] = str(cfg)
    cmd = [
        binary,
        "run",
        "--auto",
        "--format",
        "json",
        "--dir",
        str(ctx.project),
        "-m",
        f"llama/{ctx.model}",
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
        part = event.get("part") or {}
        if event.get("type") == "tool_use":
            tools.append(part.get("tool") or "?")
        elif event.get("type") == "text" and part.get("text"):
            texts.append(part["text"])
    return {
        "answer": texts[-1] if texts else out[-700:],
        "tools": tools,
        "tool_calls": len(tools),
        "timed_out": timed_out,
        "exit_code": code,
        "error": None,
        "raw_tail": out[-700:],
    }
