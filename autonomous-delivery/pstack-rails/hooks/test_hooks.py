#!/usr/bin/env python3
"""Tests for the pstack-rails hooks, in throwaway workspaces and a fake plugin
cache: the Agent and Workflow guards, the script scanner, and session start.
Add a case with every rule change.

Run: python3 hooks/test_hooks.py
"""
import json, os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PLUGIN = os.path.dirname(HERE)
LIMIT = 10_000
sys.path.insert(0, HERE)
from workflow_scan import scan  # noqa: E402

failures = []


def workspace(configured, meta_repo=True):
    root = os.path.realpath(tempfile.mkdtemp(prefix="pstack-rails-test-"))
    if meta_repo:
        open(os.path.join(root, ".gitmodules"), "w").close()
    if configured:
        os.makedirs(os.path.join(root, ".pstack-rails"))
        open(os.path.join(root, ".pstack-rails", "config.md"), "w").close()
    return root


def claude_config(with_pstack):
    config = os.path.realpath(tempfile.mkdtemp(prefix="pstack-rails-config-"))
    if with_pstack:
        for version in ("0.9.1", "0.15.36"):
            for skill in ("poteto-mode", "why"):
                folder = os.path.join(config, "plugins", "cache", "cursor-plugins", "pstack", version, "skills", skill)
                os.makedirs(folder)
                open(os.path.join(folder, "SKILL.md"), "w").close()
    return config


CONFIG = claude_config(True)
NO_PSTACK = claude_config(False)
NEWEST = os.path.join(CONFIG, "plugins", "cache", "cursor-plugins", "pstack", "0.15.36")
WHY_SKILL = os.path.join(NEWEST, "skills", "why", "SKILL.md")
SET_UP, NOT_SET_UP, PLAIN = workspace(True), workspace(False), workspace(False, meta_repo=False)
FAKE_SKILL = os.path.join(SET_UP, "fake", "pstack", "skills", "a", "SKILL.md")
os.makedirs(os.path.dirname(FAKE_SKILL))
open(FAKE_SKILL, "w").close()


def run(hook, project, payload, config=CONFIG):
    result = subprocess.run([sys.executable, os.path.join(HERE, hook)], input=payload, capture_output=True, text=True,
                            env={**os.environ, "CLAUDE_PROJECT_DIR": project, "CLAUDE_PLUGIN_ROOT": PLUGIN,
                                 "CLAUDE_CONFIG_DIR": config})
    if result.returncode:
        failures.append(f"{hook} exited {result.returncode}: {result.stderr.strip()}")
    return json.loads(result.stdout) if result.stdout.strip() else {}


def denied(output):
    return output.get("hookSpecificOutput", {}).get("permissionDecision") == "deny"


def expect(name, output, should_deny):
    if denied(output) != should_deny:
        failures.append(f"{name}: expected {'deny' if should_deny else 'pass'}, got {output or 'pass'}")


# The Agent guard.
AGENT_CASES = [
    ("poteto-agent", {"subagent_type": "pstack:poteto-agent", "prompt": "x"}, SET_UP, False),
    ("comment-sicko", {"subagent_type": "pstack:comment-sicko", "prompt": "x"}, SET_UP, False),
    ("Explore", {"subagent_type": "Explore", "prompt": "x"}, SET_UP, False),
    ("general-purpose", {"subagent_type": "general-purpose", "prompt": "x"}, SET_UP, True),
    ("no type", {"prompt": "x"}, SET_UP, True),
    ("routed by an installed skill", {"subagent_type": "general-purpose", "prompt": f"Follow {WHY_SKILL} now."}, SET_UP, False),
    ("routed by a missing skill", {"subagent_type": "general-purpose", "prompt": "Follow /tmp/pstack/skills/why/SKILL.md"}, SET_UP, True),
    ("routed by a relative path", {"subagent_type": "general-purpose", "prompt": "Follow pstack/skills/why/SKILL.md"}, SET_UP, True),
    ("routed by a skill outside the plugins cache", {"subagent_type": "general-purpose", "prompt": f"Follow {FAKE_SKILL}"}, SET_UP, True),
    ("not set up", {"subagent_type": "general-purpose", "prompt": "x"}, NOT_SET_UP, False),
]
for name, tool_input, project, should_deny in AGENT_CASES:
    payload = json.dumps({"tool_name": "Agent", "tool_input": tool_input, "cwd": project})
    expect(f"guard-agent {name}", run("guard-agent.py", project, payload), should_deny)
