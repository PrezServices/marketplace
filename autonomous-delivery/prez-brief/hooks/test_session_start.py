#!/usr/bin/env python3
"""Tests for session-start.py: brief.md is injected, with the plugin root filled
in and under Claude Code's 10,000 character cap, only in a set-up workspace.

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
os.makedirs(os.path.join(configured, ".prez-brief"))
open(os.path.join(configured, ".prez-brief", "config.md"), "w").close()
code, out = run(configured)
context = out.get("hookSpecificOutput", {}).get("additionalContext", "")
if code or "prez-brief:create-task" not in context:
    failures.append("set-up workspace: brief.md not injected")
if "${CLAUDE_PLUGIN_ROOT}" in context or PLUGIN not in context:
    failures.append("set-up workspace: plugin root not substituted")
if len(context) > LIMIT:
    failures.append(f"brief context is {len(context)} characters, over the {LIMIT} cap")

meta_repo = tempfile.mkdtemp()
open(os.path.join(meta_repo, ".gitmodules"), "w").close()
for name, folder in (("meta-repo not set up", meta_repo), ("unrelated folder", tempfile.mkdtemp())):
    code, out = run(folder)
    if code or out:
        failures.append(f"{name}: expected silence, got {out}")

for failure in failures:
    print("FAIL", failure)
print(f"brief context: {len(context)}/{LIMIT} characters")
print("ok" if not failures else f"{len(failures)} failed")
sys.exit(1 if failures else 0)
