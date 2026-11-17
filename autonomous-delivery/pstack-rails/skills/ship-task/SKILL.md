---
name: ship-task
description: >-
  Carry a ticket whose PRs are open to done: get each PR green, verify it
  independently, merge it, take the change through every deploy stage the
  repo has, QA the acceptance criteria on each stage, and fix what QA finds
  under the same ticket. Use when `implement-task` reaches its PRs, when
  someone says "ship <KEY>", "deploy <KEY>", "QA <KEY>" or "is <KEY> live?",
  or when a session resumes a ticket that sits in review.
---

# Shipping a ticket

An open PR is the middle of the work. The ticket is done when its acceptance
criteria are proven on the last stage the repo has, which is production where
one exists. You own every step between. Nobody is waiting to be asked.

**Tracker.** Read the **Tracker** section of `.pstack-rails/config.md`, then
the adapter it names in `${CLAUDE_PLUGIN_ROOT}/trackers/`. With no tracker,
the evidence goes in the PR instead of a ticket comment.

**Delivery.** Read the **Delivery** section of `.pstack-rails/config.md`. It
says who merges and, per repo, the stages in order, with how code reaches
each one, where it runs, how to drive it and what must never be driven. When
the section or a repo's rows are missing, read the repo's
`.github/workflows/`, deploy config and README, write the rows, say so in one
line, and go on. That change gets its own PR on the workspace repo. A config
written before 0.4.0 has a **Deploys** section with a `Go` line. Read `Go` as
`Deploy`, and read `Merge` as `user` until the person sets it.

**pstack.** The playbooks named below are in
`<pstack>/skills/poteto-mode/playbooks/`, where `<pstack>` is the path the
session orders give. Read each one before its step. Asking for this skill is
the request to land that Babysit and Shipping wait for.

## Input

$ARGUMENTS: a ticket key. The PRs, the deploy runs and the stage are looked
up.

## When you stop

These need the person. Anything else is yours.

| Condition | What you do |
| --- | --- |
| A deploy or a QA step would message a customer, move money or delete data | prepare it, show the exact action, wait |
| A standing order in the config names a gate | follow the order |
| Delivery says `Merge: user` | get the PR merge-ready, say so, and continue from step 3 once it merges |
| The evidence says a goal or an acceptance criterion is wrong | `implement-task` section 4, the commitment row |
| Access you lack and cannot get | comment what and who, transition to `blocked` |

A wait covers that step only. Work that does not depend on the answer goes
on.

## 1. Get it green

Run pstack's Babysit playbook in `drive` mode on the ticket's PRs, lowest
first. Done when the forge says each PR can merge.

## 2. Verify, then merge

Run pstack's Shipping playbook. The verdict on each PR comes from an agent
that did not write the code. It runs the change the way a user would, with
the repo's verify skill, and posts `PASS`, `PASS+NOTES` or `FAIL` on the PR.
Green CI is not a verdict.

Merge on a pass, the way the repo's history shows it merges. A `FAIL` goes to
step 6. Read the PR back and confirm it reads merged.

## 3. Deploy, lowest stage first

For each stage in the repo's Delivery rows, in order:

- **Pin what ships.** The ref, its head sha, and
  `git log --oneline <deployed sha>..<ref>`. Commits that belong to another
  ticket ship with yours. Name them.
- **One deploy per stage at a time.** List the runs first and wait for any in
  progress or queued.
- **Trigger** the way the row says. A merge that deploys is the trigger, so
  find the run it started. A dispatch is
  `gh workflow run <file> -R <owner>/<repo> --ref <ref>`.
- **Watch** with `gh run watch <run-id> -R <owner>/<repo> --exit-status`.
  Never cancel a deploy that is running. On a failure, read
  `gh run view <run-id> --log-failed`, name the cause, and go to step 6.
- **Confirm the revision.** A green run is not proof. Read what the stage
  serves (a deployment's commit, a version endpoint, a build id in the page)
  and check that it carries the merge commit. Note the time. Every log query
  in step 4 starts there.

Schema changes apply before the code that needs them. Each deploy leaves the
code already running in a working state.

A stage is promoted only after step 4 passes on the stage below it.

## 4. QA the stage

Prove every acceptance criterion against the deployed system. A local run
proves your working tree and nothing about the deploy.

1. **Baseline.** Before the deploy when you can, record the symptom or the
   absence the ticket changes, as numbers or a capture.
2. **Drive** the scenario each criterion describes, through the real surface,
   with the repo's verify skill pointed at the stage's URL. Use the test
   identities the Delivery row names. On production, drive only what the row
   marks safe.
3. **Check four things per criterion.** The stored fact, printed raw. What
   the user sees, agreeing with it. The old symptom gone since the deploy
   time. The neighbouring behaviour in the same flow unchanged.
4. **Wait on a condition, never a sleep.** Poll the store or the log with a
   timeout.

A criterion that cannot be driven safely on this stage is named with the
reason. It is not a pass.

## 5. Record it

One comment on the ticket per stage:

```
**<Stage> QA <date>: PASS|FAIL** (PR #NNN merged, deploy <run id> green, <revision> at <time>)

<one line on how the scenario was driven>

| Criterion | Evidence |
| --- | --- |
| … | … |

Not exercised: <criterion and why, or "none">
```

Numbers and ids, no raw dumps, no secrets.

| Result | Tracker |
| --- | --- |
| PASS, a later stage remains | stays `in-review`. Go to step 3 for the next stage |
| PASS on the last stage | `done`. When the tracker's automation moved it earlier, leave it and say so in the comment |
| FAIL | back to `in-progress`. Go to step 6 |

## 6. Fix what you find

A defect found at any step is yours, under the same ticket.

1. When production is broken for users, restore it first. Use the repo's
   rollback, or a revert PR through steps 1 to 3, and say what you rolled
   back.
2. Run pstack's Bug fix playbook with the QA evidence as the report. The
   reproduction lands before the fix.
3. Ship the fix through steps 1 to 5 again, from the lowest stage.

A defect that the ticket did not cause and that sits outside its repos gets
its own ticket through `pstack-rails:create-task`, linked from the comment.
The ticket you hold still finishes.

## 7. Close out

- Remove the worktrees
  (`git -C <repo> worktree remove ../tickets/<branch>/<repo>`, after
  `git status` there is clean) and the empty `tickets/<branch>/`.
- At a meta-repo root, the submodule pointer moves in its own PR.
- Reply with the goal, what shipped, the evidence per stage, and anything a
  person still owes.

Done when the last stage's QA comment says PASS and the ticket is `done`.
