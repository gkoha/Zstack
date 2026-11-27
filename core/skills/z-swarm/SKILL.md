---
name: z-swarm
description: Fan out N parallel workers across slices or races, drain them, enforce SHA and method hygiene, and return one consolidated report. Use for /z-swarm, $z-swarm, multi-arch or multi-subsystem audits, parallel build/test gauntlets, or parallel exploration.
disable-model-invocation: true
---

# Swarm

Open a todo list with one entry per phase before launching anything:

1. Frame
2. Fan out
3. Aggregate
4. Report

## Phase A: Frame

1. State the done predicate and the exact artifact or report the swarm must
   return.
2. Choose the shape:
   - **Slices:** partition the work cleanly across files, subsystems,
     architectures, configs, or test suites.
   - **Race:** send N workers at the same problem with identical briefs (or
     distinct strategies). Declare the selection rule before spawning:
     `first pass`, `rank all`, or `best-of`.
   - **Mixed:** slices with raced arms where warranted.
3. Isolate writes. Any worker that writes files, builds, or runs VMs gets
   its own output path or worktree inside an agreed location
   (`../z-mode/principles/separate-before-serializing-shared-state.md`). Ask
   the user before creating a git worktree outside the current repository.
4. Pin verification contracts. When workers verify or measure commits, every
   brief names the exact commit SHA(s). A measurement brief also names the
   exact method (sample count, workload, order, environment). Workers must
   echo both in their result.

## Phase B: Fan out

Check `../z-mode/references/harness.md` for subagent tools in the active
session.

- When the harness supports parallel subagents (such as Claude Code `Agent`,
  Gemini CLI `@generalist`, or Antigravity `invoke_subagent`),
  launch all N workers in one turn. Start each brief with
  `Read <abs path to z-mode>/worker.md before anything else.`
- When the harness has no subagent tool, state that in one line and execute
  the slices sequentially with the same per-slice contract and reporting
  table.

Every brief stands alone: goal, exact slice or race arm, exact SHA(s) and
method when applicable, verification command, writable output path (or
explicit "do not edit files"), and required output schema.

Each worker reports one status: `PASS`, `ISSUES`, or `BLOCKED`, backed by
commands and outputs (or `file:line`). A worker that proves a defect reports
`ISSUES` and lists every defect it can prove, not only the first. If a
worker drops out, continue with N-1 and record the dropout explicitly.

## Phase C: Aggregate

Inspect every worker result:
- Drop any verification or measurement result that omits the pinned SHA(s)
  or method named in its brief, and respawn that worker once (fresh). After
  a second miss, record a `GAP`. A gap never counts as a pass.
- For coverage swarms, every required slice must have a verified result.
- For races, apply the selection rule declared in Phase A without moving
  the goalposts.
- Never paste raw worker dumps into the final report.

## Phase D: Report

Return one consolidated in-chat report containing:
- a summary table (`slice/arm | status | SHA/method | key evidence`),
- one-line defect summaries for every `ISSUES` item with `file:line` or
  reproducer pointer,
- gaps, dropouts, or `BLOCKED` items,
- the selection rule and winner when a race was run.
