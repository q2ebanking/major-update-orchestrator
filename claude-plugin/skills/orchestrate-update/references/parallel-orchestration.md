# Parallel Orchestration — waves, worktrees, isolation

This is the payload of the skill. The five phases are scaffolding; the value is decomposing a
codebase-spanning change into **independent work units** and driving them **in parallel with
subagents, safely**. Chain to **superpowers:dispatching-parallel-agents** and
**superpowers:using-git-worktrees** when present; the bundled guidance below applies when they're not.

## The wave model

A **wave** is a batch of work units that are all **parallel-safe with each other**:

- **No shared files.** Two units in the same wave must not edit the same paths.
- **No intra-wave dependencies.** If unit B needs unit A's output, B goes in a later wave.
- **Ordered.** Waves run in sequence; each converges before the next begins.

A dependency graph over units determines the waves: wave 1 is everything with no unmet dependency;
wave 2 is everything whose dependencies are satisfied by wave 1; and so on. Keep waves as wide as
isolation safely allows — width is the parallelism you're buying.

```
Wave 1:  [A] [B] [C]                  ← fan out, all independent
            └── converge ──┐          (C fails → rolled forward)
Wave 2:  [C'=retry of C] [E=needs B]  ← C's dependents wait; E is free to go
            └── converge ──┐
Wave 3:  [D=needs A,C]                ← waited on C's remediation
            └── converge ──┐
Wave 4:  [F=needs E]
            └── converge → Verify (whole change)
```

Note how the retried unit **C'** runs **ahead of its dependents** (D waits for it), while an
unrelated ready unit (E, needing only the completed B) still fans out in parallel: a failed unit and
anything that depends on it can never be wave-mates, so remediation pushes only *its* dependents to a
later wave (see Failure handling).

## Isolation

Each parallel unit runs **isolated** so siblings — and the integrator — can't corrupt each other.

> ⚠️ **Shared-checkout hazard (data loss).** A subagent that runs `git checkout`/`git switch` in a
> checkout the **integrator is also using** moves that working tree out from under you, silently
> reverting your uncommitted edits (most painfully, the living plan doc). The commit stays safe on
> its branch, but working-tree changes are clobbered. **Never dispatch a unit into the integrator's
> own checkout.** Worktree isolation below is what prevents this — it is **required**, not a
> preference.

- **Required: one git worktree per unit.** The subagent works in its own worktree/branch; you
  integrate completed worktrees at convergence. Chain to **superpowers:using-git-worktrees** when
  present; otherwise the bundled steps are:

  ```sh
  # once per update: an integration branch off the base branch
  git switch -c update/<slug>

  # per unit, before dispatch — its own worktree + branch off the integration branch:
  git worktree add ../wt-<unit> -b unit/<unit> update/<slug>
  #   → dispatch the subagent with its working directory set to ../wt-<unit>

  # at converge, per unit in dependency order:
  git switch update/<slug>
  git merge --no-ff unit/<unit>      # resolve any cross-unit conflicts here
  git worktree remove ../wt-<unit>
  git worktree list                  # confirm it's actually gone before the doc records it as removed
  git branch -d unit/<unit>
  ```

  Verify runs on `update/<slug>` (the integration branch); Roll out's MR/PR(s) are cut from it.
- **The integrator gets its own worktree too.** Run your own doc edits (living plan doc, design
  artifact) and merges from a **dedicated integration worktree** on `update/<slug>` — separate from
  every unit's dispatch point — or, at minimum, commit your working-tree edits **before** each
  dispatch. This keeps subagent branch switches from ever touching your uncommitted state.
- **Measure-only / read-only agents: use a detached worktree.** For an agent that only runs a suite
  or collects a metric (no commits), add a throwaway detached checkout so it never needs a branch:

  ```sh
  git worktree add --detach ../wt-measure <ref>   # e.g. update/<slug>
  # …run the measurement there, then:
  git worktree remove ../wt-measure
  ```

- **A branch can live in only one worktree at a time.** `git worktree add` on a branch already
  checked out elsewhere errors. To give a second agent read-only access to the integration branch's
  state, use `--detach <ref>` (above) rather than the branch name.
- **Confirm worktree removal before the doc says so.** `git worktree remove`'s exit code isn't proof
  the directory is actually gone, and the living plan doc's "removed" note is not proof either — check
  `git worktree list` (it should no longer list `../wt-<unit>`) before marking the unit's worktree
  removed. A unit's worktree was once found still present and checked out on disk deep into Execute
  despite the doc recording it as "merged, removed" — undetected drift between the doc's claimed state
  and physical reality.

## Dispatching a wave

Fan out **all** the wave's units as concurrent subagents in **one batch** — a **single message
containing multiple concurrent Agent tool calls**, not one dispatch per message (sequential
messages serialize the work and defeat the parallelism). Each unit's prompt is **self-contained**:

- **Scope:** exactly which files/paths this unit owns.
- **Done-criteria:** the unit's checkable criteria, traceable to Assess.
- **Test-first:** "write the failing test(s) from the criteria before implementing."
- **Toolchain:** the lint + format commands — and the **build** command if the project has one
  distinct from tests — to apply before finishing.
- **Stay in your lane:** do not touch files outside scope; surface cross-cutting needs instead of
  reaching outside.
