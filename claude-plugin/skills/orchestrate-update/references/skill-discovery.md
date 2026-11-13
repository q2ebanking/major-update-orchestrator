# Skill & Capability Discovery — discover-then-fallback

For **every external capability** the orchestrator uses, follow the same pattern: check what the
session offers, use it if present, fall back gracefully if not. Never hard-require a specific tool.

## The pattern

1. **Discover.** Check the session's available skills, MCP servers, subagents, and CLIs for a
   capability match. Match by **capability**, not by an assumed exact name (tracker status names,
   skill names, and MCP tool names vary across environments).
2. **Reuse.** If a match is present, chain to it and adapt its output.
3. **Fall back.** If absent, use the bundled behavior named below, or hand off to the user with a
   clear ask.
4. **Present-but-unresponsive ≠ absent.** A discovered tool can be present yet fail mid-operation — a
   timeout, expired auth, or a rate limit. Don't treat that as "absent" and silently drop to the
   fallback (especially for external writes, where a silent fallback can lose or duplicate the write).
   Surface the specific blocker to the user with a concrete ask (re-authenticate, wait and retry),
   retry, and **re-verify the operation completed** — a call that timed out may have partially
   applied before the client gave up.

## Capability ↔ fallback map

| Capability | Reuse when present | Fallback when absent |
|---|---|---|
| Recon (large repos) | `Explore` / recon subagent | Inline probes + interview |
| Baseline metric capture (expensive) | Profiling/measurement subagent | Inline measurement commands |
| Guided design | `grill-with-docs`; if absent, **superpowers:brainstorming** | Bundled `guided-design.md` |
| Decomposition / plan | **superpowers:writing-plans** | Bundled planning-subagent prompt (`plan.md`) |
| Parallel dispatch | **superpowers:dispatching-parallel-agents** | Bundled fan-out (`parallel-orchestration.md`) |
| Worktree isolation | **superpowers:using-git-worktrees** | Bundled worktree commands (`parallel-orchestration.md`) |
| TDD | **superpowers:test-driven-development** | Bundled RED→GREEN→refactor |
| Skill authoring | **superpowers:writing-skills** | Bundled minimal SKILL.md template (below) |
| Whole-change verify | **superpowers:verification-before-completion** | Bundled verify checklist (`verify.md`) |
| Code review | `code-review` / **superpowers:requesting-code-review** | Bundled review checklist (`verify.md`) |
| E2E regression | Playwright / E2E runner or regression MCP, or an in-repo invocation script | Prompt user to run their suite and report |
| E2E pipeline kickoff (post-MR) | In-repo trigger script, or a session skill that initiates the pipeline against an MR (e.g. a Playwright-pipeline-kickoff skill) | Prompt user to kick off the pipeline manually and report |
| E2E pipeline results review (post-MR) | In-repo results script, or a session skill that reviews pipeline results | Prompt user to review the pipeline results manually and report |
| Diagnosis | **superpowers:systematic-debugging** | Bundled diagnosis steps (`verify.md`) |
| Lint / format | Project's own lint & formatter commands | Ask user, or note none exist |
| Tracking system | Jira / GitLab MCP or tracking skill | Manual ticket ref, or ticket-less |
| MR/PR delivery | MR/PR MCP or skill / `gh` | Branch + ready-to-paste description |

## Assistive skill scan (per phase, beyond the capability map)

The capability map above covers task-specific capabilities with a reuse-or-fallback contract. Separately, **at each phase entry**, scan the full list of skills available in the session for ones that generically strengthen that phase's work even though they aren't tied to a named capability. These are optional quality boosters — their absence never blocks a phase, unlike a capability-map miss.

Match by what the phase is trying to accomplish, not a fixed list. Examples:

| Phase | What would help | Example assistive skill |
|---|---|---|
| Assess | Pressure-test scope and acceptance criteria before they're locked | A requirements/assumption-challenging skill (e.g. `grill-me`) |
| Plan | Stress-test the design and wave decomposition before committing | `superpowers:brainstorming`, a design-review skill |
| Execute | Root-cause a stubborn failure before rolling it into the next wave | `superpowers:systematic-debugging` |
| Verify | Diagnose a failing gate; review code quality | `superpowers:systematic-debugging`, a code-review skill |
| Roll out | Tighten PR/ticket prose; render the closeout burndown clearly | A writing-clarity skill, `dataviz` |

## Phase-entry skill table

Before starting a phase's work, resolve and render a table of the skills driving it — this is what SKILL.md's "First Move Every Session" step 3 and the Lifecycle section point to:

| Role / function | Candidate skill(s) | Type | Selected |
|---|---|---|---|
| *what the phase needs* | *matching skill name(s)* | capability / assistive | *chosen one, or "—"* |

Build one row per role the phase actually needs this time — only the capability-map and assistive matches relevant to the work at hand, not every row in the map. For each row:

- **One candidate** → select it; no prompt needed.
- **Multiple plausible candidates** — two independent session skills that could both serve the same role, or a capability-map entry listing alternatives without an order — stop and ask the user which to use via `AskUserQuestion` before proceeding. An explicitly ordered fallback chain is not ambiguous: use the first available candidate in order. Never silently choose among unordered alternatives.
- **No candidate** → mark "—" and proceed on the bundled fallback (capability rows) or simply skip it (assistive rows); a missing assistive skill never blocks the phase.

Show the resolved table to the user, then proceed with the phase's work.

## Reuse-vs-author decision (skill gaps)

When a work unit needs a capability with **no matching skill** in the session, this is a **skill
gap**. Decide it in **Plan**, act on it in **Execute**. Offer the user two options per gap:

- **Handle it inline** — do the work directly this once, no reusable artifact. Best when the need is
  one-off and unlikely to recur.
- **Author a reusable skill** — via **superpowers:writing-skills** if present, else the bundled
  minimal template below. Best when the capability will recur across units or projects.

Record the decision **per unit** in the living plan doc's skill-gap log, then act on it when the unit
is dispatched.

## Bundled minimal SKILL.md template

When authoring a skill without `superpowers:writing-skills`, start from this and keep it tight — the
description states **when to use** (triggers only, no workflow summary):

```markdown
---
name: skill-name-with-hyphens
description: Use when [specific triggering conditions and symptoms].
---

# Skill Name

## Overview
What this is; the core principle in 1–2 sentences.

## When to Use
Symptoms/situations that trigger it. When NOT to use.

## Steps
1. …
2. …

## Common Mistakes
What goes wrong + the fix.
```
