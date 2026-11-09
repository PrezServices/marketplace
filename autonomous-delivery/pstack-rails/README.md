# pstack rails

Runs a workspace on [pstack](https://github.com/cursor/plugins/tree/main/pstack),
Lauren Tan's rigorous agent workflows, published by Cursor with its own
Claude Code adapter. pstack decides how
the work is done: `/pstack:poteto-mode` reads each request and picks its
playbook and skills. pstack rails adds what a workspace needs around it:

- **The entry point survives compaction.** A session-start hook, on startup,
  resume, clear and compaction, points the session at `/pstack:poteto-mode`
  and the newest installed pstack. It says where to start, not what to do.
- **Subagents stay pstack agents.** Guards on `Agent` and `Workflow` refuse a
  spawn that isn't `pstack:poteto-agent`, `pstack:comment-sicko`, a read-only
  `Explore`, or an agent whose prompt names an installed pstack `SKILL.md`.
  The refusal names the fix.
- **Tickets before pstack.** `/pstack-rails:create-task` files a ticket with
  seven fixed sections (problem, context, goals, non-goals, acceptance
  criteria, functional requirements, tech decisions) in Linear, Jira or
  GitHub Issues. "implement <KEY>" (`pstack-rails:implement-task`) reads it,
  moves it to in progress, hands it to `/pstack:poteto-mode`, and links the
  PRs. No curation step: pstack does its own planning. **Optional:** a repo no
  one team owns (a shared platform repo where any team adds its piece) sets
  the tracker to `none` and sends work straight to `/pstack:poteto-mode`.
- **Curation.** `/pstack-rails:curate-task <KEY>`, run by a person (Claude
  doesn't start it on its own), takes a ticket anyone wrote,
  often someone non-technical, to ready: it keeps the author's goals and
  criteria, has `/pstack:poteto-mode` design the how (`how` and `architect`, or
  a multi-phase plan for big work), writes the design and slices into the
  ticket, and asks the author in plain language about anything unclear.
  Optional: "implement <KEY>" works on an uncurated ticket too.
- **Workspace guards**, the same as prez rails': submodule folders stay clean
  on `main` (work happens in `tickets/<branch>/<repo>/` worktrees), no
  sweeping `git add` at the root, no force push or push to `main`.
- **The cursor-team-kit skills pstack names**, ported: `/pstack-rails:deslop`,
  `/pstack-rails:control-ui`, `/pstack-rails:control-cli`. cursor-team-kit has
  no Claude Code build.
- **Setup and teardown**, per the [delivery system contract](../README.md).

It packages the pstack enforcement from `PrezServices/autonomous-delivery`
(Diego's), rewritten as plain Python hooks so a workspace needs no toolchain.
That repo's merge gate and mise tasks stay there.

## Use it

In the workspace:

```sh
claude plugin marketplace add PrezServices/marketplace --scope project
claude plugin install pstack-rails@prezservices --scope project
```

The install brings pstack along: pstack rails depends on `pstack`, which this
marketplace lists as a pointer to Cursor's repo (`cursor/plugins`,
`harness/pstack/claude-code`), fetched from there and not copied.

Start Claude there and run `/pstack-rails:setup`. It runs pstack's own setup
(models and budget per role) as one of its steps, so there's one setup, not
two. It also maps your tracker's statuses, writes `.pstack-rails/config.md`,
and opens a PR. From the next session on, file work with
`/pstack-rails:create-task` and start it with "implement <KEY>".

To remove it, or to switch delivery systems: `/pstack-rails:teardown`, then
`claude plugin uninstall pstack-rails@prezservices --scope project` and
`claude plugin prune --scope project`, which removes pstack too.

## What's in here

| Path | What it is |
| --- | --- |
| `orders.md` | What session start injects in a set-up workspace |
| `hooks/` | Session start; the `Agent` and `Workflow` guards, with `workflow_scan.py`, which reads `agent()` calls without running the script; and the workspace guards (`no-*.py`) |
| `skills/create-task`, `skills/curate-task`, `skills/implement-task` | File a ticket; take it to ready with pstack designing the how; pick it up and hand it to pstack |
| `trackers/` | One adapter per tracker: Linear, Jira, GitHub Issues |
| `skills/setup`, `skills/teardown` | The contract's two skills |
| `skills/deslop`, `skills/control-ui`, `skills/control-cli` | Ported from cursor-team-kit; never edited by hand |
| `ported.json` | The source, pinned commit and file hashes of every ported skill |
| `scripts/port-cursor-plugin.py` | Copies the ported skills and checks them |
| `templates/config.md` | What `setup` fills in |

## Porting Cursor plugins

Cursor and Claude Code read the same `SKILL.md`, so a skill ports by copying
its folder with the source's LICENSE. `ported.json` lists what to take:

```sh
python3 scripts/port-cursor-plugin.py           # copy at the pinned commits, record hashes
python3 scripts/port-cursor-plugin.py --latest  # move each source to its newest commit first
python3 scripts/port-cursor-plugin.py --check   # offline: fail on a hand-edited or missing file
```

The script lists lines naming something only Cursor has (`.mdc` rules,
`generalPurpose` or `readonly` subagents, `~/.cursor` paths), for a person to
judge. Only skills port today. Cursor agents (frontmatter like `model: fast`,
`is_background`) and `.mdc` rules need a translation step, added when a skill
pstack uses needs one.

To add a skill, list it in `ported.json`, run the script, review the diff,
bump `version` in `.claude-plugin/plugin.json`, and open a PR.

## Tests

```sh
python3 hooks/test_hooks.py
python3 hooks/test_guards.py
python3 scripts/port-cursor-plugin.py --check
```

Add a case with every guard rule change.
