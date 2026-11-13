---
name: orchestrate-update
description: Orchestrate a codebase-spanning migration, framework upgrade, platform change, cross-cutting refactor, technical-debt sweep, or performance initiative through Assess, Plan, Execute, Verify, and Roll out. Use also for an active update's burndown or worker-usage report.
---

# Orchestrate a Major Update in Codex

Use this skill when a change spans packages, modules, or teams and cannot be
landed safely as one small change. Do not use it for a single-file fix or a
change confined to one module.

The payload is safe parallelism: decompose the change into independent work
units, isolate each unit, converge them deliberately, and independently verify
the result. The lifecycle is **Assess → Plan → Execute → Verify → Roll out**.

## Codex operating rules

You are the integrator. Preserve the user's authority over scope and external
writes; workers perform bounded implementation and verification tasks.

- First inspect the repository and `docs/*-plan.md`. An existing plan means
  resume: read only its lifecycle header, next steps, open/failed/blocked work
  units, active decisions, active execution lessons, known environmental
  failures, and tracker map. Do not load the append-only transition log on
  resume.
- Keep two documents, never duplicating their authority: a Design artifact for
  rationale, architecture, alternatives, and risks; a living plan for
  sequencing, work-unit states, criteria, baselines, and timestamps.
- Record deferred user-provided facts before proceeding with other work. Put
  the exact value, the action intentionally not taken, its reason, its owner,
  and the concrete next step in the living plan's **Deferred inputs** table.
  This includes tracker hierarchy (initiative, epic, parent), required fields,
  commit conventions, rollout constraints, and other instructions that have
  not yet been applied. Never substitute an invented value or rely on memory
  across turns.
- Make no unsupported claim. Unknown commands, paths, APIs, ticket fields, and
  baselines are `Not provided` until discovered.
- Discover the session's available skills, connectors, review tooling,
  collaboration capability, and project CLIs before using them. Reuse a
  capability when it genuinely fits; otherwise follow the bundled procedure or
  provide a user handoff. See `references/skill-discovery.md`.
- Before starting work in each lifecycle phase, announce the phase and render
  its **phase-entry skill table** with the skills you plan to attempt. Resolve
  capability-matched and assistive candidates by scanning the full
  session-available skill list, including user-specific skills not named in
  this plugin. Ask whether the user would prefer any other skills and wait for
  their response before phase work. Check any suggested skill against the
  active session and revise the proposal before proceeding. Ask the user to
  choose only among multiple unordered candidates for the same role; follow
  explicitly ordered fallback chains in order. See `references/skill-discovery.md`.
- During Assess, if no usable ticketing technology is discovered, ask once
  whether the update should use a tracker or remain ticketless. If no usable
  remote-source-repository API or CLI is discovered, ask once which remote
  system and API/CLI should be used for branch and PR/MR work. Record the
  response or explicit deferral in the living plan; do not rediscover or
  re-ask on later phases without a change in capability.
- Ask for confirmation before creating or changing tickets, pull requests,
  remote branches, or other external state. Local inspection, drafting, and
  reversible plan-document edits are in scope.
- Every acceptance criterion must be measurable. Capture its baseline and
  exact measurement method before changing code. An all-of-set criterion is
  not complete while any contributing unit remains deferred or unexecuted.
- Every work unit must have a scope, explicit done criteria, dependency set,
  story-point estimate, owner branch/worktree, and state. Never dispatch an
  unsized unit.
- A gate that is proven red on the unchanged base ref is a **known baseline
  exception**, not a green result. It may be carried only when its exact
  signature is recorded, no new findings are introduced, the affected
  acceptance criterion is explicitly written as a no-regression criterion,
  and the user accepts the remaining risk before rollout. Otherwise, it is a
  blocking remediation unit.
- Before a parallel wave, freeze an integration baseline: all predecessor code
  that the wave needs is committed and the integration checkout is clean apart
  from deliberately excluded user changes. Do not fan out from an uncommitted
  integration state. Serialize that predecessor or make and validate its
  commit first, then create every worker worktree from the same recorded ref.
- When execution exposes a reusable operational fact—such as a consumer
  compatibility boundary, test-runner constraint, worktree hazard, or proven
  flake protocol—record it immediately in the living plan's **Execution
  lessons** section. Include the evidence/trigger, the required practice, the
  scope it applies to, and whether it is provisional or proven. Apply active
  lessons to all later units; do not promote a hunch into a rule without
  evidence.

## Codex collaboration and isolation

