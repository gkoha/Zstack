# Explain the number

- Before you run, write down the result that would change your decision and
  the expected noise.
- Ask "why not twice as fast?" Name the limiter from a profile or counters:
  `perf`, VM-exit counts, `kvm_stat`, trace events, lock statistics.
- List what else the number could measure: errors, work that never ran, a
  cache, CPU frequency scaling, a debug build, a different guest config. Rule
  each one out.
- Keep the run count, spread, and limiter with the number. For a performance
  claim, run `z-benchmark`.
