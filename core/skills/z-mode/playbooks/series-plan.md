# Series plan

The plan is the deliverable. Do not implement.

1. If the change is one or two patches with an obvious approach, say so and
   skip the plan.
2. Settle open technical questions with `prototype`. Ask the user only for
   direction that no experiment can settle.
3. Write the plan in the task's `knowledge/` directory. Start with the goal, the
   patch list in order, and the dependencies between patches. Then one section
   per patch: files it touches, the one change it makes, the external contract
   it affects, and how it is verified.
4. Each patch must build and pass tests on its own.
5. Hand back the plan path. Implementation starts when the user says so.
