# C — Cadres pour construire son agent + état du tool-calling avec petits modèles locaux

Date de l'étude : 2026-11-12. Famille C de l'étude `harness-selection`. Grille : `.scratch/harness-selection/criteria.md` (portes G1-G4, contexte fixe : Qwen2.5-Coder-14B-Instruct Q5_K_M via `llama-server` tag b10216, API OpenAI-compatible, Windows + conteneurs). **Faits seulement, aucune recommandation, aucun classement.**

## 0. Méthode et conventions

- Pages web lues avec l'outil de fetch web (README, docs officielles, pages de releases/issues). Pour le code source et les dates de release j'ai aussi cloné ou téléchargé les dépôts officiels (`git clone --depth 1`, `raw.githubusercontent.com`, API GitHub `api.github.com/repos/<org>/<repo>/releases`) ; les URLs citées sont les URLs publiques correspondantes. Les numéros de ligne `L…` sont ceux de la branche par défaut à la date du jour.
- Fenêtre G4 : release **ou** commit depuis le **2026-05-12** (6 mois avant 2026-11-12).
- « non vérifié » = je n'ai pas lu de source primaire qui tranche. Rien n'a été exécuté : aucun test, aucun benchmark, aucune installation.
- Les chiffres des cartes de modèles (§ 2c) sont des **auto-déclarations des éditeurs**, pas des mesures indépendantes.
- Les « retours d'usage » sont des issues GitHub des dépôts concernés (primaires pour dire « un utilisateur a signalé », pas pour dire « le bug est général »).
- Avertissement de contexte : aucun de ces cadres n'est un harness complet pour C++/CMake/Subversion. Pour les cadres purs, les lignes « C++/CMake », « Recherche », « Édition », « Contrôle de version » sont **sans objet (à construire)** sauf mention.

## 1. Tableau de synthèse (cadres)

Légende : ✔ = vérifié ; ✔* = vérifié avec réserve (voir la section) ; ? = non vérifié ; ✘ = échec avec preuve.

| Cadre | Langage | G1 endpoint OpenAI-compat. (`base_url`) | G2 sans compte/réseau (télémétrie coupable) | G3 licence libre | G4 maintenu (≥ 2026-05-12) | Licence (SPDX) | Dernière release (date) | Dernier commit vu |
|---|---|---|---|---|---|---|---|---|
| **OpenHarness (HKUDS)** | Python (+TUI Node) | ✔ `oh provider add --base-url` | ✔* aucune télémétrie trouvée par grep (non exhaustif) | ✔ | ✔* release > 6 mois, commit dans la fenêtre | MIT | v0.1.9 (2026-05-07) | 2026-06-04 |
| **pydantic-ai** (+ `pydantic-ai-harness` / `Coder`) | Python | ✔ `OpenAICompatibleProvider` | ✔ Logfire optionnel | ✔ | ✔ | MIT | v2.68.0 (2026-11-12) ; harness 0.68.0 (2026-11-12) | 2026-11-12 |
| **smolagents** (Hugging Face) | Python | ✔ `OpenAIModel(api_base=…)` | ✔* aucune télémétrie trouvée (README, `agents.py`) | ✔ | ✔ | Apache-2.0 | v1.26.0 (2026-05-29) | 2026-10-06 |
| **LangGraph** | Python (+JS) | ✔* via `ChatOpenAI(base_url)` de LangChain (hors dépôt) | ? tracing LangSmith : défaut non lu | ✔ | ✔ | MIT | 1.2.20 (2026-11-05) | 2026-11-11 |
| **OpenAI Agents SDK** (python) | Python | ✔ `AsyncOpenAI(base_url)` + `OpenAIChatCompletionsModel` | ✔* tracing **actif par défaut**, coupable | ✔ | ✔ | MIT | v0.24.0 (2026-10-15) | 2026-11-11 |
| **Google ADK** (python) | Python | ✔* via `LiteLlm(api_base)` | ✔* télémétrie du **CLI `adk`** avec consentement, coupable | ✔ | ✔ | Apache-2.0 | v2.14.0 (2026-11-07) | 2026-11-12 |
| **Strands Agents** (SDK python) | Python (+TS) | ✔ `LlamaCppModel(base_url)` (provider natif) | ✔ OTel opt-in | ✔ | ✔ | Apache-2.0 | python/v1.64.0 (2026-11-04) | 2026-11-11 |
| **Mastra** | TypeScript | ✔ `model: {id, url}` | ✔* télémétrie CLI/serveur **par défaut**, coupable | ✔* Apache-2.0 sauf dossiers `ee/` (licence propriétaire) | ✔ | Apache-2.0 + `ee/` EE License 2.0 (API GitHub : NOASSERTION) | @mastra/core@1.82.0 (2026-11-04) | 2026-11-12 |
| **Agno** | Python | ✔ classe native `LlamaCpp(OpenAILike)` | ✔* `telemetry=True` **par défaut**, coupable | ✔ | ✔ | Apache-2.0 | v3.1.12 (2026-10-29) | 2026-11-12 |
| *Autres (voir § 1.10)* | | | | | | | | |
| Pi (`earendil-works/pi`, ex `badlogic/pi-mono`) | TypeScript | ✔ doc llama.cpp dédiée | ✔* télémétrie d'install par défaut, coupable | ✔ | ✔ | MIT | v1.5.2 (2026-11-10) | 2026-11-12 |
| Deep Agents (LangChain) | Python | ✔* via modèles LangChain | ? | ✔ | ✔ | MIT | deepagents-code==0.2.7 (2026-11-10) | 2026-11-12 |

Mention en une ligne (hors périmètre) : `autonomous-ai/openharness` est un **autre projet** homonyme (MIT), un « command center » qui orchestre d'autres agents de code (Claude Code, Codex, Hermes…) et non un cadre de boucle d'outils ; dernière release vue `v1.4.47_desktop` le 2026-11-12. Sources : https://github.com/autonomous-ai/openharness (README) ; https://api.github.com/repos/autonomous-ai/openharness/releases.

Sources communes du tableau : API releases/repos `https://api.github.com/repos/<org>/<repo>/releases` et `…/repos/<org>/<repo>` (licence SPDX, `pushed_at`) ; commits via clones `--depth 1` (`git log -1`) ; PyPI https://pypi.org/pypi/pydantic-ai-harness/json.

---

## 1.1 OpenHarness (HKUDS) — https://github.com/HKUDS/OpenHarness

