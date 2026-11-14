"""Fail fast on missing llama-server / bench-tools. Harnesses are optional."""

from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path

BENCH = Path(__file__).resolve().parent
sys.path.insert(0, str(BENCH))

from adapters import load_all  # noqa: E402
from common import RESULTS, WORK, base_url, docker_bin, docker_exec, sh  # noqa: E402


def check_llm() -> dict:
    url = base_url() + "/models"
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.load(resp)
        ids = [m.get("id") for m in data.get("data") or [] if m.get("id")]
        return {"ok": True, "url": url, "models": ids}
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "url": url, "error": str(exc)}


def check_docker() -> dict:
    ps = sh([docker_bin(), "ps", "--filter", "name=bench-tools", "--format", "{{.Status}}"])
    if "Up" not in ps:
        return {"ok": False, "error": f"container bench-tools not running: {ps or 'missing'}"}
    cmake = docker_exec("cmake --version | head -1")
    svn = docker_exec("svn --version --quiet")
    work = docker_exec("ls /workspace/app/CMakeLists.txt /workspace/svn >/dev/null && echo mounts_ok")
    ok = "cmake" in cmake.lower() and "mounts_ok" in work
    return {"ok": ok, "cmake": cmake, "svn": svn, "mounts": work}


def main() -> int:
    RESULTS.mkdir(parents=True, exist_ok=True)
    llm = check_llm()
    docker = check_docker()
    sample = (WORK / "sample" / ".git").exists()
    svn_wc = (WORK / "sample-svn" / ".svn").exists() or (WORK / "sample-svn").exists()
    adapters = {}
    for hid, mod in load_all().items():
        ok, msg = mod.available()
        adapters[hid] = {"ok": ok, "detail": msg, "kind": getattr(mod, "KIND", "?")}
    selected = None
    probes = None
    if llm.get("ok"):
        from adapters.llm import probe_native_tools, select_models

        try:
            chosen, notes = select_models(None)
            selected = {"ids": chosen, "notes": notes}
            probes = {m: probe_native_tools(m) for m in chosen}
            if probes and not any(p.get("native_tool_calls") for p in probes.values()):
                print(
                    "WARNING: no selected model returned native tool_calls on the ping probe. "
                    "On EVO-5 load Qwen3.8 / Mistral-Small-4 / gpt-oss with --jinja.",
                    flush=True,
                )
        except Exception as exc:  # noqa: BLE001
            selected = {"error": str(exc)}
    report = {
        "llm": llm,
        "selected_models": selected,
        "tool_probes": probes,
        "docker": docker,
        "worktree": sample,
        "svn_copy": svn_wc,
        "adapters": adapters,
        "fatal": not (llm["ok"] and docker["ok"] and sample),
    }
    path = RESULTS / "preflight.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    if report["fatal"]:
        print("\nFATAL: llama-server, bench-tools, or worktree missing. See scripts/setup_evo5.ps1", flush=True)
        return 1
    missing = [k for k, v in adapters.items() if not v["ok"]]
    if missing:
        print(f"\nOptional harnesses missing (will SKIP): {', '.join(missing)}", flush=True)
    print("\npreflight ok — you can start run_all.py", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
