# Bug fix

You own the diagnosis, review, and verification. Every changed line must
trace to evidence. A change that "might help" is a hypothesis and does not
ship.

1. Create or reuse the task record with `z-task-record`.
2. Reproduce on the real target: the guest, the QEMU command line, the
   selftest, or the host workload. Save the exact commands in `scripts/` and
   the failing output in `output/`. If it does not reproduce, narrow the
   conditions or add tracing until it does. Ask the user only for hardware or
   access you cannot reach.
3. Binary-search the cause. List candidate hypotheses, seed them with code
   traces and `z-why` for regression history, then eliminate them with
   runtime evidence: tracepoints, `trace_*`/`printk`, gdb, ftrace, QEMU `-d`
   and `-trace`. If it used to work, use `regression-bisect`.
4. Confirm the surviving mechanism with runtime evidence before designing the
   fix. Apply `principles/fix-root-causes.md`. If two fixes with one shared
   assumption fail, stop and apply `principles/attack-the-premise.md`.
5. Plan the fix. If it crosses a function boundary, run `z-architect`.
6. Implement the smallest fix the evidence supports. When delegating to a
   subagent, pass the confirmed root cause, exact files, and reproducer; use
   a fresh subagent for each retry rather than carrying stale failed context,
   and review the diff yourself.
7. Verify on the same surface with the original reproducer. "Inconclusive" or
   wrong-surface is not a pass. Run the narrowest relevant test suite as well.
8. If there is a cheap test (KVM selftest, kunit, qtest), add it and confirm
   it fails before the fix and passes after. Follow `z-tdd` and stage the
   failing test before the fix when the series allows it.
9. Write the commit with `z-patch`, including `Fixes:` when you found the
   culprit commit.

Reply: what was broken, the root cause with `file:line`, the fix, and the
failing-then-passing output verbatim.
