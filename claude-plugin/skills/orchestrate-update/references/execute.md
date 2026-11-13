# Phase 3 — Execute

Drive the waves. **You are the integrator; the work happens in subagents.** Lean on
**superpowers:dispatching-parallel-agents** when present; otherwise use the bundled fan-out guidance
in `parallel-orchestration.md`.

## Test-Driven Development (required)

Each work unit follows **RED → GREEN → refactor**:

- The executing subagent **first authors the failing test(s)** from the unit's done-criteria /
  acceptance criteria (RED), then implements to green, then refactors.
- Chain to **superpowers:test-driven-development** when present; otherwise bundled
  RED→GREEN→refactor guidance.
- A unit is not "done" until its tests pass. Traceability chain:
  **Assess acceptance criteria → per-unit done-criteria → failing tests → green.**

**For upgrade/migration-shaped units** (where the "feature" is *a version reached* or *a
deprecation removed*, not new behavior), the RED artifact is an **executable assertion of the target
state** — e.g. a check that the package resolves the target version, that the build/test suite runs
green under the new version, or that a deprecation count is zero — plus tests for any behavior that
had to change to get there (a migrated modifier/API still works). It fails before the migration and
passes after; "no meaningful test to write" means the done-criteria aren't concrete enough yet.

## Per-unit quality gate

After tests are green, the executing subagent:

1. Applies the project's **code formatter** to its changed files.
2. Runs the project's **linter** and fixes any lint errors it introduced (auto-fix where available).
3. **Runs the project's build, if it has one distinct from tests** — a `build`/`compile`/`bundle`
   step separate from the test runner (detect it from Assess's CI-contract mapping). For any
   compiled/bundled target (TypeScript, webpack, Vite, Rollup, esbuild), **tests-green ≠ build-green**:
   tree-shaking exposing unused imports, build-time type checks, and minification can fail while every
   test passes. A test-only per-unit gate lets a production-build regression ride **latent** from a
   toolchain wave until it finally surfaces at Verify or in CI — run the build per unit (or at minimum
   once per wave) so it's caught where it was introduced.

The commands come from Assess's toolchain discovery and are passed **in the unit's prompt**. A unit
is not "done" until it is **tests-green, formatted, lint-clean, and — for projects with a build
step — build-green**.

**Lint with the CI-equivalent command, not a local subset.** Pass the unit the same composite lint
command CI runs (recorded in Assess), not a narrower convenience script — a subset can pass locally
while CI's full gate (which may bundle template/type/style linters) fails. If a unit legitimately
can't clear a rule that CI enforces, treat that as tracked debt to suppress deliberately (with
justification), not as an "out of scope" pass — CI will still hard-fail on it.

## Per-wave loop — fan out / converge / verify

For each wave, in order:

1. **Mark in progress.** As each unit is dispatched, move its state in the living plan doc to
   **In Progress** and append an "opened" entry to the transition log (`timestamp, unit id, ticket
   ref, from → to`). If the unit has a matched ticket, transition it to the tracker's **equivalent**
   in-progress status — status names vary, so map to the equivalent rather than assuming a literal
   "In Progress" — check the living plan doc's cached Tracker Transition Map first; only invoke live
   discovery if no cached entry exists for this role (see `tracking-integration.md`). Ticket updates
   follow confirm-before-external-writes.
   Ticket-less or no tracker → update only the living plan doc.
2. **Fan out** all parallel-safe units in the wave as concurrent subagents in **one batch**. Each
   gets a self-contained prompt: scope, files, done-criteria, "write tests first," the lint/format
   (and build, if present) commands, "**stay in your lane**," and the **gate-discipline hard rules**
   (never commit on red; prove any "pre-existing" claim; no degrading/band-aid fixes; self-report
   honestly — see `parallel-orchestration.md` § Dispatching a wave). **Dispatch implementation units
   via the `implementation-executor` agent by default** — it bakes these rules in and runs on a
   cheaper model (sonnet). Executing a unit *inline in the integrator session* is a **deviation**, not
   a shortcut: do it only for a genuinely trivial unit, and when you do, **log the reason in the living
   plan doc's decisions log**. Red flag — **if you are editing a unit's source files yourself, you have
   silently become the executor: stop and dispatch.**
3. **Isolation:** each parallel unit runs in **its own git worktree** (chain to
   **superpowers:using-git-worktrees** when present; else bundled worktree steps in
   `parallel-orchestration.md`). **Delegation and worktree-isolation are independent decisions.**
   Worktrees isolate *files*; subagents isolate *context and model cost*. Forgoing worktrees —
   disjoint-file units, prohibitive monorepo install cost, or a shared build cache that defeats
   per-worktree isolation (e.g. a single embroider/temp cache) — is **not** a reason to run the unit
   inline. Dispatch an **in-place** executor on the current branch instead, serializing commits if
   units share one git index. Dropping worktrees never means dropping the subagent.
4. **Converge:** integrate completed worktrees, resolve cross-unit conflicts, run per-unit
   verification (**delegate this to a haiku agent** to keep voluminous test/lint output out of your
   context — see `parallel-orchestration.md` § Converge), move each completed unit to **Done**
   (append a "closed" transition-log entry), and transition its matched ticket to the tracker's
   equivalent done/ready-for-review status. **Fold each completed subagent's reported tokens +
   tool_uses into the usage rollup** (executor + verifier), keyed by model — see `usage-report.md`.
   Update the living plan doc + tickets, then advance to the next wave.

## Skill gaps

Act on the decision recorded in Plan: dispatch with the reused skill, or **author the new skill
first**, then dispatch. See `skill-discovery.md`.

## Failure handling — isolate, continue, report

A failing unit (subagent error, red tests, or merge conflict) does **not** abort its siblings:

- Record the failure in the living plan doc (and ticket).
- Integrate the units that **succeeded**.
- Surface the failure set at convergence.
- **Failed units roll into the next wave** as remediation work.

Units that did not complete remain **In Progress** or move to a blocked/failed state.

**Recurring-pattern audits are scoped to audit time.** When a comprehensive audit sweeps for a
recurring defect signature across the codebase (e.g. "every addon doing X"), that sweep only covers
what existed *at audit time*. A later unit that lands new code — especially a cross-repo or
dependency-bump unit pulling in code that wasn't present during the original audit — can reintroduce
instances of the same signature. Don't treat the one-time sweep as covering the plan's remaining
lifetime: when a later unit touches related territory, give it a targeted re-check for the same
signature, not just its own narrow scope.

## Gate to advance

- [ ] Every unit is tests-green, formatted, lint-clean, and — for projects with a build step — build-green.
- [ ] No unit was executed inline without a justification logged in the decisions log.
- [ ] All waves converged (or remaining failures explicitly carried forward as remediation).
- [ ] Living plan doc states + transition log current; tickets transitioned.
