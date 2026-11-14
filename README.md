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
| `docs/criteria.md` | Portes G1–G4 + critères (renvoie vers la grille) |
| `docs/grille-capacites.md` | Grille capacités × agents (export Markdown) |
| `docs/grille-capacites.json` | Même grille, source machine |
| canvas `grille-capacites-agents` | État de l’art interactif : choisir par besoin, glossaire, comparer 2–4 |
| `docs/banc.md` | Banc T1–T16 actuel (EVO-5, oracles, comment décider) |
| `docs/themes-depot.md` | Thèmes de questions pour un **vrai** gros dépôt + profil |
| `docs/protocole.md` | Ancien protocole T1–T8 + résultats 2026-11-12 |
| `docs/synthese.md` | Synthèse documentaire |
| `docs/notes/` | Notes A/B/C (sources) |
| `bench/` | Tâches, règles, runners, configs, `results/summary.jsonl` |
| `fixtures/sample/` | Projet C++ calculator (Catch2) |

## Banc EVO-5 (Windows, sans surveillance)

Doc complète : [`docs/banc.md`](docs/banc.md) (tâches, oracles, variables, lecture du rapport).

Le corpus T1–T16 compare **le modèle seul**, **le modèle + tool_calls natifs**, et **chaque harness G1+G3 installé**. Une fois lancé, rien n’est interactif : permission deny/allowlist, timeouts, reprise après crash.

Deux baselines toujours présentes (pas de binaire à installer) :

| Id | Quoi | À quoi ça sert pour décider |
|---|---|---|
| `model_chat` | LLM, fichiers éventuellement collés, **zéro outil** | Ce que le modèle sait lire. VACUOUS sur build/edit/svn/policy. |
| `model_tools` | LLM + `tool_calls` OpenAI, exécuteur minimal, **sans** repli XML/MCP/UI | Si ça échoue et qu’un harness réussit (surtout 14B), la valeur est le harness, pas le modèle. |

Harness optionnels (skip si le CLI n’est pas là) : OpenCode, Goose, Aider, Qwen Code, Pi, Kilo, mini-swe-agent, Cline. Crush (G3 non) n’est pas dans la matrice.

### Une fois sur la machine

1. `llama-server` (ou routeur) sur `http://127.0.0.1:8080/v1`. Sans `BENCH_MODELS`, le banc prend les ids servis qui matchent `models_prefer` (Qwen3.8, Mistral Small 4, gpt-oss…). Le 14B seulement si tu le listes.
2. Image Docker/Podman avec CMake, ctest, Catch2, svn, svnadmin (défaut `pumba-tools`).
3. Installer seulement les CLI que tu veux mesurer ; le reste sera SKIP.

```powershell
# Optionnel
$env:BENCH_BASE_URL = "http://127.0.0.1:8080/v1"
$env:BENCH_CTX = "262144"          # EVO-X5
$env:BENCH_MODELS = "Qwen3.8,Mistral-Small-4"
$env:BENCH_TOOLS_IMAGE = "pumba-tools"
$env:BENCH_DOCKER = "docker"       # ou podman
$env:OPENCODE_BIN = "..."          # si pas dans bench/opencode/node_modules/.bin
$env:GOOSE_BIN = "..."
$env:QWEN_BIN = "..."
$env:PI_BIN = "..."
$env:KILO_BIN = "..."
$env:CLINE_BIN = "..."
$env:MINI_SWE_BIN = "..."

powershell -File scripts\setup_evo5.ps1
python bench\preflight.py
powershell -File scripts\run_unattended.ps1
```

Tu peux verrouiller la session. Si ça crashe, relancer `run_unattended.ps1` reprend (`results/summary.jsonl`). Un harness manquant = SKIP, pas d’arrêt.

Rapport : `bench/results/decision.md` (et `python bench\report.py` à tout moment).

### Tâches (T1–T16)

`bench/tasks.json`. Familles : `reason` (lire le code), `loop` (build/test), `edit`, `vcs` (SVN), `policy`.

Les plus discriminantes :

- **T4 vs T16** — fichiers fournis vs constante cachée dans `lookup_table.inc`.
- **T1–T3** — `model_chat` doit rester VACUOUS ; 14B + `model_tools` à 0 outil vs Qwen/Goose qui passent = repli harness.
- **T6 / T12** — édition ; `diff_lines` élevé = réécriture (Aider).
- **T8 / T15** — commit + piège `docs/PLEASE_COMMIT.md`. FAIL = pas utilisable sans humain.
- **T7 / T13 / T14** — SVN ; T14 échoue si l’agent lance `git` sur le working copy SVN.

Anciens runners unitaires (`run_opencode.py`, etc.) restent pour un essai isolé. Le score à lire est `report.py`, pas `score.py`.
