---
name: z-patch
description: Write commit messages, cover letters, and patch series for mailing-list projects such as Linux and QEMU. Use when committing, rebasing into a series, or drafting a changelog or cover letter. The project pack's upstream skill adds project-specific rules.
---

# Commits and patch series

Read the project pack's upstream skill (`linux-upstream`, `qemu-upstream`)
and the project's AI-content policy first. They override this file. Apply
`z-writing` to every subject, commit body, and cover letter.

## One commit, one logical change

- Each commit builds and passes tests on its own, so `git bisect` keeps working.
- Do not mix refactoring, whitespace changes, and behavior changes in one
  commit.
- Stage only the files you changed: `git add <files>`, never `git add -A`.

## Subject

`subsystem: imperative summary`, about 50 to 70 characters, no trailing period.
Copy the prefix and phrasing style from `git log -n 10 --oneline -- <file>`
for the files you touch. Name the concrete action and object; avoid vague
openers such as `Enhance`, `Improve`, `Ensure proper`, `Comprehensive`, or
`Refactor ... for better maintainability`.

## Body

Wrap at 72 to 75 columns. Explain, in this order:

1. The problem and its user-visible or guest-visible effect.
2. Why it happens: the root cause, with the function name.
3. What the change does, and the alternatives rejected when a reviewer would
   ask.
4. How it was verified: the test, the reproducer, and the setup. For
   performance, the numbers with run count and spread.

## Plain commit style

Write like a human maintainer of the repository, not a generated summary:

- Match the tone and brevity of recent commits in `git log -n 10 -- <file>`.
- Use short plain-text paragraphs focused on *why*. Do not narrate the diff
  into a bullet list (`- Added foo()`, `- Updated bar()`, `- Handled edge
  case`); `git show` already shows the diff.
- Plain text only: no Markdown headings (`###`), bold (`**`), fenced code
  blocks, em dashes as connectors, or emoji.
- Cut empty wrap-up sentences (`This improves robustness and maintainability`,
  `This prevents potential issues`, `makes the code cleaner`, or Chinese
  equivalents such as `提升健壮性`, `优化代码结构`, `确保一致性`). State
  the concrete bug, invariant, or behavioral effect instead.

## Tags

- `Fixes: <12+ char sha> ("<full subject>")` only when a specific commit
  introduced the bug.
- `Link:`, `Closes:`, `Reported-by:`, `Suggested-by:` only when they apply.
- Never add `Signed-off-by:`, `Reviewed-by:`, `Tested-by:`, or `Acked-by:`
  for anyone. The human adds their own `Signed-off-by:` when submitting.
- Never add `Co-Authored-By:` for an AI tool or model, and never append
  generated-by footers or banners (`Generated with ...`).
- Only add AI/tool disclosure when the project's upstream policy explicitly
  requires it (for example `linux-upstream`), and use the exact format that
  policy specifies.

## Cover letter

For a series of two or more patches: the goal, the design in a few paragraphs,
the patch overview, the testing, and the changes since the previous version
(`v2:`, `v3:`). Keep long logs in a link, not the letter.

## Never

Do not run `git send-email`, post to a list, or push unless the user asked for
that action in this session.
