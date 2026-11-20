# Prove it works

Verify the real artifact directly. "It compiles", a self-report, and a cached
result do not count.

- Run the changed path: boot the kernel or start QEMU, exercise the device in a
  guest, run the selftest, kunit test, or qtest, and read the actual output.
- When the change cannot run here (missing hardware, no GPU, no nested
  virtualization), say so and name the closest check you did run.
- When a check fails, suspect the observation first: the wrong build
  directory, the module that did not reload, a guest that booted the old
  kernel.
- Script the check when you can and keep it in the task's `scripts/`.
