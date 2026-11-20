# Tool names in Claude Code and Codex

Zstack skills use generic names. Map them to the tools your session has. If a
tool is missing, do the step inline and say so in one line.

| Zstack name | Claude Code | Codex |
| --- | --- | --- |
| Run another Zstack skill | `Skill` tool with its name, or read `../<name>/SKILL.md` | Mention `$<name>`, or read `../<name>/SKILL.md` |
| Todo list | `TodoWrite` when offered, otherwise a list in the reply | `update_plan` when offered, otherwise a list in the reply |
| Subagent | `Agent` with `subagent_type: "general-purpose"` | A subagent if the session offers one, otherwise run the step inline |
| Read-only subagent | `Agent` with `subagent_type: "Explore"`, and say "do not edit files" in the brief | Same as above, and say "do not edit files" |
| Ask the user | `AskUserQuestion` | Plain text in the reply |
| Search code | `Grep`/`Glob`, or `rg` in the shell | `rg` in the shell |

## Paths

| Item | Claude Code | Codex |
| --- | --- | --- |
| Project skills | `.claude/skills/` | `.agents/skills/` |
| User skills | `~/.claude/skills/` | `~/.agents/skills/` |
| Project rules | `CLAUDE.md`, else `AGENTS.md` | `AGENTS.md` |
| Session transcripts | `~/.claude/projects/<slug>/*.jsonl`, slug is the workspace path with `/` and `.` changed to `-` | `~/.codex/sessions/` |

Read only the current workspace's transcripts. Never glob across other
projects.

## Invocation

- Claude Code: `/z-mode`. `disable-model-invocation: true` keeps the model
  from starting it on its own.
- Codex: `$z-mode` or `/skills`. `agents/openai.yaml` with
  `allow_implicit_invocation: false` keeps the model from starting it on its
  own.
