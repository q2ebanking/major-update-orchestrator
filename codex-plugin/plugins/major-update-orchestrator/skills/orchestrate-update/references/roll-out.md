# Roll out

Prepare external writes as previews: PR/MR description, ticket updates, release
or migration notes, and rollback instructions. Ask for confirmation before
posting, pushing, or transitioning remote state. A direct user instruction to
create a named ticket, branch, or PR/MR is sufficient confirmation; announce
the concise intended payload before executing rather than requiring a redundant
round trip. Re-query a ticket after a transition before reporting it complete.

## Delivery

1. Discover a usable PR/MR capability and match it to the repository's remote
   host. For example, use a GitHub capability for a GitHub remote and a GitLab
   capability for a GitLab remote; do not select a similarly named but
   incompatible connector.
2. Ask whether the user wants one aggregate PR/MR or separate PR/MRs by unit
   or ticket. Respect the recorded ticket mapping, including a remediation
   unit's inherited ticket, when splitting.
3. If no usable PR/MR capability exists, prepare the branch and a ready-to-paste
   description containing: summary, linked tickets (or `None`), acceptance
   criteria and results, quality/E2E evidence, and rollout/rollback notes.
4. When the change is stacked on an unmerged predecessor branch, target the
   PR/MR at that predecessor rather than the mainline. Include a `Stacked on:`
   link and record a concrete retarget-after-merge step in the living plan.

## Address review feedback (opt-in)

Once a PR/MR exists, ask whether the user wants review feedback handled. Do
nothing further unless they opt in; repeat this workflow when new feedback
lands or a later session resumes from the recorded PR/MR link.

1. Fetch unresolved threads with the delivery capability. If it cannot read
   review threads, ask the user to provide the feedback.
2. Triage each item: an actionable code change, a question requiring a reply,
   or a documented won't-fix/out-of-scope decision.
3. Apply a trivial, localized code change only with its affected verification
   gate. Convert a substantial or cross-cutting change into a sized remediation
   work unit and return through Execute and Verify; never waive a gate because
   the work originated in review.
4. Draft replies and show all external replies or thread resolutions for
   confirmation before posting. Record the outcome, push verified fixes, and
   leave any user-designated thread unresolved.

After the remote write, re-query the created ticket/MR or its pipeline state
when the connector supports it. Finish the living plan with criteria outcomes,
post-rebase gate evidence, final links and remote status, known baseline
exceptions, known follow-ups, and a worker-usage rollup. Keep unresolved risks
visible rather than declaring the update complete.

## Post-MR E2E pipeline (only when Verify recorded a `post-mr` deferral)

Skip this section unless the living plan's **Deferred inputs** table records a
`post-mr` E2E deferral. That suite was not runnable until an MR/PR existed, so
run it after creating the MR/PR and before closing out the update.

1. **Discover, in order:** (1) an **in-repo trigger script** that starts the
   pipeline for an MR/PR ref, then (2) a session skill that initiates that kind
   of pipeline, then (3) user handoff to start it manually. In the handoff
   case, record the coverage gap in the MR/PR description using the same
   convention as a Verify coverage gap.
2. Kick off the pipeline for the newly created MR/PR and record its URL or ID
   in the living plan. This is an external write: preview the intended action
   and obtain the required confirmation before triggering it.
3. **Wait for completion.** The pipeline blocks the Roll out gate; do not
   close out while it is running.
4. On completion:
   - **Pass:** resolve the Deferred-inputs row, mark the criterion satisfied,
     and proceed.
   - **Fail:** discover a results-review script or skill in the same order
     (in-repo script, session skill, user handoff), then triage it using
     Verify's baseline and environmental-failure rules. For a real regression,
     make one remediation attempt on the integration branch, push the fix to
     the MR/PR branch, and re-trigger the pipeline.
   - **Retry fails:** stop automatic remediation. Present a failure summary and
     recommended next steps, then wait for the user's direction before any
     additional fix or retry. Never loop silently beyond one failed retry.

Do not mark the update complete unless this pipeline passes or its absence is
explicitly recorded as a user-owned coverage gap.

## Closeout gate

- [ ] PR/MR opened and linked to its ticket(s), or a branch and paste-ready
      description handed off.
- [ ] Aggregate-versus-separate and any stacked-PR decisions honored.
- [ ] Post-MR E2E pipeline passed or is not applicable.
- [ ] Review feedback was offered; accepted work was verified, replied to, and
      resolved as approved.
- [ ] Required docs, changelog, migration notes, ticket transitions, and the
      living-plan outcome are complete.