Use Codex's native collaboration capability when it is available. Before
planning each wave, identify the independent code-changing units and available
worker capacity. When at least two such units are eligible, dispatch as many as
capacity permits in separate worktrees. Serialize a wave only when it has an
explicit recorded reason: a real dependency or shared mutable state, constrained
test resources, unavailable capacity, or a user request. An integration
worktree is the convergence point, not a reason to serialize independent work.
If collaboration is unavailable, run the wave serially and record that fact.

For parallel code-changing units, create one Git worktree and branch per unit
from the integration branch before dispatch. Give each worker its exact
worktree path and require it to work only there. Codex workers share the parent
workspace by default, so never dispatch concurrent writers in the same checkout
or branch.

```sh
git worktree add ../wt-<unit-id> -b update/<slug>-<unit-id> update/<slug>
```

Each executable worktree needs its own real, lockfile-respecting dependency
install. Never symlink `node_modules`, package-store links, generated output,
or mutable caches between concurrent worktrees unless the package manager and
the project explicitly support that arrangement. Record the install command
and any shared read-only cache in the plan.

Use a detached worktree for a read-only verifier when isolation is needed:

```sh
git worktree add --detach ../wt-verify-<unit-id> <ref>
```

Dispatch every eligible independent unit up to the current collaboration
concurrency limit. Give each worker a fresh,
self-contained brief rather than a long inherited transcript. When the user
asks for model accounting, explicitly request an available model at dispatch
and record it as the **requested model**; record an **actual model** only when
the platform returns it. Suggested Codex tiers, when available:
`gpt-5.6-luna` for mechanical measurement and gate-running, `gpt-5.6-terra`
for bounded implementation, and `gpt-5.6-sol` for ambiguous architectural or
root-cause work. Otherwise use the closest available fast, standard, or
high-reasoning option. Never infer model, token, or tool-use telemetry from a
worker's result or from the request.

Use `gpt-5.6-luna` as the default for routine verifiers: full-suite gates,
focused test runs, inventory checks, and other deterministic evidence gathering.
Escalate a verifier to `gpt-5.6-terra` when it must diagnose an environmental
failure, test-order issue, or unclear result. Reserve `gpt-5.6-sol` (or the
strongest available equivalent) for ambiguous behavioral debugging and complex
remediation. If a selected model reports capacity exhaustion, retry the unit
with a different available model before changing its scope or declaring it
blocked; preserve the failed dispatch and fallback model in the usage record.
The model tier changes orchestration reliability and diagnosis quality, not the
test command's runtime, so keep the verification command and evidence criteria
unchanged during a model fallback.

Keep available worker capacity productively occupied during verification: while
a dependent-suite verifier runs, dispatch independent source-conversion or
diagnostic units from the same committed baseline into separate worktrees. Do
not wait for a verifier merely because it is running. Respect dependency order,
browser/CPU/disk capacity, and the rule that no unit integrates until its
predecessor's canonical gate is green; if resources become constrained, reduce
test concurrency before reducing independent source throughput.

Use event-driven worker monitoring for an active update. Keep the orchestration
turn alive with the collaboration wait mechanism rather than relying on the
user to prompt progress or polling agent lists on a fixed interval. When a
worker completion, failure, interruption, or capacity error arrives: reconcile
its result against the exact plan unit and commit, record evidence and lessons,
integrate only when predecessor gates permit, and immediately refill any newly
available slot with the next independent unit. After each transition, re-check
the live board and continue waiting while runnable work remains. Stop the
monitor only at a real lifecycle boundary (for example, all planned work is
blocked pending user direction, or the update reaches Verify/Roll out).

For a worker brief, include only:

1. Unit ID, worktree path, branch, and exclusively owned files.
2. Done criteria and the acceptance criteria it satisfies.
3. Exact test, formatter, lint, and build commands discovered in Assess.
4. Test-first requirement and the hard gate rules below.
5. Required completion report: changed files, test evidence, each gate result,
   commit, requested model, actual model/usage if reported, and unresolved
   cross-cutting issues.

Hard gate rules: write the failing test **or** establish an executable
target-state assertion first; do not touch another unit's files; do not commit
on red except for a documented known baseline exception; prove any claim that
a failure predates the unit; never remove tests, relax checks, or add a
band-aid merely to reach green. Target-state assertions are appropriate for
mechanical migrations when a behavioral test would not exercise the change
(for example, source inventory, compiler, emitted-entrypoint, or declaration
checks).

For long-running commands, use Codex's tracked command/session execution
directly. Do not use `nohup`, `disown`, or an untracked shell detach; wait for
the tracked process to finish before grading it.

## Reused Skills (discover-then-fallback)

**All of these skills are optional**; the orchestrator runs with none of them
present. Inspect the active Codex session's available skills and chain to a
matching skill when one is available. Otherwise use the bundled procedure or
the Codex capability described above. Match by capability, not by an assumed
exact name:

