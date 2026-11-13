# Guided Design (bundled fallback)

Used in Plan 2a when `uux-planning-docs` is not present. Produces a reviewed **Design artifact**
(template: `design-artifact-template.md`). The goal is a collaborative, evidence-driven design
walkthrough — not a form to fill in silently.

## Principle

Interactive **checkpoints**, not section-by-section nagging. Work through decisions collaboratively,
one area at a time, and converge on a documented design the user has reviewed. Label every unknown
`TBD` / `Not provided`. Fabricate nothing — not a file path, not an API, not a constraint.

## Walkthrough

Ask **one focused question at a time**. Prefer concrete multiple-choice framing (with your
recommendation and its reasoning) over open prompts when the options are known.

1. **Context & scope.** Restate the change and its boundaries. Confirm what is in and out of scope.
   Surface anything from Assess that constrains the design (criteria, baselines, risk areas).
2. **Approach alternatives.** Lay out 2–3 viable approaches with tradeoffs. Lead with your
   recommendation and why. Capture the chosen approach and the rejected ones (with the reason) —
   rejected alternatives are part of the record.
3. **Architecture / integration model.** How the change fits the existing structure: module
   boundaries, shared code, sequencing constraints, migration/compat strategy (codemods vs. manual,
   dual-run/feature-flag, big-bang vs. incremental).
4. **Risks & constraints.** Technical risks, blast radius, rollback story, external dependencies,
   anything that could force a re-plan.

## Review checkpoint (required)

Draft the Design artifact, then present it for **one review checkpoint** before saving. Invite
corrections. Only save once the user approves. The saved artifact is authoritative for
*why/architecture/tradeoffs/risks* and is cross-linked from the living plan doc.

## Scale to the change

For a small update, the Design artifact may be a short, decision-focused document — a few paragraphs
capturing the approach, the key decision, and the risks. Don't pad it. For a large migration it may
warrant a full section per decision area. Match the artifact's weight to the change.

## Handing off to decomposition

The approved design is the **input to Plan 2b**. The decomposition (planning subagent or
**superpowers:writing-plans**) reads it to derive the waves and work units. Keep the design free of
sequencing/progress detail — that belongs in the living plan doc (authority boundary).
