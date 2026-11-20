# Attack the premise

When two fixes that share one assumption have failed the same check, suspect the
assumption, not the fixes.

- Write the assumption down in one sentence.
- Find an observation that would come out differently if it were false, and
  make it: a tracepoint, a `printk`/`trace_*` call, a gdb breakpoint, a register
  dump.
- Do not write the next fix until the assumption is written down and tested.
