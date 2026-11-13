# <Update name> — Living Plan

## Lifecycle

- Phase: Assess | Plan | Execute | Verify | Roll out
- Last updated: <ISO-8601 timestamp>
- Design artifact: <repository-relative path>
- Integration branch: `update/<slug>`
- Tracker / remote repository: <verified technology/API or ticketless / Not provided>
- Next step: <one concrete action>

## Acceptance criteria and baselines

| ID | Criterion | Baseline and method | Target | Supporting units | Verdict |
|---|---|---|---|---|---|
| AC-1 | <measurable condition> | <before value; exact command> | <target> | <unit IDs> | Pending |

## Waves and work units

| Wave | Unit | Scope | Depends on | Isolation / base ref | Requested model | Points | State | Criteria |
|---|---|---|---|---|---|---:|---|---|
| 1 | U1 | <exclusive paths> | — | worktree / `<commit>` | <model or Not requested> | 3 | Todo | AC-1 |

_Wave scheduling rule: a failure creates a distinct, sized `Todo` remediation
unit in the following wave. It cannot be dispatched or moved to `In Progress`
until the current wave's healthy siblings have converged. The failed unit stays
pending; its criteria do not transfer to the remediation implicitly._

## Wave dispatch decisions

_Make the parallelism decision explicit before each wave. An integration
worktree is the convergence point, not a serialization reason._

| Wave | Independent eligible units | Available worker capacity | Planned dispatches | Serialization / reduction reason | Evidence |
|---|---|---:|---:|---|---|
| 1 | U1, U2 | <N> | <N> | <Not applicable, or concrete reason> | <capacity check / dependency> |

## Toolchain and known failures

- CI-equivalent test command: <command or Not provided>
- Formatter check: <command or Not provided>
- Lint command: <command or Not provided>
- Build command: <command or Not provided>
- Known environmental failures: <evidence-backed list or None>
- Known baseline exceptions: <exact base-ref signature, user acceptance, or None>

## Test-execution manifest

_The manifest is authoritative for required coverage. A port chosen
automatically makes a command independently addressable; it does not waive the
global host-concurrency limit discovered in Assess._

- Global stable test concurrency: <N / probe command / Not captured>

| Gate | Unit / worktree | Exact command | Expected count or completion signal | Concurrency eligible | Attempts / verdict |
|---|---|---|---|---|---|
| Fast package gate | U1 | <command> | <signal> | Yes | Pending |
| Consumer smoke | U1 | <command> | <signal> | Yes | Pending |
| Full regression segment | U1 | <command> | <signal> | No | Pending |

_Record interrupted, altered, or partial runs as `Incomplete`/`Abandoned`; do
not aggregate them into a pass. For a segmented full gate, retain the runner's
missed/unmatched-test output with the results._

## Execution lessons

_Capture reusable facts learned while executing this update. These are
operational rules for later units—not a narrative log. Add a lesson as soon as
evidence reveals it, and read active lessons on resume. Mark a lesson
`Provisional` until it has a reproducible trigger or independent confirmation;
do not turn a hunch into mandatory process._

| Timestamp | Trigger / evidence | Required practice | Applies to | Status |
|---|---|---|---|---|
| <ISO-8601 timestamp> | <observed failure or measurement> | <specific repeatable action> | <units / gate / environment> | Provisional \| Proven \| Retired |

## Deferred inputs

_Before doing unrelated work, record every user-provided fact whose action is
being intentionally deferred. Preserve its exact value so a later session does
not need to infer or ask for it again. Resolve or explicitly waive each row
before closeout._

| Timestamp | Input / exact value | Deferred action | Reason | Owner | Next step | State |
|---|---|---|---|---|---|---|
| <ISO-8601 timestamp> | <e.g. Initiative `UUX-123`> | Create Epic and parent it to the Initiative | <why it is not being done now> | Integrator | <concrete action> | Pending |

## Decisions

| Timestamp | Decision | Rationale |
|---|---|---|

## Skill-gap decisions

| Unit / capability | Chosen path | Rationale | Owner | Next step | State |
|---|---|---|---|---|---|
| <U1 / capability> | Inline \| Author reusable skill \| Handoff | <why> | Integrator | <concrete action> | Pending |

## Tracker transition map

| Orchestrator state | Tracker state / transition | Required intermediate states or fields | Verified |
|---|---|---|---|
| Todo → In Progress | <actual transition ID/name> | <none or ordered hops> | Pending |

## Rollout outcome

| Item | Result |
|---|---|
| Final target ref | <target branch and commit> |
| Post-rebase verification | <commands and outcomes> |
| Ticket | <URL/status or Not used> |
| PR/MR | <URL/status or Not created> |
| Remaining risk / follow-up | <item or None> |

## Transition log

| Timestamp | Unit | From | To | Evidence |
|---|---|---|---|---|

## Worktree retirement log

_Retain active, dirty, pipeline, and artifact-bearing worktrees. A read-only
verifier may retire after its evidence is recorded outside the worktree; a code
worker may retire only after integration and independent verification. Record
the user's cleanup authorization and do not delete branches unless separately
approved._

| Timestamp | Worktree / unit | Eligibility evidence | User authorization | Removal result |
|---|---|---|---|---|
| <ISO-8601 timestamp> | `<path>` / U1 | <clean verifier; evidence path> | <request/plan reference> | Removed / Retained |

## Worker usage rollup

| Worker / unit | Requested model | Actual reported model | Dispatches | Tokens | Tool uses |
|---|---|---|---:|---:|---:|
| U1 | <model or Not requested> | Not reported | 1 | Not reported | Not reported |

_Requested model records dispatch intent only. Do not identify it as actual
execution telemetry unless the platform reports that value._
