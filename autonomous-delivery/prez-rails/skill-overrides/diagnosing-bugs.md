# diagnosing-bugs: our changes

These apply when the bug is in a deployed system. Bugs you can reproduce in
local code follow the skill as written.

- **Production is read-only.** There, the feedback loop is reading evidence:
  logs, stored rows, read-only queries. A diagnosis built from that evidence is
  valid without a repro, so keep going without a loop.
- **Repros run where the repo page's QA section allows**: a non-production
  environment, or production with the test identities and flows it marks
  safe. Production config and data stay as they are.
- **Run anything that sends a message, moves money or reaches a real user once,
  on purpose, with a test identity.** Loops, parallel runs and stress tests
  stay away from those paths.
