# Assess

Inspect before planning. Map package/module boundaries, public APIs, generated
artifacts, CI workflow, lockfiles, test types, and the current Git state.

Define acceptance criteria as predicates that can be evaluated at Verify. For a
comparative target, record the before value, command, environment, sample size,
and normalization method. Re-run a test/build baseline once to detect flakes.
Record a failure as environmental only with evidence from the base branch or a
reproducible environment difference.

Before planning a parallel test wave, build a test-execution manifest. Include
every required suite or named segment, its command, expected test count or
completion signal, worktree, and concurrency eligibility. For test runners
that start browsers, servers, or other scarce host resources, run a small
capacity probe and record the maximum stable concurrency. Dynamic/zero ports
remove one collision class but do not make the runner or host infinitely
parallel-safe.

For a public template/module migration, discover the most representative
downstream consumer and run a compile or smoke baseline there. In particular,
record any module-resolution, strict-template-scope, helper, modifier, or
transpilation differences that package-local checks cannot see.

Discover ticket tracker, source-repository remote API/CLI, PR/MR, and review
capabilities before depending on them. Perform a read-only health check for
each discovered connector. If no usable ticket tracker exists, ask once whether
to use a ticketing technology or proceed ticketless. If no usable remote
repository API/CLI exists, ask once which remote system and API/CLI should own
branch and PR/MR operations. Record the answers, including an explicit
deferral, in the living plan.

Inspect repository policy before the first commit or push: commit-message and
branch-name hooks, contribution instructions, target branch, MR template,
required checks, and merge requirements. Use the discovered convention in the
first local commit rather than learning it from a rejected push.

For a red baseline, preserve the exact command, ref, finding signatures, and
count. A later result is a known baseline exception only if the same signatures
are reproduced on the unchanged base ref and the change adds none. Phrase the
criterion as "no new findings" rather than calling the full gate green.
