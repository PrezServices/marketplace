---
name: create-roadmap
description: >-
  Build or update a roadmap for a line of work that runs on external windows
  and deadlines (funding, hiring, certification, partnerships, compliance):
  one Claude Doc with nine fixed sections that leads with the single
  decision to act on now, plus a numbered Spanish kit in the repo with the
  documents the roadmap needs, kept in sync with every fact settled in chat.
  Use when asked to make a roadmap, plan a programme, map a landscape of
  options and deadlines, or update a roadmap doc built this way. Not for
  one ticket's PR plan (that is Slicing in `create-task`).
---

# Building a roadmap

The reader is the user a month from now, opening the doc to know what to do
next. The doc answers that in its first paragraph; everything below it is
the evidence and the standing routine that keeps the answer current.

**Config.** Read `.company-ops/config.md` first. When it is missing, say so
in one line, name `/company-ops:setup`, and stop. Its **Documents** section
gives where roadmaps live, the title pattern and the two languages; its
**Conventions** section gives the legend and the writing rules; its
**Entities** table gives the rows of the fit assessment; its **Knowledge
base** gives the path step 2 reads.

Two artefacts, one source of truth:

| Artefact | Holds | Language |
| --- | --- | --- |
| The doc, one tab | the strategy: decision, landscape, fit, calendar, routine | the doc language |
| Kit folder in the repo, `<topic>/00-…06-*.md` | the drafts the strategy needs: master narrative, forms, contracts, budget, tracker | the kit language, `[bracketed]` placeholders for unknowns |

Facts settled in chat go into both the same turn.

## 1. Find or birth the doc

Search the user's docs for a roadmap on the topic. One exists: read it in
full, strip it to text, and edit in place. Never recreate a doc.

None exists: birth the skeleton first, before any research, with the title
from the config's pattern, a byline of an as-of date chip and a mention of
the user, and one pending block per section below. Open it and keep the
user posted in one line per section as it fills.

## 2. Gather inputs

In this order, stopping when the question at hand is answered:

1. The existing doc and its open questions.
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
the chain of facts that gates admissibility for it. Order the whole doc by
what blocks that deadline. Everything later is **projected from past
cadence** and says so.

## 4. The nine sections

In this order, all present.

1. **Summary.** The single decision to act on now and its deadline; who or
   what the second candidate is; what stays on hold; why the obvious
   alternative doesn't fit. Then `Next actions:` as a checklist, each
   `By <date chip>: <action> (owner: <person>)`, or `From <date>:` for
   watch items.
2. **Landscape.** The legend from the config's Conventions. One table per kind of option (money, institutions, platforms, legal
   regimes), with named columns that fit the kind, always ending in the
   next window or the source. Each window tagged C or I. Lower-priority
   options are one closing sentence, not rows.
3. **Fit assessment.** Table `Entity | Best-fit options | Blockers to
   resolve`, then the framing paragraphs: the exclusion or trap to avoid,
   how to position, sequencing constraints ("winning X first blocks Y").
4. **Calendar.** One paragraph on what is confirmed and each option's
   cadence, with "recheck official pages monthly". A `Window | What happens
   | Our move` table when windows are many.
5. **Document kit.** Checklists under bold groups (Legal and tax,
   Narrative, Team, Numbers, Evidence, per-entity extras). Rule: build once
   per entity, refresh on a named cadence, covers most of any application.
   Each item maps to a file in the repo kit.
6. **Best practices.** One subsection per option: score weights or
   selection criteria, admissibility-critical rules first, then writing
   advice. A General subsection: one master narrative, every claim
   demonstrable, log every application and reuse reviewer feedback.
7. **Ongoing roadmap.** Numbered list of about four phases, each
   `**<phase name>** (<absolute date range>).` plus two or three sentences
   naming the deliverables and the gate that closes the phase. Then a
   `Monthly cadence` checklist: first-Monday watchlist, update metrics and
   master answers, the six-week rule (confirm eligibility against the
   official bases, assign an owner, internal deadline two days before
   close), log results, periodic kit refresh.
8. **Open questions.** Checklist; each question says what it decides and
   carries a proposed answer the user can accept with a "yes".
9. **Sources.** Grouped links to the official pages opened; third-party
   sources labeled as such.

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
  the Blockers column, not in a graph.
- Current state only: when the user settles a fact, replace it in every
  place the doc mentions it (summary, next actions, fit cell, framing
  paragraph, open question) in one update call, and drop the caveats they
  waved off. The doc's history keeps the old text.
- A new asset the user names is mined for evidence, then evaluated both as
  narrative and as a legal vehicle against each option's thresholds; the
  result is a comparison table and an open question, not a decision.
- Replies in chat lead with the deadline and the blocking facts, compact.

## 7. Close

Save a memory note with the facts not derivable from the doc or repo
(entity choices, stipends, the user's standing preferences). Reply with one
line and the doc link.

## Anti-patterns

- Research before the skeleton exists
- A summary that lists options instead of naming the decision
- A window without its confidence tag
- A guessed value where a `[placeholder]` belongs
- A dated decision header or "previously we thought" in the doc
- Recreating the doc instead of editing it
