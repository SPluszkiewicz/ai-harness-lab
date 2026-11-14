"""Resume rules: only a recorded verdict is done; blips retry before that write."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from run_all import FINAL, transient_failure  # noqa: E402


def main() -> None:
    assert "PASS" in FINAL and "ERR" in FINAL and "TIMEOUT" in FINAL
    assert transient_failure({
        "verdict": "ERR",
        "why": "git reset failed: timeout",
        "tool_calls": 0,
    })
    assert transient_failure({
        "verdict": "ERR",
        "why": "LLM HTTP 503: unavailable",
        "error": "connection refused",
        "tool_calls": 0,
    })
    assert not transient_failure({
        "verdict": "TIMEOUT",
        "why": "timeout",
        "tool_calls": 4,
    })
    assert not transient_failure({
        "verdict": "FAIL",
        "why": "no evidence of cmake",
        "tool_calls": 2,
    })
    assert not transient_failure({
        "verdict": "ERR",
        "why": "boom",
        "tool_calls": 3,
    })
    print("ok resume rules")


if __name__ == "__main__":
    main()
