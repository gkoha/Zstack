# Tool names in Claude Code, Codex, Gemini CLI, and Antigravity

Zstack skills use generic names. Map them to the tools your session has. If a
tool is missing, do the step inline and say so in one line.

| Zstack name | Claude Code | Codex | Gemini CLI | Antigravity |
| --- | --- | --- | --- | --- |
| Run another Zstack skill | `Skill` tool with its name, or read `../<name>/SKILL.md` | Mention `$<name>`, or read `../<name>/SKILL.md` | `activate_skill` with its name, or read `../<name>/SKILL.md` | Read `../<name>/SKILL.md` |
| Todo list | `TodoWrite` when offered, otherwise a list in the reply | `update_plan` when offered, otherwise a list in the reply | `write_todos` | `update_steps` |
| Subagent | `Agent` with `subagent_type: "general-purpose"` | A subagent if the session offers one, otherwise run the step inline | `@generalist` | `invoke_subagent` |
| Read-only subagent | `Agent` with `subagent_type: "Explore"`, and say "do not edit files" in the brief | Same as above, and say "do not edit files" | `@codebase_investigator` | `invoke_subagent` with the `research` type |
| Ask the user | `AskUserQuestion` | Plain text in the reply | `ask_user` | `ask_question` |
| Search code | `Grep`/`Glob`, or `rg` in the shell | `rg` in the shell | `grep_search`/`glob`, or `rg` in the shell | `rg` in the shell |

## Paths

| Item | Claude Code | Codex | Gemini CLI | Antigravity |
| --- | --- | --- | --- | --- |
| Project skills | `.claude/skills/` | `.agents/skills/` | `.agents/skills/` or `.gemini/skills/` | `.agents/skills/` |
| User skills | `~/.claude/skills/` | `~/.agents/skills/` | `~/.agents/skills/` or `~/.gemini/skills/` | `~/.gemini/config/skills/` |
| Project rules | `CLAUDE.md`, else `AGENTS.md` | `AGENTS.md` | `GEMINI.md`, plus `AGENTS.md` only if `context.fileName` lists it | `AGENTS.md` |
| Session transcripts | `~/.claude/projects/<slug>/*.jsonl`, slug is the workspace path with `/` and `.` changed to `-` | `~/.codex/sessions/` | `~/.gemini/tmp/<project_hash>/chats/` | `~/.gemini/antigravity-cli/brain/<conversation-id>/.system_generated/logs/transcript.jsonl` |

Read only the current workspace's transcripts. Never glob across other
projects.

## Invocation

- Claude Code: `/z-mode`. `disable-model-invocation: true` keeps the model
  from starting it on its own.
- Codex: `$z-mode` or `/skills`. `agents/openai.yaml` with
  `allow_implicit_invocation: false` keeps the model from starting it on its
  own.
- Gemini CLI: ask for the skill by name, for example "use the z-mode skill
  for this task". The model calls `activate_skill` and the CLI asks you to
  confirm. Gemini CLI documents only `name` and `description`, so the
  manual-only flags above are not enforced there. The confirmation prompt is
  the only gate.
- Antigravity: mention the skill by name. The same limit applies: nothing
  stops the agent from loading a manual-only skill on its own, so these
  skills rely on their descriptions saying "Use for /z-xxx".
