# Independent Plan Reviewer — canonical dispatch

The plan is never graded sound on its own drafting subagent's self-report either — the same
discipline as `independent-verifier.md`, applied one phase earlier. A fresh, independent agent
adversarially probes the **draft** living plan doc's wave/unit decomposition before it reaches the
user checkpoint (Plan 2b). Catching a hidden shared-file conflict, a missed dependency, or a coverage
gap here is far cheaper than catching it once Execute has already burned cycles on a flawed plan.

Dispatched **once**, after the planning subagent (or `writing-plans`) produces the draft living plan
doc and before it is presented to the user for the plan checkpoint (`plan.md` § 2b).

## Why independent

- **Independent** — a *separate* agent that did not write the plan and has no stake in it looking
  complete. The planning subagent's decomposition is a *claim* about parallel-safety and coverage;
  this produces a *result*.
- **Judgment, not mechanics.** Spotting a hidden shared-file conflict between two units both marked
  "parallel-safe," or a dependency implied by overlapping scope but never declared, requires reasoning
  about what the paths actually mean — not running a fixed command and reporting exit codes. This is
  why it runs on a judgment-capable model, unlike the mechanical code verifier.
- **Structured verdict only** — the reviewer returns a compact findings list, not a narrated walk
  through every unit, keeping the integrator's context cheap.

## Model & isolation

- **Model:** sonnet (judgment task — reasoning about decomposition semantics, not mechanical
  execution). Escalate a single dispatch to opus only if the decomposition is unusually large or
  architecturally ambiguous, matching the escalation pattern already used elsewhere in this skill
  (`verify.md`, `parallel-orchestration.md`) — a standing opus reviewer is rarely worth its cost.
- **Isolation:** read-only. Point it at the current repo tree (to check declared scopes against real
  paths/modules) and the draft living plan doc; it makes **no edits, no commits**, and does not
  implement anything.

## Inputs (fill in before dispatch)

- **Draft living plan doc:** the "Waves & work units" block and the "Acceptance criteria" table,
  as produced by the planning subagent — not yet user-approved.
- **Design artifact:** for architecture/constraints context the decomposition should respect.
- **Assess findings:** scope, dependency map, acceptance criteria with baselines/thresholds.

## Dispatch prompt (template)

```
You are an INDEPENDENT plan reviewer. Do not edit any file, do not commit. Only inspect and report.

Draft living plan doc (Waves & work units + Acceptance criteria): <paste or path>
Design artifact: <path>
Assess findings (scope, dependency map, acceptance criteria): <path or summary>

Probe the decomposition for each of the following, checking declared unit scopes against the actual
repo tree where relevant:

  1. Shared-file conflicts — two units in the SAME wave whose path scopes overlap despite being
     marked parallel-safe.
  2. Missed dependencies — a unit's scope touches a path/module another unit also touches (or
     plausibly depends on), but no dependency is declared and they're not ordered into separate waves.
  3. Unsized units inside a wave — any unit lacking a story-point size that is nonetheless placed in
     a wave (violates: an Unsized unit may not enter a wave).
  4. Coverage gaps — any acceptance criterion in the criteria table with no unit mapped in
     "Satisfied by," especially an absolute all-of-set criterion.
  5. Isolation-method mismatches — a unit marked non-overlapping-path isolation whose scope actually
     overlaps a wave-mate's, or a worktree unit with no clear scope boundary.

Return ONLY this verdict — no narration, no per-unit walkthrough:

  VERDICT: CLEAN | ISSUES-FOUND
  Model: <state your own model identity — you know it>
  Waves inspected: <count>  ·  Units inspected: <count>
  Findings:
    - [<category from 1-5>] Unit(s): <A, B> — <one-line description> — Suggested fix: <one line>
    - ... (or "none")
```

## Reading the verdict (integrator)

- **CLEAN or resolved-ISSUES-FOUND is required before the plan checkpoint.** This is a hard gate, the
  same as the code verifier's: do not present the plan to the user for approval while a finding is
  outstanding. Resolve each finding (re-wave, re-size, re-map criteria coverage, or split a unit),
  then re-dispatch only if the fix materially changed the decomposition — a small edit (e.g. adding a
  declared dependency) does not require a full re-review.
- **This supplements the user checkpoint, it does not replace it.** A CLEAN verdict means the
  decomposition is internally sound; the user still reviews and approves waves and story points at
  the Plan 2b checkpoint (`plan.md`) on their own merits (priority, scope, sizing judgment).
- **A finding the integrator disagrees with is still logged.** If a finding is a false positive (e.g.
  an apparent path overlap that is actually read-only in one unit), record the reasoning in the living
  plan doc's decisions log rather than silently dismissing it — the same evidence-driven discipline as
  everywhere else in this skill.
- Record the outcome as a decisions-log entry; the raw reasoning stays in the subagent, out of the
  integrator's context.
