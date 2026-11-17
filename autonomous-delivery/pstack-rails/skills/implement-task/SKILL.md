---
name: implement-task
description: >-
  Pick up a filed ticket and own it until it is verified in production: read
  it from the tracker, check it has goals and acceptance criteria, move it to
  in progress, run /pstack:poteto-mode with the ticket as the request, write
  pstack's design changes back into it, link the PRs, then land, deploy and
  QA the change through `pstack-rails:ship-task`. Use when someone says
  "implement <KEY>", "pick up this ticket" or "build this task", or pastes a
  ticket key and expects code.
---

# Picking up a ticket

The ticket says what and why; pstack decides how. This skill is the hand-off
on either side of pstack's work: it loads the ticket and keeps the tracker
true, and leaves the planning, building and verifying to `/pstack:poteto-mode`.

**You own the ticket to the end.** It is done when its acceptance criteria
are proven on the last stage the repo deploys to, which is production where
one exists. An open PR is the middle. You merge, deploy, QA each stage and
fix what QA finds, without being asked, and stop only where
`pstack-rails:ship-task` says a person is needed.

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
- Be fully autonomous. Done means every acceptance criterion is proven on
  the last stage this repo deploys to, not that a PR is open. After the PRs
  open, go on through pstack-rails:ship-task: green, an independent verdict,
  merge, deploy and QA on each stage, and a fix for whatever QA finds. Pause
  only where that skill says a person is needed.
- Verify before the PR, on the real surface:
  - Run the repo's gates, then drive the change the way a user would with
    the repo's verify skill (.claude/skills/verify-*). A repo with none gets
    one first: follow <pstack>/skills/create-verification-skill/SKILL.md.
  - When the change touches files a formal check covers
    (.claude/skills/verify-formal*, a formal/ folder, a coverage record), run
    that check and read a TLA+ result with pstack's statechart skill.
  - When the change adds or changes a state machine, concurrent writers,
    retries, idempotency, a parser, or money or permission logic that no
    check covers, write the check as part of this ticket: follow
    <pstack>/skills/create-formal-verification-skill/SKILL.md. It picks the
    tool from the question: a model checker such as TLA+ for the order of
    events, a proof or a verifier that runs on the code (Lean, Kani, Verus)
    for every input, and generated-input tests where no verifier runs on the
    language.
  - A counterexample is a finding. Fix the code, never weaken the property.
  - Say in the PR what each check covers and what it leaves out.

<the ticket's full description>
```

Replace `<pstack>` with the pstack path the session orders give. pstack
chooses its playbook and skills from there. Stay out of its way: answer what
it asks, and keep the tracker in step with what it does.

## 4. Keep the tracker true

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

## 5. Ship it

Run `pstack-rails:ship-task <KEY>` as soon as the PRs are open. Do not end
the turn on a PR link. That skill gets the PRs green, verifies and merges
them, deploys and QAs each stage, fixes what QA finds, and removes the
worktrees.

Done when `ship-task` is done: the last stage's QA comment says PASS and the
ticket is `done`.
