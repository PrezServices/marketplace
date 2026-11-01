#!/usr/bin/env python3
"""PreToolUse hook on Edit, Write, MultiEdit, NotebookEdit and Bash: keeps the
submodule folders (every path in .gitmodules) clean on main.

Denies a file edit whose path is inside a submodule folder, and a git write
(commit, add, push, checkout, switch, reset, rebase, merge, stash, cherry-pick,
am) that acts inside one, whether from the cwd, `git -C <dir>` or `cd <dir> &&`.
Reads like `git status` pass, and tickets/<branch>/<repo>/ worktrees are not
submodule folders, so all work there passes.
"""
import re
from _lib import tool, inp, flat, GIT, deny, in_submodule, git_dirs

if tool in ("Edit", "Write", "MultiEdit", "NotebookEdit"):
    path = inp.get("file_path") or inp.get("notebook_path") or ""
    sub = in_submodule(path) if path else None
    if sub:
        deny(f"{sub}/ is a submodule folder and stays clean on main. "
             f"Work in tickets/<branch>/{sub}/ (rails-new-ticket <branch> {sub}).")

if re.search(GIT + r"(?:commit|add|push|checkout|switch|reset|rebase|merge|stash|cherry-pick|am)\b", flat):
    for d in git_dirs():
        sub = in_submodule(d)
        if sub:
            deny(f"{sub}/ is a submodule folder and stays clean on main. "
                 f"Branch and commit in tickets/<branch>/{sub}/ instead.")
