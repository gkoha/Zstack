---
name: z-no-comments
description: Audit comments and lint/warning suppressions in the current diff for Linux kernel or QEMU code: delete narration and dead code, expose workaround/hack confessions as root-cause refactor targets, and encode real constraints in types, static checks, or tests. Use for /z-no-comments or $z-no-comments before review or patch prep.
disable-model-invocation: true
---

# No comments (comment and workaround audit)

Audit comments and warning suppressions in scope to remove narration noise
and expose workaround code hiding behind prose.

## Scope

Use the files or diff named by the user. Otherwise use the current branch
diff against its merge base plus the working tree.

## Steps

1. **Run the strict comment audit.**
   - When the harness supports subagents (see
     `../z-mode/references/harness.md`), spawn a fresh subagent with
     `references/reviewer-brief.md` and the exact scope. The reviewer
     audits comments and flags `MUST KILL` symbols only; it never edits
     application logic.
   - When subagents are unavailable, run the same strict pass yourself
     following `references/reviewer-brief.md` before moving to step 2.
2. **Inspect the audit report and comment diff.**
   - Reject any application-code edits made during step 1, out-of-scope
     changes, deletions of keep-list-protected comments (SPDX/license,
     locking/memory-barrier annotations, hardware quirks/spec refs,
     public/kernel-doc contracts, verified external-constraint links), or
     false `MUST KILL` flags on legitimately required code.
   - Reshape flags on *our-code surprises* stay actionable; do not restore
     their excuse comments. A keep survives only with proof it documents an
     external constraint we cannot reshape (hardware, guest ABI, spec,
     kernel/QEMU subsystem rule).
   - Audit missed warning/checker suppressions (`__maybe_unused`, pragma
     warning disables, checkpatch/sparse/sanitizer suppressions). Any
     suppression masking a real correctness, lifetime, or safety bug stays
     an actionable `MUST KILL`.
   - Before accepting or restoring thin `IMPORTANT`, `do not remove`,
     `HACK`, or `workaround` comments, trace the named symbol or run `z-why`
     on it. If a keep claim is refuted or remains ambiguous after tracing,
     delete the comment.
   - If a subagent report failed these checks, revert its diff and rerun it
     once with the exact failure named. If a second run fails, stop and
     report it open.
3. **Shape the root-cause fixes.**
   - Fix trivial accepted `MUST KILL` items directly (delete a dead branch,
     drop an unused parameter, rename an opaque symbol, use the proper API).
   - If any accepted fix crosses a function boundary or needs a redesign,
     run `z-architect` once for the accepted set and surrounding code. Stop
     at the sketch; step 4 implements.
4. **Implement the smallest root-cause fix in scope.**
   - Remove each named workaround without widening scope beyond the fence.
   - If the true root cause lies outside scope, land the smallest clean
     in-scope fix and report the remainder open.
   - Follow `../z-mode/principles/fix-root-causes.md` and
     `../z-mode/principles/redesign-from-first-principles.md` for intent,
     without bolting on new symptom guards.
5. **Encode real constraint comments instead of leaving prose.**
   - For comments saying `do not remove`, `must stay in sync with X`, or
     `must be called with lock Y held`, leave verified external keeps alone
     and offer the cheapest in-scope structural encoding for in-tree
     invariants: `lockdep_assert_held()`, `bql_locked()` assertion,
     `BUILD_BUG_ON` / `QEMU_BUILD_BUG_ON`, strong types, a sparse
     annotation, or a regression test.
   - Wait for interactive approval before adding new structural checks
     outside the original diff (unless pre-approved in an autonomous run).
     Once encoded, delete the redundant prose comment; if not approved,
     delete unverified prose or report the unenforced constraint open.
6. **Verify** the tree still builds cleanly without new warnings and narrow
   tests stay green.

Reply: deletion count, restored keep-list comments (if any), `z-architect`
sketch (if run), root-cause fixes applied, constraint encodings added or
offered, unenforced constraints, and remaining open items.
