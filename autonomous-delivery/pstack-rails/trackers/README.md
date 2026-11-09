# Trackers

The ticket skills (`create-task`, `implement-task`) describe *what* to do
with a ticket. *How* to do it in a given
tracker lives in one adapter file here. The workspace picks the adapter in the
**Tracker** section of `.pstack-rails/config.md`, together with the values only the
workspace knows: the team or project key, and the real name of each status.

Before a skill's first tracker call in a session, read the **Tracker**
section of `.pstack-rails/config.md` and then the adapter it names. When the two
disagree, the project config wins.

| Adapter | Tracker |
| --- | --- |
| [`linear.md`](linear.md) | Linear, through the Linear MCP |
| [`jira.md`](jira.md) | Jira Cloud, through the Atlassian MCP |
| [`github-issues.md`](github-issues.md) | GitHub Issues and Projects, through `gh` |

## The vocabulary the skills use

### Kinds

| Kind | What it is |
| --- | --- |
| **container** | The body of work a task belongs to: a Jira Epic, a Linear Project, a GitHub parent issue or milestone |
| **task** | One unit of work, built in one PR per repo, or split into sub-tasks |
| **sub-task** | One slice of a task, one PR. Its work belongs to its task's container |
| **bug** | A defect in shipped behaviour. A bug found while QA-ing a task is a sub-defect: a bug whose parent is that task |

### Statuses

The skills move tickets between these logical statuses. The workspace maps each
one to the tracker's real status name. A logical status the workspace leaves
unmapped is skipped, and the skill says so instead of inventing one.

| Logical status | Meaning | Who moves a ticket there |
| --- | --- | --- |
| `backlog` | Filed, not started | `create-task` |
| `ready` | Curated: pstack designed it and the author has nothing open | `curate-task` |
| `in-progress` | pstack is working on it | `implement-task` |
| `in-review` | A PR is open | `implement-task`, or the tracker's Git automation |
| `done` | Merged | the tracker's Git automation, or a human |
| `blocked` | Waiting on something outside the ticket | anyone, with a comment naming what |
| `cancelled` | Not doing it | a human |

### Operations

Every adapter says how to do each of these, and what goes wrong:

- **read** a ticket: description as Markdown, status, labels, parent, container,
  assignee, relations, comments
- **search**, for duplicates, open and closed
- **create** a task, sub-task or bug, with container or parent, assignee and
  sprint or cycle
- **update the description**: whether it replaces the whole body
- **comment**
- **transition** to a status
- **label**: add and remove
- **link** two tickets
- **resolve the assignee** from the human's email
- **current sprint or cycle**
- **branch name** for a key, and how PRs get linked back

## Adding a tracker

Write `<tracker>.md` with one section per operation above, plus a **Traps**
section. Add a row to the table at the top. Then a workspace can name it.
