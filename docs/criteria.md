# Choosing a coding-agent harness plugged into a local LLM

**Question:** can an existing agent harness, maintained elsewhere, plugged into the
local llama.cpp, replace Pumba's specialization (in-house agent,
C++ index, named tools, sandbox)? Which one, and at what cost?

**Fixed context (not up for discussion in this study)**

- Chat model: Qwen2.5-Coder-14B-Instruct Q5_K_M served by `llama-server` (llama.cpp, tag b10216), OpenAI-compatible API. 32,768-token window on the 14B profiles, 262,144 on the EVO-X5. Swappable for other GGUFs.
- Target: C++/CMake tree (Qt possible), Git **and** Subversion copies, Windows host + Podman/WSL containers.
- Everything stays local. The code does not leave the machine.
- Decided: "no shell" is a **preference**, not a requirement. A shell with approval is acceptable. A "pass everything by default" authorization is noted as a risk.
- License: any license that allows internal company use is acceptable (never distributed), GPL included. FSL-1.1-MIT (Crush) is therefore accepted.
- Decided 2026-11-12: Subversion support **is** a requirement. No harness covers it, so every candidate is evaluated as "harness + read-only `svn_*` wrappers".
- Decided 2026-11-12: a terminal interface is enough. A shared web page is not required, so Refact's and OpenHands' browser UI is no longer a differentiator.
- Decided 2026-11-12: each harness is tested with two models, the 14B above and a more recent one that claims tool use. The test machine has an RTX 4080 with 16 GiB.

## Gates (a no eliminates, with proof)

| Id | Gate | Test |
|---|---|---|
| G1 | Talks to a local OpenAI-compatible endpoint, with no mandatory cloud service | Documented config with arbitrary `base_url` |
| G2 | Works without an account, without mandatory outbound network. Telemetry can be turned off | Telemetry documentation, or reading the code |
| G3 | Open-source license | The repository's LICENSE file |
| G4 | Maintained: a release or a commit in the last 6 months (today's date: 2026-11-12) | Releases or commits page |

## Grid (filled 2026-11-14)

The composite criteria below are split into ~61 atomic columns.

- Preferred view: interactive canvas `grille-capacites-agents` (open beside chat) — chooser by need, glossary of every column, side-by-side of 2–4 tools. Pumba is one product in the corpus, not the baseline.
- Executable bench (T1–T16, model vs harness, EVO-5): [`banc.md`](banc.md)
- Static export: [`grille-capacites.md`](grille-capacites.md)
- Machine source: [`grille-capacites.json`](grille-capacites.json)

Cells are sourced facts or `nv`. Do not invent values.

Write **unverified** rather than guess. Each cell cites its source (URL).

| Criterion | What we look for |
|---|---|
| Nature | Terminal agent, editor extension, web application, or **framework for building** your own agent |
| License (SPDX) | |
| Last release / last commit | Date |
| Tool-calling with a local model | Native OpenAI calls, or a fallback format in the text (XML, tagged JSON)? Does it require `--jinja` or a chat template? How does it handle a malformed call? |
| Small models | Published evidence with a local model ≤ 30B (benchmark, issue, usage report) or dedicated tuning? |
| Context management | Compaction, tool output cap, adaptation to 32k |
| C++ / CMake | Built-in LSP (clangd)? Build and test launching? None? |
| Repository search | grep only, repo map, semantic index? If an index: which embedding model, can it be local? |
| MCP | MCP client? Supported transports (stdio, HTTP)? Can Serena be plugged in? |
| Command execution | Shell present? Approval model? Allowlist possible? Sandbox? Default mode |
| Editing | Mechanism (diff, search-replace, patch). Automatic commit? Can it be forbidden? |
| Version control | Native Git? Subversion? |
| Interface | Terminal, IDE, web page? Server or headless mode? Deployable in a container? |
| Scriptable | Can you run a question and get back the answer and the tool calls without a human (to replay `eval_tools_scenarios.json`)? |
| Extension | Custom tools, hooks, project rules (equivalent of `rules/*.md`) |
| Observability | Turn logs or traces |
| Risks noted | Telemetry, auto-approval, commits, hidden cloud dependency |

## What we do not do

- No recommendation in the research notes: facts only.
- No in-house benchmark at this stage.
- No secondary source when a primary source exists (README, official docs, LICENSE, code, releases page). A blog is only accepted for a usage report, flagged as such.
