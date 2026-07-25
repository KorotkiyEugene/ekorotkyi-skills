---
name: writing-technical-docs
description: >-
  Standards and an audit checklist for producing high-quality technical documents —
  design docs, specs, architecture writeups, RFCs, API/reference docs, README/onboarding
  guides, test reports, or any explanatory prose that mixes formulas, numbers, diagrams,
  and reasoning. Use this skill whenever you are WRITING, REVIEWING, IMPROVING, or
  RESPONDING TO FEEDBACK ON such a document — even if the user does not say "documentation"
  and even for a "quick" edit. Trigger on requests like "write a design doc", "document
  this module/system", "explain how X works", "clean up this spec", "the docs are unclear",
  "add a section on Y", "make this readable for non-experts", or any complaint that a
  formula, number, term, or figure is undefined, unexplained, or unillustrated.
---

# Writing Technical Documents

A good technical document lets a domain expert AND an engineer with only a basic
background follow it end to end, because every claim is *earned* by the reasoning
before it. These standards make that the default. Apply them whether you are drafting
from scratch or fixing an existing document.

## The one rule that matters most

**Fix systematically, never reactively.** When a reader (or reviewer) points out one
gap — an undefined symbol, an unexplained number, a missing figure — treat it as an
instance of a *class*. Audit the whole document for every instance of that class and
fix them all in one pass. Never patch only the single spot raised.

Why: piecemeal patching is the fastest way to exhaust a reader's goodwill. They point
at one undefined term, you fix that term, they find the next one, and it reads as
carelessness. One systematic pass costs you a few minutes and buys the reader a document
they can trust. If you catch yourself editing the exact thing that was flagged and
nothing else, stop — you are doing it wrong.

## The six standards

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
citing rather than deriving, say so and point to the source — that is still showing the
provenance.

### 2. Define before first use

Introduce every term, symbol, unit, convention, coordinate frame, and named operation
*before* it appears — never as a forward reference to something explained later. Name
operations explicitly ("this is the scalar/dot product", "ᴴ is the conjugate
transpose", "E[·] is the expectation") rather than assuming the notation speaks for
itself.

Why: a forward reference forces the reader to hold an undefined token in their head and
read on faith, or to stop and search. Both break the flow you are trying to build.

### 3. Illustrate concepts

Anything geometric, spatial, architectural, or conceptual gets a figure. Prefer figures
computed from real data or the real system over hand-drawn ones — a plot that comes out
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

### 5. Two-audience readability

Write so a specialist and a competent generalist both get through it. This mostly means
spelling out the causal links (standard 1) in plain language and not skipping the step
that "everyone knows" — because not everyone does, and the ones who do lose nothing from
one extra clause.

### 6. Verify visuals before claiming done

Render every figure, diagram, and typeset PDF and actually look at it before you commit
or say it is finished. "It compiled" or "the code ran" is not "it is correct." Label
collisions, clipped edges, overflow, squashed aspect ratios, and plain wrong values are
common and only visible to the eye. If your environment can render an image, render it
and inspect it; if it cannot, say so explicitly rather than assuming success.

## Two modes

### Writing a new document

1. Start from the reader's path, not the section list: what must they understand
   first, second, third? Introduce each concept the first time it is *needed*, in
   data-flow / cause-and-effect order.
2. Draft with the six standards on from the start — it is cheaper than retrofitting.
3. Before presenting: run the audit below.

### Reviewing or improving an existing document (or acting on feedback)

1. Read the WHOLE document first. Do not start editing at the first problem.
2. For each of the six standards, scan the entire document and list every violation —
   every undefined symbol, every asserted number, every un-illustrated concept, every
   forward reference. This list is the work.
3. Fix the whole list in one pass (the "one rule" above).
4. Re-render and inspect any figures/PDFs you touched (standard 6).

## The audit checklist

Run this before calling a document done. Answer each with a concrete location, not "yes."

- [ ] **Symbols:** every symbol in every formula is decoded at its point of use.
- [ ] **Numbers:** every quoted number/threshold/result shows its derivation or cited source.
- [ ] **Causality:** each step states how it follows from the previous — no unexplained leaps.
- [ ] **Definitions:** every term/convention/operation is named and defined before first use; no forward references.
- [ ] **Figures:** every geometric/conceptual claim that would land better as a picture has one; vectors drawn as vectors; load-bearing trade-offs shown with data.
- [ ] **Self-contained:** no argument depends on the reader opening another document.
- [ ] **Two audiences:** a non-specialist engineer could follow the causal chain.
- [ ] **Visuals verified:** every figure/PDF rendered and eyeballed; values and layout correct.
- [ ] **Systematic:** if this pass was triggered by one piece of feedback, the whole *class* of that issue was swept, not just the flagged instance.

## Red flags that you are drifting

- You are writing "ALWAYS"/"NEVER" instead of explaining *why* — reframe with the reason.
- You fixed exactly what was flagged and nothing adjacent — you skipped the systematic pass.
- You wrote "as shown above/below" pointing at something not yet (or never) shown.
- You committed a figure you did not open, or a PDF you did not page through.
- A number appears with no unit, no derivation, and no citation.
