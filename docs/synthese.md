# Synthèse de l'étude harness (2026-11-12)

Croisement des trois notes : `notes/A-terminal.md`, `notes/B-editeur-web.md`, `notes/C-cadres-et-toolcalling.md`. Grille et portes : `criteria.md`. Les URL sources sont dans les notes.

**Limites** : rien n'a été exécuté. Tout est documentaire (README, docs, code lu à un commit précis). Les chiffres de modèles sont des auto-déclarations des éditeurs. Le comportement réel avec `llama-server` b10216 et Qwen2.5-Coder-14B n'est vérifié pour aucun candidat.

## 1. Portes : qui sort

| Candidat | Motif |
|---|---|
| Gemini CLI | G1 : pas de fournisseur compatible OpenAI |
| Plandex | G4 : dernier commit 2025-10-03 |
| Roo Code | Arrêté le 2026-05-15 (le fork Zoo Code est actif) |
| Void | Déprécié (dernier commit 2026-06-02) |
| Continue | « no longer actively maintained » |
| Tabby | Interface web sous licence Enterprise (`ee/`), pas un agent de code |
| SWE-agent v1 | Remplacé par mini-swe-agent |
| Open WebUI | Licence à clause de marque (G3 limite), client MCP sans stdio |

**À ta décision** : Crush est sous FSL-1.1-MIT (usage interne permis, conversion en MIT après 2 ans). Pas libre au sens strict.

**Passent avec réglages** (télémétrie à couper, voir notes) : OpenCode, Aider, Goose, Qwen Code, Pi, Cline, Kilo Code, Zoo Code, OpenHands, Refact, Zed, Pochi, llama.vscode, Codex CLI (API Responses seulement), cadres Python (pydantic-ai, smolagents, LangGraph, Strands, Agno, Mastra, ADK, OpenAI Agents SDK, OpenHarness HKUDS).

## 2. Le fait qui change la question : le modèle

- Qwen2.5-Coder-14B-Instruct : **aucun score de tool-calling publié** (model card, BFCL du 2026-04-12). Son gabarit de chat contient un bloc d'outils de style Hermes, et llama.cpp gère le format Qwen 2.5 Coder. Il n'y a pas de preuve de fiabilité pour le 14B.
- Pour toute la classe ≤ 32B, le BFCL montre une chute en multi-tour (Qwen3-30B-A3B-Instruct FC : 30 % en multi-tour contre 85,8 % en non-live).
- La boucle de Pumba compense déjà cela (relances, appels déguisés, lots malformés).
- Modèles plus récents qui revendiquent un usage d'outils en agent (auto-déclaré) : Qwen3.8-27B, Devstral-Small-2-24B, GLM-4.7-Flash, gpt-oss-20b, Qwen3-Coder-30B-A3B (son parseur d'outils XML n'est pas dans llama.cpp b10216).
- Seul Aider publie des mesures pour Qwen2.5-Coder-14B (benchmark d'édition, 2024) : 69,2 % de réussite, 100 % de réponses bien formées en format `whole`. Il n'utilise pas le tool-calling : il passe par des formats d'édition en texte.

**Conséquence** : comparer des harness uniquement sur le 14B mesure autant le modèle que le harness.

## 3. Ce qu'aucun candidat ne couvre

| Besoin Pumba | État |
|---|---|
| Subversion | **Aucun des candidats** ne le mentionne dans les sources lues |
| Interdiction de committer | Aider committe par défaut (désactivable). Les autres n'ont pas d'auto-commit trouvé, mais le shell permet `git commit` |
| Isolation réseau et sandbox de commandes | OpenHands (Docker). Les autres : aucune sandbox, approbations seulement |
| Phase **editing** → `build_step` | Aucun. Possible par hooks (OpenHarness HKUDS, Claude-like) ou à construire |
| Index C++ sémantique local | Refact (AST tree-sitter C++ + recherche sémantique) ; Kilo Code (indexation de code documentée). Non testés |

## 4. Intelligence C++ intégrée (clangd / LSP)

| Candidat | Constat |
|---|---|
| Crush | LSP clangd par défaut (`auto_lsp`) : `lsp_definition`, `references`, `symbols`, `call_hierarchy`, `rename`, `replace_symbol`, `diagnostics`. Lancement sous Windows non vérifié |
| Kilo Code | LSP clangd intégré (`--background-index --clang-tidy`), outils `lsp` et `diagnostics` |
| Zed | clangd, outil `diagnostics` ; GPL ; pas de mode serveur |
| OpenCode | V1 : clangd. **V2 : plus de LSP** (migration documentée) |
| Aider | Pas de LSP ; repo map tree-sitter avec requêtes C++, `--lint-cmd` / `--test-cmd` |
| Goose, Cline, Pi, OpenHands, Qwen Code | Pas de LSP par défaut ; tout via shell |
| Refact | AST tree-sitter C++, pas de clangd |

## 5. Forme (page web, serveur, scriptable)

| Candidat | Constat |
|---|---|
| Refact | Binaire unique : démon résident, **GUI navigateur**, LSP, agent CLI headless. « Early preview » pour le démon |
| OpenHands | Application web + Agent Server en Docker. Pas de LSP. Recommande Qwen3.6-35B-A3B en local |
| Cline | CLI scriptable (`--json`), tableau de bord web local. **CLI one-shot = mode yolo par défaut** |
| OpenCode, Goose, Crush, Pi, Aider | Scriptables sans humain (`run`, `--output-format`, `--message`). Présence des appels d'outils dans la sortie : à vérifier |
| Cadres | `pydantic-ai`, `smolagents`, etc. : à intégrer. Ils remplaceraient `tool_loop`, pas le produit |

## 6. Risques par défaut relevés

OpenCode (tout autorisé, shell hors projet compris), Goose (mode autonome par défaut), Pochi (tout autorisé), Pi (ni approbation ni sandbox), Qwen Code (statistiques vers Alibaba), Cline (télémétrie et feature flags), Kilo Code (PostHog), cadres : OpenHarness HKUDS et Strands remplacent un JSON d'arguments illisible par `{}`.

## 7. Cadres : pour remplacer seulement `tool_loop`

`pydantic-ai` (MIT, v2.68.0 du 2026-11-12) : actif, validation Pydantic, fournisseur OpenAI-compatible. Pas de preuve sur llama-server avec petit modèle (issue de port #11244). `smolagents` (Apache-2.0, v1.26.0 du 2026-05-29). OpenHarness HKUDS : dernier commit 2026-06-04, remplacement silencieux des arguments illisibles. Aucun ne fournit la phase **editing**, l'annulation de tour ni les relances de Pumba : à construire par-dessus.
