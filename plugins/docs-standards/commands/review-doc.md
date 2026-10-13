---
description: Audit a technical document against the writing-technical-docs standards and fix every issue in one pass
argument-hint: "[path to the document, or leave blank for the current/most-recent doc]"
---

Invoke the `writing-technical-docs` skill, then run its **audit checklist** against the
document at `$ARGUMENTS` (if empty, the document currently in focus or most recently
discussed). If the document is in Ukrainian, also read the skill's
`references/ukrainian-engineering-prose.md`; if it reports measured results (a test
report, a comparison, a results section), also invoke `reporting-experiments` and audit
against its quick-reference table.

Do a full review pass, not a spot check:

1. Read the whole document first.
2. For each of the standards, scan the entire document and list *every* violation with
   its location: undefined or undecoded symbols, asserted numbers, unexplained causal
   leaps, forward references, products whose kind is never named, informal labels used
   before the construction they stand for, one letter with two meanings, results
   quoted without their hardware terms, derivations with no running numeric example,
   references by invented label, figures or tables no sentence cites, un-illustrated
   concepts, external dependencies, stage sections that open with a formula instead of
   what and why, dashes used as connectives, status labels in headings, calques
   (Ukrainian), numbers without a run, mechanisms without a control, a missing "what
   this does not show".
3. Run the mechanical sweeps and quote their output: the dash grep over the source and
   the figure scripts, the terminology grep for Ukrainian, `check_section_refs.py`
   where the document is typeset.
4. Present the findings grouped by standard.
5. Fix the entire list in one pass (never patch only one instance of a class).
6. Re-render and visually inspect any figures or PDFs you changed.

Report what you found and what you fixed, organized by the checklist.
