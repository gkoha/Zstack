---
name: z-how
description: Explain how a kernel, KVM, VFIO, or QEMU subsystem or code path works, or where a change should live. Use for "how does X work", walkthroughs before changing code, and placement or layering questions. Use z-why for history and motivation.
---

# How

1. State your reading of the question if it is ambiguous, then explore.
2. Start from the symbol or file named, else from `MAINTAINERS` and `git grep`.
   Follow the path end to end: entry point (ioctl, MMIO handler, QMP command,
   VM exit), the core logic, and the exit or completion.
3. For a large area, hand the exploration to a read-only subagent with this
   brief: "Explain this area to a senior engineer new to it. Cite `file:line`
   for every claim. Do not edit files." Review the result before presenting it.
4. Write: overview, key structs and their owners, the step-by-step flow with
   `file:line`, the locking and lifetime rules, and the gotchas.
