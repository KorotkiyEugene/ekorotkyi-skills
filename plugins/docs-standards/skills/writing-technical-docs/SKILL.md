---
name: writing-technical-docs
description: >-
  Standards and an audit checklist for producing high-quality technical documents:
  design docs, specs, architecture writeups, RFCs, API/reference docs, README/onboarding
  guides, test reports, or any explanatory prose that mixes formulas, numbers, diagrams,
  and reasoning. Use this skill whenever you are WRITING, REVIEWING, IMPROVING, or
  RESPONDING TO FEEDBACK ON such a document, even if the user does not say "documentation"
  and even for a "quick" edit. Trigger on requests like "write a design doc", "document
  this module/system", "explain how X works", "clean up this spec", "the docs are unclear",
  "add a section on Y", "make this readable for non-experts", or any complaint that a
  formula, number, term, or figure is undefined, unexplained, or unillustrated. Also use
  it for an EXPLANATION GIVEN IN CHAT: "explain what X is", "what does this formula
  mean", "how does R⁻¹ null the jammer", "I don't understand this step", or any
  follow-up question that shows the previous explanation left a term or step undefined.
---

# Writing Technical Documents

A good technical document lets a domain expert AND an engineer with only a basic
background follow it end to end, because every claim is *earned* by the reasoning
before it. These standards make that the default. Apply them whether you are drafting
from scratch, fixing an existing document, or explaining something in a chat reply: an
explanation in the terminal is a document the reader cannot scroll back through, and
every term it leaves undefined comes back as the next question.

## The one rule that matters most

**Fix systematically, never reactively.** When a reader (or reviewer) points out one
gap (an undefined symbol, an unexplained number, a missing figure), treat it as an
instance of a *class*. Audit the whole document for every instance of that class and
fix them all in one pass. Never patch only the single spot raised.

Why: piecemeal patching is the fastest way to exhaust a reader's goodwill. They point
at one undefined term, you fix that term, they find the next one, and it reads as
carelessness. One systematic pass costs you a few minutes and buys the reader a document
they can trust. If you catch yourself editing the exact thing that was flagged and
nothing else, stop: you are doing it wrong.

## If the document is not in English

Write in the document's language as an engineer writes in it. Never draft in English and
translate sentence by sentence: the English sentence skeletons survive the translation,
and a reader of the target language sees them before anything else. For a document in
Ukrainian, read `references/ukrainian-engineering-prose.md` before drafting or editing: it
carries the vocabulary the field uses, the calques that mark a text as translated, and the
sweep to run before delivery.

## The thirteen standards

Create a todo for each of these and check the whole document against it.

### 1. Derive, don't assert

Every formula decodes each of its symbols where it appears. Every number, result, or
threshold shows the reasoning or arithmetic that produces it. Every causal step says how
it follows from the one before.

- Bad: "the null depth is ~30 dB at the band edge."
- Good: "two unit signals differing in phase by δ leave a residual |1−e^{jδ}| ≈ δ;
  across the aperture δ runs to ±Δφ/2, so the null depth is 20·log10(Δφ/2) ≈ 30 dB."

A reader who cannot reconstruct *where a number came from* cannot check it, trust it, or
adapt it. "Trust me" is not an argument. When a step is a well-known result you are
citing rather than deriving, say so and point to the source; that is still showing the
provenance.

The derivation does not stop where the ideal model stops. Each result carries the
non-ideal terms the real system adds and what they cost: channel mismatch, calibration
error, finite word length, ADC dynamic range, finite sample support, latency. A null
depth derived for matched channels and quoted without the mismatch term is a number the
hardware will never show.

In a document about a system (its architecture, its deployment, its operation), the
provenance of a statement is a line of the source or a record, cited. A fact the writer
remembers, infers or finds plausible is cited to its line or left out, and a clause whose
cited page turns out not to carry it is dropped, not kept on trust. What was not run on a
real system (a manifest never applied, a console procedure never clicked through, a path
never exercised) is listed in one section, «Not verified», and presented as verified
nowhere else. Nothing is added that nobody asked for: a document gains no fact because the
writer found it interesting, since every added sentence is one more the reader must check.
A name quoted from a record, a script or a screen keeps its wording even where the
document's own term has changed, and the text says once what the quoted name stands for.

### 2. Define before first use

