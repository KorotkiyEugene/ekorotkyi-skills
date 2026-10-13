---
name: documenting-existing-designs
description: >-
  Use when producing a report, design summary, block diagram, module inventory, or a
  "where is X / how does X work / what is missing" answer about an EXISTING codebase or
  hardware design that you did not write: reverse-engineering an inherited FPGA/RTL
  project, a legacy service, a vendor drop, a partial checkout, or a tree that mixes
  several revisions of the same modules. Trigger on "document this design", "draw the
  block diagram of", "what does this module do", "which files are missing", "write up
  the architecture of this repo", "review notes on this RTL", or any analysis where
  some sources are absent, duplicated, or of uncertain revision.
---

# Documenting existing designs

An analysis report about code you did not write is only as trustworthy as its weakest
claim, and the reader cannot tell the weak claims from the strong ones unless you mark
them. The report has a fixed shape. Produce these parts, in this order.

## 1. Inventory, generated, before any prose

Enumerate what the build *lists* against what *exists*, with a script, and keep the
script. For an RTL project: every file the `.qsf`/`.xpr`/filelist names, every module
the top level instantiates, and for each one every path in the tree that defines it
(present in the target directory, present only in another directory, absent). For a
software project: every import or dependency against what resolves.

Counts made by eye drift between sections of the same document ("ten missing" in the
summary, thirteen names in the appendix). A generated inventory is the one source of
those numbers; the report quotes it.

Absence is a finding, not a gap in your work. State what is not in the tree and the
search that proves it: a census of file extensions, a grep for every mechanism that could
carry the thing (`$readmem`, `.mif`, `initial` blocks, `INIT_FILE`), the build list
entries with no file. "There is no firmware in this checkout" with the census beside it
is a stronger result than a guess at what the firmware does.

## 2. A provenance tier on every claim

Define the tiers once, in the conventions section, then carry a tier on **every block in
every figure, every row of every table, and every stated number**:

| Tier | Meaning |
|---|---|
| A | Read from the source being documented. Authoritative. |
| B | Read from a same-named file elsewhere (another directory, revision, or project). Port count and parameter list cross-checked against the instantiation. Presented as a reference implementation, not as this design's source. |
| C | Source absent. Everything shown is derived from the instantiation: port order, which nets are driven versus read, parameter values, names. No internal structure is invented. |

The tier column is a REQUIRED field of the module table, and the tier mark is a
REQUIRED element of every block. A cell that says "correlation-matrix estimator" for a
tier-C module says so from the *name*; write "name suggests correlation over the 8 I/Q
inputs (C)" and nothing more specific.

Two cases that come up every time:

- If a module's own source is present but a child it instantiates is absent, the module
  stays tier A for what was read from it, and the absent children are named in its row.
- If the top level contains inline logic that is not an instance (a read multiplexer, an
  export of a bus window, a status-word concatenation), it is drawn as its own block and
  tiered A, and the inventory reports instances and inline blocks as separate counts.

A tier-B claim is provisional until checked. When the cross-check fails (the same-named
file has four data inputs and the instantiation passes eight), demote it to C and say
that you did. When a better source turns up later, promote it and say that too.

## 3. Numbers traced to a line

Every width, address, frequency, latency, and count in the report is followed by the
arithmetic or the `file:line` that produces it, in the style of `writing-technical-docs`.
Two checks that catch most errors in this kind of report:

- **Units follow the addressing.** A slot of 2048 addresses on a 32-bit word-addressed bus
  is 8 KB, not 2 KB. Say "2048 words × 32 bit = 8 KB".
