# Contributing

Thanks for your interest in improving the Major Update Orchestrator. This project
is a [Claude Code](https://claude.com/claude-code) plugin made of markdown skills
and commands — there is no compiled code, so contributions are almost always edits
to the skill guidance, its reference files, or the docs.

## Ground rules

- Be respectful. This project follows the [Code of Conduct](CODE_OF_CONDUCT.md).
- Keep the skill **generic and platform-agnostic**. It discovers capabilities in
  the session and falls back gracefully; never hard-require a specific tool,
  tracker, or CI system.
- Match the surrounding style: concise, trigger-conditions-only skill
  descriptions (no workflow summaries), reference files kept tight and
  cross-referenced by name.

## How to propose a change

1. Create a branch off `main`.
2. Make your change. If you touch the skill's behavior, update the relevant
   reference file under `claude-plugin/skills/orchestrate-update/references/`.
3. Run the checks below locally.
4. Open a merge request against `main` and describe what changed and why.

## Testing

Two layers, both described in [TESTING.md](TESTING.md):

- **Structural validation (automated, runs in CI):**

  ```sh
  python3 claude-plugin/scripts/validate.py
  ```

  It validates the manifest, required files, and that every skill/command is
  well-formed. This runs on every merge request and must pass before merge.

- **Behavioral tests (run by a reviewer):** for changes that alter the
  orchestrator's behavior, exercise the affected phase(s) per the procedure in
  TESTING.md and note the outcome in the merge request. These require a live
  agent session and can't run in CI.

## Reporting issues

Open an issue describing the problem, what you expected, and how to reproduce it.
For anything security-sensitive, contact the maintainers directly rather than
filing a public issue.
