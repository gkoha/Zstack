---
name: qemu-dev
description: QEMU development knowledge for virtualization work - KVM accelerator, VFIO and iommufd, virtio and vhost, virtio-gpu, migration and VMState, machine-type compatibility, tracing, builds, and tests. Use when reading, debugging, or changing QEMU source in any repository that contains QEMU (upstream, a vendor fork, or a vGPU project). Use qemu-upstream only for patches meant for upstream QEMU.
---

# QEMU development

## Repository rules first

- Read the repository's `AGENTS.md` and `docs/devel/code-provenance.rst` when
  they exist. In upstream QEMU, agent output may not go into upstream
  contributions. Permitted uses are research, static analysis, debugging,
  local experiments not meant for upstream, and trivial changes. Flag this
  early when a request would cross it.
- If the repository has its own `qemu-codebase` skill, read it for orientation
  and its task-record rules. It overrides this file where they differ.
- Before calling a crash a security bug, read `docs/system/security.rst`. Only
  bugs that break guest isolation with KVM or Xen on virtualization boards and
  devices count. TCG is out of scope. Never report one publicly.

## Task records

Use `z-task-record` with this layout, which matches existing QEMU records:
`.mydoc/YYYY-MM-DD-short-name/` containing `readme.md`, `outputs/`,
`knowledge/`, and `scripts/`.

## Where virtualization code lives

| Area | Code | Read first |
| --- | --- | --- |
| KVM accelerator | `accel/kvm/`, `target/*/kvm/`, `hw/i386/kvm/` | `include/system/kvm.h` and callers |
| VFIO devices | `hw/vfio/` | `docs/devel/vfio-iommufd.rst` |
| iommufd backend | `backends/iommufd.c`, `hw/vfio/iommufd.c` | `docs/devel/vfio-iommufd.rst` |
| vfio-user | `hw/vfio-user/` | `docs/system/devices/vfio-user.rst` |
| virtio and vhost | `hw/virtio/` | `docs/devel/migration/virtio.rst` |
| virtio-gpu, vhost-user-gpu | `hw/display/virtio-gpu*.c`, `hw/display/vhost-user-gpu.c` | nearby callers |
| Migration | `migration/`, `include/migration/vmstate.h` | `docs/devel/migration/main.rst` |
| VFIO migration | `hw/vfio/migration*.c` | `docs/devel/migration/vfio.rst` |
| Machine-type compat | `hw_compat_*` in `hw/core/machine.c` | `docs/devel/migration/compatibility.rst` |
| QOM, qdev, reset | `qom/`, `hw/core/` | `docs/devel/qom.rst`, `qdev-api.rst`, `reset.rst` |
| Memory API | `system/memory.c`, `system/physmem.c` | `docs/devel/memory.rst` |
| QAPI and QMP | `qapi/` | `docs/devel/qapi-code-gen.rst` |

Use `MAINTAINERS` and `scripts/get_maintainer.pl --nogit -f <path>` to find
subsystem boundaries. Verify a path exists before citing it.

## Virtualization rules

- Guest-written registers, MMIO and PIO accesses, virtqueue descriptors, and
  DMA addresses are untrusted. Validate at the device model boundary. A
  guest-triggerable `assert()`, `abort()`, or `g_assert()` is a bug.
- Know which context runs the code: a vCPU thread, the main loop with the BQL,
  an iothread with its AioContext, or the migration thread. Check
  `bql_locked()` assumptions and `docs/devel/multiple-iothreads.rst`.
- A change to device state that a guest can observe needs migration handling:
  a `VMStateDescription` field, a subsection with a `needed` callback, or a
  property with a compat entry so old machine types keep old behavior.
- Check a migration change with `scripts/vmstate-static-checker.py` and, when
  possible, a migration between the old and new binary.
- A new device property default or guest-visible behavior on an existing
  machine type needs a `hw_compat_*` entry.
- Device realize must clean up everything it allocated on each error path.
  Unrealize and reset must undo realize-time and runtime state.

## Debugging

- Tracing: `docs/devel/tracing.rst`. Add trace events in the subsystem's
  `trace-events` file. Enable at runtime with `-trace` or QMP `trace-event-set-state`.
- `-d` logging, `-D <file>`, QEMU's gdbstub (`-s -S`) for the guest, and gdb
  attached to the QEMU process for QEMU itself.
- Run under ASan or UBSan with a sanitizer build when memory errors are
  suspected.

## Building and testing

- QEMU builds out of tree, and a checkout may have several build directories.
  Find the configured one from context (a directory containing `meson-info/`).
  Do not assume `build/`.
- Build with `make -C <builddir>` or `ninja -C <builddir>`. Run tests through
  that directory's `pyvenv` and `meson test` wrapper.
- Choose the narrowest test: one qtest (`tests/qtest/`), one unit test
  (`tests/unit/`), one functional test (`tests/functional/`), or the migration
  tests (`tests/qtest/migration/`). Run `make check-qtest` or wider suites only
  when the change is shared.
- For VFIO and GPU changes that need hardware, say which hardware the check
  needs when it is not present, and run what is possible without it.
