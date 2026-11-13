# Testing

This plugin is composed of markdown skills and commands, so its test suite has
two layers: **structural validation**, a script a reviewer or contributor runs
by hand, and **behavioral tests** that a reviewer runs in a live agent session.
No CI runs either automatically on this repo yet.

## 1. Structural validation

`claude-plugin/scripts/validate.py` is the automated-suite script. Run it locally before
opening a pull request:

```sh
python3 claude-plugin/scripts/validate.py
```

It checks:

- `claude-plugin/.claude-plugin/plugin.json` is valid JSON and declares `name` and `version`.
- The required files are present: `README.md`, `LICENSE.md`,
  `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`.
- At least one command exists under `commands/`.
- Every `skills/*/SKILL.md` has frontmatter with `name` and `description`.
- The community-health files carry no unresolved placeholders (`INSERT ...`,
  `TBD`, `TODO`).

A merge request must not merge while this fails.

### Codex package checks

The separately maintained Codex package has dependency-free structural checks:

```sh
python3 codex-plugin/plugins/major-update-orchestrator/scripts/validate.py
```

They validate the Codex manifest, skill frontmatter, every reference path used
by the skill, and the repository marketplace entry. This command runs in CI
alongside the Claude plugin validator. If the local Codex installation includes
the `plugin-creator` skill and its validator dependencies, contributors may
also run that skill's `validate_plugin.py` against
`codex-plugin/plugins/major-update-orchestrator`; its installation path is
intentionally not prescribed here.

## 2. Behavioral tests (reviewer-run)

The orchestrator's real behavior can only be exercised in a live agent session,
so these are run by a reviewer for any change that alters behavior, and the
outcome is noted on the merge request:

1. **Full-lifecycle dry run.** Against a sample multi-package change, walk all
   five phases (Assess → Plan → Execute → Verify → Roll out), including at least
   one parallel wave that contains a **failing unit** (to confirm
   isolate-continue-report) and a **Verify-failure remediation loop**.
2. **Graceful-fallback run.** Repeat in a minimal environment (no superpowers
   skills, no tracker, no MR/PR tooling) and confirm the bundled fallbacks
   engage instead of hard failures.
3. **Burn-down mid-run.** After some units have closed, request a burn-down
   chart and confirm it renders the remaining-effort table, the Mermaid curve,
   and the ASCII fallback from the transition log — with ticket links on matched
   units and graceful handling of an empty log.

The two capability profiles (rich vs. minimal) are the pressure scenarios: the
skill should behave correctly in both. Record which profile was exercised and
the result in the merge request description.
