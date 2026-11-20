# Runtime forensics

Diagnose a live system by instrumenting it. The output is a cited diagnosis,
not a fix.

1. Capture a signal from the running system: `perf`, ftrace or `trace-cmd`,
   bpftrace, `kvm_stat`, gdb attached to QEMU, QEMU `-trace` or `trace-event`
   over QMP, the guest kernel through QEMU's gdbstub, or `/proc` and debugfs.
2. Reduce the signal to the finding: the hot function, the stuck thread and
   its wait reason, the exit that loops without progress. Parse large output in
   a script or subagent per `principles/guard-the-context-window.md`.
3. Prove the mechanism cheaply: one extra tracepoint, a breakpoint, or a
   changed parameter that should change the result.
4. Map the finding to source: file, function, line.

Ask before attaching to production processes, enabling heavy tracing on a
shared host, or running as root on the host.

Reply: the signal, the finding, the proof, the source location, and the
artifact paths. Route to `bug-fix` or `perf-issue` for the fix.