- Planning → **superpowers:writing-plans**
- Parallel dispatch → **superpowers:dispatching-parallel-agents** or Codex
  native collaboration
- Worktree isolation → **superpowers:using-git-worktrees**
- TDD → **superpowers:test-driven-development**
- Skill authoring for skill gaps → **superpowers:writing-skills**
- Whole-change verification → **superpowers:verification-before-completion**
- Code review → **superpowers:requesting-code-review** or an available
  session code-review skill/agent
- Diagnosis → **superpowers:systematic-debugging**
- Guided design → **mattpocock-skills:grilling** to grill against project
  evidence and record the decisions in the design artifact; if unavailable,
  use **superpowers:brainstorming**; if neither skill is available, use the
  bundled Guided design reference

See `references/skill-discovery.md` for the phase-entry skill table, capability
discovery, and bundled fallbacks.

## 1. Assess

Load `references/assess.md`. Inspect the codebase, CI configuration, package
topology, Git state, test/build/lint/format commands, and available tracker or
review tooling. Use `references/tracking-integration.md` when a tracker exists.

Produce findings that include:

- In-scope and explicitly out-of-scope surfaces, dependency map, and blast
  radius.
- Measurable acceptance criteria, each with a baseline or `Not captured`,
  exact measurement method, and units that will satisfy it.
- Exact CI-equivalent test, format, lint, and build commands; baseline result
  for each, including proven environmental failures.
- A test-execution manifest: every required suite or named segment, its owning
  package/worktree, its exact command, expected count or completion signal,
  and whether it may run concurrently. For browser/server-backed tests, first
  measure and record the host's maximum stable parallelism. Automatic port
  selection prevents port collisions; it does not prove the host, browser, or
  cache is safe at arbitrary concurrency.
- An early downstream-consumer compile or smoke gate for each changed public
  template/module surface. Package-local typecheck and build results alone do
  not prove that a classic or otherwise different consumer can resolve the
  changed imports, helpers, modifiers, or generated module format.
- Tracking ticket reference or an explicit ticketless decision; never invent a
  ticket. If neither tracker nor remote repository tooling was discovered,
  record the one-time user prompt and response described above.

Do not advance until criteria, baselines, toolchain, and Git state are known or
explicitly recorded as unavailable.

## 2. Plan

Load `references/plan.md`. Facilitate a guided design with
`references/guided-design.md` if architecture is not already approved. Write a
Design artifact using `references/design-artifact-template.md`, then a living
plan at `docs/<slug>-plan.md` using `references/living-plan-template.md`.

Plan ordered waves. Units in a wave must have no file, migration-order, or
shared-resource conflict. Encode dependencies between waves explicitly. Each
unit must map to criteria and include a realistic point estimate; record the
team velocity used for a forecast.

Before presenting the plan for approval, obtain an independent review of the
draft decomposition using `references/plan-review.md`. Resolve its findings
(including re-waving, re-sizing, or repairing criterion coverage) before
Execute; this is a gate, not advisory feedback.

For every missing capability a unit needs, decide with the user whether to do
the work inline for this update or create a reusable skill. Record the decision
and its rationale in the living plan's **Skill-gap decisions** table. A missing
skill never blocks the plan by itself, but an undecided gap may not be silently
carried into Execute.

If execution reveals substantial work outside the planned units (for example,
temporary migration suppressions that need type hardening), pause that work,
add bounded and sized units with criteria coverage to a later wave, and update
the plan before dispatching it. Do not hide scope expansion inside a completed
unit.

For every unit, define a fast gate (unit/package check), an integration smoke
gate, and the required full regression gate before implementation. If the full
gate is split into segments, preserve an exhaustive manifest and validate that
the runner reports no omitted or unmatched tests. A change to the command,
parallelism, filtering, or environment ends the previous attempt: record it as
`Abandoned` or `Incomplete`, with its evidence, rather than combining partial
green outputs into a passing gate.

Preview the Design artifact, work-unit table, point estimates, expected wave
parallelism, and any external ticket writes. Get approval before committing to
external systems or starting implementation.

## 3. Execute

Load `references/execute.md`. For each wave:

**Wave scheduling invariant:** a failed unit creates a distinct, sized
remediation unit in Wave N+1 with state `Todo`. Do not dispatch or mark that
remediation `In Progress` while Wave N is still executing. Continue only the
already-planned, independent healthy siblings in Wave N; the remediation is
the first eligible work for Wave N+1 after Wave N converges. The failed unit
and its criteria remain pending until the remediation verifies green.

1. Move selected units to In Progress in the living plan and append a
   timestamped transition. Update a matched ticket only after confirmation.
