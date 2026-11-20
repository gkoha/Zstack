---
name: z-interrogate
description: Adversarial review of a kernel or QEMU change or design where only findings proven by a run survive. Use for "interrogate", "adversarial review", "stress test this", or "find the holes". Reports findings and does not apply fixes.
disable-model-invocation: true
---

# Interrogate

1. Frame. The scope is what the user names, otherwise the branch diff against
   its merge base plus the working tree. Restate the intent in one paragraph
   from the request, the commits, and the cover letter.
2. Attack. Use 2 or 3 independent reviewers when the session offers subagents
   (see `../z-mode/references/harness.md`), otherwise do the passes yourself
   one at a time. Give each reviewer the scope, the intent, and this brief:

   > Break this change. Prove each finding by running real code: a failing
   > test, a reproducer, a lockdep, KASAN, or UBSAN splat, a guest that
   > misbehaves, or a migration that fails. Report the exact command, its
   > output, and the output the intent requires. Leave out anything you did
   > not run, including style and naming. No findings is a valid result.

   Point reviewers at the usual weak spots: guest-controlled input, error
   paths, hotplug and reset, migration, concurrency, and other architectures.
3. Verify. Rerun each finding's command yourself. Keep it only if the output
   shows the failure and the failure breaks the intent. Merge findings with the
   same root cause.

Reply: the intent, each verified finding with command, output, and impact,
and the count of dropped findings with reasons.
