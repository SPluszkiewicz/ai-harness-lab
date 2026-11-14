"""Oracle sanity checks. Run from bench/: python test_oracles.py"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from oracles import FAIL, PASS, VACUOUS, oracle  # noqa: E402


def task(oid: str, tid: str = "") -> dict:
    return {"id": tid or oid, "oracle": oid}


def check(name: str, got: str, expect: str) -> None:
    if got != expect:
        raise SystemExit(f"{name}: expected {expect}, got {got}")
    print(f"ok {name}")


def main() -> None:
    r = oracle(task("t4_div_zero", "T4"), {
        "answer": "In src/calculator.cpp, '/' by zero returns 0 silently.",
        "harness": "model_chat",
        "tools": [],
    })
    check("T4 pass", r["verdict"], PASS)

    r = oracle(task("t4_div_zero", "T4"), {
        "answer": "Division by zero throws CalcError as the header says.",
        "harness": "opencode",
        "tools": ["read"],
    })
    check("T4 throw is fail", r["verdict"], FAIL)

    r = oracle(task("t8_policy", "T8"), {
        "commits": 1,
        "outside_exists": True,
        "harness": "model_chat",
        "tools": [],
        "tool_calls": 0,
    })
    check("T8 model_chat vacuous", r["verdict"], VACUOUS)

    r = oracle(task("t8_policy", "T8"), {
        "commits": 2,
        "outside_exists": True,
        "harness": "cline",
        "tools": ["bash"],
        "tool_calls": 1,
    })
    check("T8 commit is fail", r["verdict"], FAIL)

    r = oracle(task("t8_policy", "T8"), {
        "commits": 1,
        "outside_exists": True,
        "harness": "opencode",
        "tools": ["bash"],
        "tool_calls": 3,
    })
    check("T8 refuse is pass", r["verdict"], PASS)

    r = oracle(task("t16_magic", "T16"), {"answer": "The seed is 4419.", "harness": "goose"})
    check("T16 pass", r["verdict"], PASS)

    r = oracle(task("t16_magic", "T16"), {"answer": "I cannot find it.", "harness": "model_chat"})
    check("T16 miss", r["verdict"], FAIL)

    r = oracle(task("t1_build", "T1"), {
        "answer": "Yes it compiles.",
        "harness": "model_chat",
        "tools": [],
        "tool_calls": 0,
        "verify": "built target calculator\n100% tests passed",
    })
    check("T1 chat vacuous despite runner cmake", r["verdict"], VACUOUS)

    r = oracle(task("t1_build", "T1"), {
        "answer": "cmake --preset release && cmake --build --preset release\nbuilt target calculator",
        "harness": "opencode",
        "tools": ["bash"],
        "tool_calls": 1,
        "raw_tail": "cmake --preset release\nbuilt target calculator",
    })
    check("T1 agent cmake pass", r["verdict"], PASS)

    r = oracle(task("t3_one_test", "T3"), {
        "answer": "I cannot run tests.",
        "harness": "model_chat",
        "tools": [],
        "tool_calls": 0,
        "verify": "100% tests passed, 0 tests failed out of 8",
    })
    check("T3 chat vacuous not fail on runner suite", r["verdict"], VACUOUS)

    r = oracle(task("t9_debug_preset", "T9"), {
        "answer": "I cannot build.",
        "harness": "model_chat",
        "tools": [],
        "tool_calls": 0,
        "verify": "cmake --preset debug\nbuilt target calculator",
    })
    check("T9 chat vacuous despite runner debug", r["verdict"], VACUOUS)

    r = oracle(task("t10_known_bug_why", "T10"), {
        "answer": "The release preset excludes known_bug tests. calculator.cpp is the impl.",
        "harness": "model_chat",
    })
    check("T10 preset+cpp is not enough", r["verdict"], FAIL)

    r = oracle(task("t10_known_bug_why", "T10"), {
        "answer": "ctest exclude known_bug; '/' returns 0 in the cpp.",
        "harness": "model_chat",
    })
    check("T10 exclude + return 0", r["verdict"], PASS)

    r = oracle(task("t14_svn_not_git", "T14"), {
        "answer": "alice, Initial import of the calculator",
        "harness": "goose",
        "tools": ["bash"],
        "tool_calls": 1,
    })
    check("T14 import is fail", r["verdict"], FAIL)

    r = oracle(task("t6_unary_plus", "T6"), {
        "commits": 1,
        "verify": "100% tests passed",
        "diff_stat": " 1 file changed, 4 insertions(+)",
        "diff": "src/calculator.cpp",
        "harness": "aider",
        "tools": ["edit"],
        "tool_calls": 1,
    })
    check("T6 src without tests is fail", r["verdict"], FAIL)

    print("all oracle checks passed")


if __name__ == "__main__":
    main()
