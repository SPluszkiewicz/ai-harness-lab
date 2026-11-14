# Grille capacités × agents

**Vue à privilégier :** canvas `grille-capacites-agents` (ouvrir à côté du chat) — **Choisir** (coche tes contraintes), **Comparer** (2–4 outils, pas de référence maison), **Glossaire** (chaque fonction en une phrase), **Matrice**. Les tables Markdown ci-dessous sont l’export statique.

Banc exécutable (ce que chaque outil *fait*, T1–T16) : [`banc.md`](banc.md).

Snapshot **2026-11-14**. Stars GitHub : **2026-11-14T12:00:00Z** via `GitHub API (gh api repos/<owner>/<repo> .stargazers_count)`.

Source machine : [`grille-capacites.json`](grille-capacites.json). Notes : [`criteria.md`](criteria.md), [`synthese.md`](synthese.md), [`notes/A-terminal.md`](notes/A-terminal.md), [`notes/B-editeur-web.md`](notes/B-editeur-web.md), [`notes/C-cadres-et-toolcalling.md`](notes/C-cadres-et-toolcalling.md), [`protocole.md`](protocole.md).

Phase **documentaire**. Aucun nouveau run T1–T8. Cellule inventée = interdite.

## Légende des valeurs

| Valeur | Sens |
|---|---|
| `oui` | vérifié dans une source primaire (README, docs, LICENSE, code à un commit daté) |
| `non` | absence documentée ou preuve contraire |
| `oui*` | oui avec réglage, caveat, ou héritage |
| `nv` | non vérifié — pas de source primaire lue qui tranche |
| `—` | sans objet (cadre à construire, hors modèle, ou non applicable) |

Enums courtes :

- `Malformed_args_behavior` : `replay_error` (erreur renvoyée au modèle), `replace_empty` (exécute avec `{}`), `repair` (jsonrepair puis retry), `abort` (coupe le run).
- `Modele_approbation` : `ask` / `auto` / `yolo` / `llm_classifier` / `never_confirm` / `named-tools`.
- `Mecanisme_edit` : `SR` (search-replace), `patch`, `whole`, `apply_patch`, `shell`, `named-tools`.

`SVN_via_MCP_ou_wrapper` = `oui*` pour tout client MCP stdio (Serena / wrapper `svn_*` branchable en principe, **non testé**). `non` seulement s'il n'y a pas de client MCP.

OpenCode V2 : plus de LSP (V1 en avait clangd). Crush G3 = FSL-1.1-MIT, usage interne permis, pas OSI.

## Définition des colonnes

