"""Shared helpers for the PreToolUse guard hooks in this folder.

Each no-*.py guard enforces one rule and is registered on its own, with its own
tool matcher, in hooks.json. Importing this module reads the hook
event from stdin and exposes the tool name, its input, the cwd and the Bash
command on one line. deny() prints the block decision with the one-line reason
the agent relays; a guard that returns without calling it lets the call pass.
"""
import json, os, re, sys

root = os.path.realpath(os.environ.get("CLAUDE_PROJECT_DIR") or ".")
event = json.load(sys.stdin)

# The plugin's hooks run in every project it is enabled in. The guards act only
# in a workspace that /pstack-rails:setup has configured; anywhere else they pass.
if not os.path.isfile(os.path.join(root, ".pstack-rails", "config.md")):
    sys.exit(0)
tool = event.get("tool_name", "")
inp = event.get("tool_input", {}) or {}
cwd = os.path.realpath(event.get("cwd") or os.getcwd())

# The Bash command on one line, or "" for other tools.
flat = " ".join((inp.get("command", "") or "").split()) if tool == "Bash" else ""

GIT = r"\bgit\b(?:\s+-C\s+\S+)?\s+"


def deny(reason):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }))
    sys.exit(0)


def submodules():
    names = []
    try:
        for line in open(os.path.join(root, ".gitmodules")):
            m = re.match(r"\s*path\s*=\s*(\S+)", line)
            if m:
                names.append(m.group(1))
    except OSError:
        pass
    return names


def in_submodule(path):
    """The submodule this path is inside, or None. tickets/ worktrees are not submodules."""
    real = os.path.realpath(path)
    for name in submodules():
        folder = os.path.join(root, name)
        if real == folder or real.startswith(folder + os.sep):
            return name
    return None


def git_dirs():
    """Where git acts: every `git -C <dir>` and `cd <dir>` in the command, or the cwd when there are none."""
    dirs = []
    for pattern in (r"git\s+-C\s+(\S+)", r"(?:^|&&|;)\s*cd\s+(\S+)"):
        for m in re.finditer(pattern, flat):
            d = m.group(1).strip("'\"")
            dirs.append(d if os.path.isabs(d) else os.path.join(cwd, d))
    return dirs or [cwd]
