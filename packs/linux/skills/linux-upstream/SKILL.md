---
name: linux-upstream
description: Rules for preparing Linux kernel patches for a mailing list - AI-assistance disclosure, DCO, checkpatch, maintainers, commit format, Fixes tags, and the security process. Use only when the work is meant to be posted upstream or to a kernel list. Do not use for local experiments.
---

# Upstream kernel patches

Read first, in full: `Documentation/process/coding-assistants.rst`,
`Documentation/process/generated-content.rst`, and
`Documentation/process/submitting-patches.rst`. Do not rely on keyword search.

## AI-assistance rules

- Never add `Signed-off-by:`. Only the human can certify the DCO. The human
  reviews the whole contribution and adds their own sign-off.
- Disclose meaningful tool or AI use in the changelog or cover letter: which
  tools were used and for which part.
- For a bug found and fixed with AI help, follow the procedure in
  `coding-assistants.rst`: reproduce, fix, build without new warnings, pass
  `checkpatch.pl`, commit with a `Fixes:` tag, find maintainers, and state
  explicitly what could not be built, tested, or reproduced.

## Checks

- `scripts/checkpatch.pl --strict` on each patch. Review its output by hand.
- Build each commit, with `W=1` for touched files. Run relevant selftests or
  kunit tests.
- `scripts/get_maintainer.pl <patch>` for recipients.
- Subject prefix copied from `git log --oneline -- <file>`. Body wrapped at 75
  columns. `Fixes: <12-char sha> ("<subject>")` when it applies.
- Generate with `git format-patch` into the task's `output/` directory when the
  user asks. Use `-v<N>` and a cover letter for a series.

## Security

Read `Documentation/process/threat-model.rst` to decide whether a bug is a
vulnerability. Vulnerabilities follow `Documentation/process/security-bugs.rst`
and are never posted publicly. Leave the decision and the sending to the user.

## Never

Do not send mail, post to a list, or push. The user sends the patches.
