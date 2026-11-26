# Autonomous run

You own the exit condition. Define done as a checkable predicate, then drive
to it without stopping on reversible work.

1. Create or reuse the task record with `z-task-record`.
2. State the exit condition as a checkable predicate before the first
   iteration (for example: "all tests in `tools/testing/selftests/kvm` pass",
   "the VFIO hot-unplug repro passes 50 consecutive iterations under KASAN",
   or "every commit in the 6-patch series builds cleanly with `W=1` and passes
   checkpatch").
3. Open a decision log via `z-log` in the task's `output/decisions.tsv`.
4. Loop until the predicate holds:
   - Make the smallest change the current evidence justifies. Delegate
     discrete fixes to a fresh subagent when the harness offers subagents,
     and inspect every diff yourself.
   - Verify against the real artifact and predicate. Keep and commit locally
     if the predicate advanced (`git add <files>`, never `-A`); revert in
     full if it did not. Changes that "might help" are reverted, not left to
     ride (`principles/sequence-verifiable-units.md`).
   - Log each iteration in `z-log` with what changed, evidence pointer, and
     whether the predicate moved.
5. Own mid-run discoveries that support the goal. Fix flaky local test
   harnesses, broken helper scripts, related bugs, or drift in separate
   commits rather than parking them for the user. Never pause to ask about
   reversible local work.
6. Respect hard safety boundaries at all times. Stop and ask the user before:
   deleting data or VM images, force-pushing, pushing to a shared remote,
   sending mail or posting to a list, loading kernel modules or changing host
   state as root, creating a worktree outside the repository, or making a
   product/contract call no experiment can settle. Never add `Signed-off-by:`.
7. Stop when the predicate is met. A plateau is not a stop: pivot the
   hypothesis, re-read the source, or apply `principles/attack-the-premise.md`
   to push past it. Surface a genuine dead end rather than spinning, and
   never relax the predicate to declare victory.
8. Finish with `z-log`'s end-of-run audit and `principles/prove-it-works.md`.

Reply: the exit condition, iterations run, what landed, what was reverted,
the `decisions.tsv` path, and the final predicate state with output.
