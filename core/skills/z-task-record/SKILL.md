---
name: z-task-record
description: Create or update the local `.mydoc/` task record for a development task in a kernel, QEMU, or other virtualization repository. Use before the first edit of a task that changes project files or runs builds, tests, VMs, or debugging sessions worth keeping. Do not use for pure questions, code reviews, or skill and AI-tool configuration maintenance.
---

# Task record

A task record keeps the plan, commands, results, and artifacts of one task in
the repository's `.mydoc/` directory, outside of any patch.

## Project rules first

If the repository has its own task-record rules (a project-local skill such as
`qemu-codebase` or `linux-kernel-development`, or rules in `.mydoc/README.md`),
follow them. They decide the directory names, the readme file name, and which
tasks need a record. Use the defaults below only for what they leave open.

## When a record is needed

- Needed: a task that changes project files, and a debugging, build, test, or
  performance session whose commands and results should be kept.
- Not needed: explanations, reviews, static reading, and maintenance of skills
  or AI-tool configuration.
- A task that starts as research and later needs edits gets its record before
  the first edit.

## Steps

1. Decide whether the request continues an existing task. Search
   `.mydoc/README.md` and the task directories. Reuse a match.
2. For a new task, create `.mydoc/YYYY-MM-DD-short-name/`. Add a numeric suffix
   if the path exists. Create inside it exactly:
   - `README.md`: the task objective, scope, plan, and dated log.
   - `output/`: logs, generated results, and reports.
   - `knowledge/`: analysis, references, and notes worth reusing.
   - `scripts/`: task-specific scripts.
   Ask the user before creating any other directory.
3. Create `.mydoc/README.md` if it is missing. Add one line per task: name,
   purpose, status, and a relative link.
4. Check that `.mydoc/` is ignored: `git check-ignore -q .mydoc`. If it is not,
   add `/.mydoc/` to `.git/info/exclude`. Do not edit the tracked
   `.gitignore` for this.
5. After each working session, append a dated entry: actions, commands, results,
   failures, changed files, checks run, and next steps.
6. When a new finding contradicts an earlier entry, correct the earlier claim
   and note what replaced it.

## Rules

- Keep source changes in their normal repository paths. Record the paths in the
  log instead of copying files into `output/`.
- Do not reorganize task directories that use an older layout. Ask first.
- Never include `.mydoc/` content in a commit or patch.
