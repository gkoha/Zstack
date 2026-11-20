---
name: z-architect
description: Sketch structs, function signatures, ownership, locking, and lifetime before writing kernel or QEMU code that crosses a function or file boundary. Use for "design this", "architect this", or a non-trivial change where starting with code would lock in the wrong shape.
---

# Architect

1. Trace every subsystem the change touches: callers, callees, locks, and
   object lifetimes. Cite `file:line`.
2. Sketch two different shapes. For each, write:
   - the new or changed structs and their fields,
   - the function signatures and which file owns them,
   - who allocates and frees each object, and the lifetime mechanism
     (refcount, RCU, devm, QOM parent, `realize`/`unrealize`),
   - the lock or context that protects each shared field,
   - the external contracts it touches (uAPI, QAPI, migration, machine types).
3. Pick the shape where each piece of state has one owner, each operation has
   one code path, and callers need to know the least. Say why the other lost.
4. If the same workaround appears twice in a sketch, redesign instead.
5. Hand the chosen shape to the implementation step and check the diff against
   it.
