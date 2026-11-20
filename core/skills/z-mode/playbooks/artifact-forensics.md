# Artifact forensics

The capture already exists: a kernel oops, a vmcore, a QEMU core dump, a
`dmesg` log, a QEMU log, a trace file, or a CI failure log. Read it. Do not
rerun it unless asked.

1. Identify the format and load it with the right tool: `scripts/decode_stacktrace.sh`
   or `faddr2line` for an oops, `crash` for a vmcore, `gdb` with matching
   binaries for a core dump, `trace-cmd report` or the QEMU `simpletrace.py`
   for traces.
2. Confirm you have the matching build: same commit, config, and debug info.
   Without matching symbols, say so. A frame without a source line is not yet a
   diagnosis.
3. Narrow to the first wrong event, not the last crash. Read back from the
   crash to the first warning, the first error, or the first unexpected state.
4. Map it to source: file, function, line.
5. If a second artifact exists from a good run, diff the two. Otherwise call
   the finding the strongest hypothesis the artifact supports.

Reply: the artifact, the finding, the source location, and whether it is
confirmed or a hypothesis.
