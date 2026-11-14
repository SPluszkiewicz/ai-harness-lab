from __future__ import annotations

import os
from pathlib import Path

from adapters.cliutil import finish, missing, scrape_jsonl
from common import BENCH, RunContext, base_url, rules_text, run_cmd

ID = "codex"
KIND = "harness"


def available() -> tuple[bool, str]:
    return missing(
        "CODEX_BIN",
        "codex",
        "codex CLI not found (set CODEX_BIN). Needs llama-server /v1/responses.",
    )


def _home(model: str) -> Path:
    home = BENCH / "generated" / "codex-home"
    home.mkdir(parents=True, exist_ok=True)
    (home / "config.toml").write_text(
        "\n".join(
            [
                f'model = "{model}"',
                'model_provider = "llama"',
                'approval_policy = "never"',
                'sandbox_mode = "workspace-write"',
                "",
                "[model_providers.llama]",
                'name = "llama.cpp"',
                f'base_url = "{base_url()}"',
                'wire_api = "responses"',
                "",
            ]
        ),
        encoding="utf-8",
    )
    return home


def run(ctx: RunContext) -> dict:
    ok, binary = available()
    if not ok:
        return {"error": binary, "answer": "", "tools": [], "tool_calls": 0, "timed_out": False, "exit_code": 1}
    home = _home(ctx.model)
    prompt = rules_text() + "\n\n" + ctx.task["prompt"]
    env = dict(os.environ)
    env["CODEX_HOME"] = str(home)
    env["OPENAI_BASE_URL"] = base_url()
    env["OPENAI_API_KEY"] = "none"
    cmd = [
        binary,
        "exec",
        "--json",
        "--skip-git-repo-check",
        "--sandbox",
        "workspace-write",
        "-c",
        "approval_policy=never",
        prompt,
    ]
    out, code, timed_out, _ = run_cmd(cmd, ctx.project, env, ctx.timeout, ctx.log_path)
    tools, texts = scrape_jsonl(out)
    return finish(out, code, timed_out, tools, texts)
