# Type system discipline

Make the compiler and static checkers reject impossible states, swapped
arguments, and unvalidated external data before tests even run.

- Wrap semantically distinct primitives instead of passing raw `int`, `u64`,
  or `void *` across boundaries (distinct structs, `typedef` handles, or
  explicit enums for states and error domains).
- Use kernel and QEMU static annotations wherever the codebase supports them:
  `__user`, `__iomem`, `__rcu`, `__bitwise`, `__le32`/`__be32`,
  `__acquires`/`__releases`, and `const` on read-only views. Check with
  `sparse` (`C=1`) or `W=1` when available.
- Treat guest memory, ioctl arguments, sysfs writes, QMP payloads, and
  migration streams as untrusted bytes until parsed and bounds-checked at the
  boundary into a validated internal struct.
- Encode layout and enum invariants at compile time with `BUILD_BUG_ON`,
  `QEMU_BUILD_BUG_ON`, or `static_assert`, and handle enum variants
  exhaustively so adding a variant breaks the build until every switch deals
  with it.
