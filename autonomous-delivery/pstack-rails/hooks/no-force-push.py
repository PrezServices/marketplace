#!/usr/bin/env python3
"""PreToolUse hook on Bash: no force push and no push to main.

Denies `git push` with -f, --force or --force-with-lease, and any push whose
target is main or master. Work reaches main through a PR from a branch, and
a pushed branch is only ever moved forward with new commits. Pushes to any
other branch and every pull pass.
"""
import re
from _lib import flat, GIT, deny

if re.search(GIT + r"push\b", flat):
    if re.search(r"\s(?:-f|--force|--force-with-lease(?:=\S+)?)\b", flat):
        deny("Force push is off in this workspace. Push a new commit instead.")
    if re.search(r"\bpush\s+(?:\S+\s+)?(?:main|master)(?::\S+)?\s*$", flat) or re.search(r"\bpush\s+\S+\s+(?:HEAD:)?(?:main|master)\b", flat):
        deny("Pushing to main is off; open a PR from a branch.")
