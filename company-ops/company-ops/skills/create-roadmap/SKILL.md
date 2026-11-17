---
name: create-roadmap
description: >-
  Build or update a roadmap for a line of work that runs on external windows
  and deadlines (funding, hiring, certification, partnerships, compliance):
  one Claude Whiteboard with nine fixed regions that leads with the single
  decision to act on now, plus a numbered Spanish kit in the repo with the
  documents the roadmap needs, kept in sync with every fact settled in chat.
  Use when asked to make a roadmap, plan a programme, map a landscape of
  options and deadlines, or update a roadmap board built this way. Not for
  one ticket's PR plan (that is Slicing in `create-task`).
---

# Building a roadmap

The reader is the user a month from now, opening the board to know what to
do next. The board answers that at its top left; everything else on it is
the evidence and the standing routine that keeps the answer current. The
user rearranges the board by hand between sessions, so the skill edits what
is there and never rebuilds it.

**Config.** Read `.company-ops/config.md` first. When it is missing, say so
in one line, name `/company-ops:setup`, and stop. Its **Documents** section
gives where roadmaps live, the title pattern and the two languages; its
**Conventions** section gives the legend and the writing rules; its
**Entities** table gives the rows of the fit assessment; its **Knowledge
base** gives the path step 2 reads.

Two artefacts, one source of truth:

| Artefact | Holds | Language |
| --- | --- | --- |
| The board, one Whiteboard | the strategy: decision, landscape, fit, calendar, routine | the board language |
| Kit folder in the repo, `<topic>/00-…06-*.md` | the drafts the strategy needs: master narrative, forms, contracts, budget, tracker | the kit language, `[bracketed]` placeholders for unknowns |

Facts settled in chat go into both the same turn.

**The board's rules.** The Whiteboard type is
`https://claude.ai/artifact/PLsEyfjXbDUM1iasW7rjLR`. Before the first write
of a session, read its instructions (Artifact tool, `action: "read"` with
that `type_url`). They give the element format, the colour limit, the
spacing and the edit-in-place rules, and they win over anything here that
contradicts them. Content goes through `ArtifactData` batch writes, never
through files published to the board.

## 1. Find or birth the board

List the user's artifacts for a Whiteboard titled by the config's pattern
for the topic. One exists: read `board/meta` and every element before any
write, and never send `type_url` again. Edit in place.

None exists: birth the frame first, before any research. Publish with the
Whiteboard `type_url`, the title from the config's pattern, and no files.
Then one batch writes `board/meta` and the frame: the title as `text` size
title, under it one `text` size large for the takeaway sentence, 10 words at
most, and the nine containers of the layout below, each titled and empty.
Keep the user posted in one line per region as it fills.

### Layout

Nine containers, about 1500 wide in all, read left to right then top to
bottom. None overlaps another. A container grows down when its contents
need more room, and the row below moves down with it.

| Row | Left | Middle | Right |
| --- | --- | --- | --- |
| 1 | Summary | Landscape | Fit assessment |
| 2 | Calendar | Ongoing roadmap (spans middle and right) | |
| 3 | Document kit | Best practices | Open questions |
| 4 | Sources (spans all three) | | |

Three marks, no fourth: blue for the decision and the next actions, yellow
for open questions, white for everything else.

## 2. Gather inputs

In this order, stopping when the question at hand is answered:

1. The existing board and its open questions.
2. The knowledge base the config names (offering, audience, entities,
   legal hub, pricing).
3. Repos and document folders of any entity the roadmap covers, for dates,
   customers, legal status and past work. Pitch decks are read by unzipping
   the `pptx`.
4. Official pages of each programme, institution or regulator, fetched into
   the scratchpad with `curl` and read there. A third-party page is a lead,
   never a source.
5. The user, for anything only they decide.

## 3. Find the critical path

Before writing, name the **one confirmed deadline** closest in time and
the chain of facts that gates admissibility for it. Order the whole board by
what blocks that deadline. Everything later is **projected from past
cadence** and says so.

## 4. The nine regions

Each region keeps the content rules below and takes the board form in its
table row. Text longer than a label gets a width, 300 to 400, so it wraps.

