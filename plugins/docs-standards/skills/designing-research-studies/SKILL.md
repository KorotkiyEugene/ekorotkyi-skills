---
name: designing-research-studies
description: >-
  Use when an R&D study, a thesis project, a method comparison or a measurement campaign
  is being planned and nothing has been run yet: writing a research design document,
  turning a topic into hypotheses that can lose, choosing candidate methods and the rules
  that will discard them, fixing the evaluation protocol (splits, seeds, condition bands,
  operating points, baselines), budgeting runs and deciding what gets cut when time runs
  out, listing risks with their rollbacks, and keeping a ledger of decisions while the
  study runs. Trigger on "дизайн дослідження", "сформулюй гіпотези", "план експериментів",
  "протокол оцінювання", "які експерименти потрібні", "як чесно порівняти методи",
  "research design", "what experiments should we run", "which baseline", "what would
  falsify this", "is this comparison controlled", and on any request to start building a
  model or a benchmark before the questions above have written answers.
---

# Designing research studies

An R&D study is the set of decisions made before the first run: what would count as a
loss, which methods compete, on what data, by which numbers, and what gets cut when the
deadline comes. A study that starts with a run and decides these things on the way ends
with results nobody can defend, because every decision was made with the numbers already
in view. This skill gives the design document its shape and the rules that make each
decision checkable later. It assumes `writing-technical-docs` governs the prose and that
`reporting-experiments` and `writing-research-reports` will consume what the design fixes.

## The design document

Write it before anything is built, keep it under version control, and treat it as the
authority that the plan and the report argue from. The sections, in order (a skeleton
with the questions each section answers is in
[references/research-design-template.md](references/research-design-template.md)):

1. **Intent and motivation.** The problem in one paragraph, the gap in numbers (what the
   closest known work achieves and what the application needs), and why the study is
   possible now (a platform, a dataset, a tool).
2. **Goals, non-goals, anti-goals.** Goals are the deliverables. Non-goals are the things a
   reader might expect and will not get, stated so nobody argues about them later.
   Anti-goals are outcomes that would make the study a failure even if every goal is met
   (a result that depends on an operating point chosen on the test set, a model that
   cannot run on the target platform).
3. **Constraints.** Platform, operator set, memory, licences of the data, compute budget,
   deadline. Each with its value and its source, because a constraint without a source
   is renegotiated every week.
4. **Problem statement and hypotheses** (below).
5. **Method space and sieve rules** (below).
6. **Checkpoints** (below).
7. **Experiment protocol** (below).
8. **System architecture**, when the study delivers a system: the pipeline from input to
   decision with the stage boundaries that experiments may move.
9. **Stages and deliverables.** A table: stage, content, the artefact that proves it is
   done. The order in which nothing is cut comes first (see budget).
10. **Risks and rollbacks.** A table: risk, the sign that it has happened, the fallback
    that still yields a complete study.
11. **Left to the implementer.** Hyperparameters, grids, library choices, file layouts:
    named here so the implementer knows what is theirs to decide.
12. **Questions to the author.** The facts only the owner of the work knows (deadline,
    whether a live demonstration is required, publication requirements, access to
    sources). Listed, not guessed.

## Hypotheses that can lose

A hypothesis is a sentence that a specific measured outcome would refute. Write each as
two parts:

> **H.** *claim with a number, a condition and a cost:* method A loses no more than 2
> percentage points of accuracy to method B in the operating range from −10 dB upward
> while costing at least 50 times fewer operations.
> **Refuted by:** a gain of B over A above 2 points in the −10...0 dB bands on the named
> dataset with the same network, over three seeds.

Rules, each with its reason:

- **One variable per hypothesis.** A claim about "the new representation and the new
  head" cannot be refuted by any single result, so it is two hypotheses.
- **The threshold is in the sentence** (points, times, percent), with the condition band
  and the dataset. "Better" is not refutable; "no worse than 2 points at −10 dB" is.
- **The refutation criterion is written before the run and not moved after.** If a
  criterion must change (a dataset turned out unavailable, a cost model was wrong), the
  change is dated, reasoned, and reported in the results as a change, so the reader sees
  that the bar moved and why.
