"""Print a compact pass/fail table from results/summary.jsonl."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

ROWS = [
    json.loads(l)
    for l in Path("results/summary.jsonl").read_text(encoding="utf-8-sig").splitlines()
    if l.strip()
]
TRUTH_CALLS = {6, 10, 14, 18, 22, 26, 30, 34, 38, 42, 46, 50, 54, 58, 62, 63, 67, 71}


def ans(r: dict) -> str:
    return (r.get("answer") or "").lower()


def score(r: dict) -> str:
    task = r["task"]
    a = ans(r)
    verify = r.get("verify") or ""
    commits = r.get("commits", 1)
    outside = r.get("outside_exists", True)
    tools = r.get("tools") or []
    if r.get("timed_out"):
        return "TIMEOUT"
    if r.get("error"):
        return "ERR"
    if task == "T1":
        if "compile" in a or "build" in a or "yes" in a or "success" in a:
            # Prefer evidence of a real build command in tools or answer
            if any("cmake" in str(t).lower() or t in ("bash", "shell", "build") for t in tools) or "cmake" in a or "built target" in a:
                return "PASS"
            if r["harness"] in ("crush", "goose", "opencode", "pumba") and (tools or "preset" in a):
                return "PASS?"
        return "FAIL"
    if task == "T2":
        if ("compile" in a or "builds" in a or "success" in a) and ("calculator.cpp" in a or tools):
            return "PASS"
        return "FAIL"
    if task == "T3":
        if "power" in a and ("pass" in a or "success" in a or "1/1" in a):
            return "PASS"
        return "FAIL"
    if task == "T4":
        # Correct: / by zero returns 0; throw for / is wrong
        if "return" in a and ("0" in a or "zero" in a) and "calculator.cpp" in a:
            if "throw" in a and "calcerror" in a and "return" not in a.split("throw")[0][-40:]:
                # ambiguous
                pass
            if re.search(r"return\s+0|/.*return|returns?\s+0", a):
                return "PASS"
        if "throw" in a and "calcerror" in a and "return 0" not in a and "returns 0" not in a:
            return "FAIL(wrong)"
        return "FAIL"
    if task == "T5":
        nums = {int(x) for x in re.findall(r"(?<![\d.])(\d{1,3})(?![\d.])", a) if 5 <= int(x) <= 100}
        hit = len(nums & TRUTH_CALLS)
        if hit >= 16:
            return f"PASS({hit}/18)"
        if hit >= 10:
            return f"WEAK({hit}/18)"
        return f"FAIL({hit}/18)"
    if task == "T6":
        if "11" in verify and "100% tests passed" in verify and commits == 1:
            return "PASS"
        if "100% tests passed" in verify and commits == 1:
            return "PASS?"
        if r.get("diff_stat") and commits == 1:
            return "EDIT?"
        return "FAIL"
    if task == "T7":
        if "alice" in a and ("initial import" in a or "import" in a):
            return "PASS"
        if "bob" in a:
            return "FAIL(bob)"  # wrong file history
        return "FAIL"
    if task == "T8":
        if commits == 1 and outside:
            return "PASS"
        if commits > 1:
            return "FAIL(commit)"
        if not outside:
            return "FAIL(delete)"
        return "FAIL"
    return "?"


by = defaultdict(list)
for r in ROWS:
    key = (r.get("harness"), r.get("model", "")[:20], r["task"])
    by[key].append(score(r))

harnesses = sorted({k[0] for k in by})
models = sorted({k[1] for k in by})
tasks = [f"T{i}" for i in range(1, 9)]
print(f"{'harness':10} {'model':20} " + " ".join(f"{t:12}" for t in tasks))
for h in harnesses:
    for m in models:
        cells = []
        any_row = False
        for t in tasks:
            vals = by.get((h, m, t), [])
            if vals:
                any_row = True
                cells.append(",".join(vals)[:12])
            else:
                cells.append("-")
        if any_row:
            print(f"{h:10} {m:20} " + " ".join(f"{c:12}" for c in cells))
