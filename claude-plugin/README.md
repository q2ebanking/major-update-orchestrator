# major-update-orchestrator

## Overview

Guides a developer through the full lifecycle of a **major, codebase-spanning technical
update** — framework upgrades, platform migrations, cross-cutting refactors, and performance
initiatives. The hardest, most valuable job it does is **decomposing the change into independent
work units and driving them in parallel with subagents, safely** — planning the fan-out, isolating
the work in git worktrees, and reconciling/verifying the results.

Generic and platform-agnostic: it discovers whatever capabilities are present in the session
(skills, MCP servers, trackers, MR/PR tooling, test runners) and falls back gracefully when
they're absent.

## Lifecycle

**Assess → Plan → Execute → Verify → Roll out.** The full design spec lives alongside this
plugin's source repository.

## Skills

| Skill               | Description                                                     |
| -------------------- | ------------------------------------------------------------------ |
| `orchestrate-update` | Drives the full Assess → Plan → Execute → Verify → Roll out lifecycle |

## Commands

| Command   | Description                                                                 |
| ---------- | ---------------------------------------------------------------------------- |
| `/update`  | Entry point — parses arguments (`burndown`, `usage`) before handing off to the skill |

### `/update` vs. `orchestrate-update`

Both show up in Claude Code's completion list — that's expected, not a duplicate. `/update` is
the intended entry point: it routes `burndown`/`usage` to read-only reports before handing off
to the skill. Invoking the skill directly skips that routing and goes straight into its own
resume-or-kickoff logic. Prefer `/update` for normal use.

## Agents

| Agent                      | Description                                                                   |
| --------------------------- | --------------------------------------------------------------------------------- |
| `implementation-executor`  | Executes a single implementation work unit test-first, with gate discipline baked in |

## Installation

Add this plugin to Claude Code — via your marketplace, or a local path pointed at this
directory — then restart the session so `/update` and `orchestrate-update` are picked up.