Introduce every term, symbol, unit, convention, coordinate frame, and named operation
*before* it appears, never as a forward reference to something explained later. Name
operations explicitly ("this is the scalar/dot product", "ᴴ is the conjugate
transpose", "E[·] is the expectation") rather than assuming the notation speaks for
itself.

Why: a forward reference forces the reader to hold an undefined token in their head and
read on faith, or to stop and search. Both break the flow you are trying to build.

A term is introduced by its full name, the name that says what the thing is of or for, and
a short form is used afterwards only if a reader who opens the document at that page, having
read nothing before, still knows what the word means: «operator» passes, «cycle», «final»,
«export» and «platform» do not and keep their full names («billing cycle», «audit export»,
«container platform») wherever they appear. A definition never defines the short form:
«One run of the pipeline over one tenant is a cycle» leaves the reader not knowing what
the cycle is a cycle of.

The same holds for tools, commands and products, and it holds per chapter. A command of the
framework, an abbreviation of the protocol, a resource kind of the platform is said to be
what it is at its first use in each chapter, in a sentence of its own («the framework's
command `build` compiles the application»), because a reader opens a chapter, not the
document. The term the writer finds too standard to define is the one the reader asks
about: a file format every engineer of the stack knows is still defined at its first
mention. A reference to a part of the document carries the part's number, set by the
toolchain, and is a link to it; the name alone tells the reader neither that it is a part
of this document nor where. And the vocabulary is the field's own, checked against the
field's references (its standards, its vendors' manuals), not a near-synonym the writer
coined.

Three classes of token are left undefined most often, because to the author they do not
look like terms at all:

- **The kind of product.** `R·v`, `wᴴx`, `x xᴴ`, `c·u` and `A·B` are five different
  operations (matrix × vector, scalar or dot product, outer product, number × vector,
  matrix × matrix). At the first product of each kind, say which one it is and what it
  produces (a vector, a number, a matrix), and write one of them out element by element.
  A reader who does not know whether `R·v` is a dot product has nothing to picture and
  stops there.
- **Informal labels.** "The sum combination", "the difference", "points along the first
  axis", "the direction of the vector", "the jammer subspace", "eigenmode". Each is a
  shorthand for a construction the author has in mind. Give the construction before the
  label: what a two-element vector is as an arrow, which axis is which, what "same
  direction" means for a complex vector, what "sum" is as a formula.
