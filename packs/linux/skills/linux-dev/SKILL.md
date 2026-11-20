---
name: linux-dev
description: Linux kernel development knowledge for virtualization work - KVM, VFIO and mdev, iommufd and IOMMU drivers, virtio and vhost, GPU passthrough and vGPU drivers, builds, selftests, and kernel debugging. Use when reading, debugging, or changing kernel source in any Linux tree (mainline, stable, or a vendor kernel). Use linux-upstream only for patches meant for a kernel mailing list.
---

# Linux kernel development

## Repository rules first

- If the tree has a project-local skill (for example
  `linux-kernel-development`) or `.mydoc/README.md`, follow its rules first.
  They override this file where they differ.
- For AI-assisted work, read `Documentation/process/coding-assistants.rst`
  and `Documentation/process/generated-content.rst`. Never add
  `Signed-off-by:`.
- Work on a local branch in this tree. Ask before creating a worktree in
  another directory. Preserve the user's uncommitted changes.

## Task records

Use `z-task-record` with the layout existing kernel records use unless the
tree says otherwise: `.mydoc/<short-task-name>/` containing `README.md`,
`output/`, `knowledge/`, and `scripts/`. Keep `.mydoc/` and local debug
directories out of patches.

## Where virtualization code lives

| Area | Code | Read first |
| --- | --- | --- |
| KVM core | `virt/kvm/`, `include/linux/kvm_host.h` | `Documentation/virt/kvm/api.rst`, `locking.rst`, `vcpu-requests.rst` |
| KVM x86 | `arch/x86/kvm/` (`vmx/`, `svm/`, `mmu/`) | `Documentation/virt/kvm/x86/` |
| KVM arm64 | `arch/arm64/kvm/` | `Documentation/virt/kvm/arm/` |
| KVM uAPI | `include/uapi/linux/kvm.h` | `Documentation/virt/kvm/api.rst` |
| VFIO core | `drivers/vfio/`, `include/linux/vfio.h` | `Documentation/driver-api/vfio.rst` |
| VFIO PCI and variant drivers | `drivers/vfio/pci/` (`nvgrace-gpu/`, `xe/`, `mlx5/`) | `vfio_pci_core.c` and callers |
| Mediated devices (vGPU) | `drivers/vfio/mdev/`, `include/linux/mdev.h`, `samples/vfio-mdev/` | `Documentation/driver-api/vfio-mediated-device.rst` |
| Intel GVT-g | `drivers/gpu/drm/i915/gvt/` | nearby callers |
| iommufd and IOMMU | `drivers/iommu/iommufd/`, `drivers/iommu/` | `Documentation/userspace-api/iommufd.rst` |
| VFIO uAPI | `include/uapi/linux/vfio.h` | `Documentation/driver-api/vfio.rst` |
| virtio and vhost | `drivers/virtio/`, `drivers/vhost/` | `virtio_ring.c` and callers |
| virtio-gpu guest driver | `drivers/gpu/drm/virtio/` | nearby callers |

Use `MAINTAINERS` and `scripts/get_maintainer.pl -f <path>` for subsystem
boundaries. Verify a path exists before citing it.

## Virtualization rules

- Everything from a guest or user space is untrusted: ioctl arguments, guest
  memory, MMIO and PIO exits, hypercalls, virtqueue descriptors. Use
  `copy_from_user`, bounds checks, and `array_index_nospec` for indexes from
  untrusted input. A guest- or user-triggerable `BUG_ON` or `WARN_ON` is a
  bug.
- Know the context: vCPU thread, IRQ, softirq, workqueue, or the VFIO device
  file release path. Follow `Documentation/virt/kvm/locking.rst` for KVM lock
  order. Do not sleep under spinlocks or in atomic context.
- uAPI headers, ioctl numbers and layouts, KVM capabilities, VFIO region and
  IRQ indexes, and documented sysfs files are external contracts. New behavior
  goes behind a new capability or flag. See
  `../z-mode/principles/keep-external-contracts.md`.
- Device release and error paths must undo every allocation, mapping, pin,
  and IRQ registration. VFIO DMA pins and IOMMU mappings leak silently.

## Debugging

- Debug configs: `CONFIG_PROVE_LOCKING`, `CONFIG_KASAN`, `CONFIG_UBSAN`,
  `CONFIG_DEBUG_ATOMIC_SLEEP`, `CONFIG_KMEMLEAK`. See
  `Documentation/dev-tools/`.
- Decode an oops with `scripts/decode_stacktrace.sh` or `scripts/faddr2line`
  against the matching `vmlinux` and modules.
- Tracing: ftrace and `trace-cmd`, KVM tracepoints (`events/kvm/`),
  `perf kvm stat`, bpftrace. Kernel gdb helpers live in `scripts/gdb/`.
- Boot test kernels in a VM (QEMU with `-kernel`) rather than on the host.
  Ask before loading a module or rebooting the host.

## Building and testing

- Build out of tree with `make O=<dir>` when the tree uses one. Find the
  existing build directory and `.config` from context. Do not assume.
- Build the narrowest target first: `make O=<dir> drivers/vfio/` or
  `M=<dir>` for modules, then a full build when shared headers changed.
- A patch must not add warnings. Use `W=1` for the touched files.
- Tests: KVM selftests (`tools/testing/selftests/kvm`), VFIO selftests
  (`tools/testing/selftests/vfio`), kunit (`tools/testing/kunit/kunit.py`).
- For GPU or VFIO hardware that is not present, say which hardware the check
  needs, and run what is possible without it, such as `samples/vfio-mdev`
  sample drivers.
