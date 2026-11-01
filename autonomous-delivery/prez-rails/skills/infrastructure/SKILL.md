---
name: infrastructure
description: >-
  The rules for infrastructure. Use when designing, ticketing, writing or
  reviewing infra (services and their bindings, runtime config, CI and
  deploy workflows, hosting projects, databases and caches), and whenever
  work adds, provisions or reads a secret, API key, token or password
  (GitHub Actions secrets, runtime secrets, local env files, hosting
  environment variables).
---

# Infrastructure

Each topic below is one file of rules. Read every file whose topic the work
touches; a review of an infra diff reads all of them. Done when each rule in
those files is met by the work, or broken as a stated trade.

| Topic | File | Applies when the work |
| --- | --- | --- |
| Secrets | [`secrets.md`](secrets.md) | adds, provisions, renames or reads a credential, or touches how one reaches the code |

Infra is a hard stop (**Hard stops** in the rails and the project config): a ticket touching it is
`Driver: engineer only`.

## Adding a rule

A new rule joins the topic file it belongs to. A new topic gets its own file,
a row in the table above, and its trigger words in the `description`.
