# Guard the context window

Large inputs crowd out reasoning.

- Do not read a whole build log, `dmesg`, trace, or core dump into the main
  conversation. Filter it first with `grep`, `tail`, or a script, or hand it to
  a subagent and keep only the reduced finding.
- Read large source files by range, starting from the symbol you need.
- Save raw artifacts in the task's `output/` directory and cite the path.