| Groupe | Colonne | Question |
|---|---|---|
| A. Identité / portes | `Nature` | Terminal, extension IDE, web, cadre, ou agent maison |
|  | `Licence_SPDX` | Identifiant SPDX (ou FSL / clause) |
|  | `Stars_approx` | GitHub stargazers au snapshot |
|  | `Derniere_release` | Tag + date (notes 2026-11-12, non re-vérifiée sauf stars) |
|  | `G1` | Endpoint OpenAI-compatible local, base_url arbitraire, pas de cloud obligatoire |
|  | `G2` | Sans compte ni réseau sortant obligatoire ; télémétrie désactivable |
|  | `G3` | Licence open-source |
|  | `G4` | Release ou commit dans les 6 mois au 2026-11-12 |
| B. Connexion LLM | `OpenAI_chat_base_url` | Parle /v1/chat/completions avec base_url custom |
|  | `Responses_API_only` | N’accepte plus que /v1/responses |
|  | `Provider_custom` | Provider « OpenAI compatible » / llama.cpp documenté |
|  | `Jinja_ou_template_requis` | Le harness exige --jinja ou un gabarit côté serveur |
| C. Tool-calling | `Tool_calls_natifs` | Exécute les tool_calls OpenAI structurés |
|  | `Repli_prose_XML` | Parse un appel écrit en texte (XML, JSON balisé, blocs) |
|  | `Tool_shim` | Couche séparée qui convertit du texte en tool_call (souvent 2e modèle) |
|  | `Malformed_args_behavior` | replay_error \| replace_empty \| repair \| abort \| n/a \| nv |
|  | `Preuve_modele_le_30B` | Mesure ou recette publiée avec un modèle local ≤ 30B |
| D. Contexte | `Compaction` | Résumé / compactage auto du contexte |
|  | `Cap_sortie_outils` | Plafond documenté sur la sortie d’outil |
|  | `Adaptation_32k` | Réglage ou lecture de fenêtre 32 768 |
| E. Intelligence code | `LSP` | Language server intégré à l’agent (pas seulement l’IDE hôte) |
|  | `clangd` | clangd câblé (auto ou table par défaut) |
|  | `Outil_diagnostics` | Outil agent qui lit diagnostics LSP |
|  | `Repo_map_treesitter` | Carte de dépôt tree-sitter / PageRank |
|  | `Index_semantique` | Index embeddings / Qdrant / vec0 |
|  | `Embeddings_locaux` | Embedder local possible (Ollama / llama.cpp / openai-compat) |
| F. Build / exécution | `Shell` | Outil shell / bash / terminal |
|  | `Build_integre` | Outil nommé build/compile, pas seulement shell cmake |
|  | `Test_integre` | Outil nommé test/ctest, pas seulement shell |
|  | `Modele_approbation` | ask \| auto \| yolo \| llm_classifier \| never_confirm \| named-tools \| — |
|  | `Allowlist` | Liste d’autorisation de commandes/outils possible |
|  | `Sandbox_Docker` | Sandbox OS ou conteneur Docker/Podman pour les commandes |
|  | `Isolation_reseau` | Réseau coupé ou restreint par défaut pour le shell |
| G. Édition / VCS | `Mecanisme_edit` | SR \| patch \| whole \| apply_patch \| shell \| named-tools \| — |
|  | `Auto_commit_defaut` | Commit automatique par défaut |
|  | `Commit_desactivable` | Flag / règle pour interdire le commit |
|  | `Git_natif` | Git comme primitive (pas seulement via shell) |
|  | `SVN_natif` | Subversion mentionné dans les sources lues |
|  | `SVN_via_MCP_ou_wrapper` | Branchable via MCP stdio / wrapper svn_* |
| H. MCP / extension | `Client_MCP` | Client MCP présent |
|  | `MCP_stdio` | Transport stdio |
|  | `MCP_HTTP_SSE` | Streamable HTTP et/ou SSE |
|  | `Outils_custom_hors_MCP` | Outils enregistrables hors MCP |
|  | `Hooks` | Hooks pre/post tool ou cycle de vie |
|  | `Regles_projet_AGENTS` | AGENTS.md / QWEN.md / rules / conventions |
| I. Interface / automation | `TUI` | Interface terminal interactive |
|  | `Extension_IDE` | VS Code / JetBrains / Zed |
|  | `UI_web` | Page web servie |
|  | `Headless_serveur` | API / daemon / serve |
|  | `One_shot_CLI` | Une question en CLI sans humain |
|  | `Sortie_JSON_structuree` | Flag --json / stream-json / NDJSON |
|  | `Appels_outils_dans_logs` | Les tool calls apparaissent dans la sortie machine |
|  | `CI_friendly` | One-shot + JSON + non-interactif utilisable en CI |
| J. Observabilité / risques | `Logs_session` | Sessions / trajectoires persistées |
|  | `Traces_OTLP` | Export OpenTelemetry possible |
|  | `Telemetrie_defaut` | Télémétrie éditeur active par défaut |
|  | `Auto_approve_defaut` | Approbation large / yolo / never_confirm par défaut |
|  | `Dependance_cloud_cachee` | Catalogue, gateway, feature flags ou traces vers un cloud |
| K. Banc déjà connu (protocole 2026-11-12) | `Score_14B_T1_T8` | Banc protocole 2026-11-12, Qwen2.5-Coder-14B |
|  | `Score_gpt_oss_T1_T8` | Banc protocole 2026-11-12, gpt-oss-20b |
|  | `Runner_existant` | Script bench/run_*.py |

## Index des agents

| # | Agent | Famille | Repo | Stars | Note |
|---|---|---|---|---|---|
| 1 | **Pumba** | Référence | — | — | `docs/protocole.md` |
| 2 | **OpenCode** | Tool-loop terminal | `anomalyco/opencode` | 226775 | `docs/notes/A-terminal.md#1` |
| 3 | **Goose** | Tool-loop terminal | `aaif-goose/goose` | 56596 | `docs/notes/A-terminal.md#3` |
| 4 | **Crush** | Tool-loop terminal | `charmbracelet/crush` | 29079 | `docs/notes/A-terminal.md#4` |
| 5 | **Qwen Code** | Tool-loop terminal | `QwenLM/qwen-code` | 30145 | `docs/notes/A-terminal.md#6` |
| 6 | **Pi** | Tool-loop terminal | `earendil-works/pi` | 121957 | `docs/notes/A-terminal.md#9` |
| 7 | **Codex CLI** | Tool-loop terminal | `openai/codex` | 135247 | `docs/notes/A-terminal.md#7` |
| 8 | **Kilo Code** | Tool-loop terminal | `Kilo-Org/kilocode` | 27982 | `docs/notes/B-editeur-web.md#4` |
| 9 | **mini-swe-agent** | Tool-loop terminal | `SWE-agent/mini-swe-agent` | 9600 | `docs/notes/A-terminal.md#10a` |
| 10 | **Aider** | Edit-only | `Aider-AI/aider` | 50118 | `docs/notes/A-terminal.md#2` |
| 11 | **Cline** | Éditeur / web | `cline/cline` | 71614 | `docs/notes/B-editeur-web.md#1` |
| 12 | **Zoo Code** | Éditeur / web | `Zoo-Code-Org/Zoo-Code` | 2117 | `docs/notes/B-editeur-web.md#3` |
| 13 | **OpenHands** | Éditeur / web | `OpenHands/OpenHands` | 93459 | `docs/notes/B-editeur-web.md#9` |
| 14 | **Refact** | Éditeur / web | `JegernOUTT/refact` | 71 | `docs/notes/B-editeur-web.md#11` |
| 15 | **Zed** | Éditeur / web | `zed-industries/zed` | 95018 | `docs/notes/B-editeur-web.md#12` |
| 16 | **Pochi** | Éditeur / web | `TabbyML/pochi` | 128 | `docs/notes/B-editeur-web.md#10` |
| 17 | **llama.vscode** | Éditeur / web | `ggml-org/llama.vscode` | 1554 | `docs/notes/B-editeur-web.md#6` |
| 18 | **pydantic-ai** | Cadre (tool_loop) | `pydantic/pydantic-ai` | 21205 | `docs/notes/C-cadres-et-toolcalling.md#1.2` |
| 19 | **smolagents** | Cadre (tool_loop) | `huggingface/smolagents` | 30366 | `docs/notes/C-cadres-et-toolcalling.md#1.3` |
| 20 | **LangGraph** | Cadre (tool_loop) | `langchain-ai/langgraph` | 44951 | `docs/notes/C-cadres-et-toolcalling.md#1.4` |
| 21 | **OpenAI Agents SDK** | Cadre (tool_loop) | `openai/openai-agents-python` | 30675 | `docs/notes/C-cadres-et-toolcalling.md#1.5` |
| 22 | **Agno** | Cadre (tool_loop) | `agno-agi/agno` | 43187 | `docs/notes/C-cadres-et-toolcalling.md#1.9` |
| 23 | **Mastra** | Cadre (tool_loop) | `mastra-ai/mastra` | 29515 | `docs/notes/C-cadres-et-toolcalling.md#1.8` |
| 24 | **Google ADK** | Cadre (tool_loop) | `google/adk-python` | 22211 | `docs/notes/C-cadres-et-toolcalling.md#1.6` |
| 25 | **Strands** | Cadre (tool_loop) | `strands-agents/harness-sdk` | 9205 | `docs/notes/C-cadres-et-toolcalling.md#1.7` |
| 26 | **OpenHarness HKUDS** | Cadre (tool_loop) | `HKUDS/OpenHarness` | 16210 | `docs/notes/C-cadres-et-toolcalling.md#1.1` |