expect("guard-agent unreadable input", run("guard-agent.py", SET_UP, "not json"), True)
expect("guard-agent input that isn't an object", run("guard-agent.py", SET_UP, "[1]"), True)


# The Workflow guard.
GOOD = 'const r = await agent("review it", {label: "a", agentType: "pstack:poteto-agent"})'
WORKFLOW_CASES = [
    ("pstack agent", GOOD, False),
    ("no agentType", 'await agent("x", {label: "a"})', True),
    ("no options", 'await agent("x")', True),
    ("other type", 'await agent("x", {agentType: "general-purpose"})', True),
    ("const literal", 'const T = "pstack:comment-sicko"\nawait agent("x", {agentType: T})', False),
    ("shorthand const", 'const agentType = "Explore"\nawait agent("x", {agentType})', False),
    ("variable type", 'await agent("x", {agentType: pick()})', True),
    ("spread options", 'await agent("x", {...opts})', True),
    ("agent as a value", "const run = agent\nawait run('x')", True),
    ("nested workflow", 'await workflow("other")', True),
    ("eval", 'eval("agent(1)")', True),
    ("routed by skill path", f'await agent("Follow {WHY_SKILL}", {{label: "w"}})', False),
    ("agent in a string", 'log("agent(x)")\n' + GOOD, False),
    ("agent in a comment", '// agent("x")\n' + GOOD, False),
    ("template prompt", 'await agent(`a ${b} c`, {agentType: "pstack:poteto-agent"})', False),
    ("unclosed string", 'await agent("x, {agentType: "pstack:poteto-agent"})', True),
    ("second call bad", GOOD + '\nawait agent("y", {label: "b"})', True),
    # From the pre-push review: each one let a general-purpose agent through.
    ("BOM before a division", 'const n = 1 \ufeff/ agent("p", {agentType: "general-purpose"}) / 2', True),
    ("postfix ++ before a division", 'let i = 1; const n = i++ / agent("p", {agentType: "general-purpose"}) / 2', True),
    ("keyword property before a division", 'const o = {of: 1}; const n = o.of / agent("p", {agentType: "general-purpose"}) / 2', True),
    ("parameter shadows a const", 'const T = "pstack:poteto-agent"\nconst f = (T) => agent("p", {agentType: T})\nf("general-purpose")', True),
    ("destructuring shadows a const", 'const T = "pstack:poteto-agent"\n{ const {T} = {T: "general-purpose"}; await agent("p", {agentType: T}) }', True),
    ("agent renamed by destructuring", 'const { agent: spawn } = globalThis; await spawn("p", {agentType: "general-purpose"})', True),
    ("agent by its string name", 'globalThis["agent"]("p", {agentType: "general-purpose"})', True),
    ("code from a constructor", '(async () => {}).constructor("return agent(1)")()', True),
    ("skill path in a comment of a fake install", f'await agent(/* {FAKE_SKILL} */ "x", {{label: "w"}})', True),
    ("regex still after return", 'function f(s) { return /agent\\(/.test(s) }\n' + GOOD, False),
]
for name, script, should_deny in WORKFLOW_CASES:
    payload = json.dumps({"tool_name": "Workflow", "tool_input": {"script": script}, "cwd": SET_UP})
    expect(f"guard-workflow {name}", run("guard-workflow.py", SET_UP, payload), should_deny)

script_file = os.path.join(SET_UP, "flow.js")
with open(script_file, "w") as handle:
    handle.write('await agent("x", {label: "a"})')
payload = json.dumps({"tool_name": "Workflow", "tool_input": {"scriptPath": "flow.js"}, "cwd": SET_UP})
expect("guard-workflow bad scriptPath file", run("guard-workflow.py", SET_UP, payload), True)
with open(os.path.join(SET_UP, "latin1.js"), "wb") as handle:
    handle.write(b'// caf\xe9\nawait agent("p", {agentType: "general-purpose"})')
