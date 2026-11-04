#!/usr/bin/env python3
"""PreToolUse hook on Bash: no sweeping adds at the workspace root.

Denies `git add -A`, `git add --all`, `git add .` and `git commit -a` when git
acts at the workspace root. Pulling a submodule folder moves its recorded
pointer, and a sweeping add commits that drift unnoticed (it has shipped
pointer bumps, and once a pin to an unpushed commit, that way). Staging by path passes,
and so does any add inside a tickets/<branch>/<repo>/ worktree.
"""
import os, re
from _lib import root, flat, GIT, deny, git_dirs

if any(os.path.realpath(d) == root for d in git_dirs()):
    if re.search(GIT + r"add\s+(?:-A\b|--all\b|\.(?:\s|$))", flat):
        deny("At the workspace root, `git add -A` / `git add .` stages the moved submodule "
             "pointers with everything else. Stage by path.")
    if re.search(GIT + r"commit\s+(?:\S+\s+)*-[a-zA-Z]*a", flat):
        deny("At the workspace root, `git commit -a` stages the moved submodule pointers "
             "with everything else. Stage by path, then commit.")
