# Phase 5 — Roll out

Deliver the verified change and close out. Only reachable once Verify is fully green.

## Delivery (discover-then-fallback)

1. Check the session for an **MR/PR MCP or skill** (e.g. a GitLab MR skill, a GitHub MR/PR
   integration, or the `gh` CLI). If several are present, **match the tool to the repo's remote
   host** (`gh` / GitHub integration ↔ GitHub, GitLab MR skill ↔ GitLab).
2. **If found:** open the MR/PR(s) **linked to the tracking ticket(s)**.
3. **If none:** prepare the branch(es) and a **ready-to-paste MR/PR description**, and hand off to
   the user. Use this skeleton:

   ```markdown
   **Summary:** what changed and why (1–3 sentences).
   **Tickets:** linked ticket(s), or "None".
   **Acceptance criteria:** each criterion + pass/fail; comparative ones with before → after numbers.
   **Quality:** lint/format clean; regression result (or `unit-tests-only` note from Verify).
   **Rollout / rollback:** deployment notes and how to revert.
   ```

**Prompt single-vs-separate:** ask whether the user wants a **single aggregate** MR/PR for review or
**separate** MR/PRs (e.g. per unit/ticket). Respect the tracker/ticket mapping when splitting — and
honor the **remediation-unit mapping** recorded in Plan (a remediation unit rides its parent's
ticket/PR unless it was given its own).

**Stacked on an unmerged predecessor:** when this change builds on a branch that hasn't merged yet
(common for chained hops — e.g. `4.12 → 5.12 → 6.12` — or a large change split into dependent
MR/PRs), **target the MR/PR at the predecessor branch**, not the mainline. Add a `Stacked on:
<predecessor MR/PR link>` note to the description and a next-step in the living plan doc:
"**after `<predecessor>` merges, retarget this MR to `<main>`** (`git rebase --onto <main>
<predecessor-branch>` then force-push, or repoint the target branch)." Keep that retarget in
**Next steps** until it's done — it's easy to forget once the predecessor merges.

All external creations follow **confirm-before-external-writes**: preview the MR/PR title, target
branch, and description, and get confirmation before creating.

## Post-MR E2E pipeline (discover-then-fallback — only when Verify recorded a `post-mr` deferral)

Skip this section entirely unless Verify's living-plan-doc **Deferred inputs** table has a `post-mr`
E2E deferral recorded (see `verify.md` §4). When it does, the suite could only be exercised once an
MR/PR existed — now that one does, run it before closeout.

1. **Discover, in order:** (1) an **in-repo trigger script** that kicks off the pipeline against an
   MR/PR ref (e.g. a script that calls the CI API with an MR number), then (2) a session skill for
   initiating this kind of pipeline (e.g. a Playwright-pipeline-kickoff skill), before falling back to
   (3) prompting the user to kick it off manually and report back — noting the gap in the MR/PR
   description per the same convention as a Verify coverage gap.
2. **Kick off** the pipeline against the just-created MR/PR and record the pipeline reference (URL/ID)
   in the living plan doc.
3. **Wait for completion** — this step **blocks** the Roll out gate; don't close out with the pipeline
   still running.
4. **On completion:**
   - **Pass** → resolve the Deferred-inputs row, mark the criterion satisfied, proceed.
   - **Fail** → discover a results-review skill/script the same way (in-repo script → session skill →
     fallback) and triage the failures, filtering **known environmental failures** the same way Verify
     does (see `verify.md` §4). A real regression gets **one** automatic remediation attempt: fix on
     the integration branch, push to the MR branch, and re-kick-off the pipeline.
   - **If that retry still fails:** stop auto-remediating. Present the user a **failure summary and
     recommended next steps** (e.g. retry again, treat as a known/flaky failure, or escalate) and wait
     for their direction before attempting any further fix — never loop silently past one failed
     retry.

## Address review feedback (opt-in — after the MR/PR is open)

Once the MR/PR exists, **ask the user whether they want you to work its code-review feedback** —
some teams prefer to drive review themselves. Only proceed on a yes. This step is **repeatable**:
run it again whenever new comments land, including in a later session (the MR/PR link lives in the
living plan doc, so a resumed session can pick it up).

When the user opts in:

1. **Fetch the open review threads.** Use the same MR/PR MCP/skill discovered in Delivery
   (discover-then-fallback) to read the **unresolved** comments/threads. Match by capability (list
   review comments); if none is available, ask the user to paste the feedback.
2. **Triage each comment:**
   - **Actionable code change** → make the fix. Trivial/localized fixes apply directly on the
     integration branch; substantial or cross-cutting ones become a **remediation work unit looped
     back through Execute** (TDD + per-unit gate), then re-verify the affected criteria. Never skip
     the gate for a "quick" review fix.
   - **Question / clarification** → answer it; no code change.
   - **Won't-fix / out-of-scope / disagree** → capture the rationale for the reply; don't change code.
3. **Reply and resolve (confirm-before-external-writes).** Draft a reply per thread — what changed
   (link the commit) or why not — and **preview all replies to the user before posting**. On
   confirmation, post each reply and **resolve** the thread. Leave threads the user wants to keep
   open unresolved, and don't resolve a reviewer's thread they've asked to hold.
4. **Record it.** Append the fixes to the living plan doc (and any remediation units to the wave
   log), then push the new commits so the MR/PR updates.

**Model note:** reading/summarizing threads and drafting mechanical replies is **haiku/sonnet**-level;
deciding whether a comment warrants a code change — and how — is integrator judgment.

## Closeout

- Update project docs / changelog / migration notes as the change requires.
- Transition tracking ticket(s) to the appropriate state (e.g. Ready to Test), with links to the
  MR/PR(s) — using the tracker's **equivalent** workflow state (see `tracking-integration.md`).
- **Finalize the living plan doc:** mark phases complete, record outcomes vs. acceptance criteria
  (with the comparative before/after numbers), and close the transition log.
- **Render the model & token usage report** from the usage rollup — a per-model breakdown of subagent
  spend for the run (see `usage-report.md`). Read-only; include it in the closeout summary.

## Gate to complete

- [ ] MR/PR(s) opened and linked to tickets, or branch + ready-to-paste description handed off.
- [ ] Single-vs-separate decision honored.
- [ ] Post-MR E2E pipeline green, or not applicable (no `post-mr` deferral recorded in Verify).
- [ ] Review feedback offered; if accepted, fixes applied, replies posted, and threads resolved (or
      the user declined / none yet). Repeatable as new comments land.
- [ ] Docs/changelog/migration notes updated as needed.
- [ ] Tickets transitioned with MR/PR links.
- [ ] Living plan doc finalized (phases complete, outcomes recorded).
- [ ] Model & token usage report rendered in the closeout summary.
