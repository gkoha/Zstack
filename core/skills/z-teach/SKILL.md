---
name: z-teach
description: Explain a kernel, QEMU, or virtualization subsystem or change plainly so a person truly understands it. Runs z-how and z-why and weaves them into a clear, paced explanation with incremental diagrams. Use for /z-teach, $z-teach, "teach me this", or "help me really understand X".
disable-model-invocation: true
---

# Teach

Explain what a thing is, how it works, and why it is built that way in one
plain account at the reader's pace. The goal is genuine understanding, not
producing a reference dump or changing code.

`z-teach` sits on top of `z-how` and `z-why`. Orient yourself in the code
first, then invoke `z-how` for mechanics and `z-why` for design rationale
and history (in parallel when subagents are available, see
`../z-mode/references/harness.md`). Combine what they find into one clear
account. Reword freely for teaching, with one exception: preserve `z-why`'s
epistemic labels (recorded in commit/list history vs inferred vs unknown),
because those hedges are findings, not style.

## Steps

1. **Choose the few load-bearing ideas.** Pick what the reader needs to walk
   away understanding based on why they are asking (about to change it,
   reviewing a series, debugging a crash, new to the subsystem) and what
   they already know from this conversation. Do not quiz them. Skip what
   they plainly know and put depth where their question sits.
2. **Delegate the digging to `z-how` and `z-why`.** Match scope to the
   question: run both for a subsystem or non-trivial change; one may suffice
   for a narrow question.
3. **Start with a plain definition, then build in layers.**
   - Name the thing and say what it is in general terms the way a senior
     engineer says it out loud, then tie it directly to this codebase
     ("in KVM x86, this is used to ...").
   - Walk through what actually happens during a real event (a guest MMIO
     write, a VFIO DMA map, a live migration switchover) rather than listing
     functions and struct fields. Listing symbols is reference, not
     teaching.
   - Start with the smallest complete picture (a few crisp sentences or a
     short first layer), then stop and let the user pull deeper. Never dump
     a wall of text.
   - Do not print meta-framing labels ("the one idea to hold onto", "key
     insight", "at its core", "TL;DR").
4. **Keep it a real conversation, not teaching theater.**
   - No quizzes, no "Pause here", no "the sentence to nail", and no
     announcing that something is "tricky" or "worth slowing down on". Just
     explain it clearly.
   - Offer concrete next layers at the end (for example, locking rules,
     error/teardown paths, or migration details) and follow the user's lead.
     When running one-shot with no interactive follow-up expected, deliver
     the full core cleanly and put optional deep dives at the end.
5. **Build diagrams incrementally.**
   - Open the exact `file:line` or diff when reading the real code lands the
     idea fastest.
   - For any flow or structure with three or more moving parts, never drop
     one giant all-at-once diagram. Draw a short series of Mermaid diagrams
     (2-3 small diagrams) where each redraws the previous one and adds one
     new piece (for example: first Guest → KVM exit; then add QEMU/VFIO
     handler; then add the return/interrupt path), so the reader watches the
     mechanism assemble. A single dense diagram is reference, not teaching.
   - A simple two-part point needs no diagram.

Apply `z-writing`: plain spoken prose, concrete actors and mechanisms, no AI
filler, no em dashes as connectors.
