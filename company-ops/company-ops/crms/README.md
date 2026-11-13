# CRMs

The `crm` skill describes *what* to do with a person, a company or a deal.
*How* to do it in a given CRM lives in one adapter file here. The workspace
picks the adapter in the **CRM** section of `.company-ops/config.md`,
together with the values only the workspace knows: the workspace slug, the
default owner, and the real name of each stage.

Before a skill's first CRM call in a session, read the **CRM** section of
`.company-ops/config.md` and then the adapter it names. When the two
disagree, the config wins. With `none`, the skill stops with one line.

| Adapter | CRM |
| --- | --- |
| *none yet* | PRE-13 adds `attio.md`, Attio through the Attio MCP |

## The vocabulary the skills use

### Kinds

| Kind | What it is |
| --- | --- |
| **person** | One human the company talks to |
| **company** | The organisation a person belongs to |
| **deal** | One opportunity with a company, with a value and a stage |
| **pipeline** | The ordered stages a deal moves through |
| **touch** | One contact with a person: a message, a call, a meeting, an event |
| **owner** | The workspace member responsible for a person or a deal |

### Stages

The skills move deals between these logical stages. The workspace maps each
one to the CRM's real stage name. A logical stage the workspace leaves
unmapped is skipped, and the skill says so instead of inventing one.

| Logical stage | Meaning |
| --- | --- |
| `lead` | Known, not contacted |
| `contacted` | First touch sent |
| `qualified` | They replied and fit |
| `proposal` | A proposal or price is with them |
| `won` | Signed or paid |
| `lost` | Said no, or silent past the follow-up rule |

### Operations

Every adapter says how to do each of these, and what goes wrong:

- **find** a person or a company by identity (email, a unique id, name plus
  company), and what to do when more than one matches
- **upsert a person**, linked to a company
- **upsert a company**
- **create a deal**, linked to a person and a company, in a stage
- **log a touch** on a person, and on the deal when there is one
- **move a deal** to a stage
- **add to pipeline**: a deal in `lead`
- **review**: deals by stage with owner, value and last touch; people by last
  touch and next step
- **resolve the owner** from the human's email

## Adding a CRM

Write `<crm>.md` with one section per operation above, plus a **Traps**
section. Add a row to the table at the top. Then a workspace can name it.
