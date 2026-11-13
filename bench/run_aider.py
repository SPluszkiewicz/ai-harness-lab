"""Replay bench tasks through Aider (edit formats, no tool-calling).

    python run_aider.py MODEL TASK[,TASK...] TRIALS
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
SITE = BENCH / "aider" / "site"
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
    prompt = task["prompt"] + (SVN_NOTE if task["kind"] == "vcs" else "")
    env = dict(
        os.environ,
        PYTHONPATH=str(SITE),
        OPENAI_API_BASE="http://127.0.0.1:8080/v1",
        OPENAI_API_KEY="none",
        AIDER_ANALYTICS="false",
    )
    raw = BENCH / "results" / "aider" / model
    raw.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable,
        "-m",
        "aider.main",
        "--model",
        f"openai/{model}",
        "--openai-api-base",
        "http://127.0.0.1:8080/v1",
        "--openai-api-key",
        "none",
        "--no-auto-commits",
        "--no-dirty-commits",
        "--yes-always",
        "--no-pretty",
        "--no-stream",
        "--no-gitignore",
        "--no-show-model-warnings",
        "--map-tokens",
        "1024",
        "--read",
        str(BENCH / "rules.md"),
        "--lint-cmd",
        "docker exec bench-tools sh -c \"cd /workspace/app && cmake --build --preset release -- -n 2>/dev/null || true\"",
        "--test-cmd",
        "docker exec bench-tools sh -c \"cd /workspace/app && cmake --preset release >/dev/null && cmake --build --preset release && ctest --preset release\"",
        "--message",
        prompt,
    ]
    if task["kind"] in ("edit", "read"):
        cmd.extend(
            [
                "--file",
                "src/calculator.cpp",
                "--file",
                "src/calculator.hpp",
                "--file",
                "tests/calculator_test.cpp",
                "--file",
                "CMakePresets.json",
            ]
        )
    started = time.time()
    timed_out = False
    try:
        proc = subprocess.run(
            cmd,
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
        out = ((exc.stdout or "") if isinstance(exc.stdout, str) else "") + "\n" + (
            (exc.stderr or "") if isinstance(exc.stderr, str) else ""
        )
        code = -1
    elapsed = round(time.time() - started)
    (raw / f"{task['id']}-{trial}.txt").write_text(out, encoding="utf-8")
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
    answer = ""
    for line in reversed(out.splitlines()):
        if line.strip() and not line.startswith(("INFO", "WARNING", "Aider v", "Model:", "Repo-map:")):
            answer = line.strip()
            break
    # Prefer the last substantial block
    blocks = [b.strip() for b in out.split("\n\n") if len(b.strip()) > 40]
    if blocks:
        answer = blocks[-1][:700]
    row = {
        "harness": "aider",
        "model": model,
        "task": task["id"],
        "trial": trial,
        "elapsed_s": elapsed,
        "timed_out": timed_out,
        "exit_code": code,
        "commits": commits,
        "outside_exists": (WORK / "outside.txt").exists(),
        "diff_stat": sh(["git", "diff", "--shortstat"], project_git),
        "verify": verify,
        "answer": answer,
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
                f"{model} {task_id}#{trial}: {row['elapsed_s']}s exit={row['exit_code']} "
                f"commits={row['commits']} diff={row['diff_stat']!r} timeout={row['timed_out']}",
                flush=True,
            )


if __name__ == "__main__":
    main()
