"""Unattended matrix runner. Resume-safe. Never prompts.

    python run_all.py
    python run_all.py --only opencode,goose
    python run_all.py --models gpt-oss-20b-MXFP4
    python run_all.py --tasks T4,T8,T16
"""

from __future__ import annotations

import argparse
import faulthandler
import json
import os
import sys
import threading
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

BENCH = Path(__file__).resolve().parent
sys.path.insert(0, str(BENCH))

from adapters import load_all  # noqa: E402
from common import (  # noqa: E402
    RESULTS,
    RunContext,
    WORK,
    append_jsonl,
    beat,
    child_pid,
    ctest_release,
    idle_seconds,
    kill_tree,
    load_tasks,
    pid_is_running,
    reset_work,
    row_key,
    snapshot,
    timeout_s,
)

# Persisted ERR/TIMEOUT stay done: transient blips are retried before the row is written.
FINAL = {"PASS", "FAIL", "VACUOUS", "ERR", "TIMEOUT"}
TRANSIENT_NEEDLES = (
    "connection",
    "refused",
    "10061",
    "10060",
    "timed out",
    "timeout",
    "llm http",
    "git reset",
    "snapshot",
    "unreachable",
    "closed",
    "docker",
    "urlopen",
    "temporary failure",
)
MAX_TRANSIENT = 3
from oracles import oracle  # noqa: E402

SUMMARY = RESULTS / "summary.jsonl"
PROGRESS = RESULTS / "progress.json"
LOG = RESULTS / "unattended.log"
LOCK = RESULTS / "run.lock"


def log(msg: str) -> None:
    beat()
    RESULTS.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} {msg}"
    print(line, flush=True)
    try:
        with LOG.open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")
            fh.flush()
    except OSError:
        pass


def _watchdog() -> None:
    while True:
        time.sleep(30)
        limit = timeout_s() * 2 + 180
        idle = idle_seconds()
        if idle < limit:
            continue
        log(f"WATCHDOG no heartbeat for {int(idle)}s — exit 75 so the launcher resumes")
        pid = child_pid()
        if pid:
            kill_tree(pid)
        os._exit(75)


def iter_rows():
    if not SUMMARY.exists():
        return
    for line in SUMMARY.read_text(encoding="utf-8-sig").splitlines():
        if not line.strip():
            continue
        try:
            yield json.loads(line)
        except json.JSONDecodeError:
            continue


def done_keys() -> set[str]:
    """Skip a cell only when a real verdict was recorded. Old rows without one are re-run."""
    keys: set[str] = set()
    for row in iter_rows():
        if (row.get("verdict") or "") not in FINAL:
            continue
        keys.add(
            row_key(
                row.get("harness", ""),
                row.get("model", ""),
                row.get("task", ""),
                int(row.get("trial") or 0),
            )
        )
    return keys


def transient_failure(row: dict) -> bool:
    """Connection / git / docker blip with no tool call. A real TIMEOUT is kept."""
    if row.get("verdict") != "ERR":
        return False
    if int(row.get("tool_calls") or 0) > 0:
        return False
    blob = f"{row.get('why') or ''} {row.get('error') or ''}".lower()
    return any(needle in blob for needle in TRANSIENT_NEEDLES)


def shrink(row: dict) -> dict:
    limits = {
        "answer": 12000,
        "raw_tail": 4000,
        "diff": 8000,
        "verify": 4000,
        "error": 2000,
        "why": 500,
    }
    for key, limit in limits.items():
        value = row.get(key)
        if isinstance(value, str) and len(value) > limit:
            row[key] = value[:limit] + "\n…[truncated]"
    return row


def safe_model_dir(model: str) -> str:
    cleaned = "".join(c if c not in '<>:"/\\|?*' else "_" for c in model).strip(" .")
    return (cleaned[:80] or "model")


def models_from(args: argparse.Namespace) -> list[str]:
    from adapters.llm import select_models

    explicit = [m.strip() for m in (args.models or "").split(",") if m.strip()]
    last = "no attempt"
    for attempt in range(1, 11):
        beat()
        try:
            chosen, notes = select_models(explicit or None)
            for note in notes:
                log(note)
            if not chosen:
                raise RuntimeError("empty model list")
            return chosen
        except Exception as exc:  # noqa: BLE001
            last = str(exc)
            log(f"LLM not ready ({exc}) {attempt}/10 — sleep 30s")
            time.sleep(30)
    log(f"ERROR: no usable model after 10 tries: {last}")
    raise SystemExit(4)


def verify_for(task: dict) -> str:
    # Independent post-state check only. Loop tasks (T1/T2/T3/T9) must be
    # scored from the agent's log — a clean fixture always builds.
    if task["id"] != "T6":
        return ""
    try:
        return ctest_release()
    except Exception as exc:  # noqa: BLE001
        return f"verify error: {exc}"


