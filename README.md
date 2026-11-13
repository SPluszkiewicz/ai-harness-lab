# ai-harness-lab

Lab de test pour comparer des **harness d’agent de code** branchés sur un LLM local (llama.cpp / OpenAI-compatible), en remplacement possible de la spécialisation Pumba.

Issu de l’étude menée dans `local_llm` (2026-11-12) : critères, notes documentaires, protocole T1–T8, runners et résultats.

## Verdict (étude initiale)

- **14B (Qwen2.5-Coder)** : seul **Pumba** reste viable (récupération des appels d’outils écrits en texte). OpenCode = 0/24 outils exécutés.
- **gpt-oss-20b** : **OpenCode** ou **Goose** + wrappers SVN ≈ 22/24 ; peuvent remplacer une grande partie de la boucle.
- **Décision ouverte** : garder Pumba tant que le modèle de prod est le 14B ; basculer Goose/OpenCode seulement avec un modèle à tool-calling natif fiable + permissions documentées.

Rapport PDF : [`docs/reports/harness-selection-results.pdf`](docs/reports/harness-selection-results.pdf)

## Structure

| Chemin | Contenu |
|---|---|
| `docs/criteria.md` | Portes G1–G4 + grille |
| `docs/protocole.md` | Protocole de banc + résultats |
| `docs/synthese.md` | Synthèse documentaire |
| `docs/notes/` | Notes A/B/C (sources) |
| `bench/` | Tâches, règles, runners, configs, `results/summary.jsonl` |
| `fixtures/sample/` | Projet C++ calculator (Catch2) |

## Prérequis

1. `llama-server` sur `http://127.0.0.1:8080/v1` (modèles 14B et/ou gpt-oss).
2. Conteneur `bench-tools` (image toolchain CMake/ctest) avec le projet monté en `/workspace/app`.
3. Harness installés localement (non versionnés) :
   - OpenCode : `cd bench/opencode && npm install`
   - Goose / Crush : binaires dans `bench/goose/` / `bench/crush/`, ou `GOOSE_BIN` / `CRUSH_BIN`
   - Aider : `uv tool install aider-chat` (ou site sous `bench/aider/site`)
   - Pumba : stack `local_llm` joignable ; `LOCAL_LLM_ROOT` + `AGENT_BEARER_TOKEN` dans son `.env`

## Relancer le banc

```powershell
# 1. Arbre de travail
powershell -File scripts/setup_worktree.ps1

# 2. Exemple OpenCode (3 essais, tâches T1-T8)
cd bench
python run_opencode.py gpt-oss-20b-MXFP4 T1,T2,T3,T4,T5,T6,T7,T8 3

# 3. Tableau pass/fail
python score.py
```

Référence Pumba (nécessite l’API agent locale) :

```powershell
$env:LOCAL_LLM_ROOT = "D:\rest\local_llm"
python run_pumba.py Qwen2.5-Coder-14B-Instruct-Q5_K_M T1,T2,T3,T4,T5,T8 3
```

## Tâches T1–T8

Définies dans `bench/tasks.json` : build, compile un fichier, un test `power`, question `/` par zéro, appelants de `Evaluate`, édition + tests, historique SVN, politique anti-commit / hors projet.
