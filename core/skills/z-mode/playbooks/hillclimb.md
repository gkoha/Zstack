# Hillclimb

You own the metric and the experiment's integrity. Supervise, review, and
verify; delegate attempts when the harness supports subagents. Use for
sustained, iterative improvement of one measurable metric (throughput,
latency, VM-exit rate, migration downtime, memory footprint) against a
target. A one-off perf fix belongs in `perf-issue.md`.

Core discipline: one change, one measurement, keep or revert. Never stack
untested changes, and never claim a win from code inspection
(`principles/prove-it-works.md`).

1. Create or reuse the task record with `z-task-record`.
2. Ground the workload and architecture before choosing the metric. Trace the
   hot path, name the realistic workload dimensions that move the result
   (packet size, queue depth, vCPU count, memory size, dirty rate, pinning),
   and pick a case that reproduces the problem. If nothing reproduces it, fix
   the repro instead of hillclimbing. Fix one metric, the better direction,
   and a checkable stop predicate that pairs a target with an attempt floor
   so a lucky early win cannot end the run (for example, "at least 30% lower
   VM-exit rate and at least 8 iterations").
3. Build the measurement harness, prove its sensitivity, then freeze it
   (`principles/build-the-lever.md`). Run contrasting realistic workloads and
   confirm the target case reproduces the slowness while easier cases
   separate cleanly. Vet the harness with `z-benchmark` before freezing it,
   and have it print both error counts and work-done counts (such as
   tracepoint or completed-op counts). Once frozen, one repeatable command
   emits the metric as the median and spread of N runs. Record the baseline
   and a green regression gate (the tests that must keep passing) before any
   code changes.
4. Open a decision log with `z-log` in the task's `output/decisions.tsv`, one
   row per attempt (hypothesis, change, before/after/delta, gate result,
   verdict `kept` or `reverted`). Read it before each attempt so you do not
   repeat dead ends. Keep it out of git patches.
5. Ground each hypothesis in the architecture model from step 2 so it names a
   concrete mechanism (for example, "avoid taking BQL on the virtio-net RX
   kick path"), not a guess. Order ideas using the seven mantras in
   `perf-issue.md` step 4 (borrow their order, not that playbook's stop
   rule).
6. Loop, one hypothesis per iteration:
   - Delegate the tightly scoped change to a fresh subagent when available
     (otherwise implement inline with the same review separation). When
     several independent hypotheses are live, fan them out in separate
     worktrees (`principles/separate-before-serializing-shared-state.md`).
   - Measure before and after with the frozen harness and run the regression
     gate.
   - Keep the change only when the metric moves past the noise floor and the
     gate stays green. Otherwise revert it in full. A tweak that "might
     help" is reverted.
   - Make one local commit per accepted win (`git add <files>`, never `-A`).
     Log the row via `z-log` either way, kept or reverted.
   Verify each unit before starting the next
   (`principles/sequence-verifiable-units.md`).
7. Push past the first plateau. After several rejects in a row, switch
   category, combine near-misses, re-profile with `perf` / `perf kvm stat` /
   ftrace, or try a deeper structural change before concluding the hill is
   climbed. Correctness and simplicity outrank the number: revert a win that
   breaks behavior, and keep a simplification that holds the number
   (`principles/laziness-protocol.md`).
8. Stop when the predicate is met, or when only marginal ideas remain and
   their complexity does not earn its place. Never relax the predicate to
   declare victory. Surface a genuine dead end instead of spinning.
9. Run `z-log`'s end-of-run audit and prepare the accepted commits with
   `preparing-a-series`.

Reply: the metric and target, baseline to final with percent delta and
spread, iterations run (kept vs reverted), each accepted change on one line,
the `decisions.tsv` path, and the best untried idea if pushed further.
