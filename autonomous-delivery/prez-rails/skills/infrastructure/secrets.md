# Secrets

**GitHub is the source of truth.** A credential lives as a GitHub Actions
secret, and the deploy workflow syncs it into the runtime on every deploy.
Values set by hand in a dashboard drift and get overwritten, so they are
avoided.

- **Org or repo.** A credential more than one repo uses (the Cloudflare
  account token and ids, `CLAUDE_CODE_OAUTH_TOKEN`) is an **organization**
  secret. One only a single repo uses is a **repository** secret. Either way,
  GitHub never shows the value again; a moved or recreated repo or org gets
  its values re-entered by a human.
- **Reaching the runtime.** A new runtime secret is a change in one PR to
  every place the sync names it: the deploy workflow's sync list, the env the
  step passes, and the runtime's typed config. For a Cloudflare Worker that is
  the wrangler-action `secrets:` list, the step's `env:` and the `Env` type.
  Leave a name out of the sync until its GitHub secret exists: syncing an
  empty one clobbers whatever value is set.
- **Absent means off.** Code reads a missing secret as "feature unavailable"
  and answers with a clear error (for example a 503 naming the feature),
  never a crash.
- **Non-secret config** (ids, URLs, feature switches) goes in the runtime's
  plain config (`vars` in a wrangler config) or the platform's plain
  environment variables, not in a secret.
- **Local development** reads secrets from git-ignored files (`.dev.vars`
  for Workers, `.env*.local` for Vite). Commit an `.example` file with
  every name and no values.
- **The browser holds no secrets.** Every variable a frontend build exposes
  (`VITE_*`, `NEXT_PUBLIC_*`) ships inside the JavaScript bundle and is
  public. A credential the webapp needs is fetched
  from the server at runtime, scoped to the user.
- **Migrations-only credentials** (the direct, unpooled database URL) stay in
  CI and never sync into the runtime.

A secret set by hand in a dashboard, a credential in a frontend build variable, or
a value committed to the repo is a gap. Name it in the ticket or review and
propose the GitHub-secret shape beside it.

A credential that genuinely can't follow this (a per-environment value the
workflow can't select yet, a platform that can't read from GitHub) is a trade.
Name the reason and the cost, set it beside the rule, and let the user choose.