- **Nature** : « agent harness » Python (CLI `oh`, TUI React/Ink) avec 43 outils, skills, plugins, mémoire, swarm ; l'auteur se présente comme infrastructure légère d'agent, pas comme bibliothèque minimale. https://github.com/HKUDS/OpenHarness/blob/main/README.md
- **Licence** : MIT. https://github.com/HKUDS/OpenHarness/blob/main/LICENSE
- **Release / commit** : release v0.1.9 le 2026-05-07 (API https://api.github.com/repos/HKUDS/OpenHarness/releases/latest) ; dernier commit sur `main` le 2026-06-04 (`fix(config): preserve profile auth when overriding model`, `git log -1` du clone). Aucune activité depuis ~5 mois. La release seule sortirait de la fenêtre G4 (2026-05-07 < 2026-05-12) ; le commit y reste.
- **G1** : toute API `/v1/chat/completions` ; `oh provider add … --api-format openai --base-url …` ; exemple Ollama `http://localhost:11434/v1`. Pas d'exemple `llama-server` dans le README (non vérifié si fonctionnel). https://github.com/HKUDS/OpenHarness/blob/main/README.md (sections « Provider Compatibility », « Ollama »). Le client OpenAI normalise les `base_url` personnalisées : https://github.com/HKUDS/OpenHarness/blob/main/src/openharness/api/openai_client.py (L245).
- **G2** : `grep -i telemetry|analytics|posthog|sentry` sur `src/` : aucun mécanisme de télémétrie (seulement des faux positifs « segment »). Les outils `web_search` (DuckDuckGo par défaut) et `web_fetch` sont des outils, pas de la télémétrie. https://github.com/HKUDS/OpenHarness/blob/main/README.md (§ « Web search and proxy settings »).
- **Modèle d'outils**
  - Liste d'outils : registre d'outils ; options CLI `--allowed-tools` / `--disallowed-tools` (déclarées, sémantique non lue) https://github.com/HKUDS/OpenHarness/blob/main/src/openharness/cli.py (L2272-2280) ; `allowed_tools` dans les settings https://github.com/HKUDS/OpenHarness/blob/main/src/openharness/config/settings.py (L54).
  - Validation : chaque outil a un `input_model` Pydantic ; l'engine appelle `model_validate`. Outil inconnu → `ToolResultBlock(is_error=True, "Unknown tool: X")` ; entrée invalide → `"Invalid input for X: …"`. https://github.com/HKUDS/OpenHarness/blob/main/src/openharness/engine/query.py (L909-930 environ).
  - Refus d'un shell : l'outil `Bash` existe (README, tableau des outils). Modes de permission `default` (demande avant écriture/exécution), `auto` (« Allow everything »), `plan` (bloque les écritures) ; `path_rules` et `denied_commands` dans `settings.json`. https://github.com/HKUDS/OpenHarness/blob/main/README.md (§ Permissions) ; https://github.com/HKUDS/OpenHarness/blob/main/src/openharness/permissions/modes.py.
  - Règle de phase : hooks `PreToolUse`/`PostToolUse` de types `command`, `prompt`, `http`, `agent` (https://github.com/HKUDS/OpenHarness/blob/main/src/openharness/hooks/schemas.py) ; un hook `pre_tool_use` qui bloque renvoie une erreur de résultat d'outil (query.py, L895-905). Le payload lu contient `tool_name`, `tool_input`, `event` : l'état « après une écriture, pas de compilation avant `build_step` » devrait donc être tenu par le hook lui-même (déduction du code, non testée).
- **Appels malformés** : si `function.arguments` n'est pas un JSON valide, l'argument est **silencieusement remplacé par `{}`** (non-stream et stream) ; un appel sans nom (« phantom ») est ignoré. La validation Pydantic échoue ensuite sur les champs requis → erreur d'outil renvoyée. https://github.com/HKUDS/OpenHarness/blob/main/src/openharness/api/openai_client.py (L228-236 et L405-420). Relances API : « API Retry with Exponential Backoff » (README).
- **Annulation d'un tour** : `max_turns` par défaut 200 → `MaxTurnsExceeded` (query.py L129-153, L882-884). Pas d'API d'annulation d'un tour trouvée dans `query.py` (recherche non exhaustive).
- **Streaming** : « Streaming Tool-Call Cycle » ; sortie `--output-format stream-json`. README.
- **MCP** : client MCP, transports stdio et Streamable HTTP (`mcp/client.py` importe `stdio_client` et `streamable_http_client`) ; outils nommés `mcp__<serveur>__<outil>`. Serena : non vérifié. https://github.com/HKUDS/OpenHarness/blob/main/src/openharness/mcp/client.py ; …/tools/mcp_tool.py (L22).
- **Contexte** : auto-compaction (v0.1.6) ; issues fermées #199 « Compaction + context: llama.cpp errors, n_ctx, and multimodal » et #212 « Context overflow from large MCP tool_result payloads » (toutes deux 2026-04-28). https://github.com/HKUDS/OpenHarness/issues?q=is%3Aissue%20llama
- **C++/CMake, recherche, édition, VCS** : outils `Read/Write/Edit/Glob/Grep`, `LSP` listé dans les outils de recherche (README) ; clangd, repo map, index sémantique : non vérifié. Commit automatique : non vérifié (commande `/commit` et plugin `commit-commands`). Subversion : non vérifié.
- **Interface / scriptable** : TUI ; `oh -p … --output-format json|stream-json` ; Windows natif (`openh` dans PowerShell car `oh` = alias `Out-Host`). Conteneur : non vérifié.
- **Extension** : outils Pydantic (`BaseTool`), skills `SKILL.md`, plugins compatibles claude-code, `CLAUDE.md`. Équivalent de `rules/*.md` : `CLAUDE.md` + skills.
- **Risques notés** : mode `auto` « Allow everything » ; option `--dangerously-skip-permissions` ; remplacement silencieux des arguments illisibles par `{}`.

## 1.2 pydantic-ai — https://github.com/pydantic/pydantic-ai

- **Nature** : cadre Python. S'y ajoute `pydantic-ai-harness` avec la capability **`Coder`** (FileSystem + Shell + RepoContext + SubAgents) : https://pydantic.dev/docs/ai/harness/coder/ . Package PyPI `pydantic-ai-harness` 0.68.0, MIT (https://pypi.org/pypi/pydantic-ai-harness/json ; https://raw.githubusercontent.com/pydantic/pydantic-ai-harness/main/LICENSE).
- **Licence** : MIT (API https://api.github.com/repos/pydantic/pydantic-ai).
- **Release / commit** : v2.68.0 le 2026-11-12 (https://api.github.com/repos/pydantic/pydantic-ai/releases/latest) ; harness 0.68.0 le 2026-11-12 (PyPI).
- **G1** : `OpenAICompatibleProvider(name, base_url, api_key)` avec `OpenAIChatModel` ; `VLLMProvider` ; guide Ollama. https://github.com/pydantic/pydantic-ai/blob/main/docs/models/compatible-apis.md (L331-392). Pas de provider `llama.cpp` dédié : issue ouverte #4878 « Need for llama.cpp providers » (2026-03-27) https://github.com/pydantic/pydantic-ai/issues?q=is%3Aissue%20llama.cpp . `OpenAIProvider(base_url=…)` est réservé à OpenAI ou à un proxy transparent (même page, L392).
- **G2** : instrumentation Logfire/OpenTelemetry **optionnelle** (`logfire.instrument_pydantic_ai()`), « any OTLP backend works ». https://github.com/pydantic/pydantic-ai/blob/main/README.md (L213-232). Aucune télémétrie par défaut trouvée (non exhaustif).
- **Modèle d'outils**
  - Liste fermée : outils enregistrés explicitement ; `prepare` par outil et **`prepare_tools` à l'échelle de l'agent, appelé à chaque étape**, peut filtrer, modifier ou retirer des outils ; `tool_choice` configurable (y compris par étape via une capability dont `get_model_settings` reçoit `RunContext` avec `ctx.messages` et `ctx.run_step`). https://ai.pydantic.dev/tools-advanced/ (sections « Dynamic Tools », « Tool Choice »).
  - Validation : arguments validés par Pydantic contre la signature ; `args_validator` personnalisable (lève `ModelRetry`, `ToolFailed`, `ApprovalRequired`, `CallDeferred`). Même page (L709, L862).
  - Règle de phase : hooks de cycle de vie `before_tool_validate`, `before_tool_execute`, `wrap_*`, avec `SkipToolValidation(args)` et `SkipToolExecution(result)`, et `ModelRetry`/`ToolFailed` levables depuis les hooks. https://pydantic.dev/docs/ai/core-concepts/hooks/ ; https://ai.pydantic.dev/tools-advanced/ (L815). `requires_approval` + `ApprovalRequiredToolset`.
  - Refus d'un shell : le cœur n'a pas de shell. `Coder` inclut `shell(command, mode, timeout)` : « Unrestricted commands », `Shell(denied_commands=[], allow_interactive=True, default_timeout=270)` ; on peut recomposer l'agent à partir de `FileSystem` seul (la page dit « Build the same agent from the pieces … allowlist commands »). https://pydantic.dev/docs/ai/harness/coder/ (L146-200).
  - Outils de `Coder` : `read_file`, `write_file`, `edit_file` (remplacement exact, un seul match), `list_files`, `grep` (ripgrep), `shell`, `delegate_task`. Même page.
- **Appels malformés / relances** : un échec de validation devient un `ToolReturnPart` `outcome='retried'` renvoyé au modèle ; budget par outil (`Tool(max_retries)`, `Agent(retries={'tools': N})`) ; dépassement → `UnexpectedModelBehavior`. `ToolFailed` ne consomme pas le budget ; `UsageLimits(request_limit, tool_calls_limit)` borne le run. https://ai.pydantic.dev/tools-advanced/ (L707-811, L1033). `Coder` compose `RepairToolArguments` (`json-repair` avant validation, heuristique), met `strict=False` sur ses outils, et chaque outil de fichier autorise 5 relances. https://pydantic.dev/docs/ai/harness/coder/ (L226-236, L150). Comportement sur un **nom d'outil inconnu** : non vérifié.
- **Annulation** : `CancellationToken` passé à `run/run_sync/run_stream/iter` → `RunCancelled` ; `RunContext.cancel()` depuis un outil ; les outils async parallèles sont annulés, un outil **synchrone ne peut pas être arrêté** (son thread continue, résultat jeté). https://ai.pydantic.dev/tools-advanced/ (L852-856).
- **Streaming** : `run_stream()` documenté (hooks de nœuds adaptés au streaming). https://pydantic.dev/docs/ai/core-concepts/hooks/ (L221). Détail du streaming des appels d'outils avec llama-server : non vérifié.
- **MCP** : capability `MCP('https://…/mcp')` ; `MCPToolset(max_retries=…)`. https://github.com/pydantic/pydantic-ai/blob/main/README.md (L168-172) ; https://ai.pydantic.dev/tools-advanced/ (L756). Transports supportés (stdio notamment) : non vérifié. Serena : non vérifié.
- **Modèle local / llama-server** : aucun guide `llama.cpp` ; issue #11244 (fermée 2026-10-25) : erreur de connexion due à un **port** différent — le bot de triage écrit que « llama.cpp 0.7.0 appears to default to port 9931 » (voir § 2d). https://github.com/pydantic/pydantic-ai/issues/11244 . Issue #224 « Tool calling issues with vllm » (fermée 2025-08-25, 30 commentaires, contenu non lu).
- **Contexte** : `Coder` ajoute `ClearToolResults(max_fraction=0.7)` et tronque tout résultat > 64 000 caractères ; `RepoContext` charge `AGENTS.md` (sinon `CLAUDE.md`) avec un budget de 32 000 caractères. https://pydantic.dev/docs/ai/harness/coder/ (L155-158). Adaptation explicite à 32 k jetons : non vérifié.
- **Exécution de commandes (harness)** : « Commands are unrestricted and can outlive runs » ; le shell peut contourner les règles de chemins en lecture seule des outils fichiers ; **`LocalWorkspace` ne tourne pas sous Windows** (« use a sandbox capability there, or WSL ») ; le workspace distant/sandbox est un concept de première classe. https://pydantic.dev/docs/ai/harness/coder/ (L200, L212-214, L282, L310).
- **C++/CMake, VCS** : aucun LSP trouvé ; `git`/`rg` utilisés via shell. Index sémantique : aucun trouvé. Subversion : non vérifié.
- **Interface / scriptable** : bibliothèque ; benchmarking via Terminal-Bench 2.1 / Harbor (page Coder, § Benchmarking). Conteneur : n/a.
- **Observabilité** : spans OTel (`repair_tool_arguments`, spans d'outils), Pydantic Evals pour les trajectoires d'outils. README (L230) ; Coder (L230).
- **Risques notés** : shell non restreint par défaut dans `Coder` ; `unrestricted_filesystem=True` possible ; commandes qui survivent au run.

## 1.3 smolagents (Hugging Face) — https://github.com/huggingface/smolagents

- **Nature** : cadre Python minimal. Deux agents : `ToolCallingAgent` (appels d'outils JSON) et `CodeAgent` (l'agent écrit du Python, `executor_type` ∈ local/blaxel/e2b/modal/docker, `additional_authorized_imports`). https://github.com/huggingface/smolagents/blob/main/src/smolagents/agents.py (L1215, L1505-1535).
- **Licence** : Apache-2.0 (https://github.com/huggingface/smolagents/blob/main/LICENSE).
- **Release / commit** : v1.26.0 le 2026-05-29, v1.25.0 le 2026-05-14 (https://api.github.com/repos/huggingface/smolagents/releases) ; dernier commit 2026-10-06 (`96f33fa`, https://api.github.com/repos/huggingface/smolagents/commits?per_page=1). Aucune release depuis ~5,5 mois.
- **G1** : `OpenAIModel(model_id, api_base=…)` (alias `OpenAIServerModel`), `LiteLLMModel(api_base=…)`, `VLLMModel`, `TransformersModel`, `MLXModel`. https://github.com/huggingface/smolagents/blob/main/src/smolagents/models.py (L633, L1205-1280, L1646-1700). Pas de classe `llama.cpp` : issue ouverte #449 « Add LlamaCppModel Support » (2025-01-31). https://github.com/huggingface/smolagents/issues?q=is%3Aissue%20llama.cpp
- **G2** : aucune télémétrie trouvée dans `README.md` ni `agents.py` (recherche limitée à ces fichiers ; autres fichiers : non vérifié).
- **Modèle d'outils**
  - Liste fermée : `tools=[…]` + agents gérés ; outil inconnu → `AgentToolExecutionError("Unknown tool X, should be one of: …")`. https://github.com/huggingface/smolagents/blob/main/src/smolagents/agents.py (L1453-1467).
  - Validation : `validate_tool_arguments(tool, arguments)` (erreurs `AgentToolCallError`) ; exécution via `tool(**arguments, sanitize_inputs_outputs=True)`. Même fichier (L1474-1500).
  - `tool_choice` : valeur par défaut `"required"` dans le chemin générique des modèles API (`tool_choice: str | dict | None = "required"`, envoyé tel quel dans la requête). https://github.com/huggingface/smolagents/blob/main/src/smolagents/models.py (L510-542).
  - Règle de phase : `step_callbacks` (par type d'étape, appelés **après** l'étape), `final_answer_checks`, `planning_interval`. Pas de hook « avant chaque appel d'outil » trouvé (non exhaustif).
  - Refus d'un shell : pas d'outil shell intégré trouvé dans les fichiers lus ; le `CodeAgent` exécute du Python (exécuteur local par défaut, `executor_type="local"`, L1535). Niveau de sécurité de l'exécuteur local : non évalué.
- **Appels malformés** : si le modèle ne renvoie aucun `tool_calls`, **repli texte** : `model.parse_tool_calls(chat_message)` (`get_tool_call_from_text`) avec `AgentParsingError` en cas d'échec ; sinon `parse_json_if_needed` sur les arguments. https://github.com/huggingface/smolagents/blob/main/src/smolagents/agents.py (L1325-1335) ; models.py (L400, L589). Que l'erreur soit ensuite réinjectée telle quelle dans la mémoire/prompt : non vérifié. `final_answer` avec d'autres appels dans le même tour → erreur explicite (L1340-1352).
- **Annulation** : `interrupt_switch` testé au **début de chaque étape** (`AgentError("Agent interrupted.")`), donc pas d'annulation en cours d'appel modèle. agents.py (L470, L546-547). `max_steps` (20 par défaut).
- **Streaming** : `stream_outputs` + `run(…, stream=True)` retourne un générateur. agents.py (L352, L496, L658). Issue #1872 « Streaming outputs breaks CodeAgent due to incomplete code block termination » (2025-11-17).
- **Appels parallèles** : `ThreadPoolExecutor(max_tool_threads)` quand plusieurs appels dans un tour. agents.py (L1416-1436).
- **MCP** : `MCPClient` ; paramètres stdio, `streamable-http` (défaut), `sse` (déprécié). https://github.com/huggingface/smolagents/blob/main/src/smolagents/mcp_client.py (L30-52). Serena : non vérifié.
- **Contexte** : plafond de sortie d'outil / compaction : non vérifié.
- **Petits modèles** : issue ouverte #1860 « GPT-OSS 20B doesn't generate proper code responses » (2025-11-12). https://github.com/huggingface/smolagents/issues?q=is%3Aissue%20llama.cpp
- **Extension / interface / observabilité** : outils `Tool`, callbacks ; bibliothèque (pas d'UI) ; journaux via `logger`, `monitor`. Détails : non vérifié.
- **Risques notés** : `CodeAgent` = exécution de code généré (sandbox au choix de l'`executor_type`).

## 1.4 LangGraph — https://github.com/langchain-ai/langgraph

- **Nature** : « low-level orchestration framework » pour agents à état (checkpoints, interrupts). Le prébuilt `create_react_agent`/`AgentState` est **déprécié au profit de `langchain.agents`** (« AgentState has been moved to `langchain.agents` »). https://github.com/langchain-ai/langgraph/blob/main/README.md ; https://github.com/langchain-ai/langgraph/blob/main/libs/prebuilt/langgraph/prebuilt/chat_agent_executor.py (L53-65).
- **Licence** : MIT. https://github.com/langchain-ai/langgraph/blob/main/LICENSE
- **Release / commit** : `1.2.20` le 2026-11-05 (https://api.github.com/repos/langchain-ai/langgraph/releases) ; dernier commit 2026-11-11.
- **G1** : le cadre ne parle pas aux modèles lui-même ; il passe par les modèles LangChain. `ChatOpenAI(base_url=…)` existe (cf. issue langchain-ai/langchain#39320 « Responses API auto-routing ignores `base_url` », https://github.com/langchain-ai/langchain/issues?q=is%3Aissue%20llama-server%20tool ). Deep Agents affirme que llama.cpp s'utilise via « any LangChain chat model » (https://github.com/langchain-ai/deepagents/blob/main/README.md, § « Does this work with open-weight or local models? »). Code de `langchain-openai` : non lu.
- **G2** : LangSmith = produit complémentaire optionnel (README) ; le défaut d'activation du tracing : non vérifié.
- **Modèle d'outils** (`ToolNode`)
  - Outil inconnu → message `"Error: {requested_tool} is not a valid tool, try one of [{available_tools}]."` renvoyé au modèle. https://github.com/langchain-ai/langgraph/blob/main/libs/prebuilt/langgraph/prebuilt/tool_node.py (L117).
  - Validation : `ValidationError` Pydantic → `ToolInvocationError`, routé par `handle_tool_errors` (défaut `_default_handle_tool_errors`, personnalisable : bool, str, callable, tuple d'exceptions). Même fichier (L347-410, L757-783, L967-981).
  - Règle de phase : exprimable dans la **structure du graphe** (nœuds, arêtes conditionnelles, état personnalisé) ; `interrupt()` et `interrupt_before/after` pour approbation. https://github.com/langchain-ai/langgraph/blob/main/libs/langgraph/langgraph/types.py (L906-913). Aucun exemple « phase » lu : non testé.
  - Refus d'un shell : aucun outil intégré ; le shell n'existe que si on l'ajoute.
- **Annulation / limites** : `recursion_limit` (erreur « Recursion limit of N reached », `pregel/main.py` L3121). Annulation d'un tour en cours : non vérifié.
- **Streaming** : le prébuilt contient `_tool_call_stream.py` / `_tool_call_transformer.py` ; modes de streaming : non lus.
- **MCP** : pas dans ce dépôt (adaptateur séparé) : non vérifié.
- **Observabilité** : checkpointers (`libs/checkpoint*`), LangSmith (optionnel).
- **Risques notés** : dépendance à LangChain pour le client modèle ; migration en cours des agents prébuilts vers `langchain`.

### Deep Agents (au-dessus de LangGraph) — https://github.com/langchain-ai/deepagents
« The batteries-included agent harness » ; MIT (API) ; `deepagents-code==0.2.7` le 2026-11-10 (https://api.github.com/repos/langchain-ai/deepagents/releases) ; dernier commit 2026-11-12. Contient `libs/code` avec `HOOKS.md`, `THREAT_MODEL.md`, `EXTENSIONS.md`, `PRICING.md` (non lus). Modèles locaux : README « Any model that supports tool calling works … Ollama, vLLM, or llama.cpp » via les modèles LangChain. Tout le reste de la grille : non vérifié.

## 1.5 OpenAI Agents SDK (python) — https://github.com/openai/openai-agents-python

- **Nature** : cadre Python. **Licence** MIT (https://github.com/openai/openai-agents-python/blob/main/LICENSE). **Release** v0.24.0 le 2026-10-15 ; dernier commit 2026-11-11 (https://api.github.com/repos/openai/openai-agents-python/releases/latest).
- **G1 — utilisable avec un endpoint compatible ? Oui, documenté** : `set_default_openai_client(AsyncOpenAI(base_url=…, api_key=…))` ; `OpenAIChatCompletionsModel(model=…, openai_client=client)` ; `set_default_openai_api("chat_completions")` avec `OPENAI_BASE_URL`/`OPENAI_API_KEY`. Le document recommande **un seul « model shape »** par workflow. https://github.com/openai/openai-agents-python/blob/main/docs/models/index.md (L368-422, L674-675). Limites documentées : sorties structurées `json_schema` absentes chez certains fournisseurs (« your app will often break because of malformed JSON », L716-726) ; outils hébergés et plusieurs fonctions Responses rejetés sur Chat Completions (L175). Adaptateurs LiteLLM et any-llm : « best-effort, beta » (L738-758).
- **G2** : le **tracing est actif par défaut** ; `OPENAI_AGENTS_DISABLE_TRACING=1`, `set_tracing_disabled(True)` ou `RunConfig.tracing_disabled`. La doc recommande de le couper quand on n'a pas de clé platform.openai.com. Les traces s'affichent dans le dashboard `platform.openai.com/traces` (destination d'export par défaut déduite de cette phrase, non lue dans le code). `trace_include_sensitive_data` vaut `True` par défaut. https://github.com/openai/openai-agents-python/blob/main/docs/tracing.md (L3-11, L151) ; models/index.md (L379).
- **Modèle d'outils**
  - Liste/contrainte : `tool_choice` (`required`, nom d'outil…), `tool_use_behavior` (`stop_on_first_tool`, `StopAtTools`, fonction), `reset_tool_choice` (défaut `True`). https://github.com/openai/openai-agents-python/blob/main/docs/agents.md (L36-45, L332-447).
  - Validation / règle de phase : **guardrails d'outil** `@tool_input_guardrail` / `@tool_output_guardrail` avec `ToolGuardrailFunctionOutput.reject_content("…")` (message renvoyé au modèle) ou tripwire (`ToolInputGuardrailTripwireTriggered`, interrompt le run) ; `needs_approval` par outil. https://github.com/openai/openai-agents-python/blob/main/docs/guardrails.md (L79-90, L229-251). Les guardrails **ne s'appliquent pas** à `ShellTool`, `ApplyPatchTool`, `LocalShellTool`, `ComputerTool`, ni aux outils hébergés (L80). Accès de la garde à l'historique du tour (pour une règle « build_step avant compilation ») : non vérifié ; l'état peut passer par le `context`.
  - Observation : `RunHooks`/`AgentHooks` `on_tool_start`/`on_tool_end` (docs/agents.md L268-283).
  - Shell : `ShellTool` (local ou conteneur hébergé OpenAI), `ApplyPatchTool`, `LocalShellTool` ; ne sont donc pas des outils par défaut (il faut les ajouter). https://github.com/openai/openai-agents-python/blob/main/docs/tools.md (L6, L189).
- **Appels malformés / relances** : **nom d'outil inconnu → par défaut `ModelBehaviorError` qui interrompt le run** (`RunConfig.tool_not_found_behavior = "raise_error"`) ; l'option `"return_error_to_model"` renvoie `"Tool 'X' not found."` au modèle et relance. https://github.com/openai/openai-agents-python/blob/main/src/agents/run_config.py (L498) ; https://github.com/openai/openai-agents-python/blob/main/src/agents/run_internal/turn_resolution.py (L275-276, L2548-2553). JSON d'arguments invalide : `ModelBehaviorError("Invalid JSON input for tool …")` ; les erreurs d'outils passent par `failure_error_function`, dont la valeur par défaut renvoie un **message fixe** `"An error occurred while running the tool."` sans détail. https://github.com/openai/openai-agents-python/blob/main/src/agents/tool.py (L1895-1902, L1997-2002). Pour que le modèle voie le détail de validation, il faut fournir sa propre fonction.
- **Annulation** : `result.cancel()` (immédiat) ou `cancel(mode="after_turn")` ; sortir de la boucle `async for` **n'annule pas** le run (il continue à appeler modèle et outils). https://github.com/openai/openai-agents-python/blob/main/docs/streaming.md (L59-90). `MaxTurnsExceeded`.
- **Streaming** : ✔ (`docs/streaming.md`).
- **MCP** : stdio (`MCPServerStdio`), Streamable HTTP, SSE, et `HostedMCPTool` (exécuté côté OpenAI Responses, donc inutilisable en local) ; politiques d'approbation ; garde-fous d'outil attachables à un serveur MCP local. https://github.com/openai/openai-agents-python/blob/main/docs/mcp.md (L22-25, L98). Serena : non vérifié.
- **Contexte** : `RunState` reprenable, sessions (`docs/sessions`), « sandbox agents » (docs/sandbox_agents.md, non lu). Adaptation à 32 k : non vérifié.
- **Issues pertinentes** : la recherche « llama.cpp » ne remonte qu'une issue (#1574, `truncation` et gpt-oss, fermée 2025-08-23). https://github.com/openai/openai-agents-python/issues?q=is%3Aissue%20llama.cpp
- **Risques notés** : tracing par défaut vers un service OpenAI ; arrêt du run sur nom d'outil inconnu par défaut ; erreur d'outil opaque par défaut.

## 1.6 Google ADK (python) — https://github.com/google/adk-python

- **Nature** : cadre Python (agents, workflows, runners, CLI `adk`). **Licence** Apache-2.0 (https://github.com/google/adk-python/blob/main/LICENSE). **Release** v2.14.0 le 2026-11-07 ; dernier commit 2026-11-12 (https://api.github.com/repos/google/adk-python/releases/latest).
- **G1** : via le wrapper `LiteLlm` (`src/google/adk/models/lite_llm.py` : paramètres `api_base`/`api_key`, commentaires citant Ollama, LM Studio, vLLM). Pas de provider `llama.cpp` : la seule mention de llama.cpp dans ce fichier concerne le nom `gemma-4` (L1040). https://github.com/google/adk-python/blob/main/src/google/adk/models/lite_llm.py . Issues (LM Studio via LiteLLM) : #6482 « role='tool_responses' for Gemma-4 models breaks tool calling on LM Studio » (fermée 2026-10-07, 9 commentaires), #6334 « wrong tool role for Gemma4 model » (fermée 2026-07-15). https://github.com/google/adk-python/issues?q=is%3Aissue%20llama.cpp
- **G2** : le **CLI `adk`** envoie des métriques d'usage à `https://play.googleapis.com/log` (Clearcut, `log_source` 3007) ; consentement stocké dans `~/.adk/config.json` ; si aucune préférence, le CLI demande `Enable telemetry? [Y/n]` ; `adk telemetry disable`. https://github.com/google/adk-python/blob/main/src/google/adk/cli/_telemetry/_metrics_reporter.py (L38-43, L218) ; https://github.com/google/adk-python/blob/main/src/google/adk/cli/cli_tools_click.py (L421-466) ; https://github.com/google/adk-python/blob/main/src/google/adk/utils/_telemetry_config.py. Effet sur l'usage en bibliothèque (sans le CLI) : non vérifié.
- **Modèle d'outils**
  - Callbacks d'agent : `before_tool_callback`, `after_tool_callback`, `on_tool_error_callback` sur `LlmAgent`. https://github.com/google/adk-python/blob/main/src/google/adk/agents/llm_agent.py (L553-587). Sémantique de retour (court-circuit de l'outil) : non lue.
  - Validation : `FunctionTool` prétraite, valide et convertit les arguments (types primitifs, enums, conteneurs, modèles Pydantic). https://github.com/google/adk-python/blob/main/src/google/adk/tools/function_tool.py (L289-318) ; …/tools/base_tool.py (L263-276).
  - Refus d'un shell : aucun shell dans le cœur trouvé (non exhaustif).
- **Appels malformés / relances** : plugin `ReflectRetryToolPlugin` (réflexion + relance sur erreur d'outil ; son prompt cite « Wrong Function Name … only use available tools »). https://github.com/google/adk-python/blob/main/src/google/adk/plugins/reflect_retry_tool_plugin.py (L481). Comportement par défaut sur nom inconnu : non vérifié.
- **Annulation** : le runner annule la tâche racine quand le consommateur sort tôt de la boucle ; API d'annulation d'un tour dédiée : non vérifiée. https://github.com/google/adk-python/blob/main/src/google/adk/runners.py (L845-864).
- **Streaming** : non lu.
- **MCP** : `McpToolset` avec `StdioConnectionParams`, `SseConnectionParams`, `StreamableHTTPConnectionParams`. https://github.com/google/adk-python/blob/main/src/google/adk/tools/mcp_tool/mcp_session_manager.py (L321-526). Serena : non vérifié.
- **Risques notés** : télémétrie du CLI proposée à la première commande ; paquet orienté Gemini/Vertex par défaut (les modèles locaux passent par LiteLLM).

## 1.7 Strands Agents — https://github.com/strands-agents/harness-sdk (ex `sdk-python`)

- **Nature** : SDK Python et TypeScript « for building and running AI agents » ; le dépôt est un monorepo (`strands-py`, `strands-ts`, `harness-py`/`harness-ts` = agent « entièrement assemblé » via `create_harness()`, `strands-cli`, `strands-mcp` = serveur MCP de documentation). https://github.com/strands-agents/harness-sdk/blob/main/README.md . Le harness et le CLI n'ont pas été examinés.
- **Licence** : Apache-2.0 (`LICENSE.APACHE`). **Release** `python/v1.64.0` le 2026-11-04 ; `harness-python/v0.3.4` le 2026-11-04 ; `harness-cli/v0.3.0` le 2026-11-10 (https://api.github.com/repos/strands-agents/harness-sdk/releases). Dernier commit 2026-11-11.
- **G1** : **provider natif `LlamaCppModel(base_url="http://localhost:8080")`** avec paramètres propres à llama.cpp (`grammar`, `json_schema`, mirostat, `slot_id`, `cache_prompt`). https://github.com/strands-agents/harness-sdk/blob/main/strands-py/src/strands/models/llamacpp.py (L85-171, L449-453). **`tool_choice` est ignoré** par ce provider (« accepted for interface consistency but is currently ignored », avertissement émis). Même fichier (L634-654). Sans modèle explicite, `Agent()` instancie `BedrockModel()` (AWS) : https://github.com/strands-agents/harness-sdk/blob/main/strands-py/src/strands/agent/agent.py (L408).
- **G2** : télémétrie OTel **opt-in** (`OTEL_EXPORTER_OTLP_ENDPOINT`, `telemetry/config.py`). Aucune télémétrie éditeur trouvée (non exhaustif).
- **Modèle d'outils**
  - Hook `BeforeToolCallEvent` : `selected_tool` modifiable, `cancel_tool: bool | str` (« A user defined message that when set, will cancel the tool call ») → règle de phase possible nativement. https://github.com/strands-agents/harness-sdk/blob/main/strands-py/src/strands/hooks/events.py (L226-242).
  - « Interventions » : actions `Proceed`, `Deny` (« The reason is shown to the model as the cancellation message »), confirmation humaine. https://github.com/strands-agents/harness-sdk/blob/main/strands-py/src/strands/interventions/actions.py ; répertoire `vended_interventions`.
  - Outil inconnu : résultat d'erreur `"Unknown tool: X"` ; la chaîne de middleware s'exécute quand même. https://github.com/strands-agents/harness-sdk/blob/main/strands-py/src/strands/tools/executors/_executor.py (L290-296, L673-684). Un nom d'outil invalide est remplacé dans le flux (`event_loop/streaming.py` L91-117).
  - Refus d'un shell : le SDK n'ajoute pas de shell ; dépôts frères `strands-agents/shell` et `box` cités dans le README (non examinés).
- **Appels malformés** : issue ouverte #2051 (2026-04-04) « Malformed tool input JSON silently replaced with empty dict, no logging » (python, `area-tool`). https://github.com/strands-agents/harness-sdk/issues?q=is%3Aissue%20llama.cpp . Politique de relance au-delà : non vérifié.
- **Annulation** : `agent.cancel(message=…, after_current_tools=…)` → `stop_reason="cancelled"` ; `cancel_signal` (threading.Event) passable à l'invocation ; le README liste « turn limits, token budgets, cancellation, stop reasons ». https://github.com/strands-agents/harness-sdk/blob/main/strands-py/src/strands/agent/agent.py (L141, L489, L680-705).
- **Streaming** : ✔ (événements `StreamEvent`). Issues du provider llama.cpp : #5490 « LlamaCppModel buffers streamed responses until HTTP EOF » (ouverte, 2026-10-24) ; #5428 « reports tool_use instead of max_tokens when a tool call is cut off by max_tokens » (ouverte, 2026-10-22) ; #3902 « drops the trailing usage chunk after finish_reason » (fermée 2026-08-25) ; #3422 « llama.cpp sampling params are nested under extra_body and silently dropped over raw httpx » (fermée 2026-07-23). https://github.com/strands-agents/harness-sdk/issues?q=is%3Aissue%20llama.cpp
- **MCP** : sous-package `tools/mcp` ; transports : non lus.
- **Contexte** : `ContextWindowOverflowException` géré par le provider llama.cpp ; compactage/`context_manager` présents (non lus). Issue #2052 (fermée 2026-06-26) : Ollama, Mistral, LlamaAPI, Writer manquaient de `ContextWindowOverflowException`.
- **Risques notés** : `tool_choice` ignoré avec llama.cpp ; arguments d'outil illisibles remplacés par `{}` sans journal (issue ouverte) ; modèle par défaut = Bedrock.

## 1.8 Mastra — https://github.com/mastra-ai/mastra

- **Nature** : cadre TypeScript (agents, workflows, outils, mémoire, serveur, Studio) ; fonction `createCodingAgent()` (`@mastra/core` ≥ 1.48.0) qui assemble un agent de code avec **workspace local, signaux de tâche, retries réseau, goal judge**. https://github.com/mastra-ai/mastra/blob/main/docs/src/content/en/reference/coding-agent/create-coding-agent.mdx . Le produit « Mastra Code » n'est pas inclus (son prompt, modes et outils).
- **Licence** : Apache-2.0 pour tout sauf les dossiers `ee/` (`@mastra/core/auth/ee`, `agent-builder/ee`, `editor/ee`…) sous « Mastra Enterprise Edition License v2.0 » (effective 2026-09-22, texte non lu en entier). https://github.com/mastra-ai/mastra/blob/main/LICENSE.md ; https://github.com/mastra-ai/mastra/blob/main/ee/LICENSE . L'API GitHub renvoie `NOASSERTION`.
- **Release / commit** : `@mastra/core@1.82.0` le 2026-11-04 (https://api.github.com/repos/mastra-ai/mastra/releases) ; dernier commit 2026-11-12.
- **G1** : `model: { id, url: "http://…/v1" }` pour tout endpoint OpenAI-compatible ; exemple LM Studio `http://localhost:1234/v1` ; la doc recommande LM Studio. Pas de mention de `llama-server`. https://github.com/mastra-ai/mastra/blob/main/docs/src/content/en/models/index.mdx (L346-443).
- **G2** : par défaut Mastra collecte de la télémétrie (OS, versions, événements serveur `mastra_feature_usage`, `mastra_model_token_usage_v2` toutes les 15 min, avec `project_id` = hash du chemin et `project_id2` = hash du remote Git) ; la doc précise que **ces événements ne sont pas anonymes** ; coupure par `MASTRA_TELEMETRY_DISABLED` (documentée pour le Studio ; la coupure des événements serveur par cette variable : formulation de la page lue seulement pour le Studio). https://github.com/mastra-ai/mastra/blob/main/docs/src/content/en/reference/cli/mastra.mdx (L2160-2180).
- **Modèle d'outils**
  - Schémas Zod `inputSchema`/`outputSchema` ; si l'entrée viole `inputSchema`, l'erreur de validation est renvoyée au modèle sans demande d'approbation. https://github.com/mastra-ai/mastra/blob/main/docs/src/content/en/reference/tools/create-tool.mdx (L112, L148-155).
  - Liste/phase : options d'appel `activeTools` (liste des outils actifs), **`prepareStep`** (callback avant chaque étape), `toolChoice`, `requireToolApproval` ; hook par outil avant l'approbation (`{ proceed:false, output }` rejette l'appel). https://github.com/mastra-ai/mastra/blob/main/docs/src/content/en/reference/agents/generate.mdx (L338-372) ; create-tool.mdx (L155).
  - Refus d'un shell : `createCodingAgent` : « The default workspace runs commands on the host machine with the permissions of your application process » ; sandbox interchangeable (E2B…). create-coding-agent.mdx.
- **Appels malformés / relances** : validation Zod ci-dessus ; processeurs d'erreurs réseau dans `createCodingAgent` ; comportement sur nom d'outil inconnu et sur JSON illisible : non vérifié.
- **Annulation** : `abortSignal` (y compris les sous-agents en cours). https://github.com/mastra-ai/mastra/blob/main/docs/src/content/en/reference/streaming/agents/stream.mdx (L352, L978-982).
- **Streaming** : ✔ (`agent.stream`). Détails avec llama-server : non vérifié.
- **MCP** : `MCPClient` : `command` → stdio ; `url` → Streamable HTTP. https://github.com/mastra-ai/mastra/blob/main/docs/src/content/en/reference/tools/mcp-client.mdx (L217-218). Serena : non vérifié.
- **Issues locales** : #15234 « Skills cause "Assistant response prefill is incompatible with enable_thinking" with Qwen 3.5 » (fermée 2026-04-20). https://github.com/mastra-ai/mastra/issues?q=is%3Aissue%20llama.cpp
- **Windows** : non vérifié.
- **Risques notés** : télémétrie par défaut non anonyme côté serveur ; code `ee/` sous licence propriétaire ; commandes du workspace sur l'hôte avec les droits du processus.

## 1.9 Agno — https://github.com/agno-agi/agno

- **Nature** : cadre Python (agents, teams, workflows, AgentOS). **Licence** Apache-2.0. **Release** v3.1.12 le 2026-10-29 ; dernier commit 2026-11-12 (https://api.github.com/repos/agno-agi/agno/releases/latest).
- **G1** : classe native **`LlamaCpp(OpenAILike)`**, `base_url` par défaut `http://127.0.0.1:8080/v1`, `id` par défaut `ggml-org/gpt-oss-20b-GGUF`. https://github.com/agno-agi/agno/blob/main/libs/agno/agno/models/llama_cpp/llama_cpp.py . Autres : `OpenAILike`, `LMStudio`, `Ollama`, `vLLM`. Note : le serveur actuel documente le port 9931 (voir § 2d), pas 8080.
- **G2** : **`telemetry: bool = True` par défaut** (https://github.com/agno-agi/agno/blob/main/libs/agno/agno/agent/agent.py L398-400) ; la variable `AGNO_TELEMETRY` écrase le champ : `agent.telemetry = (valeur.lower() == "true")` — toute valeur autre que `true` coupe, y compris `false`/`0` (https://github.com/agno-agi/agno/blob/main/libs/agno/agno/agent/_init.py L62-67). Endpoint d'API `https://os-api.agno.com` (https://github.com/agno-agi/agno/blob/main/libs/agno/agno/api/settings.py L57). Issue fermée #8181 (2026-09-21) : « Telemetry is blocking (synchronous) and adds ~1s latency on every `agent.run()` — undocumented, opt-out not mentioned ». https://github.com/agno-agi/agno/issues?q=is%3Aissue%20llama.cpp
- **Modèle d'outils**
  - Paramètres d'agent : `tool_call_limit`, `tool_choice`, `tool_hooks`, `pre_hooks` (L199-213). https://github.com/agno-agi/agno/blob/main/libs/agno/agno/agent/agent.py
  - Outil inconnu : `log_error("Function X not found")` et retour `None` ; ce que voit le modèle : non vérifié. https://github.com/agno-agi/agno/blob/main/libs/agno/agno/utils/functions.py (L18-24).
  - Arguments : `json.loads`, repli `ast.literal_eval` ; en cas d'échec, `function_call.error = "Error while decoding function arguments … Please make sure we can json.loads() the arguments and retry."` ; les arguments non-objet sont refusés. **Toute valeur chaîne `"none"`/`"null"`/`"true"`/`"false"` est convertie en `None`/`True`/`False`** (même fichier, L26-70), y compris pour un argument légitimement textuel. Validation du schéma des paramètres : non vérifié.
  - Refus d'un shell / règle de phase : `tool_hooks` et `pre_hooks` existent ; sémantique de blocage : non lue.
- **Annulation** : `Agent.cancel_run(run_id)`. agent.py (L910-911). **Streaming** : non lu. **MCP** : `agno/tools/mcp` (stdio, SSE, Streamable HTTP : `StreamableHTTPClientParams`, `SSEClientParams`).
- **Issues** : #5106 « Tool calls not parsed correctly with v2 » (fermée 2026-07-16, 12 commentaires, « stale ») ; #3594 « content: None raises errors in local LLM frameworks » (fermée 2025-06-24) ; #4246 « In the case of "OpenAI-like" models, the agent doesn't seem to take into account the instructions or system messages » (fermée 2025-08-19) ; #7493 « Gemma 4: Interleaved reasoning (<|channel> delimiters) leakage/parsing failure » (fermée 2026-04-14). https://github.com/agno-agi/agno/issues?q=is%3Aissue%20llama.cpp (contenus non lus).
- **Risques notés** : télémétrie par défaut ; coercition silencieuse de chaînes en booléens/None.

## 1.10 Autres cadres

### Pi — https://github.com/earendil-works/pi (ancien `badlogic/pi-mono`)
- **Nature** : « minimal, extensible agent harness » TypeScript : paquets `ai` (API LLM unifiée), `agent` (boucle d'agent), `coding-agent` (CLI), `mcp`, `tui`, `telemetry` (contrats seulement), `codemode`. Le README dit qu'il **saute volontairement sous-agents et mode plan**. https://github.com/earendil-works/pi/blob/main/README.md . MIT ; v1.5.2 le 2026-11-10 (https://api.github.com/repos/badlogic/pi-mono/releases) ; dernier commit 2026-11-12.
- **G1** : « Any OpenAI-compatible API: Ollama, vLLM, LM Studio, etc. » (packages/ai/README.md L98) ; **documentation dédiée llama.cpp** : routeur `llama serve`, `/login llama.cpp`, URL par défaut `http://127.0.0.1:9931`, variables `LLAMA_BASE_URL`/`LLAMA_API_KEY`. https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/llama-cpp.md
- **G2** : `enableInstallTelemetry` vaut `true` par défaut (« anonymous install/update reporting and selected provider attribution headers », ne contrôle pas les contrôles de mise à jour) ; coupure `PI_TELEMETRY=0` ou réglage. https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/settings.md (L166-171) ; …/src/cli/args.ts (L467). Contenu exact envoyé : non lu.
- **Outils** : boucle `agent-loop.ts` : outil inconnu → résultat d'erreur `"Tool X not found"` (L730), arguments validés par `validateToolArguments` avant `beforeToolCall` (qui peut bloquer, avec `terminate: true`) ; `afterToolCall` ; `toolExecution: parallel|sequential`. https://github.com/earendil-works/pi/blob/main/packages/agent/src/agent-loop.ts ; https://github.com/earendil-works/pi/blob/main/packages/agent/README.md (L111-122). Politique de relance sur JSON malformé : non lue.
- **MCP** : paquet `mcp` : client propre (sans SDK officiel) : transports stdio et Streamable HTTP. https://github.com/earendil-works/pi/blob/main/packages/mcp/README.md
- **Issues locales** : #11573 « The codemode annotation spells `tools.`, and small local models copy `tools.` into the tool-call name » (fermée 2026-10-29) ; #10885 « Context overflow from llama.cpp server ("Context size has been exceeded.") is not detected, so auto-compaction never triggers » (ouverte, 2026-10-13) ; #11472 « rpc mode: "turn_end could not resolve the persisted assistant entry ID" aborts every run with local openai-completions providers » (fermée 2026-10-27) ; #11200 « processResponsesStream crashes when function_call_arguments.done omits arguments » (fermée 2026-10-21). https://github.com/badlogic/pi-mono/issues?q=is%3Aissue%20llama.cpp
- Reste de la grille (annulation, compactage, sandbox, Windows) : non vérifié. Le README mentionne l'installeur Windows PowerShell.

### Table réduite des autres cadres (peu ou pas approfondis)

| Cadre | Licence | Dernière release (date) | Faits vérifiés | Non vérifié |
|---|---|---|---|---|
| LangChain (`langchain-ai/langchain`) | MIT | `langchain==1.5.0` (2026-11-11) | `create_agent`/`AgentState` vivent dans `langchain.agents` (message de dépréciation de LangGraph) | middleware d'outils, `base_url`, télémétrie |
| Microsoft Agent Framework | MIT | `python-1.25.0` (2026-11-07) | README : OpenTelemetry intégré | G1, outils, annulation, G2 |
| OpenAI Agents SDK JS | MIT | `v0.22.0-alpha.2` (2026-11-08, alpha) | — | tout le reste |
| Vercel AI SDK | Apache-2.0 (texte de `LICENSE` ; API : NOASSERTION) | `ai@7.0.170` (2026-11-11) | licence | tout le reste |
| CrewAI | MIT | `1.15.40` (2026-11-11) | README § Telemetry : **télémétrie anonyme par défaut**, `share_crew=True` ajoute des données détaillées ; modèles par défaut = API OpenAI | G1 llama-server, méthode de coupure, outils |
| Haystack (deepset) | Apache-2.0 | `v3.5.0` (2026-11-10) | licence, release | tout le reste |
| LlamaIndex | MIT | `v0.14.25` (2026-09-21) | licence, release | tout le reste |

Sources : `https://api.github.com/repos/<org>/<repo>` et `…/releases` pour ces dépôts (`langchain-ai/langchain`, `microsoft/agent-framework`, `openai/openai-agents-js`, `vercel/ai`, `crewAIInc/crewAI`, `deepset-ai/haystack`, `run-llama/llama_index`) ; https://raw.githubusercontent.com/microsoft/agent-framework/main/README.md ; https://raw.githubusercontent.com/crewAIInc/crewAI/main/README.md (L538, L590-619) ; https://raw.githubusercontent.com/vercel/ai/main/LICENSE.

Non examinés du tout : Semantic Kernel, AutoGen (l'API GitHub a répondu 403 pendant la collecte), DSPy, Letta, Goose, etc.

---

# Partie 2 — Tool-calling avec petits modèles

## 2a. Comment `llama-server` gère le function calling

Sources : https://github.com/ggml-org/llama.cpp/blob/master/docs/function-calling.md ; https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md ; https://github.com/ggml-org/llama.cpp/blob/master/common/chat.cpp ; https://github.com/ggml-org/llama.cpp/blob/master/docs/autoparser.md ; et les mêmes fichiers au tag `b10216` (`https://github.com/ggml-org/llama.cpp/blob/b10216/<chemin>`).

**Versions**
- `b10216` : publié le 2026-07-31T22:04:52Z (« vulkan: add POOL_1D op »). https://github.com/ggml-org/llama.cpp/releases/tag/b10216
- Plus récent vu : `b12318` le 2026-11-12 11:36 (pré-release). https://github.com/ggml-org/llama.cpp/releases
- L'API GitHub marque comme « latest » le tag `v0.9.0` (2026-11-04) ; la signification de ces tags `v0.x` à côté des `bNNNN` n'est pas expliquée dans les pages lues (non vérifié). Un bot de pydantic-ai parle de « llama.cpp 0.7.0 » (issue #11244). https://api.github.com/repos/ggml-org/llama.cpp/releases/latest

**`--jinja` et gabarits**
- La doc : le function calling OpenAI-compatible de `llama-server` est activé par `--jinja` ; il faut un gabarit Jinja compatible outils (vérifiable dans `/props`, champs `chat_template` / `chat_template_tool_use`). `--chat-template-file` pour surcharger ; en dernier recours `--chat-template chatml`. https://github.com/ggml-org/llama.cpp/blob/master/docs/function-calling.md (intro, § Usage).
- **`--jinja` est « default: enabled » dans le README serveur, y compris au tag b10216** (`| --jinja, --no-jinja | … (default: enabled)`). https://github.com/ggml-org/llama.cpp/blob/b10216/tools/server/README.md (L225) ; master (L237). La doc `function-calling.md` écrit encore `llama-server --jinja …` dans ses exemples.
- Formats « natifs » listés par la doc : Llama 3.1/3.3/3.2, Functionary v3.1/v3.2, **Hermes 2/3, Qwen 2.5, Qwen 2.5 Coder**, Mistral Nemo, Firefunction v2, Command R7B, DeepSeek R1 (« WIP / seems reluctant to call any tools? »), GPT-OSS (Harmony), LLM-jp-4.1. Sinon format **Generic** (« you'll see `Chat format: Generic` in the logs », « may consume more tokens and be less efficient »). Le tableau gabarit → format range `Qwen-Qwen2.5-Coder-7B-Instruct` et `…32B-Instruct` sous « Hermes 2 Pro » ; **le 14B Coder n'a pas de ligne dans ce tableau**. https://github.com/ggml-org/llama.cpp/blob/master/docs/function-calling.md (L10-100)
- **Écart doc/code** : sur `master`, `common/chat.h` énumère `COMMON_CHAT_FORMAT_CONTENT_ONLY`, `PEG_SIMPLE`, `PEG_NATIVE`, `PEG_GEMMA4`, `PEG_MINIMAX_M3` ; l'analyse de gabarit se fait par un « auto-parser » différentiel (`docs/autoparser.md` : « analyzes chat templates to determine how to parse model outputs, including content, reasoning, and tool calls », construit un parseur PEG « and optional GBNF grammar »). Le tableau « Hermes 2 Pro / Generic… » de `function-calling.md` n'est donc pas la description du code actuel. https://github.com/ggml-org/llama.cpp/blob/master/common/chat.h (L242-250) ; https://github.com/ggml-org/llama.cpp/blob/master/docs/autoparser.md . Au tag b10216 `chat.cpp` contient déjà `autoparser::` (L889).
- Gestionnaires spécialisés présents sur master et **absents de `chat.cpp` au tag b10216** (0 occurrence de « qwen3 » à b10216, 3 sur master) : détection « Qwen3-Coder XML tool calls, also used by Nemotron Nano 3, Qwen3.5 and StepFun-3.5-Flash » (master, `chat.cpp` L1432-1439), Gemma4, DeepSeek V3.2/V4, MiniMax-M3, MiniCPM5. Comment b10216 traite un gabarit Qwen3-Coder (autoparser générique ?) : non vérifié.

**Appels parallèles**
- « Multiple/parallel tool calling is supported on some models but disabled by default, enable it by passing `"parallel_tool_calls": true` in the completion endpoint payload » ; le README serveur ajoute « only supported on some models, verification is based on jinja template ». https://github.com/ggml-org/llama.cpp/blob/master/docs/function-calling.md ; …/tools/server/README.md (L1458).

**Grammaires et contraintes**
- Paramètres de sampling `grammar` (GBNF) et `json_schema` ; `response_format` accepte `json_object`, `json_schema` (avec ou sans enveloppe OpenAI). https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md (L583-585, L1440-1446)
- **`grammar` + `tools` incompatibles** : `throw std::runtime_error("Cannot specify grammar with tools")` si `tool_choice != none` et une grammaire est fournie. Présent à b10216 (L3093) et sur master. https://github.com/ggml-org/llama.cpp/blob/b10216/common/chat.cpp
- `tool_choice` accepte `auto`, `none`, `required`, sinon `Invalid tool_choice` (chat.cpp, `common_chat_tool_choice_parse_oaicompat`). L'API Anthropic compatible accepte aussi `{"type":"tool","name":…}` (README L1847-1849).
- **Grammaire paresseuse** (« lazy grammar ») avec déclencheurs : à b10216, `grammar_lazy = has_tools && tool_choice == AUTO` dans un des chemins (L1090) ; dans un autre, `!(response_format || (has_tools && tool_choice == REQUIRED))` (L1254). Autrement dit en `auto` la contrainte ne s'applique qu'après détection du début d'un appel ; en `required` elle est active d'emblée. https://github.com/ggml-org/llama.cpp/blob/b10216/common/chat.cpp
- Avertissement du code : « Template supports tool calls but does not natively describe tools. The fallback behaviour used may produce bad results, inspect prompt w/ --verbose & consider overriding the template. » (master `chat.cpp`, après le bloc `params.parallel_tool_calls`).
- Mise en garde de la doc : « Beware of extreme KV quantizations (e.g. `-ctk q4_0`), they can substantially degrade the model's tool calling performance. » (b10216 L333 ; master identique).

**Autres éléments serveur (version master)**
- `--tools` (outils intégrés expérimentaux pour le Web UI : `read_file`, `file_glob_search`, `grep_search`, `exec_shell_command`, `write_file`, `edit_file`, `get_info`), `--tools-runtime docker|podman|ssh`, `--agent`, `--allow-unauthenticated-tools`, proxy/stdio MCP côté serveur (PR #26062, « Only the stdio transport is supported »). `--tools` existe déjà au tag b10216 (README L201) ; je n'ai pas trouvé `--tools-runtime` ni la section MCP dans le README de b10216 (non exhaustif). https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md (L205-210, L357-403)
- Raisonnement : `--reasoning-format`, `--reasoning on|off|auto`, `reasoning_content`, `--reasoning-budget`, `--skip-chat-parsing` (sortie « pure content » avec appels d'outils dans le texte). README (L238-246).
- Port d'exemple des docs actuelles : **9931** (`curl http://localhost:9931/v1/chat/completions`), alors que les docstrings de Strands et la valeur par défaut d'Agno disent 8080. README (L1480-1500) ; function-calling.md (L289-360).

**Issues du dépôt llama.cpp liées au tool-calling** (voir aussi § 2d)
- #12279 (mars 2025, build 4856) : https://github.com/ggml-org/llama.cpp/issues/12279 — détail en § 2b.
- #13825 « Eval bug: Uncaught exception [json.exception.parse_error.101] during tool use crashes llama-server » (2025-05-27, build 5505, fermée « stale »). https://github.com/ggml-org/llama.cpp/issues/13825
- #14697 « Regression: Tool calls still returned in content field as JSON string instead of tool_calls array » (Devstral-Small-2507 Q8, build 5894, fermée « stale » 2026-10-25). https://github.com/ggml-org/llama.cpp/issues/14697
- #19009 « GLM 4.7 "Template supports tool calls but does not natively describe tools." » (labels bug, chat parser, regression ; fermée 2026-02-04). https://github.com/ggml-org/llama.cpp/issues?q=is%3Aissue%20Qwen2.5-Coder%20tool%20call
- #15012 « Feature Request: Qwen3-Coder Tool Call Parser » (fermée « stale » 2025-11-18, 43 commentaires). Même liste.

## 2b. Fiabilité du tool-calling de Qwen2.5-Coder-14B-Instruct et de sa classe

**Ce que disent les sources primaires de Qwen**
- Carte du modèle `Qwen/Qwen2.5-Coder-14B-Instruct` : met en avant la génération/le raisonnement/la correction de code et « a more comprehensive foundation for real-world applications such as Code Agents » ; contexte 131 072 jetons, `config.json` réglé à 32 768 (YaRN statique recommandé seulement pour les longs contextes, avec impact possible sur les textes courts) ; **aucune section function calling, aucun score de tool-use** sur la page. https://huggingface.co/Qwen/Qwen2.5-Coder-14B-Instruct
- Le `chat_template` de `tokenizer_config.json` du modèle **contient** un bloc d'outils de style Hermes (`<tools></tools>` dans le prompt système, appels attendus dans `<tool_call>{"name": …, "arguments": …}</tool_call>`). Vérifié par téléchargement. https://huggingface.co/Qwen/Qwen2.5-Coder-14B-Instruct/raw/main/tokenizer_config.json
- Blog Qwen2.5-Coder (2024-11-12) : benchmarks de génération (EvalPlus, LiveCodeBench, BigCodeBench), réparation (Aider 73.7 pour le 32B), raisonnement, multilingue, complétion ; licence Apache-2.0 pour 0.5B/1.5B/7B/14B/32B ; **aucun résultat de tool-calling ou de BFCL** sur la page lue. https://qwenlm.github.io/blog/qwen2.5-coder-family/
- Documentation Qwen « Function Calling » : rédigée pour **Qwen3** ; recommande le tool use de style Hermes ; conclut : « It is not guaranteed that the model generation will always follow the protocol even with proper prompting or templates … In production code, be prepared that if it breaks, countermeasures or rectifications are in place » ; déconseille les gabarits à mots d'arrêt (ReAct) pour les modèles à raisonnement. Cette page ne dit rien de Qwen2.5-Coder. https://qwen.readthedocs.io/en/latest/framework/function_call.html
- Rapport technique Qwen2.5-Coder (arXiv 2409.12186) : non lu → section tool-use : non vérifié. https://arxiv.org/abs/2409.12186

**Berkeley Function-Calling Leaderboard (BFCL)**
- Données officielles `https://gorilla.cs.berkeley.edu/data_overall.csv` (109 lignes) ; page `https://gorilla.cs.berkeley.edu/leaderboard.html` : « Last Updated: 2026-04-12 ».
- **Aucune ligne `Qwen2.5-Coder-*` ni `Qwen2.5-*` dans ce fichier.** Absents aussi : `gpt-oss`, `Devstral`, `Qwen3-Coder`, `Qwen3.8`, `GLM-4.7-Flash` (recherche par nom dans le CSV).
- Lignes Qwen présentes (score global ; multi-tour ; AST non-live) : Qwen3-32B (FC) 48,71 % (rang 29 ; 47,87 % ; 88,77 %) ; Qwen3-32B (Prompt) 46,78 % (rang 33) ; Qwen3-30B-A3B-Instruct-2507 (FC) 41,39 % (rang 41 ; 30,00 % ; 85,77 %) ; (Prompt) 36,70 % ; Qwen3-14B (FC) 41,03 % (rang 43 ; 34,75 %) ; (Prompt) 37,77 % ; Qwen3-8B (FC) 42,57 % ; Qwen3-4B-Instruct-2507 (FC) 35,68 % ; Qwen3-235B-A22B-Instruct-2507 (Prompt) 52,15 % (rang 23) mais **(FC) 47,99 % avec AST non-live à 37,40 % contre 90,33 % en Prompt** : l'écart FC/Prompt de ce modèle est de plus de 50 points sur la catégorie AST non-live.
- Lecture des colonnes : le multi-tour (`Multi Turn Acc`) est nettement plus bas que le non-live pour toute la classe ≤ 32B (ex. Qwen3-30B-A3B-Instruct-2507 FC : 30,00 % contre 85,77 %).
- Ce que ça ne permet pas de dire : le niveau du 14B Coder sur BFCL (pas de ligne). Sources : https://gorilla.cs.berkeley.edu/data_overall.csv ; https://gorilla.cs.berkeley.edu/leaderboard.html

**Retours d'usage primaires (issues)**
- llama.cpp #12279 (mars 2025) avec Qwen2.5-Coder **7B** `unsloth/…-128K-GGUF` : ids d'appel vides (corrigé par le PR #12292), `content` manquant (PR #12293), et surtout, après un résultat d'outil, la réponse était `"<tool_response>\n8.17.3\n</tool_response>"` au lieu de conclure ; contournement : `--repeat-penalty 1.2` (puis 1.1) ; le mainteneur Ochafik constate que le **32B** (`unsloth/Qwen2.5-Coder-32B-Instruct-128K-GGUF`) « is doing fine » alors que le 7B « struggles w/ repetitions » ; ggerganov obtient la bonne réponse avec le 7B non fine-tuné quantifié en Q4_K et échantillonnage glouton, et soupçonne le fine-tune/les paramètres RoPE de la variante Unsloth. https://github.com/ggml-org/llama.cpp/issues/12279 (commentaires 2025-03-10 à 2025-03-13). Rien de comparable lu pour le 14B.
- Le même PR #12034 (cité dans l'issue) s'intitule « `tool-call`: fix Qwen 2.5 Coder support, add micro benchmarks, support trigger patterns for lazy grammars ».

## 2c. Modèles locaux récents (≤ 32B, GGUF disponibles) réputés pour le tool-calling en agent de code

Aucune source primaire indépendante comparant ces modèles avec `llama-server` n'a été trouvée : **les chiffres ci-dessous sont des auto-déclarations des cartes de modèles**. Tailles lues dans l'API Hugging Face (`safetensors.total`) ; dates de création/dernière modif idem. Les GGUF cités sont ceux trouvés par recherche sur l'API Hugging Face (téléchargements indiqués par l'API).

| Modèle (carte primaire) | Taille / licence | Ce que dit la carte | GGUF vus | Notes llama.cpp |
|---|---|---|---|---|
| **Qwen3.8-27B** — https://huggingface.co/Qwen/Qwen3.8-27B (créé 2026-08-05, maj 2026-11-07) | 27,8 B dense ; Apache-2.0 ; vision-langage | Tableau agentique : Terminal Bench 2.1 (Terminus) 73,0 (Qwen3.6-27B : 63,4) ; SWE-bench Pro 61,7 (53,5) avec le harness Claude Code, 256 K de contexte ; remarque : en tâches agentiques multi-tours un effort de raisonnement faible « can also lead to insufficient analysis, more failures, and repeated retries » ; recommande une longueur de sortie suffisante | `unsloth/Qwen3.8-27B-GGUF` (≈ 6,1 M téléchargements) | la carte ne mentionne ni llama.cpp ni parseur d'outils |
| **Qwen3-Coder-30B-A3B-Instruct** — https://huggingface.co/Qwen/Qwen3-Coder-30B-A3B-Instruct (2025-07-31) | 30,5 B MoE ; Apache-2.0 | « Qwen3-Coder excels in tool calling capabilities » ; « specially designed function call format » (Qwen Code, Cline) | non listé dans la recherche ciblée | gestionnaire XML Qwen3-Coder sur master, absent de `chat.cpp` à b10216 (voir § 2a) ; issue #15012 (feature request de parseur) |
| **Devstral-Small-2-24B-Instruct-2512** — https://huggingface.co/mistralai/Devstral-Small-2-24B-Instruct-2512 (2025-11-28, maj 2026-07-15) | 24 B ; Apache-2.0 | SWE-bench Verified 68,0 %, SWE-bench Multilingual 55,7 %, Terminal Bench 2 : 22,5 % (auto-déclaré) ; « excels at using tools to explore codebases, editing multiple files » ; tool calling pris en charge | GGUF communautaires Unsloth et Bartowski cités par la carte | la carte exige les changements du PR llama.cpp #17945 pour ces GGUF ; issue #14697 (Devstral Small 2507 : appels renvoyés dans `content`) |
| **GLM-4.7-Flash** — https://huggingface.co/zai-org/GLM-4.7-Flash (2026-01-19) | 31,2 B ; MIT | SWE-bench Verified 59,2, τ²-Bench 79,5 (GPT-OSS-20B : 34,0 / 47,7 ; Qwen3-30B-A3B-Thinking-2507 : 22,0 / 49,0) ; « Preserved Thinking mode » conseillé pour le multi-tour | non cherché | issue llama.cpp #19009 (GLM 4.7 « does not natively describe tools », fermée 2026-02-04) |
| **gpt-oss-20b** — https://huggingface.co/openai/gpt-oss-20b (2025-08-04) | 20,9 B ; Apache-2.0 | « native capabilities for function calling, web browsing, Python code execution, and Structured Outputs » | — | format Harmony listé « natif » par la doc llama.cpp ; valeur par défaut de la classe `LlamaCpp` d'Agno ; issue smolagents #1860 (« doesn't generate proper code responses ») |

Hors de la contrainte « ≤ 32B » (cités pour éviter les confusions de noms, tailles lues sur l'API HF) : Qwen3.8-Flash-Next (180 B), GLM-5.3-Flash (321,3 B malgré « Flash »), Qwen3-Coder-Next (79,7 B).

Lignes BFCL de la même classe de taille (snapshot 2026-04-12, voir § 2b) : xLAM-2-32b-fc-r 54,66 % (rang 18, multi-tour 69,50 %, licence cc-by-nc-4.0) ; Arch-Agent-32B 45,37 % (rang 37) ; Qwen3-32B FC 48,71 % ; Gemma-3-27b-it (Prompt) 29,47 % ; Phi-4 (Prompt) 28,79 % ; Granite-20b-FunctionCalling 23,23 %. Aucun des modèles du tableau ci-dessus n'y figure, sauf la famille Qwen3 déjà citée.

## 2d. Problèmes connus signalés sur les dépôts d'agents avec un endpoint llama.cpp / petit modèle

(recherches « llama.cpp » ou « llama-server » dans les issues ; l'état « fermée » ne veut pas dire résolu pour tous ; contenus non lus sauf mention)

| Dépôt | Issue | Fait |
|---|---|---|
| llama.cpp | #12279 | voir § 2b (Qwen2.5-Coder-7B, `<tool_response>` renvoyé en contenu, id vide, 500 « Expected 'content' ») |
| llama.cpp | #13825 / #14697 / #19009 | voir § 2a |
| pydantic-ai | #11244 (fermée 2026-10-25) | `ModelAPIError: Connection error` avec llama.cpp « 0.7.0 » ; réponse du bot : l'erreur vient du **port** (« llama.cpp 0.7.0 appears to default to port 9931 ») ; fermée par l'auteur « the port change » https://github.com/pydantic/pydantic-ai/issues/11244 |
| pydantic-ai | #4878 (ouverte) | « Need for llama.cpp providers » https://github.com/pydantic/pydantic-ai/issues?q=is%3Aissue%20llama.cpp |
| pydantic-ai | #224 (fermée 2025-08-25) | « Tool calling issues with vllm » (30 commentaires, non lue) |
| smolagents | #1860, #1872, #449 | gpt-oss-20B code ; streaming + CodeAgent ; demande d'un `LlamaCppModel` https://github.com/huggingface/smolagents/issues?q=is%3Aissue%20llama.cpp |
| strands | #5490, #5428, #3902, #3422, #2051 | streaming bufferisé jusqu'à l'EOF HTTP ; `tool_use` rapporté au lieu de `max_tokens` ; chunk d'usage final perdu ; paramètres de sampling perdus ; arguments d'outil malformés remplacés par `{}` https://github.com/strands-agents/harness-sdk/issues?q=is%3Aissue%20llama.cpp |
| agno | #5106, #3594, #4246, #8181 | appels d'outils mal analysés (v2) ; `content: None` ; instructions ignorées avec OpenAI-like ; télémétrie bloquante https://github.com/agno-agi/agno/issues?q=is%3Aissue%20llama.cpp |
| google/adk-python | #6482, #6334 | rôle `tool_responses`/« tool » erroné avec Gemma 4 via LiteLLM sur LM Studio https://github.com/google/adk-python/issues?q=is%3Aissue%20llama.cpp |
| mastra | #15234 | `Skills` avec Qwen 3.5 : « Assistant response prefill is incompatible with enable_thinking » https://github.com/mastra-ai/mastra/issues?q=is%3Aissue%20llama.cpp |
| pi (earendil-works/pi) | #11573, #10885, #11472, #11200, #10889, #10077 | petits modèles locaux qui recopient le préfixe `tools.` dans le nom d'appel ; dépassement de contexte llama.cpp non détecté donc compactage jamais déclenché (ouverte) ; mode RPC avorté avec providers `openai-completions` locaux ; plantage sur `function_call_arguments.done` sans arguments ; llama.cpp absent de la liste des providers (fermée) ; `contextWindow` réinitialisé à 128000 https://github.com/badlogic/pi-mono/issues?q=is%3Aissue%20llama.cpp |
| OpenHarness | #199, #212 (fermées 2026-04-28) | erreurs `n_ctx` de llama.cpp avec la compaction ; débordement de contexte par de gros `tool_result` MCP https://github.com/HKUDS/OpenHarness/issues?q=is%3Aissue%20llama |
| langchain | #39320, #29323, #32884 | `base_url` ignoré par le routage Responses pour certains noms de modèle ; « VLLMOpenAI api issues » ; données d'outil MCP non repassées pour un Llama 3.3 70B https://github.com/langchain-ai/langchain/issues?q=is%3Aissue%20llama-server%20tool |
| openai-agents-python | #1574 | une seule issue pertinente (truncation et gpt-oss) https://github.com/openai/openai-agents-python/issues?q=is%3Aissue%20llama.cpp |

Contenus partagés par plusieurs sources de la section 1 : les cadres qui injectent `tool_choice: required` (smolagents) ou ignorent `tool_choice` (Strands `LlamaCppModel`) se comportent différemment face à la grammaire paresseuse de `llama-server` décrite en § 2a ; aucun test n'a été fait.

---

## 3. Ce que je n'ai pas pu vérifier

- Pour **aucun** cadre : le comportement réel avec `llama-server` b10216 + Qwen2.5-Coder-14B (rien n'a été exécuté).
- **OpenHarness** : sémantique de `--allowed-tools`/`--disallowed-tools` ; ce que fait `provider.py`/`registry.py` pour llama.cpp ; commit automatique ; clangd/LSP effectif ; Subversion ; mécanisme d'annulation d'un tour ; intégration de Serena.
- **pydantic-ai** : comportement sur nom d'outil inconnu ; transports MCP (stdio ?) ; streaming des appels d'outils avec llama-server ; plafond de sortie adapté à 32 k ; contenu de l'issue #224 ; licence du paquet harness si distinct du dépôt principal (PyPI dit MIT).
- **smolagents** : télémétrie dans les fichiers non lus ; réinjection des erreurs d'étape dans le prompt ; niveau de sécurité de l'exécuteur local ; compactage ; documentation OpenTelemetry (mentionnée de mémoire, non lue).
- **LangGraph** : défaut d'activation de LangSmith ; code de `langchain-openai` ; annulation d'un tour ; modes de streaming ; MCP (adaptateur hors dépôt) ; comportement de `langchain.agents.create_agent` et de ses middlewares.
- **OpenAI Agents SDK** : destination exacte de l'export de traces dans le code ; accès d'un guardrail d'outil à l'historique du tour ; contenu de `docs/sandbox_agents.md`.
- **Google ADK** : effet de la télémétrie hors CLI ; comportement par défaut sur nom d'outil inconnu ; sémantique des retours de `before_tool_callback` ; streaming ; API d'annulation ; documentation `adk-docs` sur LiteLLM/Ollama/vLLM (non lue).
- **Strands** : politique de relance sur arguments malformés (au-delà de l'issue #2051) ; transports MCP ; harness (`create_harness`, `strands` CLI) ; dépôts `shell` et `box`.
- **Mastra** : formulation exacte de la coupure des événements serveur par `MASTRA_TELEMETRY_DISABLED` ; texte intégral de l'`ee/LICENSE` ; comportement sur nom d'outil inconnu et sur JSON malformé ; Windows.
- **Agno** : ce qui est renvoyé au modèle quand un nom d'outil est inconnu ; validation de schéma des paramètres ; streaming ; sémantique des `tool_hooks`/`pre_hooks` ; contenu des issues #5106, #3594, #4246, #7493.
- **Pi** : contenu exact de la télémétrie d'install ; annulation ; compaction ; sandbox ; relance sur JSON malformé.
- **Autres cadres** (LangChain, Microsoft Agent Framework, OpenAI Agents JS, Vercel AI SDK, CrewAI, Haystack, LlamaIndex) : presque tout hors licence/release ; Semantic Kernel, AutoGen, DSPy, Letta non examinés.
- **llama.cpp** : sens des tags `v0.x` (ex. v0.9.0) par rapport aux `bNNNN` ; comportement exact d'un gabarit Qwen2.5-Coder-14B avec l'auto-parser au tag b10216 (la doc ne liste pas le 14B Coder dans son tableau) ; contenu des issues #13825 et #14697 au-delà de leur en-tête.
- **Fiabilité du 14B Coder** : aucun score de tool-calling publié par Qwen ni par BFCL (aucune ligne) ; rapport technique arXiv 2409.12186 non lu.
- **Modèles ≤ 32B** : aucun benchmark indépendant d'agent de code avec `llama-server` ; GGUF de Qwen3-Coder-30B-A3B, GLM-4.7-Flash, gpt-oss-20b non recherchés précisément ; scores des cartes non reproduits.
