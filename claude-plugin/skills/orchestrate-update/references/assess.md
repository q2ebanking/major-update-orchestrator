# Phase 1 — Assess

**Goal:** understand current state, scope, and blast radius; define what "done" means; anchor the
work to a tracking ticket. No implementation artifact is created yet — findings feed Plan.

## Recon (adaptive to repo size)

- **Always interview the developer:** what's changing, why, known risk areas, deadlines.
- **Small repos:** confirm with a few targeted **read-only** probes — package manifests, dependency
  graph, test/build scripts, `git status`.
- **Large / multi-package repos:** dispatch a **recon subagent** (e.g. `Explore`) to map structure,
  packages, dependency edges, and test setup, returning a **compact summary**. This keeps large
  file reads out of your main context.

## Requirements & measurable acceptance criteria

Define the requirements and desired outcome, then the **measurable acceptance criteria** — the
concrete, checkable conditions that constitute "requirements met." Every criterion must be gradable
without judgment calls. Examples:

- Performance target: `p95 login < 800ms`
- Version target: `all packages on Ember 6.12`
- Quality state: `zero deprecation warnings in build`

Criteria are one of two kinds:

- **Comparative** — graded against a before-value (performance, bundle/asset size, memory, test-run
  time, warning/error counts, coverage). **Requires a baseline** (below) **and an explicit
  target/threshold** — an absolute value or a max delta (e.g. `≤ 10 warnings`, `≥ 50% reduction`,
  `within +5%`), **never a bare direction word** like "reduced" or "faster" (a direction can't be
  graded pass/fail).
  - **Major-version / framework upgrades — set the threshold provisionally.** When the "after"
    value is genuinely unknowable up front (a new framework's bundle size, warning profile, or
    runtime characteristics), a hard pre-work threshold is a guess that's often wrong by
    construction. Either carry **explicit headroom** (e.g. `bundle within +20% — provisional, revise
    after first build`) or mark it `TBD — set after wave N`, note it as provisional, and firm it up
    from the first real measurement. This avoids false precision; it does **not** waive the revision
    discipline — setting the final value still gets a logged rationale via SKILL.md Principle 5.
- **Absolute** — a state reached (a version, warnings at zero). Checked by presence/absence; no
  before-value needed.

## Baseline data capture (scaled to the criteria)

For **every comparative criterion**, capture the **before-value now**, plus the **exact measurement
method** — command, tool, environment, sample size / number of runs — so Verify can re-run it
identically. Record both in the findings (and later in the living plan doc); the before-value is the
denominator Verify grades the delta against.

- Expensive/involved baselines (e.g. a profiling run) may be dispatched to a subagent to keep the
  main context lean. Simple metric extraction (bundle size, warning counts) is **haiku**-level; a
  profiling run that needs output parsing is **sonnet**-level.
- If a comparative criterion **cannot** be baselined, either make it absolute, or mark the baseline
  `Not captured` and flag that its delta cannot be verified. **Never fabricate a before-value.**
- **Note environment-dependent failures now.** If the test/build baseline shows failures that are
  environmental (offline/CDN, network-only, CI-only, browser-specific) rather than real, record them
  in the living plan doc's **Known environmental failures** list with their reason and which
  environment they pass in. This is the baseline Verify grades against — it stops each session from
  re-diagnosing the same non-blocking failures. Also record the **recon subagent** as **sonnet**-level
  (mapping module/dependency coupling well enough to inform wave boundaries is light structural
  judgment — beyond haiku pattern-matching, which can miss non-obvious coupling — but short of the
  opus-level calls the integrator makes).

### Validate the baseline is representative (don't anchor to a false number)

A baseline becomes the denominator for every comparison and, for a test baseline, the bar the whole
change is graded against — so a wrong baseline corrupts the work silently and for a long time. Before
you record a test/build or comparative baseline, **confirm it actually measures what you think:**

- **Does the runner exercise the whole surface?** Confirm the count/metric reflects *all* expected
  test types (unit **and** integration/rendering/end-to-end), not a subset a broken or misconfigured
  runner silently skipped. A suite that reports "green" while executing a fraction of its tests is the
  classic false baseline.
