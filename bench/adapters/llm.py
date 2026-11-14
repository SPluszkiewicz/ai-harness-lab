"""Minimal OpenAI-compatible client for llama-server."""

from __future__ import annotations

import json
import urllib.error
import urllib.request

from common import BENCH, base_url, env, timeout_s


def chat(
    model: str,
    messages: list[dict],
    tools: list[dict] | None = None,
    max_tokens: int = 2048,
    timeout: int | None = None,
) -> dict:
    body: dict = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": 0.2,
        "stream": False,
    }
    if tools:
        body["tools"] = tools
        body["tool_choice"] = "auto"
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        base_url() + "/chat/completions",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout or timeout_s()) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as exc:
        err = exc.read().decode("utf-8", "replace")
        raise RuntimeError(f"LLM HTTP {exc.code}: {err[:400]}") from exc


def list_served_models() -> list[str]:
    url = base_url() + "/models"
    with urllib.request.urlopen(url, timeout=10) as resp:
        data = json.load(resp)
    return [m.get("id") for m in data.get("data") or [] if m.get("id")]


def _skip(model_id: str, needles: list[str]) -> bool:
    low = model_id.lower()
    return any(n.lower() in low for n in needles)


def resolve_name(wanted: str, served: list[str]) -> str | None:
    if wanted in served:
        return wanted
    hits = [s for s in served if wanted.lower() in s.lower()]
    if len(hits) == 1:
        return hits[0]
    if not hits:
        return None
    # Several matches: shortest id (usually the alias, not a shard name).
    hits.sort(key=len)
    return hits[0]


def select_models(explicit: list[str] | None = None) -> tuple[list[str], list[str]]:
    """Return (chosen ids, notes). Notes are human warnings, not fatals."""
    matrix = json.loads(BENCH.joinpath("matrix.json").read_text(encoding="utf-8"))
    skip = list(matrix.get("models_skip_substrings") or [])
    prefer = list(matrix.get("models_prefer") or [])
    notes: list[str] = []
    served = list_served_models()
    chat = [s for s in served if not _skip(s, skip)]
    if not chat:
        raise RuntimeError(f"no chat models on {base_url()}/models (got {served})")

    wanted = explicit if explicit else None
    if wanted is None:
        raw = env("BENCH_MODELS", "")
        wanted = [p.strip() for p in raw.split(",") if p.strip()] or None

    if wanted:
        chosen: list[str] = []
        for w in wanted:
            hit = resolve_name(w, chat) or resolve_name(w, served)
            if hit is None:
                raise RuntimeError(
                    f"model {w!r} not on the server. Served: {served}"
                )
            chosen.append(hit)
        notes.append("BENCH_MODELS / --models (resolved against /v1/models)")
        return chosen, notes

    chosen = []
    for needle in prefer:
        for s in chat:
            if needle.lower() in s.lower() and s not in chosen:
                chosen.append(s)
    if chosen:
        notes.append(
            "auto: served ids matching matrix.json models_prefer "
            f"{prefer} (14B is not in that list)"
        )
        return chosen, notes

    notes.append(
        "auto: no prefer match; using every non-embedding model on the server"
    )
    weak = [s for s in chat if "14b" in s.lower() or "qwen2.5-coder" in s.lower()]
    if weak and weak == chat:
        notes.append(
            "WARNING: only the 14B-class model is loaded. "
            "On EVO-5 load Qwen3.8-27B, Mistral-Small-4, or gpt-oss instead."
        )
    return chat, notes


def probe_native_tools(model: str) -> dict:
    """One dummy tool_call. Native = the server returned tool_calls, not prose."""
    ping = [
        {
            "type": "function",
            "function": {
                "name": "ping",
                "description": "Health check. Always call this tool; do not answer in plain text.",
                "parameters": {
                    "type": "object",
                    "properties": {"x": {"type": "string", "description": "any token"}},
                    "required": ["x"],
                },
            },
        }
    ]
    try:
        data = chat(
            model,
            [{"role": "user", "content": "Call the ping tool with x=hi. Do not reply with words."}],
            tools=ping,
            max_tokens=256,
        )
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "native_tool_calls": False, "error": str(exc)[:300]}
    msg = (data.get("choices") or [{}])[0].get("message") or {}
    calls = msg.get("tool_calls") or []
    content = msg.get("content") or ""
    return {
        "ok": True,
        "native_tool_calls": bool(calls),
        "n_calls": len(calls),
        "content_preview": content[:160],
        "finish_reason": (data.get("choices") or [{}])[0].get("finish_reason"),
    }
