---
name: z-writing
description: Plain, specific technical writing for replies, documentation, code comments, commit messages, and cover letters. Use when writing or reviewing any prose.
---

# Writing

Write so a tired engineer understands on the first read.

## Content

- Name the real symbol, file, config option, command, or number. Not "this can
  cause issues", but "a guest write to BAR0 offset 0x10 triggers `abort()`".
- Label each claim: read in code (`file:line`), measured (command and output),
  or inferred.
- Cut a sentence that could appear unchanged in another project's docs.

## Sentences

- One idea per sentence. Split a sentence the reader must reread.
- Active voice. Name the actor: the guest, the vCPU thread, the driver.
- Use the plain word: "use", not "utilize" or "leverage".
- Keep "only" and "not" next to the word they change.
- Make each "it", "this", and "they" point at one obvious thing.
- At most one hedge per claim.

## Avoid

- Filler: "in order to", "it is important to note that".
- AI vocabulary: delve, crucial, robust, leverage, landscape, pivotal,
  seamless, showcase, underscore.
- "serves as" or "stands as" instead of "is".
- "Not just X, but Y" constructions, forced lists of three, and dramatic
  reveals.
- Em dashes as connectors. Use a period or a comma.
- Decorative emoji, praise openers, and closing pleasantries.

## Code comments

Comment why, not what: the invariant, the lock that protects a field, the
hardware quirk, the spec section. Delete comments that restate the code.

## Documents

One document has one purpose: a tutorial, a how-to, a reference, or an
explanation. Do not mix them. Headings in sentence case. Numbered lists for
steps, bullets otherwise.
