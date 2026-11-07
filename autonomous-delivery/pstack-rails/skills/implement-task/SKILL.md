---
name: implement-task
description: >-
  Pick up a filed ticket and hand it to pstack: read it from the tracker,
  check it has goals and acceptance criteria, move it to in progress, run
  /pstack:poteto-mode with the ticket as the request, write pstack's design
  changes back into it, then link the PRs and move it to in review. Use when someone says "implement <KEY>", "pick up
  this ticket" or "build this task", or pastes a ticket key and expects code.
---

# Picking up a ticket

The ticket says what and why; pstack decides how. Tickets follow
`${CLAUDE_PLUGIN_ROOT}/ticket.md`. This skill is the hand-off
on either side of pstack's work: it loads the ticket and keeps the tracker
true, and leaves the planning, building and verifying to `/pstack:poteto-mode`.

**What's fixed and what's open.** Goals, Non-goals and Acceptance criteria are
the commitment, and only the human changes them. Functional requirements and
Tech decisions are the starting design: pstack may change them, as an
engineer curating the ticket would, as long as it writes each change back
into the ticket.

**Tracker.** Read the **Tracker** section of `.pstack-rails/config.md`. When
its adapter is `none` (or missing), this workspace works without tickets:
say so in one line, offer to take the request straight to
`/pstack:poteto-mode`, and stop here. Otherwise read
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
| **Goals** or **Acceptance criteria** is missing or empty | which one; offer to fill it in with `prez-brief:create-task` when prez brief is installed, or ask the filer to. The other sections may be thin; pstack fills them in |
| A task with open sub-tasks | the work is in the sub-tasks; name the first in Slicing order |

Done when the ticket passes every row, or the user chose to resume.

## 2. Mark it started

- Assignee: the human driving the session, resolved through the adapter,
  when it's someone else or no one.
- Transition to `in-progress`, unless it's there already.
- The branch name for the key, from the adapter. Every repo covered uses it.
- A worktree per repo covered, at `tickets/<branch>/<repo>/` from the
  workspace root. Submodule folders stay clean on `main`, and a guard refuses
  edits and git writes inside them. For each repo:

  ```sh
  git -C <repo> fetch origin
  git -C <repo> worktree add ../tickets/<branch>/<repo> <branch>                     # the branch exists locally
  git -C <repo> worktree add --track -b <branch> ../tickets/<branch>/<repo> origin/<branch>  # only on origin
  git -C <repo> worktree add --no-track -b <branch> ../tickets/<branch>/<repo> origin/main   # new
  ```

  A repo pstack finds it needs later gets its worktree the same way.

## 3. Hand it to pstack

Run `/pstack:poteto-mode` with this as the request. When the Skill tool
refuses it, open its `SKILL.md` under the pstack path the session orders give
and follow it.

```
Implement <KEY>: <title>. The ticket below is the request.

- Goals, Non-goals and Acceptance criteria are fixed. When the evidence says
  one of them is wrong, stop before building it: say why, with the evidence
  and the alternative, and wait for the human's call.
- Functional requirements and Tech decisions are a starting design. Change
  them when the code shows a better way; each change goes back into the
  ticket (see below) and into the PR's description.
- Repos covered: <each repo, with what changes there, or "find out" when the
  ticket doesn't say>. Each is its own repo, checked out on <branch name> at
  tickets/<branch>/<repo>/: work, commit and open the PR there. The folder
  <repo>/ at the root stays clean on main.
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
- **pstack changes the design** (Functional requirements or Tech decisions):
  rewrite those sections in place, by the writing rules of
  `${CLAUDE_PLUGIN_ROOT}/ticket.md` (current design only; the tracker's
  history keeps the old text), and
  comment one line per change with its reason. No need to ask first.
- **pstack pushes back on the commitment** (a goal, a non-goal or an
  acceptance criterion): comment the objection, its evidence and the
  alternative on the ticket, tell the user, and wait. On their yes, rewrite
  those sections the same way; on their no, pstack builds to the ticket as
  written. The ticket stays `in-progress` while it waits.
- **pstack stops on something outside the ticket** (access, another team's
  change): comment what it is and who can answer, and transition to
  `blocked`.
- **Merged:** the tracker's Git automation moves it to `done`. When the
  workspace has none, tell the user to move it, and why. Then remove the
  worktrees (`git -C <repo> worktree remove ../tickets/<branch>/<repo>`, after
  checking `git status` there is clean) and the empty `tickets/<branch>/`.

Done when every PR is linked on the ticket and its status matches the PRs.
