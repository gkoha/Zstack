---
name: z-reframe
description: Teach the expert terminology for what the user is building or debugging, borrow concepts from neighboring systems fields that solved the same shape of problem, and rewrite their description with those terms. Use for /z-reframe or $z-reframe.
disable-model-invocation: true
---

# Reframe

Teach the user the precise domain terms for what they are building or
investigating. Start from their actual code, files, and description rather
than a generic summary.

If their description could name more than one distinct problem, first list
the two or three problems it could be, each with the one term that names it
and the observable sign that distinguishes it from the others. Then teach
the vocabulary for the most likely one and state why you picked it.

1. Give 8 to 12 terms, ranked by how much each changes what gets built or
   how it gets debugged. For each term provide:
   - the term and its meaning in one plain sentence,
   - which part of the user's description or code it names,
   - one real subsystem, paper, spec, or codebase that uses it that way
     (cite `file:line`, spec section, or a verified link),
   - what using that term lets the user ask an agent for precisely.
2. Pick 2 or 3 neighboring fields that solved the same shape of problem
   under other names (for example: database recovery, lock-free concurrency,
   networking data planes, compiler IRs, distributed state machines). For
   each, state what carries over, where the analogy breaks, and which terms
   carry back cleanly.
3. Name what the user did not mention but needs to care about (for example:
   ordering, teardown races, backward compatibility, or failure recovery).
4. Rewrite the user's original description using the sharper vocabulary.

Verify every citation (open the file or confirm the reference uses the term
that way). Cut any citation you cannot verify. No padding.
