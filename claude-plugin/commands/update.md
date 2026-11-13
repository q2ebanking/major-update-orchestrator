---
description: Orchestrate a major, codebase-spanning update through its full lifecycle (Assess → Plan → Execute → Verify → Roll out). Use `/update burndown` for an on-demand burn-down chart, or `/update usage` for a model & token usage report.
argument-hint: "[burndown | usage] | <description of the update>"
---

Use the **orchestrate-update** skill to drive this work.

Arguments: `$ARGUMENTS`

- If the arguments contain **`burndown`**: produce an on-demand burn-down chart per the skill's `references/burndown.md` — a read-only reporting action that does not change phase or state. Derive it from the living plan doc's timestamped transition log and each work unit's story-point size.
- If the arguments contain **`usage`**: produce an on-demand model & token usage report per the skill's `references/usage-report.md` — a read-only reporting action that does not change phase or state. Render it from the living plan doc's usage rollup (per-model subagent token/tool-use totals).
- Otherwise: begin (or resume) the orchestration. First look for an existing **living plan doc**; if found, read it, rebuild the todo list from its work units and states, and continue from the current phase. If none exists, start at **Assess**. Any remaining arguments are the user's description of the update to orchestrate.

Follow the skill's guiding principles throughout — discover-then-fallback for every external capability, evidence-driven (no fabrication), confirm before external writes, and keep the Design artifact and living plan doc as the two authoritative, non-overlapping sources of truth.