- **Is the number sane for the project's size?** Sanity-check the magnitude against the codebase
  (e.g. a large app reporting a handful of tests, or zero skips where you'd expect many, is a smell).
- **Is it reproducible?** Re-run once; a baseline that changes between identical runs isn't a baseline.

If any check fails, fix the measurement **before** recording the number — a false-green baseline that
rides through several units masks real regressions until something finally measures correctly. If the
baseline is later proven wrong mid-flight, revise it through the documented path (SKILL.md Principle
5), don't hand-patch it silently.

## Tracking ticket (discover-then-fallback)

See `tracking-integration.md`. In short:

1. Discover a tracking MCP/skill in the session (Jira, GitLab, etc.).
2. If found: read the existing ticket for requirements, or create a parent ticket (confirm first).
3. If none: ask the user for a ticket ID/URL to record, or proceed ticket-less and note it.

## Toolchain discovery (lint + formatter)

Detect the project's **lint and code-formatter commands** and how they're invoked — from
`package.json` scripts, a Makefile, pre-commit config, or CI config. Record them in the findings so
Execute (per-unit gate) and Verify (whole-change gate) can apply them. If none can be found, ask the
user for the commands, or explicitly note the project has no lint/format step.

- **Capture the exact command CI runs, not a convenience subset.** Projects often expose narrow
  local commands (e.g. `lint:js`, `lint:hbs`, `lint:types`) *and* a composite gate CI actually runs
  (e.g. `lint`, `test:ci`, `make test`). Record the **CI gate command verbatim** from the CI config
  (`.github/workflows/*`, `.gitlab-ci.yml`, a `Makefile` target, etc.) so Execute and Verify run the
  same thing CI does. A subset that passes locally can still hard-fail the CI pipeline — a green
  Verify that used a narrower command is a false pass. If no CI config exists, ask the user for "the
  exact lint/test command your CI runs."

## CI contract discovery (the full gate, not just lint/test)

Lint and test commands are only part of what CI enforces. Modern pipelines add **non-code gates** —
required-file/manifest validators, secret/credential checks, metadata or inventory field checks,
schema/config validation — that a change can trip **without touching code**. If these are only
discovered when the MR/PR pipeline goes red, a fully-green Verify still fails at roll-out. Map the
**whole CI contract now:**

- **Enumerate every gating job**, not just the build/test ones — inspect the CI configuration for
  validators and required-artifact checks alongside the compile/lint/test steps.
- **Follow remote / shared pipeline references.** Many projects don't define their pipeline inline —
  the local CI config **delegates to a shared or remote pipeline** (an included/remote config, a
  reusable/centralized workflow, a template repo). When it does, **fetch and read that remote
  definition** (via the CI platform's API or CLI, or the shared repo directly) to see the gates it
  actually enforces — they are invisible from the local config alone. This is discover-then-fallback:
  use whatever platform tooling the session has; otherwise ask the user for the shared pipeline's
  location.
- **When the project belongs to a family of similar repos** governed by the same shared pipeline,
  a fast way to find a missing required field/file is to **diff the target repo's config against a
  sibling repo that currently passes CI** — the delta is usually the gap.
- **Discover commit-message conventions and branch-protection rules**, not just pipeline jobs — a
  server-side commit-message hook (ticket-prefix regex, conventional-commits format, sign-off
  requirement) or branch-protection rules (required status checks, no-force-push, merge-commit
  restrictions) can reject a push independently of the CI pipeline. Actively look for these and
  record what's found, or mark `Not provided`/`Not discoverable` if they can't be determined — never
  assume neither exists just because they weren't surfaced. (Observed failure: an integration
  branch's own bundled `git merge --no-ff` step produced merge commits using git's default
  merge-commit message, which didn't match the target repo's commit-message hook — undiscovered
  until the branch was finally pushed after 58 commits had accumulated, requiring a full-branch
  history rewrite to fix.)
- Record the discovered gates (and any that this change might trip) in the findings, so Verify can
  run the full CI-equivalent gate rather than only lint/test. Pre-existing gate failures unrelated to
  the change belong in **Known environmental failures** with that note.

## Readiness gate (must pass before Plan)

- [ ] Requirements + desired outcome confirmed by the user.
- [ ] **Measurable acceptance criteria defined.**
- [ ] Every **comparative** criterion carries an explicit **target/threshold** (absolute value or
      max delta), not a direction word.
- [ ] **Baseline captured** for every comparative criterion (before-value + repeatable method), or
      explicitly marked `Not captured` where infeasible.
- [ ] Tracking ticket recorded (or explicitly waived).
- [ ] Test/build **baseline captured** (green, or knowingly-red documented) **and validated as
      representative** (runner exercises the whole test surface; count is sane; reproducible).
- [ ] **Lint/format commands identified**, including the **exact composite command CI runs** (not
      just local subsets), or their absence explicitly noted.
- [ ] **CI contract mapped** — all gating jobs (including non-code validators and any remote/shared
      pipeline the local config delegates to), or their absence explicitly noted.
- [ ] Git state clean, or a known/documented state.

Findings feed directly into Plan; do not create the living plan doc yet.
