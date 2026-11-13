# Independent plan review

Review the proposed Design artifact and living plan as a read-only worker with
no implementation stake. Return `CLEAN` only when the plan can enter Execute
without an unbounded, unsafe, or unverified unit.

Check that every acceptance criterion maps to one or more sized units; every
wave is free of file, dependency, and shared-resource conflicts; and every
unit has an exclusive scope, done criteria, base ref, test manifest, and
realistic estimate. Check that downstream-consumer, E2E, rollout, ticket, and
skill-gap requirements are either planned or explicitly deferred with an owner
and next step.

Report findings as `blocking` or `non-blocking`, citing the affected plan
section and a concrete correction. The integrator resolves every blocking
finding before user approval and records non-blocking decisions in the living
plan.