payload = json.dumps({"tool_name": "Workflow", "tool_input": {"scriptPath": "latin1.js"}, "cwd": SET_UP})
expect("guard-workflow scriptPath that isn't UTF-8", run("guard-workflow.py", SET_UP, payload), True)
payload = json.dumps({"tool_name": "Workflow", "tool_input": {"scriptPath": "missing.js"}, "cwd": SET_UP})
expect("guard-workflow missing scriptPath", run("guard-workflow.py", SET_UP, payload), True)
payload = json.dumps({"tool_name": "Workflow", "tool_input": {}, "cwd": SET_UP})
expect("guard-workflow no script", run("guard-workflow.py", SET_UP, payload), True)
payload = json.dumps({"tool_name": "Workflow", "tool_input": {"script": 'await agent("x")'}, "cwd": NOT_SET_UP})
expect("guard-workflow not set up", run("guard-workflow.py", NOT_SET_UP, payload), False)

many = "\n".join(f'await agent("x{n}")' for n in range(7))
output = run("guard-workflow.py", SET_UP, json.dumps({"tool_name": "Workflow", "tool_input": {"script": many}}))
reason = output.get("hookSpecificOutput", {}).get("permissionDecisionReason", "")
if "And 2 more." not in reason or "line 1:" not in reason:
    failures.append(f"guard-workflow lists five reasons and counts the rest: {reason[:200]}")


# The scanner on its own.
calls, problems = scan('await agent("a ${x}", {agentType: "pstack:poteto-agent"})\nconst re = /agent\\(/g')
if problems or [c["agent_type"] for c in calls] != [("literal", "pstack:poteto-agent")]:
    failures.append(f"scan: regex and template handling: {calls} {problems}")
calls, _ = scan('parallel(xs.map(x => () => agent(`do ${x.name}`, {agentType: "pstack:poteto-agent", label: x.id})))')
if [c["line"] for c in calls] != [1] or calls[0]["agent_type"] != ("literal", "pstack:poteto-agent"):
    failures.append(f"scan: nested call inside parallel(): {calls}")
calls, _ = scan('const opts = {agent: 1}\nawait agent("x", {agentType: "Explore"})')
if len(calls) != 1:
    failures.append(f"scan: an object key named agent is not a call: {calls}")


# Session start.
def session(project, config=CONFIG):
    return run("session-start.py", project, json.dumps({"hook_event_name": "SessionStart"}), config)


output = session(SET_UP)
context = output.get("hookSpecificOutput", {}).get("additionalContext", "")
if "/pstack:poteto-mode" not in context or NEWEST not in context or "${PSTACK_ROOT}" in context:
    failures.append(f"session-start set up: expected orders with the newest pstack path: {context[:200]}")
if len(context) > LIMIT:
    failures.append(f"session-start orders are {len(context)} characters, over the {LIMIT} cap")
output = session(SET_UP, NO_PSTACK)
if "not installed" not in output.get("hookSpecificOutput", {}).get("additionalContext", "") or not output.get("systemMessage"):
    failures.append(f"session-start without pstack: expected the install notice: {output}")
output = session(NOT_SET_UP)
if "/pstack-rails:setup" not in output.get("systemMessage", "") or "hookSpecificOutput" in output:
    failures.append(f"session-start not set up: expected only the setup reminder: {output}")
if session(PLAIN):
    failures.append("session-start unrelated folder: expected silence")


def orders_for(adapter_line):
    with open(os.path.join(SET_UP, ".pstack-rails", "config.md"), "w") as config_file:
        config_file.write(f"## Tracker\n\n{adapter_line}\n")
    return session(SET_UP).get("hookSpecificOutput", {}).get("additionalContext", "")


for line, ticketed in [("- **Adapter:** `linear` (team FRO)", True), ("- **Adapter:** `github-issues`", True),
                       ("- **Adapter:** `none`", False), ("- **Adapter:** `<linear | jira | github-issues | none>`", False),
                       ("", False)]:
    text = orders_for(line)
    if ("create-task" in text) != ticketed or ("no tracker" in text) == ticketed or "<!--" in text:
        failures.append(f"session-start orders for {line or 'no adapter line'!r}: expected tickets={ticketed}: {text[:300]}")


for failure in failures:
    print("FAIL", failure)
total = len(AGENT_CASES) + 2 + len(WORKFLOW_CASES) + 6 + 3 + 4 + 5
print(f"orders: {len(context)}/{LIMIT} characters")
print(f"{total - len(failures)}/{total} passed")
sys.exit(1 if failures else 0)
