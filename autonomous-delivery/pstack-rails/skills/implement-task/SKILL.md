---
name: implement-task
description: >-
  Pick up a filed ticket and own it until it is verified in production: read
  it from the tracker, check it has goals and acceptance criteria, move it to
  in progress, plan its verification, run /pstack:poteto-mode with the
  ticket as the request, write
  pstack's design changes back into it, link the PRs, then land, deploy and
  QA the change through `pstack-rails:ship-task`. Use when someone says
  "implement <KEY>", "pick up this ticket" or "build this task", or pastes a
  ticket key and expects code.
---

# Picking up a ticket

The ticket says what and why; pstack decides how. This skill is the hand-off
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
| **Goals** or **Acceptance criteria** is missing or empty | which one; offer to fill it in with `pstack-rails:create-task`. The other sections may be thin; pstack fills them in |
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

## 3. Plan the verification

Run `pstack-rails:plan-verification <KEY>`. It reads the ticket and the code,
picks the methods the change needs (driving the real surface, a TLA+ model,
a code verifier, property tests, mutation testing, contract tests, visual
diff), and writes the plan into the ticket with a reason for each method it
skips. A ticket that already has a plan keeps it, checked against the code
as it is now.

Done when the ticket's Tech decisions hold a Verification plan.

## 4. Hand it to pstack

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
- Be fully autonomous. Done means every acceptance criterion is proven on
  the last stage this repo deploys to, not that a PR is open. After the PRs
  open, go on through pstack-rails:ship-task: green, an independent verdict,
  merge, deploy and QA on each stage, and a fix for whatever QA finds. Pause
  only where that skill says a person is needed.
- Verify by the ticket's Verification plan (in Tech decisions). Run each
  method it names, in the order it gives: a design method such as a TLA+
  model before the first line of code, the rest before the PR. A
  counterexample or a surviving mutant is a finding: fix the code, never
  weaken the rule. When the work shows a trait the plan missed, add the
  method and update the plan. The PR's Verification section has one bullet
  per planned method: what ran, what it found, what it leaves out.

<the ticket's full description>
```

Replace `<pstack>` with the pstack path the session orders give. pstack
chooses its playbook and skills from there. Stay out of its way: answer what
it asks, and keep the tracker in step with what it does.

## 5. Keep the tracker true

- **A PR opens:** comment the PR links on the ticket and transition to
  `in-review`, unless the tracker's Git automation already did.
- **pstack changes the design** (Functional requirements or Tech decisions):
  rewrite those sections in place, by `pstack-rails:create-task`'s rules
  (current design only; the tracker's history keeps the old text), and
  comment one line per change with its reason. No need to ask first.
- **pstack pushes back on the commitment** (a goal, a non-goal or an
  acceptance criterion): comment the objection, its evidence and the
  alternative on the ticket, tell the user, and wait. On their yes, rewrite
  those sections the same way; on their no, pstack builds to the ticket as
  written. The ticket stays `in-progress` while it waits.
- **pstack stops on something outside the ticket** (access, another team's
  change): comment what it is and who can answer, and transition to
  `blocked`.
- **Merged:** a merge is not done. When the tracker's Git automation moves
  the ticket to `done` on merge, leave it there and say in the QA comment
  what is still unproven. `ship-task` sets the status the evidence supports.

Done when every PR is linked on the ticket and its status matches the PRs.

## 6. Ship it

Run `pstack-rails:ship-task <KEY>` once pstack has opened the ticket's last
PR. Do not end the turn on a PR link. That skill gets the PRs green, verifies and merges
them, deploys and QAs each stage, fixes what QA finds, and removes the
worktrees.

Done when `ship-task` is done: the last stage's QA comment says PASS and the
ticket is `done`.
