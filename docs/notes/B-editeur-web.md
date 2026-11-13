# Famille B — éditeurs, applications de bureau, applications web/serveur

Recherche documentaire du 2026-11-12. Grille et portes : `.scratch/harness-selection/criteria.md` appliquées telles quelles (G1 endpoint OpenAI-compatible avec `base_url` arbitraire ; G2 sans compte ni réseau sortant obligatoire, télémétrie désactivable ; G3 licence open-source ; G4 release ou commit dans les 6 mois, soit depuis le 2026-05-12). Aucune recommandation, aucun classement. Chaque affirmation cite un fichier du dépôt (lu dans un clone `--depth 1` le 2026-11-12) ou une URL. « Non vérifié » = je n'ai pas trouvé de source primaire.

Dates de release : relevées dans `https://github.com/<org>/<repo>/releases.atom` le 2026-11-12 (l'API GitHub était limitée en débit).

## Tableau récapitulatif

Verdicts : **oui** / **non** / **nv** (non vérifié) ; « avec réserve » = voir la section du candidat (le détail est dans la section).

| # | Candidat | Nature | Licence | Dernière release | G1 | G2 | G3 | G4 |
|---|---|---|---|---|---|---|---|---|
| 1 | Cline | Extension VS Code/JetBrains + CLI + Desktop + dashboard navigateur | Apache-2.0 | v4.1.26 (2026-10-26) | oui | oui, avec réserve (télémétrie par défaut) | oui | oui |
| 2 | Roo Code | Extension VS Code + CLI `roo` | Apache-2.0 | v3.54.0 (2026-05-15) | oui (CLI : sans base URL) | oui (code lu) | oui | oui littéral (181 j), **projet arrêté le 2026-05-15** |
| 3 | Zoo Code (fork de Roo) | Extension VS Code + CLI | Apache-2.0 | v3.96.0 (2026-11-07) | oui (hérité) | oui, avec réserve (PostHog) | oui | oui |
| 4 | Kilo Code | Extension VS Code, JetBrains, CLI, Cloud Agent | MIT | v7.8.27 (2026-11-05) | oui | oui, avec réserve (PostHog par défaut) | oui | oui |
| 5 | Continue | Extension VS Code/JetBrains + CLI `cn` | Apache-2.0 | v2.1.0-vscode (2026-06-19) | oui | oui (code lu) | oui | oui littéral ; **« no longer actively maintained »**, dernier commit 2026-07-20 |
| 6 | llama.vscode | Extension VS Code | MIT | v0.0.77 (2026-11-05) | oui | oui (code lu) | oui | oui |
| 7 | Void | Éditeur de bureau (fork VS Code) | Apache-2.0 + MIT | « Beta » (2026-05-13) | oui | oui, avec réserve (PostHog) | oui | oui littéral ; **déprécié**, dernier commit 2026-06-02 |
| 8 | Tabby | Serveur auto-hébergé (complétion, chat, Answer Engine) | Apache-2.0 hors `ee/` ; `ee/` sous licence Enterprise | v0.32.0 (2026-01-26) | oui | oui, avec réserve (stats d'usage par défaut) | **partiel** (`ee/` non libre) | oui (commit 2026-06-30) ; dernière release stable : 290 j |
| 9 | OpenHands (Agent Canvas + SDK) | Application web + Agent Server (Docker) | MIT | Canvas v1.39.0 (2026-11-11) ; SDK v1.62.0 | oui | oui, avec réserve (PostHog soumis à consentement) | oui | oui |
| 10 | Pochi (équipe Tabby) | Extension VS Code | Apache-2.0 | 0.82.0 (2026-11-10) | oui | oui, avec réserve (PostHog) | oui | oui |
| 11 | Refact (`JegernOUTT/refact`) | Binaire Rust : daemon + GUI navigateur + LSP + CLI headless | BSD-3-Clause | v8.7.0 (2026-10-31) | oui | oui, avec réserve (code lu) | oui | oui |
| 12 | Zed | Éditeur de bureau natif + agent intégré | GPL-3.0-or-later (crates agent) | v1.29.1-pre (2026-11-11) | oui | oui, avec réserve (télémétrie par défaut, clangd téléchargé) | oui | oui |
| 13 | Open WebUI (+ Open Terminal) | Application web serveur (Docker) ; client de chat | BSD-3 + clause de marque ; Open Terminal : MIT | v0.13.3 (2026-11-08) ; Open Terminal v0.17.7 | oui | oui, avec réserve | **nv (cas limite)** | oui |
| 14 | opencode (mode web/serveur, lecture partielle) | Agent TypeScript : TUI + service + interface web | MIT | v2.2.7 (2026-11-10) | oui | **nv** | oui | oui |

Projets morts ou arrêtés (preuves dans les sections) : **Roo Code** (arrêt déclaré, fork Zoo Code), **Void** (déprécié), **Continue** (« no longer actively maintained », dépôt non archivé), **Refact historique** `smallcloudai/refact` (supplanté par `JegernOUTT/refact`, release/v8.0.4 du 2026-05-15).

---

## 1. Cline (`cline/cline`)

Base des URL : `https://github.com/cline/cline/blob/main/` (commit lu : `50e77bc`, 2026-11-12). Notation : [repo] = fichier du dépôt à cet URL.

**Portes**
- **G1 oui** — provider « OpenAI Compatible » avec `baseUrl` arbitraire, clé optionnelle : [sdk/packages/llms/src/providers/builtins.ts](https://github.com/cline/cline/blob/main/sdk/packages/llms/src/providers/builtins.ts) (`id: "openai-compatible"`, commentaire « Self-hosted endpoints (vLLM, llama.cpp, LM Studio) run without a key », `apiKeyOptional: true`) ; doc : https://github.com/cline/cline/blob/main/docs/provider-config/openai-compatible.mdx. La CLI accepte `cline auth --provider openai-native --apikey … --baseurl https://api.example.com/v1` ([apps/cli/README.md](https://github.com/cline/cline/blob/main/apps/cli/README.md)). Attention : le provider par défaut de la CLI est `cline` (`-P` défaut `cline`, modèle `anthropic/claude-sonnet-5.5`), donc un provider local doit être configuré explicitement.
- **G2 oui, avec réserve** — télémétrie activée par défaut dans l'extension, le Desktop et la CLI, désactivable (`telemetryOptOut: true` dans `~/.cline/data/settings/global-settings.json` pour la CLI) : https://github.com/cline/cline/blob/main/docs/enterprise-solutions/monitoring/telemetry.mdx. La même page dit : « With telemetry off, Cline still contacts its servers for other purposes: to sign you in, to check feature flags, and to run requests on the Cline and ClinePass providers ». Le flux de feature flags passe par PostHog (`https://data.cline.bot`) : [apps/vscode-rollout/src/rollout.ts](https://github.com/cline/cline/blob/main/apps/vscode-rollout/src/rollout.ts) L19 ; la CLI a un module `feature-flags` ([apps/cli/src/utils/feature-flags.ts](https://github.com/cline/cline/blob/main/apps/cli/src/utils/feature-flags.ts)). Pas de compte requis avec un provider local : le CLI échoue avec un message d'auth uniquement pour les providers OAuth ([apps/cli/README.md](https://github.com/cline/cline/blob/main/apps/cli/README.md)). Que les appels de feature flags se coupent entièrement : **non vérifié**. Le changement de `telemetryOptOut` dans la CLI/Desktop n'est pris en compte qu'après redémarrage du hub (même page).
- **G3 oui** — Apache-2.0 : https://github.com/cline/cline/blob/main/LICENSE (SPDX confirmé par l'API GitHub https://api.github.com/repos/cline/cline).
- **G4 oui** — dernier commit lu dans le clone : 2026-11-12 ; dernière release stable `v4.1.26` publiée 2026-10-26 (https://api.github.com/repos/cline/cline/releases/latest) ; nightlies desktop 2026-11-04 (https://github.com/cline/cline/releases.atom).

**Grille**

| Critère | Constat |
|---|---|
| Nature | Famille de produits sur un même cœur « SDK » : extension VS Code, plugin JetBrains, CLI (`npm i -g cline`), app Desktop (macOS/Windows), SDK (`@cline/sdk`), dashboard navigateur « Cline Hub ». Source : https://github.com/cline/cline/blob/main/README.md. Le dépôt a été restructuré (`apps/cli`, `apps/vscode`, `apps/cline-hub`, `sdk/packages/*`) |
| Licence | Apache-2.0 |
| Dernière release / commit | v4.1.26 le 2026-10-26 ; commit 2026-11-12 |
| Tool-calling (modèle local) | Appels **natifs** via le AI SDK (`sdk/packages/llms/src/providers/ai-sdk.ts`) ; je n'ai trouvé aucun format de repli XML dans `sdk/packages/agents` ni `core` (grep « xml » : seulement `web-fetch.ts`, `user-instruction-plugin.ts`, un test). Pas de mention de `--jinja` dans la doc. Appel malformé : `repairMalformedToolCall` répare le JSON tronqué par `jsonrepair` (commentaire : « common with weaker models ») : [ai-sdk.ts](https://github.com/cline/cline/blob/main/sdk/packages/llms/src/providers/ai-sdk.ts) L931-957 ; sinon `agent-runtime.ts` retourne l'erreur « emitted invalid JSON arguments » au modèle (`reason: "invalid_arguments"`) : [agent-runtime.ts](https://github.com/cline/cline/blob/main/sdk/packages/agents/src/agent-runtime.ts) ~L2900. Limite de tentatives consécutives : `--retries` (défaut 3). Règles de routage par modèle activant/désactivant des outils : [model-tool-routing.ts](https://github.com/cline/cline/blob/main/sdk/packages/core/src/extensions/tools/model-tool-routing.ts). Comportement réel avec Qwen2.5-Coder-14B/llama-server : **non vérifié** (aucun test fait) |
| Petits modèles | Doc locale : recommande « Use Compact Prompt » (Settings → Features), contextes réduits, tâches ciblées ; runtimes documentés : Ollama, LM Studio, Atomic Chat (pas llama-server cité nommément) : https://github.com/cline/cline/blob/main/docs/running-models-locally/overview.mdx. Aucune preuve publiée (benchmark) de qualité avec un modèle ≤ 30B trouvée dans le dépôt : **non vérifié** |
| Contexte | Auto-compaction : CLI `--compaction <agentic\|basic\|off>` (défaut `agentic` = résumé par le modèle ; `basic` = troncature locale) ([apps/cli/README.md](https://github.com/cline/cline/blob/main/apps/cli/README.md)). Doc : « With other models, Cline falls back to standard rule-based context truncation » ([docs/features/auto-compact.mdx](https://github.com/cline/cline/blob/main/docs/features/auto-compact.mdx)). Release 4.1.26 : « Auto-compaction no longer runs for models with an unknown context limit » (donc la fenêtre doit être déclarée dans la config du modèle : Context Window size, Max Output Tokens ; doc openai-compatible). Sortie de commande plafonnée, tronquée au milieu (`maxOutputChars` défaut 48 000) : [bash.ts](https://github.com/cline/cline/blob/main/sdk/packages/core/src/extensions/tools/executors/bash.ts) + `output-limits.ts` |
| C++ / CMake | Aucun LSP/clangd intégré trouvé (grep `clangd`, « language server » dans `docs`, `sdk/packages`, `apps` : zéro résultat). Build/tests uniquement via l'outil shell `run_commands` |
| Recherche | Outil `search_codebase` : ripgrep si disponible, sinon regex ([search.ts](https://github.com/cline/cline/blob/main/sdk/packages/core/src/extensions/tools/executors/search.ts)). Pas de repo map ni d'index sémantique trouvés. Outils par défaut : `read_files, search_codebase, run_commands, fetch_web_content, apply_patch, editor, skills, ask_question, submit_and_exit` ([constants.ts](https://github.com/cline/cline/blob/main/sdk/packages/core/src/extensions/tools/constants.ts)) |
| MCP | Client MCP natif. CLI : `cline mcp install <name> -- <cmd>` (stdio), `--transport http <url>`, `--transport sse <url>` ([apps/cli/README.md](https://github.com/cline/cline/blob/main/apps/cli/README.md)). Brancher Serena : stdio faisable en principe, **non testé** |
| Exécution de commandes | Outil `run_commands` (PowerShell géré). Pas de liste d'autorisation fixe : « Cline does not use a fixed allowlist. The model marks each command with a `requires_approval` flag » ([docs/features/auto-approve.mdx](https://github.com/cline/cline/blob/main/docs/features/auto-approve.mdx)). Auto-approve par catégorie (lecture, édition, commandes sûres, toutes commandes, navigateur, MCP). Mode YOLO existant. **Défaut CLI : `cline "prompt"` en one-shot et en stdin = mode yolo** (« runs a single turn in yolo mode »; `--auto-approve false` pour imposer l'approbation) ([apps/cli/README.md](https://github.com/cline/cline/blob/main/apps/cli/README.md)). En mode Plan, garde `command-guard` bloquant les commandes qui éditent des fichiers ([command-guard-extension.ts](https://github.com/cline/cline/blob/main/sdk/packages/core/src/extensions/tools/command-guard-extension.ts)). Pas de sandbox de commandes documentée (le `--data-dir` « enables sandbox mode » ne concerne que l'état local) |
| Édition | Outils `editor` et `apply_patch` (patch). Checkpoints avec `/undo` ([docs/core-workflows/checkpoints.mdx](https://github.com/cline/cline/blob/main/docs/core-workflows/checkpoints.mdx)). Auto-commit : non trouvé (la doc YOLO liste « Commit and push changes » parmi les risques, car le modèle peut l'exécuter via le shell) |
| Contrôle de version | Git via shell et checkpoints ; aucune mention de Subversion (grep `svn`/`subversion` : zéro) |
| Interface | Terminal (TUI, headless), VS Code/JetBrains, Desktop, dashboard web `cline hub dashboard` (port 8787, `HOST=0.0.0.0` possible, `ROOM_SECRET` requis hors loopback) : https://github.com/cline/cline/blob/main/apps/cline-hub/README.md ; `kanban` (port 3484, `--host 0.0.0.0`) : https://github.com/cline/cline/blob/main/docs/kanban/remote-access.mdx. Le dashboard pilote un daemon « hub » **local** qui exécute les sessions sur la machine hôte. Déploiement en conteneur partagé multi-utilisateurs : **non documenté** (aucun Dockerfile dans docs) ; le dashboard est décrit comme dashboard « local hub » ; l'isolation entre utilisateurs n'est pas décrite |
| Scriptable | Oui : `cline --json "…"` (NDJSON : `agent_event` etc.), stdin, `-t` timeout, `-c` cwd ([apps/cli/README.md](https://github.com/cline/cline/blob/main/apps/cli/README.md)). Les appels d'outils sont dans le flux NDJSON (fixtures `apps/cli/src/tests/fixtures/*.json`) ; format exact des événements d'outil : non lu en détail |
| Extension | Rules (`.clinerules/`, `.cline/rules/`, `.cursorrules`, `.windsurfrules`, `AGENTS.md`) : [docs/customization/cline-rules.mdx](https://github.com/cline/cline/blob/main/docs/customization/cline-rules.mdx) ; hooks : [docs/customization/hooks.mdx](https://github.com/cline/cline/blob/main/docs/customization/hooks.mdx) ; skills ; outils personnalisés via le SDK et plugins ; sous-agents et équipes |
| Observabilité | Historique de sessions (`cline history`), journal `cline doctor log` (`CLINE_LOG_PATH`), export OpenTelemetry (docs `enterprise-solutions/monitoring/opentelemetry.mdx`), intégration Langfuse (`sdk/packages/llms/src/services/langfuse-telemetry.ts`) |
| Risques notés | Télémétrie on par défaut (device ID, compte si connecté) ; feature flags PostHog contactés même télémétrie coupée ; mode yolo par défaut en one-shot CLI ; les requêtes vers les providers `cline`/`clinePass` incluent prompts dans la télémétrie (n'affecte pas un provider local) ; modèle décide lui-même `requires_approval` pour les commandes ; produit pivoté (CLI/Desktop/Hub) : doc locale encore centrée sur Ollama/LM Studio |

## 2. Roo Code (`RooCodeInc/Roo-Code`) — extension arrêtée le 2026-05-15

Base des URL : `https://github.com/RooCodeInc/Roo-Code/blob/main/` (dernier commit lu sur `main` : 2026-05-15 14:04 -04:00, « Remove roocode.com web app (#12375) »).

**Preuve d'arrêt** : le README du dépôt dit « The Roo Code Extension was shut down on May 15th. » et renvoie vers ZooCode (fork communautaire) et Cline : https://github.com/RooCodeInc/Roo-Code/blob/main/README.md (section « Disclaimer »). Le CHANGELOG 3.53.0 mentionne « going all-in on Roomote » et « a community team has stepped up » : https://github.com/RooCodeInc/Roo-Code/blob/main/CHANGELOG.md. Le dépôt n'est pas archivé au sens GitHub (non vérifié : l'API GitHub était limitée au moment du contrôle ; la page HTML ne l'indique pas).

**Portes**
- **G1 oui** — provider « OpenAI Compatible » avec Base URL : https://github.com/RooCodeInc/Roo-Code/blob/main/apps/docs/docs/providers/openai-compatible.md. **Limite CLI** : la CLI `roo` ne connaît que 5 providers (`anthropic, openai-native, gemini, openrouter, vercel-ai-gateway`) et n'expose aucune option de base URL : https://github.com/RooCodeInc/Roo-Code/blob/main/apps/cli/src/lib/utils/provider.ts et https://github.com/RooCodeInc/Roo-Code/blob/main/apps/cli/README.md (défaut `--provider openrouter`). Brancher la CLI sur un llama-server : **non vérifié** (aucun chemin documenté).
- **G2 oui (code lu)** — aucune occurrence de `telemetry`/`posthog` (insensible à la casse) dans `src/`, `packages/`, `apps/cli` au commit lu (grep `rg -i telemetry`, `rg -i posthog` hors CHANGELOG, `.md` et locales : seulement d'anciennes notes de version `apps/docs/docs/update-notes/v3.28*.mdx`). Mais `PRIVACY.md` (daté 2025-09-11) décrit encore une télémétrie PostHog activée par défaut avec opt-out : https://github.com/RooCodeInc/Roo-Code/blob/main/PRIVACY.md. Contradiction doc/code non résolue ; **à noter : le code lu ne contient pas la télémétrie**.
- **G3 oui** — Apache-2.0 : https://github.com/RooCodeInc/Roo-Code/blob/main/LICENSE.
- **G4 non (arrêt déclaré)** — dernière release `v3.54.0` = 2026-05-15 (https://github.com/RooCodeInc/Roo-Code/releases/tag/v3.54.0), dernier commit 2026-05-15 ; soit 181 jours avant le 2026-11-12 (littéralement dans la fenêtre de 6 mois de 3 jours, mais l'extension est déclarée arrêtée). Successeur : voir section Zoo Code.

**Grille**

| Critère | Constat |
|---|---|
| Nature | Extension VS Code (+ CLI `roo` qui charge le bundle de l'extension via un shim `vscode`, `apps/cli`) : https://github.com/RooCodeInc/Roo-Code/blob/main/apps/cli/README.md |
| Licence | Apache-2.0 |
| Dernière release / commit | v3.54.0, 2026-05-15 ; CLI `0.1.17` le 2026-03-04 (https://github.com/RooCodeInc/Roo-Code/blob/main/apps/cli/CHANGELOG.md) |
| Tool-calling | **Natif exclusivement**, « there is no XML-based fallback ». Si le modèle ne gère pas les tools, il ne peut pas être utilisé : https://github.com/RooCodeInc/Roo-Code/blob/main/apps/docs/docs/providers/openai-compatible.md. Prompt système : « Use the provider-native tool-calling mechanism. Do not include XML markup » : https://github.com/RooCodeInc/Roo-Code/blob/main/src/core/prompts/sections/tool-use.ts. `--jinja` : non mentionné dans la doc. Appel malformé : `ToolRepetitionDetector.ts`, `validateToolUse.ts` existent ; comportement exact sur JSON malformé : non lu. CLI : `--consecutive-mistake-limit` défaut 10 |
| Petits modèles | La doc locale ne cite que Ollama et LM Studio et prévient que les modèles locaux n'ont pas toutes les fonctions : https://github.com/RooCodeInc/Roo-Code/blob/main/apps/docs/docs/advanced-usage/local-models.md. Preuve ≤ 30B : **non vérifié** |
| Contexte | Type `context-management` dans `packages/types/src/context-management.ts` ; mécanisme de condensation : non lu. Réglages utilisateur Context Window / Max Output Tokens (doc openai-compatible) |
| C++ / CMake | Aucun LSP clangd. Tree-sitter (`src/services/tree-sitter`) pour les définitions de code ; build/tests via `execute_command` |
| Recherche | `search_files` (ripgrep, `src/services/ripgrep`), `list_files`, `codebase_search` (index sémantique) avec embedders `openai-compatible`, `ollama`, `gemini`, `mistral`, `bedrock`, `openrouter`, `vercel-ai-gateway` (`src/services/code-index/embedders/`) et base vectorielle Qdrant (`vector-store/qdrant-client.ts`) → embedding local possible via Ollama/openai-compatible ; Qdrant à héberger |
| MCP | Client avec `stdio`, `sse`, `streamable-http` (`src/services/mcp/McpHub.ts` L6-8 et L76 : « Server type must be 'stdio', 'sse', or 'streamable-http' »). Serena : stdio possible, non testé |
| Exécution de commandes | Outil `execute_command` ; réglages `roo-cline.allowedCommands` (défaut `["git log","git diff","git show"]`), `roo-cline.deniedCommands` (défaut `[]`), `commandExecutionTimeout` (défaut 0 = sans limite) : https://github.com/RooCodeInc/Roo-Code/blob/main/src/package.json L280-306. **CLI : par défaut tout est auto-approuvé** (outils, commandes, navigateur, MCP) ; `--require-approval` pour l'inverser : https://github.com/RooCodeInc/Roo-Code/blob/main/apps/cli/README.md. Pas de sandbox |
| Édition | Outils `apply_diff`, `apply_patch`, `edit_file`, `edit`, `search_replace`, `search_and_replace`, `write_to_file` (`src/core/tools/`). Checkpoints (`src/services/checkpoints`). Pas d'auto-commit trouvé |
| Contrôle de version | Git via checkpoints (shadow) et shell ; Subversion : aucune mention trouvée |
| Interface | Extension VS Code ; CLI TUI/`--print`/`--stdin-prompt-stream`. **Pas de mode serveur web.** Prérequis CLI : Node ≥ 20, macOS Apple Silicon ou Linux x64 (pas Windows natif) |
| Scriptable | Oui : `roo --print --output-format stream-json`, `--stdin-prompt-stream` (NDJSON), `--ephemeral`, `--oneshot` |
| Extension | Modes personnalisés (`.roomodes`), règles (`.roo/`), `AGENTS.md`, skills (`src/services/skills`), slash commands, custom tools (`packages/types/src/custom-tool.ts`), MCP |
| Observabilité | Historique de tâches ; `-d/--debug` côté CLI. Pas d'export de traces trouvé |
| Risques notés | Projet arrêté ; CLI auto-approuve tout par défaut ; CLI sans base URL ; PRIVACY.md en contradiction avec le code |

## 3. Zoo Code (`Zoo-Code-Org/Zoo-Code`) — fork communautaire de Roo Code (ajouté hors liste)

Ajouté parce que le README de Roo Code le désigne comme alternative (https://github.com/RooCodeInc/Roo-Code/blob/main/README.md). Étude plus courte : le code est un fork de Roo Code, donc la plupart des constats de la section 2 s'appliquent ; seuls les écarts vérifiés sont listés.

**Portes**
- **G1 oui (hérité)** — même base de code et mêmes providers que Roo Code. Le CLI de Zoo Code reprend la même liste de 5 providers sans base URL : https://github.com/Zoo-Code-Org/Zoo-Code/blob/main/apps/cli/src/lib/utils/provider.ts. Vérification directe du provider « OpenAI Compatible » dans Zoo : non refaite.
- **G2 oui avec réserve** — télémétrie PostHog (`https://us.i.posthog.com`) active sauf si `telemetrySetting === "disabled"` (`isTelemetryOptedIn` = `telemetrySetting !== "disabled"`) et sauf télémétrie VS Code coupée : https://github.com/Zoo-Code-Org/Zoo-Code/blob/main/packages/types/src/telemetry.ts L24-26, https://github.com/Zoo-Code-Org/Zoo-Code/blob/main/packages/telemetry/src/PostHogTelemetryClient.ts L39, https://github.com/Zoo-Code-Org/Zoo-Code/blob/main/src/extension.ts L185-187. La clé PostHog vient de `process.env.POSTHOG_API_KEY` au build ; si les builds publiés la contiennent : non vérifié. Le package `@roo-code/cloud` (`CloudService`) est toujours importé (`src/core/webview/webviewMessageHandler.ts`) : fonctions cloud optionnelles, comportement hors connexion non vérifié.
- **G3 oui** — Apache-2.0 : https://github.com/Zoo-Code-Org/Zoo-Code/blob/main/LICENSE (README et https://www.zoocode.dev/ le confirment).
- **G4 oui** — dernier commit lu 2026-11-12 ; releases `v3.96.0` 2026-11-07, `v3.94.0` 2026-10-31, `v3.92.0` 2026-10-24 : https://github.com/Zoo-Code-Org/Zoo-Code/releases.atom.

| Critère | Constat |
|---|---|
| Nature | Extension VS Code + CLI (`apps/cli`), fork de Roo Code créé le 2026-04-23 (source secondaire pour la date : résultat de recherche GitHub ; le README du dépôt dit qu'il continue le projet après l'arrêt de l'équipe Roo) : https://github.com/Zoo-Code-Org/Zoo-Code |
| Licence | Apache-2.0 |
| Dernière release | v3.96.0, 2026-11-07 |
| Tool-calling | Même prompt « provider-native tool-calling mechanism. Do not include XML markup » (`src/core/prompts/sections/tool-use.ts`) → natif seulement (hérité de Roo). Reste : non vérifié |
| Petits modèles | **non vérifié** |
| Recherche | Hérité de Roo (`codebase_search` + Qdrant) ; le README annonce « Semble codebase intelligence » (recherche sémantique à la demande sans indexation séparée) — non lu en détail |
| MCP, exécution, édition, interface | Hérités ; le README annonce « per-mode MCP restrictions ». Pas de mode serveur web trouvé |
| Risques notés | Projet de communauté jeune (< 1 an) ; télémétrie PostHog en opt-out ; dépend d'un fork d'un projet arrêté |

## 4. Kilo Code (`Kilo-Org/kilocode`)

Base des URL : `https://github.com/Kilo-Org/kilocode/blob/main/`. Dernier commit lu : 2026-11-12 10:38 +01:00. Le README déclare « `main` is not accepting new features » (les nouveautés vont sur la branche `v2`, qui existe : `git ls-remote` renvoie `refs/heads/v2`). Le dépôt actuel est un fork d'**opencode** (répertoires `packages/opencode`, `.opencode`, `packages/kilo-vscode`, `packages/kilo-jetbrains`, `packages/kilo-telemetry`, `packages/kilo-web-ui`).

**Portes**
- **G1 oui** — « Custom provider » avec Provider API « OpenAI Compatible » + Base URL arbitraire, clé API optionnelle : https://github.com/Kilo-Org/kilocode/blob/main/packages/kilo-docs/pages/ai-providers/openai-compatible.md ; providers locaux documentés : Ollama, LM Studio, Atomic Chat (`packages/kilo-docs/pages/ai-providers/`). La clé `tool_call: true` doit être posée dans `kilo.jsonc` pour que le modèle reçoive des outils : https://github.com/Kilo-Org/kilocode/blob/main/packages/kilo-docs/pages/code-with-ai/agents/custom-models.md L84 et L425. Le README dit « No API keys required to start » (via le Kilo Gateway par défaut) : https://github.com/Kilo-Org/kilocode/blob/main/README.md ; fonctionnement 100 % hors Gateway : **non testé**.
- **G2 oui, avec réserve** — télémétrie PostHog (`https://us.i.posthog.com`, clé en dur dans `packages/kilo-telemetry/src/client.ts`) **activée par défaut** ; coupée par `experimental.openTelemetry: false` dans `kilo.jsonc` ou `KILO_TELEMETRY_LEVEL` différent de `all` : https://github.com/Kilo-Org/kilocode/blob/main/packages/kilo-docs/pages/getting-started/settings/index.md L301 (« Telemetry is enabled by default. Set `experimental.openTelemetry` to `false` … to opt out »), https://github.com/Kilo-Org/kilocode/blob/main/packages/opencode/src/kilocode/cli/setup.ts L99-103, https://github.com/Kilo-Org/kilocode/blob/main/packages/kilo-telemetry/src/telemetry.ts L138. `PRIVACY.md` (daté 2025-03-07) ne mentionne aucune télémétrie, ce qui contredit le code : https://github.com/Kilo-Org/kilocode/blob/main/PRIVACY.md. Autres appels sortants par défaut : téléchargement automatique de serveurs LSP (dont `clangd`), désactivable par `KILO_DISABLE_LSP_DOWNLOAD` (`packages/opencode/src/effect/runtime-flags.ts` L24, `lsp/server.ts`) ; liste de modèles `models.dev` (`kilo models --refresh`, doc cli-reference).
- **G3 oui** — MIT : https://github.com/Kilo-Org/kilocode/blob/main/LICENSE.
- **G4 oui** — release `v7.8.27` 2026-11-05 (pre-release `v7.8.28` 2026-11-07) : https://github.com/Kilo-Org/kilocode/releases.atom ; dernier commit 2026-11-12.

**Grille**

| Critère | Constat |
|---|---|
| Nature | Extension VS Code, plugin JetBrains, CLI (`npm i -g @kilocode/cli`, binaires Windows/macOS/Linux, images `musl`), « Cloud Agent » (service hébergé par Kilo, https://app.kilo.ai/cloud) : https://github.com/Kilo-Org/kilocode/blob/main/README.md |
| Licence | MIT |
| Dernière release / commit | v7.8.27 (2026-11-05) ; commit 2026-11-12 |
| Tool-calling | Appels natifs via le AI SDK (héritage opencode). Pas de repli XML trouvé ; je n'ai pas cherché exhaustivement. Un outil `invalid` renvoie au modèle « The arguments provided to the tool are invalid: … » : https://github.com/Kilo-Org/kilocode/blob/main/packages/opencode/src/tool/invalid.ts. `--jinja` : non mentionné. Comportement avec Qwen2.5-Coder/llama-server : **non vérifié** |
| Petits modèles | Aucune preuve ≤ 30B trouvée dans le dépôt ; la doc `codebase-indexing.md` donne un conseil `-b`/`-ub` pour les serveurs d'embedding llama.cpp (https://github.com/Kilo-Org/kilocode/blob/main/packages/kilo-docs/pages/customize/context/codebase-indexing.md L307-309). Le Desktop (app Kilo) a un onglet avec « Extra Arguments — pass `llama.cpp` flags » (`desktop/settings/ai.md` L87) : **non lu en détail** |
| Contexte | Troncature de sortie d'outil : `MAX_LINES = 2000`, `MAX_BYTES = 50 KiB` (https://github.com/Kilo-Org/kilocode/blob/main/packages/opencode/src/tool/truncate.ts L14-15), réglables via `tool_output` ; clé `compaction` dans la config (`config/config.ts`) : comportement non lu |
| C++ / CMake | **LSP clangd intégré** (`--background-index --clang-tidy`, racine : `compile_commands.json`, `compile_flags.txt` ou `.clangd`) ; téléchargé automatiquement si absent ; `lsp: false` pour tout couper : https://github.com/Kilo-Org/kilocode/blob/main/packages/opencode/src/lsp/server.ts L937-953 + doc `cli.md` « Formatter and LSP Toggles ». Outils `lsp` et `diagnostics` (`packages/opencode/src/tool/lsp.ts`, `diagnostics.ts`). Build/tests via l'outil `shell` |
| Recherche | `grep`, `glob`, `read` (`packages/opencode/src/tool/`) ; index sémantique « codebase indexing » (`packages/kilo-indexing`) avec embedder local possible (Ollama/llama.cpp, doc ci-dessus) ; modèle d'embedding par défaut : non vérifié |
| MCP | Client avec stdio, streamable HTTP et SSE (`packages/opencode/src/mcp/index.ts` L16-18, L292). Serena : stdio possible, non testé |
| Exécution de commandes | Outil `shell`. Modèle de permission `allow/ask/deny` avec motifs de commandes, « last matching rule wins » : https://github.com/Kilo-Org/kilocode/blob/main/packages/kilo-docs/pages/code-with-ai/platforms/cli.md L265-340. **Défauts (code)** : base `"*": "allow"` (donc édition de fichiers autorisée sans demande, sauf JetBrains), `bash` : `"*": "ask"` avec liste blanche de commandes de lecture (grep, rg, jq, …) et de `touch`, `mkdir`, `cp`, `mv`, `tsc`, `tar`… autorisées ; `doom_loop: ask` ; lecture des `.env` : `ask` ; répertoires externes : `ask` : https://github.com/Kilo-Org/kilocode/blob/main/packages/opencode/src/agent/agent.ts L135-160 et `packages/opencode/src/kilocode/agent/index.ts` L55-70. `/auto-approve` bascule tout en allow ; `kilo run --auto` « auto-approves permission prompts unless a rule explicitly denies » (README). Sandbox : un package `packages/kilo-sandbox` existe ; contenu non lu |
| Édition | Outils `edit`, `write`, `apply_patch` ; snapshots (`packages/opencode/src/snapshot`, mécanisme non lu). Pas d'auto-commit trouvé |
| Contrôle de version | Git (snapshots, worktrees, `gh`) ; Subversion : aucune occurrence de `svn`/`subversion` dans `packages/opencode/src` ni dans la doc |
| Interface | TUI ; extension ; **`kilo serve`** serveur HTTP headless (`--hostname` défaut `127.0.0.1`, `--port`, `--cors`) ; `kilo attach <url>` avec mot de passe basic auth (`KILO_SERVER_PASSWORD`) ; `kilo daemon` ; `kilo console` = console web locale **dépréciée** (« deprecated ») ; « Remote Connections » vers l'interface Cloud Agents (exige Kilo Gateway) : https://github.com/Kilo-Org/kilocode/blob/main/packages/kilo-docs/pages/code-with-ai/platforms/cli-reference.md L648-662, L989+, L1069+ ; `cli.md` L664. Page web multi-utilisateurs hébergée par soi-même : **aucune trouvée** (le serveur expose une API ; `packages/kilo-web-ui` est une bibliothèque de composants UI, pas une application) |
| Scriptable | `kilo run "…"` (et `--auto`), `kilo serve` + SDK (`packages/sdk`), ACP (`kilo acp`). Format de sortie JSON de `kilo run` : non lu |
| Extension | Agents personnalisés, skills, plugins (`packages/plugin`), MCP, règles `AGENTS.md`/`.kilocode`, marketplace Kilo |
| Observabilité | Export OpenTelemetry via `OTEL_EXPORTER_OTLP_ENDPOINT` (traces et logs, doc `cli.md` L491-503) ; `kilo export`, `kilo stats`, `kilo debug` |
| Risques notés | Télémétrie PostHog on par défaut et PRIVACY.md muet ; permissions par défaut larges (`"*": "allow"`, édition libre) ; `kilo run --auto` ; téléchargement automatique de LSP ; produit orienté Gateway/cloud ; `main` gelé aux nouveautés (branche `v2` active) |

## 5. Continue (`continuedev/continue`) — « no longer actively maintained »

Base des URL : `https://github.com/continuedev/continue/blob/main/`. Dernier commit lu sur `main` : 2026-07-20 21:00 -07:00, « docs: remove Sign in link (login flow retired) (#13005) ».

**État réel** (le parent demandait de vérifier) : le README dit « The `continuedev/continue` repository is no longer actively maintained and is read-only for all users » et décrit une « Final 2.0.0 Release » de l'extension VS Code, de la CLI et du plugin JetBrains, qui a inclus « removing anonymous telemetry, pulling out authentication » : https://github.com/continuedev/continue/blob/main/README.md. Le dépôt n'est **pas archivé** au sens GitHub (API `archived: false`, `pushed_at: 2026-11-05`, relevé via https://api.github.com/repos/continuedev/continue) — le `pushed_at` récent n'a pas été rattaché à un commit sur `main` (non vérifié). Releases : `v2.1.0-vscode` et `v2.0.0-vscode` le 2026-06-19, `v1.3.40-vscode` le 2026-06-15 : https://github.com/continuedev/continue/releases.atom.

**Portes**
- **G1 oui** — provider `llama.cpp` avec `apiBase: http://localhost:8080` : https://github.com/continuedev/continue/blob/main/docs/customize/model-providers/more/llamacpp.mdx ; provider `openai` avec `apiBase` arbitraire : https://github.com/continuedev/continue/blob/main/docs/customize/deep-dives/model-capabilities.mdx.
- **G2 oui (code lu)** — aucune occurrence de `posthog` dans le code (`core/`, `extensions/`, `gui/`) au commit lu ; seules la doc (`docs/guides/running-continue-without-internet.mdx`, qui parle encore d'« Allow Anonymous Telemetry » et de PostHog) et un fichier de test mentionnent PostHog : la doc est donc en retard sur le code. Le champ `allowAnonymousTelemetry` existe encore dans `core/config/sharedConfig.ts`. La CLI contient un `telemetryService` OpenTelemetry (métriques OTLP via `@opentelemetry/exporter-metrics-otlp-http`) : https://github.com/continuedev/continue/blob/main/extensions/cli/src/telemetry/telemetryService.ts — destination par défaut : **non vérifié** (je n'ai pas lu la condition d'activation). Authentification retirée (README) : pas de compte requis.
- **G3 oui** — Apache-2.0 : https://github.com/continuedev/continue/blob/main/LICENSE.
- **G4 oui littéralement, non au sens « maintenu »** — dernier commit `main` 2026-07-20 (115 jours), dernière release 2026-06-19 ; le README annonce l'absence de maintenance. À arbitrer par le parent.

**Grille**

| Critère | Constat |
|---|---|
| Nature | Extension VS Code, plugin JetBrains (« We recommend using the Continue CLI instead »), CLI `cn` (npm `@continuedev/cli`) : README ci-dessus |
| Licence | Apache-2.0 |
| Dernière release / commit | 2026-06-19 (v2.1.0-vscode) ; commit 2026-07-20 |
| Tool-calling | Natif **seulement si le modèle est reconnu ou déclaré** : `modelSupportsNativeTools` lit `capabilities` du modèle puis une table par provider (`core/llm/toolSupport.ts` L513-523). Pour `openai`, la table renvoie vrai pour `gpt-4+`, `o1+`, `codex`, `exaone`, `gpt-oss`… (L19-45 et suivantes). Le provider `llama.cpp` : aucune entrée trouvée (grep `llama.cpp` dans ce fichier : aucun résultat) → pas d'outils natifs par défaut. Sinon **format de repli** : blocs ` ```tool ` avec `TOOL_NAME:` / `BEGIN_ARG:` / `END_ARG` (framework `SystemMessageToolCodeblocksFramework`, commentaire « Poor models are really bad at following instructions, alternate starts allowed ») : https://github.com/continuedev/continue/blob/main/core/tools/systemMessageTools/toolCodeblocks/index.ts ; sélection dans https://github.com/continuedev/continue/blob/main/gui/src/redux/thunks/streamNormalInput.ts L112-119 ; réglage `experimental.onlyUseSystemMessageTools` (force le repli). Pour forcer le natif : `capabilities: [tool_use]` dans `config.yaml` (doc model-capabilities ; « You cannot override autodetection - you can only add capabilities »). Appel malformé : non lu. Comportement avec Qwen2.5-Coder-14B + llama-server : **non vérifié** |
| Petits modèles | La doc `model-capabilities.mdx` prévient que sans capacité `tool_use` le mode Agent est indisponible. Preuve publiée ≤ 30B : **non vérifié** |
| Contexte | Non investigué en détail pour le mode agent (extension) ; la CLI a des services de session ; **non vérifié** |
| C++ / CMake | Aucun clangd géré par l'agent trouvé (non cherché exhaustivement) ; l'extension s'appuie sur l'IDE |
| Recherche | Pipelines de retrieval (`core/context/retrieval/`, avec ou sans reranker) et `repoMapRequest.ts` (liste de modèles, `llama3.1` y figure). Modèle d'embedding et possibilité locale : **non vérifié** |
| MCP | Client avec stdio, SSE, streamable HTTP et WebSocket (`core/context/mcp/MCPConnection.ts` L11-16) : https://github.com/continuedev/continue/blob/main/core/context/mcp/MCPConnection.ts ; doc : https://github.com/continuedev/continue/blob/main/docs/customize/mcp-tools.mdx. Serena : stdio possible, non testé |
| Exécution de commandes | CLI : outil `Bash` ; permissions `allow` / `ask` / `exclude` par outil ; défauts : outils de lecture `allow`, `Edit`/`MultiEdit`/`Write`/`Bash` = `ask` ; **en mode headless, les outils `ask` sont exclus** ; motifs glob (`Bash(npm install*)`) ; `--allow "*"` pour tout autoriser ; `permissions.yaml` persistant : https://github.com/continuedev/continue/blob/main/docs/cli/tool-permissions.mdx. Pas de sandbox trouvé |
| Édition | Outils `Edit`, `MultiEdit`, `Write` ; commit : la CLI ajoute une signature de commit aux messages générés (`CONTINUE_CLI_DISABLE_COMMIT_SIGNATURE`) : https://github.com/continuedev/continue/blob/main/extensions/cli/README.md |
| Contrôle de version | Git (diff via `/diff` du serveur) ; Subversion non cherché → **non vérifié** |
| Interface | Extension IDE ; CLI TUI ; headless `cn -p` (`--format json`, `--silent`) ; **`cn serve`** : serveur HTTP Express avec routes `GET /state`, `POST /message`, `POST /permission`, `POST /pause`, `GET /diff`, `POST /exit` (https://github.com/continuedev/continue/blob/main/extensions/cli/src/commands/serve.ts L215-340) — API de pilotage d'un agent, **sans page web servie** (non trouvée dans ce fichier) ; mode `cn remote` lié à l'authentification supprimée |
| Scriptable | Oui : `cn -p "…" --format json`, stdin ; `cn ls --json` |
| Extension | Règles (`.continue/rules`), prompts, agents de config (`config.yaml`), MCP, skills (`skills/`) |
| Observabilité | Sessions (`cn ls`), télémétrie OTLP côté CLI (non lue) |
| Risques notés | Projet non maintenu (README) ; doc contredit le code sur la télémétrie ; tool-calling natif non activé par défaut pour `llama.cpp` (repli textuel) |

## 6. llama.vscode (`ggml-org/llama.vscode`)

Base des URL : `https://github.com/ggml-org/llama.vscode/blob/master/` (branche par défaut non relevée ; clone `--depth 1` de HEAD : commit `v0.0.77`, 2026-11-06 00:33 +02:00).

**Portes**
- **G1 oui** — réglages `endpoint_chat`, `endpoint_tools`, `endpoint_embeddings`, clés `api_key_chat`, `api_key_tools`… dans `src/configuration.ts` (défaut `127.0.0.1:8011`) ; l'agent exige un « tools model » (message d'erreur si absent ou si `endpoint_tools` n'est pas défini, `src/llama-agent.ts` ~L900). README : « Could work with external models (for example from OpenRouter) » : https://github.com/ggml-org/llama.vscode/blob/master/README.md.
- **G2 oui (code lu)** — aucune occurrence de `telemetry`, `posthog`, `analytics`, `sentry` dans `src/` ni `package.json` (grep). Appels sortants volontaires : installation automatique de llama.cpp au démarrage (« Now automatic on starting llama-vscode » : script officiel `llama.app`, brew ou winget), recherche/téléchargement de modèles Hugging Face, bot Telegram optionnel (`src/telegram-bot.ts`, `node-telegram-bot-api`), outil `web_browser` (http(s) seulement, adresses privées/loopback bloquées : `src/web-browser.ts` L22). Pas de compte.
- **G3 oui** — MIT : https://github.com/ggml-org/llama.vscode/blob/master/LICENSE.
- **G4 oui** — releases `v0.0.77` 2026-11-05, `v0.0.76` 2026-11-01, `v0.0.75` 2026-11-01 : https://github.com/ggml-org/llama.vscode/releases.atom.

**Grille**

| Critère | Constat |
|---|---|
| Nature | Extension VS Code (complétion FIM + chat + « Llama Agent »), disponible aussi sur Open VSX : README |
| Licence | MIT |
| Dernière release | v0.0.77, 2026-11-05 |
| Tool-calling | **Natif** : lit `choices[0].message.tool_calls` de `/v1/chat/completions` (`src/llama-agent.ts` L1218-1235). La commande de lancement prédéfinie du « tools model » inclut `--jinja` : `llama serve -hf MODEL --jinja -c 0 -ub 1024 -b 1024 --cache-reuse 256 …` (https://github.com/ggml-org/llama.vscode/blob/master/src/constants.ts L98). Aucun repli textuel trouvé. Appel inconnu : « Tool not found » renvoyé comme sortie d'outil (L1226). Limite de boucles : `tools_max_iterations` |
| Petits modèles | README : « Works with local models - gpt-oss 20B is the best choice for now » ; les paramètres FIM recommandés vont de 1,5B à 30B (Qwen2.5-Coder FIM) ; aucun benchmark chiffré trouvé |
| Contexte | `-c 0` côté serveur ; module `language-model-token-limits.ts` (marge de sécurité, max output tokens bornés) ; compaction : non trouvée (non vérifié) |
| C++ / CMake | Outils `get_errors` (diagnostics VS Code, donc clangd si l'extension C/C++ est installée) et `rename_symbol` : s'appuient sur VS Code, pas de LSP propre. Build via `run_terminal_command` |
| Recherche | Outils `search_source`, `regex_search`, `read_file`, `list_directory` (`src/tools.ts`) ; embeddings optionnels (`endpoint_embeddings`, chunks) ; modèle d'embedding par défaut : non vérifié |
| MCP | « MCP tools selection for the agent (from VS Code installed MCP Servers) » : le client MCP est celui de VS Code (transports = ceux de VS Code, non vérifié) : README |
| Exécution de commandes | `run_terminal_command`. Réglage `llama-vscode.tools_permissions_mode` : `Ask` (défaut dans `src/configuration.ts` L92), `AllowAll` (« YOLO »), `AutoAskIfUnsure`, `AutoDenyIfUnsure` (commandes sûres autorisées, dangereuses refusées, le reste jugé par le LLM) : https://github.com/ggml-org/llama.vscode/blob/master/package.json L1501-1509. Délai de permission `tools_permission_timeout` 600 s. Pas de sandbox |
| Édition | Outils `edit_file`, `multi_edit_file`, `delete_file`, `get_diff` ; pas d'auto-commit trouvé |
| Contrôle de version | `src/git.ts` + outil `get_diff` ; Subversion non cherché |
| Interface | VS Code uniquement (vue Explorer + deep links `vscode://…`) ; accès « from phone via a Telegram bot ». **Aucun mode serveur, CLI ni web** (dépend de l'API `vscode`) |
| Scriptable | Non trouvé (deep link `vscode://ggml-org.llama-vscode?view=agent&prompt=…` ouvre VS Code) |
| Extension | 22 enregistrements `toolsFunc.set` dans `src/tools.ts` (le README annonce « 9 internal tools », donc il est en retard) dont `custom_tool`, `custom_eval_tool` (JavaScript), `delegate_task`, `create_agent`, `search_tools` ; hooks (`src/hooks.ts`, événement `preToolUse`) ; agents/envs exportables ; fichiers `.md` de contexte |
| Observabilité | Journal dans l'UI (`tools_log_calls`) ; autre : non vérifié |
| Risques notés | Dépendance à VS Code ; v0.0.x ; installation automatique de binaires (llama.cpp) au démarrage ; mode `AllowAll` disponible |

## 7. Void (`voideditor/void`) — déprécié

Base des URL : `https://github.com/voideditor/void/blob/main/`. Dernier commit lu : 2026-06-02 15:03 -07:00, message « all repos ».

**Preuve** : le README dit « Void is deprecated and no longer accepting contributions », renvoie vers `voideditor/void-forks` pour « newer Void forks » et vers les Releases pour télécharger « an old version » : https://github.com/voideditor/void/blob/main/README.md. Dernières entrées de releases : « Beta » 2026-05-13, `v1.2.4` 2025-04-16 : https://github.com/voideditor/void/releases.atom. Je n'ai pas examiné les forks listés (non vérifié).

**Portes**
- **G1 oui** — provider `openAICompatible` : « Use any provider that's OpenAI-compatible (use this for llama.cpp and more) » : https://github.com/voideditor/void/blob/main/src/vs/workbench/contrib/void/common/voidSettingsTypes.ts L123 ; endpoints configurables pour Ollama, vLLM, LM Studio, LiteLLM.
- **G2 oui avec réserve** — télémétrie PostHog (`posthog-node`) dans le processus principal, avec clé d'opt-out `void.app.optOutAll` : https://github.com/voideditor/void/blob/main/src/vs/workbench/contrib/void/electron-main/metricsMainService.ts L11-16, L126, L150 ; https://github.com/voideditor/void/blob/main/src/vs/workbench/contrib/void/common/storageKeys.ts L23. Le README dit « Void sends messages directly to providers without retaining your data ». Host PostHog et événements envoyés : non lus (non vérifié). Hérite aussi de la télémétrie de VS Code (non vérifié pour ce fork ; `product.json` non lu).
- **G3 oui** — Apache-2.0 pour les ajouts de Void (`LICENSE.txt`), MIT pour la base VS Code (`LICENSE-VS-Code.txt`) : https://github.com/voideditor/void/blob/main/LICENSE-VS-Code.txt.
- **G4 non (déprécié)** — dernier commit 2026-06-02 (163 jours, littéralement dans la fenêtre), dernière release « Beta » 2026-05-13 ; projet déclaré déprécié et fermé aux contributions.

**Grille**

| Critère | Constat |
|---|---|
| Nature | Éditeur de bureau (fork de VS Code, Electron), pas une extension : README |
| Licence | Apache-2.0 (ajouts) + MIT (VS Code) |
| Dernière release / commit | « Beta » 2026-05-13 ; commit 2026-06-02 |
| Tool-calling | Format dépendant du modèle : `specialToolFormat` ∈ `openai-style`, `anthropic-style`, `gemini-style` ; « null means "can't call tools by default", and asks the LLM to output XML in agent mode » : https://github.com/voideditor/void/blob/main/src/vs/workbench/contrib/void/common/modelCapabilities.ts L170. Pour Qwen2.5-Coder, l'entrée `qwen2.5coder` (via détection par nom, L437) ne définit **pas** `specialToolFormat` (L349-355) → repli **XML** dans le prompt (`systemToolsXMLPrompt`, `common/prompt/prompts.ts` L380-411). `--jinja` : non mentionné. Appel malformé : non lu |
| Petits modèles | Entrées dédiées pour modèles open source : `qwen2.5coder` (FIM oui, contextWindow 32 000, reservedOutputTokenSpace 4 096, pas de reasoning), `qwen3`, `qwq`, `llama3.x`, `qwen2.5-coder:7b/3b/1.5b` (Ollama) : modelCapabilities.ts. Preuve de qualité en agent avec ≤ 30B : **non vérifié** |
| Contexte | Fenêtre et sortie réservée déclarées par modèle (ci-dessus) ; compaction : non vérifié |
| C++ / CMake | Hérite de VS Code (extensions de langage) ; pas de LSP géré par l'agent (non cherché exhaustivement) |
| Recherche | Outils d'agent dans `contrib/void` ; index sémantique : non vérifié |
| MCP | Client MCP avec `StdioClientTransport`, `StreamableHTTPClientTransport`, `SSEClientTransport` : https://github.com/voideditor/void/blob/main/src/vs/workbench/contrib/void/electron-main/mcpChannel.ts L13-15 |
| Exécution de commandes | non vérifié (outils de terminal et réglages d'approbation non lus) |
| Édition | `EditCodeService` : diffs affichés pendant le streaming ; checkpoints (README « checkpoint and visualize changes ») |
| Contrôle de version | non vérifié |
| Interface | Application de bureau uniquement ; aucun mode serveur ou web documenté dans le README. Le dépôt contient les répertoires `remote/` et `cli/` hérités de VS Code, leur usage pour servir Void : non vérifié |
| Scriptable | Non trouvé |
| Extension | `.voidrules` à la racine du dépôt (règles du projet) ; MCP |
| Observabilité | non vérifié |
| Risques notés | Projet déprécié ; télémétrie PostHog ; repli XML pour Qwen2.5-Coder ; éditeur à installer sur chaque poste |

## 8. Tabby (`TabbyML/tabby`)

Base des URL : `https://github.com/TabbyML/tabby/blob/main/`. Dernier commit lu : 2026-06-30 09:53 -07:00, « Revert "feat: add Avian as a model provider (#4448)" (#4510) ».

**Constat de nature** : Tabby est un serveur d'assistant de complétion et de chat (« self-hosted AI coding assistant … alternative to GitHub Copilot », README : https://github.com/TabbyML/tabby/blob/main/README.md) avec une interface web (« Answer Engine », admin, code browser). Je n'ai trouvé **aucune boucle d'agent avec appels d'outils** dans le dépôt : aucune occurrence de `tool_calls`/`function_call`/`tools` dans `crates/tabby-inference` et `crates/http-api-bindings` ; aucun client MCP (grep `mcp` : seulement la feuille de route et des bundles JS minifiés). La feuille de route cite « Agentic task automation — Model / MCP Integration with RooCode » : https://github.com/TabbyML/tabby/blob/main/website/docs/roadmap.mdx L19-20. L'agent de l'équipe est un autre projet, `TabbyML/pochi` (voir section dédiée si ajoutée plus bas). Le README annonce ces nouveautés d'agent hors du dépôt Tabby (« Pochi tasks »).

**Portes**
- **G1 oui (pour le chat et la complétion)** — `[model.chat.http] kind = "openai/chat"` avec `api_endpoint` ; doc llama.cpp : https://github.com/TabbyML/tabby/blob/main/website/docs/references/models-http-api/llama.cpp.mdx (chat OpenAI-compatible, complétion `llama.cpp/completion`, embeddings `llama.cpp/embedding`).
- **G2 oui avec réserve** — « Tabby collects usage stats by default » (contenu de `HealthState` : modèle, chat_model, device, arch, cpu_info, version…) ; désactivé par `TABBY_DISABLE_USAGE_COLLECTION=1` : https://github.com/TabbyML/tabby/blob/main/website/docs/administration/usage-collection.md et https://github.com/TabbyML/tabby/blob/main/crates/tabby-common/src/usage.rs L76. Les extensions IDE ont aussi une collecte anonyme (opt-out dans les réglages) : https://github.com/TabbyML/tabby/blob/main/website/docs/extensions/configurations.md L49-51. Compte : l'administration web demande la création d'un compte admin (comportement non vérifié dans le code).
- **G3 non pour une partie du dépôt (à arbitrer)** — `LICENSE` : le contenu hors `ee/` est Apache-2.0, mais tout `ee/` est sous une « Tabby Enterprise license » : usage en production réservé à qui a accepté les Tabby Subscription Terms et dispose d'« un Enterprise license pour le bon nombre de sièges », copie/redistribution interdites : https://github.com/TabbyML/tabby/blob/main/LICENSE et https://github.com/TabbyML/tabby/blob/main/ee/LICENSE. Le répertoire `ee/` contient `tabby-webserver`, `tabby-ui`, `tabby-schema`, `tabby-db` : c'est-à-dire l'interface web et le serveur de comptes. Si le binaire `tabby serve` publié embarque `ee/` : non vérifié (la présence de `ee/tabby-webserver/ui/_next/…` dans l'arbre le suggère).
- **G4 oui** — dernier commit 2026-06-30 (135 jours) ; dernière release stable `v0.32.0` 2026-01-26 (derniers tags : `v0.33.0-dev.0` 2026-01-29, `nightly` 2026-03-02) : https://github.com/TabbyML/tabby/releases.atom. La dernière release stable date de 290 jours.

**Grille** (abrégée : Tabby ne fait pas d'agent de code)

| Critère | Constat |
|---|---|
| Nature | Serveur auto-hébergé (Rust ; Docker `tabbyml/tabby`) : complétion de code, chat, « Answer Engine », indexation de dépôts, plugins IDE (VS Code, JetBrains, Vim) |
| Licence | Apache-2.0 hors `ee/` ; licence Enterprise pour `ee/` |
| Dernière release / commit | v0.32.0 (2026-01-26) ; commit 2026-06-30 |
| Tool-calling | **Non applicable / non trouvé** (pas d'appels d'outils côté serveur) |
| Petits modèles | Le démarrage documenté utilise `StarCoder-1B` + chat `Qwen2-1.5B-Instruct` (README). Pas d'évaluation d'agent |
| Contexte | Contexte de complétion enrichi (snippets locaux, LSP, dépôt indexé) : README ; compaction : non applicable |
| C++ / CMake | Les clients utilisent des déclarations LSP locales pour la complétion (README, entrée 04/19/2024) ; pas de build/test |
| Recherche | Index de dépôts (code browser, Answer Engine) avec modèle d'embedding configurable (`[model.embedding.http] kind = "llama.cpp/embedding"`), local possible |
| MCP | Aucun client MCP trouvé |
| Exécution de commandes | Aucune |
| Édition | Complétion inline et « edit via chat command » dans l'IDE (vscode CHANGELOG) ; pas d'agent |
| Contrôle de version | Intégrations GitHub/GitLab (issues, MR comme contexte) ; Subversion : non vérifié |
| Interface | **Page web servie par le serveur** (chat, Answer Engine, admin, code browser), déployable en Docker (`docker run … tabbyml/tabby serve …`), multi-utilisateurs avec comptes (LDAP, SSO dans la liste des nouveautés du README) ; c'est la partie `ee/` sous licence Enterprise |
| Scriptable | API HTTP (« OpenAPI interface » : README) ; pas de rejeu d'outils |
| Extension | Documentation propre (REST), dépôts de contexte ; pas de règles `rules/*.md` au sens agent |
| Observabilité | Rapports d'usage et Activities dans l'UI admin (README : « Reports », « Activities ») |
| Risques notés | Pas d'agent ; interface web sous licence Enterprise ; collecte d'usage on par défaut ; cadence de releases stables lente |

## 9. OpenHands (`OpenHands/OpenHands`, désormais « Agent Canvas ») + moteur `OpenHands/software-agent-sdk`

**Changement structurel à noter** : le dépôt `OpenHands/OpenHands` est aujourd'hui le frontend **« Agent Canvas »** (« The self-hosted developer control center for coding agents and automations »), qui pilote un **Agent Server** hébergé dans un autre dépôt, `OpenHands/software-agent-sdk` : https://github.com/OpenHands/OpenHands/blob/main/README.md et https://github.com/OpenHands/OpenHands/blob/main/docs/architecture.md (« Agent Canvas is not responsible for: Executing agent actions directly … Providing the sandbox »). L'ancienne GUI locale (`openhands serve`) est marquée « deprecated legacy local GUI … no longer actively maintained » : https://github.com/OpenHands/docs/blob/main/openhands/usage/run-openhands/local-setup.mdx. Les constats sur l'agent (tool-calling, outils, permissions) viennent donc du dépôt SDK.

Dernier commit lu `OpenHands/OpenHands` : 2026-11-12 19:29 +07:00 ; dernier commit `software-agent-sdk` : non relevé (clone de HEAD fait, date non lue).

**Portes**
- **G1 oui** — modèle `openai/<served-model-id>` + base URL joignable depuis le **backend**, profils LLM et « Provider Connections » (clé API et base URL optionnelle) : https://github.com/OpenHands/docs/blob/main/openhands/usage/agent-canvas/model-configuration.mdx (section « Local OpenAI-Compatible Server ») ; guide serveurs locaux LM Studio, Ollama, vLLM, SGLang : https://github.com/OpenHands/docs/blob/main/openhands/usage/llms/local-llms.mdx. La couche LLM utilise `litellm` (imports `from litellm import …` dans `openhands-sdk/openhands/sdk/llm/mixins/non_native_fc.py`). llama-server n'est pas cité nommément dans la doc ; l'API OpenAI-compatible suffit en principe (non testé).
- **G2 oui avec réserve (frontend)** — Canvas contient un client PostHog (`posthog-js`), clé et hôte dans `config/defaults.json` (`https://us.i.posthog.com`) ; la capture est **soumise à consentement** (`TelemetryConsentBanner`, `opt_out_capturing_by_default`), et désactivable par `AGENT_CANVAS_DISABLE_TELEMETRY=1` ou `VITE_DO_NOT_TRACK=1` : https://github.com/OpenHands/OpenHands/blob/main/src/services/telemetry.ts L25-30, L430-460 ; https://github.com/OpenHands/OpenHands/blob/main/src/components/features/analytics/telemetry-consent-banner.tsx. Le commentaire du code mentionne aussi une capture immédiate « for install tracking » (`enableCapturing = true`) : portée exacte non vérifiée. Côté agent-server : l'exporteur PostHog est une dépendance **optionnelle** (`posthog = [...]` dans `openhands-agent-server/pyproject.toml` L24-28 : « the core server … must be able to run without a vendor analytics SDK »). Pas de compte requis en local (clé de session générée localement : README Canvas).
- **G3 oui** — MIT : https://github.com/OpenHands/OpenHands/blob/main/LICENSE (et SDK : https://github.com/OpenHands/software-agent-sdk/blob/main/LICENSE, MIT). Le répertoire `enterprise` existe dans le dépôt de documentation, pas examiné pour le code.
- **G4 oui** — Canvas `v1.39.0` le 2026-11-11, `v1.38.0` le 2026-11-10, `v1.37.0` le 2026-11-06 : https://github.com/OpenHands/OpenHands/releases.atom ; SDK `v1.62.0` le 2026-11-11, `v1.61.0` le 2026-11-10 : https://github.com/OpenHands/software-agent-sdk/releases.atom.

**Grille**

| Critère | Constat |
|---|---|
| Nature | **Application web** (frontend React « Agent Canvas », paquet npm `@openhands/agent-canvas`, image `ghcr.io/openhands/agent-canvas`, app Electron `electron/`) + **Agent Server** REST (SDK Python) + serveur d'automatisations optionnel. Peut aussi lancer des agents tiers via ACP (Claude Code, Codex, Gemini, Pi, OpenCode) : README |
| Licence | MIT |
| Dernière release | Canvas v1.39.0 (2026-11-11) ; SDK v1.62.0 (2026-11-11) |
| Tool-calling | `native_tool_calling` **vrai par défaut** (`LLM.native_tool_calling: bool = Field(default=True)`) ; si faux, **repli « prompt-mocked »** : les outils sont décrits dans le prompt et reconvertis (`NonNativeToolCallingMixin`, `fn_call_converter`, mots d'arrêt) : https://github.com/OpenHands/software-agent-sdk/blob/main/openhands-sdk/openhands/sdk/llm/llm.py L555-559, L1444-1475 ; https://github.com/OpenHands/software-agent-sdk/blob/main/openhands-sdk/openhands/sdk/llm/mixins/non_native_fc.py. `--jinja` : non mentionné (doc centrée LM Studio). Appel malformé : converti en `AgentErrorEvent` « so the agent can correct itself » (`openhands-sdk/openhands/sdk/agent/agent.py` L1383, L1613-1616) |
| Petits modèles | Doc officielle : « Local LLMs can have limited functionality; use a capable model and GPU-backed server » ; mise à jour « 2026/05/21: We now recommend Qwen3.6-35B-A3B as the first local model to try » (35B, hors seuil ≤ 30B ; MoE « A3B » = 3B actifs d'après le nom, non détaillé dans la doc) ; contexte conseillé : « at least 22000 … 32768 (recommended) » : https://github.com/OpenHands/docs/blob/main/openhands/usage/llms/local-llms.mdx. Aucun résultat de benchmark ≤ 30B lu |
| Contexte | `LLMSummarizingCondenser` : `max_size = 240` événements par défaut, `keep_first = 2`, `max_tokens` optionnel, LLM de résumé indépendant (`openhands-sdk/openhands/sdk/context/condenser/llm_summarizing_condenser.py` L54-70) ; sortie de commande plafonnée à 30 000 caractères (`MAX_CMD_OUTPUT_SIZE`, `openhands-tools/openhands/tools/terminal/constants.py` L18). Seuil 240 événements : l'adaptation à une fenêtre de 32 k n'est pas documentée (non vérifié) |
| C++ / CMake | Aucun LSP/clangd trouvé dans `openhands-tools` (outils : `terminal`, `file_editor`, `apply_patch`, `glob`, `grep`, `browser_use`, `task_tracker`, `delegate`, `planning_file_editor`, …). Build via `terminal`. Un éditeur OpenVSCode embarqué est servi sous `/vscode` (SELF_HOSTING.md) |
| Recherche | `grep`, `glob` (pas de repo map ni d'index sémantique trouvés) |
| MCP | Client MCP via `fastmcp` ; transports **SSE, Streamable HTTP, stdio** : https://github.com/OpenHands/docs/blob/main/openhands/usage/settings/mcp-settings.mdx L17-19 ; OAuth pour serveurs distants (`sdk/guides/mcp.mdx`). Serena : aucune mention ; stdio possible, non testé |
| Exécution de commandes | Outil `terminal`. **Politique de confirmation par défaut : `NeverConfirm`** (agent-server `models.py` L190 et `conversation/state.py` L180) ; alternatives `AlwaysConfirm`, `ConfirmRisky` (analyse de risque) : https://github.com/OpenHands/software-agent-sdk/blob/main/openhands-sdk/openhands/sdk/security/confirmation_policy.py. **Sandbox** : option 1 « sans sandbox » (avertissement : « the agent will have full access to your filesystem ») ; option 2 stack complète dans un conteneur Docker (projets montés sur `/projects`, utilisateur uid 10001) ; option 3 `OH_CONVERSATION_RUNTIME=docker` = un conteneur par conversation : README Canvas. Liste d'autorisation de commandes : non trouvée |
| Édition | Outils `file_editor`, `apply_patch`, `planning_file_editor` ; auto-commit : non vérifié |
| Contrôle de version | Intégrations Git (module `openhands/sdk/git`, GitHub/GitLab/Linear/Slack dans les automatisations) ; Subversion : non vérifié |
| Interface | **Page web** (`/canvas` en Docker, `/` en npm), WebSocket, ingress unique ; déploiement serveur documenté (VM, nginx + TLS, `--public`, `LOCAL_BACKEND_API_KEY` ⇒ écran de saisie de clé) : https://github.com/OpenHands/OpenHands/blob/main/docs/SELF_HOSTING.md. Les listeners locaux sont en loopback ; `--host 0.0.0.0` possible. Plusieurs backends interchangeables dans l'UI. **Un seul secret partagé** (`LOCAL_BACKEND_API_KEY`) ; gestion multi-utilisateurs avec comptes : non trouvée pour la version auto-hébergée (non vérifié) |
| Scriptable | Agent Server REST + SDK Python (`openhands-sdk`), conversations lancées par API, événements et appels d'outils exposés (`LOG_ALL_EVENTS`) ; format exact : non lu |
| Extension | Skills, hooks (`openhands/sdk/hooks`), plugins (`plugin`), sous-agents (`delegate`, `subagent`), `AGENTS.md`, profils d'agents et de LLM ; automatisations planifiées/webhooks |
| Observabilité | Module `openhands/sdk/observability` ; événements persistés par conversation ; guide `sdk/guides/observability.mdx` : non lu |
| Risques notés | `NeverConfirm` par défaut ; l'option 1 donne accès complet au disque hôte ; clé unique partagée en mode public ; avertissement SELF_HOSTING.md sur l'origine partagée de l'éditeur OpenVSCode (issue #16492 : le JS de l'origine peut lire les clés de session de tous les backends enregistrés dans le navigateur) ; télémétrie PostHog du frontend sous consentement ; dépôt scindé (UI / SDK) donc deux versions à suivre ; repli non natif en prompt, comportement avec Qwen2.5-Coder non vérifié |

## 10. Pochi (`TabbyML/pochi`) — agent de l'équipe Tabby (ajouté hors liste)

Ajouté parce que le README de Tabby renvoie vers lui pour les fonctions d'agent (https://github.com/TabbyML/tabby/blob/main/README.md). Dépôt : https://github.com/TabbyML/pochi. Dernier commit lu : 2026-11-12 13:07 UTC. Étude partielle.

- **G1 oui** — provider « OpenAI Compatible » : fichier de réglages avec `providers.<id>.baseURL`, `apiKey`, `models.<id>.contextWindow/maxTokens` (défauts **10k** de contexte et **4096** de sortie si non précisés) : https://github.com/TabbyML/pochi/blob/main/packages/docs/content/docs/models.mdx. « Pochi leverages the AI SDK to support various LLM providers and can run local models ».
- **G2 oui (code lu, avec réserve)** — README : « No account is required to use the BYOK model » (https://github.com/TabbyML/pochi/blob/main/README.md). Client PostHog (`posthog-node`, hôte `https://us.i.posthog.com`, clé en dur) dans `packages/vscode/src/lib/posthog.ts` ; `capture()` ne fait rien tant qu'aucun `distinctId` n'a été fixé par `identify()` (c'est-à-dire sans connexion à un compte) : https://github.com/TabbyML/pochi/blob/main/packages/vscode/src/lib/posthog.ts. Le lien entre `identify()` et la connexion n'a pas été tracé (non vérifié). Complétion « Tab » : modèle interne de Pochi ; son endpoint par défaut est non vérifié.
- **G3 oui** — Apache-2.0 : https://github.com/TabbyML/pochi/blob/main/LICENSE (répertoire `private/` présent à la racine, non examiné).
- **G4 oui** — `pochi-vscode@0.82.0` 2026-11-10, `0.81.1` 2026-11-09, `0.81.0` 2026-11-04 : https://github.com/TabbyML/pochi/releases.atom.

| Critère | Constat |
|---|---|
| Nature | Extension VS Code / Open VSX (`packages/vscode`, webview `packages/vscode-webui`) ; paquets `vendor-codex`, `vendor-gemini-cli`, `vendor-github-copilot`, `vendor-qwen-code`, `vendor-tabby` (intégrations de fournisseurs). Pas de CLI ni de serveur trouvé dans `packages/` (non cherché exhaustivement) |
| Licence | Apache-2.0 |
| Tool-calling | Utilise le AI SDK ; format natif vs repli : **non vérifié** |
| Petits modèles | **non vérifié** |
| Contexte | « Auto Compact » (compactage dans la tâche courante ou nouvelle tâche avec résumé) : README et `packages/docs/content/docs/auto-compact.mdx` |
| MCP | stdio (« Local MCP Servers (Stdio Transport) »), HTTP distant, SSE : https://github.com/TabbyML/pochi/blob/main/packages/docs/content/docs/mcp.mdx |
| Exécution de commandes | **« By default, all permissions in Pochi are enabled »** (Read, Write, Execute, Use MCP, Retry) ; réglages d'auto-approbation modifiables : https://github.com/TabbyML/pochi/blob/main/packages/docs/content/docs/permissions.mdx. Sandbox : non trouvé |
| Contrôle de version | Worktrees Git par tâche (« Parallel Agents ») et intégration GitHub (README) ; Subversion non cherché |
| Interface | VS Code uniquement (README) |
| Risques notés | Tout autorisé par défaut ; contexte par défaut de 10k pour un modèle custom ; télémétrie PostHog liée à la connexion |

## 11. Refact (`JegernOUTT/refact`, suite de `smallcloudai/refact`) — ajouté hors liste

**Statut des dépôts** : `smallcloudai/refact` est « kept as the legacy archive … no longer the active development home », son README renvoie vers `JegernOUTT/refact` et annonce « Refact Cloud has been retired » (dernier commit 2026-05-30, dernière release `release/v8.0.4` 2026-05-15) : https://github.com/smallcloudai/refact/blob/main/README.md ; https://github.com/smallcloudai/refact/releases.atom. Le développement actif est dans https://github.com/JegernOUTT/refact (dernier commit lu : 2026-11-12 23:50 +11:00 ; releases `v8.7.0` 2026-10-31, `v8.6.4` 2026-09-07, `v8.6.3` 2026-09-04 : https://github.com/JegernOUTT/refact/releases.atom). Base des URL ci-dessous : `https://github.com/JegernOUTT/refact/blob/main/`. Que `JegernOUTT/refact` soit un fork autorisé par l'équipe d'origine : indiqué par le README du dépôt legacy ; la relation juridique n'est pas vérifiée.

**Portes**
- **G1 oui** — « Ollama, LM Studio, vLLM, and any OpenAI-compatible `/chat/completions`, `/responses`, `/completions`, or embeddings route can be wired in » ; fournisseurs en YAML (`~/.config/refact/providers.d/*.yaml`, `base_provider: litellm|custom`, `endpoint`, `api_key`) : https://github.com/JegernOUTT/refact/blob/main/README.md et https://github.com/JegernOUTT/refact/blob/main/docs/refact-without-ide.md. Les modèles ne sont proposés à l'agent que si `supports_tools` est vrai (`refact-agent/engine/src/caps/caps.rs` L259 : `supports_agent = supports_tools`).
- **G2 oui (code lu, avec réserve)** — README : « No bundled cloud is required, no account is mandatory … network traffic is limited to configured providers and integrations ». Aucun hôte d'analytics tiers (PostHog, Sentry, Segment, etc.) trouvé dans `refact-agent/engine/src` ni `Cargo.toml` (grep). Le module `perf_telemetry.rs` agrège des métriques de performance en local (« telemetry artifacts » sous `~/.cache/refact/`). Appels réseau par fonction : `refact self-update`, marketplace d'extensions, serveurs MCP, et « Buddy » qui peut « file GitHub issues for confirmed product bugs » : non désactivé par défaut d'après le README, réglage exact : non vérifié. Les identifiants `com.smallcloud.codify` dans `src/buddy/improvement_*.rs` sont des manifestes de plugin, pas des appels réseau.
- **G3 oui** — BSD-3-Clause : https://github.com/JegernOUTT/refact/blob/main/LICENSE (badge `license` du README et fichier `LICENSE` du dépôt legacy : « BSD 3-Clause License, Copyright (c) 2023, Small Magellanic Cloud AI Ltd. » ; le fichier du fork n'a été lu que sur ses 3 premières lignes : même texte).
- **G4 oui** — voir ci-dessus (2026-11-12 / 2026-10-31). Le README signale : « The resident daemon is an early preview and may be buggy » ; les plugins IDE et le moteur sont « the stable surfaces ».

**Grille**

| Critère | Constat |
|---|---|
| Nature | Binaire unique `refact` (Rust) : daemon résident + workers par projet + **GUI dans le navigateur** (`refact ui`) + LSP/HTTP pour VS Code et JetBrains + agent CLI headless : README ; guide https://github.com/JegernOUTT/refact/blob/main/docs/refact-without-ide.md |
| Licence | BSD-3-Clause |
| Dernière release / commit | v8.7.0 (2026-10-31) ; commit 2026-11-12 |
| Tool-calling | Passe par des modèles déclarés `supports_tools` ; je n'ai pas trouvé de repli textuel (grep sur `src/caps`, `src/llm`) : **natif seulement, non confirmé** ; comportement sur appel malformé : non lu ; besoin de `--jinja` : non mentionné. Avec Qwen2.5-Coder-14B/llama-server : **non vérifié** |
| Petits modèles | Aucune preuve ≤ 30B trouvée (le dépôt contient `perf_reports/` et `docs/competitive`, non lus) |
| Contexte | « four-stage pressure valve » avant chaque appel : dédoublonnage des fichiers de contexte, compression des sorties d'outils, réparation de l'ordre appel/résultat, rognage au budget ; rapports `compression_report` ; plans exemptés de compression : README (section Modes, transitions, compression) |
| C++ / CMake | Indexation AST par tree-sitter, dont `tree-sitter-cpp = "0.23"` (`refact-agent/engine/Cargo.toml` L71), outil `symbol_def`, recherche sémantique SQLite + `vec0`. Pas de clangd trouvé. Build/tests : `shell`, `process_*` |
| Recherche | `tree`, `cat`, regex, AST `symbol_def`, recherche sémantique, mémoire/trajectoires ; embeddings configurables par fournisseur (`EmbeddingPresets`), local possible (Ollama/LM Studio/OpenAI-compatible `embeddings`) ; modèle par défaut : non vérifié |
| MCP | « connect stdio servers or Streamable HTTP/SSE endpoints, including OAuth-capable configs », découverte paresseuse (`mcp_tool_search`, `mcp_call`) : README. Serena : stdio possible, non testé |
| Exécution de commandes | Outils `shell`, `process_start/read/wait/kill`, `process_write_stdin` (PTY), `cron_*`. **Défauts dans le code** (mode agent de `customization_registry.rs` L850-870) : règle `shell` = `ask`, `tree` = `auto`, `auto_approve_editing_tools: true` (patchs auto-approuvés), `auto_approve_dangerous_commands: false` ; README : « confirmation gates and limited auto-approval for patch-like edits ». Règles de confirmation par motif configurables par mode. Sandbox : agents de tâches dans des **worktrees git isolés** (isolation de fichiers, pas de sandbox de commandes) |
| Édition | `apply_patch`, `create_textdoc`, `update_textdoc*`, `mv`, `rm`, `undo_textdoc` ; checkpoints (`checkpoints_enabled: true`) ; génération de message de commit (`src/agentic/generate_commit_message.rs`) ; auto-commit : non vérifié |
| Contrôle de version | Git (panneau Git de la GUI, worktrees) ; **Subversion : seulement pour lister les fichiers du dépôt** (`svn list -R` si `.svn` existe et `svn` dans le PATH : `src/files_in_workspace.rs` L65, L1076-1078) ; pas d'autre fonction SVN trouvée |
| Interface | **Page web servie par le daemon** (`http://127.0.0.1:<port>`) avec chat, projets, Files, Git, Terminal PTY, diagnostics (`refact doctor`) ; accès réseau : `refact daemon --foreground --bind 0.0.0.0` ; « When the dashboard is reachable beyond localhost, Basic auth is required » (jeton généré dans `~/.cache/refact/daemon.json`, ou identifiants statiques) : docs/refact-without-ide.md. Pas de Dockerfile applicatif trouvé hormis `refact-agent/engine/docker/lsp-*.Dockerfile` (build du LSP). Déploiement en conteneur partagé multi-utilisateurs : **non documenté** ; un seul jeton/identifiant ; état par projet dans `<project>/.refact/` |
| Scriptable | « headless agent CLI » (guide) ; `refact ui --json`, `refact status/ps/logs/events/doctor` ; sessions pilotables via HTTP du daemon ; format de sortie d'un run sans humain : non lu |
| Extension | Modes YAML (`ask, explore, plan, agent, debug, buddy, task_planner, task_agent`), skills (`activate_skill`), slash commands, hooks pré/post-outil, sous-agents avec schémas, marketplace, `AGENTS.md`, règles de confidentialité dans `~/.config/refact/` |
| Observabilité | `refact events`, `refact logs`, trajectoires sous `.refact/trajectories/`, `compression_report`, `perf_reports` |
| Risques notés | Daemon en « early preview » ; édition auto-approuvée par défaut dans le mode agent (d'après le code lu) ; fork communautaire d'un produit dont le cloud a été arrêté ; surface très large (Buddy, planificateur, cron) ; sans auth multi-utilisateurs |

## 12. Zed (`zed-industries/zed`) — agent intégré + modèles locaux

Base des URL : `https://github.com/zed-industries/zed/blob/main/` (clone sparse `--depth 1` : commit `6ceb6fee`, 2026-11-12 08:49 UTC). Docs : `docs/src/ai/*.md` du même dépôt (reflets de https://zed.dev/docs/ai/overview).

**Portes**
- **G1 oui** — fournisseur `language_models.openai_compatible.<nom>.api_url` (« custom base URL, model ID, and API key ») + fournisseurs dédiés `llama.cpp` (`api_url`, auto-découverte via `/props` et `/models/sse`), `ollama`, `lmstudio` : `docs/src/ai/use-api-access.md` (section `openai-compatible`), `docs/src/ai/use-a-local-model.md`.
- **G2 oui avec réserves (docs lues)** — pas de compte requis pour les modèles locaux (non vérifié explicitement : aucune phrase « no sign-in needed » trouvée ; les fournisseurs locaux sont décrits sans connexion). Télémétrie désactivable : `"telemetry": {"diagnostics": false, "metrics": false}` (`docs/src/telemetry.md`) ; `"disable_ai": true` coupe l'IA (`docs/src/ai/quick-start.md` L80-88). Le code de l'agent émet des événements télémétrie (ex. `telemetry::event!("Agent Thread Completion Usage Updated", …)`, `crates/agent/src/thread.rs` ~L3715), donc `metrics: false` est nécessaire. Appels sortants par défaut : Sentry/Snowflake/Amplitude (diagnostics + métriques, toutes les 5 min), installation automatique de `clangd` si absent du `$PATH` (`docs/src/languages/cpp.md`), mises à jour automatiques et extensions (non lus dans le détail : non vérifié).
- **G3 oui** — licences du dépôt racine : `LICENSE-GPL` (GPL-3.0) et `LICENSE-APACHE` ; les crates `agent` et `language_models` déclarent `license = "GPL-3.0-or-later"` (`crates/agent/Cargo.toml`, `crates/language_models/Cargo.toml`). Pas de `LICENSE-AGPL` à la racine dans ce commit. Les autres crates (Apache-2.0 pour certaines) : non énumérées, non vérifié.
- **G4 oui** — `v1.29.1-pre` 2026-11-11, nightly 2026-11-12 : https://github.com/zed-industries/zed/releases.atom ; dernier commit lu 2026-11-12.

**Grille**

| Critère | Constat |
|---|---|
| Nature | Éditeur de bureau natif (Rust, GPUI), agent intégré (« Zed Agent ») + agents externes via ACP + « Terminal Threads » : `docs/src/ai/zed-agent.md`, `external-agents.md`, `terminal-threads.md` |
| Licence | GPL-3.0-or-later (crates `agent`, `language_models`) ; fichier `LICENSE-APACHE` aussi présent |
| Dernière release | v1.29.1-pre, 2026-11-11 (nightly 2026-11-12) |
| Tool-calling | **Natif** (`tools` OpenAI). Pour un fournisseur `openai_compatible`, capacités par défaut : `tools: true`, `images: false`, `parallel_tool_calls: false`, `prompt_cache_key: false`, `chat_completions: true`, `interleaved_reasoning: false` (`use-api-access.md`). Pour llama.cpp/Ollama : `supports_tools` par modèle, découverte automatique des capacités tools/vision par llama.cpp. JSON d'arguments invalide : événement dédié `ToolUseJsonParseError` (`crates/agent/src/thread.rs` ~L3700), traité par `handle_tool_use_json_parse_error_event` ; réparation de JSON partiel `fix_streamed_json` / `parse_tool_arguments` (`crates/language_models/src/util`, utilisé par DeepSeek, Mistral, Bedrock ; pour openai_compatible non vérifié). Aucun repli textuel (XML/codeblock) trouvé : non vérifié exhaustivement. `--jinja` : non mentionné dans les docs de Zed (la doc `llama serve` ne le cite pas ; non vérifié). Modèle Qwen2.5-Coder cité en exemple Ollama/LM Studio (`qwen2.5-coder`, `qwen2.5-coder-7b`) |
| Petits modèles | Docs : exemple `gemma-4-26B-A4B-it` (llama.cpp), `qwen2.5-coder` (Ollama, `max_tokens: 32768`), `mistral` ; Ollama : contexte par défaut `num_ctx` = 4096 si non réglé (`use-a-local-model.md`). Aucun benchmark trouvé |
| Contexte | Compaction automatique activée par défaut à 90 % de la fenêtre (`auto_compact`, seuil en %, en tokens ou en tokens restants ; `agent.compaction_model` séparé) : `docs/src/ai/agent-settings.md` L58-81. `context_window` / `max_tokens` surchargeables ; llama.cpp : longueur lue via `/props` |
| C++ / CMake | `clangd` via LSP intégré, binaire `$PATH` sinon téléchargé ; `binary.path/arguments`, `ignore_system_version` : `docs/src/languages/cpp.md`. Outil agent `diagnostics` (erreurs/avertissements du LSP) : `docs/src/ai/tools.md`. CMake : non vérifié |
| Recherche | Outils `grep` (regex), `find_path` (glob), `list_directory`, `read_file`, `diagnostics`, `fetch`, `search_web` (réservé aux abonnés Zed Pro avec le fournisseur Zed) : `docs/src/ai/tools.md`. Pas d'index sémantique/embeddings trouvé pour l'agent (non vérifié) |
| MCP | Client MCP : Tools et Prompts (pas Sampling/Elicitation), `notifications/tools/list_changed` ; serveurs locaux (`command`, `args`, `env`) et distants (`url`, `headers`, OAuth MCP standard) dans `context_servers` : `docs/src/ai/mcp.md`. Noms de permission `mcp:<serveur>:<outil>` |
| Exécution de commandes | Outil `terminal`. Permissions : `agent.tool_permissions.default` = `confirm` (défaut) / `allow` / `deny` ; par outil `always_allow`, `always_deny` (prioritaire, non contournable), `always_confirm` en regex Rust (`docs/src/ai/tool-permissions.md`). Sandbox OS optionnel pour `terminal` et `fetch` (bubblewrap sous Linux, WSL sous Windows, rien à installer sous macOS) : écritures limitées aux répertoires du projet, `.git` protégé en écriture, réseau bloqué par défaut ; n'isole pas Zed, les agents externes ni les Terminal Threads : `docs/src/ai/sandboxing.md`. Note du même fichier : le sandbox Windows est plus faible que Linux/macOS |
| Édition | Outils `edit_file`, `write_file`, `copy_path`, `move_path`, `delete_path`, `create_directory` ; permissions par chemin ; revue des diffs dans l'éditeur (non détaillé : non vérifié) |
| Contrôle de version | Panneau Git intégré, génération de message de commit par IA (`docs/src/git.md` cité dans `privacy-and-security.md`). Subversion : non trouvé (non vérifié) |
| Interface | **Application de bureau uniquement.** Un « Zed headless server » existe pour le développement distant (SSH) : l'UI, le LLM et l'agent tournent côté client local, le serveur ne fait tourner que code, LSP, tâches et terminal (`docs/src/remote-development.md` L15-19). Aucun mode CLI/serveur d'agent, ni page web multi-utilisateurs, trouvé dans les docs lues |
| Scriptable | Non trouvé pour l'agent (pas de mode non interactif dans les docs lues : non vérifié) ; agents externes pilotables par ACP |
| Extension | Profils d'agent (`agent-profiles.md`), règles (`rules.md`), instructions (`instructions.md`), skills (`skills.md`), extensions et serveurs MCP en extension (`docs/src/extensions/mcp-extensions.md`) |
| Observabilité | `zed::OpenTelemetryLog` (journal de ce que Zed a envoyé) ; journal de l'agent : non vérifié |
| Risques notés | GPL-3.0 ; télémétrie par défaut (désactivable) ; `clangd` téléchargé automatiquement ; contexte Ollama 4096 par défaut ; pas de mode serveur/web ; `parallel_tool_calls` désactivé par défaut pour openai_compatible |

## 13. Open WebUI (`open-webui/open-webui`) + Open Terminal (`open-webui/open-terminal`)

Base des URL : `https://github.com/open-webui/open-webui/blob/main/` (clone `--depth 1`, commit `b0e6098e`, 2026-11-09 08:48 +09:00). Pertinence pour un agent de code : Open WebUI est d'abord un client de chat web ; la couche « agent » (exécution de commandes, fichiers) est fournie par un projet séparé, **Open Terminal** (`README.md` L92 : « The action layer that turns Open WebUI into a full agent harness »). Les deux sont décrits ensemble ci-dessous.

**Portes (Open WebUI)**
- **G1 oui** — `OPENAI_API_BASE_URLS` (liste séparée par `;`) et `OPENAI_API_KEYS`, `ENABLE_OPENAI_API` : `backend/open_webui/config.py` L309-354 ; Ollama aussi (`ENABLE_OLLAMA_API`). Connexions « Direct » (navigateur → endpoint) : `ENABLE_DIRECT_CONNECTIONS` (défaut `False`).
- **G2 oui avec réserves (code lu)** — authentification locale : `WEBUI_AUTH` vaut `True` par défaut (`env.py` L765), le premier compte créé sur l'instance est local, pas de compte externe ; `WEBUI_AUTH=False` = mode sans compte (non testé : non vérifié que c'est fonctionnel avec plusieurs utilisateurs). Télémétrie : `.env.example` L78-80 propose `SCARF_NO_ANALYTICS=true`, `DO_NOT_TRACK=true`, `ANONYMIZED_TELEMETRY=false` (cette dernière vise Chroma). Valeurs par défaut effectives de Scarf : non vérifié. `OFFLINE_MODE` (défaut `false`) coupe aussi `ENABLE_VERSION_UPDATE_CHECK` (`env.py` L1196-1203). OpenTelemetry désactivé par défaut (`ENABLE_OTEL=False`). Appels sortants par défaut non listés ici : téléchargement de modèles d'embedding depuis Hugging Face (RAG, non vérifié ligne à ligne), vérification de version.
- **G3 non vérifié (cas limite)** — `LICENSE` : « Open WebUI License », texte BSD-3-Clause + clause 4 qui interdit de modifier, retirer ou remplacer la marque « Open WebUI » sauf (i) ≤ 50 utilisateurs sur 30 jours glissants, (ii) autorisation écrite, (iii) licence entreprise ; le code antérieur au commit `60d84a3a` reste en BSD-3 (`LICENSE_HISTORY`). `pyproject.toml` : `license = { file = "LICENSE" }`. Pas un identifiant SPDX standard ; l'appartenance à la définition « open-source » est à trancher par le parent (non OSI, non vérifié auprès de l'OSI). https://github.com/open-webui/open-webui/blob/main/LICENSE.
- **G4 oui** — v0.13.3 2026-11-08 (releases.atom : https://github.com/open-webui/open-webui/releases.atom) ; dernier commit lu 2026-11-09.

**Portes (Open Terminal)** : G1 sans objet (c'est un serveur d'outils, pas un client LLM) ; G2 oui (API key générée au démarrage si absente, `README.md` L49) ; G3 oui — MIT (`LICENSE`) ; G4 oui — v0.17.7, 2026-11-10 (https://github.com/open-webui/open-terminal/releases.atom).

**Grille (Open WebUI)**

| Critère | Constat |
|---|---|
| Nature | Application web serveur (FastAPI + Svelte), conteneur Docker (`Dockerfile`, `docker-compose*.yaml`), multi-utilisateurs avec rôles ; client de chat, pas un agent de code |
| Licence | « Open WebUI License » = BSD-3-Clause + clause de marque (voir G3) ; Open Terminal : MIT |
| Dernière release | v0.13.3, 2026-11-08 ; Open Terminal v0.17.7, 2026-11-10 |
| Tool-calling | Mode **natif** par défaut : le mode `legacy` (prompt) n'est activé que si `params.function_calling == 'legacy'` (`backend/open_webui/utils/middleware.py` L2072, L2158…), donc par défaut les `tools` OpenAI sont envoyés au serveur. Réparation/repli pour llama-server `--jinja` : non vérifié |
| Petits modèles | Non vérifié (aucun chiffre trouvé dans le dépôt lu) |
| Contexte | Gestion de contexte propre (troncature, RAG, mémoires) : non détaillée, non vérifié |
| C++ / CMake | Aucun support (pas de LSP) |
| Recherche | RAG/embeddings (Chroma `chromadb==1.5.9` dans `backend/requirements.txt`) sur documents téléversés ; pas de recherche de code intégrée au dépôt de l'utilisateur. Côté Open Terminal : explorateur de fichiers + terminal (`README.md` L76) |
| MCP | Client MCP natif en **streamable HTTP uniquement** : `backend/open_webui/utils/mcp/client.py` L10-12 importe `mcp.client.streamable_http_client` ; aucun `stdio` trouvé dans ce fichier. `mcp==2.3.0` ; `TOOL_SERVER_CONNECTIONS` pour les serveurs d'outils (OpenAPI et MCP : `config.py` L368, `utils/tools.py` L218). Approbation d'appels d'outils : `backend/open_webui/utils/tool_approval.py` (états `requires_approval`, actions `approve`/`reject`/`answer`) |
| Exécution de commandes | Interpréteur de code intégré (`ENABLE_CODE_EXECUTION` défaut `True`, `CODE_EXECUTION_ENGINE` défaut `pyodide`, exécution dans le navigateur ; `config.py` L391-415) — pas un shell système. Shell réel : via **Open Terminal** (Docker : `docker run -d --name open-terminal …` ; sur machine nue, les commandes tournent avec les droits de l'utilisateur ; l'API key donne accès commandes et fichiers : `README.md` L15-52 du dépôt open-terminal). Autorisations par outil : `tool_permissions.py`, `tool_approval.py` (détail de l'allowlist : non vérifié) |
| Édition | Via Open Terminal (API fichiers) ; pas d'outil d'édition par patch dans Open WebUI lui-même (non vérifié) |
| Contrôle de version | Non trouvé pour Open WebUI ; Open WebUI Computer (autre projet) annonce « git » : https://github.com/open-webui/computer (non lu) ; Subversion : non trouvé |
| Interface | **Serveur web multi-utilisateurs en conteneur** (comptes, rôles, groupes, SSO ; en-têtes d'auth de confiance `WEBUI_AUTH_TRUSTED_EMAIL_HEADER`…, `env.py` L812-815). Il n'a pas de CLI d'agent. Le journal du changelog indique que des agents de code (Claude Code, Codex, Pi) apparaissent dans le sélecteur de modèles via Open Terminal (`CHANGELOG.md`, entrée « Coding agents as models ») : ce sont des agents tiers, pas un agent propre |
| Scriptable | API HTTP FastAPI (OpenAI-compatible côté Open WebUI) ; détail non vérifié |
| Extension | Outils/fonctions/pipelines Python (`backend/open_webui/functions.py`), serveurs d'outils OpenAPI/MCP |
| Observabilité | OpenTelemetry (`docker-compose.otel.yaml`, `ENABLE_OTEL*` désactivés par défaut) |
| Risques notés | Licence à clause de marque ; couche agent séparée (Open Terminal) ; MCP stdio absent ; interpréteur Pyodide ≠ shell ; mode `legacy`/natif par modèle ; API key Open Terminal = accès shell |

## 14. opencode (`anomalyco/opencode`) — mode web/serveur (lecture rapide)

Base : clone `--depth 1`, commit `3d308eae`, 2026-11-12 11:03 UTC. Docs : `services/site/src/docs/content/*.mdx` du dépôt https://github.com/anomalyco/opencode (pages V2 ; le dossier `v1/` contient l'ancienne doc). Lecture **partielle** : seuls l'interface web, les permissions, MCP, les fournisseurs et le réseau ont été lus. Le reste est « non vérifié ». Ce projet relève aussi de la famille CLI/TUI ; il n'est traité ici que pour son mode serveur/web.

**Portes**
- **G1 oui** — fournisseur `@opencode/ai/providers/openai-compatible` avec `settings.baseURL` (`providers.mdx` L61-73, L217-235) ; Ollama détecté sur `http://127.0.0.1:11434` (`providers.mdx` L527-548). llama-server : non cité dans `providers.mdx` (non vérifié, mais le fournisseur openai-compatible est générique).
- **G2 non vérifié** — le catalogue de modèles vient de https://models.dev (`models.mdx` L11) ; la variable `OPENCODE_DISABLE_MODELS_FETCH` existe dans `packages/cli/src/server-process.ts` ; `OPENCODE_DISABLE_AUTOUPDATE` dans `packages/cli/src/services/updater.ts` ; `OPENCODE_DISABLE_FREE_MODELS` masque les modèles gratuits hébergés. L'interface web embarque `@sentry/solid` (`packages/app/package.json` L72) : activation et collecte non vérifiées. Aucune page « telemetry » trouvée dans les docs V2 (`rg` sur `telemetry` : seulement une note de migration sur `openTelemetry`). Compte : non requis d'après `cli/web.mdx` (mot de passe du serveur local + lien `opencode pair`).
- **G3 oui** — MIT (« Copyright (c) 2025 opencode », `LICENSE`).
- **G4 oui** — v2.2.7, 2026-11-10 (https://github.com/anomalyco/opencode/releases.atom) ; dernier commit lu 2026-11-12.

**Grille**

| Critère | Constat |
|---|---|
| Nature | Agent de code TypeScript (monorepo Bun : `packages/cli`, `tui`, `server`, `app`, `desktop`, `sdk`, `plugin`…) : TUI + service d'arrière-plan + interface web + application de bureau |
| Licence | MIT |
| Dernière release | v2.2.7, 2026-11-10 |
| Tool-calling | Fournisseurs via AI SDK ; formats « freeform » (`text`, `regex`, `lark`) ignorés sans perte du modèle (`models.mdx` L237) ; repli textuel et `--jinja` : non vérifié |
| Petits modèles | Exemple Ollama `qwen3:8b` dans la doc (`providers.mdx` L534) ; aucun benchmark trouvé |
| Contexte | Compaction automatique, réglage `buffer` = part de fenêtre laissée libre avant compaction (`config.mdx` L371) |
| C++ / CMake | Doc LSP présente seulement dans `v1/content/lsp.mdx` (contient `clangd`) ; état en V2 : non vérifié |
| Recherche | Outils `grep`, `glob`, `read` cités dans `tools.mdx` ; index sémantique : non vérifié |
| MCP | Serveurs `local` (stdio) et `remote` (URL, OAuth par défaut) ; commande `opencode mcp add` : `mcp-servers.mdx`. Prompts, resources, instructions exposés en plus des tools |
| Exécution de commandes | Outil `shell` (hôte). Permissions : liste ordonnée de règles `{action, resource, effect}` avec `allow`/`deny`/`ask`, la dernière règle correspondante gagne, `ask` par défaut si aucune règle (`permissions.mdx`). Sandbox : non vérifié |
| Édition | Un outil d'édition cité dans `tools.mdx` L13 ; détails non vérifiés |
| Contrôle de version | Git (`packages/core/src/git.ts`, worktrees, `config.mdx` L509) ; Subversion non trouvé |
| Interface | **Serveur local + interface web** : « served from the same server that powers the TUI … available by default and password-protected » ; accès par `opencode pair` (lien à usage unique, expiration 5 min, cookie de session 30 jours) ; écoute sur localhost par défaut (port 49374 sous Linux/macOS/WSL, 28894 sous Windows) ; `opencode serve`, `opencode service …` ; accès distant via OpenTunnel (`pair --remote`) : `cli/web.mdx`. Multi-utilisateurs avec comptes : non trouvé (mot de passe unique : non vérifié) ; image Docker officielle : non vérifié |
| Scriptable | `opencode serve`, SDK (`packages/sdk`, `packages/client`), plugins `server`/`cli` (`build/plugins/*.mdx`) ; mode non interactif : non vérifié |
| Extension | Plugins (`build/plugins`), skills, agents, `AGENTS.md` (`instructions.mdx`) ; `OPENCODE_DISABLE_CLAUDE_CODE*` indique une lecture des fichiers Claude Code |
| Observabilité | OTLP logs/traces (`packages/util/src/observability/otlp.ts`, lit `OTEL_RESOURCE_ATTRIBUTES`) ; activation par défaut : non vérifié |
| Risques notés | Dépôt récemment renommé/déplacé (V1→V2 avec rupture de config, `migrate-v1.mdx`) ; collecte `models.dev` ; Sentry front : à vérifier |


---

## Candidats non couverts ou couverts partiellement

Données de release seulement (releases.atom du 2026-11-12), pas de grille :
- **Eclipse Theia** (IDE web/desktop avec Theia AI) : v1.77.0, 2026-11-05 — licence, télémétrie, outils : non vérifié.
- **Dyad** (app de bureau locale) : v1.23.0, 2026-11-09 — non vérifié.
- **Goose** (agent, app de bureau + CLI) : v1.59.0, 2026-11-10 — non vérifié (probablement couvert par la famille CLI).
- **LibreChat**, **AnythingLLM** : non regardés.
- **Zed** : agent seulement ; les extensions de langage et le serveur distant ne sont pas évalués.
- **opencode** : section 14 en lecture partielle (web, permissions, MCP, fournisseurs).

## Ce que je n'ai pas pu vérifier (liste consolidée)

Commun à presque tous : **aucun test réel** n'a été fait (consigne : documentaire uniquement). Donc pour chaque candidat, le comportement de **Qwen2.5-Coder-14B via llama-server avec `--jinja`** n'est pas vérifié (appels natifs, repli, JSON malformé), et **aucune preuve publiée de qualité d'agent avec un modèle ≤ 30B** n'a été trouvée sauf mentions d'exemples de configuration dans les docs.

Par candidat (détails dans chaque section) :
- **Cline** : coupure totale des appels de feature flags à l'opt-out ; Qwen2.5-Coder-14B/llama-server ; qualité ≤ 30B.
- **Roo Code** : CLI `roo` sur un llama-server (aucun chemin documenté) ; ≤ 30B ; le détail de `PRIVACY.md` face au code.
- **Zoo Code** : présence du code Roo cloud dans les builds publiés ; comportement hors connexion ; vérification directe du provider OpenAI-compatible.
- **Kilo Code** : Qwen2.5-Coder/llama-server ; modèle d'embedding par défaut.
- **Continue** : condition d'activation de la télémétrie par défaut (la doc parle encore de PostHog, le code n'en contient plus) ; embeddings locaux ; Subversion ; Qwen2.5-Coder/llama-server ; ≤ 30B.
- **llama.vscode** : transports MCP (ceux de VS Code) ; compaction ; modèle d'embedding par défaut ; observabilité ; Subversion.
- **Void** : plusieurs points dont l'usage des répertoires `remote/` et `cli/` hérités de VS Code pour servir Void, outils de terminal et réglages d'approbation, compaction, index sémantique, ≤ 30B.
- **Tabby** : comportement de l'opt-out dans le code ; si le binaire publié embarque `ee/` ; Subversion.
- **OpenHands** : portée exacte de certaines télémétries ; auto-commit ; Subversion ; Qwen2.5-Coder.
- **Pochi** : endpoint par défaut de la télémétrie ; format natif vs repli ; CLI/serveur (non cherché exhaustivement) ; contenu de `private/`.
- **Refact** : réglage exact de l'envoi de rapports d'erreurs ; auto-commit ; modèle d'embedding par défaut ; Qwen2.5-Coder/llama-server.
- **Zed** : absence de compte (aucune phrase explicite) ; réparation de JSON pour le fournisseur OpenAI-compatible ; repli textuel et `--jinja` ; licence de chaque crate ; CMake ; index sémantique ; mode non interactif ; Subversion ; détail des mises à jour automatiques et des extensions.
- **Open WebUI** : valeurs par défaut de Scarf ; téléchargements Hugging Face par défaut (RAG) ; repli de tool-calling ; petits modèles ; allowlist détaillée des outils ; MCP stdio (absent du fichier client lu) ; statut « open-source » de la licence (clause 4).
- **opencode** : télémétrie (Sentry front, OTLP), Docker, multi-utilisateurs, mode non interactif, LSP V2, sandbox, repli de tool-calling.
- **Dates** : toutes les dates de release viennent de `releases.atom` (pas de l'API GitHub, limitée en débit) ; les dates de création de fork (Zoo Code) viennent d'une source secondaire.
