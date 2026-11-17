# pstack rails

This workspace delivers through **pstack**, installed at `${PSTACK_ROOT}`.

<!-- with tracker -->
- Work starts from a ticket. File one with `pstack-rails:create-task`; pick
  one up with "implement <KEY>" (`pstack-rails:implement-task`), which hands
  it to `/pstack:poteto-mode`. Work with no ticket gets one first. Curation
  is the user's call: when a ticket is only an idea, suggest they run
  `/pstack-rails:curate-task <KEY>`.
<!-- without tracker -->
- This workspace has no tracker: start work with `/pstack:poteto-mode`
  directly. Each PR description says what it is for, what changed and how it
  was verified.
<!-- end -->
- You own the work until it is proven on the last stage the repo deploys to,
  which is production where one exists. An open PR is the middle:
  `pstack-rails:ship-task` gets it green, verified, merged, deployed and
  QA-ed on each stage, and you fix what QA finds. Pause only where that
  skill's "When you stop" table says.
- `/pstack:poteto-mode` reads the request and chooses its own playbook and
  skills.
- Open a pstack skill by its `SKILL.md` under `${PSTACK_ROOT}/skills/`, and
  map Cursor names with `${PSTACK_ROOT}/docs/harness/claude-code.md`.
- Subagents run as `pstack:poteto-agent`, or `pstack:comment-sicko` for the
  no-comments pass; a read-only look may use `Explore`. A hook refuses any
  other type, in the `Agent` tool and in `Workflow` scripts alike.
- When pstack names a skill from `cursor-team-kit` (`/deslop`, `control-ui`,
  `control-cli`), it is `/pstack-rails:<name>` here.
- Submodule folders follow origin, not the commit this workspace records, and
  that commit is never bumped. Each folder sits on its branch (`submodule.<name>.branch`
  in `.gitmodules`, `main` when unset) at origin's latest commit. At session
  start, and before you read a submodule folder to answer a question about
  current code, run `git pull && ${RAILS_ROOT}/scripts/sync` from the workspace
  root. Exit 2 names the folders it skipped and does not block work. Any other
  non-zero exit is an error: say so.
<!-- with tracker -->
- Submodule folders stay clean. Each ticket works in
  `tickets/<branch>/<repo>/` worktrees, which `implement-task` creates.
<!-- without tracker -->
- Submodule folders, when there are any, stay clean. A change works in
  `tickets/<branch>/<repo>/` worktrees. Run `${RAILS_ROOT}/scripts/sync <repo>`,
  then `git -C <repo> worktree add ../tickets/<branch>/<repo> -b <branch> origin/<the repo's branch>`.
<!-- end -->
- Stage by path at the root. Guards refuse edits and git writes in a
  submodule folder, sweeping adds at the root, force pushes and pushes to
  `main`.
- The project's own facts (tracker, repos, delivery stages, standing orders) are in
  `.pstack-rails/config.md`. Read it before the first change of a session.
