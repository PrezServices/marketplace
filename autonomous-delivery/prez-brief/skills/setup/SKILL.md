---
name: setup
description: >-
  Set up prez brief in a workspace after installing the plugin: write the
  project config (tracker, repos, knowledge base) that ticket writing and
  research need. Use right after `claude plugin install prez-brief@...`, or to
  re-run setup after adding a repo or changing tracker.
disable-model-invocation: true
---

# Setting up prez brief

Run from the workspace root. Everything this writes is something
`/prez-brief:teardown` knows how to remove; keep it that way.

## 1. Check the workspace

- The current folder is a git repo root. Otherwise stop.
- **One ideation plugin per workspace.** When another one's plugin or config
  folder is there, stop and name it. A delivery system (prez rails, pstack
  rails) alongside is expected.
- When `.prez-brief/config.md` exists, this is a re-run: update in place,
  showing each change, and keep the human-written lines.

## 2. The project config

Fill `${CLAUDE_PLUGIN_ROOT}/templates/config.md` into `.prez-brief/config.md`.

- **Tracker.** When the delivery system's config (`.pstack-rails/config.md`,
  `.prez-rails/config.md`) already has a **Tracker** section with a real
  adapter, offer to copy its adapter, keys and `backlog` mapping, so both
  plugins point at the same tracker. Otherwise ask which adapter in
  `${CLAUDE_PLUGIN_ROOT}/trackers/`, list the real teams, projects and
  statuses with its tools instead of asking the user to type them, and map
  `backlog`. When the tracker's tools aren't connected, say which to connect
  and wait. prez brief needs a tracker: with none, say so and stop.
- **Repos.** From `.gitmodules` and each repo's README, or the one repo.
- **Knowledge base.** A folder that is a wiki (a `wiki/` folder, a schema
  `CLAUDE.md`) is proposed; otherwise `none`.

Done when every section is filled or explicitly `none`, and the user has seen
the file.

## 3. Land it

Commit on a branch, staging by path (`.prez-brief/`, `.claude/settings.json`),
and open a PR on the workspace repo. Then tell the user, in two lines: what
was written, and that tickets start with `/prez-brief:create-task` from the
next session.
