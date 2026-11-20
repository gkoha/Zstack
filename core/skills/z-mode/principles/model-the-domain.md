# Model the domain

Encode the domain in a data structure instead of scattered conditionals.

- Use an explicit state enum and transition function instead of several
  booleans that must stay in sync. Device, migration, and vCPU lifecycles are
  state machines.
- Use a table indexed by register offset, capability ID, or exit reason
  instead of a growing `switch` spread across files.
- Do not force it. Keep plain code when the shape is local and will not grow.

The sign you skipped this: a feature adds one more `else if`, or a second flag
that must match the first.
