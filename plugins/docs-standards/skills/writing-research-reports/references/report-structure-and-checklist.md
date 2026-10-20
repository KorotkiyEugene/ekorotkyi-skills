# Report structure, formatting rules and the pre-submission checklist

Distilled from the public thesis-writing guides for technical fields (the Tampere
University guide for technical fields in particular) and from the department templates
that examiners actually check against. Where a department template differs, the template
wins on structure and this file wins on content.

## 1. Parts of a thesis or an R&D report

| Part | Requirements |
|---|---|
| Title | Short, precise, with the key terms, no abbreviations, no trade names. An adjective ("efficient", "fast", "lightweight") commits the work to measuring it. |
| Abstract | One page. Aim, materials, methods, numeric results, conclusions, recommendations. Understandable to a non-specialist. No citations, figures or tables. Nothing absent from the body. Written last. |
| Abbreviations | Every abbreviation used in the body, expanded; Cyrillic abbreviations after their first definition in the text, Latin ones only for established designations. |
| Introduction | Two to four pages: relevance with the gap in numbers, aim, tasks, object and subject, methods, novelty, practical value, structure. No method details, no results. The first figure introduces the system with the contribution highlighted. |
| Review and problem statement | Reader is an engineer, not a specialist in the topic: every concept defined. The problem and the criteria for judging a solution stated explicitly. Similar works end in a comparison table. Closes with the gap table and the hypotheses table. |
| Methods and materials | Alternatives and the reasons for the choice. Data of unquestionable provenance. Enough detail to repeat without the author. Novelty relative to prior work made explicit where the method is described. |
| Results and discussion | Partly self-contained. Concise and exact: figures for trends, tables for numbers. Sources of error, deviations from expectation, reliability. Comparison with prior work: similarities, differences, limitations, the recommended approach. No advertising words. |
| Conclusions | The most read chapter after the abstract: two to four pages. Main results with key numbers and conditions, their meaning, limitations, recommendations for use, further work, an honest assessment of the work's quality. A summary table: aim, methods, results, strengths, weaknesses, time spent, cost. |
| Sources | Only those cited in the text. One style. Full bibliographic data. Access date for online sources. |
| Appendices | Each referenced from the text, each with a heading and a short description. Full measurement tables, long listings, instructions for reproduction. |

Reference lengths from the guides: 55 to 75 pages of body text for a master's thesis.
Conclusions, abstract and introduction are written last, in that order, so that they
agree.

## 2. Properties of the research the text must show

1. **Objectivity, validity, reliability.** Results are not fitted to expectations; the
   metric measures what is claimed; another researcher repeats the experiment from the
   description and gets the same numbers.
2. **A hypothesis that can be refuted.** The work tests concrete claims that could turn
   out false, with the refuting outcome written before the run.
3. **Alternative explanations and counter-evidence.** For every key result: what else
   could have produced it (leakage between splits, unequal record lengths, an operating
   point chosen on the test set) and how that was excluded.
4. **Controlled comparisons.** One variable at a time; the same data, splits, protocol
   and hyperparameter budget for every method compared.
5. **Quantitative results with conditions.** Every "better", "faster", "lighter" has a
   number, a unit and the conditions (condition band, split, input size, hardware, power
   mode). An average over conditions without the breakdown is not a result.
6. **Honesty.** No invented, selected or silenced results; failed experiments and
   losses are reported like successes; every borrowed idea, figure, table and line of
   code is cited.
7. **Reproducibility.** Tool versions, data generation parameters, seeds, splits, model
   configurations, run commands; evaluation code in an open repository; full sweeps in
   the appendices.

## 3. Style of the text

1. From the general to the specific: the reader is told what comes, shown it, and given
   the summary. Every chapter opens with what is known and closes with a summary. A
   chapter never opens with a figure, a table or a list.
2. Short sentences, impersonal register, no first person. Established terminology,
   neutral language, no jargon, no advertising words. New terms and foreign words marked
   at first use, abbreviations expanded at first use.
3. Argumentation: conclusions from premises, no generalisation from a small sample, no
   causal claim without evidence, no conflicting claims. Refuting one claim does not
   prove its opposite.
