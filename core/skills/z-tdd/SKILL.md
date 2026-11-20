---
name: z-tdd
description: Write a failing regression test before a kernel or QEMU fix when a cheap test exists (KVM selftest, kunit, VFIO selftest, qtest, unit test). Use when the user asks for a regression test or TDD, or the bug has an obvious cheap test target. Skip when the only test needs special hardware or a long integration setup.
---

# Failing test first

1. Choose the narrowest existing harness for the code path:
   - Linux: `tools/testing/selftests/kvm`, `tools/testing/selftests/vfio`,
     kunit (`tools/testing/kunit/kunit.py`), subsystem selftests.
   - QEMU: `tests/unit`, `tests/qtest`, `tests/functional`.
   If none fits without large new infrastructure, skip the new test and use
   the closest reproducer script instead. No test is better than a bad test.
2. Write the smallest test that encodes the intended behavior.
3. Run it before the fix and confirm it fails for the intended reason.
4. Fix the bug with the smallest change.
5. Run it again and confirm it passes. Run the neighboring tests.

Do not weaken existing assertions to make a test pass. Report the failing
output, the passing output, and the commands.
