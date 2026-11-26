---
name: z-blast-radius
description: Find what a kernel or QEMU change could break outside its diff, and prove the one fact its safety depends on by running code. Use for "blast radius", "what could this break", or a small diff you do not trust.
---

# Blast radius

Companion to `z-how` and `z-why`. `z-how` explains what the code does,
`z-why` explains why it is shaped that way, and `z-blast-radius` finds what a
change breaks somewhere else before it ships.

Listing callers is not the job. `git grep` does that in a second. Find the
breakage that a symbol search does not show.

## Do not trust your own writeup

A blast-radius writeup that sounds convincing is worthless on its own. Find
the one or two facts the whole change depends on and prove them by running
real code.

### How sure are you

For each safety fact the change depends on, push it as far down this ladder
as is cheap, and state explicitly which level you reached:

1. **You said so.** Worthless on its own.
2. **You pointed at the line.** A real `file:line` in the tree or header.
3. **You showed the bad case cannot reach.** You traced the failure path step
   by step and showed why it is impossible.
4. **You ran real code.** A test, selftest, kunit, qtest, or small script
   that exercises the exact code path and fails loudly if the assumption is
   false.
5. **You reproduced it on the live target.** A booted kernel, QEMU guest,
   migration, or lockdep/KASAN run exercising the real surface.

## Steps

1. Read the change: the diff, the symbols it adds, changes, or removes, and
   what now behaves differently, including behavior the diff does not spell
   out. Inspect the commits or series in full.
2. Find the one fact the change is safe because of, for example "this path
   runs only with the BQL held", "no guest can reach this state before
   `realize` completes", or "this ioctl cannot race with `vfio_device_fops`
   release". Spend your time here rather than writing a long list of maybes.
3. Look where grep stops:
   - other architectures and build configurations (`#ifdef`, `Kconfig`, `meson`
     options) that compile the same code differently,
   - user space and guests that read the same bytes: uAPI structs, ioctls,
     sysfs, QMP replies, migration streams, guest-visible registers,
   - other execution contexts: IRQ, softirq, vCPU threads, iothreads,
     migration thread, hotplug and unplug, reset, suspend and resume,
   - error and teardown paths, and old machine types or old kernels on the
     other side of a migration,
   - code two or three hops downstream that assumes an old invariant.
4. Rate each confirmed risk honestly with a real `file:line`, realistic
   likelihood, and real cost. List what you checked and cleared separately. A
   search that finds nothing is still a finding. Never invent a caller.
5. Prove the key fact at Level 4 or Level 5 by running real code: a selftest,
   qtest, lockdep/KASAN/UBSAN run, cross-version migration, or a small
   reproducer script. Paste the command and output. If you cannot prove it,
   mark it `unproven` and state the level where you stopped.
6. For a wide or high-risk change, run this review via `z-arena` or parallel
   reviewers so independent passes catch different failure modes.

Reply:
- **What it does:** including implicit behavior changes.
- **Key safety fact:** the statement, the proof level reached (1-5), and the
  evidence (or `unproven`).
- **Risks:** `file:line`, failure mechanism, likelihood, impact, and how to
  check.
- **Cleared:** what you inspected and why it is safe.
- **Before merging:** the cheapest concrete check or reproducer to run.
