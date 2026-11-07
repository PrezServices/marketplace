# prez brief

The product side of autonomous delivery: it shapes work and writes the
ticket a delivery system builds. If the delivery system is the engineering
team, prez brief is the product team. It is optional: a workspace runs one
delivery system, and may add prez brief in front of it.

- **Tickets.** `/prez-brief:create-task` files or rewrites a ticket in
  Linear, Jira or GitHub Issues with the seven sections of
  [the ticket contract](../ticket.md): the commitment (Problem statement to
  Acceptance criteria) and a starting design (Functional requirements, Tech
  decisions) that engineering owns from there.
- **Shaping an idea first.** `grilling` stress-tests a plan, `research`
  answers a question with sources (durable findings go to the knowledge
  base), `prototype` tries an idea cheaply.

It works with any delivery system that reads the contract: pstack rails
picks a ticket up with "implement <KEY>"; prez rails curates it first.

## Use it

In the workspace:

```sh
claude plugin marketplace add PrezServices/marketplace --scope project
claude plugin install prez-brief@prezservices --scope project
```

Start Claude there and run `/prez-brief:setup`. It writes
`.prez-brief/config.md` (tracker, repos, knowledge base), copying the tracker
from the delivery system's config when there is one, and opens a PR.

To remove it: `/prez-brief:teardown`, then
`claude plugin uninstall prez-brief@prezservices --scope project`.

## What's in here

| Path | What it is |
| --- | --- |
| `brief.md` | What session start injects in a set-up workspace |
| `ticket.md` | A copy of the [ticket contract](../ticket.md) |
| `hooks/` | Session start |
| `skills/create-task` | Writes the ticket |
| `skills/grilling`, `skills/research`, `skills/prototype` | Matt Pocock's ([mattpocock/skills](https://github.com/mattpocock/skills), MIT), recorded in `skills-lock.json` and used as shipped |
| `skill-overrides/` | Our changes to those, read before using one |
| `trackers/` | One adapter per tracker: Linear, Jira, GitHub Issues |
| `skills/setup`, `skills/teardown`, `templates/config.md` | The contract's setup and teardown |

## Tests

```sh
python3 hooks/test_session_start.py
```
