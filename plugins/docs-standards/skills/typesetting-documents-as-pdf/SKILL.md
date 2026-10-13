---
name: typesetting-documents-as-pdf
description: >-
  How to turn a Markdown or text document into a typeset PDF that is actually correct:
  choosing the toolchain from what the document contains, and then finding the layout
  defects that a successful build hides. Use this skill whenever the user asks for a PDF,
  a printable or typeset version, a report to send or share, "оформи"/"format this
  nicely", or any conversion of prose into a paginated document. Also use it when a PDF
  already exists and something looks wrong: text running off the page, tables cut at the
  margin, broken diagrams, tofu boxes, wrong quotes, or headings stranded at a page foot.
  A build that exits zero tells you nothing about whether the pages are right, so reach
  for this even when the conversion "just worked".
---

# Typesetting documents as PDF

A PDF build almost always succeeds. That is the problem. The engine exits zero, a file
appears, and the defects (a table cut off at the trim, a diagram reflowed into nonsense,
every opening quote pointing the wrong way) are visible only to the eye and only if you
look. This skill is about the looking, and about the handful of conversion faults that
cause most of what you will find.

It assumes the `writing-technical-docs` standards already govern the *content*. This is
about the *artifact*.

## Choose the toolchain from the content, not from habit

No toolchain is the right default. Decide by asking what the document contains that could
break, then pick something that can protect it:

| The document contains | What it needs | Reasonable choice |
|---|---|---|
| Plain prose, simple tables | Almost nothing | Any HTML-to-PDF route, or pandoc's default |
| Unicode box-drawing or ASCII diagrams | Lines that must never reflow, and a font with the glyphs | LaTeX (pandoc + tectonic/xelatex) |
| Very wide tables | Real column-width control and page-breaking tables | LaTeX, `longtable` |
| Heavy math | Proper math setting | LaTeX |
| A house style to match | Whatever that style is written in | Match it |

State your reasoning when you choose. "I picked LaTeX because the document has box-drawing
figures that must not reflow and table rows up to 587 characters" is a decision the user
can disagree with. "I used pandoc" is not.

**Check what is installed before designing around a tool.** `pandoc`, `tectonic`,
`xelatex`, `weasyprint`, `wkhtmltopdf`, `typst`, `pdftoppm`, `pdftotext`: availability
varies a lot, and it often narrows the choice for you.

## Measure the source before you set the page

Three measurements decide page geometry, and all three are cheap. Guessing at them and
then discovering the consequence twenty pages in is the slow path.

```bash
python3 scripts/measure_source.py DOC.md
```

It reports the widest line inside code fences, the widest table row, and whether the
document uses box-drawing characters. Use them like this:

- **Widest fenced line** sets the monospace size. A monospace font's advance width is
  roughly 0.6 em, so *N* columns at size *s* occupy `N × 0.6 × s` points. Solve for the
  size that fits your text block, then take one step smaller for headroom. Write the
  arithmetic into the header as a comment; the next person to change the margins needs
  to know what the size was protecting.
- **Widest table row** tells you whether you need wrapping columns (almost always) and
  whether anything needs a landscape page.
- **Box-drawing characters** mean the monospace font must cover U+2500 to U+257F. Menlo,
  DejaVu Sans Mono and most terminal fonts do; many text fonts do not, and the failure
  mode is a page of tofu boxes or silently dropped glyphs.

## If a house style exists, adopt it

Before inventing a look, ask whether the project or the user already has a typeset report,
and read its source. Matching an existing style is nearly free and worth more than
anything you would invent: it makes the new document belong to the same body of work.

Look for a `.tex`, a template, or a previous PDF and its source. Take the fonts, the
margins, the paragraph treatment, the table style, the semantic colour macros. Note the
comments in it; house styles usually record why a choice was made, and those reasons
still apply.

## The five conversion faults worth knowing in advance

These are not exotic. In a single real 25-page conversion, the first four appeared; the
fifth turned up in the next document. Knowing them turns a long debugging session into
five targeted fixes.

### 1. Markdown tables become non-wrapping columns

pandoc's `gfm` reader carries no column-width information, because GFM pipe tables have
none to carry. The LaTeX writer therefore emits `@{}llll@{}`, and an `l` column never
wraps: a wide table runs straight off the paper, cutting words at the trim.

Fix with the bundled `scripts/tablewidths.lua`, which measures the longest cell per column
and assigns relative widths. Setting a width is what makes pandoc emit a wrapping `p{...}`
column instead of `l`.

It compresses the range with a square root rather than using raw proportions. A 3-character
column beside a 587-character one would otherwise get 0.5% of the text block, which is
narrower than a single word and produces one character per line. Square-rooting gives about
8% against 92%, which keeps both readable.

