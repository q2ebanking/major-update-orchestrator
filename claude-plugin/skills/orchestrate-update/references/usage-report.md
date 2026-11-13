# Model & Token Usage Report

A budget-accounting report that breaks down **how much subagent work each model did** across the
orchestration. Rendered automatically at Roll out Closeout and available on demand at any phase (via
`/update usage` or natural language) — like the burn-down, it is **read-only** and never changes
phase or state.

## What is (and isn't) measurable

- **Measurable — subagent usage.** Every subagent completion reports its own token count and tool-use
  count (the `subagent_tokens` / `tool_uses` figures in the completion notification). The integrator
  records these, keyed by the **model it dispatched that subagent on** (haiku / sonnet / opus).
- **Not measurable — the integrator's own tokens.** The driver cannot observe its own in-session token
  consumption, so the report covers **dispatched subagent work only** and says so in a footnote. Do
  **not** estimate or fabricate the integrator's usage (Principle 3, no fabrication).
- **Unreported dispatches.** If a completion carries no usage figure (e.g. a chained session skill or
  a hand-off that doesn't report), still count the **dispatch** and its **tool_uses** if available, and
  record its tokens as **`unreported`** — never invent a number. Note in the report how many dispatches
  were unreported so the totals are read with that caveat.

## Recording (do this as work completes)

Maintain the **`## Model & token usage (rollup)`** table in the living plan doc
(`living-plan-doc-template.md`), updated **in place** — not append-only, so it stays a handful of rows
and never needs archiving. When a subagent completes and reports usage, add its tokens, tool_uses, and
a `+1` dispatch to the row for the model it ran on:

- **At wave convergence** — fold in every unit's executor **and** its independent verifier
  (`parallel-orchestration.md` § Converge, `execute.md` step 4), where you are already updating the doc.
- **Other dispatches** — recon (Assess), baseline capture, whole-change verifier + review (Verify),
  burn-down full-log reader, tracker-transition batches, roll-out thread work: add each when it
  completes.

Recording as you go (rather than reconstructing at the end) is what makes a resumed session's totals
correct — a later session cannot see an earlier session's completion notifications.

## Rollup table (lives in the living plan doc)

```markdown
## Model & token usage (rollup)
_Subagent accounting, updated in place at each convergence. Integrator's own tokens are excluded
(not self-observable in-session). Skip on resume — not actionable state._
| Model  | Dispatches | Tokens | Tool uses |
|--------|-----------|--------|-----------|
| haiku  | <n> | <sum> | <sum> |
| sonnet | <n> | <sum> | <sum> |
| opus   | <n> | <sum> | <sum> |
| **Total** | <n> | <sum> | <sum> |
_Unreported-token dispatches: <n> (tool_uses counted; tokens excluded from the token sum)._
```

## Report format (Closeout + on demand)

Render straight from the rollup — no extra reads:

```markdown
### Model & token usage
| Model  | Dispatches | Tokens | % of tokens | Tool uses |
|--------|-----------|--------|-------------|-----------|
| haiku  | … | … | … % | … |
| sonnet | … | … | … % | … |
| opus   | … | … | … % | … |
| **Total** | … | … | 100% | … |

_Subagent work only — the integrator's own tokens are not self-observable and are excluded.
Unreported-token dispatches: <n>._
```

Add one line of read-out: which model carried the most tokens, and whether the split matches the
intended tiering (mechanical → haiku, implementation → sonnet, judgment → opus). A surprise — e.g. opus
dominating a run with few judgment-heavy units — is a signal that work was dispatched over-powered and
worth a note for next time.

## On demand (`/update usage`)

Read-only, any phase: read the rollup section from the living plan doc, render the report above, and
stop. Do **not** change phase or state, and do **not** re-dispatch work to "measure" — the rollup is
the source of truth. If the rollup section is absent (an older plan doc), say so and report only what
later dispatches have recorded rather than reconstructing history.
