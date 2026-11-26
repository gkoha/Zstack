# Feature map layout example

Put `README.md` and one markdown file per core feature under
`verify-<project>/features/`.

## `features/README.md`

```markdown
# Feature map

| Feature | File | Primary surface |
| --- | --- | --- |
| Guest boot and serial console | `guest-boot.md` | QEMU + Linux `-kernel` |
| VFIO device hotplug and reset | `vfio-hotplug.md` | QMP + guest `dmesg` |
| Live migration round-trip | `live-migration.md` | Source/dest QEMU + QMP |
```

## Example feature file (`features/live-migration.md`)

```markdown
# Live migration round-trip

## Sub-features

- Pre-copy TCP migration between source and destination QEMU instances
- Device VMState preservation across migration
- Post-migration guest workload continuity

## How to reach it (user/guest POV)

Start a source VM running a lightweight guest workload, start a matching
destination VM with `-incoming defer`, trigger migration via QMP, and verify
the guest remains responsive on the destination.

## Driving it with QMP

1. Run Doctor on both source and destination QMP sockets.
2. Issue `migrate-incoming` on destination and `migrate` on source.
3. Poll `query-migrate` until `status` is `completed` (fail on `failed` or
   timeout).
4. Run a guest command over serial/SSH on destination and capture `dmesg`
   and `query-status`.

## Gotchas

- Always start source and destination with identical machine type and device
  properties unless explicitly testing cross-version compatibility.
- Use temporary qcow2 overlays so migration tests never corrupt the base
  guest image.
```
