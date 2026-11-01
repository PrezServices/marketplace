#!/usr/bin/env python3
"""Tests for the guard hooks: runs each no-*.py guard on sample tool calls,
inside a throwaway workspace, and checks it denies or passes as expected. Add a
case here with every rule change.

Run: python3 hooks/test_guards.py
"""
import json, os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SUB = "server"


def workspace(configured):
    root = os.path.realpath(tempfile.mkdtemp(prefix="prez-rails-test-"))
    with open(os.path.join(root, ".gitmodules"), "w") as gitmodules:
        gitmodules.write(f'[submodule "{SUB}"]\n\tpath = {SUB}\n\turl = ../{SUB}.git\n')
    os.makedirs(os.path.join(root, SUB))
    os.makedirs(os.path.join(root, "tickets", "b", SUB))
    if configured:
        os.makedirs(os.path.join(root, ".prez-rails"))
        open(os.path.join(root, ".prez-rails", "config.md"), "w").close()
    return root


CONFIGURED = workspace(True)
UNCONFIGURED = workspace(False)

# (guard, tool, input as a function of the root, cwd relative to the root, workspace, should deny)
CASES = [
    ("no-submodule-edits", "Edit", lambda r: {"file_path": f"{r}/{SUB}/x.ts"}, ".", CONFIGURED, True),
    ("no-submodule-edits", "Edit", lambda r: {"file_path": f"{r}/tickets/b/{SUB}/x.ts"}, ".", CONFIGURED, False),
    ("no-submodule-edits", "Bash", lambda r: {"command": "git commit -m x"}, SUB, CONFIGURED, True),
    ("no-submodule-edits", "Bash", lambda r: {"command": f"git -C {SUB} push"}, ".", CONFIGURED, True),
    ("no-submodule-edits", "Bash", lambda r: {"command": f"cd {SUB} && git add x"}, ".", CONFIGURED, True),
    ("no-submodule-edits", "Bash", lambda r: {"command": "git status"}, SUB, CONFIGURED, False),
    ("no-sweeping-adds", "Bash", lambda r: {"command": "git add -A"}, ".", CONFIGURED, True),
    ("no-sweeping-adds", "Bash", lambda r: {"command": "git add ."}, ".", CONFIGURED, True),
    ("no-sweeping-adds", "Bash", lambda r: {"command": "git commit -am x"}, ".", CONFIGURED, True),
    ("no-sweeping-adds", "Bash", lambda r: {"command": "git add CLAUDE.md"}, ".", CONFIGURED, False),
    ("no-sweeping-adds", "Bash", lambda r: {"command": f"git -C tickets/b/{SUB} add -A"}, ".", CONFIGURED, False),
    ("no-force-push", "Bash", lambda r: {"command": "git push --force"}, ".", CONFIGURED, True),
    ("no-force-push", "Bash", lambda r: {"command": "git push -f origin x"}, ".", CONFIGURED, True),
    ("no-force-push", "Bash", lambda r: {"command": "git push origin main"}, ".", CONFIGURED, True),
    ("no-force-push", "Bash", lambda r: {"command": "git push -u origin feat/x"}, ".", CONFIGURED, False),
    ("no-force-push", "Bash", lambda r: {"command": "git pull origin main"}, ".", CONFIGURED, False),
    # Not set up with /prez-rails:setup: every guard passes.
    ("no-submodule-edits", "Edit", lambda r: {"file_path": f"{r}/{SUB}/x.ts"}, ".", UNCONFIGURED, False),
    ("no-sweeping-adds", "Bash", lambda r: {"command": "git add -A"}, ".", UNCONFIGURED, False),
    ("no-force-push", "Bash", lambda r: {"command": "git push --force"}, ".", UNCONFIGURED, False),
]

failed = 0
for guard, tool, make_input, cwd, root, want in CASES:
    tool_input = make_input(root)
    event = {"tool_name": tool, "tool_input": tool_input, "cwd": os.path.join(root, cwd)}
    result = subprocess.run([sys.executable, os.path.join(HERE, guard + ".py")], input=json.dumps(event),
                            capture_output=True, text=True, env={**os.environ, "CLAUDE_PROJECT_DIR": root})
    got = '"deny"' in result.stdout
    if got != want or result.returncode:
        failed += 1
        label = "configured" if root == CONFIGURED else "unconfigured"
        print(f"FAIL {guard}: {tool_input} in {cwd} ({label}): want deny={want}, got {got} {result.stderr.strip()}")
print(f"{len(CASES) - failed}/{len(CASES)} pass")
sys.exit(1 if failed else 0)
