# Phase 4 — Verify

Whole-change verification, **beyond** the per-unit verification already done at each wave's
convergence. Delegate the rigor pass to **superpowers:verification-before-completion** when present;
else use this bundled checklist.

**Verify independently, and more than once.** As at wave convergence, the gate-running here is
delegated to an **independent** agent that re-runs the suite **multiple times (default 3×)** and
returns a structured verdict — never grade the whole change on a single run or on a subagent's own
say-so (SKILL.md Principle 8). See `references/independent-verifier.md` for the canonical dispatch
prompt and verdict format; keep the *judgment* (§1) with the integrator.

## 1. Grade every acceptance criterion (pass/fail)

**Model note:** the *measuring* is mechanical — absolute checks (version present, warning counts) are
**haiku**-level; comparative re-measurement + delta computation is **sonnet**-level. Delegate the
runs to keep their output out of your context; keep the **judgment** (is the criterion met given
ambiguous results?) with the integrator.

- **Absolute criteria:** check presence/absence directly (version reached, warnings at zero). For an
  **"all-of-set"** criterion (e.g. *all packages on version X*), cross-check the **criteria → units**
  map from Plan: it **fails** if any mapped unit was deferred, `Unsized`, or otherwise unexecuted —
  never grade it pass on a partial set. Surface the blocking units and get a user re-scope decision.
- **Comparative criteria:** **re-run the recorded baseline measurement method** and grade the delta
  against the captured before-value (e.g. before vs. after p95, bundle size). **Report both
  numbers**, not just pass/fail. Use the exact method recorded in Assess so the comparison is valid.

## 2. Whole-change lint & format gate

Run the **exact composite lint/test command CI runs** (recorded in Assess) across the integrated
change — not a convenience subset — and confirm the **formatter** has been applied (no diff on a
format-check). Must be clean before advancing. A gate that used a narrower command than CI's is a
**false pass**: it will go red the moment the MR pipeline runs. When the CI gate bundles lint into a
composite target (e.g. `test:ci` runs lint before tests, so a lint failure aborts the run), run that
composite target here so Verify matches the pipeline.

## 3. Code review of the produced code (discover-then-fallback)

Run a review over the **integrated change**. Reuse a code-review skill/agent present in the session
(e.g. a `code-review` skill, `platform-framework-mr-review`, or **superpowers:requesting-code-review**);
if several are present, prefer the most **project-specific** reviewer, and if still ambiguous, ask
the user. Else apply a bundled review checklist:

- Correctness against the acceptance criteria.
- Matches surrounding conventions.
- Error handling.
- Test quality (tests actually exercise the criteria, not just pass).
- No leftover scaffolding / debug code / dead code.

When falling back to a **fresh** bundled-review agent (no session review skill), run it on **sonnet**
— whole-change review is structured analysis of code semantics (correctness, conventions, error
handling, test quality), beyond haiku-level pattern matching, but doesn't need opus.

Triage findings: **blocking** issues generate remediation work units (looped back through Execute);
**non-blocking** issues are recorded in the living plan doc.

## 4. End-to-end regression suite (discover-then-fallback)

Run the project's project-wide **regression suite against the integration branch** — the converged
result of all waves, **not** per-unit — and grade the outcome as part of the pass/fail gate.

- **For dependency/version-upgrade work, verify on a CLEAN dependency re-resolve.** Before the
  regression run, wipe the resolved dependency state and re-resolve from scratch on the integration
  branch (`rm -rf node_modules <lockfile>` then reinstall / `npm ci` / `bundle install` / language-
  appropriate). A subagent's **cache-warm worktree can report green while masking latent resolution
  or compilation failures** that only surface on a fresh install — exactly what a reviewer or CI hits
  on a clean checkout. Also confirm the lockfile is stable (no unexpected drift) after the re-resolve.
  For non-dependency work (refactors, feature additions) this clean step is optional.
  - **To isolate a suspected install/resolution failure, reproduce it in a throwaway clean checkout**
    (a fresh temp directory with only the manifest + lockfile, dependencies installed from scratch)
    rather than debugging in a worktree carrying local caches and config. This confirms whether the
    failure is real (reproduces clean) or an artifact of local state, before you push and let CI find
    it. This is where **runtime/engine constraints bite** — a dependency that pins a runtime version
    can hard-fail a clean install on a newer runtime even though a warm worktree never re-checked it.
  - **A package manager's success output for a patch/override/resolution write is a CLAIM, not a
    RESULT** — the same standard already applied to a subagent's own test/lint self-report (never
    converge on it un-verified, SKILL.md Principle 8). Before relying on a write like
    `pnpm patch-commit`, an override, or a resolution pin, confirm it actually materialized in the
    **resolved** dependency store — e.g. for pnpm, check the resolved path for the patch's
    hash/marker (`readlink -f node_modules/.pnpm/<pkg>*`); use the equivalent resolved-store check
    for the project's package manager. If it didn't materialize, don't assume the write silently
    no-op'd and move on — re-run a plain install and re-check. (Observed failure: `pnpm patch-commit`
    reported success and even ran its own auto-install, but the patch didn't actually re-link into
    the resolved `node_modules` tree until a separate, explicit plain `pnpm install` was run
    afterward — this recurred more than once in-session before being caught.)

