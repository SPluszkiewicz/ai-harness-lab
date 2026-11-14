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
]


def load_all() -> dict:
    out = {}
    for name in ADAPTERS:
        mod = import_module(name)
        out[mod.ID] = mod
    return out
