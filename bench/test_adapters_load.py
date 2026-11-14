"""Smoke: every matrix harness has an adapter module."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from adapters import load_all  # noqa: E402


def main() -> None:
    matrix = json.loads(Path("matrix.json").read_text(encoding="utf-8"))
    adapters = load_all()
    missing = [h["id"] for h in matrix["harnesses"] if h["id"] not in adapters]
    extra_pumba = "pumba" in adapters
    if missing:
        raise SystemExit(f"matrix ids without adapter: {missing}")
    if extra_pumba:
        raise SystemExit("pumba must not have an adapter")
    print(f"ok {len(adapters)} adapters: {', '.join(adapters)}")


if __name__ == "__main__":
    main()
