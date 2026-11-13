# PrezServices marketplace

The Claude Code plugins PrezServices builds and uses, in one catalog. Add it
once per machine, then install any plugin from it by name:

```sh
claude plugin marketplace add PrezServices/marketplace
claude plugin install <plugin>@prezservices --scope project
```

Use `--scope project` inside the repo a plugin is for, so the choice is
committed to that repo's `.claude/settings.json` for everyone. Each teammate
still runs the `install` line once. The repo is private: installs use your
own git credentials (`gh auth login` is enough).

## Catalog

| Plugin | Category | What it is |
| --- | --- | --- |
| [`prez-rails`](autonomous-delivery/prez-rails/) | autonomous-delivery | An autonomous delivery system for meta-repos |
| [`pstack-rails`](autonomous-delivery/pstack-rails/) | autonomous-delivery | Runs a workspace on pstack, with its entry point and agent guards |
| `pstack` | autonomous-delivery | A pointer to Cursor's pstack (`cursor/plugins`, `harness/pstack/claude-code`), so pstack-rails can install it as a dependency |
| [`company-ops`](company-ops/company-ops/) | company-ops | Runs the company, not the code: roadmaps now, CRM and outreach next |

The catalog is `.claude-plugin/marketplace.json`. Plugins are grouped by
category, one folder per category.

## Where a plugin lives

The catalog is meant to hold **pointers**: a plugin lives in its own repo, and
its entry here names that repo pinned to a tag or commit:

```json
{ "name": "<plugin>", "category": "<category>",
  "source": { "source": "github", "repo": "PrezServices/<plugin>", "ref": "v1.0.0" } }
```

A young plugin can **incubate** in its category folder here, listed by
relative path (`"source": "./<category>/<plugin>"`). Move it to its own repo
when another team adopts it, when it needs its own release tags, or when its
visibility should differ from this repo's. Only the entry's `source` changes;
the install name stays `<plugin>@prezservices`.

## Adding a plugin

Add its entry to `.claude-plugin/marketplace.json` and a row to the catalog
table above, then validate with `claude plugin validate .`.
