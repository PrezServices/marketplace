#!/usr/bin/env python3
"""PreToolUse guard on Agent and Task: a subagent runs as a pstack agent.

Passes pstack:poteto-agent, pstack:comment-sicko, a read-only Explore agent,
and any agent whose prompt names the absolute path of an installed pstack
SKILL.md (how pstack's own why, swarm, reflect, arena and interrogate start
general-purpose agents). Refuses everything else, naming the fix.
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _pstack import BRIEF, RULE, allowed, deny, read_event, shown

event = read_event()
tool_input = event.get("tool_input") or {}
agent_type = tool_input.get("subagent_type")
agent_type = agent_type if isinstance(agent_type, str) else None
if not allowed(agent_type, str(tool_input.get("prompt") or "")):
    named = "no subagent_type" if agent_type is None else f'subagent_type "{shown(agent_type)}"'
    deny(f"{RULE} This agent has {named}, which is not a pstack agent. {BRIEF}")
