# Minimize reader load

Reader load is the work a reviewer does to understand the code: layers to trace
and mutable state to keep in mind.

- Inline wrappers and ops tables that only forward to one implementation.
- Prefer return values over out-parameters and globals. Keep state local.
- State a locking or lifetime invariant once, next to the struct field, not in
  every caller.

The test: can a reviewer answer "where does this value come from?" and "what
can change it?" in 30 seconds?
