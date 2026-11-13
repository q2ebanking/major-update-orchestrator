# Execute

Use worktrees for concurrent writers and integrate commits into the integration
branch one at a time. Each worker begins with a failing behavioral test or an
executable target-state assertion, runs the exact discovered gates, and commits
only when all gates are green or a recorded known baseline exception applies.
Use target-state assertions for mechanical work where a new behavioral test
would not be meaningful, such as zero legacy source files, compiler success,
or emitted public-entrypoint checks.

Before starting a wave, reconcile its recorded dispatch decision with live
capacity. Dispatch every eligible independent code-changing unit up to that
capacity. If the planned dispatch count is reduced or the wave is serialized,
record the concrete dependency, shared mutable state, test-resource limit,
capacity limit, or user request that caused it; do not cite the integration
worktree as the reason.

When a unit fails, immediately record its exact evidence and create a separate,
sized remediation unit in the **next** wave with state `Todo`. Keep the failed
unit and its criteria pending. Continue only independent siblings already
planned in the current wave; do not dispatch, mark In Progress, or fold the
remediation into that wave. The next wave begins only after the current wave's
healthy units have converged and its exit condition is recorded.

Create all worker worktrees from the same clean, committed integration ref and
give each one an independent dependency install. Do not start a parallel wave
from uncommitted predecessor code, and do not share mutable dependency trees or
generated output between workers. Record the tested commit for every result.

Run the planned fast gate immediately after the change, then the downstream
consumer smoke gate before spending time on the full suite. Strict-template
imports and package-local builds are insufficient evidence of compatibility
with every consumer. When a shim or adapter is needed, verify its calling
contract against the original implementation and add focused coverage.

Run each full-regression manifest entry exactly as assigned. An interrupted
command, a changed filter, a changed parallelism level, or a switch to another
worktree is an `Incomplete`/`Abandoned` attempt, not evidence that can be
combined with a later run. On a failure, preserve the command and signature;
prove it on the baseline or unchanged target before labelling it environmental.

Never trust a self-report alone. A distinct verifier re-runs the integrated
unit's fast and consumer gates plus its complete regression manifest, returning
a compact PASS, FAIL, FLAKY, or INCOMPLETE verdict with commands and attempt
counts. Repeat only the affected gate when it flakes, the criterion requires
repeated measurements, or project policy says so. Preserve failed units as
remediation work instead of abandoning or silently expanding a sibling's scope.

At wave closeout, retire eligible update-owned worktrees. First inventory each
path, status, HEAD, branch/detached state, and evidence location. Remove a
read-only verifier only after its evidence is in the plan and outside the
worktree; remove a code worker only after integration and independent
verification. Retain active, dirty, pipeline, and artifact-bearing worktrees.
With the user's confirmed exact scope, use `git worktree remove <path>`, then
`git worktree prune` and `git worktree list` to confirm removal. Record the
cleanup outcome; do not delete branches as part of worktree retirement unless
explicitly requested.
