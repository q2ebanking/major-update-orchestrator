---
name: orchestrate-update
description: Use when a technical change spans many packages/modules at once — framework or platform upgrades, dependency/version bumps, cross-cutting or monorepo-wide migrations, project-wide refactors, tech-debt sweeps, or performance initiatives — any codebase-spanning change too large to land safely in a single pass.
---

# Orchestrate a Major Update

## Overview

A **major update** is a change that touches many packages/modules at once and is too large to land safely in one pass. The hardest, most valuable job here is **decomposing that change into independent work units and driving them in parallel with subagents, safely** — planning the fan-out, isolating the work, and reconciling/verifying the results.

The five-phase checklist below is scaffolding. **Parallel orchestration is the payload** — see `references/parallel-orchestration.md`.

You are the **integrator**. The work happens in subagents; you plan the waves, isolate each unit, and converge the results.

**Run the orchestrator on a judgment-capable model — sonnet is the right default; escalate specific
steps to opus rather than running the whole orchestration on it.** The integrator role is
judgment-heavy: deciding wave boundaries, triaging whether a failure blocks or rolls forward,
re-scoping when a criterion is blocked, and grading ambiguous verification results — all of which
sonnet handles. Don't drive it from haiku. Where judgment genuinely spikes, the skill already
escalates *per task* — root-cause diagnosis of a hard cross-unit failure and judgment-heavy work
units run on opus (see `references/verify.md`, `references/parallel-orchestration.md`) — so a standing
opus integrator is rarely worth its cost; reserve driving the whole run on opus for updates that are
architecturally ambiguous end to end. Mechanical work is pushed *down* to cheaper subagents
(measure-only → haiku, implementation → sonnet); the orchestrator stays on the model that can make the
calls, and borrows a stronger one only for the calls that need it.

## When to Use

- A framework/runtime upgrade across many packages (e.g. "move every package to Ember 6").
- A platform migration or cross-cutting refactor touching many modules.
- A performance or quality initiative with a measurable target across the codebase.
- Any change large enough that you'd naturally split it into batches.

**When NOT to use:** a single-file fix, a change confined to one module, or work with no parallelism to exploit. Use normal development flow instead.

## First Move Every Session

