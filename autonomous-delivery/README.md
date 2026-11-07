# Autonomous delivery

Plugins a team installs on a workspace, usually a meta-repo (a repo that
holds the project's repos as submodules), so agents can take work from an
idea to a shipped change. They come in two roles, like the product and
engineering teams of a company:

- An **ideation plugin** (the product team) shapes the work: research,
  grilling, prototypes, and the ticket that says what to deliver and how
  anyone can tell. Optional.
- A **delivery system** (the engineering team) builds it: picks the ticket
  up, designs, codes, reviews, ships. Exactly one per workspace.

They meet at [the ticket](ticket.md): the ideation plugin writes its
commitment and a starting design, and the delivery system builds to the
commitment and owns the design. A workspace with no ideation plugin files
tickets by hand, or, where the delivery system allows it, works without
tickets at all.

## The contract every plugin here follows

So teams can try one, drop it and try another, each plugin:

1. **Installs as a plugin**: `claude plugin install <name>@prezservices --scope
   project`. Skills, hooks and scripts all live in the plugin.
2. **Keeps the workspace neutral.** The project's own facts go in one config
   folder at the workspace root (`.<name>/`), and nothing else in the
   workspace refers to the plugin.
3. **Ships `/<name>:setup`**, which writes that folder and any workspace
   changes, and **`/<name>:teardown`**, which removes exactly those.
4. **Stays inactive where it isn't set up.** Its hooks pass in a project with
   no config folder.
5. **Follows [the ticket](ticket.md)** when it writes or reads tickets, and
   ships a copy of it as `ticket.md`. A change to the ticket is copied into
   every plugin in the same PR.
6. **Swaps in four steps**: `/<old>:teardown`, `claude plugin uninstall
   <old>@prezservices --scope project`, `claude plugin install
   <new>@prezservices --scope project`, `/<new>:setup`. A delivery system
   swaps without touching the ideation plugin, and the other way round.

## Vocabulary

| Term | Meaning |
| --- | --- |
| ideation plugin | The product side a workspace may install, such as prez brief |
| delivery system | The engineering side a workspace installs exactly one of, such as prez rails |
| playbook | One way of handling one situation inside a delivery system |
| skill | The unit Claude Code loads |

## Plugins

| Plugin | Role | What sets it apart |
| --- | --- | --- |
| [`prez-brief`](prez-brief/) | ideation | Writes the seven-section ticket in Linear, Jira or GitHub Issues, with grilling, research and prototypes to shape it |
| [`prez-rails`](prez-rails/) | delivery system | Tickets are contracts: an engineer curates each one so anyone, engineer or not, can drive it from ticket to PR to QA. Carries its own ticket writing for now |
| [`pstack-rails`](pstack-rails/) | delivery system | pstack's playbooks decide the work: every session starts at `/pstack:poteto-mode`, and subagents run as pstack's agents. Tickets are optional |
