# Figure it out

When no narrower playbook fits (a large cross-subsystem migration, an
ambitious multi-part feature, or unattended work a reviewer will audit later),
design an auditable playbook before writing code.

Open a todo list with the phases below first.

## Phase A: Frame

Ground in the codebase first, then commit. Do not start until you can state:

- The definition of done as a falsifiable predicate (`principles/prove-it-works.md`).
- Scope, quantified: rough units, affected subsystems, and blockers surfaced
  during grounding.
- The rigor level, biased high. External contracts (uAPI, QAPI, VMState,
  machine types) and high blast-radius changes get higher rigor. Rigor means
  gates and artifacts, not "try harder".

Create or reuse the task record with `z-task-record`. Present the framing and
tradeoffs before committing to a long run. Reversible local work proceeds
(`principles/never-block-on-the-human.md`), while a multi-hour run earns one
checkpoint with the user.

## Phase B: Design the workflow

Decompose into atomic, independently verifiable units sequenced
riskiest-unknown-first. Build scaffolding and verification before features
(`principles/foundational-thinking.md`).

- Build the verification harness first and capture the pre-change baseline,
  so checks read as "old value vs new value".
- For one-way-door design choices, run `z-architect` (or `z-arena` when
  multiple valid shapes exist). Skip them for mechanical work whose shape is
  already settled (`principles/laziness-protocol.md`).
- Decide what fans out. Parallelize only across clean seams, and give each
  worker its own worktree or output path
  (`principles/separate-before-serializing-shared-state.md`).
- Write the phase list into the task readme and add its concrete steps to the
  todo list between Phase C and Phase D.

## Phase C: Run the loop

Treat each unit as an experiment: state the hypothesis, make the smallest
change, measure against the predicate on the real artifact, keep it if it
advanced, revert it if it did not. Verify each unit before starting the next
(`principles/sequence-verifiable-units.md`).

- Inspect the real artifact, never a self-report. When a check passes too
  easily, suspect the observation method before the system.
- Pair delegated work with an independent check. If a worker games a gate,
  reset and tighten the contract. If the gate itself is wrong, fix the gate
  in its own commit rather than routing around it.
- Use a strict three-state verdict: `VERIFIED`, `NOT VERIFIED`, or
  `INCONCLUSIVE`. `INCONCLUSIVE` is not a pass. Never hide a negative.

## Phase D: Keep the audit trail

Log every real decision point, pivot, revert, and unit verdict via `z-log` as
each step lands, not from memory at the end. Keep the TSV in the task's
`output/` directory (outside git patches).

## Phase E: Verify and hand back

Verify the complete result against the Phase A predicate on the real target,
not only the synthetic harness. Encode any recurring correction as a script,
static check, or test (`principles/encode-lessons-in-structure.md`). Run the
end-of-run audit required by `z-log`.

Reply: the playbook you designed, the rigor level and why, the decision-log
path, what is verified against the predicate, and what remains open.
