from __future__ import annotations

import json
import os

from common import BENCH, RunContext, base_url, ctx_limit, docker_bin, find_bin, materialize_rules, run_cmd

ID = "opencode"
KIND = "harness"


def available() -> tuple[bool, str]:
    path = find_bin(
        "OPENCODE_BIN",
        BENCH / "opencode" / "node_modules" / ".bin" / "opencode.cmd",
        BENCH / "opencode" / "node_modules" / ".bin" / "opencode",
    )
    if path:
        return True, str(path)
    return False, "opencode CLI not found (npm install in bench/opencode or set OPENCODE_BIN)"


def _config(model: str, edit: bool) -> Path:
    models = {
        model: {
            "name": model,
            "tool_call": True,
            "limit": {"context": ctx_limit(), "output": 4096},
        }
    }
    cfg = {
        "$schema": "https://opencode.ai/config.json",
        "autoupdate": False,
        "share": "disabled",
        "instructions": [str(materialize_rules())],
        "provider": {
            "llama": {
                "npm": "@ai-sdk/openai-compatible",
                "name": "llama.cpp (local)",
                "options": {"baseURL": base_url(), "apiKey": "none"},
                "models": models,
            }
        },
        "permission": {
            "edit": "allow" if edit else "deny",
            "bash": {
                "*": "deny",
                f"{docker_bin()} exec bench-tools *": "allow",
                "git log*": "allow",
                "git diff*": "allow",
                "git status*": "allow",
                "git show*": "allow",
                "rg *": "allow",
                "grep *": "allow",
            },
        },
    }
    path = BENCH / "generated" / "opencode.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
    return path


def run(ctx: RunContext) -> dict:
    ok, bin_or_msg = available()
    if not ok:
        return {"error": bin_or_msg, "answer": "", "tools": [], "tool_calls": 0, "timed_out": False, "exit_code": 1}
    edit = ctx.task.get("kind") in {"edit", "policy"}
    cfg = _config(ctx.model, edit=edit)
    prompt = ctx.task["prompt"]
    env = dict(os.environ)
    env["OPENCODE_CONFIG"] = str(cfg)
    env["OPENCODE_DISABLE_AUTOUPDATE"] = "1"
    env["OPENCODE_DISABLE_MODELS_FETCH"] = "1"
    cmd = [
        bin_or_msg,
        "run",
        "--format",
        "json",
        "--dir",
        str(ctx.project),
        "-m",
        f"llama/{ctx.model}",
        prompt,
    ]
    out, code, timed_out, _elapsed = run_cmd(cmd, ctx.project, env, ctx.timeout, ctx.log_path)
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
    answer = texts[-1] if texts else out[-700:]
    return {
        "answer": answer,
        "tools": tools,
        "tool_calls": len(tools),
        "timed_out": timed_out,
        "exit_code": code,
        "error": None,
        "raw_tail": out[-700:],
    }
