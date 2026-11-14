from __future__ import annotations

import json
import os

from adapters.cliutil import finish, missing
from common import BENCH, RunContext, base_url, rules_text, run_cmd

ID = "crush"
KIND = "harness"


def available() -> tuple[bool, str]:
    return missing("CRUSH_BIN", "crush", "crush.exe not found (set CRUSH_BIN or place under bench/crush/)")


def _config(model: str):
    host = base_url()
    if host.endswith("/v1"):
        host = host[:-3]
    cfg = {
        "providers": {
            "llamacpp": {
                "id": "llamacpp",
                "name": "llama.cpp",
                "type": "llamacpp",
                "base_url": host,
                "api_key": "none",
            }
        },
        "models": {"large": {"model": model, "provider": "llamacpp"}},
        "options": {"disable_provider_auto_update": True},
    }
    path = BENCH / "generated" / "crush.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
    return path


def run(ctx: RunContext) -> dict:
    ok, binary = available()
    if not ok:
        return {"error": binary, "answer": "", "tools": [], "tool_calls": 0, "timed_out": False, "exit_code": 1}
    cfg = _config(ctx.model)
    prompt = rules_text() + "\n\n" + ctx.task["prompt"]
    env = dict(os.environ)
    env["CRUSH_CONFIG"] = str(cfg)
    env["CRUSH_DISABLE_METRICS"] = "1"
    env["DO_NOT_TRACK"] = "1"
    env["CRUSH_DISABLE_PROVIDER_AUTO_UPDATE"] = "1"
    cmd = [binary, "run", "-y", "-q", "-m", f"llamacpp/{ctx.model}", prompt]
    out, code, timed_out, _ = run_cmd(cmd, ctx.project, env, ctx.timeout, ctx.log_path)
    tools = [w for w in ("bash", "edit", "write", "grep", "view") if w in out.lower()]
    return finish(out, code, timed_out, tools, [out[-700:]] if out.strip() else [])
