"""Replay the bench tasks through the Pumba agent (reference).

    python run_pumba.py LABEL TASK[,TASK...] TRIALS

The agent mounts ./sample read-only, so only read tasks and the policy task are run.
Rows go to results/summary.jsonl with harness="pumba".
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import httpx

BENCH = Path(__file__).resolve().parent
ROOT = Path(
    __import__("os").environ.get("LOCAL_LLM_ROOT")
    or (BENCH.parents[1] / "local_llm")
).resolve()
TASKS = {t["id"]: t for t in json.loads((BENCH / "tasks.json").read_text(encoding="utf-8"))}


def token() -> str:
    env_path = ROOT / ".env"
    if not env_path.is_file():
        raise SystemExit(f"LOCAL_LLM_ROOT .env missing: {env_path} (set LOCAL_LLM_ROOT)")
    for line in env_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("AGENT_BEARER_TOKEN="):
            return line.split("=", 1)[1].strip()
    raise SystemExit("AGENT_BEARER_TOKEN missing")


def main() -> None:
    label, ids, trials = sys.argv[1], sys.argv[2].split(","), int(sys.argv[3])
    headers = {"Authorization": f"Bearer {token()}"}
    raw = BENCH / "results" / "pumba" / label
    raw.mkdir(parents=True, exist_ok=True)
    for task_id in ids:
        for trial in range(1, trials + 1):
            started = time.time()
            error = None
            body: dict = {}
            try:
                resp = httpx.post(
                    "http://127.0.0.1:8090/chat",
                    json={"query": TASKS[task_id]["prompt"]},
                    headers=headers,
                    timeout=900,
                )
                resp.raise_for_status()
                body = resp.json()
            except (httpx.HTTPError, json.JSONDecodeError) as exc:
                error = str(exc)
            elapsed = round(time.time() - started)
            (raw / f"{task_id}-{trial}.json").write_text(json.dumps(body, ensure_ascii=False, indent=1), encoding="utf-8")
            calls = body.get("tool_calls") or []
            row = {
                "harness": "pumba",
                "model": label,
                "task": task_id,
                "trial": trial,
                "elapsed_s": elapsed,
                "tool_calls": len(calls),
                "tools": [c.get("name") for c in calls],
                "tool_errors": sum(1 for c in calls if "failed" in (c.get("result_summary") or "")),
                "nudges": body.get("nudges"),
                "route": body.get("route"),
                "error": error,
                "answer": (body.get("answer") or "")[:700],
            }
            with (BENCH / "results" / "summary.jsonl").open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
            print(f"{label} {task_id}#{trial}: {elapsed}s tools={len(calls)} nudges={row['nudges']} route={row['route']} err={error}", flush=True)


if __name__ == "__main__":
    main()