2. Confirm the recorded wave-dispatch decision, create the worktrees, and
   dispatch every eligible independent unit up to capacity. Continue siblings
   if one worker fails.
3. Integrate clean worker commits one at a time into `update/<slug>`. Resolve
   conflicts in the integration worktree; do not hide them in a worker branch.
4. Independently verify every integrated unit. A worker's green report is a
   claim, not a result. Use a separate read-only Codex worker, or a clean
   integration checkout if none is available, to re-run the fast and consumer
   smoke gates plus the required full regression manifest. One independent
   clean full-gate pass is the default; repeat the affected gate when it is
   flaky, when a criterion requires a repeated measurement, or when the
   project policy requires it. Record each attempt and do not call a partial
   segmented run green.
5. Mark independently verified units Done. On failure, append a **Todo**
   remediation unit to the next wave and preserve the failed unit's pending
   status; never pull remediation forward into the active wave. Healthy,
   pre-planned siblings continue. Update the plan's next steps, execution
   lessons, and Last updated timestamp.

Retire worktrees as part of every wave closeout; do not let completed verifier
checkouts accumulate. Classify each worktree before deleting it:

- An active worker, an uncommitted implementation, a pipeline commit awaiting
  integration, or an untracked evidence/artifact directory is **retain**.
- A read-only verifier with no source changes is removable once its result is
  recorded in the plan and durable evidence is retained outside the worktree.
- A code-changing worktree is removable only after its commit is integrated
  and independently verified on the integration ref.

Before cleanup, inventory only worktrees owned by the update; check their exact
paths, `git status --short`, HEAD, branch/detached state, and whether evidence
is stored solely inside the directory. Never remove a dirty or untracked-
artifact worktree merely to make the list shorter. Obtain user confirmation for
the exact removal set unless it was already authorized in the plan or request.
Use `git worktree remove <exact-path>` (not broad filesystem deletion), run
`git worktree prune`, and confirm the removed paths no longer appear in
`git worktree list`. Record the unit, paths, evidence location, and result in
the transition log. Do not delete local branches unless that is separately in
scope.

## 4. Verify

Load `references/verify.md`. Verify the fully integrated branch, not individual
worktrees:

- Grade every acceptance criterion against its recorded baseline and report
  before/after values.
- Run the CI-equivalent composite gate, formatter check, lint, and build.
- Run the project's end-to-end/regression suite, including a clean dependency
  resolve for dependency upgrades when practical, or record a `post-mr`
  deferral when the suite can run only after an MR/PR exists. See
  `references/verify.md`.
- Request or perform an independent code review of the integrated diff.

Any red criterion, flaky verifier run, or blocking review issue creates a
remediation wave and returns to Execute. Verify again after the final rebase
onto the intended target branch and before remote rollout. Never proceed to
Roll out on red, except for a documented, user-accepted known baseline
exception that does not violate a no-regression criterion. A recorded
`post-mr` E2E deferral is the sole exception: Roll out owns running and grading
that suite after the MR/PR exists; it cannot close out while that gate is
pending or red.

When a test fails, preserve the exact failure, environment, command, and
attempt. Compare it against the recorded base/integration baseline or a
targeted unchanged reproduction before calling it environmental. A changed
failure signature, an unproven baseline, or an exhausted retry budget is a
blocking remediation unit—not an "unrelated flake." Keep healthy siblings
moving, but leave the affected acceptance criterion pending.

## 5. Roll out

Load `references/roll-out.md`. Prepare and create or hand off the PR/MR using
the documented delivery procedure, including the single-versus-separate and
stacked-PR decisions. If Verify recorded a `post-mr` E2E deferral, trigger and
wait for that pipeline after the MR/PR is created before closeout. Offer to
work review feedback only after the MR/PR is open; use its documented triage
and confirmation rules. Preview external writes and obtain confirmation before
creating them. A direct user instruction to create a named ticket, branch, or
PR/MR is confirmation; state the intended payload concisely in commentary
before executing rather than asking a redundant question. Transition tickets
only after re-querying to verify their new state.

Finalize the living plan with outcomes, links, post-rebase gate evidence,
known baseline exceptions, follow-ups, remote ticket/MR links and status, and
the recorded worker usage summary. Separate requested model from actual
reported model, and state which usage data was not reported rather than
estimating it.

## Read-only reports

At any phase, a request for a **burndown** or **usage report** is read-only: do
not alter phase, ticket, plan, or code state. Load `references/reporting.md`.
For a burndown, read both active and archived transition entries, plot remaining
sized points over time, and clearly distinguish deferred or unsized work. For a
usage report, aggregate only worker-provided model, token, and tool-use figures;
show `Not reported` for unavailable values.
