# Autonomous delivery

An **autonomous delivery system** is a way of working a team installs on a
meta-repo (a repo that holds the project's repos as submodules), so agents can
take work from ticket to shipped change. Each one is a plugin, and a
workspace runs exactly one at a time.

## The contract every delivery system follows

So teams can try one, drop it and try another, each delivery system here:

1. **Installs as a plugin**: `claude plugin install <name>@prezservices --scope
   project`. Skills, hooks and scripts all live in the plugin.
2. **Keeps the meta-repo neutral.** The project's own facts go in one config
   folder at the workspace root (`.<name>/`), and nothing else in the
   meta-repo refers to the system.
3. **Ships `/<name>:setup`**, which writes that folder and any workspace
   changes, and **`/<name>:teardown`**, which removes exactly those.
4. **Stays inactive where it isn't set up.** Its hooks pass in a project with
   no config folder.
5. **Swaps in four steps**: `/<old>:teardown`, `claude plugin uninstall
   <old>@prezservices --scope project`, `claude plugin install
   <new>@prezservices --scope project`, `/<new>:setup`.

## Vocabulary

| Term | Meaning |
| --- | --- |
| delivery system | The whole way of working a meta-repo installs, such as prez rails |
| playbook | One way of handling one situation inside a delivery system |
| skill | The unit Claude Code loads |

## Systems

| System | What sets it apart |
| --- | --- |
| [`prez-rails`](prez-rails/) | Tickets are contracts: an engineer curates each one so anyone, engineer or not, can drive it from ticket to PR to QA |
| [`pstack-rails`](pstack-rails/) | pstack's playbooks decide the work: every session starts at `/pstack:poteto-mode`, and subagents run as pstack's agents |
