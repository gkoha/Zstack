# Subtract before you add

Remove complexity first, then build on the simpler base.

- Delete dead code, unused fields, stale `#ifdef` branches, and one-caller
  wrappers before adding the new shape.
- Design for observed use, not speculative hardware or configurations.
- Order the series so removal patches come before the new feature.
