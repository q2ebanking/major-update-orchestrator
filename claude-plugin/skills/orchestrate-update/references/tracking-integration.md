# Tracking Integration — discover-then-fallback

The orchestrator anchors work to a tracking system when one is available, and works cleanly without
one. It never hard-requires a tracker.

## Discover

Check the session for a tracking MCP/skill — Jira, GitLab issues, GitHub issues, or a project
tracking skill. Match by **capability** (read an issue, create an issue, transition an issue), not by
an assumed exact tool name.

## Read / create / link

- **Existing parent ticket:** read it for requirements and existing sub-tickets. Map the
  decomposition's work units onto existing sub-tickets where they correspond.
- **Create (confirm first):** create a parent ticket in Assess and/or one ticket per work unit in
  Plan. **Preview the ticket contents** — title, description, and the **story-point size** — and get
  user confirmation before any write. This is a hard-to-reverse external write.
- **Sizing reconciliation:** if a ticket already carries a size, adopt it; otherwise propose writing
  the unit's Plan size back to the ticket (confirm first).

## Status transitions — map to the tracker's equivalent

Workflow state names **and the transitions between them** vary between trackers and projects.
**Never assume a literal status string or a hardcoded transition id/name.**

| Orchestrator state | Tracker equivalent (examples) |
|---|---|
| Unit dispatched | "In Progress" / "In Development" / "Doing" |
| Unit converged (done) | "Done" / "Ready for Review" / "Code Review" |
| Change rolled out | "Ready to Test" / "In QA" / "Resolved" |

**Discover, then map by role — don't guess:**

0. **Check the cache first.** Before enumerating, check the living plan doc's Tracker Transition Map
   for a resolved role → transition entry for this project/issue-type. If one exists, use it directly
   and skip to step 6 (confirm the transition landed). Only fall through to live discovery (step 1
   onward) if no cached entry exists.
1. **Enumerate** the issue's *actually available* transitions via the tracker API (e.g. Jira
   `getTransitionsForJiraIssue`) — availability depends on issue type, project workflow, and the
   current status, so query the specific issue.
2. **Map by role** (to-in-progress / to-done / to-rolled-out) to what the enumeration returned, not
   to an assumed id or label.
3. **Handle hidden/blocked transitions.** Workflow validators or required-field screens can hide the
   expected transition (e.g. no direct "In Progress" path; only a "Close" transition that also sets a
   resolution). If the role you need isn't available, look for an alternate transition that reaches
   an equivalent state, and supply any fields it requires (e.g. a resolution). If none works or it's
   ambiguous, **surface the available options to the user and ask** which to use.
4. **Multi-hop paths.** Many workflows block a direct jump to the target status — the state you want
   is only reachable *through* an intermediate one (e.g. `Backlog → In Progress → Acceptance`, with
   no `Backlog → Acceptance` transition). If the target role isn't directly available, check whether
   a **two-hop path** exists: transition to the intermediate state, **re-enumerate** from there, then
   transition to the target. Execute the hops in sequence and confirm each. Record the full path in
   the transition map so later sessions don't rediscover it.
5. **Map the user's words to a real status — don't assume the literal string exists.** When the user
   asks for a status by an informal name ("ready to test", "in review", "done"), treat it as a
   **role**, not a literal: enumerate the issue's statuses/transitions and pick the workflow status
   that fills that role. If no status matches the name literally and the best fit has a *different*
   name (e.g. the ready-to-test role is a status literally named "Acceptance"), **tell the user which
   status you resolved it to** rather than silently transitioning to a differently-named state.
6. **Confirm the transition actually landed.** A transition API call returning success is **not**
   proof the status changed — validators, permissions, or async post-functions can no-op or partially
   apply. **Re-query the issue** after each transition and confirm the current status is what you
   expected before reporting done or firing the next hop. If it didn't change, surface the actual
   state.
7. **Cache the resolved mapping in the living plan doc** (a small "tracker transition map" note:
   role → transition id(s) + any multi-hop path + required fields) so later units and later sessions
   reuse it instead of rediscovering. **Resolve it in Plan** (during ticket sync), not on the first
   write — see `plan.md`. Record it once per project/issue-type.

**Model note:** transition discovery and firing are mechanical extraction/API work — **haiku**-level.
If several transitions are needed at once, batch them into a single haiku subagent to keep this off
the integrator's heavy model.

## Transition timing

- **On dispatch** (Execute, per unit): move the matched ticket to the in-progress equivalent, and
  append the transition to the living plan doc's timestamped log.
- **On converge** (Execute, per unit): move to the done/ready-for-review equivalent, append to the
  log.
- **On roll out** (Phase 5): move to the ready-to-test equivalent, with a link to the MR/PR.

All ticket writes follow **confirm-before-external-writes**, and every transition is **re-verified**
after firing (re-query the issue; API success ≠ status changed — see step 6 above).

**When the tracker tool is present but unresponsive.** A discovered tracker MCP/tool can be *present*
yet fail mid-operation — a timeout, an expired auth token, or a rate limit. This is distinct from the
tool being absent (see `skill-discovery.md`): don't silently fall back to ticket-less. Surface it to
the user with the specific ask (re-authenticate, wait and retry), retry the write, then **re-query to
confirm it landed** — a call that timed out may have partially applied before the client gave up.

## Fallback — no tracker

- Ask the user for a ticket ID/URL to **record** as the parent reference, or
- Proceed **ticket-less**: track everything in the living plan doc, and annotate units `(no ticket)`.
  The burn-down still renders from the living plan doc's transition log and unit sizes; it simply
  omits the ticket-link columns.
