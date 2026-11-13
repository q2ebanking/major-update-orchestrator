# Independent Verifier — canonical dispatch

Independent verification is the skill's core rigor discipline (SKILL.md Principle 8): a unit — or the
whole change — is **never** graded green on its own self-report. This file is the canonical, bundled
prompt + verdict contract so the verifier isn't re-improvised each time. It is **discover-then-fallback
compatible**: if the session has a verification skill (e.g. **superpowers:verification-before-completion**),
chain to it; otherwise dispatch a plain subagent with the prompt below.

Used in two places:

- **Per-unit, at wave convergence** (`parallel-orchestration.md` § Converge, `execute.md`) — one
  verifier across the wave's converged worktrees.
- **Whole-change, in Verify** (`verify.md`) — one verifier on the integration branch.

## Why independent + multi-run

- **Independent** — a *separate* agent that only inspects and runs; it does not implement, so it has
  no stake in reporting success. The executing subagent's "tests pass" is a *claim*; this produces a
  *result*.
- **Multi-run (default 3×)** — a single green run hides flakes and order-dependent passes. Re-running
  the same gate several times and requiring **all** runs green catches non-determinism before it
  reaches a reviewer or CI.
- **Structured verdict only** — the verifier returns a compact verdict, not raw suite output (which is
  voluminous and would bloat the integrator's context). It runs on **haiku**: this is mechanical
  execution, not judgment. The *judgment* — is an ambiguous or partial result acceptable? — stays with
  the integrator.

## Model & isolation

- **Model:** haiku (mechanical run-and-report).
- **Isolation:** read-only. Point it at the already-converged worktree/branch, or give it a throwaway
  **detached** worktree (`git worktree add --detach <ref>`); it must **never** run
  `git checkout`/`git switch` in the integrator's checkout (see the shared-checkout hazard in
  `parallel-orchestration.md`). It makes **no commits**.

## Inputs (fill in before dispatch)

- **Target:** worktree path(s) or branch/ref to verify.
- **Gate commands:** the exact commands to run, in order — the **CI-equivalent composite** test/lint
  command (from Assess), the formatter check, and the build if separate. Not a convenience subset.
- **Run count:** default **3**; raise for suites with a known flake history.
- **Known environmental failures:** the list from the living plan doc, so genuinely-environmental
  failures are reported as annotated-not-blocking rather than as regressions.
- **Normalization:** the volatile-output mask (from the living plan doc) to apply before comparing
  runs, so a determinism check compares behavior, not timestamps/durations/paths.
- **Success predicate:** the exact pass condition, matching the criterion's **documented target** —
  **including any known-acceptable deviations** (N baseline skips, M pre-existing warnings, a subset
  scope). Bake these thresholds into the gate commands or the verdict interpretation you hand the
  verifier; do **not** give it a re-typed stricter "all green" ideal. A predicate that ignores
  documented-acceptable skips/warnings produces a **false RED** on a result that actually meets the
  criterion — the verifier runs on haiku and grades against the predicate you give it, so the
  predicate must carry the acceptable state; the reasoning about it stays with you.

## Dispatch prompt (template)

For any gate command expected to run more than a few minutes, the verifier must background it with
the session's native background-execution facility (e.g. the Bash tool's `run_in_background: true`)
applied directly to the command itself — never a shell-level `nohup ... & disown`. The native
mechanism delivers an immediate completion notification, success or failure, the moment the process
actually exits; a shell-level detach only gets checked via periodic log polling, which misses fast
failures until the next poll and gives no live status in between. Never combine the two: wrapping a
command in `nohup ... &` **and also** setting `run_in_background: true` double-backgrounds it — the
tool-level tracking fires on the wrapper shell's immediate exit, not the real command's completion,
silently detaching it from notification tracking. (Observed: a `pnpm run build:noprereq` reported
"completed" in ~1 second while the actual 40+ minute build kept running, detached and untracked.)

```
You are an INDEPENDENT verifier. Do not modify any code, do not commit, do not switch branches.
Only run the commands given and report.

Target: <worktree path / branch ref>
Run each of these gate commands, in order, <RUN_COUNT> times total:
  1. <exact CI-equivalent test command>
  2. <formatter check command>        # must show no diff
  3. <lint command, if separate>
  4. <build command, if separate>

Before comparing runs, normalize volatile output with: <normalization mask, or "none">.
Treat these as known non-blocking environmental failures (annotate, don't fail on them):
  <known environmental failures, or "none">.

Return ONLY this verdict — no raw suite output:

  VERDICT: GREEN | RED
  Model: <state your own model identity — you know it>
  Runs: <passed>/<total> fully green
  Per-gate: <tests: pass/fail> · <format: clean/diff> · <lint: clean/fail> · <build: pass/fail>
  Test counts: <passed>/<skipped>/<failed>   (flag if this looks off for the project size)
  Non-determinism: <none | which check varied across runs>
  Env-annotated (non-blocking): <list, or none>
  Failures (real): <file:test — one line each, or none>
  git status: <clean | dirty — list unexpected files>
  Worktrees: <expected-removed list matches actual | mismatch: ...>   # wave-convergence dispatches only
```

The `Worktrees` field only applies when the verifier is being dispatched at **wave-convergence time**
(not for the whole-change Verify phase). When the living plan doc claims certain unit worktrees were
"merged, removed," the verifier confirms via `git worktree list` that they're actually gone rather than
taking the claim on faith.

## Reading the verdict (integrator)

- **GREEN only if every run was fully green** across every gate. `2/3` is **RED** — investigate the
  non-determinism before converging.
- **Reconcile a RED against known-acceptable baselines before treating it as a fail.** If the verdict
  is RED but the failing/skipped/warning count matches a **documented-acceptable** baseline (Assess's
  known skips, recorded non-blocking warnings), the *predicate* was too strict, not the change —
  re-grade against the criterion's actual target rather than converging on the RED label. A genuine
  regression is any deviation **not** on that documented list; a match to it is a predicate-spec bug
  to fix (see § Inputs — Success predicate), not a failure to remediate.
- **A self-report / verdict mismatch is a signal, not noise.** If a unit reported itself green but the
  independent verifier returns RED, trust the verifier and treat the unit as failed — roll it into the
  next wave as remediation (`parallel-orchestration.md` § Failure handling).
- **Sanity-check the counts.** A test count far below expectations (or unexpected skips) can mean the
  runner isn't executing the whole surface — the same false-green failure mode Assess's baseline
  validation guards against. Reconcile it before grading.
- **An interrupted-then-resumed verifier is not trustworthy — discard it, don't resume or average it.**
  If a verifier dispatch was interrupted (by the harness, a context limit, or any other cause) and
  resumed before completing its full run count, its verdict carries no weight: discard it entirely and
  dispatch a fresh verifier rather than resuming it. Do not attempt to merge a partial
  pre-interruption tally with a post-resumption one — the two are not comparable. For a large target
  (many packages/modules), the fresh re-dispatch can be scoped narrowly to just the portion that hadn't
  completed, rather than re-running the whole thing. (Observed: an independent haiku verifier was
  killed and resumed several times mid-run and gave inconsistent GREEN/RED/GREEN verdicts across the
  resumptions before all packages finished — treated as unreliable, and correctly fixed by dispatching
  a second, freshly-scoped verifier rather than trusting the resumed one.)
- Record the outcome as a transition-log entry; the raw output stays in the subagent, out of your
  context.
