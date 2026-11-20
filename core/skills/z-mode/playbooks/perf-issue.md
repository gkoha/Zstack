# Perf issue

Tie every change to a measurement. Do not reason about speed from source alone.

1. Create or reuse the task record with `z-task-record`.
2. Capture a baseline on the real workload. Vet it with `z-benchmark`. Save the
   raw data in `output/`.
3. Find the limiter: `perf record`/`perf top`, `perf kvm stat`, `kvm_stat`,
   VM-exit and interrupt counts, ftrace, lock statistics, QEMU trace events.
4. Try the cheapest idea first, and stop when one meets the target:
   1. Do not do the work.
   2. Do it once, not again.
   3. Do less of it.
   4. Do it later.
   5. Do it off the hot path, for example outside the BQL or in an iothread.
   6. Do it concurrently.
   7. Do it cheaper.
5. One change, one measurement. Keep it only when the number moves past the
   noise and tests stay green. Revert it otherwise.
6. Record before, after, run count, spread, and limiter in the commit message.

Reply: baseline, result, delta, run count, limiter, and the artifact paths.
