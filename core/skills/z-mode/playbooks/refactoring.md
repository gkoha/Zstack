# Refactoring

The structure changes. The behavior does not. If you find a bug, split it out
and route it to `bug-fix`.

1. Create or reuse the task record with `z-task-record`.
2. Pin the behavior first: an existing test, a new characterization test, or a
   script that records output before and after. Compiling is not a pin.
3. Name the target structure. Apply `principles/model-the-domain.md` and
   `principles/redesign-from-first-principles.md`.
4. Subtract first: dead code, one-caller wrappers, stale `#ifdef` branches.
5. Move in small steps that keep the pin green. For an internal API change,
   apply `principles/migrate-callers-then-delete.md`. Do not touch external
   contracts.
6. Prove behavior is unchanged with the pin on the real artifact.
7. Keep the change only if it lowers reader load. Otherwise revert it.
8. Prepare the series with `preparing-a-series`: removals, then the reshape.

Reply: the structure that changed, the pin, the equivalence evidence, and what
was reverted.