- **Derived clocks show the parameter that pins them.** "101 MHz because `clockFreq1 =
  101000000` is passed to the UART divider at `InterfaceBlockA.v:4`", not "101 MHz".

## 4. Diagrams derived from the netlist and audited

Draw connectivity from the instantiation list, never from memory of a previous drawing.
Generate the diagram with a script that carries the connection table and **fails** when a
drawn block has no wires or a required link is missing. Then check the *content* against
the source (every instance appears exactly once; every module-to-module link is a wire),
and only then check the *rendering*.

Tier-C blocks are drawn as black boxes with their inferred pins, visually distinct from
read blocks (dashed border), and the legend explains every visual encoding used. The full
rules, including what a block diagram of a hardware design must and must not show, are in
`references/block-diagrams.md`; read it before drawing. If the drawing tool cannot express
a rule (Mermaid has no junction-dot trunk and no split fill), the legend states which rule
was substituted and how, so the reader knows the deviation is the tool's, not the design's.

When the detailed diagram will not survive reduction to a report page, ship it as a
separate standalone sheet with an auto-fit page, give the report a coarser overview drawn
for A4, and generate both from the same style file and the same source facts.

## 5. Anomalies flagged, not corrected or explained away

A missing comma in a port list, an empty concatenation element, a bus select with no
slave, an output driven by nothing: record each with its `file:line` and what it implies.
Do not silently fix it in the description of the design, and do not attach a story
("evidently hand-edited after the last build") that the evidence does not contain. The
finding is the observation plus its consequence; the cause is the reader's to establish.

## 6. A verification statement

The report ends by saying what was mechanically checked: the inventory script that
produced the counts, the diagram audit that passed, which numbers were traced to a
source line, and what was rendered and looked at. If something could not be verified in
the environment (no renderer, no simulator), the statement says so rather than implying
it was.

## 7. Verification against real artefacts, when they exist

When a real artefact of the design is available (a flash dump, a captured stream, a
production image, a log), the report verifies its structural claims against it and says
what that verification did and did not cover. Four rules, all learnt the hard way:

- **Decode with a kept script; account for the whole.** The decoder that reads the
  artefact is shipped beside the report and its output is what the report's tables
  include. It ends with a coverage accounting: every element of the artefact (every
  programmed byte of the image) either lies inside a decoded structure or is listed as
  unexplained. A structure that "matches" while a third of the bytes are unattributed
  has not been verified.
- **Recompute, do not compare.** Checksums, signatures, cross-field arithmetic (a
  counter that must advance by the previous record's length, a threshold that the
  recorded maxima must be consistent with) are recomputed by the decoder and reported
  as pass/fail rows, not read off by eye.
- **Scope the variant.** If the artefact comes from a different variant of the design
  (another channel count, another device, another build), the report states which
  claims rest on code the artefact proves is shared (formats that match exactly) and
  which rest on the design that produced it (bit maps, calibrations, channel-dependent
  sizes), with a per-quantity table saying which transfer and which do not. Design-
  dependent fields from the other variant are quoted as raw values, not interpreted
  with this design's bit map.
- **When two readings disagree, decode the bytes yourself.** Two sub-analyses gave
  opposite mappings for a pair of templates; both were wrong in part. The decision was
  made by decoding the template bytes and printing the check, and the print is in the
  report. A disagreement between analyses is never settled by picking one.

The artefacts themselves live in the report's tree: a copy of the image or file the
report describes (with a build-time guard that it still equals the original), the full
generated listing or decode, and the scripts. A reader must be able to reproduce every
number without the analyst's scratch directory. Corrections the artefact forces on an
earlier report are applied there and listed here (`writing-technical-docs`, standard 9).

## Quick reference

| Report part | Required element |
|---|---|
| Inventory | Generated by a kept script; present / elsewhere / absent per item |
| Conventions | Tier table defined before first tier mark |
| Module table | Tier column on every row |
| Figures | Tier mark on every block; C blocks are dashed black boxes; legend covers every encoding |
| Numbers | Arithmetic or `file:line` beside each |
| Anomalies | `file:line` + consequence; no invented cause |
| Closing | Verification statement naming the checks run and the ones not possible |
| Artefacts | Decoder shipped; coverage accounting with the leftover listed; checks recomputed as pass/fail rows; variant scope stated per quantity; source artefact copied into the tree with a drift guard |

**REQUIRED BACKGROUND:** `writing-technical-docs` governs the prose (derive, define,
illustrate, self-contained, verify visuals). `typesetting-documents-as-pdf` governs the
PDF artifact. This skill governs what an analysis of someone else's design must contain.