def run_trial(mod, harness_id: str, kind: str, model: str, task: dict, trial: int) -> dict:
    project = reset_work(task)
    raw_dir = RESULTS / harness_id / safe_model_dir(model)
    raw_dir.mkdir(parents=True, exist_ok=True)
    ctx = RunContext(
        harness=harness_id,
        kind=kind,
        model=model,
        task=task,
        trial=trial,
        project=project,
        timeout=timeout_s(),
        log_path=raw_dir / f"{task['id']}-{trial}.txt",
    )
    result = mod.run(ctx)
    if ctx.log_path.exists():
        log_text = ctx.log_path.read_text(encoding="utf-8", errors="replace")[-8000:]
        if len(log_text) > len(result.get("raw_tail") or ""):
            result["raw_tail"] = log_text
    snap = snapshot()
    row = {
        "harness": harness_id,
        "kind": kind,
        "model": model,
        "task": task["id"],
        "family": task.get("family"),
        "trial": trial,
        "utc": datetime.now(timezone.utc).isoformat(),
        **result,
        **snap,
        "verify": verify_for(task),
    }
    scored = oracle(task, row)
    row["verdict"] = scored.get("verdict")
    row["why"] = scored.get("why")
    if "diff_lines" in scored:
        row["diff_lines"] = scored["diff_lines"]
    return row


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", default="", help="comma harness ids")
    parser.add_argument("--models", default="", help="comma model ids as served by llama-server")
    parser.add_argument("--tasks", default="", help="comma task ids")
    parser.add_argument("--trials", type=int, default=0)
    args = parser.parse_args()

    if LOCK.exists():
        try:
            old = int((LOCK.read_text(encoding="utf-8").strip() or "0"))
        except ValueError:
            old = 0
        if old and pid_is_running(old) and old != os.getpid():
            log(f"ERROR: another run_all.py is live (pid {old}). One llama-server client at a time.")
            return 3
        log(f"stale lock (pid {old or '?'}); continuing (resume).")
    LOCK.parent.mkdir(parents=True, exist_ok=True)
    LOCK.write_text(str(os.getpid()), encoding="utf-8")
    RESULTS.mkdir(parents=True, exist_ok=True)
    fault_log = open(RESULTS / "faulthandler.log", "ab")  # noqa: SIM115
    faulthandler.enable(file=fault_log)
    faulthandler.dump_traceback_later(900, repeat=True, file=fault_log)
    threading.Thread(target=_watchdog, name="bench-watchdog", daemon=True).start()

    try:
        if not (WORK / "sample" / ".git").exists():
            log("ERROR: bench/work/sample missing. Run scripts/setup_evo5.ps1 first.")
            return 2

        matrix = json.loads((BENCH / "matrix.json").read_text(encoding="utf-8"))
        tasks = load_tasks()
        task_ids = [t.strip() for t in args.tasks.split(",") if t.strip()] or list(tasks)
        trials = args.trials or int(matrix.get("trials") or 3)
        models = models_from(args)
        adapters = load_all()
        only = {x.strip() for x in args.only.split(",") if x.strip()}
        wanted = [h["id"] for h in matrix["harnesses"] if not only or h["id"] in only]

        done = done_keys()
        log(f"resume: {len(done)} trials already in {SUMMARY.name}")
        log(f"models={models} harnesses={wanted} tasks={task_ids} trials={trials}")

        skipped: dict[str, str] = {}
        for hid in wanted:
            mod = adapters.get(hid)
            if mod is None:
                skipped[hid] = "no adapter"
                continue
            try:
                ok, msg = mod.available()
            except Exception as exc:  # noqa: BLE001
                ok, msg = False, str(exc)
            if not ok:
                skipped[hid] = msg
                log(f"SKIP {hid}: {msg}")

        total = 0
        ran = 0
        for hid in wanted:
            if hid in skipped:
                continue
            mod = adapters[hid]
            kind = getattr(mod, "KIND", "harness")
            for model in models:
                for tid in task_ids:
                    task = tasks.get(tid)
                    if task is None:
                        log(f"SKIP unknown task {tid}")
                        continue
                    for trial in range(1, trials + 1):
                        total += 1
                        key = row_key(hid, model, tid, trial)
                        if key in done:
                            continue
                        log(f"RUN {key}")
                        row: dict = {}
                        for attempt in range(1, MAX_TRANSIENT + 1):
                            try:
                                row = run_trial(mod, hid, kind, model, task, trial)
                            except Exception as exc:  # noqa: BLE001
                                log(f"  ERR {key}: {exc}")
                                row = {
                                    "harness": hid,
                                    "kind": kind,
                                    "model": model,
                                    "task": tid,
                                    "family": task.get("family"),
                                    "trial": trial,
                                    "verdict": "ERR",
                                    "why": str(exc)[:300],
                                    "error": traceback.format_exc()[-800:],
                                    "timed_out": False,
                                    "tools": [],
                                    "tool_calls": 0,
                                    "commits": 0,
                                    "outside_exists": True,
                                }
                            if not transient_failure(row) or attempt == MAX_TRANSIENT:
                                break
                            delay = 20 * attempt
                            log(
                                f"  transient ({row.get('why')}); "
                                f"retry {attempt}/{MAX_TRANSIENT} in {delay}s"
                            )
                            time.sleep(delay)
                        try:
                            append_jsonl(SUMMARY, shrink(row))
                        except Exception as exc:  # noqa: BLE001
                            log(f"  could not record {key}: {exc}")
                        log(
                            f"  {row.get('verdict')} tools={row.get('tool_calls')} "
                            f"why={row.get('why')}"
                        )
                        ran += 1
                        done.add(key)
                        try:
                            PROGRESS.write_text(
                                json.dumps({"ran": ran, "last": key, "skipped": skipped}, indent=2),
                                encoding="utf-8",
                            )
                        except OSError:
                            pass
        log(f"done. new={ran} skipped_harnesses={skipped}")
        return 0
    finally:
        if LOCK.exists():
            LOCK.unlink()


if __name__ == "__main__":
    raise SystemExit(main())