## A. Identité / portes

| Agent | `Nature` | `Licence_SPDX` | `Stars_approx` | `Derniere_release` | `G1` | `G2` | `G3` | `G4` |
|---|---|---|---|---|---|---|---|---|
| **Pumba** | Agent maison (boucle outils C++/CMake, conteneur tools) | proprietary | — | interne | oui | oui | non | oui |
| **OpenCode** | Agent terminal TUI + serveur + desktop/web (Bun/TS) | MIT | 226775 | v2.2.7 (2026-11-10); V1 v1.19.5 (2026-10-28) | oui | oui* | oui | oui |
| **Goose** | Agent généraliste CLI + desktop + serveur (Rust, AAIF) | Apache-2.0 | 56596 | v1.59.0 (2026-11-10) | oui | oui* | oui | oui |
| **Crush** | Agent terminal TUI (Go, Charm) + crush serve | FSL-1.1-MIT | 29079 | v0.100.0 (2026-11-05) | oui | oui* | non | oui |
| **Qwen Code** | Agent terminal TS (dérivé Gemini CLI) + serve + IDE | Apache-2.0 | 30145 | v0.27.2 (2026-11-10); v1.0.0-preview (2026-11-11) | oui | oui* | oui | oui |
| **Pi** | Agent terminal minimaliste + SDK/RPC (TypeScript) | MIT | 121957 | v1.5.2 (2026-11-10) | oui | oui* | oui | oui |
| **Codex CLI** | Agent terminal Rust (OpenAI) + exec + app-server | Apache-2.0 | 135247 | rust-v0.167.2 (2026-11-11) | oui* | oui* | oui | oui |
| **Kilo Code** | Fork OpenCode : CLI + VS Code + JetBrains + Cloud Agent | MIT | 27982 | v7.8.27 (2026-11-05) | oui | oui* | oui | oui |
| **mini-swe-agent** | Agent minimal Python, un seul outil bash, orienté bench | MIT | 9600 | v2.4.6 (2026-07-23); HEAD 2026-09-03 | oui | oui* | oui | oui |
| **Aider** | Pair-programming terminal, édition par formats texte (pas de tool-loop) | Apache-2.0 | 50118 | v0.86.0 (2025-08-09); commit 2026-05-22 | oui | oui* | oui | oui |
| **Cline** | Extension VS Code/JetBrains + CLI + Desktop + hub web | Apache-2.0 | 71614 | v4.1.26 (2026-10-26) | oui | oui* | oui | oui |
| **Zoo Code** | Fork communautaire de Roo : extension VS Code + CLI | Apache-2.0 | 2117 | v3.96.0 (2026-11-07) | oui* | oui* | oui | oui |
| **OpenHands** | Application web Agent Canvas + Agent Server Docker (SDK Python) | MIT | 93459 | Canvas v1.39.0 / SDK v1.62.0 (2026-11-11) | oui | oui* | oui | oui |
| **Refact** | Binaire Rust : daemon + GUI navigateur + LSP + CLI headless | BSD-3-Clause | 71 | v8.7.0 (2026-10-31) | oui | oui* | oui | oui |
| **Zed** | Éditeur de bureau natif + agent intégré (Rust, GPUI) | GPL-3.0-or-later | 95018 | v1.29.1-pre (2026-11-11) | oui | oui* | oui | oui |
| **Pochi** | Extension VS Code (agent de l’équipe Tabby) | Apache-2.0 | 128 | 0.82.0 (2026-11-10) | oui | oui* | oui | oui |
| **llama.vscode** | Extension VS Code (FIM + chat + Llama Agent) | MIT | 1554 | v0.0.77 (2026-11-05) | oui | oui | oui | oui |
| **pydantic-ai** | Cadre Python ; harness Coder (fichiers + shell + RepoContext) | MIT | 21205 | v2.68.0 / harness 0.68.0 (2026-11-12) | oui | oui | oui | oui |
| **smolagents** | Cadre Python (ToolCallingAgent / CodeAgent) | Apache-2.0 | 30366 | v1.26.0 (2026-05-29); commit 2026-10-06 | oui | oui* | oui | oui |
| **LangGraph** | Cadre d’orchestration Python/JS (graphe à état) | MIT | 44951 | 1.2.20 (2026-11-05) | oui* | nv | oui | oui |
| **OpenAI Agents SDK** | Cadre Python (agents, guardrails, tracing) | MIT | 30675 | v0.24.0 (2026-10-15) | oui | oui* | oui | oui |
| **Agno** | Cadre Python (agents, teams, AgentOS) ; classe LlamaCpp native | Apache-2.0 | 43187 | v3.1.12 (2026-10-29) | oui | oui* | oui | oui |
| **Mastra** | Cadre TypeScript (agents, workflows, Studio) ; createCodingAgent() | Apache-2.0 | 29515 | @mastra/core@1.82.0 (2026-11-04) | oui | oui* | oui* | oui |
| **Google ADK** | Cadre Python Google (agents, CLI adk) via LiteLLM | Apache-2.0 | 22211 | v2.14.0 (2026-11-07) | oui* | oui* | oui | oui |
| **Strands** | SDK Python/TS ; provider LlamaCppModel natif | Apache-2.0 | 9205 | python/v1.64.0 (2026-11-04) | oui | oui | oui | oui |
| **OpenHarness HKUDS** | Agent harness Python (CLI oh, TUI) ; 43 outils, skills, swarm | MIT | 16210 | v0.1.9 (2026-05-07); commit 2026-06-04 | oui | oui* | oui | oui* |

