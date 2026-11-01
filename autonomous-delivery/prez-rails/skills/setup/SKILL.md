---
name: setup
description: >-
  Set up prez rails in a meta-repo after installing the plugin: write the
  project config (tracker, statuses, hard stops, deploys, knowledge base),
  write a page for every repo from its code and workflows, and prepare the
  workspace (ticket worktrees, submodule settings, OpenSpec). Use right after
  `claude plugin install prez-rails@...`, when the session-start reminder
  says the workspace isn't set up, or to re-run setup after adding a repo or
  changing tracker.
disable-model-invocation: true
---

# Setting up prez rails

Run from the meta-repo root. Everything this writes lives in files
`/prez-rails:teardown` knows how to remove; keep it that way.

## 1. Check the workspace

- The current folder is a git repo root with a `.gitmodules`. Otherwise stop:
  prez rails runs on a meta-repo.
- **One delivery system per workspace.** Look in `.claude/settings.json`
  `enabledPlugins` and at the root for another delivery system's plugin or
  config folder. When one is there, stop and name it; the user tears it down
  first.
- When `.prez-rails/config.md` exists, this is a re-run: update in place,
  showing each change, and keep the human-written lines.

## 2. The project config

Fill `${CLAUDE_PLUGIN_ROOT}/templates/config.md` into `.prez-rails/config.md`.
Ask the user only what the workspace can't tell you, one question at a time:

- **Tracker.** Which adapter, then its keys. Use the adapter's tools to list
  the real teams, projects and statuses instead of asking the user to type
  them, and map each logical status from what exists. A logical status with
  no real match stays blank; tell the user, and offer the one-line fix in the
  tracker (a missing `ready` status is the common one). When the tracker's
  tools aren't connected, say which to connect and wait.
- **Hard stops.** The rails' list applies everywhere. Propose additions from
  what the repos show (a payments module, a public SDK) and let the user pick.
- **Deploys.** Who triggers: `session` or `user`.
- **Knowledge base.** A submodule that is a wiki (a `wiki/` folder, a schema
  `CLAUDE.md`) is proposed; otherwise `none`.

Done when every section is filled or explicitly blank, and the user has seen
the file.

## 3. The repo pages

For every submodule, fill `${CLAUDE_PLUGIN_ROOT}/templates/repo-page.md` into
`.prez-rails/repos/<repo>.md` from what the repo shows: its `CLAUDE.md` and
`AGENTS.md`, its manifest scripts, `.github/workflows/` (CI gates, the review
bot and its stance, the deploy trigger and steps), its hosting config. Run
`rails-sync` first so you read current `main`. With more than three repos,
brief one subagent per repo with the template and these sources.

Every line is something read in the repo, with the file it came from where a
reader would want to check. What the repo doesn't show (a test identity, a
platform the workflows don't name) is written as `unknown: <what to find
out>`, never guessed. Deploy and QA must say plainly when the only environment
is production.

Done when every submodule has a page and every `unknown` is listed for the
user.

## 4. The workspace

Show each change, then make it:

- `.gitmodules`: each submodule gets `branch = main`, `update = merge` and
  `ignore = all`, so `rails-sync` can track the latest `main` without the
  pointers showing up as changes.
- `.gitignore`: `tickets/`.
- OpenSpec, for changes spanning repos: when the root has no `openspec/`,
  copy `${CLAUDE_PLUGIN_ROOT}/templates/openspec-config.yaml` to
  `openspec/config.yaml` and create `openspec/specs/` and
  `openspec/changes/archive/` with a `.gitkeep` each. A change inside one repo
  goes in that repo's own `openspec/`.

## 5. Land it

Commit on a branch, staging by path, and open a PR on the meta-repo. Then tell
the user, in four lines: what was written, the `unknown`s to fill, that the
rails load from the next session on, and that the first ticket starts with
`/prez-rails:create-task` or "implement <KEY>".
