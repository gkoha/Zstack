# Figure it out

When no playbook fits, design one before writing code.

1. Frame: the definition of done as a checkable statement, the scope, the
   risks, and the rigor level. Higher for external contracts and guest-visible
   changes.
2. Design: split the work into independently verifiable units, riskiest
   unknown first. Build the verification script before the work and record the
   baseline.
3. Write the phase list into the task readme and present it. A multi-hour run
   gets one checkpoint with the user.
4. Run each unit as an experiment: hypothesis, smallest change, check on the
   real artifact, keep or revert. Log each result in the task readme.
5. Finish with `principles/prove-it-works.md` against the definition of done.
