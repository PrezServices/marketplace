#!/usr/bin/env python3
"""SessionStart hook: points the session at pstack, after every startup,
resume, clear and compaction, so the entry point survives a compaction.

- Workspace set up (.pstack-rails/config.md exists): inject orders.md with the
  newest installed pstack's path. When pstack isn't installed, say so instead.
- A meta-repo (.gitmodules) not set up yet: tell the user once to run
  /pstack-rails:setup.
- Anywhere else: silent.

The orders say where to start, not what to do: pstack's poteto-mode picks its
own playbook and skills.
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _pstack import configured, newest_pstack, project_root

plugin_root = os.environ.get("CLAUDE_PLUGIN_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root = project_root()
event_name = "SessionStart"
try:
    event_name = json.load(sys.stdin).get("hook_event_name", event_name)
except ValueError:
    pass

INSTALL = ("claude plugin marketplace add cursor/plugins --scope project && "
           "claude plugin install pstack@cursor-plugins --scope project")


def emit(context=None, message=None):
    output = {}
    if message:
        output["systemMessage"] = message
    if context:
        output["hookSpecificOutput"] = {"hookEventName": event_name, "additionalContext": context}
    print(json.dumps(output))
    sys.exit(0)


if configured(root):
    pstack = newest_pstack()
    if pstack is None:
        emit(context="This workspace delivers through pstack (.pstack-rails/config.md), but pstack is not installed "
                     f"on this machine, so its agents cannot start. Tell the user to run `{INSTALL}` and start a new "
                     "session, and make no changes until then.",
             message="pstack-rails: pstack is not installed. Run: " + INSTALL)
    with open(os.path.join(plugin_root, "orders.md")) as orders_file:
        emit(context=orders_file.read().replace("${PSTACK_ROOT}", pstack))

if os.path.isfile(os.path.join(root, ".gitmodules")):
    emit(message="pstack-rails is installed but this workspace isn't set up yet. Run /pstack-rails:setup to configure it.")

sys.exit(0)
