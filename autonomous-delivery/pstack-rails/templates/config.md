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

## Tracker

- **Adapter:** `<linear | jira | github-issues | none>` (`${CLAUDE_PLUGIN_ROOT}/trackers/<adapter>.md`)
- <the adapter's keys: Linear team key; Jira cloud id, project key, board id; GitHub issues repo and project number>

With `none`, the workspace works without tickets: requests go straight to
`/pstack:poteto-mode`, and the keys and status table below are removed.

| Logical status | Status in the tracker |
| --- | --- |
| `backlog` | |
| `ready` | |
| `in-progress` | |
| `in-review` | |
| `done` | |
| `blocked` | |
| `cancelled` | |

A status left blank is skipped by the skills, which say so.

## Forge

- **Forge:** `<GitHub (gh) | other>`

## Delivery

A ticket is done when its acceptance criteria are proven on the last stage
below. `pstack-rails:ship-task` reads this section.

- **Merge:** `<session | user>`. `session`: the session merges a PR once it
  is green and an agent that did not write it has verified it. `user`: the
  session gets the PR merge-ready and waits for the merge.
- **Deploy:** `<session | user>`. `session`: the session triggers deploys that
  need a trigger. `user`: the session prepares them and waits for an explicit
  go.
- **Always the person's call:** a deploy or a QA step that messages a
  customer, moves money or deletes data.

One row per repo and stage, lowest stage first. A repo that deploys nowhere
has one row that says so, and its last stage is the merged PR.

| Repo | Stage | How code reaches it | Where it runs | How to QA it | Never drive |
| --- | --- | --- | --- | --- | --- |
| `<repo>` | `<development \| production \| none>` | <on merge to `<branch>`, workflow file; or the dispatch command> | <URL> | <the verify skill, the test identities, what proves the revision> | <flows and identities QA must not touch> |

## Subagents

The `Agent` and `Workflow` guards pass pstack's own agents
(`pstack:poteto-agent`, `pstack:comment-sicko`) and any agent whose prompt
names an installed pstack `SKILL.md`. They also pass each agent type listed
here, and nothing else. List only agents that cannot do the work outside
pstack: read-only ones, or ones that stand in for a tool. The guards match the
name alone, so a project, user or plugin agent defined under a listed name
passes too, with whatever tools it declares.

- `Explore`: a read-only look
- `web-fetch`: reads web pages, for a session with no WebFetch tool of its own

## Standing orders

The operator's orders and gates for this workspace, read before acting. Keep
them short; pstack's playbooks decide the rest.

- <order, or "none">

## Knowledge base

- **Path:** `<folder, e.g. brain/>`, or `none`.
