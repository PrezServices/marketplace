---
name: crm
description: >-
  Record and review the company's people, companies and deals in whatever
  CRM the workspace names: capture a lead, log a call or message as a touch
  note, move a deal through the pipeline, add a deal, review the pipeline or
  the last touches. Use when asked to record a lead or contact, log a
  conversation, move or add a deal, or ask what is in the pipeline and who
  was last spoken to.
---

# Working the CRM

The reader of what this skill writes is the next person who opens the
record, often the user a month later. Every touch note says what happened
and what comes next, in one fixed shape, so a timeline reads as one story.

**Config.** Read `.company-ops/config.md` first. When it is missing, say so
in one line, name `/company-ops:setup`, and stop. Its **CRM** section names
the adapter, the workspace, the default owner and the stage map. When the
adapter is `none`, say the workspace has no CRM, in one line, and stop.
Otherwise read `${CLAUDE_PLUGIN_ROOT}/crms/<adapter>.md` and do every
operation below the way it says. The vocabulary is in
`${CLAUDE_PLUGIN_ROOT}/crms/README.md`.

## Two rules that override everything else

**Writes are shown first.** A write that creates or changes a record is one
line of plan before the call, in the form "Create person Ana Pérez at Acme,
note: Event · 2026-11-13", and runs on the user's yes. Reads run without
asking. A record in the CRM is customer data, and a wrong write is visible
to everyone who opens it.

**Identity is resolved, never guessed.** Before any write, find the person
or company by the adapter's identity order. Exactly one match proceeds.
None creates. Two or more stop the operation and show the candidates for
the user to pick.

## Operations

Match the request to one of these. A request that spans two (a lead met at
an event who already has a deal) runs them in the order listed.

### Capture

"Record <name> from <company> as a lead, met at <event>."

1. Find the company by domain, then by name. Find the person by the
   identity order.
2. Upsert the company, then the person linked to it, with the lead source
   and where they were met when the request says.
3. Log one touch note on the person with channel `Event` or what the
   request names, dated today, saying where they were met.
4. When the request names an opportunity, run **Add to pipeline**.

### Log

"Log this call", "log it", a pasted WhatsApp or email exchange.

1. Find the person. Find their open deal when one exists.
2. Write one touch note in this shape, in the language the conversation
   happened in, on the person, and the same note on the deal when there is
   one:

   ```
   <Channel> · <YYYY-MM-DD> · <owner first name>
   <Two to four sentences of what was said and decided.>
   Next: <action> by <YYYY-MM-DD>, or "none".
   ```

   Channels: `WhatsApp`, `Email`, `Call`, `Meeting`, `LinkedIn`, `Event`,
   `Other`.
3. When there is a deal and the note's Next line carries a date, move the
   deal's next-step date to it.

### Move

"Move <deal> to proposal."

1. Find the deal by name, then by its person or company.
2. Map the logical stage through the config's table. An unmapped stage
   stops here, with one line saying which stage has no mapping and that
   nothing changed.
3. Set the stage.

### Add to pipeline

"Add a deal for <company>", or the last step of Capture.

1. Find the person and the company.
2. Create the deal, linked to both, owned by the default owner, with the
   value when the request gives one, in the lowest mapped logical stage.
   Say which stage that is when it is not `lead`.

### Review

"What's in the pipeline", "who did we last talk to", "what's due this
week".

1. Read open deals, or people, from the CRM. Never answer from memory or
   from an earlier reply.
2. Reply with one table:

   | Review | Columns |
   | --- | --- |
   | Pipeline | Deal, Stage, Owner, Value, Last touch, Next step |
   | People | Person, Company, Last touch, Next step |

   Sorted by next step, soonest first, then by last touch, oldest first.
   A deal or person with no touch note shows "none" in Last touch.

## Anti-patterns

- A write without its one-line plan and the user's yes
- A phone number used alone to match a person
- A note in free prose instead of the fixed shape
- A review answered from memory
- A stage name typed from the CRM instead of the config's table
- Changing the CRM's data model from this skill; the adapter says what
  goes through the CRM's own UI
