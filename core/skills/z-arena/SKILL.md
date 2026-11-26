---
name: z-arena
description: Spawn N independent candidates at the same non-trivial design or implementation task, cross-judge against a hidden rubric, pick a clean base, graft the strongest parts of losing candidates, and verify. Use for /z-arena, $z-arena, or when one attempt would lock in the wrong architecture.
disable-model-invocation: true
---

# Arena

Open a todo list with one entry per phase before launching anything:
`Frame`, `Fan out`, `Cross-judge`, `Pick`, `Graft`, `Verify`.

## Phase A: Frame

Every candidate receives the same core task contract.

1. State the exact artifact each candidate will produce (design sketch,
   patch series, data structure refactor, or prototype).
2. Derive the **rubric**: 3 to 6 concrete, gradeable criteria for what makes
   a winning solution on *this* task (for example: lock ordering simplicity,
   external-contract preservation, teardown/error-path safety, minimal diff
   outside the subsystem, testability). Hold the rubric back from
   candidates; it is for Phases C and D.
3. Plan diversity across N candidates (usually 2 or 3):
   - If the harness supports distinct models, spread candidates across
     models.
   - In a single-model harness (typical Claude Code or Codex), give each
     candidate either an independent clean run or a distinct architectural
     lens (for example: minimal-diff integration vs explicit state-machine
     reshape vs zero-new-lock isolation) so candidates explore genuinely
     different shapes.
4. Give each candidate its own isolated output path (for example under
   `.mydoc/<task>/output/arena-<slug>/candidate-<n>/` or separate branches),
   per `../z-mode/principles/separate-before-serializing-shared-state.md`.
   Ask the user before creating a git worktree outside the repository.

## Phase B: Fan out

Check `../z-mode/references/harness.md`. When subagents are available, spawn
all N candidates in parallel in one turn, starting each brief with
`Read <abs path to z-mode>/worker.md before anything else.` Give each
candidate:
- the task and shared grounding pointers (`file:line`, docs),
- its own isolated output path,
- instructions to produce the artifact plus a short rationale naming the
  alternatives it considered and rejected.

When subagents are unavailable, note it in one line and run N separate,
explicitly isolated passes yourself before moving to Phase C. If a candidate
fails to produce output, proceed with N-1 and record the dropout.

## Phase C: Cross-judge

After all candidates finish, spawn one fresh read-only judge subagent (if
available; prefer a different model family when the harness supports it).
Pass the candidates by anonymized path label (`candidate-1`, `candidate-2`,
...) and the Phase A rubric. The judge scores each candidate criterion by
criterion and recommends one base. If subagents are unavailable, note that
Phase C was skipped and run the rubric scoring yourself in Phase D.

## Phase D: Pick a base

Read every candidate end to end yourself before picking. Score each
criterion by criterion against the rubric rather than on gut feel, and
compare with the Phase C judge when present:
- Agreement confirms the base.
- Disagreement flags a hidden bias or an ambiguous rubric; read both
  rationales closely before deciding.

Prefer the base a future maintainer can extend without breaking invariants
(locks, lifetimes, uAPI/QAPI/migration contracts). On a tie, pick the
cleaner boundary and smaller surface
(`../z-mode/principles/laziness-protocol.md`).

## Phase E: Graft

Walk each losing candidate once more for specific strengths worth porting
into the chosen base (usually 1 or 2 concrete ideas per loser, such as a
cleaner error-unwinding path, a missed edge-case guard, or a better test).
Fold each graft in by hand under one coherent mental model
(`../z-mode/principles/redesign-from-first-principles.md`). Never paste
pieces together mechanically.

- If all candidates converge on the same shape, treat that as strong signal
  and ship the consensus shape without forced grafting.
- If candidates diverge wildly on basic assumptions, Phase A was
  under-specified: reframe and re-run rather than averaging incompatible
  designs.

## Phase F: Verify

Verify the synthesized artifact on the real target per
`../z-mode/principles/prove-it-works.md` (build, narrow tests, live check).
If verification uncovers a bug the arena missed, either Phase A missed a
constraint (reframe and re-run) or a losing candidate handled it and Phase E
missed the graft (go back to Phase E). Never paper over it.

## Output

Deliver the synthesized artifact plus a concise synthesis note covering:
- the rubric,
- chosen base and why,
- Phase C judge verdict (or that Phase C was skipped),
- each graft and which candidate it came from,
- what was rejected and why,
- any convergence or dropouts,
- the verification commands and output.
