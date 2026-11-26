# Separate before serializing shared state

When concurrent contexts or parallel workers might write the same struct,
file, branch, or state directory, ask first whether they need one shared
object or are publishing independent facts.

- Default to isolating writes: per-CPU data, per-vCPU or per-AioContext
  state, RCU-published snapshots, or separate worktrees and output files per
  worker, merging only at read time. Two workers updating different fields of
  the same file or struct is still shared mutation.
- Serialize structurally (a lock with a documented order, a single writer
  thread, atomic compare-and-swap, or sequential phases) only when a single
  shared write target is a genuine invariant.
- Prose instructions are not concurrency control. "We need a lock" is a smell
  to inspect before adding one.
