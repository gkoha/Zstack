# Foundational thinking

Get the data structure right before writing logic.

- Name the core structs, who owns each object, and its lifetime: refcount,
  RCU, devm, QOM parent, or `realize`/`unrealize`.
- Trace every access path. Name the lock, BQL, RCU read side, or AioContext
  that protects each shared field.
- Before sharing state between contexts (vCPU threads, IRQ, softirq,
  iothreads, migration thread), ask what happens if another context changes
  it concurrently. If the answer is not "nothing", isolate or lock it.
- Land scaffolding first: tests, tracepoints, and shared types before features.
