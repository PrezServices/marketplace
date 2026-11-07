---
name: setup
description: >-
  Set up pstack rails in a workspace after installing the plugin: make sure
  pstack itself is installed and its models chosen, then write the project
  config (tracker, repos, forge, deploys, standing orders). Use right after `claude
  plugin install pstack-rails@...`, when the session-start reminder says the
  workspace isn't set up, or to re-run setup after adding a repo.
disable-model-invocation: true
---

# Setting up pstack rails

Run from the workspace root, usually a meta-repo. Everything this writes is
something `/pstack-rails:teardown` knows how to remove; keep it that way.

## 1. Check the workspace

- The current folder is a git repo root. Otherwise stop.
- **One delivery system per workspace.** Look in `.claude/settings.json`
  `enabledPlugins` and at the root for another delivery system's plugin or
  config folder (such as `prez-rails@prezservices` or `.prez-rails/`). When
  one is there, stop and name it; the user tears it down first.
- When `.pstack-rails/config.md` exists, this is a re-run: update in place,
  showing each change, and keep the human-written lines.

## 2. pstack itself

pstack is Cursor's plugin, `pstack@cursor-plugins`. pstack rails declares it
as a dependency, so installing pstack rails installs it, once the
`cursor-plugins` marketplace is added. pstack rails only loads with pstack
present, so a session running this skill already has it.

- Check that `.claude/settings.json` lists `cursor-plugins` under
  `extraKnownMarketplaces` and enables `pstack@cursor-plugins`, so teammates
  get both when they open the workspace. When either is missing, show the
  change and make it on the user's yes.
- When `~/.claude/rules/pstack-models.md` doesn't exist, tell the user to run
  `/pstack:setup-pstack` in the next session: it picks the models and budget
  for each pstack role, per user. A project that needs its own choices puts
  them in `.claude/rules/pstack-models.md`, which wins inside the workspace.

Done when pstack is enabled in `.claude/settings.json` and the user knows
whether the models step is left.

## 3. The project config

Fill `${CLAUDE_PLUGIN_ROOT}/templates/config.md` into `.pstack-rails/config.md`.
Read what the workspace shows (`.gitmodules`, each repo's README and
`CLAUDE.md`, the root `CLAUDE.md`, `.github/workflows/`) and ask the user only
what it can't tell you, one question at a time:

- **Tracker.** Which adapter in `${CLAUDE_PLUGIN_ROOT}/trackers/`, or `none`.
  `none` suits a repo no one team owns, such as a shared platform repo where
  any team adds its own piece: work goes straight to `/pstack:poteto-mode`,
  with no tickets. Propose it when the workspace shows no tracker in use. With
  `none`, write the Adapter line as `none` and drop the keys and the status
  table. Otherwise, the adapter's
  keys. Use the adapter's tools to list the real teams, projects and statuses
  instead of asking the user to type them, and map each logical status from
  what exists. A logical status with no real match stays blank; tell the
  user. When the tracker's tools aren't connected, say which to connect and
  wait.
- **Deploys.** Who triggers: `session` or `user`.
- **Standing orders**, if any.

Done when every section is filled or explicitly `none`, and the user has seen
the file.

## 4. The workspace

Ticket worktrees live in `tickets/<branch>/<repo>/`. Add `tickets/` to
`.gitignore`, showing the change first.

## 5. Land it

Commit on a branch, staging by path (`.pstack-rails/`, `.claude/settings.json`,
`.gitignore`),
and open a PR on the workspace repo. Then tell the user, in three lines: what
was written, that pstack loads from the next session, and that work starts
with `/pstack-rails:create-task` or "implement <KEY>", or, with no tracker,
with `/pstack:poteto-mode`.
