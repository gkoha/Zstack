# Investigation

Read-only. The output is a cited explanation or a recommendation, not a code
change. No task record.

1. Find the code with `git grep`, `rg`, `MAINTAINERS`, and the project pack's
   orientation section. Read declarations and callers before documentation.
2. For "how does it work", follow `z-how`. For "why is it like this", follow
   `z-why`.
3. Write: overview, key structures, how it works step by step, where things
   live (`file:line`), and gotchas such as locking, lifetime, and contracts.
   For a choice between options, give a tradeoff table and a recommendation.
4. Label each claim: read in code, measured, or inferred.

If the answer leads to a code change, stop and route to `bug-fix` or `feature`.
