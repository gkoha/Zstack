# Make operations idempotent

Design state-changing lifecycle paths, teardown handlers, and automation
scripts to converge to the right end state however many times they run and
wherever a previous attempt failed.

- Derive each step from the state that exists now, not from what a prior run
  intended to do. Read current state, compare to the goal, and apply only the
  difference.
- Make cleanup and error paths safe to re-enter: device `unrealize`, reset,
  hot-unplug, VFIO release, DMA unpin, and test teardown should handle
  partially initialized or already-released resources without leaking or
  double-freeing.
- Make artifacts left behind by a crashed run (temp files, locks, stale VM
  sockets, half-written logs) recognizable as stale on the next run. Write
  files to a temp path and atomically rename into place.
- Ask before shipping: what happens if this runs twice? What if it fails after
  each allocation or registration?
