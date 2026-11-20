---
name: qemu-upstream
description: Rules for preparing patches for upstream QEMU - the AI-content policy, checkpatch, maintainers, commit format, and the security process. Use only when the work is meant to be submitted to the qemu-devel list. Do not use for vendor forks or local experiments.
---

# Upstream QEMU patches

## Policy gate

Read `AGENTS.md` and `docs/devel/code-provenance.rst` before anything else.
Agent output may not be included in an upstream QEMU contribution. Permitted
uses are researching APIs and algorithms, static analysis, debugging, local
experiments not meant for upstream, and trivial non-copyrightable changes.

- If the user asks for code, commit messages, or cover letters that will go
  upstream, decline that part and point to `docs/devel/code-provenance.rst`.
- You may still review the user's own patches, run checks, debug, and explain
  findings.
- Follow `../z-mode/playbooks/preparing-a-series.md` only for checks: build
  each commit, run `scripts/checkpatch.pl`, find maintainers. Do not write the
  upstream text.

## Checks on the user's series

- `scripts/checkpatch.pl` on each patch, or `--branch <base>..HEAD`. Review
  its output by hand.
- Build each commit. Run the tests for the touched area.
- `scripts/get_maintainer.pl -f <file>` for the recipient list.
- Compare against `docs/devel/submitting-a-patch.rst` and `docs/devel/style.rst`:
  subject prefix, `Signed-off-by:` from the author, one change per commit,
  cover letter for a series.
- For Rust changes, consider `make clippy` and `make rustfmt`.

## Security

Potential vulnerabilities follow https://www.qemu.org/contribute/security-process/.
Never file them as public issues or list posts. Check `docs/system/security.rst`
first to decide whether the bug is inside the security boundary.

## Never

Do not add `Signed-off-by:`, send mail, or push.
