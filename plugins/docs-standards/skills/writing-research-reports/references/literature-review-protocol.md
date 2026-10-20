# A literature review that can be checked

A review chapter written from memory and from abstracts is the part of a thesis most
often found wanting: a claim about "the state of the art" with one citation, numbers
quoted without their conditions, a bibliography entry nobody can resolve. The protocol
below makes the review reproducible by another person and usable twice: as the input to
the research design and as the review chapter of the report.

## 1. The protocol document

Write it before the first search and keep it in the repository. It fixes:

- **The two audiences.** The design (which representations, models, metrics and
  protocols are standard; which results must be beaten; what works on the target
  platform; where the gaps are) and the report (a review by topic with a verified
  bibliography, comparison tables, the statement of novelty relative to the closest
  prior work).
- **Thematic blocks.** One block per question of the study, each with its leading
  questions and its seed works for snowballing (forward and backward citation
  following). Typical blocks for a system study: the task formulation and metrics, the
  candidate methods per axis, the datasets, the platform and its constraints, the
  transfer from synthetic to real data, the representation and its cost.
- **Sources and the search log.** The databases and tools used, with the rule that a
  search not written to the log did not happen: query, date, database, number of hits,
  what was kept. Domestic or institutional literature gets its own quota per block when
  the department expects it.
- **Inclusion and exclusion rules.** Years, languages, venue types, the minimum
  reported detail (a result without its condition is not evidence), what to do with
  works read only from the abstract (marked as such, never quoted for a number).
- **The record format for each work** (below) and the output format for each block.
- **Verification of the bibliography.** Every entry is checked by a script against its
  identifier (DOI, arXiv number, ISBN): the identifier resolves, the title and the
  authors match. Entries that fail are fixed or removed. Works without an identifier are
  cited by the official repository URL with the access date.

## 2. The record of one work

For every work that is kept, one record with these fields, so that the comparison tables
are generated rather than composed:

| Field | Content |
|---|---|
| key | the bibliography key |
| question | which block question it answers |
| task and data | what was solved, on which data, what size, synthetic or measured |
| method | the method in one line, with the parameter count or cost when given |
| result | the number, its metric, its condition (noise band, input size, split), its hardware |
| protocol | how operating points were chosen, how many seeds, whether the split is by record |
| comparable to | which other records share enough conditions to be put in one table |
| limitation | what the work does not show (ranges not swept, assumptions, missing baseline) |
| read from | full text or abstract only |

## 3. The output of a block

Each block produces one file with:

1. The questions and the answer to each in a paragraph, with citations.
2. A comparison table of the works that share conditions (generated from the records),
   with a "comparable" column and the conditions in the header.
3. The baseline numbers that this study must reproduce or beat, each with its condition.
4. **Gaps and possible novelty**: what no work in the block does, what is done only under
   conditions that do not match the study's, what has never been compared under one
   protocol. This section is the raw material of the hypotheses.
5. The list of records.

## 4. The synthesis

Two documents are written from the blocks:

- **The review chapter** (`writing-research-reports`): organised by the study's
  questions, with the block tables, the reproduced point of reference, the gap table and
  the hypotheses table at the end.
- **The design brief**: the one-page input to the research design: which candidates
  survive the review and why, which were discarded on paper with their reason, which
  baselines and protocols are standard, which numbers to beat, and the open questions
  the design must settle. The design document argues from the brief and cites it.

## 5. Keeping it honest

- A number quoted from a work carries its conditions in the same sentence or the same
  table row. A number without conditions is replaced by the sentence "the work reports
  X under conditions it does not state".
- Works read only from the abstract are cited for what they propose, never for a result.
- When the review is updated (a new work, a corrected number), the block file, the
  review chapter and the design brief are all updated, and the change is dated: three
  documents that disagree are worse than none.
- The search log, the records and the verification script stay in the repository with
  the chapter, so that an examiner's "why is work Y missing" has an answer in the log.
