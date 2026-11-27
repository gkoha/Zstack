---
name: z-recall
description: Reconstruct recent working context from workspace session transcripts, .mydoc/ task records, git history, and live repo state, returning a tight status capsule. Use for /z-recall, $z-recall, "where did I leave off", or "catch me up on X".
disable-model-invocation: true
---

# Recall

Rebuild working context across recent sessions and shared repository history
before starting or resuming work. Keep the result tight and on-topic. Read
only what the in-scope threads require, then stop.

Working context lives in two places:
1. **Your own session history and `.mydoc/` records**: what you tried,
   decided, and left half-done.
2. **The shared record**: commits, reverts, branches, stashes, patch output
   directories, and issue/mailing-list records around the same subsystem. A
   long-running bug or series keeps much of its truth here, so never rely on
   transcripts alone.

See `../z-mode/references/harness.md` for Claude Code, Codex, Gemini CLI,
and Antigravity session transcript paths. Read only the active workspace's
transcripts. Never glob across other projects.

## Steps

1. **Classify, then route.** Resuming one specific interrupted session is
   `../z-mode/playbooks/session-pickup.md`, not `z-recall`. If the user
   already handed you a complete state capsule (branch, paths, exact task),
   use it and skip mining.
2. **Lock the scope before searching.** Pin the time window (default: last 7
   days), the topic or subsystem if named, and the active workspace. State
   the locked scope back. Never silently shrink "all" to "last N".
3. **Mine workspace transcripts and `.mydoc/` records.**
   - Read `.mydoc/README.md` and matching task readmes/decision logs first.
   - For session transcripts, order candidate files by modification time
     (`ls -t`), never by UUID. Grep for the topic first, then read only
     matching regions. Skip the current chat and obvious subagent/test
     noise.
   - When many transcripts match and subagents are available, fan out
     read-only subagents across slices so raw transcripts stay out of the
     main context (`../z-mode/principles/guard-the-context-window.md`). Each
     returns per-session: topic, goal, decisions, open threads, corrections,
     and artifacts (branches, commits, `.mydoc/` paths).
4. **Sweep the shared record whenever a subsystem, file, feature, or bug is
   named.** Run in parallel with step 3:
   - `git log` (including reverts and `Fixes:` commits) on the touched paths,
   - local branches, worktrees, tags, stashes, and patch artifacts in
     `.mydoc/*/output/`,
   - any available issue tracker or mailing-list context if accessible.
   Null results are findings; skip unavailable external tools and say so.
   Skip this step only for pure activity recall ("what did I work on this
   week") with no named target.
5. **Verify against live state.** Check every branch, commit SHA, dirty tree
   file, and patch series surfaced in steps 3-4 with `git status`, `git
   branch -vv`, and `git log`. When an answer hinges on what an earlier
   agent actually ran (commands, exit codes, files read), verify the real
   transcript or `.mydoc/` output rather than trusting a summary.

## Output contract

Lead with the capsule, then thread status, problems, and next move. Cut
everything else.

- **Capsule:** at most 5 bullets stating what this work is and where it
  stands overall.
- **Threads:** one line each, prefixed with exactly one status tag:
  `[merged <sha>]`, `[series ready <path>]`, `[in flight <branch>]`,
  `[verified, uncommitted]`, `[reverted <sha>]`, or `[planned, not started]`.
  Every thread must carry a tag.
- **Problems:** at most 5 recurring blockers, failed approaches, or reverted
  attempts so the next run starts past where the last one failed.
- **Next move:** the single highest-value concrete next action.

Use `z-writing` for plain, concise phrasing.
