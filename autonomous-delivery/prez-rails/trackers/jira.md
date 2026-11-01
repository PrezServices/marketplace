# Jira

Through the Atlassian MCP server. The project config (`.prez-rails/config.md`) gives the
**cloud id** (`<site>.atlassian.net`), the **project key**, the **board id**,
and maps each logical status to a Jira status.

## Kinds

| Kind | In Jira |
| --- | --- |
| container | An **Epic**. A task's `parent` is the epic |
| task | Issue type `Task` |
| sub-task | Issue type `Sub-task`, whose `parent` is the task |
| bug | Issue type `Bug`. A sub-defect is the project's sub-task bug type (often `Sub-defect` or `Sub-bug`) under the task QA failed on |

## Operations

**Read.** `getJiraIssue` with `responseContentFormat: "markdown"`, asking
for `description`, `status`, `labels`, `parent`, `assignee`, `issuelinks` and,
when a skill needs history, `comment`.

**Search.** JQL through `searchJiraIssuesUsingJql`: `project = <KEY> AND text
~ "<keyword>"`, without a status filter, so closed issues show up too.

**Create.** `getJiraIssueTypeMetaWithFields` first; take option values only
from `allowedValues`. Then `createJiraIssue` with `contentFormat:
"markdown"`.

**Update the description.** `editJiraIssue` **replaces the whole
description**. Read it first, send the entire body, even for one line.

**Comment.** `addCommentToJiraIssue`, `contentFormat: "markdown"`.

**Transition.** `getTransitionsForJiraIssue` for the ids (they're stable, but
check once per session), then `transitionJiraIssue`.

**Label.** `labels` is an array on the issue. Read it, then send the whole
array with the change.

**Link.** `createIssueLink`, default type `Relates`.

**Assignee.** `lookupJiraAccountId` from the human's email.

**Sprint.** The active sprint on the board is the open one; the workspace may
name a prefix to tell team sprints apart. Work started in this session goes in
it as part of the create; work filed for later stays in the backlog. **Never
send `Sprint` on a sub-task**: Jira rejects it, and sub-tasks inherit the
parent's sprint.

**Branch name.** `<KEY>-<short-slug>` (`ABC-123-short-slug`). Jira's
development panel links branches and PRs whose names carry the key.

## Traps

- The Atlassian MCP can't upload attachments. Hand a rendered diagram to the
  user to attach.
- Don't create work under an epic whose status is a done, cancelled or
  archived one; raise it. When the epic is in its backlog status, creating its
  first task moves it to its in-progress status in the same action.
- A sub-task's work must belong to its task's epic. When it doesn't, it isn't a
  sub-task of that task.
