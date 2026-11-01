#!/usr/bin/env python3
"""SessionStart hook: loads the prez rails into the session.

A plugin can't ship a CLAUDE.md, so the always-on rules live in rails.md and
this hook injects them as additionalContext (Claude Code caps it at 10,000
characters; test_session_start.py checks the size).

- Workspace set up (.prez-rails/config.md exists): inject rails.md.
- A meta-repo (.gitmodules) not set up yet: tell the user once to run
  /prez-rails:setup, and inject nothing else.
- Anywhere else: silent.
"""
import json, os, shutil, sys

plugin_root = os.environ.get("CLAUDE_PLUGIN_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
project_root = os.path.realpath(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd())
event_name = "SessionStart"
try:
    event_name = json.load(sys.stdin).get("hook_event_name", event_name)
except ValueError:
    pass


def emit(context=None, message=None):
    output = {}
    if message:
        output["systemMessage"] = message
    if context:
        output["hookSpecificOutput"] = {"hookEventName": event_name, "additionalContext": context}
    print(json.dumps(output))
    sys.exit(0)


if os.path.isfile(os.path.join(project_root, ".prez-rails", "config.md")):
    with open(os.path.join(plugin_root, "rails.md")) as rails_file:
        rails = rails_file.read().replace("${CLAUDE_PLUGIN_ROOT}", plugin_root)
    missing = [tool for tool in ("gh", "openspec") if shutil.which(tool) is None]
    if missing:
        rails += "\n\nMissing on this machine: " + ", ".join(missing) + ". Tell the user before a skill needs it."
    emit(context=rails)

if os.path.isfile(os.path.join(project_root, ".gitmodules")):
    emit(message="prez-rails is installed but this workspace isn't set up yet. Run /prez-rails:setup to configure it.")

sys.exit(0)
