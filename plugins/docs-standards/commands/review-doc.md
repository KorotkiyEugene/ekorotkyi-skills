---
description: Audit a technical document against the writing-technical-docs standards and fix every issue in one pass
argument-hint: "[path to the document, or leave blank for the current/most-recent doc]"
---

Invoke the `writing-technical-docs` skill, then run its **audit checklist** against the
document at `$ARGUMENTS` (if empty, the document currently in focus or most recently
discussed). If the document is in Ukrainian, also read the skill's
`references/ukrainian-engineering-prose.md`; if it reports measured results (a test
report, a comparison, a results section), also invoke `reporting-experiments` and audit
against its quick-reference table; if it describes a system someone else built, also
invoke `documenting-existing-designs`.

Do a full review pass, not a spot check, and a bounded one:

1. Read the whole document first.
2. Run the outsider read of standard 5 on each chapter first: one fresh reader per
   chapter, told to know none of the frameworks, protocols and platforms the text names,
   with the brief `references/outsider-reader-brief.md` and one question, «can I
   understand this sentence on the first read, and do I need it?». Keep its list apart
   from the audit's findings, so that the elementary faults (a command used as if known,
   a pronoun without its noun, a label that is not a sentence, a count nobody can use)
   are not buried under them.
3. For each of the standards, scan the entire document and list *every* violation with
   its location: undefined or undecoded symbols, asserted numbers, unexplained causal
   leaps, forward references, products whose kind is never named, informal labels used
   before the construction they stand for, one letter with two meanings, results
   quoted without their hardware terms, derivations with no running numeric example,
   references by invented label, figures or tables no sentence cites, un-illustrated
   concepts, external dependencies, stage sections that open with a formula instead of
   what and why, dashes used as connectives, status labels in headings, calques
   (Ukrainian), numbers without a run, mechanisms without a control, a missing "what
   this does not show"; and, by the sentence rules, sentences over 40 words or with a
   semicolon, pronouns without their noun, code identifiers standing in for ideas, a
   title page or a heading that talks about the document instead of its subject.
4. Run the mechanical sweeps and quote their output: the dash grep over the source and
   the figure scripts, the terminology grep for Ukrainian, `check_sentences.py`,
   `check_section_refs.py` and `check_word_gaps.py` where the document is typeset.
5. Present the findings grouped by standard, the outsider read's list first. When the
   review was triggered by the owner's finding, restate the class it belongs to in one
   sentence with three to five old/new examples, and sweep only after the owner's yes.
6. Fix the entire list in one pass by one writer (never patch only one instance of a
   class; rewrite paragraphs whole rather than patching words into them).
7. Re-render and visually inspect any figures or PDFs you changed, then verify once with
   a closed criterion («false against its source», or the owner's class in the owner's
   words). Findings of another kind go to the owner as a list, not into another round;
   a second verification pass is the last.
8. For a finished document, end with the audience read: one fresh reader reads the whole
   built document once as the reader of its title page, with the brief
   `references/audience-read-brief.md`, and gives a verdict per criterion (structure,
   language, facts, form, completeness) with every residue marked decisive or minor.

Report what you found and what you fixed, organized by the checklist, with the audience
read's five verdict lines when it ran.
