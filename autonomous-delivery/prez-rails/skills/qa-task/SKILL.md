---
name: qa-task
description: >-
  QA a merged-and-deployed task end to end and move it on: read the ticket's
  acceptance criteria, take a baseline, confirm the deployed revision, drive
  the real scenario through the deployed system, verify the outcome in stored
  data and logs as well as on screen, post an evidence comment and move the
  ticket to the status the evidence supports, or file a sub-defect. Use when
  someone says "QA <KEY>", "verify this in <env>" or "is this ticket done?",
  or after a deploy of ticket work.
---

# QA-ing a task

You are the QA engineer for a ticket that is merged and deployed. Your job is
to **prove the acceptance criteria against the deployed system**, record the
proof on the ticket, and move it to the status the evidence supports. Code is
fixed elsewhere: a failure becomes a sub-defect through `prez-rails:create-task`.

**Tracker.** Read the **Tracker** section of `.prez-rails/config.md`, then
the adapter it names in `${CLAUDE_PLUGIN_ROOT}/trackers/`.

**The repo page is the environment guide.** For each repo covered, the
**Deploy** and **QA** sections of `.prez-rails/repos/<repo>.md` name the
environments, what proves a rollout, how to drive a scenario, the test
identities, where the evidence lives, and what must never be driven. This
skill is the method; the page holds the facts. A repo with no QA section is
QA-ed only as far as its criteria can be read without driving anything; say so.

## Input

$ARGUMENTS: a ticket key, optionally the deploy run and the environment.
Missing pieces are looked up.

## Step 0: Load context

1. Read the ticket with its comments. Pin three things:
   - **Acceptance criteria**: each becomes one row of the evidence table.
   - **Post-deploy verification**, when the ticket has one: the author's own
     checklist, which outranks anything you'd invent.
   - **Which environment the criteria name.** A pass anywhere else can't
     finish the ticket (Step 6).
2. Find the PR: `gh pr list -R <owner>/<repo> --search "<KEY>" --state
   merged`. Its description says what the author already verified, so you
   cover what they left for after deploy.
3. Find the deploy the page names and wait for it to finish green before
   Step 2. A half-rolled deploy proves nothing.

## Step 1: Baseline, before you touch anything

Measure the symptom the ticket fixes as it stands, in the target environment,
over a window long enough to be unambiguous: a log signature counted, a table
population counted, a screen state captured. Write the numbers down verbatim.
A baseline of "0 rows, 12 errors" is what turns "3 rows, 0 errors" into proof.
When the ticket adds new behaviour with no prior symptom, the baseline is its
absence.

## Step 2: Confirm the deployed revision

A green run is necessary, not sufficient. Read the artifact the page names
(a service's current deployment, a platform deployment's commit, a build
id) and check it carries the merge commit. Note its timestamp: every
log query in Step 4 starts there.

## Step 3: Drive the scenario

Drive the scenario the criteria describe through the deployed system, the way
the page says: a real request, a real screen, a test identity the page names.
Evidence from the deployed system is the only evidence here; a local run
proves your working tree, not the deploy.

When the only environment is production, drive only the flows the page marks
safe, with the test identities it names, and never anything that moves real
money or reaches a real user. When a criterion can't be driven safely, wait
for organic traffic and say so.

## Step 4: Verify

Wait on a condition, not a sleep: poll the store or the log until the row or
line appears, with a timeout.

For each scenario:

1. **The fact the ticket is about**: the stored row, field or event, printed
   raw. Types and units are often the whole point (integer minor units, not
   floats; UTC instants).
2. **The user-visible effect**: what the screen or response shows, agreeing
   with the stored data.
3. **The old symptom is gone**: the Step 1 query again, from the deploy
   timestamp to now.
4. **Nothing else regressed**: the neighbouring behaviour in the same flow
   looks as before. Name what you looked at.

When a criterion needs data no test identity has, say so instead of faking
it. Unit coverage on the same path substitutes only when the PR has it.

## Step 5: Post the evidence

One ticket comment, shaped like this:

```
**<Env> QA <date> — PASS|FAIL** (PR #NNN merged, deploy <id> green, <artifact> at <ts>)

<one line: how the scenario was driven>

Baseline before deploy (<window>): <numbers from Step 1>.

After deploy:
| Scenario | Identity | What landed |
|---|---|---|
| … | … | … |

- <raw evidence>
- <log result since deploy>
- <screen matched stored data>
- <anything odd, and why it's unrelated>

<criteria not exercised, and why>

Remaining for done: <criteria for another environment, verbatim>
```

Numbers and ids in the table or bullets, not prose. Under ~250 words. No raw
JSON dumps or secrets.

## Step 6: Transition

| Evidence | Move to |
| --- | --- |
| PASS, criteria name a later environment | `ready-to-deploy` |
| PASS where the criteria ask (or "any env") | `done` |
| Any FAIL | leave the status; file a **sub-defect** under this task with `prez-rails:create-task`, link the comment, tell the user |
| Deploy unfinished, or revision unchanged | nothing on the ticket; report and wait |

When the tracker's automation already moved the ticket (see the adapter's
Traps), record that in the comment rather than moving it back. Assign the
ticket to whoever ran QA when it's unassigned. Leave the container alone.

## Step 7: Follow-through in the later environment

When the criteria name a later environment: after its deploy, repeat Step 2
there, then gather evidence the way that environment's page section allows
(organic traffic when driving is off-limits). Post a second comment of the
same shape and move the ticket to `done`.

## Anti-patterns

- QA before the revision moved: you're testing the old code
- `sleep N` between drive and check, instead of polling a condition
- PASS from the screen alone: it looked fine before the fix too; the stored
  fact is the criterion
- Driving real money or a real user's session to get evidence
- Leaving the ticket in review after a green QA, or calling it done when the
  criteria name a later environment
