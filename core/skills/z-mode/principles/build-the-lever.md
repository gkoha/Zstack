# Build the lever

When the work is not trivial, build the tool that does it or proves it, instead
of doing it by hand.

- Examples: a Coccinelle semantic patch, a `sed`/`git grep` script, a
  KVM selftest, a qtest, a VM boot script, a trace-parsing script.
- Do the first unit by hand, build the tool, and prove it reproduces that unit.
  Make it safe to rerun.
- Keep the tool in the task's `scripts/` directory. A reviewer reruns it.
- Write the smallest script that works, never a framework.
