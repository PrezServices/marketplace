---
name: teardown
description: >-
  Remove company-ops from a workspace before uninstalling the plugin: remove
  the config setup wrote and the plugin's entry in the workspace settings,
  and open a PR. Use when the user wants to uninstall company-ops or move
  its config somewhere else.
disable-model-invocation: true
---

# Tearing down company-ops

Run from the workspace root. Teardown removes what `/company-ops:setup`
wrote, and nothing else. Roadmap kit folders such as `internships/` are
content the company keeps, never part of the removal.

## 1. Show the removal

One list, before touching anything:

- `.company-ops/`, the whole folder. Offer to keep the entities table and
  standing orders somewhere neutral first when another tool could use them.
- The `company-ops@prezservices` entry in `enabledPlugins` of
  `.claude/settings.json`.

## 2. Remove and land

Make the removals the user agreed to, commit on a branch staging by path, and
open a PR on the workspace repo.

## 3. Uninstall

Give the user the command, to run themselves:

```sh
claude plugin uninstall company-ops@prezservices --scope project
```

Run teardown before uninstalling: once the plugin is gone, so is this skill.
