# Read-only reporting

For a burndown, derive remaining points from every sized unit's timestamped
state transitions. Render a remaining-effort table plus a compact Mermaid or
ASCII trend. Do not label the effort complete while unsized or deferred units
remain.

For a usage report, show both the model requested at dispatch and the model
actually reported by the platform. Aggregate tokens and tool uses only from
worker-provided telemetry. The integrator's own token use is not self-observable.
If actual model, token count, or tool-use count is unavailable, preserve `Not
reported` rather than filling the gap with an estimate.
