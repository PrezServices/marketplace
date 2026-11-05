"""Shared helpers for the pstack-rails hooks.

The hooks run in every project the plugin is enabled in, and act only in a
workspace /pstack-rails:setup configured (.pstack-rails/config.md exists).
"""
import json, os, re, sys

POTETO_AGENT = "pstack:poteto-agent"
COMMENT_SICKO = "pstack:comment-sicko"
PSTACK_AGENTS = (POTETO_AGENT, COMMENT_SICKO)
READ_ONLY_AGENT = "Explore"
VERSION = re.compile(r"^\d+\.\d+\.\d+$")
SKILL_FILE = re.compile(r"""[^\s"'`()<>,;|]+/SKILL\.md""")
PSTACK_SKILL = re.compile(r"(?:^|/)pstack/(?:[^/]+/)*skills/[a-z0-9][a-z0-9-]*/SKILL\.md$")

RULE = "This workspace delivers through pstack, and its subagents run as pstack agents (.pstack-rails/config.md)."
EXCEPTIONS = (f'A read-only look may use "{READ_ONLY_AGENT}". A pstack skill that starts general-purpose agents '
              "(why, swarm, reflect, arena, interrogate) may keep that type once each prompt names the absolute "
              "path of an installed pstack SKILL.md.")
BRIEF = f'Spawn it with subagent_type "{POTETO_AGENT}", or "{COMMENT_SICKO}" for the no-comments pass. {EXCEPTIONS}'


def project_root():
    return os.path.realpath(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd())


def configured(root):
    return os.path.isfile(os.path.join(root, ".pstack-rails", "config.md"))


def plugins_cache():
    config = os.environ.get("CLAUDE_CONFIG_DIR") or os.path.join(os.path.expanduser("~"), ".claude")
    return os.path.join(config, "plugins", "cache")


def _folders(path):
    try:
        return sorted(entry.name for entry in os.scandir(path) if entry.is_dir())
    except OSError:
        return []


def newest_pstack(cache=None):
    """The root of the newest installed pstack, or None."""
    cache = cache or plugins_cache()
    installs = []
    for marketplace in _folders(cache):
        for version in _folders(os.path.join(cache, marketplace, "pstack")):
            root = os.path.join(cache, marketplace, "pstack", version)
            if VERSION.match(version) and os.path.isfile(os.path.join(root, "skills", "poteto-mode", "SKILL.md")):
                installs.append((tuple(int(part) for part in version.split(".")), root))
    return max(installs)[1] if installs else None


def installed_pstack_roots(cache=None):
    cache = cache or plugins_cache()
    return [os.path.realpath(os.path.join(cache, marketplace, "pstack", version))
            for marketplace in _folders(cache) for version in _folders(os.path.join(cache, marketplace, "pstack"))
            if VERSION.match(version)]


def names_installed_skill(text):
    """True when the text names the SKILL.md of a pstack installed in the plugins cache."""
    roots = None
    for named in SKILL_FILE.findall(text or ""):
        path = os.path.expanduser(named)
        if not (os.path.isabs(path) and PSTACK_SKILL.search(path) and os.path.isfile(path)):
            continue
        roots = installed_pstack_roots() if roots is None else roots
        real = os.path.realpath(path)
        if any(re.match(re.escape(root + os.sep) + r"skills/[a-z0-9][a-z0-9-]*/SKILL\.md$", real) for root in roots):
            return True
    return False


def allowed(agent_type, prompt):
    return agent_type in PSTACK_AGENTS or agent_type == READ_ONLY_AGENT or names_installed_skill(prompt)


def shown(value, limit=80):
    return value if len(value) <= limit else value[:limit] + "..."


def read_event():
    """The hook event, or exit quietly when the workspace isn't set up."""
    if not configured(project_root()):
        sys.exit(0)
    try:
        event = json.load(sys.stdin)
    except ValueError as error:
        deny(f"{RULE} The hook could not read the call, so it refuses it. {error}")
    if not isinstance(event, dict) or not isinstance(event.get("tool_input") or {}, dict):
        deny(f"{RULE} The hook could not read the call, so it refuses it.")
    return event


def deny(reason):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": reason,
    }}))
    sys.exit(0)
