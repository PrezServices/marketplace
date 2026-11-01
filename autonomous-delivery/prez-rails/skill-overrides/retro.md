# retro: our changes

- **Steering files** are `CLAUDE.md` files (the meta-repo's for what holds
  across repos, each sub-repo's for that repo) and the repo pages in
  `.prez-rails/repos/`. A trap or pattern a session learned goes in the repo
  page.
- **A fix to an upstream skill** (Matt Pocock's, Cursor's, OpenSpec's) goes in
  `skill-overrides/<skill-name>.md` in the prez-rails plugin, through a PR on
  the plugin. The vendored skill stays as shipped.
- **A rule of the rails themselves** (a stage, a hard stop, a PR rule) is a
  prez-rails change: draft it as a PR on the plugin, never as a local edit.
