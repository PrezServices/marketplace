#!/usr/bin/env python3
"""Port skills from Cursor plugins into this plugin, at a pinned commit.

Cursor and Claude Code read the same SKILL.md format, so a skill ports by
copying its folder (with the source plugin's LICENSE) into skills/<name>/.
ported.json names each source plugin, the commit it is pinned to, the skills
taken from it, and the sha256 of every file copied.

  port-cursor-plugin.py           Copy every listed skill at its pinned commit and rewrite the hashes.
  port-cursor-plugin.py --latest  Move each source to the newest commit on its default branch first.
  port-cursor-plugin.py --check   Offline: fail when a ported file differs from its recorded hash.

A ported skill is never edited by hand; a change goes upstream or into a new
pin. After copying, the script lists lines that name something only Cursor
has (.mdc rules, generalPurpose or readonly subagents, ~/.cursor paths), so a
person can judge whether the skill still works in Claude Code.
"""
import hashlib, json, os, re, shutil, subprocess, sys, tempfile

PLUGIN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(PLUGIN, "ported.json")
SKILLS = os.path.join(PLUGIN, "skills")
CURSOR_ONLY = re.compile(r"\.mdc\b|generalPurpose|readonly:\s*true|~/\.cursor|\.cursor/|is_background|bugbot|cursor-agent", re.I)


def sha256(path):
    with open(path, "rb") as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def files_under(folder):
    for base, _, names in os.walk(folder):
        for name in sorted(names):
            path = os.path.join(base, name)
            yield os.path.relpath(path, PLUGIN), path


def git(*args, cwd=None):
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def check(manifest):
    problems = []
    for source, entry in manifest.items():
        for relative, expected in entry.get("files", {}).items():
            path = os.path.join(PLUGIN, relative)
            if not os.path.isfile(path):
                problems.append(f"{source}: {relative} is missing")
            elif sha256(path) != expected:
                problems.append(f"{source}: {relative} differs from {entry['commit'][:12]}")
        recorded = set(entry.get("files", {}))
        for skill in entry["skills"]:
            for relative, _ in files_under(os.path.join(SKILLS, skill)):
                if relative not in recorded:
                    problems.append(f"{source}: {relative} is not from the source")
    for problem in problems:
        print("FAIL", problem)
    print("ported skills match ported.json" if not problems else f"{len(problems)} problems; re-run without --check to restore them")
    return 1 if problems else 0


def port(manifest, latest):
    owned = {skill: source for source, entry in manifest.items() for skill in entry["skills"]}
    for source, entry in manifest.items():
        with tempfile.TemporaryDirectory() as scratch:
            git("clone", "--quiet", "--filter=blob:none", "--no-checkout", f"https://github.com/{entry['repo']}", scratch)
            git("sparse-checkout", "set", entry["path"], cwd=scratch)
            commit = git("rev-parse", "origin/HEAD", cwd=scratch) if latest else entry["commit"]
            git("checkout", "--quiet", commit, cwd=scratch)
            plugin = os.path.join(scratch, entry["path"])
            license_file = os.path.join(plugin, "LICENSE")
            entry["commit"], entry["files"] = commit, {}
            for skill in entry["skills"]:
                if owned.get(skill) != source:
                    sys.exit(f"{skill} is listed under two sources")
                origin = os.path.join(plugin, "skills", skill)
                if not os.path.isfile(os.path.join(origin, "SKILL.md")):
                    sys.exit(f"{source} has no skills/{skill}/SKILL.md at {commit[:12]}")
                target = os.path.join(SKILLS, skill)
                shutil.rmtree(target, ignore_errors=True)
                shutil.copytree(origin, target)
                if os.path.isfile(license_file):
                    shutil.copy(license_file, os.path.join(target, "LICENSE"))
                for relative, path in files_under(target):
                    entry["files"][relative] = sha256(path)
                    for number, line in enumerate(open(path, errors="replace"), 1):
                        if CURSOR_ONLY.search(line):
                            print(f"review {relative}:{number}: {line.strip()[:120]}")
            print(f"{source}: {len(entry['skills'])} skills at {commit[:12]}")
    with open(MANIFEST, "w") as handle:
        json.dump(manifest, handle, indent=2)
        handle.write("\n")
    return 0


if __name__ == "__main__":
    with open(MANIFEST) as handle:
        manifest = json.load(handle)
    sys.exit(check(manifest) if "--check" in sys.argv else port(manifest, "--latest" in sys.argv))
