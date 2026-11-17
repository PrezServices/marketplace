# pstack rails

This workspace delivers through **pstack**, installed at `${PSTACK_ROOT}`.

<!-- with tracker -->
- Work starts from a ticket. File one with `pstack-rails:create-task`; pick
  one up with "implement <KEY>" (`pstack-rails:implement-task`), which hands
  it to `/pstack:poteto-mode`. Work with no ticket gets one first. Curation
  is the user's call: when a ticket is only an idea, suggest they run
  `/pstack-rails:curate-task <KEY>`.
- You own a ticket until its acceptance criteria are proven on the last
  stage the repo deploys to, which is production where one exists. An open
  PR is the middle: `pstack-rails:ship-task` gets it green, verified, merged,
  deployed and QA-ed on each stage, and you fix what QA finds. Pause only
  for what reaches a customer, moves money or deletes data, and for the
  gates in the config's standing orders.
<!-- without tracker -->
- This workspace has no tracker: start work with `/pstack:poteto-mode`
  directly. Each PR description says what it is for, what changed and how it
  was verified.
- You own a change until it is proven on the last stage the repo deploys to,
  which is production where one exists. An open PR is the middle:
  `pstack-rails:ship-task` gets it green, verified, merged, deployed and
  QA-ed on each stage, and you fix what QA finds. Pause only for what
  reaches a customer, moves money or deletes data, and for the gates in the
  config's standing orders.
<!-- end -->
- `/pstack:poteto-mode` reads the request and chooses its own playbook and
  skills.
- Open a pstack skill by its `SKILL.md` under `${PSTACK_ROOT}/skills/`, and
  map Cursor names with `${PSTACK_ROOT}/docs/harness/claude-code.md`.
- Subagents run as `pstack:poteto-agent`, or `pstack:comment-sicko` for the
  no-comments pass; a read-only look may use `Explore`. A hook refuses any
  other type, in the `Agent` tool and in `Workflow` scripts alike.
- When pstack names a skill from `cursor-team-kit` (`/deslop`, `control-ui`,
  `control-cli`), it is `/pstack-rails:<name>` here.
<!-- with tracker -->
- Submodule folders stay clean on `main`. Each ticket works in
  `tickets/<branch>/<repo>/` worktrees, which `implement-task` creates.
<!-- without tracker -->
- Submodule folders, when there are any, stay clean on `main`. A change works
  in `tickets/<branch>/<repo>/` worktrees
  (`git -C <repo> worktree add ../tickets/<branch>/<repo> -b <branch> origin/main`).
<!-- end -->
- Stage by path at the root. Guards refuse edits and git writes in a
  submodule folder, sweeping adds at the root, force pushes and pushes to
  `main`.
- The project's own facts (tracker, repos, delivery stages, standing orders) are in
  `.pstack-rails/config.md`. Read it before the first change of a session.
