# company-ops config

The company's own facts for the company-ops skills. Written by
`/company-ops:setup`; edit it by hand or re-run setup. Removed by
`/company-ops:teardown`. Every company-ops skill reads this file before its
first action and stops when it is missing.

## Entities

The legal entities the company works through. A roadmap evaluates each one
against a programme's thresholds; the CRM owner and the kit's fixed facts
come from the first row.

| Entity | Legal form | Country | Role |
| --- | --- | --- | --- |
| `<name>` | `<SpA, Ltda, holding, …>` | `<country>` | `<applicant, holding, past venture>` |

## Knowledge base

- **Path:** `<path to the wiki folder, such as prez-brain/wiki/>`

## CRM

- **Adapter:** `<attio | none>` (`${CLAUDE_PLUGIN_ROOT}/crms/<adapter>.md`)
- **Workspace:** `<the CRM workspace slug or URL>`
- **Default owner:** `<email>`

With `none`, the workspace has no CRM: `/company-ops:crm` stops with one
line, and the workspace, owner and stage table below are removed.

| Logical stage | Stage in the CRM |
| --- | --- |
| `lead` | |
| `contacted` | |
| `qualified` | |
| `proposal` | |
| `won` | |
| `lost` | |

A stage left blank is skipped by the skills, which say so.

## Documents

- **Roadmaps live in:** Claude Docs, one tab per roadmap
- **Title pattern:** `Prez Services — <Topic> Roadmap (<Country>)`
- **Doc language:** English
- **Kit language:** Spanish, in a numbered folder at the workspace root named after the topic

## Conventions

- Legend on every landscape table: `C = confirmed on an official page, I = inferred`.
- One named owner per action.
- Absolute dates. A date chip only where someone acts on it.
- Unknowns bracketed, never invented.

## Standing orders

The operator's orders and gates for this workspace, read before acting. Keep
them short.

- none
