---
name: speeding-up-simulation
description: Use when a Verilog/SystemVerilog simulation or regression is slow, when writing testbench infrastructure (clock generators, logging, monitors, coverage sampling, randomization constraints), or when reviewing TB/RTL code for simulation cost — before reaching for a bigger machine or more licenses.
---

# Simulation Performance Coding

Distilled from Cummings, *Verilog Coding Styles for Improved Simulation Efficiency* (ICU-1997, Best Paper 1st) and Cummings/Rose/Sherer, *Yikes! Why is My SystemVerilog Still So Slooooow?* (DVCon-2019, Best Paper 1st; benchmarks on all three major simulators, reported anonymized as A/B/C).

## The cost model

Event-driven simulators charge per *event* and per *awake process*. Everything below reduces to: fewer processes, fewer wake-ups, fewer events, no hidden software costs (string building, heap churn, deep loops) in per-cycle paths. "Let sleeping processes lie."

## The catastrophic offenders (DVCon-2019, measured)

| Offender | Slower by (sim A/B/C) | Fix |
|---|---|---|
| Unguarded message/string building (`$sformatf` loop feeding `uvm_info`) — even when verbosity filtering means *nothing prints* | **3304 / 9148 / 9717 %** | Guard construction itself: `if (uvm_report_enabled(...))` or a verbosity/plusarg flag around the *formatting*, not just the printing |
| "Clever" foreach sorting **constraint** (`payload[i] >= payload[i-1]`) | **1535 / 3621 / 6553 %** | `post_randomize()` + `payload.sort()` — up to 1000× |
| Bit-blasting a vector op into a per-bit `generate` of always blocks | −2 / 53 / **316 %** | Full-vector operations in one process |
| `new()` inside a hot loop instead of construct-once-reuse | 14 / 26 / **82 %** | Hoist construction; pool/reuse objects; prefer `struct` over `class` for plain data containers; `ref` args for big objects |
| Unconditional analysis-port sampling+broadcast with **no connected consumers** | 25 / 28 / 40 % | `if (ap.size()) forever collect();` |
| While-loop "behavioral FSM" (process wakes every clk in every state) | 1 / 2 / 41 % | Standard FSM coding — and note the reverse: proper 3-always style benchmarked 1/2/41% *slower* than while-loops on one tool, yet the paper still mandates standard styles — correctness and synthesizability outrank this delta |

Also from 2019: static arrays over dynamic where size is near-fixed; queues for front/back ops, dynamic arrays for random access (queue indexing O(1), associative O(log n)); DPI/virtual calls moved *inside* their qualifying `if` so the wake-up optimization survives; assertion attempts minimized (trigger on first cycle of enabling condition, single-clock, split rather than long multi-cycle); vectored/auto coverage bins, covergroups sampled on a specific qualified event (`@(posedge valid iff collect_cov)`), never the raw clock; `wire logic` ports measured −3…7% — "not worth the extra coding effort".

## Testbench infrastructure rules (1997 measurements that still hold, mechanism-confirmed 2019)

1. **Merge same-clock assignments into one always block** — 4 blocks vs 1 cost +34%. Process count is the metric; don't scatter cycle counters, loggers, watchdogs across separate always blocks when one serves. (SV caveat: `always_ff`/`always_comb` single-driver checking may legitimately force separate blocks in RTL — this rule is for TB code and same-variable-group logic.)
2. **Behavioral clock oscillators, never gate/primitive ones** (+85–89%): `initial begin clk <= 0; forever #(CYCLE/2) clk = ~clk; end`.
3. **Monitor/debug data: hierarchical references, NOT ports.** Passing data over module ports cost **+46%** vs hierarchical reference (Verilog-XL measurement; the principle — extra hierarchy/port shuffling costs — was reconfirmed by 2019's inlining discussion). Ports stay recommended for *design* connectivity; but a TB monitor reading `dut.u_core.state` hierarchically (or a bound monitor module) beats routing debug buses out through ports. Don't invert this one.
4. **`$time` display is expensive** (+43–99% per displayed value in the 1997 tables): keep time values out of per-cycle logs; no unconditional per-cycle `$display`/`$fdisplay` at all — and never `$fflush` per cycle.
5. **Coarse `timescale`** — 1ns/1ps cost +99% time/+156% memory *on Verilog-XL*; modern simulators are far less sensitive, but don't ask for 1 ps precision you don't use.
6. Era-specific 1997 advice that should NOT be repeated as current: removing begin-end pairs (+6% then, noise now), `` `define`` vs parameter memory tricks, case-vs-if microdeltas. Cite the mechanism, not the 1997 number.

## Regression discipline (composite of both papers' practice)

Nightly runs: silent, self-checking, fail-fast (error cap + `$fatal`), no waves, watchdog-bounded, stimulus preloaded via `$readmemh`. Debug is a *rerun* of the same seed with plusarg-gated logging and windowed, scope-limited dumping (`$dumpvars(1, dut_scope)` from `+wave_start=N`) — one extra run of one failing test instead of taxing every passing test.

## Red flags

String/`$sformatf` work outside a verbosity guard · a sorting/ordering `foreach` constraint · `new()` in a `forever` loop · per-bit generate always blocks for vector math · unconditional `ap.write()` monitors · several `always @(posedge clk)` TB blocks that could be one · per-cycle `$fflush`, `$time` printing, or unconditional logging · gate-primitive clock generator · `$dumpvars(0, tb)` in a nightly regression · 1997-era folklore ("remove begin-end", "`define is faster") presented as current fact.
