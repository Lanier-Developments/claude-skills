---
name: github-actions-workflows
description: Write, review, and debug GitHub Actions workflows with least-privilege permissions, pinned actions, caching, and safe secret handling. Use when creating or editing files under .github/workflows, fixing a failing or slow CI run, or hardening a pipeline.
---

# GitHub Actions Workflows

## When to use

- Creating a new workflow or reusable workflow, or editing an existing one.
- A run is failing, flaky, slow, or expensive.
- Reviewing a pipeline for security before it goes on a public repo.
- Do NOT use for application code bugs that merely show up in CI; fix those in the code.

## Steps

1. Read the existing workflows and any reusable workflows or composite actions before changing anything, so new work follows the repo's conventions.
2. Set permissions explicitly. Put `permissions: contents: read` at the top level and widen per job only where needed (for example `id-token: write` for OIDC, `packages: write` for publishing).
3. Pin third-party actions to a full commit SHA with a version comment. First-party `actions/*` may use a major tag if the repo's policy allows.
4. Add `concurrency` with `cancel-in-progress: true` for PR builds, and `timeout-minutes` on every job so a hung step cannot burn runner time.
5. Cache dependencies with the built-in cache option of the setup action (`cache: pip`, `cache: npm`, and so on) before reaching for a manual `actions/cache` step.
6. Use a matrix for version or OS coverage, and set `fail-fast: false` when you want every combination reported.
7. Authenticate to clouds with OIDC rather than long-lived keys stored as secrets.
8. Lint before committing: `actionlint` for workflow syntax and `shellcheck` for inline scripts.

## Security checklist

- Never interpolate untrusted input (`github.event.pull_request.title`, branch names, issue bodies) directly into a `run:` script. Pass it through `env:` and reference the environment variable.
- Avoid `pull_request_target` combined with checking out the PR head; that runs untrusted code with write access and secrets.
- Do not echo secrets, and do not pass them to steps from untrusted forks.
- On a public repository, do not attach self-hosted runners to workflows that run fork PRs.
- Keep artifact retention short unless there is a reason to keep them.

## Debugging

- Re-run with debug logging by setting the `ACTIONS_STEP_DEBUG` and `ACTIONS_RUNNER_DEBUG` secrets to `true`.
- Reproduce locally with `act` for simple jobs, accepting that it does not match hosted runners exactly.
- For slow runs, read the per-step timings first, then check cache hit rates and whether jobs that could run in parallel are chained with `needs`.
- For "works locally, fails in CI", compare tool versions and the working directory before suspecting anything exotic.

## Output

The changed workflow files, a short note on what was changed and why, and any follow-up the author must do outside the repo (for example configuring an OIDC trust relationship or a required secret).
