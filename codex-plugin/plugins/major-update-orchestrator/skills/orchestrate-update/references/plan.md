# Plan

The Design artifact owns architecture: goals, context, alternatives, decision,
risks, and rollback. The living plan owns delivery: criteria, baselines, waves,
work-unit state, estimates, transitions, and next steps.

Order units by real dependencies. For each wave, record its independent eligible
units, available worker capacity, planned dispatch count, and any serialization
reason. When collaboration is available, dispatch every eligible independent
code-changing unit up to capacity in its own worktree/branch. Serialization
requires a real dependency or shared mutable state, constrained test resources,
unavailable capacity, or a user request; the integration worktree itself is not
a reason. Get user approval for the design and wave plan before implementation
begins.

When execution reveals follow-on work outside the existing unit table, add it
as a bounded, sized remediation or hardening unit in a later wave before
dispatch. Update its acceptance-criterion coverage and transitions; do not
retrofit new scope into a unit already marked Done.

Freeze a clean, committed integration ref before creating worktrees for a
parallel wave. A worker must be able to reproduce its starting state from that
ref; a prior unit that is still uncommitted belongs in a serialized predecessor
wave. Give each executable worktree a real dependency installation—never a
symlinked `node_modules` tree unless the project has documented that it is
safe.

Attach a gate manifest to each unit: fast/package, consumer-smoke, and full
regression commands, plus expected coverage. If the full regression is divided
into named segments, assign every segment exactly once and retain the runner's
unmatched/missed-test output as part of the evidence. Record a global test
concurrency limit based on an Assess capacity probe, even if individual test
commands select free ports automatically.

If model accounting is requested, put the requested model in the unit row and
the worker brief. Treat platform-reported actual model, tokens, and tool uses
as separate optional fields; absence is `Not reported`, never an estimate.

## Independent plan review

Before Execute, dispatch a read-only, independent reviewer using
`plan-review.md`. Give it the Assess findings, approved Design artifact, and
draft living-plan sections—not the integrator's reasoning transcript. It must
check for missing criterion coverage, unsafe same-wave overlap, unbounded or
unsized work, unproven assumptions, incomplete gate manifests, and ticket or
rollout dependencies that would block delivery later. Resolve every finding in
the plan before asking the user to approve the waves.

## Skill-gap decisions

For each unit that requires a capability unavailable in the current session,
offer two explicit choices: handle it inline for this update or author a
reusable skill. Record the chosen option, rationale, owner, and next step in
the living plan. If the user selects skill authoring, keep that work bounded
and sized as a separate unit; do not hide it inside the implementation unit
that needs the capability.

## Ticket mapping and transitions

Map every work unit to an existing ticket or an explicit ticketless marker.
When a tracker is in use, adopt a ticket's existing estimate or propose writing
the unit's estimate back after confirmation. A remediation unit inherits its
parent's ticket unless the plan explicitly assigns another one. Resolve the
tracker's actual transition path during Plan, including any required multi-hop
states, and record it in the living plan before the first ticket update.

Define each wave's exit condition. A failed unit does not halt independent
siblings in its current wave, but its remediation is a new, sized **Todo**
unit in the next wave—not concurrent work in the current one. Preserve the
failed unit and its criteria as pending. Do not mark or dispatch a Wave N+1
remediation In Progress until Wave N has converged; record this dependency in
the work-unit table.
