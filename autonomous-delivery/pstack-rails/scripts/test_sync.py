#!/usr/bin/env python3
"""Tests for scripts/sync: drives the real script against throwaway origins and a
throwaway workspace repo in a temp dir, one row per outcome of the script's
table plus the cases that decide which outcome a folder gets. Add a row with
every change to the script.

Run: python3 scripts/test_sync.py
"""
import itertools, os, shutil, subprocess, sys, tempfile
from collections import namedtuple

HERE = os.path.dirname(os.path.abspath(__file__))
SYNC = os.path.join(HERE, "sync")

# Nothing here reads or writes the user's git config. Origins are local paths, which need the file
# transport, so it is switched on for these processes only.
ENV = {**{key: value for key, value in os.environ.items() if not key.startswith("GIT_")},
       "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1",
       "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.com",
       "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.com",
       "GIT_CONFIG_COUNT": "1", "GIT_CONFIG_KEY_0": "protocol.file.allow", "GIT_CONFIG_VALUE_0": "always"}


def run_git(*args, cwd=None):
    return subprocess.run(["git", *args], cwd=cwd, env=ENV, capture_output=True, text=True)


def git(*args, cwd=None):
    result = run_git(*args, cwd=cwd)
    if result.returncode:
        raise RuntimeError(f"git {' '.join(args)} in {cwd}: {result.stderr.strip()}")
    return result.stdout.strip()


def write(folder, name, content):
    with open(os.path.join(folder, name), "w") as handle:
        handle.write(content)


def read(folder, name):
    with open(os.path.join(folder, name)) as handle:
        return handle.read()


def commit(folder, name, content):
    write(folder, name, content)
    git("add", name, cwd=folder)
    git("commit", "-q", "-m", name, cwd=folder)
    return git("rev-parse", "HEAD", cwd=folder)


class World:
    """Bare origins, seed clones to move them forward from, and a workspace repo recording each
    origin as a submodule. Every origin has main and development, each with its own commits."""

    def __init__(self):
        self.base = os.path.realpath(tempfile.mkdtemp(prefix="pstack-rails-sync-"))
        self.root = os.path.join(self.base, "workspace")
        self.recorded, self.extra, self.result = {}, {}, None
        self.counter = itertools.count(1)
        git("init", "-q", "-b", "main", self.root)

    def origin(self, name):
        return os.path.join(self.base, "origins", name + ".git")

    def seed(self, name):
        return os.path.join(self.base, "seeds", name)

    def folder(self, path):
        return os.path.join(self.root, path)

    def add(self, name, path=None, branch=None, default_branch="main"):
        path = path or name
        seed = self.seed(name)
        git("init", "-q", "-b", "main", seed)
        commit(seed, "README", "one\n")
        git("switch", "-q", "-c", "development", cwd=seed)
        commit(seed, "development", "dev\n")
        git("init", "-q", "--bare", self.origin(name))
        git("remote", "add", "origin", self.origin(name), cwd=seed)
        git("push", "-q", "origin", "main", "development", cwd=seed)
        git("--git-dir", self.origin(name), "symbolic-ref", "HEAD", f"refs/heads/{default_branch}")
        git("submodule", "add", "-q", "--name", name, self.origin(name), path, cwd=self.root)
        if branch:
            git("config", "-f", ".gitmodules", f"submodule.{name}.branch", branch, cwd=self.root)
        git("add", ".gitmodules", path, cwd=self.root)
        git("commit", "-q", "-m", f"add {name}", cwd=self.root)
        self.recorded[path] = git("rev-parse", "HEAD", cwd=self.folder(path))

    def advance(self, name, branch="main"):
        seed = self.seed(name)
        git("switch", "-q", branch, cwd=seed)
        commit(seed, f"moved{next(self.counter)}", "x\n")
        git("push", "-q", "origin", branch, cwd=seed)

    def tip(self, name, branch="main", short=False):
        return git("--git-dir", self.origin(name), "rev-parse", *(["--short"] if short else []), branch)

    def line(self, name, branch="main", path=None):
        return f"{path or name}: {branch} at {self.tip(name, branch, short=True)}"

    def detach(self, path):
        git("switch", "-q", "--detach", cwd=self.folder(path))

    def edit(self, path):
        write(self.folder(path), "README", "edited\n")

    def clone_workspace(self):
        clone = os.path.join(self.base, "clone")
        git("clone", "-q", self.root, clone)
        self.root = clone

    def state(self, path):
        folder = self.folder(path)
        branch = run_git("symbolic-ref", "--short", "-q", "HEAD", cwd=folder).stdout.strip() or None
        return branch, git("rev-parse", "HEAD", cwd=folder)

    def cloned(self, path):
        return os.path.exists(os.path.join(self.folder(path), ".git"))

    def run(self, args):
        self.result = subprocess.run([SYNC, *args], cwd=self.root, env=ENV, capture_output=True, text=True)
        return self.result


