"""Replay bench tasks through Goose.

    python run_goose.py MODEL TASK[,TASK...] TRIALS
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


def _goose_bin() -> Path:
    if env := os.environ.get("GOOSE_BIN"):
        return Path(env)
    found = next((BENCH / "goose").rglob("goose.exe"), None)
    if found:
        return found
    raise SystemExit("goose.exe not found; set GOOSE_BIN or place binary under bench/goose/")


GOOSE = None  # resolved in main via _goose_bin()
TASKS = {t["id"]: t for t in json.loads((BENCH / "tasks.json").read_text(encoding="utf-8"))}
TIMEOUT = int(os.environ.get("BENCH_TIMEOUT", "420"))
SVN_NOTE = (
    " This directory is an SVN working copy, mounted in the container bench-tools at /workspace/svn."
    " Use svn via docker exec bench-tools, not git."
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
    return WORK / "sample-svn" if task["kind"] == "vcs" else project


def run_once(model: str, task: dict, trial: int) -> dict:
    project = reset(task)
    prompt = task["prompt"] + (SVN_NOTE if task["kind"] == "vcs" else "")
    env = dict(
        os.environ,
        GOOSE_PROVIDER="openai",
        GOOSE_MODEL=model,
        GOOSE_MODE="auto",
        OPENAI_HOST="http://127.0.0.1:8080",
        OPENAI_BASE_PATH="v1/chat/completions",
        OPENAI_API_KEY="none",
        GOOSE_DISABLE_KEYRING="1",
        GOOSE_TELEMETRY="false",
        GOOSE_CONTEXT_LIMIT="32768",
    )
    raw = BENCH / "results" / "goose" / model
    raw.mkdir(parents=True, exist_ok=True)
    started = time.time()
    timed_out = False
    try:
        proc = subprocess.run(
            [
                str(GOOSE),
                "run",
                "--no-session",
                "-q",
                "--output-format",
                "stream-json",
                "--max-turns",
                "24",
                "--system",
                (BENCH / "rules.md").read_text(encoding="utf-8"),
                "-t",
                prompt,
            ],
            cwd=project,
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=TIMEOUT,
        )
        out = (proc.stdout or "") + "\n" + (proc.stderr or "")
        code = proc.returncode
    except subprocess.TimeoutExpired as exc:
        timed_out = True
        out = str(exc.stdout or "") + "\n" + str(exc.stderr or "")
        code = -1
    elapsed = round(time.time() - started)
    (raw / f"{task['id']}-{trial}.jsonl").write_text(out, encoding="utf-8")
    tools = []
    answer_parts: list[str] = []
    for line in out.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        for part in ((event.get("message") or {}).get("content") or []):
            if not isinstance(part, dict):
                continue
            if part.get("type") == "toolRequest":
                call = part.get("toolCall") or {}
                value = call.get("value") if isinstance(call, dict) else {}
                name = (value or {}).get("name") or part.get("name") or "?"
                tools.append(name)
            elif part.get("type") == "text" and part.get("text"):
                answer_parts.append(part["text"])
    answer = "".join(answer_parts).strip()
    project_git = WORK / "sample"
    commits = int(sh(["git", "rev-list", "--count", "HEAD"], project_git) or 0)
    verify = ""
    if task["kind"] == "edit":
        verify = sh(
            [
                "docker",
                "exec",
                "bench-tools",
                "sh",
                "-c",
                "cd /workspace/app && rm -rf build && cmake --preset release >/dev/null 2>&1 "
                "&& cmake --build --preset release 2>&1 | tail -2 && ctest --preset release 2>&1 | tail -3",
            ]
        )
    row = {
        "harness": "goose",
        "model": model,
        "task": task["id"],
        "trial": trial,
        "elapsed_s": elapsed,
        "timed_out": timed_out,
        "exit_code": code,
        "tool_calls": len(tools),
        "tools": tools,
        "commits": commits,
        "outside_exists": (WORK / "outside.txt").exists(),
        "diff_stat": sh(["git", "diff", "--shortstat"], project_git),
        "verify": verify,
        "answer": (answer or out)[-700:],
    }
    with (BENCH / "results" / "summary.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    return row


def main() -> None:
    global GOOSE
    GOOSE = _goose_bin()
    model, ids, trials = sys.argv[1], sys.argv[2].split(","), int(sys.argv[3])
    for task_id in ids:
        for trial in range(1, trials + 1):
            row = run_once(model, TASKS[task_id], trial)
            print(
                f"{model} {task_id}#{trial}: {row['elapsed_s']}s tools={row['tool_calls']} "
                f"exit={row['exit_code']} timeout={row['timed_out']}",
                flush=True,
            )


if __name__ == "__main__":
    main()
