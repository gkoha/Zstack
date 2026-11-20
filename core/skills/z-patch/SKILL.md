---
name: z-patch
description: Write commit messages, cover letters, and patch series for mailing-list projects such as Linux and QEMU. Use when committing, rebasing into a series, or drafting a changelog or cover letter. The project pack's upstream skill adds project-specific rules.
---

# Commits and patch series

Read the project pack's upstream skill (`linux-upstream`, `qemu-upstream`)
and the project's AI-content policy first. They override this file.

## One commit, one logical change

- Each commit builds and passes tests on its own, so `git bisect` keeps working.
- Do not mix refactoring, whitespace changes, and behavior changes in one
  commit.
- Stage only the files you changed: `git add <files>`, never `git add -A`.

## Subject

`subsystem: imperative summary`, about 50 to 70 characters, no trailing period.
Copy the prefix style from `git log --oneline -- <file>` for the files you
touch.

## Body

Wrap at 72 to 75 columns. Explain, in this order:

1. The problem and its user-visible or guest-visible effect.
2. Why it happens: the root cause, with the function name.
3. What the change does, and the alternatives rejected when a reviewer would
   ask.
4. How it was verified: the test, the reproducer, and the setup. For
   performance, the numbers with run count and spread.

## Tags

- `Fixes: <12+ char sha> ("<full subject>")` only when a specific commit
  introduced the bug.
- `Link:`, `Closes:`, `Reported-by:`, `Suggested-by:` only when they apply.
- Never add `Signed-off-by:`, `Reviewed-by:`, `Tested-by:`, or `Acked-by:`
  for anyone. The human adds their own `Signed-off-by:` when submitting.
- Disclose meaningful tool or AI assistance as the project requires.

## Cover letter

For a series of two or more patches: the goal, the design in a few paragraphs,
the patch overview, the testing, and the changes since the previous version
(`v2:`, `v3:`). Keep long logs in a link, not the letter.

## Never

Do not run `git send-email`, post to a list, or push unless the user asked for
that action in this session.
