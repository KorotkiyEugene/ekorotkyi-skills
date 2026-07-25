---
description: Audit a technical document against the writing-technical-docs standards and fix every issue in one pass
argument-hint: "[path to the document, or leave blank for the current/most-recent doc]"
---

Invoke the `writing-technical-docs` skill, then run its **audit checklist** against the
document at `$ARGUMENTS` (if empty, the document currently in focus or most recently
discussed).

Do a full review pass, not a spot check:

1. Read the whole document first.
2. For each of the six standards, scan the entire document and list *every* violation
   with its location — undefined symbols, asserted numbers, unexplained causal leaps,
   forward references, un-illustrated concepts, external dependencies.
3. Present the findings grouped by standard.
4. Fix the entire list in one pass (never patch only one instance of a class).
5. Re-render and visually inspect any figures or PDFs you changed.

Report what you found and what you fixed, organized by the checklist.
