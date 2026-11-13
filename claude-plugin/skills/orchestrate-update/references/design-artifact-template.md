# Design Artifact Template

Authoritative for **why / architecture / tradeoffs / risks**. Created in Plan 2a, reviewed once
before saving. Cross-linked with the living plan doc; it does **not** carry sequencing or progress
(that lives in the living plan doc — authority boundary).

Copy the block below into `docs/<slug>-design.md` (or alongside the living plan doc) and fill it in.
Label unknowns `TBD` / `Not provided`. Scale the depth to the change.

```markdown
# <Update name> — Design

**Status:** Draft | Reviewed
**Date:** <YYYY-MM-DD>
**Parent ticket:** <ref/URL or "None">
**Living plan doc:** <link>

## 1. Context & scope
What is changing and why. In scope / out of scope. Constraints carried from Assess
(acceptance criteria, baselines, known risk areas).

## 2. Approach
### Chosen approach
<the approach and why it was chosen>

### Alternatives considered
- <alternative> — rejected because <reason>
- <alternative> — rejected because <reason>

## 3. Architecture / integration model
How the change fits the existing structure: module boundaries, shared code, migration/compat
strategy (codemods vs. manual, dual-run/flagged, incremental vs. big-bang), sequencing constraints.

## 4. Risks & constraints
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| <risk> | <L/M/H> | <L/M/H> | <mitigation> |

Rollback story. External dependencies. Anything that could force a re-plan.

## 5. Acceptance criteria (reference)
Link to the criteria (owned in the living plan doc / Assess findings). Do not redefine them here.
```
