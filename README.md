# Major Update Orchestrator

A distributable [Claude Code](https://claude.com/claude-code) **plugin** that guides a developer
through the full lifecycle of a **major, codebase-spanning technical update** — the kind of change
that touches many packages/modules at once: framework upgrades, platform migrations, cross-cutting
refactors, and performance initiatives.

The hardest, most valuable job it does is **decomposing a codebase-spanning change into independent
work units and driving them in parallel with subagents, safely** — planning the fan-out, isolating
the work in git worktrees, and reconciling/verifying the results. The five-phase checklist is the
scaffolding; parallel orchestration is the payload.

The skill is **generic and platform-agnostic**. It adapts to whatever environment it runs in by
**discovering capabilities present in the session** (skills, MCP servers, trackers, MR/PR tooling,
test runners) and **falling back gracefully** when they are absent. It never hard-requires a
specific tool.

## Install

### Claude Code

**In a session** (interactive — opens the `/plugin` panel rather than installing directly;
Claude Code 2.1.275+):

```
/plugin install major-update-orchestrator --marketplace q2ebanking/major-update-orchestrator
```

If this marketplace isn't added yet, Claude Code asks you to confirm adding it, then opens the
plugin's details so you can pick an install scope (user, project, or local). It doesn't print a
success message in this form — the panel is the confirmation. No restart needed once you've
chosen a scope.

**From your shell**, outside a session, this installs directly with no panel (Claude Code
2.1.292+):

```
claude plugin install major-update-orchestrator --marketplace q2ebanking/major-update-orchestrator
```

Either form skips a separate `/plugin marketplace add` step — `--marketplace` adds and installs
together. To add the marketplace once and install by name afterward instead:

```
/plugin marketplace add q2ebanking/major-update-orchestrator
/plugin install major-update-orchestrator@major-update-orchestrator
```

**Trying it without installing anything:** clone the repo and load the plugin directory directly
for one session:

```
git clone https://github.com/q2ebanking/major-update-orchestrator.git
cd major-update-orchestrator
claude --plugin-dir ./claude-plugin
```

This loads `/update` and the `orchestrate-update` skill for that session only — nothing is
recorded in your settings. Run `/reload-plugins` after editing plugin files.

## Codex version

The separately maintained Codex implementation is in
[`codex-plugin/`](codex-plugin). Its marketplace contains the
[`major-update-orchestrator`](codex-plugin/plugins/major-update-orchestrator)
package, which has its own manifest, Codex-native orchestration guidance, and
tests. You can install it directly from the GitHub repository without cloning
the project; see its [installation instructions](codex-plugin/plugins/major-update-orchestrator/README.md).

## Use

```
/update <describe the update you want to make>
```

- Kicks off (or resumes) the orchestration. On resume it reads the existing **living plan doc** and
  continues from the current phase.
- `/update burndown` — renders an on-demand burn-down chart (remaining effort over time) from the
  living plan doc. Read-only; works in any phase.

You can also just describe a large update in natural language; the `orchestrate-update` skill
triggers on codebase-spanning changes.

### `/update` vs. `/orchestrate-update`

Typing `/major-update-orchestrator:` in Claude Code's completion list shows **both** `update` and
`orchestrate-update` — that's expected, not a duplicate. Claude Code exposes every installed skill
as a directly-invocable slash command in addition to any explicit `commands/` entry, so the skill
itself is typeable alongside its command wrapper. They aren't equivalent:

- **`/update`** is the intended entry point. It parses its arguments first — routing `burndown` and
  `usage` to read-only reports, and everything else to kickoff/resume — before handing off to the
  `orchestrate-update` skill.
- **`/orchestrate-update`** invokes the skill directly, skipping that argument parsing. There's no
  `burndown`/`usage` routing on this path; it goes straight into the skill's own resume-or-kickoff
  logic (look for a living plan doc, resume if found, else start at Assess).

Prefer `/update` for normal use.

## The Lifecycle

**Assess → Plan → Execute → Verify → Roll out.**

1. **Assess** — scope and blast radius, **measurable acceptance criteria**, baseline capture for
   comparative criteria, tracking-ticket discovery, lint/format discovery.
2. **Plan** — guided design → an authoritative **Design artifact**, then decomposition into
   **ordered waves of parallel-safe work units**, each **sized in story points**, with a recorded
   velocity for the forecast, synced to tickets.
3. **Execute** — drive the waves: fan out parallel subagents (each in its own git worktree),
   **test-first (RED → GREEN → refactor)**, per-unit format + lint gate, converge, and roll failed
   units into the next wave.
4. **Verify** — grade every acceptance criterion against its baseline, whole-change lint/format,
   code review, and an **E2E regression suite against the integration branch**. Never advance on red.
5. **Roll out** — open the MR/PR(s) linked to the tickets (or hand off a ready-to-paste
   description), transition tickets, and finalize the living plan doc.

## Two authoritative documents

- **Design artifact** — *why / architecture / tradeoffs / risks*.
- **Living plan doc** — *how / sequencing / progress*: the lifecycle header, acceptance criteria
  with captured baselines, the wave/work-unit encoding with per-unit story points and state, a
  timestamped transition log (the data source for the burn-down), decisions, and skill-gap log.

They are cross-linked; neither redefines the other's facts.

## Layout

This repo hosts two independently maintained products side by side — a Claude Code plugin and a
Codex plugin — plus repo-wide community-health files shared by both:

```
major-update-orchestrator/
├── claude-plugin/                   # Claude Code plugin
│   ├── .claude-plugin/plugin.json   # manifest
│   ├── commands/update.md           # /update entry point          ← installed
│   ├── agents/                                                     ← installed
│   ├── skills/orchestrate-update/                                  ← installed
│   │   ├── SKILL.md                 # conductor + 5-phase checklist
│   │   └── references/              # per-phase + per-topic guides, templates
│   └── scripts/validate.py          # structural validation (CI)
├── .agents/plugins/marketplace.json # Root Codex marketplace
├── codex-plugin/
│   └── plugins/major-update-orchestrator/  # Codex plugin (see its own README)
├── CONTRIBUTING.md · TESTING.md     # how to contribute and test
├── CODE_OF_CONDUCT.md · LICENSE.md
└── README.md
```

**What gets installed.** Claude Code only activates a plugin's *components* — the `commands/`,
`skills/`, `agents/`, `hooks/` directories and any MCP servers declared in the manifest, resolved
relative to `claude-plugin/`. That's the entire installed surface: only `/update` and the
`orchestrate-update` skill.

The conference deck tooling that introduces this project lives in a **separate sibling project**
(`../major-update-orchestrator-presentation`), so it is neither installed nor shipped with the
plugin.

## Testing

The plugin is markdown skills and commands, so the test suite has two layers:

- **Structural validation.** `python3 claude-plugin/scripts/validate.py` checks the manifest,
  required files, and that every skill/command is well-formed. Run it before opening a pull
  request; no CI runs it automatically on this repo yet.
- **Behavioral tests (reviewer-run).** Exercising the orchestrator end-to-end requires a live
  agent session; the procedure is in [`TESTING.md`](TESTING.md).

## Contributing

Contributions are welcome — see [`CONTRIBUTING.md`](CONTRIBUTING.md) for how to propose a change
and run the checks. Participation is governed by our [Code of Conduct](CODE_OF_CONDUCT.md).

## License

Licensed under the Apache License, Version 2.0 — see [`LICENSE.md`](LICENSE.md).
