---
name: plan-verification
description: >-
  Decide which verification methods a change needs before any code is
  written: read the ticket and the code it touches, find the traits each
  method is for, and write a plan that names each method to run, what it
  checks, and each method skipped with its reason. Covers driving the real
  surface, a TLA+ model of a design, fault injection, a proof or code-level
  verifier, decision tables, property tests, mutation testing, contract
  tests, output and visual diff, and accessibility checks. Use when
  `implement-task` reaches it, or when someone asks "how should we verify
  this?", "does this need a model?" or "what tests does this need?".
---

# Planning the verification

A method earns its place when the change has the trait that method is for.
Running every method on every change wastes the run and buries the result
that matters. Running none leaves the bugs that tests rarely reach. This
skill picks, and writes the reasons down.

The plan is required. The choice of methods is yours, and each choice
carries its reason.

## Input

$ARGUMENTS: a ticket key, or a description of the change when there is no
ticket.

## 1. Find the traits

Read the ticket, then the code it will touch. For each trait below, answer
yes or no, and name the file or the ticket line that shows it. A trait you
cannot see in the code or the ticket is a no.

When the code and the ticket disagree, plan against the code and list each
difference in the plan. When the change is already built, plan against what
was built and mark each method as run or not yet run.

An **actor** is any process that writes the state: a browser tab, a worker,
a queue consumer, a cron, another service. Two tabs are two actors.

| Trait | What it looks like |
| --- | --- |
| **Visible behavior** | Anything a user or a caller can observe: a screen, a response, a message, a stored record |
| **Ordering** | The result depends on the order of events. More than one actor writing the same record, a retry, a queue, a webhook that can arrive twice or late, a lock, a flow that can stop between an outside side effect (a call to another service, a message sent) and the write that records it |
| **States** | The thing moves between named states and some moves are not allowed: an order, a session, a subscription, a job |
| **Costly logic** | A wrong answer loses money, leaks data or lets someone in: amounts and rounding, permissions, a parser of outside input, crypto, deletion. Data sent to a third party without the user's consent is a leak |
| **Wide input** | A pure function, written or specified by the ticket, whose inputs vary widely and whose output obeys a rule you can state: a round trip, an order kept, a total conserved, a bound never crossed |
| **Many UI states** | A screen with many combinations of input, data and viewport: a form, a list with filters, a layout that reflows |
| **Fixed look** | The change must match a design or an earlier build pixel for pixel |
| **Unchanged output** | The ticket promises that some output stays identical: a build with a flag off, a response for existing callers, a migration that keeps the data |
| **Accessibility criteria** | An acceptance criterion names keyboard use, a screen reader, focus, contrast or motion |
| **Consumed contract** | An API, an event, a schema or a file format that this repo produces and code outside it reads today or by the end of the ticket. An API this code only calls is not one |
| **Tests carry the risk** | The code has a Costly logic, Ordering or States trait and its safety rests on tests. Judge this last, after the other methods are chosen, because they may add the tests |

## 2. Map traits to methods

| Method | Run it when | What it proves | Skip it when |
| --- | --- | --- | --- |
| **Drive the real surface** | Visible behavior. Always | The acceptance criteria hold on the running system | Never |
| **Model the design (TLA+)** | Ordering, or States with more than one actor | No order of events breaks the rule, within the bounds of the model | One actor, every state change sits in one function a test can walk, and no step can stop after an outside side effect |
| **Fault injection** | Ordering, where a flow can stop between an outside side effect and the write that records it | The real code recovers when it is stopped at each such point and run again: nothing sent twice, nothing lost | No outside side effect in the flow |
| **Verify the code** | Costly logic, in a language with a verifier a developer here can install | The rule holds for every input, or every input up to a bound | No verifier runs on the language. Use property tests and say so |
| **Decision table test** | Costly logic that decides who may do what | Every combination of actor, resource and action gets the answer the ticket states, with none left out | The rule has one input |
| **Property tests** | Wide input. Costly logic with no verifier, other than a who-may-do-what rule. The rules of a TLA+ model, replayed on the real code | The rule holds on thousands of generated inputs, with a shrunk counterexample when it does not | Glue code with no rule to state |
| **Interaction property tests** | Many UI states | No sequence of generated user actions breaks an invariant of the screen | Static content. A screen with one path |
| **Visual diff** | Fixed look | The pixels match the reference | The ticket changes the look on purpose and names no reference |
| **Output diff** | Unchanged output | The output is byte for byte what it was, or differs only where the ticket says | Nothing is promised to stay the same |
| **Accessibility check** | Accessibility criteria | The criterion holds when driven by keyboard and read through the accessibility tree, plus an automated audit | No such criterion |
| **Contract test** | Consumed contract | Producer and consumer agree on the shape, old and new | No reader outside the repo |
| **Mutation testing** | Tests carry the risk | The tests fail when the code is broken on purpose | Docs, config, generated code, a change with no logic, a repo with no tests on the changed code |

