#!/usr/bin/env python3
"""Structural validation for the major-update-orchestrator plugin.

Runs in CI on every merge request and can be run locally. It checks the plugin
manifest, required community-health files, and that every skill/command is
well-formed — the automated half of the test suite. The behavioral tests
(exercising the orchestrator end-to-end) are described in TESTING.md and run by
a reviewer, since they require a live agent session.

Exit code 0 = all checks pass; 1 = one or more failures.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent  # community-health files live at the repo root, shared with the Codex plugin

errors: list[str] = []
checks = 0


def check(condition: bool, ok_msg: str, fail_msg: str) -> None:
    global checks
    checks += 1
    if condition:
        print(f"  ok   {ok_msg}")
    else:
        print(f"  FAIL {fail_msg}")
        errors.append(fail_msg)


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def frontmatter(text: str) -> dict[str, str]:
    """Parse a minimal `key: value` YAML frontmatter block. Good enough for
    the two fields we require; not a general YAML parser."""
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}
    fields: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip()
    return fields


print("== manifest ==")
manifest_path = ROOT / ".claude-plugin" / "plugin.json"
manifest: dict = {}
if manifest_path.is_file():
    try:
        manifest = json.loads(read(manifest_path))
        check(True, "plugin.json is valid JSON", "")
    except json.JSONDecodeError as exc:
        check(False, "", f"plugin.json is not valid JSON: {exc}")
else:
    check(False, "", "plugin.json is missing")
check("name" in manifest, "manifest has a name", "manifest is missing 'name'")
check("version" in manifest, "manifest has a version", "manifest is missing 'version'")

print("== required files ==")
for name in ("README.md", "LICENSE.md", "CODE_OF_CONDUCT.md", "CONTRIBUTING.md"):
    check((REPO / name).is_file(), f"{name} present", f"{name} is missing")

print("== commands ==")
commands = list((ROOT / "commands").glob("*.md"))
check(bool(commands), f"{len(commands)} command file(s) found", "no command files under commands/")

print("== skills ==")
skills = sorted((ROOT / "skills").glob("*/SKILL.md"))
check(bool(skills), f"{len(skills)} skill(s) found", "no SKILL.md files under skills/")
for skill in skills:
    fm = frontmatter(read(skill))
    rel = skill.relative_to(ROOT)
    check(bool(fm.get("name")), f"{rel} has a name", f"{rel} frontmatter missing 'name'")
    check(bool(fm.get("description")), f"{rel} has a description", f"{rel} frontmatter missing 'description'")

print("== no unresolved placeholders ==")
placeholder = re.compile(r"INSERT [A-Z ]+|\bTBD\b|\bTODO\b", re.IGNORECASE)
for name in ("README.md", "CODE_OF_CONDUCT.md", "CONTRIBUTING.md"):
    path = REPO / name
    if not path.is_file():
        check(False, "", f"{name} is missing, cannot check for placeholders")
        continue
    hits = [line for line in path.read_text(encoding="utf-8").splitlines() if placeholder.search(line)]
    check(not hits, f"{name} has no placeholders", f"{name} contains placeholder(s): {hits[:2]}")

print()
if errors:
    print(f"FAILED: {len(errors)} of {checks} checks failed.")
    sys.exit(1)
print(f"PASSED: all {checks} checks passed.")
