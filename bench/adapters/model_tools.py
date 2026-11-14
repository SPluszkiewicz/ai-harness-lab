"""Baseline B: model + native tool_calls only. No prose fallback, no MCP, no product.

Writes stay inside the project. Shell is executed in the project cwd with a
machine-level deny list (format/shutdown). git commit is allowed so T8/T15
measure whether the *model* obeys written rules without a harness permission
layer.
"""

from __future__ import annotations

import json
import re
import time
from pathlib import Path

from adapters.llm import chat
from common import RunContext, beat, rules_text, run_shell

ID = "model_tools"
KIND = "model"
MAX_TURNS = 16
TOOL_CAP = 4000

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a text file relative to the project root.",
            "parameters": {
                "type": "object",
                "properties": {"path": {"type": "string"}},
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Overwrite a text file relative to the project root.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "content": {"type": "string"},
                },
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "grep",
            "description": "Search project files for a regex.",
            "parameters": {
                "type": "object",
                "properties": {"pattern": {"type": "string"}},
                "required": ["pattern"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "bash",
            "description": "Run a shell command in the project directory. Build/test only via docker exec bench-tools.",
            "parameters": {
                "type": "object",
                "properties": {"command": {"type": "string"}},
                "required": ["command"],
            },
        },
    },
]

HARD_DENY = re.compile(
    r"(format\s+[cC]:|shutdown|rm\s+-rf\s+/|del\s+/s\s+[cC]:|bcdedit|diskpart)",
    re.I,
)


def available() -> tuple[bool, str]:
    return True, "built-in"


def _safe(project: Path, rel: str) -> Path:
    path = (project / rel).resolve()
    root = project.resolve()
    if root not in path.parents and path != root:
        raise ValueError(f"path escapes project: {rel}")
    return path


def _cap(text: str) -> str:
    if len(text) <= TOOL_CAP:
        return text
    return text[: TOOL_CAP // 2] + "\n…[truncated]…\n" + text[-TOOL_CAP // 2 :]


def _exec(project: Path, name: str, args: dict) -> str:
    try:
        if name == "read_file":
            path = _safe(project, str(args.get("path", "")))
            return path.read_text(encoding="utf-8", errors="replace")
        if name == "write_file":
            path = _safe(project, str(args.get("path", "")))
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(str(args.get("content", "")), encoding="utf-8")
            return f"wrote {path.relative_to(project)}"
        if name == "grep":
            pattern = str(args.get("pattern", ""))
            rx = re.compile(pattern)
            hits: list[str] = []
            for file in list(project.rglob("*")):
                if not file.is_file() or "build" in file.parts or ".git" in file.parts:
                    continue
                if file.suffix.lower() not in {".cpp", ".hpp", ".h", ".txt", ".md", ".json", ".inc", ".cmake", ""}:
                    if file.name not in {"CMakeLists.txt", "CMakePresets.json", "AGENTS.md"}:
                        continue
                try:
                    for i, line in enumerate(file.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                        if rx.search(line):
                            hits.append(f"{file.relative_to(project).as_posix()}:{i}:{line}")
                            if len(hits) >= 80:
                                return "\n".join(hits)
                except OSError:
                    continue
            return "\n".join(hits) or "(no matches)"
        if name == "bash":
            command = str(args.get("command", ""))
            if HARD_DENY.search(command):
                return "blocked: machine-level deny"
            text, code, timed = run_shell(command, project, timeout=90)
            if timed:
                return "timeout: command killed"
            return _cap(text or f"exit {code}")
        return f"unknown tool {name}"
    except Exception as exc:  # noqa: BLE001
        return f"tool error: {exc}"


def run(ctx: RunContext) -> dict:
    rules = rules_text()
    messages: list[dict] = [
        {
            "role": "system",
            "content": rules
            + "\nYou have tools. Use them. Do not invent file contents. Native tool_calls only.",
        },
        {"role": "user", "content": ctx.task["prompt"]},
    ]
    tools_used: list[str] = []
    answer = ""
    timed_out = False
    started = time.time()
    try:
        for _ in range(MAX_TURNS):
            beat()
            left = ctx.timeout - (time.time() - started)
            if left <= 1:
                timed_out = True
                break
            data = chat(ctx.model, messages, tools=TOOLS, timeout=max(5, int(left)))
            msg = (data.get("choices") or [{}])[0].get("message") or {}
            calls = msg.get("tool_calls") or []
            content = msg.get("content") or ""
            if content:
                answer = content
            if not calls:
                break
            messages.append(msg)
            for call in calls:
                fn = call.get("function") or {}
                name = fn.get("name") or "?"
                raw_args = fn.get("arguments") or "{}"
                tools_used.append(name)
                try:
                    args = json.loads(raw_args) if isinstance(raw_args, str) else (raw_args or {})
                except json.JSONDecodeError:
                    args = {}
                    result = f"invalid JSON arguments: {raw_args[:200]}"
                else:
                    result = _exec(ctx.project, name, args)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": call.get("id") or name,
                        "content": _cap(result),
                    }
                )
    except Exception as exc:  # noqa: BLE001
        ctx.log_path.write_text(json.dumps(messages, ensure_ascii=False, indent=2)[-8000:], encoding="utf-8")
        return {
            "answer": answer,
            "tools": tools_used,
            "tool_calls": len(tools_used),
            "error": str(exc),
            "timed_out": timed_out,
            "exit_code": 1,
            "raw_tail": answer[-700:],
        }
    ctx.log_path.write_text(json.dumps(messages, ensure_ascii=False, indent=2)[-12000:], encoding="utf-8")
    return {
        "answer": answer,
        "tools": tools_used,
        "tool_calls": len(tools_used),
        "error": None,
        "timed_out": timed_out,
        "exit_code": 1 if timed_out else 0,
        "raw_tail": answer[-700:],
    }
