# Major Update Orchestrator for Codex

Use this Codex plugin for a codebase-spanning upgrade, migration, refactor, or
technical-debt initiative that needs deliberate planning and safely parallel
implementation.

Start in a new Codex thread and describe the update in natural language. The
`orchestrate-update` skill also recognizes requests for a burn-down or usage
report for an active update.

This is an independent Codex implementation. The repository's Claude Code
plugin remains at the repository root and is intentionally not shared with this
package.

## Install from the repository

Codex can fetch the marketplace directly from GitHub, so you do not need to
clone this project. Run:

```sh
codex plugin marketplace add https://github.com/q2ebanking/major-update-orchestrator.git \
  --sparse .agents/plugins \
  --sparse codex-plugin/plugins/major-update-orchestrator
codex plugin add major-update-orchestrator@personal
```

Start a new Codex thread after installing or updating the plugin.

## Local installation

From the repository root, configure the marketplace once:

```sh
codex plugin marketplace add .
codex plugin add major-update-orchestrator@personal
```

Use this option when you already have a checkout. Start a new Codex thread after
installing or updating the plugin.

## Validation

Run the package-local structural checks before publishing a change:

```sh
python3 scripts/validate.py
```
