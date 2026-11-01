# <repo>

<one line: what this repo is>

## Patterns

How the repo is organized, so a new piece lands where its siblings do.

## Traps

What has already cost a session time here, one line each. Grows from the
**Traps hit** sections of merged PRs.

## Tech debt

What we know is bad and are fixing slowly.

## Gates

The exact commands a PR must pass, as the repo runs them.

## Review bot

The workflow that reviews PRs, the reviewer it runs, and where its stance
lives. `none` when there is no bot.

## Deploy

Trigger (on merge, on dispatch, platform), environments, workflow, inputs,
order constraints, the artifact that proves a rollout and the smoke check,
side steps, rollback, traps.

## QA

Where and how to drive a scenario in each environment, the test identities,
where the evidence lives (logs, stores, screens), and what must never be
driven.