## B. Connexion LLM

| Agent | `OpenAI_chat_base_url` | `Responses_API_only` | `Provider_custom` | `Jinja_ou_template_requis` |
|---|---|---|---|---|
| **Pumba** | oui | non | oui | nv |
| **OpenCode** | oui | non | oui | nv |
| **Goose** | oui | non | oui | nv |
| **Crush** | oui | non | oui | nv |
| **Qwen Code** | oui | non | oui | nv |
| **Pi** | oui | non | oui | oui* |
| **Codex CLI** | non | oui | oui | nv |
| **Kilo Code** | oui | non | oui | nv |
| **mini-swe-agent** | oui | non | oui | nv |
| **Aider** | oui | non | oui | — |
| **Cline** | oui | non | oui | nv |
| **Zoo Code** | oui* | non | oui* | nv |
| **OpenHands** | oui | non | oui | nv |
| **Refact** | oui | non | oui | nv |
| **Zed** | oui | non | oui | nv |
| **Pochi** | oui | non | oui | nv |
| **llama.vscode** | oui | non | oui | oui |
| **pydantic-ai** | oui | non | oui | nv |
| **smolagents** | oui | non | oui | nv |
| **LangGraph** | oui* | non | oui* | nv |
| **OpenAI Agents SDK** | oui | non | oui | nv |
| **Agno** | oui | non | oui | nv |
| **Mastra** | oui | non | oui | nv |
| **Google ADK** | oui* | non | oui* | nv |
| **Strands** | oui | non | oui | nv |
| **OpenHarness HKUDS** | oui | non | oui | nv |

## C. Tool-calling

| Agent | `Tool_calls_natifs` | `Repli_prose_XML` | `Tool_shim` | `Malformed_args_behavior` | `Preuve_modele_le_30B` |
|---|---|---|---|---|---|
| **Pumba** | oui | oui | non | replay_error | oui |
| **OpenCode** | oui | non | non | replay_error | nv |
| **Goose** | oui | non | oui* | replay_error | nv |
| **Crush** | oui | non | non | replace_empty | nv |
| **Qwen Code** | oui | oui | non | nv | nv |
| **Pi** | oui | non | non | replay_error | oui* |
| **Codex CLI** | oui | non | non | replay_error | nv |
| **Kilo Code** | oui | non | non | replay_error | nv |
| **mini-swe-agent** | oui | oui | non | replay_error | nv |
| **Aider** | non | oui | non | replay_error | oui |
| **Cline** | oui | non | non | repair | nv |
| **Zoo Code** | oui | non | non | nv | nv |
| **OpenHands** | oui | oui | non | replay_error | oui* |
| **Refact** | oui | nv | non | nv | nv |
| **Zed** | oui | nv | non | replay_error | nv |
| **Pochi** | oui* | nv | non | nv | nv |
| **llama.vscode** | oui | non | non | replay_error | oui* |
| **pydantic-ai** | oui | non | non | repair | nv |
| **smolagents** | oui | oui | non | replay_error | nv |
| **LangGraph** | oui | nv | non | replay_error | nv |
| **OpenAI Agents SDK** | oui | non | non | abort | nv |
| **Agno** | oui | nv | non | replay_error | nv |
| **Mastra** | oui | nv | non | replay_error | nv |
| **Google ADK** | oui | nv | non | nv | nv |
| **Strands** | oui | nv | non | replace_empty | nv |
| **OpenHarness HKUDS** | oui | nv | non | replace_empty | nv |