4. Lists: a justified order, parallel structure, short items, numbered when referenced,
   tied to the surrounding text.
5. Numbers as digits, units abbreviated, a non-breaking space between number and unit, a
   leading zero in fractions, digit groups separated. Numbers put on a scale: the price,
   not "cheap".

## 4. Figures, tables, formulas, code

1. Every figure and table is referenced from the text and discussed with its numbers,
   so the reader knows what to notice. Continuous numbering, separate for figures and
   tables.
2. Figures from analysis tools are edited before publication: clutter removed, axes
   named with units, scale from zero or marked logarithmic, line labels beside lines,
   font not smaller than the body's small size, black text, readable in grey scale, in
   the document's language. Figures are computed by kept scripts from the actual models
   and data, so a corrected number regenerates the figure. The caption says what to
   notice.
3. Tables: caption above, rules only at top, bottom and under the header, numbers
   aligned on the decimal mark, the best value in a column marked, rows ordered by
   meaning rather than alphabet, common powers of ten moved to the header, no table
   split across pages.
4. Formulas numbered when referenced; variables defined at first use; one symbol, one
   meaning; variables in italics, functions and operators upright, logarithms with their
   base; a sentence never starts with a symbol; a formula is part of a sentence with its
   punctuation.
5. Code: monospace; up to ten lines as a formula, up to a page as a figure ("Listing N"),
   longer in an appendix; keywords marked, lines numbered, commented, and its action
   described in the text. Identifiers in the prose in italics or monospace; a sentence
   never starts with an identifier.

## 5. Citations

1. One style for the whole work; numeric styles (IEEE or the local standard) in order of
   first appearance are the norm in technical departments. All authors in the
   bibliography, first author and "et al." in the text.
2. The citation stands as close as possible to the borrowed claim, before the full stop.
   A borrowed paragraph is recognisable as borrowed. Borrowed figures and tables are
   cited in the caption; modified ones are marked "adapted from".
3. Primary sources over secondary; secondary citation marked explicitly. No encyclopaedia
   or forum entries. Peer-reviewed publications over preprints; preprints marked.
4. Typical errors that must not survive: "better, faster, cheaper" without a citation and
   a number; one source where several are needed; an undefined relation to prior work;
   mixed formats of names and venues; sources without citations in the text; errors of
   the sources repeated.
5. The bibliography is built from a database whose every entry is verified by a script
   (the identifier resolves, title and authors match); the text cites by key through a
   key map; entries without a citation do not reach the list.

## 6. The writing process

1. Write from the start, not at the end: notes, decisions and results are recorded in
   the repository when they appear (handoffs, design documents, experiment protocols,
   run logs) and the text grows out of them.
2. First a table of contents with the expected length of each chapter and the placement
   of the main tables and figures, then the chapters in any order, then the
   introduction and conclusions.
3. One to three pages of good text or figures per day is the realistic rate; a few days
   of reserve for a fresh-eyed reading; versions under version control.
4. Supervisor feedback at every stage, applied in the next version rather than
   accumulated.

## 7. The pre-submission checklist

- [ ] The hypotheses and tasks in the introduction match what the results test and the
      conclusions count.
- [ ] Every quantitative claim has a number, a unit, conditions and a source (own
      experiment or citation).
- [ ] Every comparison is controlled: one variable, the same budget, data and protocol.
- [ ] Operating points were chosen on validation; the test split was used once.
- [ ] Results are given by condition band and by split, not only as an average.
- [ ] Losses after quantisation or transfer and failed variants are reported.
- [ ] For every key result the alternative explanations were considered.
- [ ] The methods suffice to repeat the work: code, commands, versions, seeds, full
      tables in appendices.
- [ ] Every figure, table, formula and appendix is referenced from the text and
      discussed.
- [ ] Figures, tables and formulas follow section 4.
- [ ] Terminology consistent and swept; abbreviations expanded; punctuation per the
      project rules (no dashes as connectives).
- [ ] One citation style; every source cited; every bibliography entry verified.
- [ ] The abstract is one page, with numbers, without citations, consistent with the
      conclusions.
- [ ] Structure and layout follow the department template, including the assignment
      sheet, the schedule and the appendices.
