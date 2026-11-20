---
name: z-benchmark
description: Vet a performance number from a kernel, KVM, QEMU, or guest benchmark before reporting or acting on it. Use when you measure a speedup, a regression, VM-exit counts, latency, or throughput.
---

# Benchmark checklist

Answer each question with evidence from a run.

## Before running

- Write the claim you expect to make, for example "virtio-net RX throughput
  is 15% higher at 64-byte packets with 4 queues".
- Record the setup: host kernel and QEMU commits, configs, CPU model, guest
  kernel, vCPU and memory size, pinning, huge pages, and the exact command line.
- Check the host load with `uptime` and `nproc`. Note CPU frequency governor
  and turbo state when timing matters.

## Questions

1. Why not twice as fast? Name the limiter from a profile you do not report:
   `perf`, `perf kvm stat`, `kvm_stat`, ftrace, VM-exit and interrupt counts.
2. Was every side tuned the same way? Same build type (no debug or KASAN
   build on one side), same kernel parameters, same pinning, same guest image.
3. Does it break physical limits? Compare with link bandwidth, disk bandwidth,
   and CPU time.
4. Did it error? Count failed requests, drops, retransmits, and guest errors.
5. Does it reproduce? Run each side at least 5 times, alternating A and B.
   Report the median and range. A gap smaller than the spread is no difference.
6. Does it matter end to end? Report a micro result next to the workload the
   user cares about.
7. Did the work happen? Confirm the guest ran the workload and the changed
   code path executed, for example with a tracepoint count.

## Report

Lead with the verdict: faster, slower, no measurable difference, or
inconclusive. Give the number, unit, run count, range, and limiter. Keep raw
data in the task's `output/` directory.