- **Gate discipline (hard rules — an independent verifier will re-check):**
  - **Never commit while any gate is red.** Tests, lint, format (and build, if present) must all be
    green in the unit's worktree before it commits.
  - **Don't rationalize a red as "pre-existing."** If the subagent believes a failure predates its
    change, it must *prove it* — cite the same check failing on the base ref (git history or the
    recorded baseline) in its report. An unproven "pre-existing" claim is treated as a real failure.
  - **No degrading or band-aid fixes.** Don't delete/skip a failing test, loosen a type, or patch a
    symptom to force green. If the honest fix is outside scope, report it — don't reach for a
    workaround.
  - **Self-report honestly.** State the true gate status; the integrator dispatches an independent
    verifier that re-runs every gate, so a false green is caught and rolled back as remediation.

  The **`implementation-executor`** agent bakes these rules in — prefer it for implementation units so
  the discipline isn't re-typed (and drifted) every wave.

Keep the prompt to what the subagent needs to execute its unit. Don't restate the whole plan.
**Leave out** the integrator's convergence concerns, other units' scopes or dependencies, the full
wave structure, and *why* the decomposition was chosen — the subagent executes one unit and does not
need the orchestration around it.

### Model per unit

The skill doesn't pin a model globally — assign per unit to match the work, so mechanical units
don't burn the integrator's heavy model:

- **Measure-only units** (run a suite / collect a metric, no code changes) → **haiku**.
- **Implementation units** (dependency bumps, code migration, moderate fixes) → **sonnet** —
  dispatch via the **`implementation-executor`** agent, which defaults to sonnet and carries the
  gate-discipline hard rules from § Dispatching a wave.
- **Judgment-heavy units** (ambiguous requirements, architectural calls) → **opus** (or inherit).

**Announce the model at dispatch, don't wait until convergence to record it.** The model is already
known before the Agent call fires — from the dispatched agent's own frontmatter (e.g.
`implementation-executor`'s `model: sonnet`) or an explicit override — so state it in the same message
that announces the dispatch (e.g. "Dispatching F9 → `implementation-executor` (sonnet)") and log it in
the transition log's "opened" entry, not only in the usage rollup after the fact. The Agent tool's own
completion notification doesn't surface which model actually ran, so the declared-at-dispatch model is
the only record — don't let it go unstated. Each dispatched agent should also state its own model
identity in its final report (see `implementation-executor.md` § "What you return"), giving a
second, independent point of confirmation.

### Subagent type per unit — fresh, not a fork, for execution work

Model is *how strong* the agent is; **agent type** is *what context it starts with* — and it matters
just as much for execution-heavy units:

- **Execution-heavy units** (code changes, dependency bumps, migrations — anything that must *use
  tools* to produce commits) → dispatch a **fresh** subagent (omit the fork option / use a
  general-purpose agent). A fresh agent starts clean and gets to work.
- **A context-inheriting fork can narrate instead of execute.** A fork that inherits a long,
  summary-laden orchestrator context is prone to *writing a recap of what should be done* rather than
  doing it — it can return quickly having made **zero tool uses**, no worktree, no commit. Reserve
  forks for **read-only survey/research** questions where you want the answer without the tool noise
  in your own context, never for units that must land code.
- If a dispatched unit returns with no worktree/branch/commit and a prose summary, that's this
  failure mode: **re-dispatch it as a fresh agent** with the same self-contained prompt.

## Converge

At the end of a wave you are the integrator:

1. Integrate each completed worktree; resolve cross-unit conflicts.
2. **Verify each unit independently — never converge on its own self-reported green.** A subagent's
   "tests pass" is a claim, not a result; self-reports are wrong often enough to leak regressions into
   the integration branch (SKILL.md Principle 8). Dispatch a **separate** agent that re-runs the gate
   (tests green, formatted, lint-clean) **multiple times — default 3×** — to catch flakes and false
   positives, and returns only a **structured verdict** (not raw output). Delegating also protects
   context: raw test/lint output is voluminous (often 10–20k tokens for a multi-unit wave), and
   running it inline dumps all of it into the integrator's context wave after wave. Run this on
   **haiku** (mechanical), across the completed worktrees; run inline only if the wave is a single
   trivial unit. Use the canonical prompt + verdict format in `independent-verifier.md`.
3. Update the living plan doc: states → Done, append "closed" transition-log entries; transition
   matched tickets; refresh the `Last updated` header timestamp. **Fold each completed subagent's
   reported tokens + tool_uses into the usage rollup** (each unit's executor and its verifier), keyed
   by the model it ran on — see `usage-report.md`.
4. **Archiving checkpoint.** If the active transition log exceeds ~50 rows, move rows for units that
   reached Done more than a wave ago into the collapsed "Archived transitions" section; archive the
   decisions log once active entries exceed ~20 **or** the active Decisions section exceeds roughly
   150 lines, whichever comes first — decision entries vary hugely in length (a root-cause
   investigation entry can run 15–20 lines), so a count-only threshold can let the doc grow very large
   while staying under the entry-count trigger. Keeping the active tables lean is what keeps each
   session's rehydration read cheap — make this a checked step here, not something you must remember
   to notice.
5. **Push the integration branch.** After merging this wave's units into `update/<slug>`, push it
   (`git push`, or `git push -u origin update/<slug>` on the first push) — don't wait until Roll out to
   push for the first time. Pushing every wave surfaces any server-side policy mismatch
   (commit-message hooks, branch-protection rules, required-status-checks, etc.) early and cheaply,
   against one wave's worth of commits, instead of catastrophically against the whole branch's history
   at the worst possible time.
6. Advance to the next wave.

## Failure handling — isolate, continue, report

A failing unit does **not** abort its siblings:

- Integrate the units that succeeded.
- Record the failure (living plan doc + ticket); surface the failure set at convergence.
- **Roll the failed unit into the next wave** as remediation. If it had cross-wave dependents,
  those dependents wait until the remediation lands.

This is what makes wide fan-out safe: one bad unit costs one unit, not the wave.
