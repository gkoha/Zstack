---
name: z-blast-radius
description: Find what a kernel or QEMU change could break outside its diff, and prove the one fact its safety depends on by running code. Use for "blast radius", "what could this break", or a small diff you do not trust.
---

# Blast radius

Listing callers is not the job. `git grep` does that. Find the breakage that a
symbol search does not show.

1. Read the change: the diff, the symbols it adds, changes, or removes, and
   what now behaves differently, including what the diff does not spell out.
2. Find the one fact the change is safe because of, for example "this path
   runs only with the BQL held" or "no guest can reach this state before
   `realize` completes".
3. Look where grep stops:
   - other architectures and config options (`#ifdef`, `Kconfig`, `meson`
     options) that build the same code differently,
   - user space and guests that read the same bytes: uAPI structs, ioctls,
     sysfs, QMP replies, migration streams, guest-visible registers,
   - other contexts that run the code: IRQ, softirq, vCPU threads, iothreads,
     the migration thread, hotplug and unplug, reset, suspend and resume,
   - error and teardown paths, and old machine types or old kernels on the
     other side of a migration.
4. Rate each risk with a `file:line`, how likely it is, and what it costs.
   List what you checked and cleared separately. Never invent a caller.
5. Prove the key fact by running real code: a test, a selftest, a lockdep or
   KASAN run, a migration between old and new binaries, or a small script.
   Paste the output. If you could not prove it, mark it unproven.

Reply: what the change does, the key fact with its proof or "unproven", the
risks, what was cleared, and the cheapest check to run before merging.