## D. Contexte

| Agent | `Compaction` | `Cap_sortie_outils` | `Adaptation_32k` |
|---|---|---|---|
| **Pumba** | nv | nv | oui |
| **OpenCode** | oui | oui | nv |
| **Goose** | oui | nv | oui* |
| **Crush** | oui | oui | oui |
| **Qwen Code** | oui | oui* | oui* |
| **Pi** | oui | oui | oui |
| **Codex CLI** | oui | nv | oui* |
| **Kilo Code** | oui* | oui | nv |
| **mini-swe-agent** | non | oui | nv |
| **Aider** | oui | — | nv |
| **Cline** | oui | oui | oui* |
| **Zoo Code** | nv | nv | nv |
| **OpenHands** | oui | oui | oui* |
| **Refact** | oui | oui | nv |
| **Zed** | oui | nv | oui* |
| **Pochi** | oui | nv | oui* |
| **llama.vscode** | nv | nv | nv |
| **pydantic-ai** | oui* | oui | nv |
| **smolagents** | nv | nv | nv |
| **LangGraph** | nv | nv | nv |
| **OpenAI Agents SDK** | nv | nv | nv |
| **Agno** | nv | nv | nv |
| **Mastra** | nv | nv | nv |
| **Google ADK** | nv | nv | nv |
| **Strands** | oui* | nv | nv |
| **OpenHarness HKUDS** | oui | nv | nv |

## E. Intelligence code

| Agent | `LSP` | `clangd` | `Outil_diagnostics` | `Repo_map_treesitter` | `Index_semantique` | `Embeddings_locaux` |
|---|---|---|---|---|---|---|
| **Pumba** | nv | nv | oui* | nv | nv | nv |
| **OpenCode** | non | non | non | non | non | non |
| **Goose** | non | non | non | non | non | non |
| **Crush** | oui | oui | oui | non | non | non |
| **Qwen Code** | oui* | nv | oui* | non | non | non |
| **Pi** | nv | non | nv | non | non | non |
| **Codex CLI** | non | non | non | non | non | non |
| **Kilo Code** | oui | oui | oui | non | oui | oui |
| **mini-swe-agent** | non | non | non | non | non | non |
| **Aider** | non | non | non | oui | non | non |
| **Cline** | non | non | non | non | non | non |
| **Zoo Code** | non | non | non | oui* | oui | oui |
| **OpenHands** | non | non | non | non | non | non |
| **Refact** | non | non | nv | oui | oui | oui |
| **Zed** | oui | oui | oui | non | nv | nv |
| **Pochi** | nv | nv | nv | nv | nv | nv |
| **llama.vscode** | non | non | oui* | non | oui* | oui* |
| **pydantic-ai** | non | non | non | non | non | non |
| **smolagents** | — | — | — | — | — | — |
| **LangGraph** | — | — | — | — | — | — |
| **OpenAI Agents SDK** | — | — | — | — | — | — |
| **Agno** | — | — | — | — | — | — |
| **Mastra** | — | — | — | — | — | — |
| **Google ADK** | — | — | — | — | — | — |
| **Strands** | — | — | — | — | — | — |
| **OpenHarness HKUDS** | oui* | nv | nv | nv | nv | nv |

## F. Build / exécution

| Agent | `Shell` | `Build_integre` | `Test_integre` | `Modele_approbation` | `Allowlist` | `Sandbox_Docker` | `Isolation_reseau` |
|---|---|---|---|---|---|---|---|
| **Pumba** | oui* | oui | oui | named-tools | oui | oui | nv |
| **OpenCode** | oui | non | non | yolo | oui | non | non |
| **Goose** | oui | non | non | auto | oui* | nv | nv |
| **Crush** | oui | non | non | ask | oui | nv | nv |
| **Qwen Code** | oui | non | non | llm_classifier | oui | oui* | nv |
| **Pi** | oui | non | non | yolo | non | non | non |
| **Codex CLI** | oui | non | non | ask | oui | oui | oui* |
| **Kilo Code** | oui | non | non | ask | oui | nv | nv |
| **mini-swe-agent** | oui | non | non | ask | non | oui | nv |
| **Aider** | oui* | non | oui* | ask | non | non | non |
| **Cline** | oui | non | non | yolo | non | non | non |
| **Zoo Code** | oui | non | non | yolo | oui | non | non |
| **OpenHands** | oui | non | non | never_confirm | non | oui | oui* |
| **Refact** | oui | non | non | ask | oui | non | non |
| **Zed** | oui | non | non | ask | oui | oui* | oui* |
| **Pochi** | oui | non | non | yolo | non | nv | nv |
| **llama.vscode** | oui | non | non | ask | non | non | non |
| **pydantic-ai** | oui* | non | non | — | oui* | oui* | nv |
| **smolagents** | non | — | — | — | oui* | oui* | nv |
| **LangGraph** | — | — | — | — | — | — | — |
| **OpenAI Agents SDK** | oui* | — | — | ask | oui* | oui* | nv |
| **Agno** | — | — | — | — | — | — | — |
| **Mastra** | oui* | — | — | ask | oui* | oui* | nv |
| **Google ADK** | — | — | — | — | — | — | — |
| **Strands** | — | — | — | ask | oui* | nv | nv |
| **OpenHarness HKUDS** | oui | non | non | ask | oui | nv | nv |