Two orderings are fixed:

- **A design method runs before the code.** The TLA+ model checks the design
  the ticket describes. Write it and check it before the first line of
  product code, because a design flaw found later costs the implementation.
- **Mutation testing runs last**, on the changed files, after the tests it
  judges exist.

## 3. Pick the tool

Use what the repo already has. Look for its verify skills
(`.claude/skills/verify-*`), a `formal/` folder, and tasks in `mise.toml`,
`Makefile` or `package.json` named for a check. When the repo has none for a
planned method:

| Method | How to get it |
| --- | --- |
| Drive the real surface | The repo's `verify-<app>` skill. None yet: follow `<pstack>/skills/create-verification-skill/SKILL.md` |
| Model the design, verify the code | Follow `<pstack>/skills/create-formal-verification-skill/SKILL.md`. It picks the tool from the question and leaves a verify skill behind. Read every TLA+ result with `<pstack>/skills/statechart/SKILL.md` |
| Property tests | The library the language's test runner supports: fast-check for TypeScript, Hypothesis for Python, proptest for Rust |
| Interaction property tests | The repo's browser harness driven by generated action sequences |
| Visual diff | pstack's Visual parity playbook (`<pstack>/skills/poteto-mode/playbooks/visual-parity.md`) |
| Output diff | Build both refs and compare with `diff -r`, or record the response before and after |
| Accessibility check | The repo's browser harness: keyboard only, the accessibility snapshot, and an axe audit |
| Fault injection | A test that lets the outside call succeed, fails the next step, then runs the flow again |
| Decision table test | A table in the test file with one row per combination, generated when the combinations are many |
| Contract test | A test in the producer that loads the consumer's recorded expectations, or a schema both sides import |
| Mutation testing | StrykerJS for TypeScript, mutmut for Python, cargo-mutants for Rust, scoped to the changed files |

`<pstack>` is the pstack path the session orders give.

Languages differ in what can be verified. Rust has verifiers that run on the
code (Kani for bounded checks, Verus for proofs). TypeScript and Python have
none a team can rely on, so Costly logic there gets property tests on the
real code. A proof in Lean of a hand-written model says nothing about the
code unless generated-input tests compare the model with the code. Plan that
pair or neither.

Adding a tool is part of the ticket when it takes one install command and
one task or config file.
When it is more, file a ticket for it through `pstack-rails:create-task`,
use the next strongest method in this ticket, and say so in the plan.

## 4. Write the plan

Write it into the ticket's **Tech decisions**, under a `**Verification
plan**` line, and comment one line saying it was added. With no ticket, put
it in the reply and later in the PR.

```
**Verification plan**

Traits found: <trait> (<file>), <trait> (<file>)

| Method | Checks | Tool | When |
| --- | --- | --- | --- |
| Drive the real surface | <each acceptance criterion, on <surface>> | <skill> | before the PR, and on each deploy stage |
| <method> | <the rule, in one plain sentence> | <tool> | <before the code \| before the PR> |

Skipped: <method> (<reason>), <method> (<reason>)
```

Every method in the step 2 table appears once, in the table or in Skipped.
State each rule as one plain sentence a person can judge without the tool:
"a note a user created stays until a delete removes it".

## 5. Hold the plan

- A counterexample or a surviving mutant is a finding. Fix the code or the
  test. Never weaken the rule, shrink the bound or delete the case to get a
  pass.
- A check you have never seen fail proves nothing. Show each new rule
  failing once on a broken variant of the code.
- When the work shows a trait the plan missed, add the method and update the
  plan in the ticket. When it shows a planned method does not apply, move it
  to Skipped with the reason. Do not drop it silently.
- The PR's `## Verification` section has one bullet per planned method: what
  ran, what it found, and what it does not cover.

Done when the plan is in the ticket and every method from step 2 is either
planned or skipped with a reason.