- **A hypothesis whose refutation nobody would want to publish is not a hypothesis.** "The
  network beats a threshold tuned on a different noise level" always wins; "the network
  beats a classical detector calibrated per band at equal false-alarm rate" can lose, and
  that is what makes the win worth something.
- **Name the alternative explanations now.** For each hypothesis, list what else could
  produce the expected result (leakage between splits, unequal record lengths, a
  threshold chosen on the test set) and the control that excludes it. The report will
  need this paragraph; writing it after the result is in is how mechanisms get invented.

## The method space and the sieve

List the candidates per axis (representation, model family, output head, training
scheme, deployment variant...) in a table with three columns: the axis, what was
discarded at review time and the documented reason, and the candidates that enter the
experiments. A candidate discarded on paper gets a reason a reader can check (an
operator the target platform does not support, a published gain smaller than its cost,
a result that only its authors reproduced), not a taste.

Then write the sieve: numbered criteria with thresholds, any one of which discards a
candidate. A typical set:

1. **Incompatible with the target platform**: the graph does not compile into the
   accelerator's supported set, or the block does not fit in the remaining logic.
2. **No gain for the cost**: the difference to the cheaper method is under 1 point over
   three seeds (inside the confidence interval) while the cost (operations, parameters,
   latency on the target) is 1.5 times higher or more.
3. **Failure at the edges**: a loss above 2 points in any condition band after
   quantisation and retraining, or a loss on real records that a small labelled set does
   not recover.
4. **Irreproducible**: the result does not repeat over three seeds, or depends on an
   operating point chosen on the test set.
5. **Hardware blocks**: a latency or energy gain under 30 % against the processor
   implementation at equal accuracy.

The thresholds are the design author's decision; they may be revised in the plan, but
only before the experiment they govern starts, never after. And the sentence that keeps
the sieve honest: **a candidate discarded at any checkpoint stays in the report with its
result and its reason. The sieve is a result.**

## Checkpoints

A table with one row per gate the candidates pass through: where it runs, what it
checks, what decision it produces. The usual ladder:

| Checkpoint | Where | What is checked | Decision |
|---|---|---|---|
| Review | desk | discard by documented properties | candidate list fixed |
| Smoke | laptop, tiny subsets | the pipeline runs end to end for every candidate, tests pass | admitted to full runs |
| Accuracy | full data, full precision, ≥ 3 seeds | sieve criteria 2 to 4 by condition band | discard by accuracy and cost |
| Deployment | target toolchain | compilation, quantisation loss per output and per band | discard by criteria 1 and 3 |
| Target hardware | the board | latency, throughput, energy, resources, processor against logic | discard hardware variants by criterion 5 |
| Real data | full data and board | transfer to measured records, cross-dataset transfer | final methods fixed |

The smoke checkpoint earns its row: a candidate that cannot run on tiny subsets on a
laptop will not run on the full data either, and finding that out costs minutes instead
of a GPU day. Give the smoke mode a flag in the code (a configuration overlay with one
epoch and tiny subsets, and a results directory that the overlay empties, so smoke
numbers can never land among results) so it cannot drift from the real pipeline.

## A protocol that survives the reviewer

Fix these in the design, because each one is a question the first reader asks:

- **Splits by record or session, never by sample.** Samples from one recording on both
  sides of a split measure memorisation. When the official split of a dataset violates
  this, report both the official split (for comparison with the literature) and a clean
  one (for the claim).
- **Condition bands.** Results are reported per band of the condition that drives
  difficulty (signal-to-noise ratio, distance, speed, record length), with the band
  edges fixed here. An average over the whole range is not a result: it hides the edge
  where the method fails.
- **Seeds.** Decisive comparisons use at least three seeds and report mean and sample
  standard deviation. A coarse sieve may use one seed on reduced data, and the report
  marks every number that came from it.
- **Operating points on validation.** Every threshold (confidence, false-alarm rate,
  detector multiplier) is chosen by a sweep on the validation split and frozen before
  the test split is touched. The test split is used once.
