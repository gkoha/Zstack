# Preparing a series

Turn finished work into patches a maintainer can review. Never send anything.

1. Read the project pack's upstream skill and the project's AI-content policy.
   If the policy forbids AI-generated content in upstream contributions, stop
   and say which part the user must write or rewrite themselves.
2. Rebase into one logical change per commit. Follow
   `principles/sequence-verifiable-units.md`.
3. Build every commit, not only the last one.
4. Run the project's style checker on each patch and review its output by hand.
5. Write each commit message with `z-patch`.
6. Find maintainers and lists with the project's `get_maintainer.pl`.
7. Generate patches with `git format-patch` into the task's `output/` directory
   when the user asks for them.
8. Report the patch list, the checks run, and what the user must do before
   sending: review, sign off, and disclose tool use.
