---
name: implement-task
description: >-
  Implement a curated task or sub-task from its ticket alone, as the execution
  contract it is: pre-flight the ticket against current main, create the
  ticket worktrees, build exactly what Functional requirements and Tech
  decisions say, pass the gates, pre-review, open the PRs and hand the driver
  a plain-language verification script. Use when someone says "implement
  <KEY>", "pick up this ticket" or "build this task", or pastes a ticket key
  and expects code. Also use before briefing a worker or subagent on a
  ticket, and before writing code for a key right after filing it, so its
  readiness gate runs first.
---

# Implementing a curated ticket

An engineer curated the ticket so that a session with no other context can
build it. You are that session. The **ticket is the contract**: Functional
requirements say what to build, Tech decisions say what is decided and what
is off-limits, Acceptance criteria say what done looks like. Your judgment
goes into executing the contract well.

The person driving you may not read code. Speak to them in plain language,
about outcomes, and ask them only what a product person can answer. A
question only an engineer can answer is a **curation gap**, and it goes to
the ticket's curator (see "Curation gaps").

The rails still bind: hard stops, pull requests, data access, time.

**Tracker.** Read the **Tracker** section of `.prez-rails/config.md`, then
the adapter it names in `${CLAUDE_PLUGIN_ROOT}/trackers/`.

## Input

$ARGUMENTS: a ticket key, optionally the repo to start in.

## Step 1: Load the contract

Read the ticket with the adapter: description, status, labels, parent,
assignee, links. Read the whole description once, then pin:

- **Repos covered**, with what changes in each.
- **The OpenSpec change** path, or the "no OpenSpec change" reason.
- **Functional requirements**, numbered, and the brief above them.
- **Tech decisions**: the diagnosed facts, do-not-touch, gates, **Driver**,
  **Left to the implementer**.
- **Acceptance criteria**, one per line.

Stop, with a comment on the ticket, when any of these holds:

| Condition | What you say |
| --- | --- |
| Status is not `ready`, and not `in-progress` with a branch for the key on origin (a resume) | the ticket isn't ready to implement, and why |
| `needs-curation` is on | the curator hasn't cleared the gap; name the comment |
| One of the seven sections, Repos covered, OpenSpec or Driver is missing | which one, so the curator adds it |
| `Driver: engineer only` and the driver isn't an engineer | it's marked for an engineer; name the curator |
| A task with open sub-tasks | the work is in the sub-tasks; name the first in Slicing order |

When you can't tell whether the driver is an engineer, ask once, in one
sentence.

## Step 2: Read the repo pages, then pre-flight the facts

For each repo covered, read `.prez-rails/repos/<repo>.md`: **Patterns**
(where a new piece lands), **Traps** (what already cost a session time),
**Tech debt**, **Gates**. A repo with no page is built from its own
`CLAUDE.md`; say so in the PR.

Facts drift between curation and pickup. After `rails-sync <repo>` for each
repo covered, check every fact in Tech decisions and the brief against the
submodule folders:

- Every path exists; every line number points at what the ticket says; every
  function, column, enum member, cron rate and helper is there.
- An existing OpenSpec change folder's `Tracking` names this ticket or its
  parent. A missing folder is expected; Step 4 writes it.
- "Reuse from <KEY>" items are merged on `main`.
- No do-not-touch file is also one the requirements change.

Write a short table: fact, where checked, holds or drifted. A drift that
changes what you'd build is a curation gap: stop. A line number that moved
over unchanged code is a note, not a gap.

Done when every fact has a row and no drifted row changes the work.

## Step 3: Worktrees

From the workspace root, one call with every repo covered:

```sh
rails-new-ticket <branch> <repo> [<repo>...]
```

`<branch>` is the adapter's branch name for the key. An existing branch is
picked up; read its log and build on it. Move the ticket to `in-progress` (a
sub-task moves its parent first).

## Step 4: Write the OpenSpec change, then build

