# Bug fix

Every changed line must trace to evidence. A change that "might help" is a
hypothesis. It does not ship.

1. Create or reuse the task record with `z-task-record`.
2. Reproduce on the real target: the guest, the QEMU command line, the
   selftest, or the host workload. Save the exact commands in `scripts/` and
   the failing output in `output/`. If it does not reproduce, narrow the
   conditions or add tracing until it does. Ask the user only for hardware or
   access you cannot reach.
3. Bisect the cause. List hypotheses, then eliminate them with runtime
   evidence: tracepoints, `trace_*`/`printk`, gdb, ftrace, QEMU `-d` and
   `-trace`. If it used to work, use `regression-bisect`.
4. Confirm the mechanism with evidence before you design the fix. Apply
   `principles/fix-root-causes.md`.
5. Plan the fix. If it crosses a function boundary, run `z-architect`.
6. Implement the smallest fix the evidence supports.
7. Verify with the same reproducer. "Inconclusive" is not a pass. Run the
   narrowest relevant test suite as well.
8. If there is a cheap test (KVM selftest, kunit, qtest), add it and show it
   failing before the fix. Follow `z-tdd`.
9. Write the commit with `z-patch`, including `Fixes:` when you found the
   culprit commit.

Reply: what was broken, the root cause with `file:line`, the fix, and the
failing-then-passing output.