1. **Look for the living plan doc** (glob `docs/*-plan.md`; the default name is `docs/<slug>-plan.md` where `<slug>` is the kebab-cased update name). If one exists, this is a **resume**; if not, this is a **kickoff**: start at Assess.
2. **Rehydration protocol (resume — do this in order, don't re-read finished work).** The plan doc
   grows unbounded (the transition log is append-only), so **read it in bounded passes rather than
   pulling the whole file into context** — the resume-critical sections are cheap; the log is not:
   1. Read the **Lifecycle header** to get the current phase (a small `limit` read of the top of the
      file is enough — don't slurp the whole doc).
   2. Read **Next steps** for the immediate action and any carried failures / remediation units.
   3. Rebuild the todo list from the **Waves & work units** tables — take units in states
      **In Progress · Failed · Blocked · Todo**; skip units already **Done**.
   4. Pick up the noted carry-forwards (known environmental failures, tracker transition map, retarget/roll-out follow-ups) from their sections rather than rediscovering them.
   - **Read:** lifecycle header · next steps · waves tables (Todo/In Progress/Failed/Blocked rows only) · tracker transition map · determinism/normalization rules · known environmental failures · any decision the next step explicitly references.
   - **Skip:** transition log (active **and** archived) · archived decisions · skill-gap log · model & token usage rollup — all append-only, historical, or read-only accounting, not actionable state. Rebuild the todo list from the Waves tables, not from history.
3. Announce which phase you're entering, then render the **phase-entry skill table** (capability-matched + assistive candidates, ambiguous rows resolved via `AskUserQuestion`) before starting the phase's work — see `references/skill-discovery.md`.

## Guiding Principles (always in force)

1. **Discover-then-fallback, everywhere — and scan broadly, not just by capability.** For every external capability — skills, tracking systems, MR/PR tooling, test runners — first check the session's available skills/tools and use what's there; otherwise fall back to bundled behavior or a user hand-off. Never hard-require a specific tool. Beyond the fixed capability map, also scan the full list of session-available skills each phase entry for ones whose purpose generically strengthens the phase at hand (e.g. a requirements-pressure-testing skill for Assess, a debugging skill for Verify) even when they aren't tied to one of the orchestrator's named capabilities. Render both kinds as the phase-entry skill table and resolve any role with more than one plausible candidate by asking the user — never guess which of several matching skills to use. See `references/skill-discovery.md`.
2. **Two authoritative documents, no drift.** The **Design artifact** owns *why/architecture*; the **living plan doc** owns *how/sequencing/progress*. Cross-linked; neither redefines the other's facts.
3. **Evidence-driven, no fabrication.** Mark unknowns `TBD` / `Not provided`. Never invent paths, criteria, commands, ticket contents, or APIs.
4. **Confirm before external or hard-to-reverse writes.** Ticket and MR/PR creation are previewed and user-confirmed before any write to an external system.
5. **Measurable acceptance criteria drive everything.** Criteria set in Assess become the failing tests in Execute and the pass/fail gates in Verify. Each criterion is **mapped to the work units that satisfy it**; an absolute "all-of-set" criterion (e.g. *all packages on version X*) cannot be graded pass while any contributing unit is unexecuted or deferred. A criterion is only as trustworthy as its **baseline** — validate the baseline is real and representative when you capture it (see `references/assess.md`), because a mis-measured baseline silently corrupts every comparison built on it. **Criteria and baselines may be revised when execution proves one wrong or mis-measured — but never silently:** log the revision in the living plan doc's decisions log (timestamp + rationale), annotate the criteria row (`revised from <X>`), and re-grade any units already graded against the old value.
6. **Persist across sessions.** The living plan doc is the cross-session source of truth: hydrate a todo list from it, write progress back. **Every time you edit the doc** (state transitions, log appends, next-steps updates), set the **`Last updated`** field in the lifecycle header to the current timestamp (`YYYY-MM-DDThh:mm`) in the same edit — a stale header misleads the next session's rehydration about how current the recorded state is.
7. **Every unit is sized and time-stamped.** Each work unit carries a **story-point** size, state transitions are logged with timestamps, and a rough **velocity** (points per two weeks) is recorded — this makes the burn-down chart and completion forecast meaningful. An `Unsized` unit **may not enter a wave**: size it before Execute, or log it as explicitly **deferred** and mark any acceptance criterion that depends on it **Blocked**.
8. **Independent verification, always.** Never converge a unit — or grade the whole change — on its **own** self-reported green; a subagent's "tests pass" is a *claim*, not a *result*, and self-reports are wrong often enough to catch regressions late. Delegate verification to an **independent** agent that re-runs the gate **multiple times (default 3×)** to catch flakes and false positives, and returns a structured verdict. See `references/independent-verifier.md`. The same discipline covers the plan itself, one phase earlier: before the Plan checkpoint, an independent reviewer adversarially probes the draft living plan doc's wave/unit decomposition for hidden shared-file conflicts, missed dependencies, unsized units, and criteria-coverage gaps — a flawed plan is far cheaper to catch here than after Execute is underway. See `references/plan-reviewer.md`.

## The Lifecycle

Five phases: **Assess → Plan → Execute → Verify → Roll out**. Load the phase's reference file when you enter it — do not preload them all. Before starting a phase's work, render its **phase-entry skill table** (see `references/skill-discovery.md`) so it's clear which reused and assistive skills are driving that phase.

| Phase | Load | Produces | Gate to advance |
|---|---|---|---|
| **1. Assess** | `references/assess.md` | Findings: scope, measurable acceptance criteria, comparative + test/build baselines, tracking ref, lint/format commands | Criteria defined; comparative baselines captured (or `Not captured`); test/build baseline captured (green or knowingly-red); ticket recorded or waived; clean/known git state; lint/format identified |
| **2. Plan** | `references/plan.md` (+ `guided-design.md`) | Design artifact + living plan doc: ordered waves of sized, scoped work units | Design reviewed; plan reviewer clean/resolved; waves + per-unit story points approved; tickets synced (confirmed); skill gaps decided |
| **3. Execute** | `references/execute.md` (+ `parallel-orchestration.md`) | Converged code, wave by wave | Every unit tests-green, formatted, lint-clean; waves converged; failures rolled forward |
| **4. Verify** | `references/verify.md` | Graded criteria, code review, whole-change lint, E2E regression on the integration branch (or a `post-mr` deferral when the suite can only run once an MR exists) | Every criterion graded pass; regression green or deferral recorded; review findings triaged; never advance on red |
| **5. Roll out** | `references/roll-out.md` | MR/PR(s) linked to tickets, post-MR E2E pipeline when deferred from Verify, opt-in review-feedback handling, closeout | Change delivered; tickets transitioned; post-MR E2E pipeline green (if applicable); review feedback offered/worked; living plan doc finalized |

**Failures never abort siblings.** A failed unit is isolated, recorded, and **rolled into the next wave** as remediation. A failed Verify generates a remediation wave looped back through Execute, then re-verifies. Never advance to Roll out on red.

## Burn-Down On Demand

At any point — any phase — the user may request a burn-down chart (via `/update burndown` or natural language). It is **read-only**: it does not change phase or state. Derive it from the living plan doc's timestamped transition log plus each unit's story-point size. See `references/burndown.md`.

## Usage Report On Demand

At any point — any phase — the user may request a model & token usage report (via `/update usage` or natural language): a per-model breakdown of subagent token and tool-use spend for the run. Like the burn-down it is **read-only** (no phase/state change), rendered from the living plan doc's usage rollup. The rollup is maintained **as subagents complete** (at each convergence and for other dispatches), so record usage along the way — a later session can't see an earlier one's completion figures. The integrator's own tokens are excluded (not self-observable). It is also rendered automatically at Roll out Closeout. See `references/usage-report.md`.

## Reused Skills (discover-then-fallback)

**All of the skills below are optional** — the orchestrator runs fully with none of them present. When one *is* present in the session, chain to it; otherwise use the bundled fallback in the referenced file. Match by capability, not by an assumed exact name:

- Decomposition/planning → **superpowers:writing-plans**
- Parallel dispatch → **superpowers:dispatching-parallel-agents**
- Worktree isolation → **superpowers:using-git-worktrees**
- TDD → **superpowers:test-driven-development**
- Skill authoring (for skill gaps) → **superpowers:writing-skills**
- Whole-change verification → **superpowers:verification-before-completion**
- Code review → **superpowers:requesting-code-review** or a session code-review skill/agent
- Diagnosis → **superpowers:systematic-debugging**
- Guided design (concepts) → **grill-with-docs** if present; otherwise
  **superpowers:brainstorming** if present, then the bundled Guided design
  reference

See `references/skill-discovery.md` for the reuse-vs-author decision and the full capability↔fallback map.

## Templates

- Design artifact → `references/design-artifact-template.md`
- Living plan doc → `references/living-plan-doc-template.md`

Both are bundled so behavior is identical in any repo.
