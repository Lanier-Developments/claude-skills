#!/usr/bin/env python3
"""Validate every skill under skills/.

Stdlib only, so it runs anywhere (laptop, CI) with no install step.
Exit code 1 if any error is found; warnings do not fail the run.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MAX_NAME = 64
MAX_DESC = 1024

# Things that should never be committed to a public skills repo.
SENSITIVE = [
    (re.compile(r"\b\d{3}[-.]\d{3}[-.]\d{4}\b"), "phone-number-like string"),
    (re.compile(r"\b(sk|pk)[-_][A-Za-z0-9]{20,}\b"), "API-key-like string"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS access key id"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private key block"),
    (re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), "SSN-like string"),
]


def parse_frontmatter(text: str) -> tuple[dict[str, str] | None, str]:
    """Parse simple `key: value` frontmatter. Returns (fields, error)."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, "file must start with a '---' frontmatter line"
    try:
        end = lines[1:].index("---") + 1
    except ValueError:
        return None, "frontmatter is not closed with '---'"
    fields: dict[str, str] = {}
    for raw in lines[1:end]:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if ":" not in raw:
            return None, f"unparseable frontmatter line: {raw!r}"
        key, _, value = raw.partition(":")
        fields[key.strip()] = value.strip()
    return fields, ""


def check_skill(skill_dir: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    md = skill_dir / "SKILL.md"
    if not md.is_file():
        return [f"{skill_dir.name}: missing SKILL.md"], warnings

    text = md.read_text(encoding="utf-8")
    fields, err = parse_frontmatter(text)
    if fields is None:
        return [f"{skill_dir.name}: {err}"], warnings

    name = fields.get("name", "")
    desc = fields.get("description", "")

    if not name:
        errors.append(f"{skill_dir.name}: frontmatter 'name' is missing")
    else:
        if not NAME_RE.match(name):
            errors.append(f"{skill_dir.name}: name {name!r} must be lowercase kebab-case")
        if len(name) > MAX_NAME:
            errors.append(f"{skill_dir.name}: name longer than {MAX_NAME} chars")
        if name != skill_dir.name:
            errors.append(f"{skill_dir.name}: name {name!r} must match the folder name")
        if "claude" in name or "anthropic" in name:
            errors.append(f"{skill_dir.name}: name must not contain 'claude' or 'anthropic'")

    if not desc:
        errors.append(f"{skill_dir.name}: frontmatter 'description' is missing")
    else:
        if len(desc) > MAX_DESC:
            errors.append(f"{skill_dir.name}: description is {len(desc)} chars (max {MAX_DESC})")
        if "<" in desc or ">" in desc:
            errors.append(f"{skill_dir.name}: description must not contain angle brackets")
        if not re.search(r"\b(use when|use for|use this|when)\b", desc, re.I):
            warnings.append(f"{skill_dir.name}: description should say WHEN to use the skill")

    body = text.split("---", 2)[-1].strip()
    if len(body.splitlines()) < 5:
        warnings.append(f"{skill_dir.name}: body is very short")

    for path in skill_dir.rglob("*"):
        if not path.is_file() or path.suffix in {".png", ".jpg", ".gif", ".pdf"}:
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern, label in SENSITIVE:
            if pattern.search(content):
                errors.append(f"{path.relative_to(ROOT)}: contains {label}")

    return errors, warnings


def main() -> int:
    if not SKILLS.is_dir():
        print("no skills/ directory found", file=sys.stderr)
        return 1

    all_errors: list[str] = []
    all_warnings: list[str] = []
    checked = 0
    for skill_dir in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        if skill_dir.name.startswith("_"):
            continue  # templates / private scratch dirs
        checked += 1
        errs, warns = check_skill(skill_dir)
        all_errors += errs
        all_warnings += warns

    for w in all_warnings:
        print(f"warning: {w}")
    for e in all_errors:
        print(f"error:   {e}")
    print(f"checked {checked} skill(s): {len(all_errors)} error(s), {len(all_warnings)} warning(s)")
    return 1 if all_errors else 0


if __name__ == "__main__":
    sys.exit(main())
