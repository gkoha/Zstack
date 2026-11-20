# Feature

1. Create or reuse the task record with `z-task-record`.
2. Trace the affected subsystem. Read the relevant documentation listed in the
   project pack.
3. Run `z-architect`. Name the structs, ownership, locking, and lifetime.
4. If the feature touches an external contract, read
   `principles/keep-external-contracts.md` and decide how old users keep their
   behavior: a capability, a property, or a machine-type compat entry.
5. Write the series plan as todo items. Each item is one reviewable patch that
   builds and passes tests on its own.
6. Implement one patch at a time. Build and run the narrowest test after each.
7. Verify on the real target: boot the guest, exercise the feature, check
   migration or hotplug if the feature affects them.
8. If the design is contested, run `z-interrogate`. If you do not trust a
   change, run `z-blast-radius`.
9. Prepare the series with `preparing-a-series`.

Reply: what you built, the decisions and alternatives, the verification
output, and open questions.
