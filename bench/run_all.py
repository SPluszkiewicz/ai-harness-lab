"""Unattended matrix runner. Resume-safe. Never prompts.

    python run_all.py
    python run_all.py --only opencode,goose
    python run_all.py --models gpt-oss-20b-MXFP4
    python run_all.py --tasks T4,T8,T16
"""

from __future__ import annotations

import argparse
import json
import os
import sys
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
    ctest_release,
    load_tasks,
    pid_is_running,
    reset_work,
    row_key,
    snapshot,
    timeout_s,
)
from oracles import oracle  # noqa: E402

SUMMARY = RESULTS / "summary.jsonl"
PROGRESS = RESULTS / "progress.json"
LOG = RESULTS / "unattended.log"
LOCK = RESULTS / "run.lock"


def log(msg: str) -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} {msg}"
    print(line, flush=True)
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def done_keys() -> set[str]:
    keys: set[str] = set()
    if not SUMMARY.exists():
        return keys
    for line in SUMMARY.read_text(encoding="utf-8-sig").splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        keys.add(row_key(row.get("harness", ""), row.get("model", ""), row.get("task", ""), int(row.get("trial") or 0)))
    return keys


def models_from(args: argparse.Namespace) -> list[str]:
    from adapters.llm import select_models

    explicit = [m.strip() for m in (args.models or "").split(",") if m.strip()]
    chosen, notes = select_models(explicit or None)
    for note in notes:
        log(note)
    return chosen


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
    raw_dir = RESULTS / harness_id / model
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
    append_jsonl(SUMMARY, row)
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
            ok, msg = mod.available()
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
                    task = tasks[tid]
                    for trial in range(1, trials + 1):
                        total += 1
                        key = row_key(hid, model, tid, trial)
                        if key in done:
                            continue
                        log(f"RUN {key}")
                        try:
                            row = run_trial(mod, hid, kind, model, task, trial)
                            log(
                                f"  {row.get('verdict')} tools={row.get('tool_calls')} "
                                f"why={row.get('why')}"
                            )
                        except Exception as exc:  # noqa: BLE001
                            log(f"  ERR {key}: {exc}")
                            append_jsonl(
                                SUMMARY,
                                {
                                    "harness": hid,
                                    "kind": kind,
                                    "model": model,
                                    "task": tid,
                                    "trial": trial,
                                    "verdict": "ERR",
                                    "why": str(exc)[:300],
                                    "error": traceback.format_exc()[-800:],
                                    "timed_out": False,
                                    "tools": [],
                                    "tool_calls": 0,
                                    "commits": 0,
                                    "outside_exists": True,
                                },
                            )
                        ran += 1
                        done.add(key)
                        PROGRESS.write_text(
                            json.dumps({"ran": ran, "last": key, "skipped": skipped}, indent=2),
                            encoding="utf-8",
                        )
        log(f"done. new={ran} skipped_harnesses={skipped}")
        return 0
    finally:
        if LOCK.exists():
            LOCK.unlink()


if __name__ == "__main__":
    raise SystemExit(main())
