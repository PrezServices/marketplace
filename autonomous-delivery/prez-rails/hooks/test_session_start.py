#!/usr/bin/env python3
"""Tests for session-start.py: what it injects in a set-up workspace, a meta-repo
not set up yet, and an unrelated folder, and that rails.md fits the 10,000
character cap Claude Code puts on additionalContext.

Run: python3 hooks/test_session_start.py
"""
import json, os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PLUGIN = os.path.dirname(HERE)
LIMIT = 10_000


def run(project):
    result = subprocess.run([sys.executable, os.path.join(HERE, "session-start.py")],
                            input=json.dumps({"hook_event_name": "SessionStart"}), capture_output=True, text=True,
                            env={**os.environ, "CLAUDE_PROJECT_DIR": project, "CLAUDE_PLUGIN_ROOT": PLUGIN})
    return result.returncode, json.loads(result.stdout) if result.stdout.strip() else {}


failures = []
configured = tempfile.mkdtemp()
os.makedirs(os.path.join(configured, ".prez-rails"))
open(os.path.join(configured, ".prez-rails", "config.md"), "w").close()
code, out = run(configured)
context = out.get("hookSpecificOutput", {}).get("additionalContext", "")
if code or "# prez rails" not in context:
    failures.append("set-up workspace: rails.md not injected")
if "${CLAUDE_PLUGIN_ROOT}" in context or PLUGIN not in context:
    failures.append("set-up workspace: plugin root not substituted")
if len(context) > LIMIT:
    failures.append(f"rails context is {len(context)} characters, over the {LIMIT} cap")

meta_repo = tempfile.mkdtemp()
open(os.path.join(meta_repo, ".gitmodules"), "w").close()
code, out = run(meta_repo)
if code or "/prez-rails:setup" not in out.get("systemMessage", "") or "hookSpecificOutput" in out:
    failures.append("meta-repo not set up: expected only the setup reminder")

code, out = run(tempfile.mkdtemp())
if code or out:
    failures.append("unrelated folder: expected silence")

for failure in failures:
    print("FAIL", failure)
print(f"rails context: {len(context)}/{LIMIT} characters")
print("ok" if not failures else f"{len(failures)} failed")
sys.exit(1 if failures else 0)
