# Authoring a skill

1. Decide where it belongs. Ask: does it still hold in another repository that
   uses the same project? Yes: the project pack in Zstack. Only in this
   repository: the repository's own `.agents/skills/`. In every project: Zstack
   `core`.
2. Write `SKILL.md` with `name` and `description`. The description says when
   to use the skill and when not to.
3. Workflow skills that must start only on request get
   `disable-model-invocation: true` and an `agents/openai.yaml` with
   `allow_implicit_invocation: false`.
4. Keep only text that changes a decision. Point to project documents instead
   of copying them.
5. Run `python3 scripts/check-skills.py` in the Zstack repository.
