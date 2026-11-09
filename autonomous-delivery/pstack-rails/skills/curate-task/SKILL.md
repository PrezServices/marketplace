---
name: curate-task
description: >-
  Curate a ticket into ready to develop with pstack: keep what its author
  asked for, have /pstack:poteto-mode design the how (how and architect, or a
  multi-phase plan for big work), write the design and slicing into the
  ticket, ask the author in plain language about anything unclear, and move
  it to ready. Use when asked to curate, refine, groom or make a ticket
  ready, especially one written by someone non-technical, or before
  "implement <KEY>" on a ticket that is only an idea.
disable-model-invocation: true
---

# Curating a ticket

The ticket's author, often someone non-technical, owns **what** gets
delivered: the commitment (Problem statement to Acceptance criteria, the
sections of `${CLAUDE_PLUGIN_ROOT}/skills/create-task/SKILL.md`). Curation owns **how**: pstack designs it
and writes Functional requirements, Tech decisions and Slicing. Curation
changes the author's words only with their yes. A curated ticket is one
`implement-task` can build without asking anyone anything.

**Tracker.** Read the **Tracker** section of `.pstack-rails/config.md`. When
its adapter is `none` (or missing), this workspace has no tickets: say so in
one line and stop. Otherwise read the adapter it names in
`${CLAUDE_PLUGIN_ROOT}/trackers/`. Every read, write, comment and transition
below goes through it.

## Input

$ARGUMENTS: a ticket key.

## 1. Load the ticket

Read it with the adapter: description, status, author, comments, links. Stop,
with one sentence to the user, when it's `done`, `cancelled` or
`in-progress` (it's being built; curation would move the ground under the
builder). A `ready` ticket is a re-curation: say so and go on.

## 2. Sort the author's words into the commitment

A non-technical author writes a story, not sections. Sort what they wrote
into Problem statement, Context, Goals, Non-goals and Acceptance criteria,
keeping their words and meaning. Nothing they wrote is dropped; what fits no
section goes in Context.

Then check the commitment as a builder would need it:

- **Acceptance criteria** are behaviour a person can see and check, each one a
  test. "It should be fast" or "it should work well" isn't one yet.
- **Goals** say what changes for whom.
- **Gaps and contradictions**: a goal with no criterion that proves it, two
  criteria that can't both hold, an obvious case nobody mentioned (an empty
  list, a failed payment, a second click).

For each finding, draft the clearer version **in the author's language and
vocabulary**, with no technical terms. These are proposals for the author;
the ticket keeps their wording until they say yes.

Done when every part of the author's text sits in a section, and every
finding has a proposal.

## 3. Have pstack design the how

Run `/pstack:poteto-mode` with this as the request. When the Skill tool
refuses it, open its `SKILL.md` under the pstack path the session orders give
and follow it.

```
Curate <KEY>: <title>. Design only: no code, no branch, no PR.

The commitment below is the author's and is fixed. Design how to deliver it
and stop before implementation.

- One PR's worth of work: run the Feature playbook's design steps only, how
  over the affected code, then architect, and stop before delegating code.
- More than one PR or phase: run the Multi-phase plan playbook, settling open
  questions by prototype, and stop at hand-back. Put the plan in the reply,
  not in a docs/ file.
- A contested design goes through interrogate first.
- Return: the technical brief and numbered functional requirements; codebase
  facts (paths with lines), reuse, access patterns, decisions with the
  alternatives rejected and why, do-not-touch paths, gates; for more than
  one PR, the slices in merge order with what each delivers; and every
  question only the author can answer, in plain language.

<the commitment as sorted in step 2>
```

pstack chooses the steps; stay out of its way. A question of fact about the
code is pstack's to settle by reading or prototyping, never the author's.

Done when pstack has returned the design, or said the commitment can't be
delivered as written and why.

## 4. Write it into the ticket

Rewrite the ticket in place, by the rules of
`${CLAUDE_PLUGIN_ROOT}/skills/create-task/SKILL.md` (current design only, values
not shapes, verified facts; the tracker's history keeps the old text):

- **The commitment**: the author's words, sorted into sections, unchanged in
  meaning. Proposals from step 2 aren't applied.
- **Functional requirements, Tech decisions**: pstack's design. Name the repos
  covered in Context.
- **Slicing**, when there's more than one PR: one line per slice, in merge
  order. Create a sub-task for each with the adapter, carrying its slice of
  the design and the criteria it proves, linked to this ticket.

## 5. Ask the author, in plain language

When step 2 or 3 left anything for the author (a proposed criterion, a gap,
a contradiction, a product choice pstack couldn't settle), post **one**
comment on the ticket, mentioning the author:

- Two or three sentences on what will be built, in their words.
- Each question numbered, with the proposed answer they can accept with a
  "yes": "When the list is empty, should it show 'No payments yet'? (proposed:
  yes)".
- No paths, code or jargon. If a question can't be said without them, it was
  pstack's to answer.

Tell the user the same, in one line each.

## 6. Move it on

- **Nothing open for the author**: transition to `ready`. When the workspace
  maps no `ready` status, add the label `curated` instead (creating it once,
  on the user's yes) and say so.
- **Questions open**: leave it in `backlog`, assigned to the author. When
  they answer, apply the answers they accepted to the commitment and run this
  skill again; a re-run only redoes the design if the answers changed what
  gets delivered.

Done when the ticket is `ready` (or `curated`) with all seven sections, or
in `backlog` with one comment holding every open question.
