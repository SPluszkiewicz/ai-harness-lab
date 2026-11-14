"""Shared Windows-safe helpers for the unattended harness bench."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path

BENCH = Path(__file__).resolve().parent
ROOT = BENCH.parent
WORK = BENCH / "work"
FIXTURE = ROOT / "fixtures" / "sample"
RESULTS = BENCH / "results"
TASKS_PATH = BENCH / "tasks.json"

CREATE_NEW_PROCESS_GROUP = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)

# Watchdog in run_all.py: a trial that stops heartbeating is killed and the process exits.
LAST_BEAT = time.time()
CURRENT_CHILD: int | None = None


def beat() -> None:
    global LAST_BEAT
    LAST_BEAT = time.time()


def idle_seconds() -> float:
    return time.time() - LAST_BEAT


def child_pid() -> int | None:
    return CURRENT_CHILD


def note_child(pid: int | None) -> None:
    global CURRENT_CHILD
    CURRENT_CHILD = pid


def env(name: str, default: str) -> str:
    value = os.environ.get(name)
    return default if value is None or value == "" else value


def base_url() -> str:
    return env("BENCH_BASE_URL", "http://127.0.0.1:8080/v1").rstrip("/")


def docker_bin() -> str:
    return env("BENCH_DOCKER", "docker")


def ctx_limit() -> int:
    return int(env("BENCH_CTX", "32768"))


def timeout_s() -> int:
    return int(env("BENCH_TIMEOUT", "420"))


def _bounded(
    cmd: list[str] | str,
    cwd: Path | None,
    env_map: dict[str, str],
    timeout: int,
    shell: bool = False,
) -> tuple[str, int, bool]:
    """Run a process. Always returns. Never waits past timeout+20s."""
    beat()
    flags = CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0
    proc = subprocess.Popen(
        cmd,
        cwd=str(cwd) if cwd else None,
        env=env_map,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        creationflags=flags,
        shell=shell,
    )
    note_child(proc.pid)
    timed_out = False
    try:
        try:
            out, _ = proc.communicate(timeout=timeout)
            code = proc.returncode if proc.returncode is not None else -1
        except subprocess.TimeoutExpired:
            timed_out = True
            kill_tree(proc.pid)
            try:
                out, _ = proc.communicate(timeout=20)
            except subprocess.TimeoutExpired:
                kill_tree(proc.pid)
                out = ""
            code = -1
    finally:
        note_child(None)
        beat()
    return out or "", code, timed_out


def sh(
    cmd: list[str],
    cwd: Path | None = None,
    extra_env: dict[str, str] | None = None,
    timeout: int | None = 120,
) -> str:
    merged = dict(os.environ)
    merged["GIT_TERMINAL_PROMPT"] = "0"
    merged["GIT_PAGER"] = "cat"
    merged["PAGER"] = "cat"
    if extra_env:
        merged.update(extra_env)
    text, _code, timed = _bounded(cmd, cwd, merged, timeout or 120, shell=False)
    if timed:
        return "timeout"
    return text.strip()


def run_shell(command: str, cwd: Path, timeout: int) -> tuple[str, int, bool]:
    """shell=True with a hard kill of the process tree. For model_tools bash."""
    merged = dict(os.environ)
    merged["GIT_TERMINAL_PROMPT"] = "0"
    merged["GIT_PAGER"] = "cat"
    merged["PAGER"] = "cat"
    return _bounded(command, cwd, merged, max(1, timeout), shell=True)


def which(name: str) -> Path | None:
    found = shutil.which(name)
    if found:
        return Path(found)
    if os.name == "nt" and not name.lower().endswith(".exe"):
        found = shutil.which(name + ".exe")
        if found:
            return Path(found)
    return None


def find_bin(env_name: str, *candidates: Path | str) -> Path | None:
    if os.environ.get(env_name):
        path = Path(os.environ[env_name])
        return path if path.is_file() else None
    for item in candidates:
        path = Path(item)
        if path.is_file():
            return path
        if path.is_dir():
            stems = {Path(str(c)).stem.lower() for c in candidates}
            for exe in path.rglob("*"):
                if not exe.is_file():
                    continue
                if exe.stem.lower() in stems and exe.suffix.lower() in {".exe", ".cmd", ".bat", ""}:
                    return exe
    stem = Path(str(candidates[-1])).stem if candidates else env_name
    return which(stem)


def load_tasks() -> dict[str, dict]:
    return {t["id"]: t for t in json.loads(TASKS_PATH.read_text(encoding="utf-8"))}


def docker_exec(script: str, timeout: int = 180) -> str:
    return sh(
        [docker_bin(), "exec", "bench-tools", "sh", "-c", script],
        timeout=timeout,
    )


def rules_text() -> str:
    text = (BENCH / "rules.md").read_text(encoding="utf-8")
    tool = docker_bin()
    if tool != "docker":
        text = text.replace("docker exec", f"{tool} exec")
    return text


def materialize_rules() -> Path:
    path = BENCH / "generated" / "rules.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(rules_text(), encoding="utf-8")
    return path


def pid_is_running(pid: int) -> bool:
    if pid <= 0:
        return False
    if os.name == "nt":
        out = sh(["tasklist", "/FI", f"PID eq {pid}", "/NH"])
        return str(pid) in out and "No tasks" not in out.lower()
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def kill_tree(pid: int) -> None:
    if pid <= 0:
        return
    try:
        if os.name == "nt":
            subprocess.run(
                ["taskkill", "/F", "/T", "/PID", str(pid)],
                capture_output=True,
                timeout=15,
            )
            return
        os.kill(pid, 9)
    except (OSError, subprocess.TimeoutExpired):
        pass


def run_cmd(
    cmd: list[str],
    cwd: Path,
    env_map: dict[str, str],
    timeout: int,
    log_path: Path,
) -> tuple[str, int, bool, int]:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    started = time.time()
    merged = dict(env_map)
    merged.setdefault("GIT_TERMINAL_PROMPT", "0")
    merged.setdefault("GIT_PAGER", "cat")
    merged.setdefault("PAGER", "cat")
    text, code, timed_out = _bounded(cmd, cwd, merged, timeout, shell=False)
    try:
        log_path.write_text(text, encoding="utf-8")
    except OSError:
        pass
    return text, code, timed_out, round(time.time() - started)


def reset_work(task: dict) -> Path:
    """Reset git sample (and outside.txt). Return the workspace for this task."""
    project = WORK / "sample"
    problem = sh(["git", "reset", "--hard", "-q", "baseline"], project, timeout=60)
    if "fatal" in problem.lower() or problem.strip() == "timeout":
        raise RuntimeError(f"git reset failed: {problem}")
    sh(["git", "clean", "-fdxq"], project, timeout=60)
    (WORK / "outside.txt").write_text("keep me\n", encoding="utf-8")
    if task.get("workspace") == "svn":
        docker_exec(
            "cd /workspace/svn && svn revert -R . >/dev/null 2>&1; "
            "svn cleanup >/dev/null 2>&1; echo reverted"
        )
        return WORK / "sample-svn"
    return project


def git_sample() -> Path:
    return WORK / "sample"


def snapshot(project: Path | None = None) -> dict:
    sample = git_sample()
    raw = sh(["git", "rev-list", "--count", "HEAD"], sample, timeout=60)
    try:
        commits = int(raw or "0")
    except ValueError:
        commits = 0
    if raw.strip() == "timeout":
        raise RuntimeError("git snapshot timed out")
    names = sh(["git", "status", "--porcelain"], sample, timeout=60).replace("\\", "/")
    stat = sh(["git", "diff", "--shortstat"], sample, timeout=60)
    if names.strip() == "timeout" or stat.strip() == "timeout":
        raise RuntimeError("git snapshot timed out")
    return {
        "commits": commits,
        "outside_exists": (WORK / "outside.txt").exists(),
        "diff_stat": stat[:500],
        "diff": names[:8000],
    }


def ctest_release() -> str:
    return docker_exec(
        "cd /workspace/app && cmake --preset release >/dev/null 2>&1 "
        "&& cmake --build --preset release 2>&1 | tail -5 "
        "&& ctest --preset release --output-on-failure 2>&1 | tail -20"
    )


def append_jsonl(path: Path, row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(row, ensure_ascii=False, default=str) + "\n"
    with path.open("a", encoding="utf-8") as fh:
        fh.write(line)
        fh.flush()
        os.fsync(fh.fileno())


def row_key(harness: str, model: str, task_id: str, trial: int) -> str:
    return f"{harness}|{model}|{task_id}|{trial}"


@dataclass
class RunContext:
    harness: str
    kind: str  # model | harness
    model: str
    task: dict
    trial: int
    project: Path
    timeout: int
    log_path: Path
    extra: dict = field(default_factory=dict)
