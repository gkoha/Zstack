---
name: z-sharpen
description: Make a kernel, QEMU, or virtualization task deeper rather than bigger, then rewrite the prompt around primary evidence, specialist tools, and objective proof. Use for /z-sharpen or $z-sharpen.
disable-model-invocation: true
---

# Sharpen

Produce a deeper version of the user's task, not a broader one. Before
rewriting the prompt, answer four questions concretely in the domain of the
task:

1. What would a senior kernel, QEMU, or virtualization maintainer do here
   that the user is not asking for?
2. What is the rawest primary material they would start from instead of
   pre-digested summaries (for example: raw ftrace/perf/kvm_stat traces,
   dmesg/vmcore, hardware or virtio spec sections, git history, or exact QMP
   / ioctl bytes)?
3. Which specific methods and tools would they use (for example: `perf kvm
   stat`, `trace-cmd`, `scripts/vmstate-static-checker.py`, `sparse C=1`,
   `lockdep`/KASAN, `git bisect`, or a narrow selftest/qtest)?
4. What, other than the agent or the user saying so, would prove the result
   is right?

Then rewrite the user's prompt to ask for exactly that.

Have the rewritten prompt instruct the agent to prototype or measure any
choice an experiment can settle and recommend an option based on observed
data, while leaving external-contract or preference calls that no experiment
can settle for the user.
