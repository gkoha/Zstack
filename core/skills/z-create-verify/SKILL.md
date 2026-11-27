---
name: z-create-verify
description: Generate or maintain a project-local verification skill (verify-<project>) and feature map that launches, health-checks, drives, proves, and cleans up a kernel, QEMU, vGPU, or virtualization project on the real target. Use for /z-create-verify, $z-create-verify, "create a verify skill", or "audit the verify skill".
disable-model-invocation: true
---

# Create or maintain a project verification skill

Every non-trivial repository needs a scripted, repeatable way to drive the
real target (a booted test VM, QEMU binary, kernel selftest, vGPU/VFIO
stack, CLI, or daemon) and prove behavior end to end. This skill generates
and maintains that as a project-local skill written for the next agent
reading it cold, mid-task.

Decide first whether you are **creating** a new verification skill or
**maintaining** an existing one.

## Where the generated skill lives

Check `../z-mode/references/harness.md` and the repository layout:
- Put project-local skills in `.agents/skills/verify-<project>/`. Codex,
  Gemini CLI, and Antigravity read that directory. Add
  `.claude/skills/verify-<project>/` only if the repository uses Claude Code
  (keep the two synchronized or symlinked).
- Never include local verification skills in upstream Linux or QEMU patches
  (list in `.git/info/exclude` if untracked in an upstream tree).

---

## Mode 1: Create a verification skill

### 1. Interview the repo, not the user

Answer from the codebase, build directories, and `.mydoc/` records first.
Ask the user only for hardware, images, or credentials you cannot observe:

- **Surface:** what does a user or guest actually touch? A QEMU VM + QMP,
  a guest kernel booted via `-kernel`, a VFIO/vGPU device, a CLI, or a
  service? Name the primary surface and secondary ones.
- **Run / Launch:** how does it build and start locally? Check configured
  out-of-tree build dirs (`meson-info/`, `O=<dir>`), Makefile targets,
  documented scripts, required guest images, kernel cmdline, and ports/sockets.
- **Drive:** how can an agent drive it programmatically? Prefer existing
  harnesses first (`meson test`, qtest, KVM/VFIO selftests, kunit, QMP
  scripts, expect/tmux/serial console, SSH). Only then design a minimal
  wrapper script.
- **Observe:** what evidence proves behavior? Guest console output, `dmesg`
  (checking for oops/lockdep/KASAN), QMP JSON responses, tracepoint counts,
  exit codes, migration state, or perf counters.
- **Isolate:** can two instances run side by side (separate QMP sockets,
  ports, tap/user net, overlay disk images, temp dirs)? If hardware (such as
  a physical GPU/VF) forces single-tenant access, state that explicitly so a
  later agent refuses to double-drive shared hardware.

If the tree does not build or start as-is, fix or report the exact blocker
first. A verification skill written against a broken base teaches wrong
steps.

### 2. Generate `verify-<project>/SKILL.md`

Include valid YAML frontmatter (`name: verify-<project>` and a concrete
`description` naming the project, surface, and trigger) and these sections,
all grounded in verified repo commands (zero placeholders):

- **Launch:** exact build + start command and how to know the target is
  *usable*, not merely alive (for example: guest login prompt or QMP
  `query-status` returning `running`, not merely `qemu-system-*` PID
  existing). Include teardown and overlay/snapshot usage so VM images are
  never mutated destructively.
- **Doctor:** one read-only health check answering "is this instance worth
  driving?" (right binary/kernel commit built, process alive, expected
  socket/port owned by us, guest responsive, no prior oops/KASAN splat).
  Agents run Doctor first whenever anything looks off.
- **Drive:** concrete harness recipes using stable handles (QMP commands,
  device IDs, guest commands, selftest flags) rather than fragile sleeps or
  hardcoded assumptions.
- **Evidence:** what to capture and where it goes (for example,
  `.mydoc/<task>/output/`). State proof standards: exercise the real path,
  capture both the action and the resulting state/side effects, check guest
  and host logs for hidden warnings/splats, and inspect what any dry-run
  mode actually skips instead of trusting its name.
- **Cleanup:** tear down only PIDs, sockets, and temp overlays started by
  this run (never `killall qemu-system-x86_64`). Cleanup removes processes
  and scratch state, never the captured proof artifacts.
- **Helpers:** any helper script shipped under `scripts/` must be executable
  and documented by exact invocation in `SKILL.md`.

### 3. Seed the feature map

Create `verify-<project>/features/README.md` plus one file per core
user/guest-facing feature (start with the top 3-5 critical flows, following
`references/feature-map-example.md`). Each file has four H2 sections:
- `## Sub-features`
- `## How to reach it (user/guest POV)`
- `## Driving it with <harness>`
- `## Gotchas`

If a precondition or hardware setup is missing, record the failure and the
reason in `Gotchas`; never weaken the verification journey to make it pass.

### 4. Prove the generated skill end to end before handoff

Follow the generated skill cold once: Launch → Doctor → Drive ONE mapped
feature → Capture evidence → Cleanup. After Cleanup, confirm the proof
artifact still exists on disk and no orphan process/socket remains. Run
Cleanup after failed attempts too. A verification skill that was never
executed is a draft, not a deliverable. If proven in a stand-in environment
(such as TCG or `samples/vfio-mdev` instead of real GPU hardware), list
every gap that remains unverified on real hardware.

---

## Mode 2: Maintain an existing verification skill

Feature maps rot as code evolves. Run this pass to audit and repair an
existing `verify-<project>/` skill.

### Outcomes

Declare one outcome explicitly:
- **clean:** every feature got source and live coverage; no edits needed.
- **changed:** proven doc, harness, or feature-map fixes applied inside the
  verification skill directory.
- **blocked:** coverage could not finish or a fix could not be verified;
  state the exact blocker.

### Edit scope

Edit only files inside the verification skill's directory (`SKILL.md`,
`features/`, its own helper scripts). Never edit product code during a
maintenance pass: if behavior changed, either fix doc drift in the map or
report a product regression clearly without papering over it.

### Steps

0. **Locate target.** Find the project-local `verify-*/` skill. If multiple
   exist, ask which one; if none exists, switch to Mode 1.
1. **Index hygiene.** Compare `features/README.md` with files in
   `features/`. Fix missing, extra, duplicate, or dead entries.
2. **Source wave.** Launch one read-only subagent per feature file in
   parallel (or inspect serially if no subagents exist). Each checks current
   source code and returns: feature summary, `file:line` entry points,
   likely doc/harness drift (or none), and one concise live verification
   recipe.
3. **Reconcile.** Merge overlapping recipes into as few live boots/sessions
   as practical. Spot-check cited drift. Sweep recent `git log` churn for
   new user/guest-facing features missing from the map (require concrete
   source paths).
4. **Live pass (required even when source looks clean).** Drive every mapped
   feature at least once following the skill's own Launch/Doctor/Cleanup
   rules. Hold three invariants:
   - Run Doctor before the first drive and after any unexpected error or
     fresh session.
   - Never hide a product regression by editing the map to match broken
     behavior.
   - Always run Cleanup and confirm evidence survives teardown.
5. **Apply verified fixes** to `SKILL.md`, `features/`, or helper scripts,
   re-run any modified recipe to prove it works, and report the outcome,
   features covered, fixes made, and any product regressions found.
