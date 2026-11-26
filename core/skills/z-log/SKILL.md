---
name: z-log
description: Keep a reviewable, append-only TSV decision trail for long-running, iterative, or unattended kernel and QEMU work, with end-of-run transcript audit and independent review. Use for /z-log, $z-log, figure-it-out, hillclimb, or autonomous runs.
disable-model-invocation: true
---

# Decision log (show your work)

Keep one canonical append-only TSV log so a human reviewer can audit a long,
multi-phase, or unattended run in minutes.

## Format

One TSV file, one row per decision or iteration. Cells stay single-line.
Evidence is always a concrete pointer, never a paragraph.

Header (see `references/decision-log-template.tsv`):

```text
ts	phase	decision	why	evidence	result
```

Columns:
- **ts:** UTC ISO8601 timestamp (`YYYY-MM-DDTHH:MM:SSZ`).
- **phase:** phase, workstream, or `start` (reserved for run boundaries).
- **decision:** what was chosen, tried, or reverted in one plain line.
- **why:** plain reason; if a principle drove it, state the concrete reason
  rather than only a jargon tag.
- **evidence:** concrete pointer proving it: commit SHA, `file:line`,
  command/log path in `.mydoc/<task>/output/`, or script path.
- **result:** observable outcome or predicate state: `tests green`,
  `reverted`, `VERIFIED`, `NOT VERIFIED`, `INCONCLUSIVE`, `blocked`, `open`.

## Logging a row

Use the helper script `scripts/log.sh` next to this file:

```bash
<path-to-z-log>/scripts/log.sh <logfile> <phase> <decision> <why> <evidence> <result>
```

The script stamps UTC `ts`, creates the parent directory and header row on
first write (using `>>`, never `>`), flattens tabs/newlines so cells stay
single-line, and quotes leading `=`, `+`, `-`, or `@` to prevent formula
injection if the TSV is opened in a spreadsheet.

Log real decision points and checkpoints, not every shell command: a design
fork chosen, a verification harness built, a unit completed with its check
result, a pivot or revert with its trigger, a blocker surfaced, or a gate
fixed. For loops (`hillclimb`, `autonomous-run`), log one row per iteration.
Apply `z-writing` to log text too.

### Run boundaries (`start` rows)

A run is one agent conversation. A session pickup, replacement agent, or new
conversation is a new run. When a run appends to an existing log, its first
row uses `phase=start` naming the `ts` range of prior rows it did not write
and identifying the new run in `evidence`. Read the tail of the log before
appending to see if another run wrote since your last turn. Use `phase=start`
for nothing else.

## Where it lives

Store the log outside tracked git patches:
- Default with `z-task-record`: `.mydoc/<task>/output/decisions.tsv` (or
  `outputs/decisions.tsv` in repositories whose convention is `outputs/`).
- Outside a `.mydoc/` task: a gitignored local path such as `decisions.tsv`.
Never include the TSV in an upstream kernel or QEMU patch.

## Append-only rule

Never edit or delete prior rows. If a decision turns out wrong, or an audit
finds an inaccurate row, append a new row that explicitly supersedes the
earlier `ts` with what actually happened and a verified pointer.

## End-of-run transcript audit

Before handing back a long or unattended run, audit your own rows against
the active workspace's session transcript (see
`../z-mode/references/harness.md`; never read transcripts from other
projects):

1. Check every row written by this run (from your `start` row or file start
   to the next run's `start` row).
2. Confirm every row maps to a real action or decision in the transcript.
3. Confirm every evidence pointer resolves on disk or in git and actually
   shows what the row claims.
4. Append any missing fork, pivot, or reverted attempt that shaped the work.
5. Append a superseding row for any inaccurate or unsupported row; never
   rewrite history.

## Independent review of the trail

When the harness offers subagents, spawn one fresh read-only subagent before
final handoff to review the TSV trail and the relevant transcript/diff. Ask
it to scan (not redo the work) for:
- decisions backed by weak, missing, or unresolved evidence,
- claimed verifications that were skipped or ran on the wrong surface,
- risky shortcuts, scope creep, or symptom-papering in hindsight,
- open gaps a reviewer skimming the summary would miss.

If subagents are unavailable, run the same adversarial pass yourself and
note that it was self-reviewed.

End the final reply for any logged run with an **Attention** section naming
whether an independent reviewer or self-review ran, followed by each flagged
row/moment (or `No flags`). Render locally with
`column -s$'\t' -t <logfile>`.

## Composing this skill

Playbooks (`figure-it-out`, `hillclimb`, `autonomous-run`) reference `z-log`
directly and let this skill own the schema, script, and audit rules.
