"""Baseline A: the model alone. Files inlined. No tools, no side effects."""

from __future__ import annotations

from pathlib import Path

from adapters.llm import chat
from common import RunContext, rules_text

ID = "model_chat"
KIND = "model"


def available() -> tuple[bool, str]:
    return True, "built-in"


def _inline(project: Path, task: dict) -> str:
    names = task.get("chat_files") or []
    chunks: list[str] = []
    for name in names:
        path = project / name
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if len(text) > 12000:
            text = text[:12000] + "\n…[truncated]"
        chunks.append(f"----- {name} -----\n{text}")
    if not chunks:
        return "(no files inlined for this task — you cannot read the disk)"
    return "\n\n".join(chunks)


def run(ctx: RunContext) -> dict:
    rules = rules_text()
    files = _inline(ctx.project, ctx.task)
    user = (
        "You are answering with no tools and no ability to run commands or edit files.\n"
        "If the question requires running a compiler, tests, git, svn, or changing files, say so.\n\n"
        f"{ctx.task['prompt']}\n\n"
        f"Repository excerpts:\n{files}"
    )
    try:
        data = chat(
            ctx.model,
            [
                {"role": "system", "content": rules},
                {"role": "user", "content": user},
            ],
            timeout=ctx.timeout,
        )
    except Exception as exc:  # noqa: BLE001
        return {"answer": "", "tools": [], "tool_calls": 0, "error": str(exc), "timed_out": False, "exit_code": 1}
    msg = (data.get("choices") or [{}])[0].get("message") or {}
    answer = msg.get("content") or ""
    raw = ctx.log_path
    raw.write_text(answer, encoding="utf-8")
    return {
        "answer": answer,
        "tools": [],
        "tool_calls": 0,
        "error": None,
        "timed_out": False,
        "exit_code": 0,
        "raw_tail": answer[-700:],
    }
