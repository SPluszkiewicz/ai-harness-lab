from __future__ import annotations

from importlib import import_module

ADAPTERS = [
    "adapters.model_chat",
    "adapters.model_tools",
    "adapters.opencode",
    "adapters.goose",
    "adapters.aider",
    "adapters.qwen",
    "adapters.pi",
    "adapters.kilo",
    "adapters.mini_swe",
    "adapters.cline",
    "adapters.crush",
    "adapters.codex",
    "adapters.zoo",
    "adapters.refact",
    "adapters.openhands",
]


def load_all() -> dict:
    out = {}
    for name in ADAPTERS:
        try:
            mod = import_module(name)
        except Exception as exc:  # noqa: BLE001
            print(f"SKIP import {name}: {exc}", flush=True)
            continue
        out[mod.ID] = mod
    return out
