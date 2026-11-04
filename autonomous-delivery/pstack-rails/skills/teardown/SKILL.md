---
name: teardown
description: >-
  Remove pstack rails from a workspace before uninstalling the plugin or
  switching to another delivery system: remove the project config setup
  wrote, and optionally pstack itself. Use when the user wants to uninstall
  pstack rails, switch delivery system, or try a different one.
disable-model-invocation: true
---

# Tearing down pstack rails

Run from the workspace root. Teardown removes what `/pstack-rails:setup`
wrote, and nothing else.

## 1. Open work first

List `tickets/*/*`. Each worktree may hold unpushed commits. For each one,
show its branch, `git -C <worktree> status --short` and unpushed commits, and
let the user choose: remove it (after pushing) or keep it. Kept worktrees
stay, and so does the `tickets/` line in `.gitignore`.

## 2. Show the removal

One list, before touching anything:

- The `tickets/` line in `.gitignore`, unless worktrees were kept.
- `.pstack-rails/`, the whole folder. Offer to keep the repos table and
  standing orders somewhere neutral first when the next delivery system could
  use them.
- pstack itself: the `pstack@cursor-plugins` entry in `enabledPlugins` and the
  `cursor-plugins` entry in `extraKnownMarketplaces` of `.claude/settings.json`.
  Ask: the user may keep pstack without the rails.
- `.claude/rules/pstack-models.md`, when setup's user put one there. Ask.

## 3. Remove and land

Make the removals the user agreed to, commit on a branch staging by path, and
open a PR on the workspace repo.

## 4. Uninstall

Give the user the commands, to run themselves:

```sh
claude plugin uninstall pstack-rails@prezservices --scope project
claude plugin uninstall pstack@cursor-plugins --scope project   # only when pstack goes too
```

The hooks already stand down once `.pstack-rails/config.md` is gone. Run
teardown before uninstalling: once the plugin is gone, so is this skill.
