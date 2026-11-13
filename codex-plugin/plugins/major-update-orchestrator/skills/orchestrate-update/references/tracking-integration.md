# Tracking integration

Tracking is optional. First discover whether the active session has an approved
tracker connector or project CLI; otherwise keep ticket references as `Not
provided` and prepare a copyable handoff.

Before any external write, preview the issue creation/update/transition payload
and ask the user to confirm. Discover the tracker's actual status names and
transition IDs rather than assuming labels such as "In Progress" or "Done".
After every transition, re-query the issue and record the verified result in the
living plan's tracker map. Cache that role-to-transition mapping for later
waves.

During Plan, map each work unit to an existing ticket or an explicit
ticketless marker. If a ticket already has an estimate, reconcile it with the
unit's point estimate; otherwise preview the proposed estimate before writing
it. A remediation unit inherits its parent unit's ticket unless the living plan
records a deliberate exception.

Resolve transition paths before the first state change, not when delivery is
blocked on one. Enumerate the transitions actually available for the relevant
issue type and record the route for each orchestration state (for example,
`Todo → In Progress → Ready for review`). Where the tracker requires multiple
hops, record each intermediate state and any required fields or approvals. If
the connector is present but unauthorised or unresponsive, record that as a
capability failure and ask the user for direction rather than silently treating
the update as ticketless.
