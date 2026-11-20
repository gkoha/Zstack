# Laziness protocol

Make the smallest change that solves the problem. Fewer lines beat tidy
boilerplate.

- Put each decision in one place and pass the result down as a plain value.
- Do not add a helper, ops table, wrapper, or config knob that has one caller.
- A guard or fallback that "might help" is not part of the fix. Delete it.
- In a kernel or QEMU patch, every changed line must belong to the one logical
  change the commit message describes.
