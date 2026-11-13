# company-ops

Runs the company, not the code. company-ops standardises the documents and
records a company keeps, on one workspace config of entities, knowledge base
and conventions, so that any session in the workspace produces the same
shape without having seen the last one.

| Skill | What it does |
| --- | --- |
| `/company-ops:setup` | Writes `.company-ops/config.md` (entities, knowledge base, CRM adapter and stage map, document conventions, standing orders) and opens a PR |
| `/company-ops:teardown` | Removes what setup wrote and opens a PR |
| `/company-ops:create-roadmap <topic>` | Builds or updates a roadmap for a line of work that runs on external windows and deadlines (funding, hiring, certification, partnerships): one doc with nine fixed sections that leads with the decision to act on now, plus a numbered kit of drafts in the repo |

The `crm` skill and its first adapter arrive in PRE-13. The CRM section of
the config and the adapter contract in `crms/README.md` are already here, so
setup asks which CRM the workspace uses today.

## Use it

In the workspace:

```sh
claude plugin marketplace add PrezServices/marketplace --scope project
claude plugin install company-ops@prezservices --scope project
```

Start Claude there and run `/company-ops:setup`. From the next session on,
`/company-ops:create-roadmap <topic>` builds a roadmap.

To remove it: `/company-ops:teardown`, then
`claude plugin uninstall company-ops@prezservices --scope project`.

## How the config works

Every skill reads `.company-ops/config.md` before its first action and stops
with one line naming setup when the file is missing. The skills carry no
company facts of their own: the entities, the knowledge base path, the CRM
and its stage names, the title pattern and the languages all come from the
config. A workspace changes a fact by editing the file or re-running setup.

External systems are adapters. The CRM a workspace uses is one line in the
config, and switching CRMs is a new file in `crms/` plus that line. The
`crm` skill does not change.

## What's in here

| Path | What it is |
| --- | --- |
| `skills/setup`, `skills/teardown` | Write and remove the config |
| `skills/create-roadmap` | The roadmap skill |
| `crms/` | The CRM adapter contract (`README.md`) and one adapter per CRM |
| `templates/config.md` | What `setup` fills in |

## Adding a skill

Write `skills/<name>/SKILL.md` with `name` and `description` in its
frontmatter. Open with who reads its output and what they need from it. Read
the config first and stop when it is missing. Put every company fact the
skill needs in the config template, never in the skill. Add a row to the
table at the top of this file, bump `version` in `.claude-plugin/plugin.json`,
and validate from the marketplace root:

```sh
claude plugin validate .
```
