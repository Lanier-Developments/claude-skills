# claude-skills

A single, version-controlled home for my Claude skills, kept in sync across every machine I work on.

Skills are small folders of instructions (plus optional scripts and reference files) that Claude loads when a task matches. Left on one laptop they drift, get lost, and can't be reviewed. This repo treats them like any other shared engineering asset: reviewed, validated, versioned, and installed the same way everywhere.

## Layout

```
skills/
  _template/                   copy this to start a new skill (ignored by tooling)
  mcp-permission-review/       example: audit an MCP server's blast radius
  commit-message-conventions/  example: Conventional Commits helper
scripts/
  install.sh                   link or copy skills into ~/.claude/skills
  validate.py                  lint every skill (stdlib only)
.github/workflows/validate.yml CI: validate, shellcheck, installer dry run
docs/design-decisions.md       why it is built this way
```

## Use it on a new machine

```bash
git clone <this-repo> ~/Projects/claude-skills
cd ~/Projects/claude-skills
scripts/install.sh            # symlinks skills/* into ~/.claude/skills
```

After that, `git pull` updates every skill on the machine at once. Useful flags:

- `--copy` copies instead of symlinking (for machines where the repo won't stay put)
- `--force` replaces an existing skill of the same name
- `--dry-run` shows what would happen
- `--target DIR` (or `CLAUDE_SKILLS_DIR`) installs somewhere other than `~/.claude/skills`

## Add a skill

1. `cp -R skills/_template skills/my-skill-name`
2. Edit `SKILL.md`. The `name` must match the folder and be lowercase kebab-case. The `description` must say what the skill does and when to use it, because that text is what Claude reads to decide whether to load it.
3. Run `python3 scripts/validate.py`.
4. Open a PR. CI runs the same checks.

## What the validator enforces

- `SKILL.md` exists with well-formed frontmatter
- `name` is kebab-case, at most 64 characters, matches its folder, and avoids reserved words
- `description` is present, at most 1024 characters, has no angle brackets, and says when to use the skill (warning if not)
- No secrets or personal identifiers slip in: API-key patterns, private keys, phone numbers, SSN-like strings

## Public versus private skills

This repo is meant to be shown, so it holds only skills that are safe to publish. Anything with client details, personal data, or employer-specific content stays out: put it in `skills/_private/` (ignored by the installer and validator) or, better, a separate private repo installed with `--target`. `private/` is also in `.gitignore`.

## Design notes

See [docs/design-decisions.md](docs/design-decisions.md) for the reasoning: symlinks versus copies, why the validator is dependency-free, how skills are scoped and tested.

## License

MIT
# claude-skills