In the worktree the ticket names for the change, run `prez-rails:openspec-propose`
with the ticket as its whole input: the exact path from Context, a `proposal.md` whose
`Tracking` gives the key, container and sprint, and a design that restates
nothing the ticket decided differently. A design that needs a decision the
ticket didn't make is a curation gap. An existing folder is read and built
from. "No OpenSpec change" skips this.

Then build requirement by requirement, in the ticket's order, inside the
worktrees only:

- **The ticket's facts are the map; the repo page is the legend.** A file the
  ticket didn't name goes where the page's Patterns put its siblings, and is
  listed in the PR.
- **Decide only what "Left to the implementer" grants.** Anything neither
  decided nor granted is a curation gap.
- **Do-not-touch is a wall.** Needing a file on it is a curation gap.
- **Values come from the ticket.** An unspelled string, status, message or
  mapping is a curation gap; invented copy is what a non-engineer driver is
  least able to catch.
- **Every Acceptance criterion gets at least one test that fails without the
  change**, written per the repo's testing conventions.
- **Scope stays inside Repos covered.**
- **Hard stops** apply even when the ticket seems to ask for one: such a ticket
  says `Driver: engineer only`, and if it doesn't, that's a curation gap.
- **Tech debt is boy-scout work.** Fix it only inside lines the ticket already
  changes, in a few lines; otherwise list it under "Noticed, not fixed".

Commit as each requirement lands, subject `<KEY>: <what>`, body naming the
requirement and why.

Done when `tasks.md` is fully checked, every requirement maps to code and a
test, and the diff touches nothing outside Repos covered.

## Step 5: Gates, then pre-review

Run the gates from Tech decisions in each worktree, as the repo page and the
repo's `CLAUDE.md` define them, and make them green by fixing the code. A gate
that only goes green by touching do-not-touch or another repo is a curation
gap.

Then run `prez-rails:review-local` in each worktree and fix every critical, high
and medium finding before the PR.

## Step 6: PR

One PR per repo, from its worktree, per **Pull requests** in the rails. Add these sections:

- **Touched outside the ticket's list**: files Tech decisions didn't name, one
  line each on why. "None" when none.
- **Decided by the implementer**: each granted choice and what was chosen.
- **Noticed, not fixed**: tech debt walked past.
- **Traps hit**: what in this repo cost a wrong turn, one line each, written so
  the next session avoids it. Say these are for the repo's page.

Link the PR on the ticket. Watch it to green per the rails:
mechanical fixes are yours; anything else goes to the driver, who forwards
design points to the curator.

## Step 7: Hand the driver a verification script

From the Acceptance criteria, write a numbered list the driver can do after
the deploy, each step as where to go, what to do, what they should see, in
app words. Post it as the last section of your final message and, when the
ticket has a post-deploy section, as a ticket comment.

Name the next prompts: `prez-rails:deploy` (when the repo's deploy isn't
automatic) and `prez-rails:qa-task`.

## Curation gaps

A curation gap is anything the ticket needed to say and didn't, or said
wrongly: a drifted fact that changes the work, an unspelled value, a decision
neither made nor granted, a do-not-touch file the work needs, a repo not
covered, an unflagged hard stop. The handling is always the same:

1. Stop building. Leave the worktrees and commits as they are.
2. Post one comment headed **Curation gap**, in two registers: a
   plain-language paragraph for the driver (what's missing, what it blocks),
   then the detail for the curator (the section, the fact as found, the
   options with your recommendation).
3. Add the `needs-curation` label. Leave the status at `in-progress`.
4. Tell the driver, in two sentences, that the ticket went back to its curator
   and that the same prompt resumes it once the label is gone.

This skill leaves the ticket's description alone. Fixing it is the curator's
call, through `prez-rails:curate-task`.

## Anti-patterns

- Asking the driver which of two technical approaches they prefer
- Editing the ticket so it matches what was built
- Building "the safe part" of a ticket that has a curation gap
- A file outside Repos covered changed "because it was quick"
- A gate skipped, lowered or marked expected-failure to get to green
- A verification script that tells the driver to read a log or run a command
