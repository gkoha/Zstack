# Sequence verifiable units

Order work as small units that each end in a state you can check.

- Each patch in a series builds and passes tests on its own. This keeps
  `git bisect` working.
- Order the series to prove itself: preparation and removal first, the new
  test before the fix when it is cheap, then the change.
- In a mechanical sweep, check after each unit, even when a tool made the edit.
- Before sending a series, build each commit, for example with
  `git rebase -x '<build command>' <base>`.