- **One letter, two meanings.** `e` as the selection vector and `e` in `e^{jφ}`; `N` as
  element count and as noise; `c` as the speed of light and as a coefficient. When the
  collision is unavoidable, name it where it happens ("this `e` is the selection vector,
  unrelated to Euler's `e`"); otherwise rename one of them.

Symbols that stand for sizes and counts (M antennas, N samples, L taps) get a notation
table in the front matter with four columns: the symbol, what it is, its value in the
scenario this document describes, and its name in the code (`nAnt`, `nSampleStaf`,
`nStafLine`). The code-name column is load-bearing: the reader who opens the source after
the document needs to know that `nAnt` is M, and the reader who opens the source first
needs the reverse.

The table is not the only decoding. Ten pages later the reader does not go back to it, so
every figure, block diagram and formula labelled with symbols is followed by one sentence
that spells each dimension out in words and numbers where it appears ("M × N_s is
8 antennas by 4000 samples, one short interval"), and every code fragment whose variables
stand for symbols is introduced with the mapping ("here `nAnt` is M and `nStafLine` is
L"). Figure labels obey the same rule as prose: an axis labelled only "N" is undecoded,
and the figure script is where that is fixed.

### 3. Illustrate concepts

Anything geometric, spatial, architectural, or conceptual gets a figure. Prefer figures
computed from real data or the real system over hand-drawn ones: a plot that comes out
of the actual model is evidence, not decoration. Draw vector quantities as labelled
vectors, and show the *constructs the formulas use*: directions, angles, projections,
data flow, the axes of a trade-off.

Why: a sentence describing a geometry makes the reader rebuild it in their head; a figure
hands it to them. When you assert a trade-off ("more taps cost more but buy deeper
nulls"), a measured sweep showing exactly where the knee is turns an opinion into a
result. If a claim is load-bearing, it deserves a picture.

### 4. Self-contained

The reader should not need another document to follow this one. Fold in the minimum
background instead of pointing away for it. Cross-references to companion documents are
fine as *optional further reading*, never as a load-bearing dependency the argument
relies on.

For a document that deploys or operates a system, the test is sharper: the operator must
be able to do it with the document alone, without opening the repository. Every command
is printed complete, every file a procedure needs (a schema, a manifest, a set of
variables) is printed or attached to the document, and every value is derived or cited
inside it. Check each step of each procedure with one question: could I run this without
the repository?

### 5. Two-audience readability

Write so a specialist and a competent generalist both get through it. This mostly means
spelling out the causal links (standard 1) in plain language and not skipping the step
that "everyone knows", because not everyone does, and the ones who do lose nothing from
one extra clause.

Each section about a stage, a block or a component opens with what it does and why it
exists, in plain words, before the first formula or line of code. The formula tells the
reader how the stage works; without the what and the why in front of it they have nowhere
to put it. The reader who already knows skips one sentence; the reader who does not is
lost without it. A chapter opens the same way: one paragraph on what it describes and for
whom, before its first section.

The test of a sentence is the reader who has not used the stack the text names. A tool, a
command, a product or a term is said to be what it is at its first use in the chapter
(standard 2), every pronoun and every «the other», «their», «those» has its noun in the
same sentence, and no noun phrase stands where a sentence should («the database the only
state» is a label nobody can read). A detail that a figure or a table beside the sentence
already shows is not repeated in prose, and a count that helps no reader is dropped rather
than decomposed: «the figure draws them as seven arrows» is not fixed by naming the seven,
it is fixed by deleting the seven. Legends and labels are sentences.

This is checked by a read, not by a checklist: every writer and checker who knows the stack
reads the shorthand as clear. Before anyone else sees a chapter, one fresh reader told to
know none of the frameworks, protocols and platforms the text names reads it with one
question, «can I understand this sentence on the first read, and do I need it?», and
lists every place that fails. The brief is `references/outsider-reader-brief.md`. Every
place on the list is rewritten as an instance of its class across the document.

### 6. Verify visuals before claiming done

Render every figure, diagram, and typeset PDF and actually look at it before you commit
or say it is finished. "It compiled" or "the code ran" is not "it is correct." Label
collisions, clipped edges, overflow, squashed aspect ratios, and plain wrong values are
common and only visible to the eye. If your environment can render an image, render it
and inspect it; if it cannot, say so explicitly rather than assuming success.

### 7. Show what you name

If the text names a concrete artefact, the artefact's content is in the document or in
a file shipped beside it: a key, a signature table, a packet template, a constant block,
a lookup table, a configuration blob. "The 60-word key schedule at 0x1301 verifies as
AES-256" without the 32 key bytes is a claim the reader cannot use or check; "the
signature comes from the table at 0x36D" without the eighteen values is the same. Print
short artefacts inline (a code block or a table with the source address of every
value); ship long or machine-readable ones (a 3072-entry table, a full disassembly, a
decoded image) as generated files in the document's tree, named in the text, produced
by the build so they cannot go stale. What cannot be shown (an absent table, encrypted
content) is stated as absent with the evidence that it is.

Why: the reader's first question about a named artefact is "what is in it", and a
document that answers "it exists and it checks out" has moved the reader's work to a
file they do not have. This is the class of omission most often caught by a reader and
missed by the author, because the author has seen the bytes.

### 8. Numbers and cross-references are generated, not typed

A table of values decoded from data, a count, a total, a "which of these checks pass"
row: generate it from the data with a kept script and include the output, so that the
document and the data cannot disagree and a rebuild after a correction updates every
number. A completeness result belongs beside it: for an inventory or a map, an
accounting that every element of the whole (every byte of the image, every file of the
tree) is inside some described part, with the leftover listed. "Zero unexplained bytes
of 12,828,369" is a stronger closing than "the regions above are what we found".

Cross-references by number are the same problem in miniature. Figures, tables and
equations are numbered by the toolchain; a section number typed by hand ("see §5.4")
is plain text and drifts silently when a heading is added or moved. Either reference
sections by label through the toolchain, or run `typesetting-documents-as-pdf`'s
`check_section_refs.py` against the built ToC and read its resolution list: it flags
references with no target and prints what every other one resolves to, which is how a
reference that points at the wrong section is found.

### 9. Corrections propagate across documents

When a later document, a verification against real data, or a reviewer corrects a
statement, the correction is applied to every document that carried it (the one rule
above, applied across documents), and the later document lists what it corrected so a
reader holding an older copy of the earlier one knows to distrust those lines. Leaving
the earlier document as it was leaves two documents that disagree.

### 10. Punctuation rhythm

Model-drafted prose uses the em dash as connective glue, twenty to thirty times more
often than the engineering literature does, and readers have learnt to read a dash-glued
text as machine output. That reading costs the document its credibility before a single
number is checked. The target in a finished document is therefore zero em dashes (—) and
en dashes (–) in prose, headings and titles, and the way to get there is not to delete
dashes but to write each connection with the mark that names the relationship:

- An aside or appositive sits in parentheses or between commas: "the phase step ψ
  (set by the arrival angle) plays the frequency."
- An explanation or consequence follows a colon: "That is invisible as a time
  shift: at 20 MHz one sample lasts 50 ns."
- Two related independent clauses get a semicolon or two separate sentences.
- A restatement is introduced by "i.e." or "that is".
- A term and its definition in a list are separated by a colon or a full stop, not a
  dash: "**M**: the number of antennas, 8."
- A numeric range is written with words ("from 13 to 15 s") or in the house style of
  the document series ("13...15 s", "13-15 s").

Two things that look like dashes are not. The minus sign (−, U+2212) in formulas, tables
and program output is mathematics and stays. A structural separator that the house style
of an existing document series already uses ("Appendix A — Title") is matched in that
series and introduced nowhere else. Before delivery, grep the source for `—` and `–`
(figure scripts included); what the grep returns is the list to rewrite.

### 11. The text addresses the reader, not the reviewer

A title or heading carries the name of the thing, never its status: no "(corrected
edition)", "updated", "v2, fixed", "final", "(as requested)". A label like that talks to
the person who asked for the change; the reader who opens the document a year later has no
such context and learns only that something was once wrong. The history of a document is
content, and content goes in the body: a section that says what changed between editions,
why, and with which numbers, where a reader can use it. The same holds for notes to the
reviewer left in the text ("TODO", "check this", "per your comment"): a document is
finished when nothing in it speaks to anyone but its reader.

The form is a professional's, and a reader who notices a machine wrote it stops trusting
it. The habits that give it away, each banned:

- **The document talking about itself.** The title page holds the title, the subtitle and
  the revision line (a commit, a build, a date), nothing else: no abstract, no «about this
  document», no conventions block, no list of readers. A convention the reader needs is
  one plain sentence where it is first needed. No sentence narrates the build, states the
  obvious («recovered from the repository»), justifies the document's own choices,
  apologises for layout, or counts the document's own pages and tables.
- **Restating.** A figure is not described three times, in a lead-in, a caption and the
  prose. The caption is one or two descriptive sentences; the prose says what the reader
  does with the figure. Provenance and verification are stated once, in the verification
  chapter, not on every caption.
- **Headings that are not names.** A heading is a noun phrase naming its subject, never a
  question, a «how to», a gerund or a sentence, and the sections of one chapter are of one
  kind and one level. A file name and a title promise chapters by those names: a document
  called «design and verification» has a chapter «Verification», and a revision may
  reorganise inside such a chapter but never renames or dissolves it. No section that is
  only a preamble, no parent with a single child, no flat pile where grouping is the
  information.
- **The heading tree moves after approval.** The tree is designed before the first
  sentence and approved by the owner, and from then on a reference, a reviewer or a
  rewrite never regroups, renames or reorders headings on its own: a change to the tree is
  proposed as a tree and made on the owner's word.

### 12. One example carries the whole argument

An explanation is one continuous build-up on a single concrete example, chosen small
enough to compute by hand and carried from the first definition to the last result. The
example is fixed before the first formula (two antennas, one jammer at power 100, noise
power 1), every operation is applied to it as soon as it is defined (`R·v` is written
out on that `R` and that `v`, with the numbers), and every later result is checked
against it (the eigenvalues are 201 and 1; the weights are `[1, −0.990]`; the null is
40 dB; the inverse computed directly agrees with the inverse computed by eigenmodes).
Then the general case is stated as what changes when the example grows.

Why: a derivation written only in symbols is a set of fragments, each of which the reader
must instantiate for themselves. The ones who cannot ask a follow-up question per
fragment ("what is the sum combination", "what does points along the first axis mean",
"what product is that"), and each answer opens the next gap. One example instantiated
once removes the whole chain of questions at the cost of a few lines of arithmetic. In a
chat reply this is the difference between one answer and six.

The example earns its place by being checkable: real numbers that add up, a figure
computed from them where the construction is geometric (standard 3), and the general
formula shown to reduce to the example's numbers.

In a document about a product or a service, the example is the thing's own case: its real
counts, its real screens, the position its specification describes, never an invented toy.
The rule is stated in words a colleague would say aloud, with the real numbers, and the
code identifiers and letter symbols stay in the citation, not in the sentence that states
the rule. A reader of such a document rejects «let N be the number of replicas and
Q = ⌊N/2⌋ + 1 the quorum (`quorum()` in the coordinator); example: a cluster of three
replicas has N = 3 and Q = 2» as prose nobody writes, and accepts «a write succeeds once
more than half of the replicas hold it: 2 of 3, 3 of 5». Where this register and a
standard disagree, the register wins, and the reviewer is told so.

### 13. Point by name or by anchor, never by an invented label

A reference into the document names the thing ("the conjugate-and-sum of §2.1", "the
difference combination `[1, −1]`") or uses an anchor the toolchain numbers (Fig. 7,
Table 2, Eq. 4, §3.2). It never uses a label the author made up and did not define:
"Reading 3", "item 3", "the second approach", "the earlier method", "case B". A label
that was never formally introduced points at nothing the reader can find.

The anchors work in both directions. Every figure, table and numbered equation is cited
from the body text at the place where the argument needs it ("Fig. 7 shows the two
towering eigenvalues this produces"), and the float sits on the page where it is cited
(Typst: `placement: auto` with `@fig-...` references; LaTeX: `[htbp]` with `\ref`). A
figure that no sentence points to is decoration the reader may never connect to the
argument; a figure three pages from its citation is one the reader has to hunt for.

In the source, a figure stands right after the paragraph that first cites it, or at the
end of the section that does, so that the typeset figure follows its citation on the same
page or the next and never crosses another section's heading. Its legend is part of the
figure script, and every legend entry and every label is a sentence («A white box is an
entry point.»), not a chain of colons and parentheses; a figure script that accepts a
legend entry which is not a sentence is corrected before the figure is. Every table has a
caption and is cited by its number; a part of the document is referred to by its name, and
the toolchain prints its number and makes the phrase a link.

## Sentences and register

The standards say what a document must contain. The sentences carry it, and a document
whose sentences a reader stumbles on fails before a single number is checked. The register
is the one of the system's own user-facing text, or of a colleague saying the fact aloud:
plain sentences, a rule stated once in words, a concrete example with the real counts, the
evidence last. These rules hold in every prose sentence, in every language:

- **One idea per sentence**, about 25 words, never more than 40. No semicolon in running
  prose: two clauses are two sentences (this outranks the semicolon that standard 10
  allows; a table cell may still list with semicolons). Subject, verb, object. No chain of
  three nouns. No «but» for «except». No «so», «thus», «therefore» unless the cause is in
  the same sentence. No filler, hedges, self-narration or colloquial shorthand.
- **The noun is in the sentence.** A pronoun stands next to the noun it replaces, or the
  noun is repeated. Every number carries its noun. A rule comes before its example, a
  definition before its use.
- **A value belongs to the thing**, never to the person who produced it: «the limits the
  operators set», never «the operators' limits». A button is named with its screen or its
  user, never as that person's property.
- **A list item is named once**, in words; a code value is not doubled beside the word
  («Pending, `pending`»): the mapping to the code's value is stated once before the list
  or shown in the figure.
- **The fact first, the evidence last.** Citations go into one «Sources:» line at the end
  of the paragraph, the document's own convention stated once, not into parentheses after
  every clause. A citation stays inline only where the sentence is about that line.
- **A code identifier appears in running text only when the sentence is about it**: a
  variable the operator sets, a route, a file to open. Never as a stand-in for an idea: not
  «as `ALLOWED_MOVES` allows» but «the service allows only the moves of its state table»;
  not «`inProd` is true when» but «the service treats itself as production when».
- **No letter symbols and no formulas** except where the document computes a number the
  reader needs, and then with the real counts.
- **A check in a runbook is a sentence** that says what to expect («Check that the health
  endpoint answers `{"ok":true}`»), never a fragment after a colon. A step is one
  imperative sentence, its command, its expected output.
- **Every sentence earns its place.** Before delivery, take each sentence out and ask
  whether the reader loses anything; a sentence that adds a definition to what the reader
  already understood, a count nobody uses, or a detail the figure beside it shows, goes.
  A derivation stays only where the reader must check or size something: a limit, a wait,
  a connection count.
- **A quoted string in another language carries its gloss** in the document's language,
  once, where it is first quoted: a screen text, a log line, a result a script prints.
- **The language is written, not translated**: a Ukrainian sentence that reads like its
  English original with the words swapped fails (`references/ukrainian-engineering-prose.md`).

The countable part is enforced by the build: `check_sentences.py` of
`typesetting-documents-as-pdf` fails a prose sentence of more than 40 words or with a
semicolon. The rest is enforced by the reads below.

## Three modes

### Writing a new document

1. Start from the reader's path, not the section list: what must they understand
   first, second, third? Introduce each concept the first time it is *needed*, in
   data-flow / cause-and-effect order.
2. The heading tree first, approved by the owner, then frozen (standard 11). A heading's
   body is exactly what its title names. The reference documents of the field (the
   professional documents of the same shape) inform what a section contains and how its
   prose reads; they never justify a change to the tree.
3. Draft with the thirteen standards on from the start; it is cheaper than retrofitting.
4. One author writes the whole text. When the writing is delegated to agents, one agent
   writes every part of the document, in the document's order, and no second writer works
   beside it. A text split among several agents writing in parallel has no integrity: each
   agent settles the names, the definitions and the register on its own, and the reader
   meets a different document in every chapter. Agents in parallel are for reading,
   checking and auditing a finished text, never for writing parts of one. A writer that
   must be replaced (context lost, usage limit reached) is replaced by one new writer,
   which reads the finished chapters as its register before writing a line.
5. The writer writes with the standards and the sentence rules open, every fact from the
   cited line it opens, and runs its own checklist on each chapter before anyone reads
   it: a term, tool or command said what it is at its first use in the chapter; every
   pronoun with its noun in the sentence; no noun phrase for a sentence; no detail the
   figure or table beside it shows; legends and labels as sentences; the chapter's opening
   paragraph; the sentence rules above.
6. Readers, on finished text only, in this order: the outsider read of each chapter
   (`references/outsider-reader-brief.md`, a fresh agent per chapter and per pass, three
   passes at most), each list rewritten by the one writer as classes across the whole
   document; then the audience read of the whole document
   (`references/audience-read-brief.md`, one fresh agent, once), whose five verdicts and
   residues go to the writer once; then the page gate of `typesetting-documents-as-pdf`,
   once, on the final build. The agent that runs the process reads a chapter in full
   itself before claiming anything about the document: agent verdicts are inputs, not
   the standard.
7. Verification is bounded, because an agent asked to find defects finds defects every
   time, and each fresh hunter applies a stricter bar than the last. Before the first
   verification agent starts, the stop condition and the budget (rounds, hours, tokens)
   are written down and told to the owner. The criterion for a finding is closed: «false
   against its source» or «an instance of the class the owner stated, in the owner's
   words». Two verification passes at most; a third needs the owner's word. A pass that
   finds nothing of a new kind ends the stage, and when the second pass finds a different
   kind of fault than the first, the agent stops and reports instead of iterating. «Until
   a check finds nothing» is not a stopping rule. When the owner asks how long, the
   answer is the state, the time spent against the estimate given, and the two ways: take
   the current green build now, or wait the stated time for the remaining steps. A sweep of a class begins with the class restated in one
   sentence and three to five old/new examples shown to the owner, and no sweep runs
   before the owner's yes: a wrong class swept perfectly is still wrong, and a class
   derived from one example («every count shows its parts» from one unparseable count) is
   usually wrong. No second loop beside the first: a layout audit does not run beside a
   content fix, since every layout fix moves pages and makes new breaks.
8. Deliver once: the whole document, with one verdict line per acceptance criterion from
   the audience read and the residue counts, the list of every change to text the owner
   had approved as old/new pairs, the facts the owner should know (what is not verified,
   what was decided without asking), and the layout residues the tools cannot close with
   their cause. Never a diff, never an acknowledgement, never a partial result shown as
   progress. Finished work is on the main branch when the message is sent, or the message
   says in its first line that it is not. A finding the owner makes afterwards is answered
   with the reason and the corrected text, never with an agreement or an apology, and
   becomes a rule of the skill only after the owner has approved the text that applies it.
9. Keep the record as the work runs. The first chapter the owner approves is the register
   for every later one: each later chapter is compared with it before a reader sees it,
   and the readers are asked whether it is the same hand. A handoff written before a
   context clear carries the owner's instructions verbatim with their times, and a plan
   derived from those words, never a process the agent invented (an approval stop per
   chapter, writers in parallel). Every time in a log comes from `date -u`, never from a
   guess. Rounds are committed as work-in-progress commits with one line each and
   squashed into one commit at delivery. An estimate names what it assumes, and when the
   class is not inventoried by a script, the time is said to be unknown rather than guessed.
10. Before presenting: run the audit below.

### Explaining something in a chat reply

1. Fix the running example first (standard 12): the smallest system that shows the
   mechanism, with numbers.
2. List the operations and labels the explanation will use, and define each before its
   first use (standard 2): what kind of product, what a vector drawn as an arrow is,
   what the informal name stands for. List the letters already taken by that point
   (`a` for the steering vector, `e` for the selection vector, `c` for the speed of
   light) and give every coefficient, index or count introduced later a letter that is
   not on the list. The reuse that slips through is a coefficient named after a vector
   defined three paragraphs earlier (`a₁, a₂` next to a steering vector `a`).
3. Build up once, continuously, from the reader's starting point to the result, applying
   every step to the example. Then state what generalizes.
4. Before sending, read the reply as the person who asked: every term that first appears
   inside a sentence that uses it is the next question they will have to ask. Define it
   there, not in the follow-up.

### Reviewing or improving an existing document (or acting on feedback)

1. Read the WHOLE document first. Do not start editing at the first problem.
2. Run the outsider read of standard 5 on each chapter first and keep its list apart: the
   elementary faults (a command used as if known, a pronoun without its noun, a label that
   is not a sentence) must not be buried under the audit's findings.
3. For each of the thirteen standards, scan the entire document and list every violation:
   every undefined symbol, every asserted number, every un-illustrated concept, every
   forward reference. This list is the work.
4. When the pass was triggered by the owner's finding, restate the class in one sentence
   and show three to five old/new examples before sweeping: the fix the owner means is
   often not the one the example suggests (an unparseable count is fixed by deleting the
   count, not by naming its parts), and a wrong class swept across the document costs
   days.
5. Fix the whole list in one pass (the "one rule" above), by one writer: the list is not
   divided among several agents, for the reason given under "Writing a new document".
   Rewrite paragraphs whole rather than patching words into them.
6. Re-render and inspect any figures/PDFs you touched (standard 6), and verify once with
   a closed criterion; findings of another kind go to the owner as a list, not into a
   second round.

## The audit checklist

Run this before calling a document done. Answer each with a concrete location, not "yes."

- [ ] **Symbols:** every symbol in every formula is decoded at its point of use.
- [ ] **Numbers:** every quoted number/threshold/result shows its derivation or cited source.
- [ ] **Causality:** each step states how it follows from the previous; no unexplained leaps.
- [ ] **Definitions:** every term/convention/operation is named and defined before first use; no forward references.
- [ ] **Operations and labels:** the first product of each kind says which product it is and what it yields; every informal label ("the sum", "the direction", "the jammer subspace") is preceded by the construction it names; no letter carries two meanings without the collision being named.
- [ ] **Hardware terms:** every derived result carries the non-ideal terms the real system adds (mismatch, calibration, word length, ADC range, sample support) or says why they are negligible.
- [ ] **Running example:** one concrete example is fixed before the first formula, every operation is applied to it with numbers, and every later result is checked against it.
- [ ] **Anchors:** every reference into the document names the thing or uses a toolchain-numbered anchor; no invented label; every figure, table and numbered equation is cited from the body where the argument needs it and sits on that page.
- [ ] **Notation:** every size symbol is in the notation table with its code name, and every diagram, formula and code fragment decodes its symbols again where it appears, figure labels included.
- [ ] **Stage openings:** every section about a stage or component says what it does and why before its first formula or code line.
- [ ] **Figures:** every geometric/conceptual claim that would land better as a picture has one; vectors drawn as vectors; load-bearing trade-offs shown with data.
- [ ] **Self-contained:** no argument depends on the reader opening another document.
- [ ] **Two audiences:** a non-specialist engineer could follow the causal chain.
- [ ] **Visuals verified:** every figure/PDF rendered and eyeballed; values and layout correct.
- [ ] **Artefacts shown:** every key, table, template, signature, constant block or blob the text names is printed or shipped as a generated file beside the document; absent ones are stated absent with evidence.
- [ ] **Generated numbers:** every decoded value, count and check result comes from a kept script the build runs; an inventory or map closes with an accounting of the whole with the leftover listed.
- [ ] **Section references:** every hand-typed §N.M was checked against the built ToC (`check_section_refs.py`) and its resolution list was read.
- [ ] **Propagated:** every correction made here was applied to the other documents that carried the statement, and listed.
- [ ] **Punctuation:** `grep -n '—\|–'` on the source and the figure scripts returns nothing but minus signs and a matched house-style separator; asides sit in parentheses or commas, explanations after colons.
- [ ] **Reader-facing:** no status label in any title or heading, no note to the reviewer in the text; edition history is a body section.
- [ ] **Language:** for a document in Ukrainian, the terminology sweep of `references/ukrainian-engineering-prose.md` was run on the prose and on the figure scripts.
- [ ] **Sentences:** every prose sentence is one idea of at most 40 words with no semicolon (`check_sentences.py` passes), every pronoun has its noun in its sentence, every number its noun, and no code identifier stands in for an idea.
- [ ] **Register:** rules are stated in words with the real counts, evidence in one «Sources:» line per paragraph, no toy example and no symbol prose in a document about a product.
- [ ] **Outsider read:** one reader told to know none of the frameworks, protocols and platforms the text names has read every chapter with one question, «can I understand this sentence on the first read, and do I need it?», and every place on its list is rewritten as a class.
- [ ] **Audience read:** one reader has read the whole built document once as the reader of the title page and given a verdict per criterion (structure, language, facts, form, completeness); every decisive residue is fixed, every minor one applied once.
- [ ] **Chapter openings and terms per chapter:** every chapter opens with what it describes and for whom; every tool, command and product is said what it is at its first use in each chapter.
- [ ] **Counts and details:** no count that helps no reader, no detail a figure or table beside the sentence shows, every legend entry and label a sentence.
- [ ] **Facts and sources:** in a document about a system, every statement comes from a cited line or record, what was not run is in «Not verified», and nothing was added that nobody asked for.
- [ ] **Form:** the title page is bare, headings are noun phrases of one kind per level, the chapters the title promises exist, the approved heading tree is unchanged, no sentence talks about the document itself.
- [ ] **Bounded:** the verification had a stop condition and a budget written down and told to the owner, at most two passes, a stop when a pass found nothing new or a different kind of fault, and the owner saw old/new examples before any sweep.
- [ ] **Systematic:** if this pass was triggered by one piece of feedback, the whole *class* of that issue was swept, not just the flagged instance.

## Red flags that you are drifting

- You are writing "ALWAYS"/"NEVER" instead of explaining *why*; reframe with the reason.
- You fixed exactly what was flagged and nothing adjacent: you skipped the systematic pass.
- You wrote "as shown above/below" pointing at something not yet (or never) shown.
- You committed a figure you did not open, or a PDF you did not page through.
- A number appears with no unit, no derivation, and no citation.
- You wrote "the key", "the table", "the template", "the signature" and the reader still cannot see a single byte of it.
- You typed a section number, and a heading was added or moved since.
- A decoded value in a table was typed from a terminal instead of written by the script that decoded it.
- An em dash in prose: the dash has become your default connective, and the reader will read the whole text as drafted by a machine.
- A heading ends in a parenthesis that describes the document's status rather than its content.
- A symbol appears in a figure, a formula or a code comment, and its last decoding is pages away.
- You wrote `R·v` and did not say what kind of product it is, or "the sum", "the direction", "the subspace", and did not build the thing first.
- You named a coefficient `a₁` and there is a vector `a` on the page.
- The whole explanation is in symbols; no number was ever computed.
- "Reading 3", "item 2", "the second approach": a reference to a label you invented.
- A figure that no sentence cites, or a citation whose figure is pages away.
- The reader's follow-up question is about a word in your previous answer.
- A Ukrainian sentence reads like its English original with the words swapped.
- A sentence of 50 words, or two clauses joined by a semicolon: two ideas, two sentences.
- A command, an abbreviation or a resource kind used in a chapter as if the reader knew it.
- «their», «the other three», «those»: a pronoun whose noun is in another sentence.
- A count in prose («seven arrows») that the reader can neither use nor check against the figure.
- A legend entry written «term: meaning (style)» instead of as a sentence.
- A title page with an abstract, a conventions block or a readers list; a sentence about the document's own build.
- A heading that asks a question or starts with «How»; a chapter the title promised that is no longer there.
- A fact you remember rather than read from the cited line; an untested procedure presented as verified.
- A sweep started from one example without the owner's yes, or a third verification round.
- A hunter's list growing with every reread: the criterion is open, and the loop has no end.
- A delivery that is a diff, a partial result, or an acknowledgement rather than the whole document with its verdicts.
