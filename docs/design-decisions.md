# Design decisions

## Why a repo at all

Skills are executable-adjacent instructions: they change how an agent behaves. That makes them worth the same controls as code. A repo gives history (what changed and why), review (a second pair of eyes before a skill goes everywhere), and a single source of truth so two machines never disagree about what a skill says.

## Symlink by default, copy on request

`install.sh` symlinks each skill into `~/.claude/skills`. Edits in the repo apply immediately and `git pull` updates everything with no reinstall step. Copy mode exists for machines where the repo directory isn't stable or where a symlink would be surprising. The installer never overwrites an existing skill without `--force`, and `--dry-run` shows the plan first.

## Description is the interface

Claude decides whether to load a skill from its name and description alone, so those two fields carry the weight. The validator treats a missing "when to use" signal as a warning and a mismatched name as an error. A skill with a vague description is effectively a skill that never fires, or one that fires when it shouldn't.

## Scope each skill narrowly

One skill, one job, with explicit "when to use" and "when not to use" sections. Narrow skills trigger more reliably, are easier to test, and can be composed. The `_template` bakes this structure in so new skills start well.

## Dependency-free validation

`validate.py` uses only the Python standard library and a small frontmatter parser, so it runs on any machine and in CI without a virtualenv or install step. The trade-off is that the parser handles only simple `key: value` frontmatter, which is all the skills here use.

## Guarding against leaks

A public skills repo is an easy place to leak something by accident: a pasted token, a phone number in an example, a client name. The validator scans every file in a skill for common secret and identifier patterns and fails the build. Pattern scanning won't catch everything, so the stronger control is structural: private material lives in an ignored directory or a separate private repo.

## Testing skills

Static checks catch structure, not behavior. Behavior is checked the manual way for now: run the skill on a few representative prompts, including one it should not trigger on, and record what changed. A natural next step is a small evaluation harness that runs a fixed prompt set against each skill and diffs results between versions.

## Possible next steps

- A prompt-based evaluation harness with golden outputs per skill
- A `scripts/list.py` that prints an index of skills and descriptions into the README
- Versioning skills with tags so a machine can pin a known-good set
