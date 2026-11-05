# GitHub Issues

Through `gh`. The project config (`.prez-brief/config.md`) names the **repo that holds the
issues** (`<owner>/<repo>`, often the meta-repo) and, when statuses live in a
Project, the **project number** and its status field. Without a Project,
statuses are labels named `status:<name>`.

## Kinds

| Kind | In GitHub |
| --- | --- |
| container | A **parent issue** with sub-issues, or a **milestone** when the workspace says so |
| task | An issue |
| sub-task | A **sub-issue** of the task |
| bug | An issue with the `bug` label. A sub-defect is a bug sub-issue of the task it was found in |

## Operations

**Read.** `gh issue view <n> -R <repo> --json
title,body,state,labels,assignees,milestone,comments`. Sub-issues and the
parent: `gh api repos/<repo>/issues/<n>/sub_issues` and `.../parent`.

**Search.** `gh issue list -R <repo> --state all --search "<keyword>"`.

**Create.** `gh issue create -R <repo> --title ... --body-file <file>
--assignee ... --label ...`. For a sub-task, add it afterwards with `gh api -X
POST repos/<repo>/issues/<parent>/sub_issues -F sub_issue_id=<issue id>`. That
takes the numeric `id`, not the issue number.

**Update the description.** `gh issue edit <n> --body-file <file>` replaces
the body. Read it first and send all of it.

**Comment.** `gh issue comment <n> --body-file <file>`.

**Transition.** With a Project: `gh project item-edit` on the status field
(ids from `gh project field-list`). Without one: swap the `status:*` label.
`done` and `cancelled` also close the issue (`gh issue close`, with `--reason
"not planned"` for `cancelled`).

**Label.** `gh issue edit <n> --add-label` / `--remove-label`. Create a missing
label once with `gh label create`.

**Link.** Write `Relates to #<n>` in a comment. GitHub has no typed relation
other than sub-issues and closing keywords.

**Assignee.** GitHub logins, not emails. Ask the human for theirs once, if
`gh api user` isn't them.

**Sprint.** An iteration field on the Project, when there is one. Otherwise
skip this and say so.

**Branch name.** `<n>-<short-slug>`. A PR body with `Closes <repo>#<n>`
links it, and closes the issue on merge.

## Traps

- **`Closes #n` closes on merge.** Use it when merging is done; use `Refs #n`
  for a PR that is one slice of the issue.
- Issues in a meta-repo are referenced from sub-repo PRs as `<owner>/<repo>#<n>`;
  a bare `#n` points at the sub-repo's own issues.
