# Living Plan Doc Template

Authoritative for **how / sequencing / progress**. Created in Plan 2b. **Read first each session**;
hydrate the todo list from it; write progress back. Cross-linked with the Design artifact; it does
**not** redefine the design's facts (authority boundary).

Copy the block below into `docs/<slug>-plan.md` and keep it current as the single source of truth.

```markdown
# <Update name> — Living Plan

## Lifecycle header
- **Current phase:** Assess | Plan | Execute | Verify | Roll out
- **Parent ticket:** <ref/URL or "None">
- **Design artifact:** <link>
- **Velocity:** <N points / two weeks, or "Not provided">
- **Started:** <YYYY-MM-DD>  ·  **Last updated:** <YYYY-MM-DDThh:mm>

## Acceptance criteria (from Assess)
| # | Criterion | Kind | Target/threshold | Baseline (before) | Satisfied by (units) | Measurement method | Latest measurement (after) | Verify result |
|---|---|---|---|---|---|---|---|---|
| 1 | <e.g. p95 login < 800ms> | comparative | << 800ms> | <920ms> | <A, D> | <cmd, env, N runs> | <TBD> | <TBD> |
| 2 | <all packages on Ember 6.12> | absolute | n/a | n/a | <A, B, C, D, E, F> | presence check | <TBD> | <TBD> |

_"Latest measurement (after)" is updated in place as Verify re-runs, so a fail → remediation →
re-verify loop doesn't re-run expensive baselines from zero._

_An absolute "all-of-set" criterion stays **Blocked** while any unit in "Satisfied by" is deferred,
`Unsized`, or unexecuted. Comparative criteria require a numeric target/threshold, not a direction._

## Waves & work units
### Wave 1
| Unit | Scope (paths) | Deps | Isolation | Size (pts) | Ticket | State | Done-criteria |
|---|---|---|---|---|---|---|---|
| A | <paths> | — | worktree | 3 | <ref> | Done | <criteria> |
| B | <paths> | — | worktree | 5 | <ref> | In Progress | <criteria> |

### Wave 2
| Unit | Scope (paths) | Deps | Isolation | Size (pts) | Ticket | State | Done-criteria |
|---|---|---|---|---|---|---|---|
| E | <paths> | B | worktree | 3 | <ref> | Todo | <criteria> |

_Unit `State` is one of: Todo · In Progress · Done · Failed · Blocked · Deferred._

_Unsized / deferred units (called out so they don't distort the burn-down):_ <none | list>

## Transition log (append-only — data source for the burn-down)
<!-- Resume/rehydration: SKIP this section. It is append-only burn-down data, not actionable state —
rebuild the todo list from the Waves tables, not from here. Keep it out of context on resume. -->
_Keep this lean. When it grows large (e.g. > ~50 rows), **archive** rows for units that reached Done
more than a wave ago into "Archived transitions" below — the burn-down reads active + archived
together, but the active table stays cheap to load on every resume._
| Timestamp | Unit | Ticket | From → To |
|---|---|---|---|
| 2026-08-14T09:00 | A | <ref> | Todo → In Progress |
| 2026-08-14T16:20 | A | <ref> | In Progress → Done |

<details><summary>Archived transitions (closed waves — burn-down data only, skip on resume)</summary>

| Timestamp | Unit | Ticket | From → To |
|---|---|---|---|
| <moved here once the unit's wave has converged and Verify has moved on> | | | |

</details>

## Model & token usage (rollup)
<!-- Resume/rehydration: SKIP this section. It is read-only budget accounting, not actionable state.
Updated IN PLACE (not append-only) as subagents complete, so it stays a few rows — see usage-report.md. -->
_Subagent accounting, updated in place at each convergence. Integrator's own tokens are excluded (not
self-observable in-session)._
| Model  | Dispatches | Tokens | Tool uses |
|--------|-----------|--------|-----------|
| haiku  | 0 | 0 | 0 |
| sonnet | 0 | 0 | 0 |
| opus   | 0 | 0 | 0 |
| **Total** | 0 | 0 | 0 |
_Unreported-token dispatches: 0 (tool_uses counted; tokens excluded from the token sum)._

## Known environmental failures (non-blocking)
_Tests/checks that fail in one environment but pass in the target; Verify annotates but does not
block on these (see `verify.md` §4). New env-only failures are added here once, not re-litigated._
| Test/check | Reason | Fails in | Passes in | Verified non-blocking (who/date) | Added |
|---|---|---|---|---|---|
| <e.g. acceptance/foo> | <CDN 403, offline-only> | <local offline> | <CI> | <reviewer, YYYY-MM-DD> | <YYYY-MM-DD> |

## Tracker transition map (resolved once, reused)
_Role → tracker transition, discovered per project/issue-type (see `tracking-integration.md`). Avoids
re-discovering hidden/validator-gated transitions each session._
| Role | Transition (id / name) | Required fields | Notes |
|---|---|---|---|
| to-in-progress | <id / name or "none available"> | <fields> | <e.g. blocked by screen validator> |
| to-done | <id / name> | <e.g. resolution=Done> | |
| to-rolled-out | <id / name> | <fields> | |

## Determinism / output normalization
_Mask applied to volatile output before diffing runs or baselines (see `verify.md` §4)._
- <e.g. `sed -E 's/ - \[[0-9]+ ms\] - / - /'` to strip timing prefixes>

## Deferred inputs
_Before doing unrelated work, record every user-provided fact whose action is intentionally deferred.
Preserve its exact value so a later session does not need to infer or ask for it again. Resolve or
explicitly waive each row before closeout._
| Timestamp | Input / exact value | Deferred action | Reason | Owner | Next step | State |
|---|---|---|---|---|---|---|
| <YYYY-MM-DDThh:mm> | <e.g. Initiative `UUX-123`> | Create Epic and parent it to the Initiative | <why it is not being done now> | Integrator | <concrete action> | Pending |

## Decisions log
<!-- Resume/rehydration: read only a decision the current Next step explicitly references; the rest is
historical context. Keep this lean the same way the transition log is: when it grows large (e.g. >
~20 entries), move decisions that are settled and no longer inform current work into "Archived
decisions" below. "Active" = still shapes current work (open trade-offs, revised criteria/baselines
with a `revised from` note); "archived" = closed rationale, kept for audit only. Default each entry to
a brief summary + rationale (2-3 lines); move lengthy root-cause narrative or investigation detail to
a linked ticket comment or appendix instead of inlining it. -->
- <YYYY-MM-DD> <decision and rationale>

<details><summary>Archived decisions (settled — audit context only, skip on resume)</summary>

- <YYYY-MM-DD> <moved here once the decision no longer informs current work>

</details>

## Skill-gap log
<!-- Also append-only; skip on resume unless a gap is carried in Next steps. Archive resolved rows
(Status = done) into a collapsed block if this grows past ~20 entries, same as above. -->
| Unit | Capability needed | Matching skill? | Decision (inline / author) | Status |
|---|---|---|---|---|
| B | <capability> | none | author (superpowers:writing-skills) | pending |

## Next steps
- <what happens next; carried failures / remediation units>
```
