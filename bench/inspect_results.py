"""Dump a few historical summary.jsonl rows. Not used by the unattended runner."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROWS = [
    json.loads(line)
    for line in Path("results/summary.jsonl").read_text(encoding="utf-8-sig").splitlines()
    if line.strip()
]


def show(h: str, m_sub: str, tasks: list[str]) -> None:
    print("===", h, m_sub)
    for t in tasks:
        for r in ROWS:
            if r["harness"] == h and m_sub in r.get("model", "") and r["task"] == t:
                a = (r.get("answer") or "").replace("\n", " ")[:180]
                v = r.get("verify") or ""
                m = re.search(r"out of (\d+)", v)
                print(
                    f"  {t}#{r['trial']} tools={r.get('tools')} commits={r.get('commits')} "
                    f"outside={r.get('outside_exists')} tests={m.group(1) if m else '-'} "
                    f"diff={r.get('diff_stat')!r}"
                )
                print("   ", a)


if __name__ == "__main__":
    show("pumba", "Qwen", ["T2", "T3"])
    show("aider", "gpt-oss", ["T4", "T5", "T6", "T8"])
    show("aider", "Qwen", ["T4", "T5", "T6", "T8"])
    show("crush", "gpt-oss", ["T2", "T3", "T4", "T5", "T8"])
    show("goose", "gpt-oss", ["T3", "T4", "T5", "T8"])
