---
name: qemu-upstream
description: Rules for preparing patches for upstream QEMU - checkpatch, maintainers, commit format, series checks, and the security process. Use when preparing patches meant for qemu-devel or a QEMU mailing list. Do not use for local experiments.
---

# Upstream QEMU patches

Follow `../z-mode/playbooks/preparing-a-series.md` and `z-patch` together
with the QEMU-specific checks below.

## Checks

- `scripts/checkpatch.pl` on each patch, or `--branch <base>..HEAD`. Review
  its output by hand.
- Build each commit, not only the last one. Run the tests for the touched
  area.
- `scripts/get_maintainer.pl -f <file>` for the recipient list.
- Compare against `docs/devel/submitting-a-patch.rst` and
  `docs/devel/style.rst`: subject prefix, one logical change per commit,
  cover letter for a series.
- For Rust changes, consider `make clippy` and `make rustfmt`.

## Security

Potential vulnerabilities follow
https://www.qemu.org/contribute/security-process/. Never file them as public
issues or list posts. Check `docs/system/security.rst` first to decide
whether the bug is inside the security boundary.

## Never

Do not add `Signed-off-by:`, send mail, or push. The user reviews the
patches, adds their own `Signed-off-by:`, and sends them.
