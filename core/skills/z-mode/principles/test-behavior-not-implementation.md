# Test behavior, not implementation

A test asserts what a user of the interface can observe: return values, error
codes, register values a guest reads back, ioctl results, QMP replies, and
guest-visible state after migration.

Judge each test against two edits:

- Break the behavior. If the test still passes, it proves nothing.
- Change only the internals. If the test fails, it is pinned to the
  implementation.

Keep the tests that catch the first and survive the second. Prefer the
project's existing harness: KVM selftests, kunit, VFIO selftests, qtest,
functional tests.
