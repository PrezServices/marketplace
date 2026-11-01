---
name: teardown
description: >-
  Remove prez rails from a meta-repo before uninstalling the plugin or
  switching to another delivery system: close or keep the ticket worktrees,
  then remove the project config, repo pages and workspace changes that
  setup made. Use when the user wants to uninstall prez rails, switch
  delivery system, or try a different one.
disable-model-invocation: true
---

# Tearing down prez rails

Run from the meta-repo root. Teardown removes what `/prez-rails:setup` wrote,
and nothing else.

## 1. Open work first

List `tickets/*/*`. Each worktree may hold unpushed commits. For each one,
show its branch and `git -C <worktree> status --short` plus unpushed commits,
and let the user choose: close it (`rails-close-ticket <branch>`, after
pushing) or keep it. Kept worktrees stay where they are, and `tickets/` stays
in `.gitignore`.

Done when every worktree is closed or explicitly kept.

## 2. Show the removal

One list, before touching anything:

- `.prez-rails/`, the whole folder. Offer to keep the repo pages somewhere
  neutral first (for example `docs/repos/`) when the next delivery system
  could use them.
- The `tickets/` line in `.gitignore`, unless worktrees were kept.
- `openspec/`, only when it holds no change outside `changes/archive/`. A live
  change is the user's call.
- In `.gitmodules`, the `update = merge` and `ignore = all` keys setup added.
  They're harmless to keep; ask.

## 3. Remove and land

Make the removals the user agreed to, commit on a branch staging by path, and
open a PR on the meta-repo.

## 4. Uninstall

Give the user the command, to run themselves:

```sh
claude plugin uninstall prez-rails@prezservices --scope project
```

The rails stop loading from the next session. The guard hooks already stand
down once `.prez-rails/config.md` is gone.
