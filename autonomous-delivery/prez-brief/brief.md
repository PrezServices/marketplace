# prez brief

This workspace shapes work with **prez brief**, the product side: what to
deliver and how anyone can tell. A delivery system, when the workspace runs
one, builds what it writes.

- A ticket is filed or rewritten with `prez-brief:create-task`, by the
  contract in `${CLAUDE_PLUGIN_ROOT}/ticket.md`: the commitment (Problem
  statement to Acceptance criteria) is product's, the design (Functional
  requirements, Tech decisions) is a starting point engineering owns.
- To shape an idea before it's a ticket: `prez-brief:grilling` to stress-test
  it, `prez-brief:research` to answer a question with sources,
  `prez-brief:prototype` to try it cheaply.
- Before using one of those, read
  `${CLAUDE_PLUGIN_ROOT}/skill-overrides/<skill-name>.md` if it exists; where
  the two disagree, the override wins.
- The project's own facts (tracker, repos, knowledge base) are in
  `.prez-brief/config.md`.
