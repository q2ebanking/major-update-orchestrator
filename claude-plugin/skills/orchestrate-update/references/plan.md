# Phase 2 — Plan

Two checkpoint-driven sub-stages. This phase carries **extra interactive emphasis on design**. If
`uux-planning-docs` is present in the session you may reuse it; otherwise use the bundled approach in
`guided-design.md`. Whichever you use, apply the concepts — interactive design checkpoints, an
authoritative design artifact, evidence-driven discipline, and a clear authority boundary between
documents.

## 2a — Guided Design (interactive)

Walk the developer through design decisions **one area at a time** and produce a reviewed **Design
artifact** (template: `design-artifact-template.md`), authoritative for:

- Approach alternatives and tradeoffs (with a recommendation).
- Architecture / integration model.
- Technical risks and constraints.

Checkpoints (not section-by-section nagging):

1. Confirm feature/change context and scope.
2. Work through the design decisions collaboratively.
3. **One review checkpoint** on the drafted Design artifact before it is saved.

Evidence-driven: label unknowns `TBD` / `Not provided`; fabricate nothing. For a small update, the
Design artifact may be a short, decision-focused document. Full walkthrough in `guided-design.md`.

## 2b — Decomposition & Plan

Once the design is approved, **dispatch a planning subagent** (or chain to **superpowers:writing-plans**
if present) to convert the approved design into the **living plan doc** (template:
`living-plan-doc-template.md`).

**Living plan doc** = the planning output + a thin **lifecycle header** you add (phase status, parent
ticket ref, acceptance criteria, skill-gap log, recorded **velocity** in points-per-two-weeks). This
one artifact is both the plan and the progress tracker.

### Bundled planning-subagent prompt (fallback when `writing-plans` is absent)

Dispatch **one** planning subagent with a self-contained prompt:

- **Inputs:** the approved Design artifact + the Assess findings (scope, acceptance criteria with
  baselines/thresholds, dependency map, lint/format commands).
- **Task:** decompose the change into **ordered waves of parallel-safe work units** (no shared files,
  no intra-wave dependencies), and for **each unit** emit every field in the work-unit encoding below
  — including a proposed **story-point size** and the acceptance criterion each unit traces to.
- **Output shape:** the "Waves & work units" block of `living-plan-doc-template.md`, filled, plus a
  proposed **criteria → units** map. Return only that filled markdown.

**Before the plan checkpoint, dispatch an independent plan reviewer** against the draft output —
same "separate agent, no stake in the outcome" discipline already used for code verification, applied
one phase earlier to catch a flawed decomposition before Execute burns cycles on it. See
`plan-reviewer.md` for the canonical dispatch, checklist, and verdict contract. Resolve every finding
(re-wave, re-size, re-map criteria coverage) before presenting the draft to the user — this is a hard
gate, not advisory.

You (the integrator) review and adjust the reconciled output with the user at the plan checkpoint;
sizes and waves are not final until approved.

### Work-unit encoding — ordered waves of parallel-safe batches

Each unit carries:

- File/path **scope**.
- **Dependencies** on other units.
- **Isolation method** (worktree vs. non-overlapping paths) — see `parallel-orchestration.md`.
- Explicit **done/verify criteria**, traceable to Assess acceptance criteria.
- A **story-point size** (required — see below).
- A **tracking-ticket ref**.

Group units into **ordered waves**: every unit in a wave must be parallel-safe with its wave-mates
(no shared files, no intra-wave dependencies). A unit that depends on another runs in a later wave.

**Criteria coverage (traceability).** Map every Assess acceptance criterion to the work unit(s) that
satisfy it, and record the mapping in the living plan doc. This is what lets Verify grade an absolute
"all-of-set" criterion honestly: it stays **fail/Blocked** while any mapped unit is unexecuted,
deferred, or `Unsized`.

### Story-point sizing (required on every unit)

Every unit gets a **story-point** size during Plan — this makes the burn-down plot remaining
**effort**, not raw unit count, and gives the ideal trend line and completion projection meaning.
The planning subagent proposes point values; the user reviews/adjusts them at the plan checkpoint.
If a unit can't be sized, mark it `Unsized` and surface it — never silently treat it as zero
(unsized work distorts the curve). An `Unsized` unit **may not enter a wave**: either size it before
Execute, or record it as **deferred / out-of-scope for this run** and mark every acceptance criterion
that depends on it **Blocked**. Deferred and `Unsized` units are **excluded from the burn-down
effort math** and listed separately (see `burndown.md`).

### Velocity for the forecast

Prompt the user for a rough **velocity**: *"about how many story points do you expect to complete in
a two-week span?"* Record this points-per-two-weeks figure in the lifecycle header. It drives the
ideal trend line and the projected completion date, and can be refined as actual throughput is
observed. If the user declines, the burn-down still plots the actual curve but omits the forecast
line.

### Ticket sync (confirm before external writes)

- If sub-tickets already exist, the decomposition **respects and maps to them**, and reconciles
  sizing: adopt the ticket's existing size if present, else propose writing the unit's size back.
- If none exist, **create one per work unit** via the discovered tracker, **including the size
  estimate** — previewed and user-confirmed before any write. If ticket-less, size still lives on
  the unit in the living plan doc. See `tracking-integration.md`.
- **Deferred and remediation units:** a deferred `Unsized` unit still gets its **own ticket** so it
  isn't lost. A remediation unit (a failed unit rolled forward, or a Verify-failure fix) **inherits
  its parent unit's ticket** unless you deliberately give it its own — record which in the living
  plan doc, and honor the same choice at Roll out when splitting MR/PRs.
- **Resolve the tracker transition map now — don't defer it to the first write.** While you're
  already talking to the tracker, enumerate the parent ticket's *available* transitions and resolve
  the role → transition map (to-in-progress / to-done / to-rolled-out) into the living plan doc's
  **Tracker transition map** (see `tracking-integration.md`). Doing this in Plan surfaces
  workflow surprises early — hidden/validator-gated transitions, **multi-hop paths** (no direct jump
  to the target status), or an unresponsive/auth-expired tracker tool — while they're cheap to
  handle, instead of at Roll out on the critical path. Leaving the map `TBD` until the first
  transition means discovering those surprises when a delivery is blocked on them.

### Skill-gap resolution (decided here, acted on in Execute)

For each unit needing a capability with no matching skill in the session, offer the user a choice —
**handle it inline** this once, or **author a reusable skill** (via **superpowers:writing-skills** if
present, else the bundled minimal SKILL.md template). Record the decision per unit in the living plan
doc's skill-gap log. See `skill-discovery.md`.

## Authority boundary

Design artifact = *why/architecture*; living plan doc = *how/sequencing/progress*. Cross-linked;
neither redefines the other's facts.

## Gate to advance

- [ ] Design artifact reviewed and saved.
- [ ] Independent plan reviewer returned CLEAN, or all findings resolved (`plan-reviewer.md`).
- [ ] Waves + per-unit story points approved by the user.
- [ ] Tickets synced (creations/updates confirmed) or ticket-less noted.
- [ ] Tracker transition map resolved into the living plan doc (or ticket-less noted).
- [ ] Velocity recorded (or user declined, noted).
- [ ] Skill gaps decided per unit.
