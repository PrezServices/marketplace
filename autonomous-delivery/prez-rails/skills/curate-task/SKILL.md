---
name: curate-task
description: >-
  Audit a task or sub-task for readiness before a session implements it from
  the ticket alone, and bring it to ready: verify every stated fact against
  current main, find every value, decision and file the implementer would
  have to guess, decide who may drive it (engineer only, or anyone) and what
  is left to the implementer, then fix the ticket or hand back the list. Use
  when an engineer asks to curate, ready, groom or sign off a ticket, to
  check whether one is ready for development, to clear a `needs-curation`
  label, or before handing a ticket to a non-engineer driver.
---

# Curating a ticket

A curated ticket is one `prez-rails:implement-task` can build with no engineer in
the session. The driver may be a product person who can answer "is this the
outcome you want" and cannot answer "which module should own this". Curation
moves every engineering decision into the ticket before pickup.

You are the engineer. The format rules are in `prez-rails:create-task`; read it
before the first edit. This skill is the readiness gate on top of it.

**Tracker.** Read the **Tracker** section of `.prez-rails/config.md`, then
the adapter it names in `${CLAUDE_PLUGIN_ROOT}/trackers/`.

## Input

$ARGUMENTS: a ticket key, optionally "for <name>" to say who will drive it.

## Step 1: Read it as the implementer will

Read the ticket with the adapter. Read the description once as the
implementing session would: no memory of the planning, no chat thread, no
OpenSpec unless the ticket names it. Then run the whole audit and write every
miss down before fixing any. The count of misses tells you whether the ticket
is close to ready or needs a rewrite, and fixing as you go hides it.

## Step 2: The audit

First read the page of each repo covered in `.prez-rails/repos/<repo>.md`:
Patterns, Traps, Tech debt, Gates. The ticket's facts and gates follow the
Patterns, and a Trap the work will walk into is named in Tech decisions.

Each item below is a yes or a listed miss.

**Shape** (per `create-task`)

- The seven sections, in order; Slicing when more than one PR.
- Repos covered, by name, each with what changes there.
- The OpenSpec change path, or "no OpenSpec change: <reason>". When the
  folder exists, its `proposal.md` `Tracking` names this ticket.
- Acceptance criteria are behavioural tests; gates are in Tech decisions.
- Every mapping of three or more cases is a table.

**Facts hold.** After `rails-sync <repo>` for each repo covered, check
every path, line number, function, column, enum member, cron rate and helper
in Tech decisions and the brief against the submodule folder. Fix each one
that moved. A fact you can't verify comes out.

**Nothing left to guess.** Walk the Functional requirements one at a time and
ask what a session would have to decide to build each:

- a string, message, status name, field value, mapping, default
- which module, layer, file or helper owns the change
- a response shape, an error case, the unrecognised value
- the order of operations when two requirements interact
- the test that proves it

Each decision is **written into the ticket** or **granted** under "Left to
the implementer". Grant only choices with no wrong answer (a local name, the
order of two independent helpers); decide the rest now.

**The walls are concrete.** Do-not-touch names files and folders. No
requirement needs a file on it.

**Hard stops are flagged.** When the work touches a hard stop (the rails'
list plus the project config's), the ticket says `Driver: engineer only`, and Tech
decisions say what the engineer's sign-off covered.

**Size fits one session.** More than about eight source files or three
hundred changed lines in one repo, or more than one repo, is a task with
sub-tasks, one per PR, in Slicing order. A non-engineer drives sub-tasks, not
the parent.

## Step 3: Decide the driver

Write both lines at the end of Tech decisions, before the closing sentence:

```
Driver: engineer only | any
Left to the implementer: none | <one line per granted choice>
```

`any` means every audit item is a yes, no hard stop is touched, and the
post-deploy verification is something a product person can do through the
app. Otherwise `engineer only`, with one clause saying why, so a later
curation knows what to clear.

## Step 4: Fix or hand back

A handful of misses: fix them now through `prez-rails:create-task` (the whole
description, current design only). A design not yet made: post the list as a
comment headed **Curation**, one miss per line, and tell the user the ticket
needs a planning pass first.

When the ticket carries `needs-curation`, an implementing session stopped on
it. Read its **Curation gap** comment first: it names the exact miss. Fix
that, re-run Step 2 on the sections it touched, and remove the label last.
The ticket stays `in-progress` (the branch exists), and the implementing
session resumes from the same prompt.

Done when the audit has no miss, both Driver lines are written, the label is
off, and the ticket is `ready`, or still `in-progress` when it came back from
an implementation. Moving a ticket to `ready` is the last act of a first
curation and the only way one gets there.

When a merged PR listed **Traps hit** for a repo, add them to that repo's page
in a workspace PR. That is how the pages grow.

## Anti-patterns

- A fact copied from the planning session instead of re-read from `main`
- "Left to the implementer" used to park a decision the curator didn't make
- `Driver: any` on a ticket that touches a hard stop
- A do-not-touch list of concepts instead of paths
- A parent task marked `Driver: any` while its slices are undefined