| Region | Board form |
| --- | --- |
| Summary | blue rounded block, `text` size large, for the decision and its deadline; one blue rounded block per next action in a column under it |
| Landscape | legend as `text` size small, then one `table` per kind of option |
| Fit assessment | one `table` Entity, Best-fit options, Blockers to resolve; framing paragraphs as one white block with wrap 400 |
| Calendar | one white block for the confirmed state and cadences; a `table` Window, What happens, Our move when windows are many |
| Document kit | one white block per bold group, items as a list inside |
| Best practices | one white block per option plus one General block |
| Ongoing roadmap | one white block per phase in a left-to-right row joined by arrows; a white Monthly cadence block under the row |
| Open questions | one yellow rounded block per question, the proposed answer in the same block |
| Sources | one `link` card per official page; a third-party page says so in its title |

1. **Summary.** The single decision to act on now and its deadline; who or
   what the second candidate is; what stays on hold; why the obvious
   alternative doesn't fit. Then the next actions, each `By <date>:
   <action> (owner: <person>)`, or `From <date>:` for watch items.
2. **Landscape.** The legend from the config's Conventions. One table per
   kind of option (money, institutions, platforms, legal regimes), with
   named columns that fit the kind, always ending in the next window or the
   source. Each window tagged C or I; a window with no tag is not written.
   Lower-priority options are one closing sentence in a white block, not
   rows.
3. **Fit assessment.** The table, then the framing paragraphs: the
   exclusion or trap to avoid, how to position, sequencing constraints
   ("winning X first blocks Y").
4. **Calendar.** What is confirmed and each option's cadence, with "recheck
   official pages monthly".
5. **Document kit.** One group each for Legal and tax, Narrative, Team,
   Numbers, Evidence, per-entity extras. Rule: build once per entity,
   refresh on a named cadence, covers most of any application. Each item
   maps to a file in the repo kit.
6. **Best practices.** Per option: score weights or selection criteria,
   admissibility-critical rules first, then writing advice. General: one
   master narrative, every claim demonstrable, log every application and
   reuse reviewer feedback.
7. **Ongoing roadmap.** About four phases, each block titled
   `<phase name> (<absolute date range>)` with two or three sentences naming
   the deliverables and the gate that closes the phase. Monthly cadence as a
   list: first-Monday watchlist, update metrics and master answers, the
   six-week rule (confirm eligibility against the official bases, assign an
   owner, internal deadline two days before close), log results, periodic
   kit refresh.
8. **Open questions.** Each says what it decides and carries a proposed
   answer the user can accept with a "yes".
9. **Sources.** The official pages opened, grouped by option.

## 5. The repo kit

A numbered folder at the workspace root named after the topic:

| File | Holds |
| --- | --- |
| `00-README.md` | index table, dated checklist, non-negotiable rules, fixed company facts |
| `01-…` | the master narrative or the governing document (contract, convenio) |
| `02-…`, `03-…` | the forms and answers, ordered by the option's score weights |
| `04-…` | budget or sizing, by activity, with milestones and a cash-flow table |
| `05-tracker.md` | applications or candidates table plus the monthly watchlist |
| `06-…` | notes on a second entity or extras |

Every unknown is `[bracketed]`, never invented. The kit stays uncommitted
until the user says to commit; it is content, not code, so no ticket.

## 6. Writing rules

The config's Conventions apply to every line. Beyond them:

- Entities and options are table rows; dependencies live in prose and in
  the Blockers column. The only arrows on the board join the phases.
- Current state only: when the user settles a fact, update the changed
  fields of every element that carried it (summary block, next-action
  block, fit cell, framing block, open question) in one batch, by id, and
  drop the caveats they waved off. No element is rebuilt and no id is
  dropped. An element the user moved keeps its position.
- A question the user answers leaves the Open questions region: remove its
  block and write the answer where it belongs, in the same batch.
- A new asset the user names is mined for evidence, then evaluated both as
  narrative and as a legal vehicle against each option's thresholds; the
  result is a comparison table and an open question, not a decision.
- Replies in chat lead with the deadline and the blocking facts, compact.

## 7. Close

Save a memory note with the facts not derivable from the board or repo
(entity choices, stipends, the user's standing preferences). Reply in two or
three sentences, what the board now says and what was assumed, plus the
board link.

## Anti-patterns

- Research before the frame exists
- A summary that lists options instead of naming the decision
- A window without its confidence tag
- A guessed value where a `[placeholder]` belongs
- A dated decision header or "previously we thought" on the board
- Rebuilding the board, or a second board for the same topic
- A fourth colour, or a grid of blocks where a table belongs
