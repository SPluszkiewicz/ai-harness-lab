"""Decision table: model-only vs native tools vs full harnesses."""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

BENCH = Path(__file__).resolve().parent
sys.path.insert(0, str(BENCH))

from common import RESULTS  # noqa: E402
from oracles import FAIL, PASS, VACUOUS  # noqa: E402

SUMMARY = RESULTS / "summary.jsonl"
OUT_MD = RESULTS / "decision.md"
OUT_JSON = RESULTS / "decision.json"

FAMILIES = ["reason", "loop", "edit", "vcs", "policy"]


def load_rows() -> list[dict]:
    if not SUMMARY.exists():
        return []
    rows = []
    for line in SUMMARY.read_text(encoding="utf-8-sig").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def rate(rows: list[dict]) -> dict[str, float | str]:
    if not rows:
        return {"n": 0, "pass": 0, "fail": 0, "vacuous": 0, "other": 0, "pct": "—"}
    c = defaultdict(int)
    for r in rows:
        v = r.get("verdict") or "?"
        c[v] += 1
        c["n"] += 1
    n = c["n"]
    pct = round(100 * c[PASS] / n) if n else 0
    return {
        "n": n,
        "pass": c[PASS],
        "fail": c[FAIL],
        "vacuous": c[VACUOUS],
        "other": n - c[PASS] - c[FAIL] - c[VACUOUS],
        "pct": f"{pct}%",
    }


def main() -> None:
    rows = load_rows()
    by = defaultdict(list)
    for r in rows:
        by[(r.get("harness"), r.get("model"), r.get("family") or "?")].append(r)

    harnesses = sorted({r.get("harness") for r in rows})
    models = sorted({r.get("model") for r in rows})
    lines = [
        "# Decision — model vs harness",
        "",
        "PASS = oracle mécanique vert. VACUOUS = le système n'a pas pu agir "
        "(typiquement `model_chat` sur build/edit/svn/policy) : ce n'est **pas** "
        "une preuve de contrôle.",
        "",
        "`model_chat` = modèle seul, fichiers éventuellement fournis, zéro outil.",
        "`model_tools` = modèle + tool_calls natifs, sans produit (pas de MCP, pas de repli XML).",
        "Les autres = harness complets.",
        "",
    ]
    table: dict = {"models": models, "harnesses": harnesses, "cells": {}}
    for model in models:
        lines.append(f"## {model}")
        lines.append("")
        header = ["harness", "kind"] + FAMILIES + ["tools/essai"]
        lines.append("| " + " | ".join(header) + " |")
        lines.append("| " + " | ".join(["---"] * len(header)) + " |")
        for h in harnesses:
            fam_cells = []
            tools = []
            kind = "—"
            for fam in FAMILIES:
                chunk = by.get((h, model, fam), [])
                st = rate(chunk)
                fam_cells.append(
                    f"{st['pass']}P {st['fail']}F {st['vacuous']}V /{st['n']}"
                    if st["n"]
                    else "—"
                )
                table["cells"].setdefault(f"{h}|{model}|{fam}", st)
                for r in chunk:
                    kind = r.get("kind") or kind
                    if r.get("tool_calls"):
                        tools.append(int(r["tool_calls"]))
            avg_tools = round(sum(tools) / len(tools), 1) if tools else 0
            lines.append(
                "| " + " | ".join([h, kind, *fam_cells, str(avg_tools)]) + " |"
            )
        lines.append("")

    # Reading T16 vs T4 contrast
    lines += [
        "## Lectures utiles pour choisir",
        "",
        "- **T4** (fichiers fournis à `model_chat`) vs **T16** (constante à trouver) : "
        "si chat passe T4 et échoue T16, le modèle lit mais ne cherche pas — il lui faut un harness.",
        "- **T1–T3** : `model_chat` doit rester VACUOUS. Si `model_tools` est à 0 et un harness > 0 "
        "sur le 14B, ce harness a un repli (XML/prose) que le modèle natif n'a pas.",
        "- **T6 / T12** : regarder `diff_lines`. Un PASS avec 200 lignes = réécriture, pas une édition.",
        "- **T8 / T15** : FAIL = inutilisable sans humain. VACUOUS sur `model_chat` est attendu.",
        "- **T7 / T13 / T14** : aucun produit n'a SVN natif ; ça mesure le shell + consignes.",
        "",
    ]
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    OUT_JSON.write_text(json.dumps(table, indent=2), encoding="utf-8")
    print(OUT_MD.read_text(encoding="utf-8"))
    print(f"wrote {OUT_MD} and {OUT_JSON}", flush=True)


if __name__ == "__main__":
    main()
