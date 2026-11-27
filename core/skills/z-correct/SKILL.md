---
name: z-correct
description: Find the mistakes agents keep repeating in a kernel, QEMU, or virtualization repository and make each one impossible. Try architecture first, then types/compiler/static checks, then a behavior test, and write docs last. Prove each check fails on a real past mistake. Use for /z-correct or $z-correct.
disable-model-invocation: true
---

# Correct

When agents keep making the same mistake in a repository, change the
repository so the next agent cannot make it again.

Assume every contributor is an agent that sees only the files it opened,
copies the nearest example, and takes the shortest path that compiles. Shape
the repository so a change that looks right from one file is right for the
whole tree.

## Find the mistake classes

Read recent commits, reverts, review comments, `AGENTS.md`/`CLAUDE.md`/`GEMINI.md`,
`.mydoc/` task records, and comments explaining workarounds. Group recurring
failures into classes. A class counts once it has happened twice.

## Fix each class at the highest level that works

1. **Eliminate it with architecture.** Give each piece of state one owner and
   each task one supported code path. Hide internal helpers (`static`, private
   headers) so the wrong call will not build. Replace hand-synced lists or
   tables with a single source of truth. Delete legacy paths and dead code an
   agent would copy.
2. **Enforce it at build or check time.** Use the type system, compiler flags
   (`W=1`), `sparse` annotations (`__user`, `__iomem`, `__rcu`), `BUILD_BUG_ON`
   / `QEMU_BUILD_BUG_ON`, `scripts/vmstate-static-checker.py`, Coccinelle
   rules, checkpatch extensions, or a repo check script whose error message
   names the exact file, macro, or API to use instead. If the bad pattern
   already exists in legacy code, fail only on new occurrences in the diff.
3. **Test the behavior.** Add or fix a narrow test (KVM/VFIO selftest, kunit,
   qtest, or unit test). Fix or delete any test that keeps passing when the
   guarded behavior breaks, or breaks when only internals change.
4. **Write docs or agent rules last, only for judgment calls.** Nothing fails
   when an agent skips prose.

Respect repository scope: in an upstream Linux or QEMU tree where repository
files cannot carry local-only harness rules, put repo-local checks in the
appropriate project workflow or note what belongs in a local script vs an
upstream patch.

## Fix and prove

Fix the most frequent classes now, one logical commit per class. Prove each
new check fails on a real past mistake (reproduce the broken pattern on a
scratch change, capture the failure, then revert the scratch change). Run the
same check locally and in CI when CI exists. Any exception goes on the
offending line with a concrete reason and owner approval.

## Keep the rule table

Maintain a compact table in the repository's agent instruction file
(`AGENTS.md`, `CLAUDE.md`, or `GEMINI.md`) pairing each durable rule with what
enforces it.
When the user corrects a mistake, fix the mistake and update the table. If a
rule is already listed with no enforcement and the mistake repeats, escalate
it to a higher level in the same change. Drop a rule once the mistake can no
longer happen.

Reply: each mistake class with its evidence, the enforcement level chosen,
why a higher level did not work, and the proof that each new check catches a
real past mistake.
