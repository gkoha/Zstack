# Prototype

The prototype is a throwaway experiment that settles one question. It is not
the real patch.

1. Write the question in one sentence: which approach is faster, whether the
   hardware behaves this way, whether a guest driver accepts this layout. No
   question means no prototype.
2. Build the smallest thing that answers it, in the task's `scripts/`
   directory or a scratch branch: a small C program, a selftest, a QEMU command
   line, a debug patch with `printk`.
3. Observe the answer directly: output, timing, trace, or guest behavior.
4. Report the answer, the evidence, and the recommended direction. Say that the
   prototype is throwaway. The real work follows `feature` or `bug-fix`.
