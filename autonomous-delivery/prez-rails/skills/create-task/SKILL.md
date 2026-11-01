---
name: create-task
description: >-
  Write or rewrite a task or sub-task in the workspace's tracker so a worker
  can implement it without guessing: seven fixed sections, facts and required
  changes only, values spelled out, tables for mappings, acceptance criteria
  that are tests, and its OpenSpec change named. Use when asked to file,
  write or open a ticket or issue, update one whose scope changed, break work
  into sub-tasks, or clean up a ticket that describes a design that no longer
  holds. To verify a shipped ticket use `prez-rails:qa-task`; to make one ready
  for pickup use `prez-rails:curate-task`.
---

# Writing a task

The reader is the engineer or agent who implements this, with no context
beyond the ticket. Everything they need is in it; nothing that leaves what
they do unchanged is.

**Tracker.** Read the **Tracker** section of `.prez-rails/config.md`, then
the adapter it names in `${CLAUDE_PLUGIN_ROOT}/trackers/`. Every create, read,
update, link and transition below goes through that adapter.

## Two rules that override everything else

### 1. Current design only

Write the description as if the current design were the only one there had
ever been. When scope changes, **replace** the outdated sections in place;
the tracker's history keeps the old text. Dated decision headers, "supersedes
the original scope", narrated alternatives and incident tallies all belong to
the history, never the description. A superseded design left in writing
invites someone to build it.

The one exception is a **rejected approach that is still tempting and still
wrong**. Keep it in Tech decisions, as a rule: "Refunding before the meter
closes is wrong because it creates a double-payment path." That is a
constraint, not history.

### 2. Sentences in prose

Write the sentence: "When the request carries `codes`, the handler calls the
code-keyed lookup." Arrows and set symbols (`->`, `∈`, `≥`) are ambiguous in
prose ("maps to", "then", "returns"?), so they live only inside code, SQL,
type signatures and diagrams, where they are the notation.

## The seven sections

Every task and sub-task has these, in this order, all required. The only extra
section is **Slicing**, after Tech decisions, when the work spans more than
one PR.

```
## Problem statement
## Context
## Goals
## Non-goals
## Acceptance criteria
## Functional requirements
## Tech decisions
## Slicing                                    (only when more than one PR)
```

**Problem statement**: the gap as it stands today, in two or three
sentences. What the system cannot do, not the story of finding out.

**Context**: what a reader needs to place the work:

- **What we build**, in the fewest precise words: endpoint and body, event
  name and payload, screen and the vocabulary.
- **Repos covered**, by name, each with what changes there: "`api` (new
  route and migration), `web` (screen and query hook)". Name the one repo
  when there is one. A sub-task names only those of its parent's repos that
  its slice touches.
- **The OpenSpec change**, as `<repo> · openspec/changes/<change-name>/`, or
  `<workspace> · openspec/changes/<change-name>/` for one spanning repos. The
  implementing session writes it at build time, from the ticket, before any
  code. A sub-task names its parent's change and the section of `tasks.md` it
  implements. Work too small for a change says "no OpenSpec change:
  <reason>".
- **References**: ticket keys with one clause each, then brain pages and PRs.
  Real relationships between tickets are tracker links.

**Goals**: what the ticket commits to, as outcomes, in a short list.

**Non-goals**: what it does not attempt, each naming the ticket that owns it.

**Acceptance criteria**: the observable outcomes QA verifies on the shipped
behaviour. Each bullet is a test someone can write, phrased as behaviour a
person sees (a customer, an operator, a screen) in domain words, even for a
backend-only ticket. Endpoints, status codes, field and table names, flags,
retry counts and test data belong in Functional requirements; the criterion
tests the behaviour they produce. Mechanical gates (suite, lint, typecheck)
go in Tech decisions.

| Leaks the implementation | Behavioural |
|---|---|
| `POST /tips` with `amount: 0` returns 422 | A tip of zero is refused with a message saying so |
| A second `stop` within 3 s returns 409 | When someone taps stop twice, the session ends once and they are charged once |

**Functional requirements**: open with a **technical brief** of a handful of
lines: the approach, the touchpoints (module, route, table, cache,
queue), the data sources, and what was decided rather than discovered. When an
OpenSpec change already exists, the brief points at it. Then the
requirements, numbered, each a decision already made. When writing the brief
shows the approach isn't decided, say so in the ticket.

