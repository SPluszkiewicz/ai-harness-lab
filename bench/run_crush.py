"""Replay bench tasks through Crush.

    python run_crush.py MODEL TASK[,TASK...] TRIALS
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


def _crush_bin() -> Path:
    if env := os.environ.get("CRUSH_BIN"):
        return Path(env)
    found = next((BENCH / "crush").rglob("crush.exe"), None)
    if found:
        return found
    raise SystemExit("crush.exe not found; set CRUSH_BIN or place binary under bench/crush/")


CRUSH = None  # resolved in main via _crush_bin()
TASKS = {t["id"]: t for t in json.loads((BENCH / "tasks.json").read_text(encoding="utf-8"))}
TIMEOUT = int(os.environ.get("BENCH_TIMEOUT", "420"))
SVN_NOTE = (
    " This directory is an SVN working copy, mounted in the container bench-tools at /workspace/svn."
    " Use svn, not git. Run svn via: docker exec bench-tools sh -c 'cd /workspace/svn && …'."
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
    prompt = (BENCH / "rules.md").read_text(encoding="utf-8") + "\n\n" + task["prompt"]
    if task["kind"] == "vcs":
        prompt += SVN_NOTE
    env = dict(os.environ)
    # Crush looks for crush.json in cwd / XDG config. Point it via CRUSH_CONFIG if supported,
    # otherwise copy into the project for the run.
    cfg = (BENCH / "crush" / "crush.json").read_text(encoding="utf-8")
    cfg_obj = json.loads(cfg)
    cfg_obj["models"] = {"large": {"model": model, "provider": "llamacpp"}}
    if "providers" in cfg_obj and "llama" in cfg_obj["providers"]:
        cfg_obj["providers"]["llamacpp"] = cfg_obj["providers"].pop("llama")
        cfg_obj["providers"]["llamacpp"]["id"] = "llamacpp"
        cfg_obj["providers"]["llamacpp"]["type"] = "llamacpp"
        cfg_obj["providers"]["llamacpp"]["base_url"] = "http://127.0.0.1:8080"
    (project / ".crush.json").write_text(json.dumps(cfg_obj, indent=2), encoding="utf-8")
    (project / "crush.json").write_text(json.dumps(cfg_obj, indent=2), encoding="utf-8")
    raw = BENCH / "results" / "crush" / model
    raw.mkdir(parents=True, exist_ok=True)
    started = time.time()
    timed_out = False
    try:
        proc = subprocess.run(
            [str(CRUSH), "run", "-y", "-m", f"llamacpp/{model}", "--quiet", prompt],
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
    row = {
        "harness": "crush",
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
        "answer": out[-700:],
    }
    with (BENCH / "results" / "summary.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    return row


def main() -> None:
    global CRUSH
    CRUSH = _crush_bin()
    model, ids, trials = sys.argv[1], sys.argv[2].split(","), int(sys.argv[3])
    for task_id in ids:
        for trial in range(1, trials + 1):
            row = run_once(model, TASKS[task_id], trial)
            print(
                f"{model} {task_id}#{trial}: {row['elapsed_s']}s exit={row['exit_code']} "
                f"commits={row['commits']} timeout={row['timed_out']}",
                flush=True,
            )


if __name__ == "__main__":
    main()
