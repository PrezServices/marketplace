---
name: implement-task
description: >-
  Pick up a filed ticket and hand it to pstack: read it from the tracker,
  check it has the seven sections, move it to in progress, run
  /pstack:poteto-mode with the ticket as the request, then link the PRs and
  move it to in review. Use when someone says "implement <KEY>", "pick up
  this ticket" or "build this task", or pastes a ticket key and expects code.
---

# Picking up a ticket

The ticket says what and why; pstack decides how. This skill is the hand-off
on either side of pstack's work: it loads the ticket and keeps the tracker
true, and leaves the planning, building and verifying to `/pstack:poteto-mode`.

**Tracker.** Read the **Tracker** section of `.pstack-rails/config.md`, then
the adapter it names in `${CLAUDE_PLUGIN_ROOT}/trackers/`. Every read,
comment and transition below goes through that adapter.

## Input

$ARGUMENTS: a ticket key, optionally the repo to start in.

## 1. Load the ticket

Read it with the adapter: description, status, parent, container, assignee,
links, comments. Stop, with one sentence to the user, when:

| Condition | What you say |
| --- | --- |
| Status is `done` or `cancelled` | it's closed; name who closed it |
| Status is `blocked` | what the blocking comment names |
| Status is `in-progress` and another branch or PR for the key exists | it's already being worked; name the branch or PR, and offer to resume it |
| One of the seven sections, or **Repos covered**, is missing | which one; offer to rewrite it with `pstack-rails:create-task` |
| A task with open sub-tasks | the work is in the sub-tasks; name the first in Slicing order |

Done when the ticket passes every row, or the user chose to resume.

## 2. Mark it started

- Assignee: the human driving the session, resolved through the adapter,
  when it's someone else or no one.
- Transition to `in-progress`, unless it's there already.
- The branch name for the key, from the adapter. Every repo covered uses it.

## 3. Hand it to pstack

Run `/pstack:poteto-mode` with this as the request. When the Skill tool
refuses it, open its `SKILL.md` under the pstack path the session orders give
and follow it.

```
Implement <KEY>: <title>. The ticket below is the request; its Tech
decisions are settled, and anything that contradicts them is raised before
building, never resolved silently in the PR.

- Repos covered: <each repo, with what changes there>. Each is its own repo:
  branch <branch name> and open the PR inside it.
- Each PR description opens with what the PR is for and links <KEY>
  (<link form from the adapter>), then says what changed and how it was
  verified.
- Done means every acceptance criterion is proven.

<the ticket's full description>
```

pstack chooses its playbook and skills from there. Stay out of its way:
answer what it asks, and keep the tracker in step with what it does.

## 4. Keep the tracker true

- **A PR opens:** comment the PR links on the ticket and transition to
  `in-review`, unless the tracker's Git automation already did.
- **pstack stops on something outside the ticket** (a missing decision,
  access, another team's change): comment what it is and who can answer, and
  transition to `blocked`.
- **Scope changes** while building: update the ticket in place, by
  `pstack-rails:create-task`'s rules, in the same session.
- **Merged:** the tracker's Git automation moves it to `done`. When the
  workspace has none, tell the user to move it, and why.

Done when every PR is linked on the ticket and its status matches the PRs.
