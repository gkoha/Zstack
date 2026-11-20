# Keep external contracts

Some interfaces outlive the code and cannot be changed in a refactor. Treat a
change to them as a design decision, not an edit.

- Kernel: uAPI headers under `include/uapi/`, ioctl numbers and struct
  layouts, sysfs and debugfs files documented in `Documentation/ABI/`, KVM
  capabilities, VFIO region and IRQ layouts.
- QEMU: QAPI/QMP schemas, command-line options, device property names and
  defaults, migration stream sections and `VMStateDescription` versions,
  machine-type compatibility (`hw_compat_*`), and guest-visible device
  behavior.
- New behavior is opt-in or gated by a capability, a property, or a new
  machine type. Old behavior stays for old users.
- Removal follows the project's deprecation process.
- State in the commit message which contract the change touches and why it
  stays compatible.