**Tech decisions**: the execution contract, everything the implementer must
not re-derive or re-argue:

- **Codebase facts**, marked "already diagnosed, don't re-derive": paths with
  line numbers, columns, enum members, cron rates, helpers. Each one read
  before it is written; a wrong fact costs more than a missing one. The
  repo's page in `.prez-rails/repos/` is the map these facts are written
  against.
- **Reuse from <KEY>**, when extending shipped work.
- **Access patterns**, when the work reads or writes stored data: the key or
  index each one uses, how often it runs, what it touches, per the **Data
  access** rule in the rails.
- **Decisions** with their alternatives closed.
- **Do not touch**: paths, not concepts.
- **Gates** the PR passes, as the repo page names them.
- **Driver**: `engineer only` or `any`, decided by `prez-rails:curate-task`.
  A ticket that touches a hard stop (**Hard stops** in the rails and the project config) is `engineer
  only`. Then **Left to the implementer**: `none`, or one line per choice the
  implementer may make.

End the section with: "Anything that contradicts these decisions is raised
before implementing, never resolved silently in the PR."

Each line lives in exactly one of Acceptance criteria (what QA verifies), the
technical brief (what the plan assumes) and Tech decisions (execution
constraints).

**Slicing**: one line per PR, in merge order, with each sub-task's key.

## Values, not shapes

A ticket that names a field without saying what goes in it is incomplete. If
the implementer would have to invent a string, it isn't done.

- A state vocabulary is a **table**: every state, its meaning, its flags, and
  the fallback row for an unrecognised value.
- A field described as "a sentence" gets **the sentence**, in the language the
  user will read it in.
- A response shape is written out, with which fields are null when.
- A mapping of three or more cases is a **table with named columns**. Tables
  force dimensions apart that arrow lists silently mix.

## Diagrams

When the work wires two or more parts together (repos, a service and its cache, a
table and its readers, a write path and a read path, a deploy
order), the ticket carries an **ASCII diagram** of that wiring, in a fenced
block right after the technical brief. It shows the parts, the data between
them, which PR owns each arrow, whether each arrow runs per request, per
write or once, and the merge and deploy order when it matters. Labels are
plain words. The diagram is rewritten in the same edit as any scope change.
Skip it only for work inside a single unit.

## Verify before asserting

Every path, line number, function, column, enum value and cron expression
goes in only after reading it on current `main` (`rails-sync <repo>`, then
the submodule folder). Re-check anything a memory told you. Read the relevant pages
of the knowledge base the project config names first; a ticket that
contradicts it is a bug in the ticket.

## Before filing

Run these, then show the full body and wait for a yes. Filing a new ticket is
the human's call; updating one the user asked you to update is not.

1. **Duplicates.** Search open and closed tickets by the component touched
   plus a domain keyword. Reuse what covers the work; mark superseded ones as
   duplicates, link them and close them. Report what the search found.
2. **Branches and PRs.** `git ls-remote --heads origin | grep -i <KEY>` and
   `gh pr list --search <KEY>` in each repo covered.
3. **The container's status.** New work goes only into a container that is
   still open; raise a closed one.
4. **Sprint or cycle.** Work started this session goes in the current one;
   work filed for later stays out. When unsure which, ask.
5. **Assignee.** The human driving the session, resolved through the adapter.
   Never unassigned, never the agent.

Filing doesn't make a ticket ready: the next step is `prez-rails:curate-task`,
never implementation.

## Writing prose

- English, except inside strings being specified, which are in the language
  the user reads.
- Business words for business concepts, technical words for technical ones.
- A claim about behaviour carries the file and line that proves it.

## Anti-patterns

- A section explaining that the scope changed
- A field named but its values left to the implementer
- A mapping written as arrow lines instead of a table
- A missing OpenSpec line, or an unstated scope ("which repos?")
- Work that wires parts together with no diagram
- Gates in Acceptance criteria, or QA outcomes in Tech decisions
- Acceptance criteria written as API or storage tests
- Paths or line numbers written from memory
- A Tech decisions section without the Driver and Left-to-the-implementer lines