def tip(name, branch="main"):
    return lambda w: w.tip(name, branch)


def recorded(path):
    return lambda w: w.recorded[path]


Row = namedtuple("Row", "name repos setup args exit out err folders extra",
                 defaults=([], None, [], 0, lambda w: [], lambda w: [], {}, None))


def moved_on(w):
    w.advance("alpha")


def moved_on_detached(w):
    w.advance("alpha")
    w.detach("alpha")


def never_cloned(w):
    w.advance("alpha")
    w.clone_workspace()


def local_change(w):
    w.advance("alpha")
    w.edit("alpha")


def local_change_ahead_of_recorded(w):
    w.advance("alpha")
    folder = w.folder("alpha")
    git("fetch", "-q", "origin", cwd=folder)
    git("merge", "-q", "--ff-only", "origin/main", cwd=folder)
    w.edit("alpha")


def diverged(w):
    w.advance("alpha")
    w.extra["local"] = commit(w.folder("alpha"), "local", "mine\n")


def main_in_another_worktree(w):
    w.advance("alpha")
    w.detach("alpha")
    git("worktree", "add", "-q", os.path.join(w.base, "elsewhere"), "main", cwd=w.folder("alpha"))


def development_moved_on(w):
    w.advance("alpha", "development")


def origin_default_is_development(w):
    w.advance("alpha", "main")


def unknown_name(w):
    w.advance("alpha")
    w.detach("alpha")


def each_moved_on(w):
    for name in w.recorded:
        w.advance(name)


def beta_unreachable(w):
    each_moved_on(w)
    shutil.rmtree(w.origin("beta"))
    w.extra["fetch"] = run_git("fetch", "--quiet", "origin", cwd=w.folder("beta"))
    if w.extra["fetch"].returncode in (0, 2):
        raise RuntimeError("the fetch from the removed origin did not fail")


def beta_unreachable_and_not_cloned(w):
    each_moved_on(w)
    shutil.rmtree(w.origin("beta"))
    w.clone_workspace()


def alpha_edited_beta_moved_on(w):
    each_moved_on(w)
    w.edit("alpha")


def problems_in_local_change(w):
    folder = w.folder("alpha")
    found = []
    if read(folder, "README") != "edited\n":
        found.append("the local change was touched")
    if git("rev-parse", "origin/main", cwd=folder) != w.tip("alpha"):
        found.append("origin/main was not fetched before the skip")
    return found


def problems_in_unknown_name(w):
    if git("rev-parse", "origin/main", cwd=w.folder("alpha")) != w.recorded["alpha"]:
        return ["alpha was fetched before the unknown name was refused"]
    return []


def problems_in_tracking(w):
    if git("config", "branch.main.remote", cwd=w.folder("alpha")) != "origin":
        return ["the branch created from origin does not track it"]
    return []


def problems_in_not_cloned(w):
    return ["gamma was cloned after the sync stopped at beta"] if w.cloned("gamma") else []


def problems_named_beta_only(w):
    if git("rev-parse", "origin/main", cwd=w.folder("alpha")) != w.recorded["alpha"]:
        return ["alpha was fetched though only beta was named"]
    return []


