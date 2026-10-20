---
name: reporting-experiments
description: >-
  Use when writing up measured results: a comparative test of two or more implementations,
  a verification campaign, a benchmark, an A/B experiment, a parameter sweep, a test or
  validation report ("звіт про випробування"), or the results section of any document
  that quotes numbers produced by running a model, a script, a simulator or hardware.
  Also use when a fix made during a campaign changes numbers that are already written
  down, or when a reader asks "where does this number come from", "what does this test
  not show", or "why is X better than Y here".
---

# Reporting experiments

A measured number without the run that produced it is an opinion with decimals. A report
of measurements is a chain from the setup to each conclusion in which every link is an
artefact the reader can open: a record, a script, a results table, a control run. This
skill gives the report its shape and the rules that keep the chain unbroken. It assumes
`writing-technical-docs` governs the prose (derive, define, illustrate, no dashes, no
status labels) and `typesetting-documents-as-pdf` governs the PDF.

## The shape of the report

Produce these parts, in this order. Each exists because its absence was what a reader
asked about first.

**1. Conditions, with every level derived.** The scene (what is measured, with what
instrument, at what sampling, with what quantisation), then a table of the records: a
label, what was changed to make it, the resulting level with the arithmetic that gives it
("multiplier 1072 instead of 10: 24.7 + 20·lg(1072/10) = 45.1 dB"), and the file name.
State what is identical across all records (the same signal, the same noise realisation,
the same seed) so the reader knows what the differences cannot come from.

**2. The measurement ceiling, beside the numbers it caps.** Every setup has a limit that
is not a property of the thing under test: the quantisation noise of the recording, the
resolution of a counter, the length of the record. Derive it ("int16 jammer file, rms
1439 LSB: its own quantisation noise lies 10·lg(1439² · 6) = 71 dB down, so no canceller
can measure deeper") and say which table entries sit on it. A reader who sees 70.5, 70.8
and 70.8 dB in three rows otherwise concludes the three algorithms are equal.

**3. Metrics, as formulas with a script name.** Each metric gets its definition with every
symbol decoded, the script that computes it, and a calibration on two extreme cases the
reader can believe (a clean record gives 9 of 9 detected; a record with no signal gives 0
of 9). A metric that has not been calibrated on a case with a known answer is an
instrument that has never been zeroed.

**4. The configurations under test, as a table.** One row per configuration: label, which
model, which construction of the thing that differs, the settings. Followed by the
sentence that says what was held equal (the same reference antenna, the same tap count,
the same sample size where the algorithm allows it). The labels in this table are the
labels in every results table.

**5. Results: the table, then what is seen and why.** Each results table is followed by
paragraphs, one per finding, each opening with the finding in bold. For every difference
the paragraph does one of two things: it names the mechanism and the control run that
isolates it, or it says in plain words that this report does not explain it, and lists
the candidates as candidates. "Remaining 1.1 dB between 23.1 and 21.0 this report does
not explain" is a result; a mechanism invented to fill the gap is a defect that a reader
will find.

**6. What the test does not show.** A section, not a sentence: the assumptions of the
setup that the real system will violate (an ideal array with matched channels, weak
reflections only, hot start with a clean first second), the ranges not swept, the cases
not generated. A claim that holds "up to the highest level tested" is written as a tested
bound, never as a limit of the algorithm.

**7. Conclusions, numbered, each with its number.** Each conclusion restates the figure
that supports it and the condition it was measured under. A conclusion the reader cannot
match to a table row is an opinion.

**8. Reproduction.** A runnable block: the commands in order, the time each takes, the
environment (tool version, platform), where the results land, and the statement that the
seeds are fixed so the numbers repeat bit for bit. If a step needs something generated
first, the block says so.

## Controls, not stories

A mechanism is claimed only after a run that changes one thing and shows the effect
move. Before writing "the median falls because the weights are rebuilt only every 5 ms",
run the 1 ms case; if the median does not move, the sentence is false, and the report
says instead that update period and sample size were tried and do not explain it. List
the controls that were run, including the ones that ruled something out: a reader who
has the same hypothesis needs to know it was tested.

## Every number names its run

- Every number in prose is in a table, and every table is a results file (`.csv`) next
  to the script that wrote it, both in the tree. Per-run results are stored (one file per
  run, regenerable, ignored by version control if large) so a figure or a table can be
  rebuilt without repeating the runs.
- Runs and drawings are separate scripts: a data script executes the runs and stores
  compact results; a figure script reads them and writes the figures. Figure labels are
  in the document's language and come from the figure script.
- When the pipeline under test changes mid-campaign (a defect fixed, a setting
  corrected), every run made before the change is invalid: clear any resume cache that
  would reuse old results, re-run everything, then sweep every document for every number
  the tables changed (`writing-technical-docs`, standard 9). The pre-change numbers
  survive in one place only, the defect ledger, as the measured cost of the defect. The
  same holds for a comment: a correction to a comment in the file the thing under test
  is built from changes its provenance, and the records are made again.
- A record carries the commit of the thing it measured and the start and end time of its
  run, and timed runs go one after the other, never side by side, so that none is timed
  under another's load. The build that reads the records refuses a record whose commit
  is not the one being built, so that the text cannot quote a number measured on other
  code. A number that moved between two runs for a reason nobody established is reported
  with the words «the cause was not established», never with a cause invented to fill
  the gap.

## When the campaign finds defects in the thing under test

Keep a defect ledger in the README of the thing under test, one row per defect: an
identifier, the file and place, what was wrong, the measured cost (before and after, on
identical records), the fix. Mark each fix in the code with the identifier (`FIX(S12)`),
and keep the original behaviour selectable where it is cheap (a solver mode, a flag), so
the cost is measured on the same records rather than remembered. Documents cite the
identifiers; the ledger carries the detail once.

## Quick reference

| Part | Required element |
|---|---|
| Conditions | Record table with derived levels and file names; what is identical across records |
| Ceiling | Derived; the entries that sit on it named |
| Metrics | Formula, symbols decoded, script name, calibration on two known cases |
| Configurations | Table with the labels used everywhere; what was held equal |
| Results | Table, then one bold finding per paragraph; mechanism with its control, or "not explained" with candidates |
| Not shown | A section: violated assumptions, ranges not swept; bounds phrased as bounds |
| Conclusions | Numbered, each with its number and condition |
| Reproduction | Runnable block, times, environment, result locations, seeds |
| Provenance | Every number in a `.csv` beside its script; runs and figures in separate scripts |
| Mid-campaign change | Caches cleared, everything re-run, every document swept |
| Defects | Ledger row with measured cost; `FIX(ID)` in code; original behaviour selectable |

## Common mistakes

| What happens | What to do instead |
|---|---|
| "The mechanism is obvious, no need for a control" | Run the control. The obvious mechanism for a 10 dB median loss (stale weights) was wrong; the real one (a level normalisation) was found by a control that changed one thing. |
| "The fix changed the numbers only slightly" | Re-run and sweep anyway. A median that moved from 20.9 to 23.1 dB survived in three documents until the sweep. |
| The ceiling is mentioned once, in the conditions | Name it again beside every table entry that sits on it. |
| A conclusion says "the limit is 65 dB" | 65 dB was the highest level generated. Write "no limit reached up to 65 dB, the highest the recording format allows". |
| Numbers typed into prose from a terminal | Numbers come from the results file; after a re-run, grep the document for each changed value. |
