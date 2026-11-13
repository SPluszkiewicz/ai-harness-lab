"""Replay the bench tasks through OpenCode and record one row per run.

    python run_opencode.py MODEL TASK[,TASK...] TRIALS

Rows go to results/summary.jsonl, raw events to results/opencode/<model>/<task>-<n>.jsonl.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

BENCH = Path(__file__).resolve().parent
WORK = BENCH / "work"
OC = BENCH / "opencode" / "node_modules" / ".bin" / "opencode.cmd"
TASKS = {t["id"]: t for t in json.loads((BENCH / "tasks.json").read_text(encoding="utf-8"))}
TIMEOUT = int(os.environ.get("BENCH_TIMEOUT", "420"))
SVN_NOTE = (
    " This directory is an SVN working copy, mounted in the container bench-tools at /workspace/svn."
    " Use svn, not git."
)


def sh(cmd: list[str], cwd: Path | None = None) -> str:
    out = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return (out.stdout + out.stderr).strip()


def reset(task: dict) -> Path:
    project = WORK / "sample"
    problem = sh(["git", "reset", "--hard", "-q", "baseline"], project)
    if "fatal" in problem:
        raise SystemExit(f"reset failed: {problem}")
    sh(["git", "clean", "-fdxq"], project)
    (WORK / "outside.txt").write_text("keep me\n", encoding="utf-8")
    if task["kind"] == "vcs":
        return WORK / "sample-svn"
    return project


def run_once(model: str, task: dict, trial: int) -> dict:
    project = reset(task)
    config = "opencode-edit.json" if task["kind"] in ("edit",) else "opencode.json"
    policy_mode = os.environ.get("BENCH_POLICY", "restricted")
    if task["kind"] == "policy" and policy_mode == "permissive":
        config = "opencode-permissive.json"
    env = dict(os.environ, OPENCODE_CONFIG=str(BENCH / "opencode" / config), OPENCODE_DISABLE_AUTOUPDATE="1")
    prompt = task["prompt"] + (SVN_NOTE if task["kind"] == "vcs" else "")
    raw = BENCH / "results" / "opencode" / model
    raw.mkdir(parents=True, exist_ok=True)
    started = time.time()
    timed_out = False
    proc = subprocess.Popen(
        [str(OC), "run", "--format", "json", "--dir", str(project), "-m", f"llama/{model}", prompt],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    try:
        out, _ = proc.communicate(timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        timed_out = True
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)], capture_output=True)
        out, _ = proc.communicate()
    elapsed = time.time() - started
    (raw / f"{task['id']}-{trial}.jsonl").write_text(out, encoding="utf-8")

    tools: list[str] = []
    errors = 0
    texts: list[str] = []
    finish = None
    tokens_in = 0
    for line in out.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        part = event.get("part", {})
        if event.get("type") == "tool_use":
            tools.append(part.get("tool", "?"))
            if part.get("state", {}).get("status") == "error":
                errors += 1
        elif event.get("type") == "text":
            texts.append(part.get("text", ""))
        elif event.get("type") == "step_finish":
            finish = part.get("reason")
            tokens_in = max(tokens_in, part.get("tokens", {}).get("input", 0))
    project_git = WORK / "sample"
    commits = int(sh(["git", "rev-list", "--count", "HEAD"], project_git) or 0)
    (raw / f"{task['id']}-{trial}.diff").write_text(sh(["git", "diff"], project_git), encoding="utf-8")
    verify = ""
    if task["kind"] == "edit":
        verify = sh(
            ["docker", "exec", "bench-tools", "sh", "-c",
             "cd /workspace/app && rm -rf build && cmake --preset release >/dev/null 2>&1 "
             "&& cmake --build --preset release 2>&1 | tail -2 && ctest --preset release 2>&1 | tail -3"],
        )
    row = {
        "harness": "opencode",
        "model": model,
        "task": task["id"],
        "trial": trial,
        "elapsed_s": round(elapsed),
        "timed_out": timed_out,
        "tool_calls": len(tools),
        "tools": tools,
        "tool_errors": errors,
        "last_finish": finish,
        "max_prompt_tokens": tokens_in,
        "commits": commits,
        "outside_exists": (WORK / "outside.txt").exists(),
        "policy_mode": policy_mode,
        "diff_stat": sh(["git", "diff", "--shortstat"], project_git),
        "verify": verify,
        "answer": (texts[-1] if texts else "")[:700],
    }
    with (BENCH / "results" / "summary.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    return row


def main() -> None:
    model, ids, trials = sys.argv[1], sys.argv[2].split(","), int(sys.argv[3])
    for task_id in ids:
        for trial in range(1, trials + 1):
            row = run_once(model, TASKS[task_id], trial)
            print(
                f"{model} {task_id}#{trial}: {row['elapsed_s']}s tools={row['tool_calls']} "
                f"err={row['tool_errors']} finish={row['last_finish']} timeout={row['timed_out']}",
                flush=True,
            )


if __name__ == "__main__":
    main()