CASES = [
    # Synced.
    Row("behind origin, then synced", repos=[{"name": "alpha"}], setup=moved_on,
        out=lambda w: [w.line("alpha")], folders={"alpha": ("main", tip("alpha"))}),
    Row("detached and clean ends on the branch at origin's tip", repos=[{"name": "alpha"}], setup=moved_on_detached,
        out=lambda w: [w.line("alpha")], folders={"alpha": ("main", tip("alpha"))}),
    Row("never cloned gets cloned and synced", repos=[{"name": "alpha"}], setup=never_cloned,
        out=lambda w: [w.line("alpha")], folders={"alpha": ("main", tip("alpha"))}),
    Row("a configured branch other than main", repos=[{"name": "alpha", "branch": "development"}],
        setup=development_moved_on, out=lambda w: [w.line("alpha", "development")],
        folders={"alpha": ("development", tip("alpha", "development"))}),
    Row("no branch configured means main, not origin's default branch",
        repos=[{"name": "alpha", "default_branch": "development"}], setup=origin_default_is_development,
        out=lambda w: [w.line("alpha")], folders={"alpha": ("main", tip("alpha"))}, extra=problems_in_tracking),
    Row("a submodule whose name differs from its path, named with a trailing slash",
        repos=[{"name": "alpha-lib", "path": "libs/alpha", "branch": "development"}],
        setup=lambda w: w.advance("alpha-lib", "development"), args=["libs/alpha/"],
        out=lambda w: [w.line("alpha-lib", "development", path="libs/alpha")],
        folders={"libs/alpha": ("development", tip("alpha-lib", "development"))}),
    Row("a workspace with no submodules has nothing to sync"),
    # Skipped: exit 2, the line on stderr.
    Row("local changes are skipped and left alone", repos=[{"name": "alpha"}], setup=local_change, exit=2,
        err=lambda w: ["alpha: has local changes, skipped"], folders={"alpha": ("main", recorded("alpha"))},
        extra=problems_in_local_change),
    Row("an initialised folder ahead of the recorded commit is not moved back to it", repos=[{"name": "alpha"}],
        setup=local_change_ahead_of_recorded, exit=2, err=lambda w: ["alpha: has local changes, skipped"],
        folders={"alpha": ("main", tip("alpha"))}),
    Row("a branch checked out in another worktree is skipped", repos=[{"name": "alpha"}], setup=main_in_another_worktree,
        exit=2, err=lambda w: ["alpha: could not switch to main, skipped"],
        folders={"alpha": (None, recorded("alpha"))}),
    Row("a diverged branch is left as is", repos=[{"name": "alpha"}], setup=diverged, exit=2,
        err=lambda w: ["alpha: main has diverged from origin/main, left as is"],
        folders={"alpha": ("main", lambda w: w.extra["local"])}),
    Row("a skip does not stop the other repos, and the exit is 2",
        repos=[{"name": "alpha"}, {"name": "beta"}, {"name": "gamma"}], setup=alpha_edited_beta_moved_on, exit=2,
        out=lambda w: [w.line("beta"), w.line("gamma")], err=lambda w: ["alpha: has local changes, skipped"],
        folders={"alpha": ("main", recorded("alpha")), "beta": ("main", tip("beta")), "gamma": ("main", tip("gamma"))}),
    Row("only the named repos are synced", repos=[{"name": "alpha"}, {"name": "beta"}], setup=each_moved_on,
        args=["beta"], out=lambda w: [w.line("beta")],
        folders={"alpha": ("main", recorded("alpha")), "beta": ("main", tip("beta"))}, extra=problems_named_beta_only),
    # Hard failures: exit 1 for a name that is not a submodule, git's own code for a git error.
    Row("an unknown name exits 1 before touching anything", repos=[{"name": "alpha"}], setup=unknown_name,
        args=["alpha", "nosuch"], exit=1, err=lambda w: ["error: 'nosuch' is not a submodule of this workspace"],
        folders={"alpha": (None, recorded("alpha"))}, extra=problems_in_unknown_name),
    Row("an unreachable origin is a hard failure that stops at that repo",
        repos=[{"name": "alpha"}, {"name": "beta"}, {"name": "gamma"}], setup=beta_unreachable,
        exit=lambda code, w: code == w.extra["fetch"].returncode and code not in (0, 2),
        out=lambda w: [w.line("alpha")], err=lambda w: w.extra["fetch"].stderr.strip().splitlines(),
        folders={"alpha": ("main", tip("alpha")), "beta": ("main", recorded("beta")),
                 "gamma": ("main", recorded("gamma"))}),
    Row("a folder that cannot be cloned is a hard failure that stops at that repo",
        repos=[{"name": "alpha"}, {"name": "beta"}, {"name": "gamma"}], setup=beta_unreachable_and_not_cloned,
        exit=lambda code, w: code not in (0, 2), out=lambda w: [w.line("alpha")],
        err=lambda w: ["fatal: clone of '%s' into submodule path '%s' failed" % (w.origin("beta"), w.folder("beta"))],
        folders={"alpha": ("main", tip("alpha"))}, extra=problems_in_not_cloned),
]


def check(row):
    world = World()
    try:
        for repo in row.repos:
            world.add(**repo)
        if row.setup:
            row.setup(world)
        result = world.run(row.args)
        problems = []
        wanted_exit = row.exit
        if not (wanted_exit(result.returncode, world) if callable(wanted_exit) else result.returncode == wanted_exit):
            problems.append(f"exit {result.returncode}")
        wanted_out, wanted_err = row.out(world), row.err(world)
        if result.stdout.splitlines() != wanted_out:
            problems.append(f"stdout {result.stdout.splitlines()}, want {wanted_out}")
        err_lines = result.stderr.splitlines()
        if (not wanted_err and err_lines) or any(line not in err_lines for line in wanted_err):
            problems.append(f"stderr {err_lines}, want {wanted_err}")
        for path, (branch, head) in row.folders.items():
            if world.state(path) != (branch, head(world)):
                problems.append(f"{path} is {world.state(path)}, want {(branch, head(world))}")
        if row.extra:
            problems.extend(row.extra(world))
        return problems
    except RuntimeError as error:
        return [str(error)]
    finally:
        shutil.rmtree(world.base, ignore_errors=True)


failed = 0
for row in CASES:
    problems = check(row)
    if problems:
        failed += 1
        print(f"FAIL {row.name}: " + "; ".join(problems))
print(f"{len(CASES) - failed}/{len(CASES)} pass")
sys.exit(1 if failed else 0)
