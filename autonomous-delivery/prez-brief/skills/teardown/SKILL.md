---
name: teardown
description: >-
  Remove prez brief from a workspace before uninstalling the plugin or
  switching ideation plugins: remove the project config setup wrote. Use when
  the user wants to uninstall prez brief or try a different ideation plugin.
disable-model-invocation: true
---

# Tearing down prez brief

Run from the workspace root. Teardown removes what `/prez-brief:setup`
wrote, and nothing else. Tickets already filed stay in the tracker, and the
delivery system keeps building them.

1. Show the removal: `.prez-brief/`, the whole folder. Offer to keep the
   repos table somewhere neutral first when the next plugin could use it.
2. Remove it on the user's yes, commit on a branch staging by path, and open
   a PR on the workspace repo.
3. Give the user the command, to run themselves, and say to run it only
   after teardown, since this skill goes with the plugin:

   ```sh
   claude plugin uninstall prez-brief@prezservices --scope project
   ```
