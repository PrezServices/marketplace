# The ticket

The ticket is where ideation hands work to implementation: an ideation plugin
writes it, an implementation plugin builds it. Both follow this page, and each
ships a copy of it as its own `ticket.md`, so a change here is copied into
every plugin in the same PR.

## Sections

Every task and sub-task has these, in this order. **Slicing** is added after
Tech decisions only when the work spans more than one PR.

| Section | Half | What it holds |
| --- | --- | --- |
| Problem statement | commitment | The gap as it stands today, in two or three sentences |
| Context | commitment | What we build, **Repos covered** (each with what changes there), references |
| Goals | commitment | What the ticket commits to, as outcomes |
| Non-goals | commitment | What it does not attempt, each naming the ticket that owns it |
| Acceptance criteria | commitment | Observable behaviour a person can check, each one a test |
| Functional requirements | design | A short technical brief, then numbered requirements |
| Tech decisions | design | Codebase facts, reuse, access patterns, decisions with reasons, do-not-touch paths, gates |
| Slicing | design | One line per PR, in merge order, with each sub-task's key |

## The two halves

- **The commitment** (Problem statement to Acceptance criteria) is product's:
  what gets delivered, and how anyone can tell. Implementation builds to it
  and doesn't change it. An objection to it goes to the human, with the
  evidence and the alternative, and waits for their call.
- **The design** (Functional requirements to Slicing) is engineering's: the
  best current answer to how. Ideation writes a starting design from what it
  knows; implementation may revise it, its own way (pstack revises it while
  building; prez rails curates it before), and writes each change back.

## Writing rules

- **Current design only.** A rewrite replaces the outdated text in place; the
  tracker's history keeps the old version. A rejected approach that is still
  tempting stays, in Tech decisions, as a rule with its reason.
- **Values, not shapes.** A field names its values; a mapping of three or more
  cases is a table.
- **Verified facts.** Every path, line number and name was read on current
  `main` before it went in.

## Statuses

The logical statuses each plugin maps to the tracker's real ones. A plugin
uses the ones its stages need and skips an unmapped one, saying so.

| Logical status | Meaning |
| --- | --- |
| `backlog` | Filed, not started |
| `ready` | Curated for pickup (used by delivery systems with a curation step) |
| `in-progress` | Being built |
| `in-review` | A PR is open |
| `ready-to-deploy` | Verified short of where the criteria ask (used by delivery systems with a QA stage) |
| `done` | Delivered |
| `blocked` | Waiting on something outside the ticket, with a comment naming what |
| `cancelled` | Not doing it |
