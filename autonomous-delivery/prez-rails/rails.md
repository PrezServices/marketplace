# prez rails

This workspace runs **prez rails**, an autonomous delivery system: tickets are
written as contracts, curated by an engineer, built by a session from the text
alone, reviewed, deployed and QA-ed, each stage through its skill. The
workspace is a meta-repo: every folder in `.gitmodules` is a separate repo.

**Project config** is `.prez-rails/config.md` at the workspace root: tracker,
statuses, hard stops, deploys, knowledge base. Read it before the first ticket
action of a session. **Repo pages** are `.prez-rails/repos/<repo>.md`: Patterns,
Traps, Tech debt, Gates, Review bot, Deploy, QA.

## Where work happens

- Submodule folders stay clean on `main`. Read them; edit, branch and commit
  only in ticket worktrees. The guard hooks enforce this.
- Implementation happens in `tickets/<branch>/<repo>/`, created with
  `rails-new-ticket <branch> <repo>...` from the workspace root. A repo the
  ticket needs later is added with the same command. When the PRs merge,
  `rails-close-ticket <branch>`.
- Sync with `git pull && rails-sync` at the start of a session and before
  reading a submodule to answer a question about current code. Done when it
  exits 0; a non-zero exit names each repo it skipped and why.
- Submodules are `ignore = all`, so `git status` at the root hides them; check
  one with `git -C <repo> status`. At the root, stage by path.
- PRs open against each sub-repo from its worktree. The meta-repo changes only
  when the workspace itself changes.

## Tickets

| Stage | Skill |
| --- | --- |
| File or rewrite a ticket | `prez-rails:create-task` |
| Make it ready for pickup | `prez-rails:curate-task` |
| Build it | `prez-rails:implement-task` |
| Pre-review before pushing | `prez-rails:review-local` |
| Ship it | `prez-rails:deploy` |
| Prove it in the deployed system | `prez-rails:qa-task` |

Code for a ticket is built through `prez-rails:implement-task`, by the session
or by a worker it briefs, so its readiness gate (curated, `ready`) always runs.
Every implementation is tracked as a ticket; work with no ticket gets one
through `create-task` first.

## Hard stops

Work that touches any of these is `Driver: engineer only`, and an engineer
signs off on the design before code: a schema or migration; auth or
permissions; money (prices, charges, payouts, balances, ledgers); a public API
or event contract another repo or a shipped client depends on; infra (deploy
workflows, CI, runtime config, secrets); deleting code or tests; a new
dependency or service. The project config may add more.

## Pull requests

- The description opens with what the PR is for and links its ticket, then
  says what changed and how it was verified.
- One PR per repo per ticket. Stack PRs when one builds on another that is
  still open, and retarget them as the base merges.
- A pushed branch moves forward only with new commits.
- After opening or pushing, watch the review and CI to completion. Answer each
  review comment in its own thread. Mechanical fixes are the session's; design
  questions go to the human.

## Data access

Choose the established best practice for data access over the shortcut, in
any store, when designing, ticketing, writing or reviewing:

- A read reaches only the data it needs, through a key or an index, so its cost
  tracks what it returns rather than what is stored.
- When the data model can't serve a read that way, the model is the gap. Fix
  the model; keep the reader honest.
- "It's small today" describes the present, and code outlives it.

Breaking a best practice is sometimes the right trade: name the practice, the
reason and the cost, set it beside the option that keeps it, and let the user
choose. The trade is always stated.

## Time

Inside our systems, time is UTC. Store and send instants as ISO-8601 Zulu
(`2026-10-20T14:30:00Z`); keys, logs, messages and payloads between services
carry UTC. Local time lives at the edge a person reads or types, converted
from the place's IANA zone there. A rule written in local time (opening hours,
"today") converts the UTC instant at the moment of comparison. Local time in
storage, keys or contracts is a gap: name it and propose the UTC shape.

## Skills from upstream

`prez-rails:` also carries vendored copies of Matt Pocock's skills (`tdd`,
`codebase-design`, `diagnosing-bugs`, `prototype`, `wizard`, `research`,
`retro`, `grilling`, `writing-for-agents`), Cursor's (`deslop`,
`thermo-nuclear-code-quality-review`) and OpenSpec's (`openspec-*`, and the
`opsx` commands, which need the `openspec` CLI). They are used as shipped.
Where they name `/opsx:<command>`, the command here is
`/prez-rails:opsx:<command>`.
**Before using one, read `${CLAUDE_PLUGIN_ROOT}/skill-overrides/<skill-name>.md`
if it exists**; where the two disagree, the override wins. Domain language and
past decisions come from the knowledge base the project config names.
