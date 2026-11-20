# Boundary discipline

Validate where untrusted data enters, then trust it inside.

- In virtualization the boundaries are: guest-written registers, MMIO/PIO
  accesses, virtqueue descriptors, DMA addresses, hypercall arguments, ioctl
  arguments from user space, QMP/command-line input, and incoming migration
  streams.
- Check sizes, offsets, indices, and overflow at that point, once. Use
  `copy_from_user`, `array_index_nospec`, `address_space_*` result checks, or
  `VMSTATE_*` validation as the code base does.
- Do not re-check the same value in every internal helper.
- A guest-triggerable `BUG_ON`, `assert`, or `abort` is a boundary failure.
  Report and fail the request instead.
