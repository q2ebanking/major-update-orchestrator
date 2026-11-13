#!/usr/bin/env python3
"""Dependency-free structural checks for the Codex plugin package."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parents[1]
MANIFEST = ROOT / ".codex-plugin" / "plugin.json"
MARKETPLACE = REPO.parent / ".agents" / "plugins" / "marketplace.json"
errors: list[str] = []


def check(condition: bool, message: str) -> None:
    if condition:
        print(f"  ok   {message}")
    else:
        print(f"  FAIL {message}")
        errors.append(message)


def load_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path.relative_to(REPO)} is not valid JSON: {exc}")
        return {}
    if not isinstance(data, dict):
        errors.append(f"{path.relative_to(REPO)} must contain a JSON object")
        return {}
    return data


print("== Codex plugin manifest ==")
manifest = load_json(MANIFEST)
for field in ("name", "version", "description", "skills", "author", "interface"):
    check(field in manifest, f"manifest has {field}")
check(manifest.get("name") == ROOT.name, "manifest name matches package directory")
check(manifest.get("skills") == "./skills/", "manifest declares ./skills/")
check(
    isinstance(manifest.get("author"), dict) and bool(manifest["author"].get("name")),
    "manifest has author name",
)
interface = manifest.get("interface", {})
check(
    isinstance(interface, dict)
    and all(interface.get(key) for key in ("displayName", "shortDescription", "longDescription", "developerName", "category")),
    "manifest has required interface fields",
)
check(isinstance(interface.get("capabilities"), list) and bool(interface["capabilities"]), "manifest has capabilities")
check(
    isinstance(interface.get("defaultPrompt"), list) and 1 <= len(interface["defaultPrompt"]) <= 3,
    "manifest has one to three starter prompts",
)

print("== skill ==")
skill = ROOT / "skills" / "orchestrate-update" / "SKILL.md"
contents = skill.read_text(encoding="utf-8") if skill.is_file() else ""
frontmatter = re.match(r"^---\n(.*?)\n---", contents, re.DOTALL)
check(frontmatter is not None, "skill has YAML frontmatter")
if frontmatter:
    check(re.search(r"^name:\s*\S+", frontmatter.group(1), re.MULTILINE) is not None, "skill frontmatter has name")
    check(re.search(r"^description:\s*\S+", frontmatter.group(1), re.MULTILINE) is not None, "skill frontmatter has description")
references = re.findall(r"references/([A-Za-z0-9.-]+\.md)", contents)
check(bool(references), "skill declares references")
for reference in sorted(set(references)):
    check((skill.parent / "references" / reference).is_file(), f"reference exists: {reference}")

print("== phase-entry skill discovery ==")
discovery = skill.parent / "references" / "skill-discovery.md"
discovery_contents = discovery.read_text(encoding="utf-8") if discovery.is_file() else ""
check("phase-entry skill table" in contents, "skill requires a phase-entry skill table")
check("assistive candidates" in contents, "skill requires an assistive-skill scan")
check("## Assistive skill scan" in discovery_contents, "discovery guide defines the assistive-skill scan")
check("## Phase-entry skill table" in discovery_contents, "discovery guide defines the phase-entry table")
check("request_user_input" in discovery_contents, "discovery guide resolves ambiguous skill matches with user input")

print("== marketplace ==")
marketplace = load_json(MARKETPLACE)
entries = marketplace.get("plugins", [])
entry = next((item for item in entries if isinstance(item, dict) and item.get("name") == ROOT.name), None)
check(isinstance(entry, dict), "marketplace includes the plugin")
if isinstance(entry, dict):
    check(
        entry.get("source") == {
            "source": "local",
            "path": "./codex-plugin/plugins/major-update-orchestrator",
        },
        "marketplace source resolves to package",
    )
    check(
        entry.get("policy") == {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
        "marketplace has installation policy",
    )
    check(bool(entry.get("category")), "marketplace has category")

print("== placeholders ==")
for path in ROOT.rglob("*"):
    if path.is_file() and path.suffix in {".md", ".json", ".py"}:
        todo_marker = "[TODO" + ":"
        check(todo_marker not in path.read_text(encoding="utf-8"), f"no TODO marker in {path.relative_to(ROOT)}")

if errors:
    print(f"FAILED: {len(errors)} check(s) failed.")
    sys.exit(1)
print("PASSED: Codex package is structurally valid.")
