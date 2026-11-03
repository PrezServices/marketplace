#!/usr/bin/env python3
"""PreToolUse guard on Workflow: every agent() in the script runs as a pstack agent.

Reads the script inline or by scriptPath, finds every agent() call with
workflow_scan, and refuses the run when a call sets no agentType, one that
isn't pstack's (or Explore), or one the scanner can't read, unless its prompt
names an installed pstack SKILL.md. Lists up to five reasons by line.
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _pstack import EXCEPTIONS, COMMENT_SICKO, POTETO_AGENT, RULE, allowed, deny, read_event, shown
from workflow_scan import scan

LISTED = 5
FIX = (f'Set agentType as a string literal on every agent() call, "{POTETO_AGENT}" or "{COMMENT_SICKO}" '
       f"for the no-comments pass. {EXCEPTIONS}")

event = read_event()
tool_input = event.get("tool_input") or {}
sources = [tool_input["script"]] if isinstance(tool_input.get("script"), str) else []
script_path = tool_input.get("scriptPath")
if isinstance(script_path, str):
    try:
        with open(os.path.join(event.get("cwd") or os.getcwd(), script_path)) as script_file:
            sources.append(script_file.read())
    except OSError as error:
        deny(f"{RULE} The hook could not read scriptPath {shown(script_path)}, so it refuses the run. {error}")
if not sources:
    deny(f"{RULE} This Workflow call names no script or scriptPath, so the hook cannot read which agents it "
         "starts. Pass the script inline or by scriptPath.")

reasons = []
for source in sources:
    calls, problems = scan(source)
    reasons += [f"line {line}: {message}" for line, message in problems]
    for call in calls:
        agent_type = call["agent_type"]
        named = agent_type[1] if agent_type[0] == "literal" else None
        if allowed(named, call["prompt"]):
            continue
        if agent_type[0] == "literal":
            reasons.append(f'line {call["line"]}: agent() sets agentType "{shown(agent_type[1])}"')
        elif agent_type[0] == "absent":
            reasons.append(f'line {call["line"]}: agent() sets no agentType')
        else:
            reasons.append(f'line {call["line"]}: the agentType option is `{shown(agent_type[1])}`, which the guard cannot read')

if reasons:
    more = f" And {len(reasons) - LISTED} more." if len(reasons) > LISTED else ""
    deny(f"{RULE} This Workflow script starts agents that are not pstack agents. "
         f"{'. '.join(reasons[:LISTED])}.{more} {FIX}")
