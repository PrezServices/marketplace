# Linear

Through the Linear MCP server. Tool and parameter names change between server
versions, so load the schemas once per session (ToolSearch for `linear`) and
use the names the schema shows. The capability names below are stable.

The project config (`.prez-rails/config.md`) gives the **team key** (the `FRO` in
`FRO-123`) and maps each logical status to a Linear workflow state.

## Kinds

| Kind | In Linear |
| --- | --- |
| container | A **Project**. A task names its project; a sub-task inherits it from its parent |
| task | An issue in the team |
| sub-task | A **sub-issue**: an issue whose `parent` is the task |
| bug | An issue with the `Bug` label. A sub-defect is a bug sub-issue of the task QA failed on |

## Operations

**Read.** Get the issue by identifier (`FRO-123`). Linear stores descriptions
as Markdown, so what comes back is what was written. Comments are a separate
list call; read them when a skill asks for the comment history (the
**Curation gap** comment, earlier QA evidence).

**Search.** List issues filtered by team and query text, once with open states
and once with completed and cancelled ones. Search by the component touched,
plus at least one domain keyword.

**Create.** Create an issue with team, title, Markdown description, project,
assignee, and the state the workspace maps to `backlog`. A sub-task sets
`parent` to the task's id. Pass labels by name only after listing the team's
labels; Linear rejects a name that doesn't exist, and creating a label is a
human's call unless the skill says otherwise (`needs-curation` may be created
once, on first use).

**Update the description.** An update sends the whole description. Read
first, send the entire body back, even for a one-line change.

**Comment.** Create a comment on the issue, in Markdown.

**Transition.** Update the issue's `state`. List the team's workflow states
once per session and map names to ids from that list, never from memory.

**Label.** Labels are a set on the issue. Read the current set, then send it
back with the label added or removed. Sending only the new label drops the
others.

**Link.** Use the issue relations the server exposes (related, blocks,
duplicate). If the server version has none, write the related key in the
description's References and say that the link is missing.

**Assignee.** Resolve the human driving the session to a Linear user by email
(list or get users). Never unassigned, never the agent.

**Sprint.** Sprints are **cycles**. Work started in this session goes in the
team's active cycle. Work filed for later stays out of cycles. When the team
has cycles turned off, skip this and say so.

**Branch name.** Linear's suggested branch name for the issue
(`gitBranchName`, lowercase: `fro-123-short-slug`). With the GitHub
integration installed, a branch or PR title that contains the key links the PR
to the issue on its own.

## Traps

- **Git automation moves states for you.** With the GitHub integration, Linear
  can move an issue when a branch is pushed, a PR opens or a PR merges. A skill
  that sets a status reads the current one first and doesn't fight the
  automation: when the merge already moved it to `done` before QA ran, `qa-task`
  says so in its evidence comment instead of moving it back. If merge-to-done
  keeps skipping QA, tell the user that the team's Git automation setting is the
  fix.
- **Projects aren't statuses.** A project has its own status (planned, started,
  completed). Don't add work to a completed or cancelled project; raise it.
- **Identifier is not id.** Most mutations take the UUID. Get it from the read,
  never by guessing from `FRO-123`.
- **Markdown checklists** (`- [ ]`) render as checkboxes. Acceptance criteria
  may use them, but QA records evidence in comments, not by ticking boxes.
