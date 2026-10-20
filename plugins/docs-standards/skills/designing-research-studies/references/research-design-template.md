# Research design document: the skeleton

Copy the headings, answer the questions under each, delete the questions. A section
whose questions have no answer yet is kept with the sentence "open: <who decides>", never
deleted: a missing section is read as "not considered".

---

# Design: <study title>

Date, author, status (draft / approved by <owner> on <date>). The document is the
authority the plan and the report argue from; later changes are dated edits with a
reason, not silent rewrites.

## 1. Intent and motivation

- What problem is solved, for whom, in one paragraph a non-specialist engineer follows.
- The gap in numbers: what the closest known work achieves (its number, its condition,
  its platform) and what the application needs (its number, its condition). Derive the
  distance between them with arithmetic where the two are in different units.
- Why now: the platform, dataset, tool or finding that makes the study possible.

## 2. Goals, non-goals, anti-goals

- Goals: the deliverables, each checkable (an artefact, a table, a measurement).
- Non-goals: what a reader may expect and will not get, with one line on why.
- Anti-goals: outcomes that make the study a failure even if every goal is met.

## 3. Constraints

| Constraint | Value | Source |
|---|---|---|
| target platform and its supported operations | | vendor document, version |
| memory, compute, deadline | | owner's decision, date |
| data licences and what they allow | | licence text |
| required compatibility (framework version, toolchain) | | |

## 4. Problem statement and hypotheses

The task(s) in one paragraph each: input, output, the metric that defines success, the
condition that drives difficulty.

| Hypothesis | Claim (number, condition band, dataset, cost) | Refuted by | Alternative explanations and their controls |
|---|---|---|---|
| H1 | | | |

## 5. Method space and sieve

| Axis | Discarded at review (reason, source) | Candidates for the experiments |
|---|---|---|
| representation | | |
| model family / output head | | |
| training scheme | | |
| deployment variant | | |

Sieve criteria (numbered, with thresholds; fixed before the experiment they govern):

1. incompatible with the target platform: ...
2. no gain for the cost: < N points over K seeds while cost ≥ M times ...
3. failure at the edges: > N points loss in any band after ...
4. irreproducible: ...
5. hardware blocks: < P % gain in latency or energy at equal accuracy ...

A candidate discarded at any checkpoint stays in the report with its result and reason.

## 6. Checkpoints

| Checkpoint | Where | What is checked | Decision |
|---|---|---|---|
| review | | | |
| smoke (tiny subsets, code flag) | | | |
| accuracy (full data, ≥ 3 seeds) | | | |
| deployment | | | |
| target hardware | | | |
| real data | | | |

## 7. Experiment protocol

- Data and splits: each dataset, task, split rule (by record / session / official),
  what is identical across runs, licence.
- Condition bands: the condition, the band edges, the rule for a value on an edge.
- Metrics: per task, with the formula or the protocol it follows, the script that
  computes it, and the two calibration cases with known answers.
- Baselines: which, how calibrated (per band, on validation), compared on which curve.
- Comparisons: one variable at a time, same evaluation code, tables generated from logs,
  full sweeps to appendices.
- Seeds: how many for the sieve, how many for decisive comparisons, how reported.
- Hardware measurements (if any): batch, number of fragments, mean and tail, stage
  breakdown, threads, power measurement point, energy as power × time.
- Transfer to real data (if any): levels from synthetic test to measured records, what
  is allowed at each level (zero-shot, small labelled set, unlabelled adaptation).

## 8. System architecture (when a system is delivered)

The pipeline from input to decision, the stage boundaries experiments may move, what
runs where (processor, accelerator, logic), the data path between them.

## 9. Stages and deliverables

| Stage | Content | Deliverable that proves completion |
|---|---|---|

Order in which nothing is cut: <stage list>. Stages that may be cut, in order of cutting.

## 10. Risks and rollbacks

| Risk | Sign that it happened | Rollback that still yields a complete study |
|---|---|---|

## 11. Left to the implementer

Hyperparameters and grids, library choices, test structure, configuration format, file
layout, figure tooling.

## 12. Questions to the author

Numbered, each with what the answer changes. Asked one per message.
