# prez-brief config

The project's own facts for prez brief. Written by `/prez-brief:setup`; edit
it by hand or re-run setup. Removed by `/prez-brief:teardown`.

## Tracker

- **Adapter:** `<linear | jira | github-issues>` (`${CLAUDE_PLUGIN_ROOT}/trackers/<adapter>.md`)
- <the adapter's keys: Linear team key; Jira cloud id, project key, board id; GitHub issues repo and project number>

| Logical status | Status in the tracker |
| --- | --- |
| `backlog` | |

prez brief files tickets in `backlog`; the delivery system moves them on.

## Repos

What a ticket's **Repos covered** names.

| Folder | Repo | What it is |
| --- | --- | --- |
| `<folder>` | `<owner/repo>` | <one line> |

## Knowledge base

- **Path:** `<folder, e.g. brain/>`, with its schema in `<file>`, or `none`.
