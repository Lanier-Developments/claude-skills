---
name: mcp-permission-review
description: Review an MCP server's tool list and configuration for over-broad permissions and estimate its blast radius. Use when asked to vet, audit, or approve an MCP server, or before connecting a new MCP server to an agent that can act on real systems.
---

# MCP Permission Review

## When to use

- Someone asks "is this MCP server safe to connect?" or wants an audit before adoption.
- A new server is being added to an agent that has write access to files, repos, mail, or infrastructure.
- Do NOT use for general code review of the server's implementation; this skill covers what the *agent* is allowed to do through it.

## Steps

1. Inventory every tool the server exposes: name, description, and input schema.
2. Classify each tool as read, write, delete, execute, or network/egress. Anything that can both read private data and send data outward is flagged as an exfiltration path.
3. Check the credentials and scopes the server runs with. Compare granted scopes to what the listed tools actually need; note every excess scope.
4. Identify which tool descriptions or returned content could carry untrusted text (web pages, emails, tickets). Those are prompt-injection entry points.
5. Estimate blast radius: if the agent misused the single most powerful tool, what is the worst reachable outcome, and is it reversible?
6. Recommend the smallest change that shrinks the radius: drop scopes, disable tools, require confirmation on write/delete/execute, or split into read-only and write servers.

## Output

A short report with: a table of tools by class, a list of excess permissions, the injection entry points, a blast-radius statement in one or two sentences, and a prioritized list of recommended changes.

## Notes

- Judge from the evidence you can see (schemas, config). If a scope or behavior can't be verified, say so rather than assuming.
- Keep the report to what a reviewer can act on in one sitting.
