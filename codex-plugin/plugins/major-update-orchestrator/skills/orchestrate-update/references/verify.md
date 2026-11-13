# Verify

Verify the converged integration branch in a clean enough environment to expose
cache-masked failures. Re-grade every criterion using its baseline method,
execute the full CI-equivalent gates, and review the integrated diff. Re-run
the affected verification gates after the final rebase onto the intended target
branch and before remote rollout. Report the exact evidence, not a generic
green claim.

Any failed criterion, gate, or blocking review finding creates a new remediation
unit and returns the lifecycle to Execute. A known baseline exception may be
carried only when it is reproduced on the unchanged base ref, its signatures
and count are unchanged, no new findings were introduced, and the user accepts
the remaining risk. It is reported as an exception, never as a green gate. Do
not roll out a partially verified change.

Use the recorded manifest to prove full coverage. A collection of individually
green segments is not a full-gate pass unless each required segment has an
expected completion signal and the runner reports no missed or unmatched tests.
If a run was interrupted or the command/environment materially changed, record
it as INCOMPLETE or ABANDONED and grade only a later complete attempt.

## Deterministic comparison and output normalization

Before comparing repeated measurements or a result with its baseline, identify
volatile output that would create a false difference: timestamps, generated
paths, random IDs, unordered records, platform-specific line endings, and
similar noise. Record a narrow, repeatable normalization rule in the living
plan—such as sorting a report, masking a known timestamp field, or using a
stable output format—and apply the same rule to baseline and post-change data.
Never normalize failures, counts, error classes, or substantive output merely
to produce a match. If meaningful output cannot be separated from volatility,
record the comparison as inconclusive and create a remediation or user-handoff
instead of declaring it green.

For any failed gate, keep the first failure's command, environment, and
signature. Compare it with a baseline or unchanged reproduction before
classifying it environmental. If that comparison is unavailable, the failure
remains a blocking remediation item; do not dismiss it as unrelated merely
because other worktrees pass.

## End-to-end regression suite (discover-then-fallback)

Run this gate once against the converged integration branch, not once per work
unit. It is distinct from Execute's per-unit regression manifest even when the
command is the same.

1. **Discover, in order:** (1) a session skill or MCP that can run the suite
   (for example, a Playwright runner or CI-regression entry point), then (2) an
   **in-repo invocation script**: a `package.json` script such as `test:e2e` or
   `e2e`, `playwright.config.*`, a Makefile target, or a CI job definition that
   runs from the checkout. Use the first suitable capability found to start the
   suite and collect its results.
2. **Classify the suite's execution mode before running it:**
   - `local`: it runs against the checkout as-is.
   - `remote-branch`: it needs a deployed preview, but one is published from a
     pushed branch without requiring an MR/PR.
   - `post-mr`: the required deployment or pipeline is triggered only when an
     MR/PR exists.

   Infer the mode from the script or CI configuration when possible; for
   example, a deploy URL versus an MR-number input. Ask the user only when the
   available evidence cannot determine it.
3. For `local` or `remote-branch`, run the suite now and apply the normal gate
   rules above. For `post-mr`, **do not run it in Verify**. Record a `post-mr`
   E2E deferral in the living plan's **Deferred inputs** table, including the
   capability, reason, and next step: “run in Roll out after MR/PR creation.”
   Mark the E2E criterion as satisfied-pending-Roll-out rather than failing
   Verify; `roll-out.md` owns its eventual execution and grading.
4. If no capability can execute the suite, hand off to the user to run it and
   report the result. Record the resulting coverage gap and do not call the
   gate green without that evidence.

For dependency or upgrade work, perform a clean dependency re-resolve where
practical and confirm the lockfile remains stable. Record the command, target
ref, execution mode, complete result, and any baseline comparison in the
living plan.
