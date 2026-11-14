"""Shared CLI adapter helpers."""

from __future__ import annotations

import json

from common import BENCH, find_bin


def missing(env_name: str, folder: str, hint: str) -> tuple[bool, str]:
    path = find_bin(env_name, BENCH / folder)
    if path:
        return True, str(path)
    return False, hint


def scrape_jsonl(out: str) -> tuple[list[str], list[str]]:
    tools: list[str] = []
    texts: list[str] = []
    for line in out.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        blob = json.dumps(event).lower()
        kind = str(event.get("type") or event.get("event") or event.get("kind") or "")
        if "tool" in kind.lower() or event.get("tool") or "tool" in blob:
            tools.append(str(event.get("tool") or event.get("name") or event.get("item_type") or "tool"))
        text = event.get("text") or event.get("content") or event.get("message")
        if isinstance(text, str) and text.strip():
            texts.append(text)
    return tools, texts


def finish(out: str, code: int, timed_out: bool, tools: list[str], texts: list[str]) -> dict:
    return {
        "answer": (texts[-1] if texts else out[-700:]),
        "tools": tools,
        "tool_calls": len(tools),
        "timed_out": timed_out,
        "exit_code": code,
        "error": None,
        "raw_tail": out[-700:],
    }
