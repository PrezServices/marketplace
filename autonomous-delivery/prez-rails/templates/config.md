# prez-rails config

The project's own facts for prez rails. Written by `/prez-rails:setup`; edit it
by hand or re-run setup. Removed by `/prez-rails:teardown`.

## Tracker

- **Adapter:** `<linear | jira | github-issues>` (`${CLAUDE_PLUGIN_ROOT}/trackers/<adapter>.md`)
- <the adapter's keys: Linear team key; Jira cloud id, project key, board id; GitHub issues repo and project number>

| Logical status | Status in the tracker |
| --- | --- |
| `backlog` | |
| `ready` | |
| `in-progress` | |
| `in-review` | |
| `ready-to-deploy` | |
| `done` | |
| `blocked` | |
| `cancelled` | |

A status left blank is skipped by the skills, which say so.

## Hard stops

In addition to the rails' list:

- <project-specific hard stops, or "none">

## Deploys

- **Go:** `<session | user>`. `session`: the session triggers deploys that need
  a trigger. `user`: the session prepares them and waits for an explicit go.
  Merging a PR is always a human's call.

## Knowledge base

- **Path:** `<folder, e.g. brain/>`, with its schema in `<file>`, or `none`.

## Repos

| Repo | Page |
| --- | --- |
| `<repo>` | [`repos/<repo>.md`](repos/<repo>.md) |
