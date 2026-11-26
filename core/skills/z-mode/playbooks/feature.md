# Feature

You own the design, review, and verification. Delegate implementation to
fresh subagents when the harness offers them; otherwise run inline with the
same review separation.

1. Create or reuse the task record with `z-task-record`.
2. Trace the affected subsystem. Read the relevant documentation listed in the
   project pack.
3. Run `z-architect`. Name the structs, organizing structure
   (`principles/model-the-domain.md`), ownership, locking, and lifetime. When
   multiple valid shapes exist and picking early would lock in the wrong
   design, run `z-arena` instead of guessing.
4. If the feature touches an external contract, read
   `principles/keep-external-contracts.md` and decide how old users keep their
   behavior: a capability, a property, or a machine-type compat entry.
5. Write a throughput checkpoint as four todo items (keep items that do not
   apply as `n/a: <reason>` rather than dropping them):
   - Blocking first steps: shared types, headers, or verification scaffolding
     that must land before fan-out.
   - Independent workstreams: disjoint files, devices, or test suites that
     can run in parallel.
   - Shared mutable state: default to splitting targets
     (`principles/separate-before-serializing-shared-state.md`); serialize
     only for genuine invariants.
   - Smallest safe decomposition: if one owner is best, say why.
6. Write the patch series plan as todo items. Each item is one reviewable
   patch that builds and passes tests on its own.
7. Implement one patch at a time. When delegating to a subagent, pass the
   exact file paths, chosen data shape, and success check; start a fresh
   subagent for each independent unit or fix round, and review the diff
   yourself. Build and run the narrowest test after each patch.
8. Verify on the real target: boot the guest, exercise the feature, check
   migration or hotplug if the feature affects them. "Inconclusive" is not a
   pass.
9. If the design is contested, run `z-interrogate`. If you do not trust a
   change, run `z-blast-radius`. Before patch prep, consider `z-no-comments`
   on the diff.
10. Prepare the series with `preparing-a-series`.

Reply: what you built, the design decisions and alternatives, the throughput
checkpoint, verification output, and open questions.
