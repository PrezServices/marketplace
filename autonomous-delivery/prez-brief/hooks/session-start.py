#!/usr/bin/env python3
"""SessionStart hook: in a workspace /prez-brief:setup configured
(.prez-brief/config.md exists), inject brief.md with the plugin root filled in.
Anywhere else: silent.
"""
import json, os, sys

plugin_root = os.environ.get("CLAUDE_PLUGIN_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
project_root = os.path.realpath(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd())
event_name = "SessionStart"
try:
    event = json.load(sys.stdin)
    if isinstance(event, dict):
        event_name = event.get("hook_event_name", event_name)
except ValueError:
    pass

if os.path.isfile(os.path.join(project_root, ".prez-brief", "config.md")):
    with open(os.path.join(plugin_root, "brief.md")) as brief_file:
        context = brief_file.read().replace("${CLAUDE_PLUGIN_ROOT}", plugin_root)
    print(json.dumps({"hookSpecificOutput": {"hookEventName": event_name, "additionalContext": context}}))
sys.exit(0)
