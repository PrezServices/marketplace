---
name: deploy
description: >-
  Ship a change to an environment, or roll one back, the way each repo
  deploys: pin what ships, trigger or watch the run, verify the rollout. Use
  when asked to deploy, ship, release, roll out or roll back, to check
  whether a merge is live yet, to find or watch a deploy run, or when a
  merged PR's next step is reaching an environment.
---

# Deploy

How a repo deploys is in the **Deploy** section of its page,
`.prez-rails/repos/<repo>.md`: the trigger (on merge, on dispatch, by a
platform such as Vercel), the environments, the workflow, the order
constraints, the artifact that proves the rollout, the side steps outside
the run, and the traps. Read it before step 1. This skill is the method.

**Who gives the go.** The **Deploys** section of `.prez-rails/config.md` says
whether the session triggers deploys itself or prepares them for the user's
explicit go. Merging a PR is a human's call either way; for repos that deploy
on merge, the merge is the deploy.

## Rules

Every deploy meets these. Breaking one is a trade the user makes knowingly,
stated before the go.

1. **Lower environment first.** When a repo has more than one environment, new
   code reaches the higher one only after the same commits ran on the lower
   one, except a hotfix the user names as such.
2. **QA before promotion.** A change reaches the higher environment after
   `prez-rails:qa-task` passed on the lower one and the ticket is
   `ready-to-deploy`.
3. **Backward compatible.** Each deploy stands on its own: it breaks nothing
   running and depends on nothing deployed later. Read the delta for a
   contract change (a table shape, an API field, an event, a config key, a
   cross-repo call) and confirm both producer and consumer work with the old
   and the new side. Between a backend and its clients, the backend ships first
   and stays compatible with the clients already in users' hands.
4. **Schema before code.** Migrations apply before the code that needs them,
   and the code still running during the gap tolerates the new schema.
5. **One deploy per environment at a time.** List the runs before triggering
   and wait for any in progress or queued to finish.

## 1. Pin what ships

- **Ref and sha.** Name the ref and its head sha.
- **Delta.** From the last successful deploy to the ref:
  `git log --oneline <deployed sha>..<ref>`. List the commits and the ticket
  keys they carry. That list is what's being approved; flag any commit that
  wasn't reviewed.
- **Rules 1 to 4** checked against the delta: the lower-environment run, the
  QA evidence, the contract read, the migrations.
- **CI** green on the head sha (`gh pr checks`, or `gh run list --branch`).
- **Order** constraints from the page.

Done when the user has, in one message: the ref, the commit list, CI state,
the rule checks, and the exact command or merge that ships it.

## 2. Trigger

- **On dispatch**: `gh workflow run <file> -R <owner>/<repo> --ref <ref> -f
  <input>=<value>`, after checking rule 5 in the same minute.
- **On merge**: the merge is the trigger; find the run it started.
- **Platform**: the platform's deployment for the merge commit.

A running deploy is let finish or fail, never cancelled mid-flight: a
half-applied migration or rollout is the hardest state to leave.

Done when the run's id or URL is in the message.

## 3. Watch

```sh
gh run watch <run-id> -R <owner>/<repo> --exit-status
gh run view <run-id> -R <owner>/<repo> --log-failed
```

A failure is reported with the failing step and its last lines, and nothing is
re-triggered until the cause is named.

Done when the run succeeded, or the failure is diagnosed in the message.

## 4. Verify the rollout

Read the artifact the page names and confirm it moved to the shipped sha after
the run started, then run the page's smoke check. Then:

- Ticket work: say it's ready for `prez-rails:qa-task`. Status changes belong to QA.
- Side steps the page lists for this kind of change run now, each named.

Done when the verification read and its timestamp are in the message.

## Rolling back

Rolling back is a forward deploy of the last good code: a revert PR merged to
`main`, or the page's rollback mechanism when it has one (a Worker version
rollback, a platform's instant rollback). Data changes the bad deploy carried
(migrations, seeds) stay; name them so the user decides what to undo, and
check that the old code tolerates the new schema before rolling it back.

## Adding a repo

Its page gets a **Deploy** section stating: trigger, environments, workflow,
inputs, order constraints, the verification artifact and smoke check, side
steps, rollback, and traps.