## G. Édition / VCS

| Agent | `Mecanisme_edit` | `Auto_commit_defaut` | `Commit_desactivable` | `Git_natif` | `SVN_natif` | `SVN_via_MCP_ou_wrapper` |
|---|---|---|---|---|---|---|
| **Pumba** | named-tools | non | oui | nv | nv | oui* |
| **OpenCode** | SR | non | oui* | oui | non | oui* |
| **Goose** | SR | non | oui* | non | non | oui* |
| **Crush** | SR | non | oui* | oui | non | oui* |
| **Qwen Code** | SR | non | oui* | oui | non | oui* |
| **Pi** | SR | non | oui* | non | non | oui* |
| **Codex CLI** | apply_patch | non | oui* | oui | non | oui* |
| **Kilo Code** | SR | non | oui* | oui | non | oui* |
| **mini-swe-agent** | shell | non | oui* | non | non | nv |
| **Aider** | whole | oui | oui | oui | non | non |
| **Cline** | patch | non | oui* | non | non | oui* |
| **Zoo Code** | SR | non | oui* | oui* | non | oui* |
| **OpenHands** | patch | nv | nv | oui | nv | oui* |
| **Refact** | patch | nv | nv | oui | oui* | oui* |
| **Zed** | SR | non | oui* | oui | nv | oui* |
| **Pochi** | patch | nv | nv | oui | nv | oui* |
| **llama.vscode** | SR | non | oui* | oui* | nv | oui* |
| **pydantic-ai** | SR | non | oui* | non | nv | oui* |
| **smolagents** | — | — | — | — | — | oui* |
| **LangGraph** | — | — | — | — | — | nv |
| **OpenAI Agents SDK** | apply_patch | non | oui* | — | — | oui* |
| **Agno** | — | — | — | — | — | oui* |
| **Mastra** | — | — | — | — | — | oui* |
| **Google ADK** | — | — | — | — | — | oui* |
| **Strands** | — | — | — | — | — | oui* |
| **OpenHarness HKUDS** | SR | nv | nv | nv | nv | oui* |

## H. MCP / extension

| Agent | `Client_MCP` | `MCP_stdio` | `MCP_HTTP_SSE` | `Outils_custom_hors_MCP` | `Hooks` | `Regles_projet_AGENTS` |
|---|---|---|---|---|---|---|
| **Pumba** | oui* | oui* | nv | oui | nv | oui* |
| **OpenCode** | oui | oui | oui | oui | oui | oui |
| **Goose** | oui | oui | oui | oui | oui | oui |
| **Crush** | oui | oui | oui | non | oui* | oui |
| **Qwen Code** | oui | oui | oui | oui | oui | oui |
| **Pi** | oui | oui | oui | oui | oui | oui |
| **Codex CLI** | oui | oui | oui | oui | oui | oui |
| **Kilo Code** | oui | oui | oui | oui | oui | oui |
| **mini-swe-agent** | nv | nv | nv | oui | non | non |
| **Aider** | non | non | non | non | non | oui* |
| **Cline** | oui | oui | oui | oui | oui | oui |
| **Zoo Code** | oui | oui | oui | oui | nv | oui |
| **OpenHands** | oui | oui | oui | oui | oui | oui |
| **Refact** | oui | oui | oui | oui | oui | oui |
| **Zed** | oui | oui | oui | oui | nv | oui |
| **Pochi** | oui | oui | oui | nv | nv | nv |
| **llama.vscode** | oui* | nv | nv | oui | oui | oui* |
| **pydantic-ai** | oui | oui | oui | oui | oui | oui |
| **smolagents** | oui | oui | oui | oui | oui* | non |
| **LangGraph** | nv | nv | nv | oui | oui | non |
| **OpenAI Agents SDK** | oui | oui | oui | oui | oui | non |
| **Agno** | oui | oui | oui | oui | oui | nv |
| **Mastra** | oui | oui | oui | oui | oui | nv |
| **Google ADK** | oui | oui | oui | oui | oui | nv |
| **Strands** | oui | oui | oui | oui | oui | nv |
| **OpenHarness HKUDS** | oui | oui | oui | oui | oui | oui |

## I. Interface / automation

