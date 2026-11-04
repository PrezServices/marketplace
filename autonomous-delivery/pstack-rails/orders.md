# pstack rails

This workspace delivers through **pstack**, installed at `${PSTACK_ROOT}`.

- Work starts from a ticket. File one with `pstack-rails:create-task`; pick
  one up with "implement <KEY>" (`pstack-rails:implement-task`), which hands
  it to `/pstack:poteto-mode`. Work with no ticket gets one first.
- `/pstack:poteto-mode` reads the request and chooses its own playbook and
  skills.
- Open a pstack skill by its `SKILL.md` under `${PSTACK_ROOT}/skills/`, and
  map Cursor names with `${PSTACK_ROOT}/docs/harness/claude-code.md`.
- Subagents run as `pstack:poteto-agent`, or `pstack:comment-sicko` for the
  no-comments pass; a read-only look may use `Explore`. A hook refuses any
  other type, in the `Agent` tool and in `Workflow` scripts alike.
- When pstack names a skill from `cursor-team-kit` (`/deslop`, `control-ui`,
  `control-cli`), it is `/pstack-rails:<name>` here.
- The project's own facts (tracker, repos, deploys, standing orders) are in
  `.pstack-rails/config.md`. Read it before the first change of a session.
