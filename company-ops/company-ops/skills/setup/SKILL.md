---
name: setup
description: >-
  Set up company-ops in a workspace after installing the plugin: check the
  plugin is enabled, then write the company config (entities, knowledge
  base, CRM adapter and stage map, document conventions, standing orders)
  and open a PR with it. Use right after `claude plugin install
  company-ops@...`, when a company-ops skill says the workspace isn't set
  up, or to re-run setup after the company's facts change.
disable-model-invocation: true
---

# Setting up company-ops

Run from the workspace root. Everything this writes is something
`/company-ops:teardown` knows how to remove; keep it that way.

## 1. Check the workspace

- The current folder is a git repo root. Otherwise stop.
- `.claude/settings.json` lists `prezservices` under `extraKnownMarketplaces`
  and enables `company-ops@prezservices`, so teammates get the plugin when
  they open the workspace. When one is missing, show the change and make it
  on the user's yes.
- When `.company-ops/config.md` exists, this is a re-run: update in place,
  showing each change, and keep the human-written lines.

## 2. The company config

Fill `${CLAUDE_PLUGIN_ROOT}/templates/config.md` into `.company-ops/config.md`.
Read what the workspace shows before asking anything, and ask the user only
what it can't tell you, one question at a time.

- **Entities.** The knowledge base's pages on the company, its legal form
  and its shareholders, and `.pstack-rails/config.md` when it exists. One row
  per entity with its role. Ask for a legal form or country the pages don't
  state.
- **Knowledge base.** The path `.pstack-rails/config.md` names under
  **Knowledge base**, or the wiki folder a repo README points at. Ask when
  neither exists.
- **CRM.** List the adapters in `${CLAUDE_PLUGIN_ROOT}/crms/` and offer
  them plus `none`. Propose `none` when no CRM tools are connected to the
  session and the knowledge base names no CRM. With a real adapter, read
  its file, then use the CRM's own tools to list the workspace, its members
  and the deal stages that exist, and map each logical stage from that list.
  A logical stage with no real match stays blank; tell the user. The default
  owner is the human driving the session, resolved by email. When the CRM's
  tools aren't connected, say which to connect and wait.
- **Documents and Conventions.** Fixed text from the template. Change a line
  only when the user says so.
- **Standing orders**, if any.

Done when every section is filled or explicitly `none`, and the user has seen
the file.

## 3. Land it

Commit on a branch, staging by path (`.company-ops/`, `.claude/settings.json`),
and open a PR on the workspace repo. Then tell the user, in three lines:
what was written, that it applies from the next session, and that a roadmap
starts with `/company-ops:create-roadmap <topic>`.
