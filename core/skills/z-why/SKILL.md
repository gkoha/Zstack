---
name: z-why
description: Answer why kernel or QEMU code is the way it is, from the commit history and list discussion rather than guesses. Use for design rationale, "why was this added", regressions, and old decisions.
---

# Why

Answer from the record, not the code.

1. Find the commits: `git log -L <start>,<end>:<file>`, `git log -S <string>`,
   `git blame -w -C`, and `git log --follow`.
2. Read each relevant commit message in full, including `Link:`, `Fixes:`,
   and `Message-Id:` tags. Open the linked list thread on lore.kernel.org or the
   qemu-devel archive when the message is thin.
3. Cite what the authors wrote. Mark your own inferences as inferences. Say
   what the record does not answer.