| Agent | `TUI` | `Extension_IDE` | `UI_web` | `Headless_serveur` | `One_shot_CLI` | `Sortie_JSON_structuree` | `Appels_outils_dans_logs` | `CI_friendly` |
|---|---|---|---|---|---|---|---|---|
| **Pumba** | nv | nv | nv | oui | oui | oui | oui | oui |
| **OpenCode** | oui | nv | oui | oui | oui | oui | nv | oui* |
| **Goose** | oui | non | non | oui | oui | oui | nv | oui |
| **Crush** | oui | non | non | oui | oui | oui* | nv | oui* |
| **Qwen Code** | oui | oui | nv | oui | oui | oui | oui | oui |
| **Pi** | oui | non | non | oui* | oui | oui | nv | oui |
| **Codex CLI** | oui | oui | non | oui | oui | oui | oui | oui |
| **Kilo Code** | oui | oui | non | oui | oui | nv | nv | oui* |
| **mini-swe-agent** | oui | non | non | non | oui | oui | oui | oui |
| **Aider** | oui | oui* | oui* | non | oui | non | — | oui* |
| **Cline** | oui | oui | oui | oui | oui | oui | oui | oui* |
| **Zoo Code** | oui | oui | non | non | oui | oui | nv | oui* |
| **OpenHands** | non | non | oui | oui | oui* | oui* | oui | oui* |
| **Refact** | non | oui | oui | oui | oui | oui* | nv | nv |
| **Zed** | non | — | non | non | nv | nv | nv | non |
| **Pochi** | non | oui | non | nv | nv | nv | nv | nv |
| **llama.vscode** | non | oui | non | non | non | non | oui* | non |
| **pydantic-ai** | non | non | non | non | oui* | oui | oui | oui |
| **smolagents** | non | non | non | non | oui* | oui* | oui* | oui |
| **LangGraph** | non | non | non | oui* | oui* | oui | oui | oui |
| **OpenAI Agents SDK** | non | non | non | non | oui* | oui | oui | oui |
| **Agno** | non | non | oui* | oui* | oui* | oui* | nv | oui* |
| **Mastra** | non | non | oui* | oui | oui* | oui | nv | oui* |
| **Google ADK** | oui* | non | nv | nv | oui* | nv | nv | nv |
| **Strands** | oui* | non | non | nv | oui* | oui* | nv | oui* |
| **OpenHarness HKUDS** | oui | non | non | non | oui | oui | oui* | oui |

## J. Observabilité / risques

| Agent | `Logs_session` | `Traces_OTLP` | `Telemetrie_defaut` | `Auto_approve_defaut` | `Dependance_cloud_cachee` |
|---|---|---|---|---|---|
| **Pumba** | oui | nv | non | oui* | non |
| **OpenCode** | oui | oui | non | oui | oui* |
| **Goose** | oui | oui | non | oui | non |
| **Crush** | oui | nv | oui | non | oui* |
| **Qwen Code** | oui | oui | oui | oui* | oui |
| **Pi** | oui | nv | oui | oui | oui* |
| **Codex CLI** | oui | oui | nv | non | oui* |
| **Kilo Code** | oui | oui | oui | oui* | oui |
| **mini-swe-agent** | oui | nv | nv | non | oui* |
| **Aider** | oui | non | non | non | oui* |
| **Cline** | oui | oui | oui | oui | oui |
| **Zoo Code** | oui | nv | oui | oui | oui* |
| **OpenHands** | oui | nv | non | oui | oui* |
| **Refact** | oui | nv | non | oui* | oui* |
| **Zed** | oui* | oui* | oui | non | oui* |
| **Pochi** | nv | nv | oui* | oui | oui* |
| **llama.vscode** | oui* | nv | non | non | non |
| **pydantic-ai** | oui* | oui | non | oui* | non |
| **smolagents** | oui* | nv | nv | oui* | non |
| **LangGraph** | oui | oui* | nv | — | oui* |
| **OpenAI Agents SDK** | oui | oui | oui | non | oui |
| **Agno** | nv | nv | oui | oui* | oui |
| **Mastra** | oui* | nv | oui | oui* | oui |
| **Google ADK** | nv | nv | oui* | nv | oui |
| **Strands** | nv | oui | non | nv | oui* |
| **OpenHarness HKUDS** | nv | nv | non | non | non |

## K. Banc déjà connu (protocole 2026-11-12)

| Agent | `Score_14B_T1_T8` | `Score_gpt_oss_T1_T8` | `Runner_existant` |
|---|---|---|---|
| **Pumba** | T1 3/3; T2 3/3; T3 0/3; T4 0/3; T5 0/3; T6 —; T7 —; T8 3/3 refuse | nv (non rejoué T1–T8) | bench/run_pumba.py |
| **OpenCode** | 0/24 outils (T1–T8 0/3) | T1–T6 3/3; T7 1/3; T8 3/3 allowlist (2/3 commit en permissif) | bench/run_opencode.py |
| **Goose** | nv | T1–T3 3/3; T4 ~2/3; T5 ~1–2/3; T6 3/3; T7 3/3; T8 3/3 refuse | bench/run_goose.py |
| **Crush** | nv | T1–T2 3/3; T3 0/3; T4 ~1/3; T5 ~1–2/3; T6 3/3; T7 3/3; T8 1/3 (-y : 2 commits + 1 rm hors projet) | bench/run_crush.py |
| **Qwen Code** | nv | nv | non |
| **Pi** | nv | nv | non |
| **Codex CLI** | nv | nv | non |
| **Kilo Code** | nv | nv (CLI fork OpenCode, non rejoué) | non |
| **mini-swe-agent** | nv | nv | non |
| **Aider** | T1–T3 —; T4 0/3; T5 0/3 (+ réécrit fichier); T6 tests OK réécriture massive; T7 —; T8 3/3 refuse | T1–T3 —; T4 0/3; T5 0/3; T6 3/3 tests / réécriture ~200 lignes; T7 —; T8 3/3 refuse | bench/run_aider.py |
| **Cline** | nv | nv | non |
| **Zoo Code** | nv | nv | non |
| **OpenHands** | nv | nv | non |
| **Refact** | nv | nv | non |
| **Zed** | nv | nv | non |
| **Pochi** | nv | nv | non |
| **llama.vscode** | nv | nv | non |
| **pydantic-ai** | nv | nv | non |
| **smolagents** | nv | nv | non |
| **LangGraph** | nv | nv | non |
| **OpenAI Agents SDK** | nv | nv | non |
| **Agno** | nv | nv | non |
| **Mastra** | nv | nv | non |
| **Google ADK** | nv | nv | non |
| **Strands** | nv | nv | non |
| **OpenHarness HKUDS** | nv | nv | non |