- **Discover, in order:** (1) a session skill/MCP (a Playwright runner/MCP, a CI regression entry
  point), then (2) an **in-repo invocation script** — a `package.json` script (`test:e2e`, `e2e`, …),
  a `playwright.config.*`, a Makefile target, or a CI job definition that runs the suite directly from
  the checkout — before falling further back to the categories below. Use whichever is found to kick
  off the suite and collect results.
- **Classify how the discovered suite can execute** before running it: `local` (runs against the
  checkout as-is), `remote-branch` (needs a deployed preview, but one publishes automatically off a
  pushed branch — no MR required), or `post-mr` (the only deployment that exists is triggered by
  opening an MR/PR, e.g. UUX). Infer this from the discovered script/CI config when it's explicit (a
  script that takes a deploy URL vs. one that takes an MR number); ask the user only when it can't be
  determined from evidence.
  - `local` / `remote-branch` → run now, per the categories below.
  - `post-mr` → **do not run here.** Record a `post-mr` deferral in the living plan doc's **Deferred
    inputs** table (capability, reason, "run in Roll out after MR creation" as the next step) and
    treat this criterion as satisfied-pending-Roll-out rather than failing Verify's gate on it —
    Roll out's post-MR E2E step (see `roll-out.md`) owns running and grading it from here.
- This gate runs on the **integration branch (whole change)** — distinct from the per-unit tests run
  inside each worktree during Execute. Even when the command is the same (e.g. `npm test`), the
  scope differs; run it against the converged branch, not a single unit.
- If the project has **no regression-grade suite** (only unit tests), do **not** silently grade
  "regression green": run what exists on the integration branch, **record the criterion's method as
  `unit-tests-only`**, and flag the coverage gap to the user rather than claiming a full pass.
- If an E2E/regression suite **exists but isn't runnable locally** — the target is not a standalone
  app (a library consumed by a host, a micro-frontend, a plugin/module that only runs inside a
  platform harness) — do **not** grade it green from a proxy alone. First **discover whether the
  host/platform repo exposes a harness or integration entry point**; if so, document its command +
  environment setup and invoke it. If the platform harness can't be automated in-session, fall back
  to: run everything that *is* runnable locally (unit/integration on the integration branch), record
  the criterion's method as **`platform-integration-required`**, prompt the user to run the
  platform-level E2E and report results, and **record the coverage gap so Roll out flags it in the
  MR/PR description** for the reviewer.
- Otherwise (no runnable suite at all) fall back to prompting the user to run their regression suite
  and report the outcome.
- **Filter known environmental failures.** Before failing on red, check the living plan doc's
  **Known environmental failures** list (see `living-plan-doc-template.md`). A failure that matches a
  recorded non-blocking entry (offline/CDN/network-only, CI-only, browser-specific, etc.) is
  **annotated, not blocking** — grade the criterion against the target environment (e.g. CI). Any
  failure **not** on the list is a real regression and blocks. New environment-only failures should
  be diagnosed and, if genuinely environmental, added to the list (with reason + environment) rather
  than re-litigated every session.
- **Normalize volatile output before comparing runs.** When you diff two runs (determinism/flake
  checks) or diff against a baseline, first mask incidental runtime data — durations (`[NNNN ms]`),
  timestamps, PIDs, temp paths, memory addresses — or the diff shows false differences. A determinism
  check compares *behavior*, not incidental data. Record the project's normalization pattern (e.g. a
  `sed`/regex mask) in the living plan doc for repeatable reuse.
- Regression failures are triaged like other Verify failures: they generate remediation work units
  looped back through Execute, then Verify re-runs. **Never advance to Roll out on a red regression.**

## 5. Cross-repo / consumer impact

Assess downstream impact where relevant (e.g. repos that consume this project's build output).
Record any consumer-side follow-ups.

**Sibling-repo drift.** When this project is one of a family of similar repos governed by shared
tooling or a shared CI contract, check the change against a **sibling repo that currently passes** —
a diff of the relevant config/manifest fields against a known-good sibling quickly surfaces a missing
required field or setting the shared pipeline will reject. This complements the CI-contract mapping
done in Assess and catches configuration drift before the MR/PR pipeline does.

## On failure — diagnose → remediation wave

Record the failure (doc + ticket), **diagnose root cause** (chain to
**superpowers:systematic-debugging** when present; else the bundled diagnosis steps below), and
generate a **remediation work unit / wave** looped back through Execute. Verify re-runs afterward.
**Never advance to Roll out on red.**

Root-cause diagnosis is **judgment-heavy** — run it at **opus** (or inherit if the integrator is
already opus); don't hand a hard cross-unit failure to a light model.

**Bundled diagnosis steps (fallback):** (1) reproduce the failure deterministically; (2) isolate it
to a single unit / commit / file (bisect the integration branch if needed); (3) reduce to a minimal
failing case; (4) form one hypothesis and test it before changing code; (5) fix, then re-run the
failing check before re-verifying the whole change.

## Gate to advance

- [ ] Every acceptance criterion graded **pass** (comparative deltas reported with both numbers).
- [ ] No criterion left **Blocked** by a deferred/`Unsized` unit (or the user has explicitly
      re-scoped it).
- [ ] Whole-change lint clean; formatter applied (no diff).
- [ ] Code review done; blocking findings remediated, non-blocking recorded.
- [ ] E2E regression on the integration branch **green**, or a `post-mr` deferral recorded (handed
      to Roll out) — for dependency/upgrade work, on a **clean dependency re-resolve** (lockfile
      stable), not a cache-warm worktree.
- [ ] Cross-repo impact assessed.
