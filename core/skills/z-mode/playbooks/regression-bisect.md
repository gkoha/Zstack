# Regression bisect

1. Create or reuse the task record with `z-task-record`.
2. Find a known-good and a known-bad commit or release. Confirm both on the
   real target before bisecting.
3. Write a script in `scripts/` that builds, runs the reproducer, and exits
   0 for good, 1 for bad, 125 for "cannot test". Apply
   `principles/build-the-lever.md`.
4. Run `git bisect start <bad> <good>` and `git bisect run <script>`. Ask the
   user first if the bisect would take hours of machine time or needs another
   worktree.
5. Verify the result. Revert the culprit on top of the bad commit and confirm
   the bug disappears.
6. Read the culprit commit and its discussion with `z-why`. Decide whether to
   fix forward or revert.
7. Continue with `bug-fix` from step 5.

Reply: the culprit commit, the bisect log path, and the revert check output.
