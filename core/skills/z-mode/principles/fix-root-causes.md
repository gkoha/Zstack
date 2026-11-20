# Fix root causes

Fix the first place the system did something wrong, not the place it crashed.

- Reproduce first. Ask "why" until the answer is a wrong decision in the code.
  When stuck, add tracing and read the actual state.
- Ask whether the state that triggered the symptom is legitimate. If it is,
  handle it. If it should never exist, a check at the crash site hides the bug.
  Find what produced the state.
- Guards, retries, swallowed errors, and clamped values are the usual ways to
  hide a bug.
- Fix the pattern: `git grep` for the same mistake elsewhere.
- Name the commit that introduced the bug for the `Fixes:` tag when there is
  one.
