---
name: commit-message-conventions
description: Write or rewrite git commit messages in Conventional Commits style with a clear subject and a body explaining why. Use when asked to commit changes, draft a commit message, clean up commit history, or write a PR description from a diff.
---

# Commit Message Conventions

## When to use

- The user asks for a commit message, a squash message, or a PR summary.
- Reviewing a branch whose history needs tidying before merge.

## Steps

1. Read the staged diff (or the commits in range) before writing anything.
2. Pick the type: feat, fix, docs, refactor, test, chore, ci, or perf. Add a scope in parentheses if one area dominates.
3. Write the subject: imperative mood, no trailing period, 72 characters or fewer.
4. Write the body only when the reason is not obvious from the diff. Explain why the change was made and any trade-off, not a line-by-line restatement.
5. Note breaking changes with a `BREAKING CHANGE:` footer.

## Output

A commit message in this shape:

```
type(scope): short imperative summary

Why this change was needed, and anything a reviewer should know.
```

## Notes

- One logical change per commit. If the diff mixes concerns, suggest splitting it.
- Follow any attribution or trailer rules the project or environment specifies.