- **One evaluation code for every method**, including the classical baselines. A
  baseline evaluated by its own script with its own matching rule is a different
  experiment.
- **Baselines calibrated once, at the same false-alarm rate.** A classical method with
  a threshold tuned for the easy regime "loses" in the hard regime by construction; the
  design says how the baseline is calibrated per band and compared on a shared operating
  curve.
- **One variable at a time.** When two methods differ in two things, add the
  configuration that differs in one.
- **The point of reference.** Name the closest published work that can be reproduced on
  your own setup, reproduce its numbers first (a checkpoint), and derive the gap with
  arithmetic (from its latency per fragment to the sample rate it can sustain, from its
  accuracy per band to the band where it fails). The gap in numbers is the motivation;
  the reproduction is what makes the later comparison fair.
- **Tables generated from run logs**, never typed; full sweeps in appendices; every run
  stores its configuration, seed, device and metrics beside the numbers.

## Budget and the order of cuts

State the compute (one GPU of a given memory, a laptop for smoke runs, a board for
measurements) and the rules it imposes: coarse sieve with one seed on reduced data,
three seeds only for survivors and decisive comparisons, mixed precision and gradient
accumulation by default. Then write two lists:

- **What is cut first** when the deadline comes (the deepest transfer levels, the
  representations beyond the baseline, the extra head variants), in order.
- **The path that is never cut**, which by itself yields a complete, defensible study
  (for a system study: environment, data, one detector, quantisation, the board). A
  study designed without this path ends with five half-results.

## While the study runs: rulings and handoffs

Design documents meet reality in the first week. Every deviation made during execution
is recorded where the report will find it, as a ruling:

> Ruling: *what was decided* — *why* — *what it costs if wrong*.

Deviating without a ruling is a decision made in secret, and the methods chapter will
later describe a protocol that was not followed. At the end of each working session,
write a handoff: what is done (with the artefacts), findings that change later stages,
open questions to the author (one per message, because a list of six gets one answer),
the rulings so far, and the next steps. The report's methods and results chapters are
assembled from these files; memory does not survive a month, a machine change or a
change of hands.

## Quick reference

| Element | Required form |
|---|---|
| Hypothesis | claim with number, condition band, dataset, cost; "refuted by" with an observable outcome; alternatives and their controls |
| Method space | axis × (discarded with reason, candidates) table |
| Sieve | numbered criteria with thresholds, fixed before the experiment they govern; discards reported as results |
| Checkpoints | where, what, decision; a smoke checkpoint on tiny subsets with a code flag |
| Splits | by record or session; official split reported beside the clean one when they differ |
| Bands and seeds | per-band tables; ≥ 3 seeds for decisive comparisons, mean ± std; one-seed sieve results marked |
| Operating points | swept on validation, frozen, test used once |
| Baselines | same evaluation code, calibrated per band, compared on a shared operating curve |
| Point of reference | reproduced before improved; the gap derived with arithmetic |
| Budget | compute stated; order of cuts; the never-cut path |
| Execution | rulings with cost if wrong; session handoffs; questions to the author one at a time |

## Common mistakes

| What happens | What to do instead |
|---|---|
| "The hypothesis is that the network is better" | Write the band, the threshold in points, the baseline and its calibration; write what result would refute it. |
| "We'll choose the threshold on the test set just this once" | Sweep on validation and freeze; a result that depends on a test-chosen point is an anti-goal. |
| "The baseline numbers are taken from the paper" | Reproduce the baseline on your own data with your own evaluation code; published numbers have different conditions. |
| "Average accuracy 92 %" | Report per band; the average hides the band at −10 dB where the method gives 30 %. |
| "We'll decide what to cut when we see how it goes" | Write the order of cuts and the never-cut path now; a cut made under deadline pressure removes the wrong thing. |
| A candidate dropped quietly after a bad run | It stays in the report with its number and reason; the sieve is a result. |
| A change of protocol mid-study, remembered but not written | A dated ruling with its cost if wrong, carried into the methods chapter. |
| "The reviewer will not ask about leakage" | The first reader asks exactly that; the design answers it with the split rule. |