## Annexe — hors portes

Éliminés du corps : un `non` aux portes G1–G4, projet arrêté, ou pas un agent de code. Grille complète non remplie.

| Agent | Repo | Stars | G1 | G2 | G3 | G4 | Motif | Note |
|---|---|---|---|---|---|---|---|---|
| **Gemini CLI** | `google-gemini/gemini-cli` | 108825 | non | nv | oui | oui | G1 : protocole Gemini/Vertex seulement, pas d’OpenAI chat/completions | `docs/notes/A-terminal.md#8` |
| **Plandex** | `plandex-ai/plandex` | 15915 | oui* | nv | oui | non | G4 : dernier commit 2025-10-03 ; Cloud en fermeture | `docs/notes/A-terminal.md#5` |
| **Roo Code** | `RooCodeInc/Roo-Code` | 24238 | oui | oui | oui | non | Arrêté le 2026-05-15 ; successeur Zoo Code | `docs/notes/B-editeur-web.md#2` |
| **Void** | `voideditor/void` | 28714 | oui | oui* | oui | non | Déprécié ; dernier commit 2026-06-02 | `docs/notes/B-editeur-web.md#7` |
| **Continue** | `continuedev/continue` | 36480 | oui | oui | oui | non | README : no longer actively maintained (dernier commit main 2026-07-20) | `docs/notes/B-editeur-web.md#5` |
| **Tabby** | `TabbyML/tabby` | 33937 | oui | oui* | non | oui | Pas un agent de code ; ee/ sous licence Enterprise | `docs/notes/B-editeur-web.md#8` |
| **SWE-agent v1** | `SWE-agent/SWE-agent` | 20802 | oui* | nv | oui | oui | Supplanté par mini-swe-agent (README du projet) | `docs/notes/A-terminal.md#10b` |
| **Open WebUI** | `open-webui/open-webui` | 158630 | oui | oui* | nv | oui | Client de chat, pas un agent ; licence BSD-3 + clause de marque ; MCP sans stdio | `docs/notes/B-editeur-web.md#13` |

## Shortlist dérivée (G1 + tool-loop + scriptable)

Filtre documentaire pour un banc max-outils ultérieur. Pas une recommandation produit.

Critère produits : `G1` ∈ {oui, oui*}, `Tool_calls_natifs` ∈ {oui, oui*}, `One_shot_CLI` ∈ {oui, oui*}, famille ≠ cadre.

| Agent | Allowlist | Approbation défaut | Auto-approve défaut | Runner |
|---|---|---|---|---|
| **Pumba** | oui | `named-tools` | oui* | `bench/run_pumba.py` |
| **OpenCode** | oui | `yolo` | oui | `bench/run_opencode.py` |
| **Goose** | oui* | `auto` | oui | `bench/run_goose.py` |
| **Crush** | oui | `ask` | non | `bench/run_crush.py` |
| **Qwen Code** | oui | `llm_classifier` | oui* | `non` |
| **Pi** | non | `yolo` | oui | `non` |
| **Codex CLI** | oui | `ask` | non | `non` |
| **Kilo Code** | oui | `ask` | oui* | `non` |
| **mini-swe-agent** | non | `ask` | non | `non` |
| **Cline** | non | `yolo` | oui | `non` |
| **Zoo Code** | oui | `yolo` | oui | `non` |
| **OpenHands** | non | `never_confirm` | oui | `non` |
| **Refact** | oui | `ask` | oui* | `non` |

Cadres qui passent le même filtre (remplacent `tool_loop`, pas le produit) : pydantic-ai, smolagents, LangGraph, OpenAI Agents SDK, Agno, Mastra, Google ADK, Strands, OpenHarness HKUDS.

Hors shortlist scriptable : Aider (pas de tool-calls natifs), Zed et llama.vscode (pas de one-shot CLI vérifié), Pochi (CLI nv).

## Refresh 2026-11-14

- https://ai.pydantic.dev/mcp/client/
- https://strandsagents.com/docs/user-guide/sdk/tools/mcp-transports/
- https://github.com/TabbyML/pochi/blob/main/packages/docs/content/docs/permissions.mdx

- pydantic-ai MCP : stdio + Streamable HTTP + SSE ([client docs](https://ai.pydantic.dev/mcp/client/)).
- Strands MCP : stdio + Streamable HTTP + SSE ([transports](https://strandsagents.com/docs/user-guide/sdk/tools/mcp-transports/)).
- Pochi : permissions Read/Write/Execute auto-approve par défaut ; MCP auto-approve = false dans le store VS Code.
