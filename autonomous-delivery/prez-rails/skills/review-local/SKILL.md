---
name: review-local
description: >-
  Review your own changes the way the repo's PR review bot will, before you
  push: the same reviewer, stance and repo context, plus the ticket's scope
  walls and acceptance criteria. Use before pushing a branch or opening or
  updating a PR, or when asked to "review locally", "pre-review" or "check
  this before the bot does".
---

# Review locally

The bot that reviews every PR builds its review from files in the repo. This
skill loads the same files, runs the same reviewer on the local diff, and adds
the two checks the bot can't make: the ticket's scope walls and its acceptance
criteria. You fix most of what the bot would flag before you push. Nothing is
posted anywhere.

Run it from the repo's worktree (`tickets/<branch>/<repo>/`), once per repo.

## 1. Pin the diff

```sh
git fetch -q origin main
base=$(git merge-base origin/main HEAD)
git diff "$base"                 # committed and uncommitted
git diff --name-status "$base"
git log --oneline "$base"..HEAD
```

An empty diff ends the review; say so.

## 2. Load what the bot loads

Find the review workflow: `.github/workflows/` in the worktree, the file
whose job runs a reviewer on `pull_request`. The repo page
(`.prez-rails/repos/<repo>.md`, **Review bot**) names it when known. From
it, take:

- **The reviewer**: a Claude Code plugin or skill (`code-review`, …) and its
  arguments, or the prompt and rubric files it reads.
- **The stance**: an `--append-system-prompt`, a `prompt:` or a system prompt
  file. Read it as instructions to you for this review.
- **The context**: the repo's `CLAUDE.md` and `AGENTS.md`, which the bot loads
  as repository context.

Every file the bot reads from elsewhere (another repo, a URL) is fetched from
the same ref the bot uses. **If any load fails, stop and report which one.** A
review with part of its rubric missing looks clean when it isn't.

## 3. Get the ticket

Take the key from the branch name and read the ticket through the workspace's
tracker adapter (**Tracker** in `.prez-rails/config.md`). Pull out its
Acceptance criteria, **Repos covered** and **Do not touch**. With no key, or
no criteria, say so and skip step 5.

**Scope walls, before anything else.** This repo is in Repos covered, and no
path in `git diff --name-status "$base"` matches Do not touch. Each miss is a
`critical` finding with the path and the ticket line it breaks. These are the
walls a curated ticket sets for a driver who can't read code, so they keep
their severity through step 6; the fix is reverting the file or sending the
ticket back to its curator.

## 4. Run the reviewer

- **The bot runs a plugin or skill you have** (for example the `code-review`
  skill): run it on the local diff at its high effort level, with the stance
  from step 2 in front of you, without posting.
- **The bot runs its own prompts**: apply them as instructions, section by
  section, finishing one section before the next. Mixing them is how findings
  get bundled.

Every finding carries severity (`critical`, `high`, `medium`, `low`,
`info`), file, line, what's wrong, the fix, and whether it is new in this
diff or pre-existing. Pre-existing findings count only at `critical` or
`high`.

## 5. Check the acceptance criteria

For each criterion record **covered** (file and function), **missing** or
**can't tell from the diff**. Missing is a `high` finding.

Check the criterion against the code itself; a passing test often asserts less
than the criterion says. For "X never appears", search for every form of X in
what ships.

## 6. Verify every finding

Try to disprove each finding against the code, the commit messages and the
repo context: confirmed, rejected or downgraded. Drop the rejected ones.
Scope-wall findings stay as they are.

## 7. Report and act

One table, by severity: severity, `file:line`, title, what you did.

If you're the one implementing:

- **Fix every `critical`, `high` and `medium` before you push.** When you think
  one is wrong, leave the code and write down why; that note is your reply if
  the bot raises it on the PR.
- **List `low` and `info`**, fixing only the trivial ones inside lines you
  already changed.
- Re-run the gates for the files you touched. Run this review again only when a
  fix changed more than the lines its finding named.

The bot may still raise things this pass missed. Expect fewer findings on the
PR, not zero.