### 2. Inline code cannot break, so long spans overflow

pandoc renders `` `git clone --depth 1 https://example.com/x` `` as
`\texttt{git\ clone\ ...}` with **control spaces**, which are unbreakable. The whole span
becomes one rigid box, and if it is wider than the column, it runs off the page.

Fix with `scripts/codebreaks.lua`, which inserts `\allowbreak` at path and flag boundaries.
`\allowbreak` is a zero-width legal break point: the line may break there and **nothing is
added to the text**.

Do not reach for `\usepackage[htt]{hyphenat}` instead. It fixes the overflow by inserting a
visible hyphen, and in a document full of paths, flags and identifiers (`--depth`,
`naecon2023-fpga-re`, `segbits_opt`) a reader cannot tell an inserted hyphen from one that
belongs to the token. That trades a layout defect for a correctness defect, which is worse.

The length threshold matters and should be low. At a 24-character threshold, the span
`fuzzers/Makefile:105` (20 characters) stayed rigid, landed at a line end and protruded
43 pt. Anything past roughly a dozen characters can fail to fit the tail of a line.

### 3. Straight quotes all come out as closing quotes

Without pandoc's `smart` extension, a source written with ASCII `"` produces output where
*every* quote is a right double quotation mark. It is easy to miss when skimming and
obvious once counted: 159 closing quotes against 1 opening quote in one real document.

Add `+smart` to the reader. It pairs quotes correctly, converts apostrophes, and leaves
code spans alone, which is what you want: a straight quote inside a shell command should
stay straight.

### 4. Headings get stranded at the foot of a page

`\clubpenalty` prevents a lone first *line* of a paragraph being left behind. It does not
prevent a *heading* being left behind, because a heading followed by a table or a code
block is a different construct and TeX will happily break between them.

If you are using `titlesec`, its own option is the fix:

```latex
\usepackage[nobottomtitles*]{titlesec}
\renewcommand{\bottomtitlespace}{0.22\textheight}
```

`\Needspace` does **not** work here, whether you patch `\section` or put it in titlesec's
format argument; titlesec evaluates that argument inside the title box rather than in
vertical mode. Two rounds of increasing the reservation will change nothing and look like a
mystery. Reach for `nobottomtitles*` first.

Size `\bottomtitlespace` to cover a heading plus a meaningful opening chunk of whatever
follows it. A heading followed by a table needs room for the table's header row and its
first wrapped row.

### 5. Glyphs the font does not carry are dropped silently

