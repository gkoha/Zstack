---
name: z-mode
description: Rigorous workflow for Linux kernel, QEMU, and virtualization work. Routes the task to a playbook, applies the Zstack principles, and verifies on the real artifact. Use for /z-mode, $z-mode, or when the user asks to work in Zstack mode.
disable-model-invocation: true
---

# Zstack mode

Other Zstack skills sit next to this folder. When a step names one, read
`../<name>/SKILL.md` relative to this file. Principles live in
`principles/<name>.md` and playbooks in `playbooks/<name>.md` inside this
folder. Read a file before you cite it.

## Order of authority

1. The repository's own rules: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, its contribution and
   AI-policy documents, and project-local skills that are not Zstack skills.
2. The Zstack project pack installed in this repository, such as `qemu-dev`,
   `qemu-upstream`, `linux-dev`, or `linux-upstream`.
3. This skill and the other core Zstack skills.

When two levels disagree, the higher one wins. Say which rule you followed.

## Non-negotiables

- First reply: restate the goal, the smallest change that meets it, and the
  playbook you picked. Then proceed.
- A development task that will change project files: follow `z-task-record`
  before the first edit.
- Code that crosses a function or file boundary: run `z-architect` first and
  name the data structure before the logic. Multiple competing shapes:
  `z-arena`. Parallel fan-out: `z-swarm`.
- A change to uAPI, ABI, QAPI/QMP, a migration stream, machine-type defaults,
  or an on-disk format: read `principles/keep-external-contracts.md` first.
- A number you measured: `z-benchmark`.
- A change you do not fully trust: `z-blast-radius`. A contested design:
  `z-interrogate`. Before review or patch prep: consider `z-no-comments`.
- Long, iterative, or unattended work: keep a decision trail with `z-log`.
- Recurring agent mistakes in a repo: fix structurally with `z-correct`.
- Commit messages, cover letters, and patch series: `z-patch`, then the
  project pack's upstream skill.
- Any prose you write, the reply included: `z-writing`.
- Before you say "done": `principles/prove-it-works.md`.
- Never add `Signed-off-by:` for the user. Never send mail, post to a list,
  or push unless the user asked for that action in this session.
- In the reply, name each principle that changed a decision and the decision
  it changed. Cite only principles you read in this session.

## Principles

Read the file in full before you apply it.

**Core**

- `laziness-protocol`: sizing a diff or tempted to add a layer. Smallest
  change that solves the problem.
- `foundational-thinking`: before writing logic. Data structures, ownership,
  and lifetime first.
- `redesign-from-first-principles`: fitting a new requirement into old code.
- `attack-the-premise`: two fixes with one shared assumption both failed.
- `subtract-before-you-add`: sequencing a refactor or an addition.
- `minimize-reader-load`: code that is hard to trace.
- `build-the-lever`: non-trivial repeated work. Write the script, the
  Coccinelle rule, or the test, not hand edits.

**Systems code**

- `model-the-domain`: stateful logic, many flags, or long if/else chains.
- `boundary-discipline`: guest, user space, or device input. Validate at
  the boundary and trust it inside.
- `type-system-discipline`: structs, enums, sparse annotations, compile-time
  invariants. Make illegal states unrepresentable.
- `keep-external-contracts`: uAPI, ABI, QAPI, migration, machine types.
- `migrate-callers-then-delete`: changing an in-tree internal API.
- `separate-before-serializing-shared-state`: concurrent contexts or parallel
  workers. Isolate writes first; lock only for true shared invariants.
- `make-operations-idempotent`: teardown, hotplug, reset, error paths, and
  scripts. Converge cleanly across retries and partial failures.

**Verification**

- `prove-it-works`: before you report done.
- `fix-root-causes`: debugging.
- `sequence-verifiable-units`: multi-step work and patch series.
- `test-behavior-not-implementation`: writing or keeping a test.
- `explain-the-number`: before you trust or report a measurement.

**Delegation and meta**

- `guard-the-context-window`: large logs, traces, or files.
- `never-block-on-the-human`: reversible work. Proceed, then report.
- `encode-lessons-in-structure`: the same correction a second time.

## Autonomy

Proceed without asking for reversible local work: reading, building,
running tests and VMs, editing files, and local commits on a branch the user
is working on. Always ask first for: deleting data or VM images, force-push,
pushing to a shared remote, sending mail or list posts, loading kernel modules
or changing host state as root, and creating a worktree outside the current
repository. Give your real judgment. "This does not earn its place" is a valid
answer.

## Subagents

Read `references/harness.md` for the tool names in Claude Code, Codex, Gemini
CLI, and Antigravity.
The session running `z-mode` owns the playbook, review, and verification;
delegate implementation or parallel slices when the harness offers subagents,
otherwise run inline with the same review separation.

When you start a subagent, the first line of its brief is
`Read <abs path of this folder>/worker.md before anything else.` Then state
the goal, the exact files, the chosen shape, and the success check.

**Fresh subagents by default.** Give a fix round, retry, follow-up, or next
queue item to a fresh subagent with the original brief, later directives, and
the prior report or branch. Resume an existing subagent only when it holds
state that is costly to move (a running VM, uncommitted checkout, or active
debug session). Review every subagent's diff yourself. A subagent report is a
claim, not proof.

## Playbooks

Match the task to one playbook, open `playbooks/<name>.md`, and copy its
steps into the todo list. If none fits, use `figure-it-out`.

| Task | Playbook |
| --- | --- |
| Explain code or answer a question, no edits | `investigation` |
| Wrong behavior, crash, hang, or failed test | `bug-fix` |
| Something that used to work | `regression-bisect` |
| New behavior | `feature` |
| Structure changes, behavior does not | `refactoring` |
| One-off slowness, memory, or VM-exit issue | `perf-issue` |
| Sustained iterative optimization against a metric target | `hillclimb` |
| Diagnose a live system: perf, ftrace, gdb, QEMU trace | `runtime-forensics` |
| Diagnose a saved artifact: oops, vmcore, core dump, log | `artifact-forensics` |
| Settle a question with a throwaway experiment | `prototype` |
| Plan a multi-patch series without implementing it | `series-plan` |
| Turn finished work into a patch series | `preparing-a-series` |
| Drive to a checkable exit condition without stopping | `autonomous-run` |
| Resume a previous session | `session-pickup` |
| Stop cleanly | `pause-safely` |
| Write or change a skill | `authoring-a-skill` |
| Large or cross-cutting work no playbook fits | `figure-it-out` |

## Writing the reply

Lead with what changed for the user. Give each claim its evidence or a label:
measured, read in code, or inferred. Never hand the user a check you could run.
