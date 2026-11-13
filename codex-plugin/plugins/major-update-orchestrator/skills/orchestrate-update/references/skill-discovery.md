# Capability discovery

At the start of Assess, inspect what the current Codex session can actually do.
Use available project tools and installed skills rather than assuming a named
integration exists.

| Need | Prefer when available | Fallback |
|---|---|---|
| Repository survey | exploration/recon skill or worker | targeted file and Git inspection |
| Guided design | `mattpocock-skills:grilling` to grill against project evidence and record decisions in the design artifact; if unavailable, `superpowers:brainstorming` | bundled Guided design reference |
| Planning | planning/design skill | bundled Plan and Guided design references |
| Independent plan review | read-only planning/review worker or skill | bundled plan-review procedure |
| Parallel work | Codex collaboration | serial waves with the same isolation rules |
| Worktree setup | Git/worktree helper | bundled Git commands in the skill |
| Verification | verification/review skill or worker | bundled Verify procedure |
| Ticket tracker | configured ticket connector/CLI | ask once whether to use a ticketing technology or proceed ticketless; record the answer |
| Source-repository remote API | configured Git-host connector/CLI | ask once which remote system/API or CLI to use for branch and PR/MR work; record the answer |
| Code review | configured review connector/CLI | bundled review procedure |
| Skill authoring | skill-creation capability | bounded inline procedure or a recorded user handoff |
| E2E regression | E2E runner/MCP or an in-repo invocation script | ask the user to run the suite and report results |
| E2E pipeline kickoff (post-MR) | in-repo trigger script or a session skill that initiates a pipeline for an MR/PR | ask the user to kick off the pipeline manually and report results |
| E2E pipeline results review (post-MR) | in-repo results script or a session skill that reviews pipeline results | ask the user to review the pipeline results manually and report |

Record a capability gap only when it changes the plan or requires a user
handoff. Never claim that a connector, skill, or model is present without
checking the active session.

A connector catalog entry is not evidence that the account is connected or
authorized. Perform a read-only health check before treating a discovered
ticket or source-repository capability as usable. Do not use plugin management
when the active session already exposes the required connector.

## Assistive skill scan (per phase, beyond the capability map)

The capability map covers direct reuse-or-fallback needs. Separately, at each
phase entry, scan the full session-available skill list for optional skills
that would improve that phase even when they do not correspond to a named
capability. Match by the work the phase needs now, not by a fixed skill name;
an absent assistive skill never blocks progress.

| Phase | What may help | Example assistive skill type |
|---|---|---|
| Assess | Pressure-test scope, assumptions, and acceptance criteria | requirements or assumption review |
| Plan | Stress-test the design and wave decomposition | design or plan review |
| Execute | Root-cause a stubborn failure | systematic debugging |
| Verify | Diagnose a failed gate or inspect code quality | debugging or code review |
| Roll out | Tighten PR/ticket prose and closeout reporting | writing clarity or visualization |

## Phase-entry skill table

Before starting work in a lifecycle phase, resolve and show the skills driving
that phase:

| Role / function | Candidate skill(s) | Type | Selected |
|---|---|---|---|
| <what the phase needs> | <matching skill name(s)> | capability / assistive | <chosen skill or —> |

Include only roles relevant to the current phase. For each role:

- One plausible candidate: select it.
- Multiple plausible candidates: ask the user to choose with
  `request_user_input` when available; otherwise ask one concise direct
  question. Do not silently choose among unordered candidates. For an
  explicitly ordered fallback chain, select the first available candidate.
- No candidate: record `—`; use the bundled fallback for a capability role or
  skip an assistive role.

Show the resolved table, then begin the phase.