A subscript zero in "C/N₀", a Greek letter in prose, an arrow, a superscript minus: when
the text font has no glyph for a character, the engine prints a warning ("could not
represent character"), exits zero, and leaves a blank where the glyph was. "C/N0" loses
its subscript and reads as a different quantity; a formula loses a symbol. Nothing on the
page says anything is missing.

Fix in two parts. First, a preparation script that rewrites the characters the fonts lack
before pandoc sees them: sub- and superscripts and Greek letters become math mode in
prose (`$_{0}$`, `$\lambda$`) and ASCII spellings inside code fences, where math is not
interpreted (`_0`, `lambda`); arrows become words. Second, a census: grep the engine log
for "could not represent" after every build and make the script exit non-zero if any
covered character survives, so the build stops instead of shipping blanks. The list of
characters is found by running the build once and reading the warnings; it is short (nine
in one document, one in the next) and specific to the font pair, so record it in the
script with the font that lacks each glyph.

The same fault has a second face inside math mode: a subscript in a non-Latin script
(`K_П`, a Cyrillic letter) is set in the math italic font, which has no such letter, and
is dropped from every one of its occurrences. Route it back to the text font with
`\text{}` (`K_{\text{П}}`), and let the preparation script do the substitution so the
source stays readable.

## Other things that will bite

- **Setting the size of plain verbatim.** `\fvset` and redefinitions of `Shaded` only apply
  when syntax highlighting is on. Code fences with no language tag produce plain
  `verbatim`, whose size hook is `\verbatim@font`:
  ```latex
  \makeatletter
  \renewcommand{\verbatim@font}{\footnotesize\ttfamily}
  \makeatother
  ```
- **`\maketitle` always emits a date**, falling back to `\today` when none is given, so the
  document silently re-dates itself on every rebuild. If the date should be the date of the
  work, set the title by hand in a `center` block.
- **Never break lines inside ASCII diagrams.** Whatever you do about long lines elsewhere,
  breaking is not available here: it destroys the picture. Make the font fit instead.
- **Comment lines inside code fences count as fenced lines.** A reproduction block whose
  comment runs to 120 characters overflows like any other fenced line; `measure_source.py`
  reports it. Wrap the comment onto a second line rather than shrinking the font.
- **Captions that carry the key need `+implicit_figures` and `[H]`.** Without
  `+implicit_figures` pandoc drops the alt text of a stand-alone image and every plot
  loses its caption silently. When captions explain the sentence directly above them,
  force placement with `\floatplacement{figure}{H}` (float.sty), so a float does not drift
  two pages from the number it illustrates.
- **A header word wider than its column collides with the next header.** The table-width
  filter sizes columns from the longest cell, and a long word in the header of a narrow
  column runs into its neighbour. Shorten the header word ("Мітка" for "Позначення")
  rather than widening the column; the body cells are what the widths are for.

## Verify: the part that is actually the skill

A build that exits zero has told you nothing. Run every check below; they take seconds and
each catches a different class.

```bash
python3 scripts/inspect_pdf.py OUT.pdf          # overflow, orphans, codepoint census
python3 scripts/contact_sheet.py OUT.pdf out/   # thumbnails for visual paging
```

**Overflow.** `pdftotext -bbox` gives the rightmost text position per page. Compare it to
where the text block ends. Distinguish two things that look alike in the numbers:
microtype's deliberate character protrusion is around 2 pt and is correct; anything beyond
a few points is a real defect. Also read the engine's `Overfull \hbox` warnings, which name
the source line.

**Codepoint census.** Two counts catch corruption that reads as normal:
- *Dashes.* If a document full of file paths shows en-dashes (U+2013) where hyphens
  (U+002D) belong, paths have been corrupted and are no longer copy-pasteable.
- *Quotes.* Opening (U+201C) and closing (U+201D) should roughly balance. A large
  imbalance means fault 3 above.

**Orphaned headings.** Check whether any page's last content line is a heading.

**Section references.** Figures, tables and equations are numbered by the toolchain;
a section reference typed as "§5.4" is plain text and drifts silently when a heading is
added or moved. `scripts/check_section_refs.py OUT.pdf src/*.md` extracts the numbered
headings from the built ToC, fails on every reference that has no target, and prints
what each remaining reference resolves to; read that list, because a reference that
resolves to the wrong heading is only visible there. Run it in the build script so the
build fails on a dangling reference. (On its first run over two finished documents it
found 30 wrong targets: an entire chapter's worth of references written against a
draft numbering.)

**Generated tables.** Values decoded from data go into the document through a script
whose output the build includes (a `{{include:generated/x.md}}` line expanded by the
build script), never by typing them; a rebuild after a correction then updates every
number. Keep the generated files in the tree so a reader can diff them.

**Orphan-check false positives.** The orphaned-heading check reads the last line of
each page and calls it a heading when it starts with a number. A table row whose first
cell is a bare chapter number, or a numbered list item, that happens to end a page
trips it. Change the wording (write "Chapter 4" rather than "4" in the cell, use a
bulleted list) rather than waiving the check: the check has no other way to see a real
stranded heading.

**Then look at the pages.** The checks above find what can be counted; they do not find a
figure that rendered as tofu, a table whose columns are technically inside the margin but
unreadably narrow, or a caption that has drifted from its figure. Build contact sheets and
page through them. For a long document this is one or two images, not fifty.

**After a heavy rewrite, page through the whole document, not the pages you edited.** A
rewritten section moves every page after it; a figure that fitted on page 41 is now split
across 41 and 42, and the pages you did not touch are where the new breaks landed.

**Re-render the images after every rebuild.** This is the easiest mistake in the whole
workflow: you fix something, rebuild the PDF, then inspect page images that are still from
the previous build and conclude the fix did not work, or worse, that it did. Delete the
old images as part of the rebuild, or compare timestamps before trusting what you see.

## Make it reproducible

Commit the build inputs next to the output: the header, any templates, the filters, and a
short `build.sh` that runs the exact command. A PDF whose build cannot be repeated is a
dead end the first time the source changes. `assets/build.sh.template` is a starting point.

Record in the header *why* each non-obvious setting is there: the size arithmetic, the
font requirement, the fault each filter is defending against. Those comments are the reason
the next change does not silently undo the fix.

## Bundled files

- `scripts/measure_source.py`: widest fenced line, widest table row, box-drawing check
- `scripts/tablewidths.lua`: pandoc filter giving tables proportional wrapping columns
- `scripts/codebreaks.lua`: pandoc filter making long inline code breakable
- `scripts/inspect_pdf.py`: overflow, orphaned headings, dash and quote census
- `scripts/check_section_refs.py`: hand-typed §N.M references checked against the built ToC, with a resolution list
- `scripts/contact_sheet.py`: page thumbnails for visual paging
- `assets/header.tex`: a commented LaTeX header carrying the fixes above
- `assets/build.sh.template`: the build command, ready to adapt
