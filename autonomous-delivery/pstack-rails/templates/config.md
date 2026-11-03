# pstack-rails config

The project's own facts for pstack. Written by `/pstack-rails:setup`; edit it
by hand or re-run setup. Removed by `/pstack-rails:teardown`. pstack decides
how to do the work; this file says what the workspace is.

## Repos

Each folder below is its own repo. Branch, commit and open PRs inside the repo
the change belongs to.

| Folder | Repo | What it is |
| --- | --- | --- |
| `<folder>` | `<owner/repo>` | <one line> |

## Forge and tracker

- **Forge:** `<GitHub (gh) | other>`
- **Tracker:** `<where work is tracked, e.g. Linear team FRO, or none>`

## Deploys

- **Go:** `<session | user>`. `session`: the session triggers deploys that need
  a trigger. `user`: the session prepares them and waits for an explicit go.
  Merging a PR is always a human's call.

## Standing orders

The operator's orders and gates for this workspace, read before acting. Keep
them short; pstack's playbooks decide the rest.

- <order, or "none">

## Knowledge base

- **Path:** `<folder, e.g. brain/>`, or `none`.
