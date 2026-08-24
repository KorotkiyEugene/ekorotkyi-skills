---
name: crossing-clock-domains
description: Use when any signal, bus, pulse, counter, or reset must pass between asynchronous (or unrelated-frequency) clock domains; when adding synchronizers; when partitioning or constraining a multi-clock design (false paths, CDC tool setup); when gate-level sims X-out at synchronizers; or when a "just add two flops" fix is being proposed for a multi-bit signal.
---

# Clock Domain Crossing

Distilled from Cummings, *CDC Design & Verification Techniques Using SystemVerilog* (SNUG-2008 Boston, Best Paper 1st) and *Synthesis and Scripting Techniques for Designing Multi-Asynchronous Clock Designs* (SNUG-2001, Best Paper 3rd).

## Overview

Any signal crossing asynchronous clock domains **will** violate setup/hold on the destination flop — that's a given, not a defect; synchronizers exist to contain the resulting metastability. STA on such paths is meaningless (`set_false_path`), and MTBF ∝ 1/(f_clk · f_data): both the sampling clock rate and the **data-change rate** shorten it. Every rule below traces to one of those two facts.

First question for every crossing: **may samples be missed** (e.g. Gray-coded FIFO pointers — yes), or must **every value be recognized** (then open-loop with analyzed frequencies, or closed-loop with acknowledge)?

## Single-bit rules

1. **2-FF synchronizer** is the standard; 3-FF for very high clock rates (MTBF too short). Nothing but flops in a synchronizer.
2. **Register the signal in the sending domain too** — an unregistered combinational output crossing the boundary carries settling glitches, which raises the effective data-change frequency and cuts MTBF. Flop-launched, flop-caught.
3. **"Three-edge" rule**: a CDC signal must stay stable ≥1.5× the receiving clock period (stable across three destination edges). A pulse merely *slightly wider* than one receiving period can straddle setup on one edge and hold on the next and vanish. A one-fast-clock-cycle pulse into a slower domain is flatly unacceptable.
4. Fast→slow with no-miss requirement: **open-loop** (stretch the pulse to ≥1.5× receiver period; legal only when clock ratios are fixed and analyzed — guard it with an SVA on minimum pulse width, or the next engineer will reuse it out of spec) or **closed-loop** (toggle the signal, synchronize it back as an acknowledge; safe for any ratio, costs round-trip latency).
5. Cross **toggles, not pulses**. The synchronized-pulse generator (2-FF sync + third flop + XOR) turns an any-polarity toggle into a clean one-cycle pulse in the receiving domain; the sender never needs to return to its initial level.

## Multi-bit rules

Never independently synchronize bits that belong together — skew means different bits land in different destination cycles (the load+enable pair that misses, sequenced enables that gap, encoded selects that glitch through a wrong decode). Three strategies, in order of preference:

1. **Consolidate** to one bit in the sending domain (drive load+enable from one flop; regenerate phase-shifted copies in the receiving domain).
2. **MCP formulation**: send the multi-bit data *unsynchronized* and hold it stable; synchronize only a toggling enable; the receiver loads data on the synchronized-enable pulse. Data can't go metastable because it isn't sampled until proven stable. Close the loop with the pulse generator's q-output fed back as acknowledge (ready/busy FSMs on both sides — the paper's `mcp_blk` has full code, appendix §12.2).
3. **Gray-coded counters** when the value is a counter (FIFO pointers): only one bit changes per increment, so a mid-transition sample is either the old or the new value. Binary counters are uncrossable (7→8 flips all bits; any value can be sampled). `bin2gray = (bin>>1)^bin`; gray2bin via `bin[i] = ^(gray>>i)`; registered Gray output always (no combinational settling on the crossing). Style #2 counter (parallel binary + Gray registers) is faster than convert-increment-convert.
4. Or pass the bus through an **async FIFO** (see designing-async-fifos), or its minimal cousin the **1-deep/2-register FIFO synchronizer** — toggle-flop pointers, `wrdy = ~(wq2_rptr ^ wptr)`, `rrdy = rq2_wptr ^ rptr` — which shaves a cycle off each MCP direction and needs no Gray logic.

## Partitioning, naming, constraints (the methodology that makes it verifiable)

- **One clock per module**; only the top level sees multiple clocks. All I/O of every design block synchronous to that block's one clock → each domain is a pure synchronous design for STA, zero false paths inside.
- **Synchronizer modules**: every crossing lives in a dedicated module with one clock, containing only synchronizers (n·(n−1) such modules worst case for n domains). No worst-case timing analysis needed on them — only min-time (hold) between stage-1/stage-2, plus (2008 update) max-time in case layout separates the pair. FPGA: add `ASYNC_REG`/keep attributes so the pair stays adjacent.
- **Domain-prefix naming**: every signal named for the clock that generates it (`uaddr`, `vdata`...; synchronized copies renamed into the new domain). Then all CDC constraints collapse to wildcards: `set_false_path -from {u*}`. The convention is only useful if the whole team holds it.
- MCP data paths: false-path (or `set_max_delay` bounded by the enable's synchronization time) the *data* bus; the synchronized enable path is the timed one.

## Reset crossing

Each domain gets its own reset synchronizer (async assert, **synchronized de-assert**) fed from the master reset; de-assert order between domains can be chained if sequencing matters. Never release one domain's reset asynchronously relative to its clock. (Details in the two Sunburst reset papers; the asend/back FSM handshake in the CDC paper survives common reset, but *partial* resets of one side of a toggle handshake produce phantom events — treat as an integration hazard.)

## Gate-level sim X-storms

Synchronizer stage-1 flops legitimately violate setup/hold in gate sims and ASIC/FPGA models drive X. Fixes, best first: two-SDF-file technique (full-timing SDF, then a second SDF zeroing setup/hold on stage-1 flops only — works in any flow); vendor synchronizer cells with SDF support; Synopsys `set_annotated_check 0 -setup -hold` on stage-1 cells; force UDP notifier inputs. Never globally disable timing checks. For RTL sims, the paper's `sync2` model with a testbench-settable per-bit `DLY` randomizes 2-vs-3-flop delay per bit — exposes designs that secretly depend on bus-coherent synchronization.

## Red flags

Multi-bit bus through parallel 2-FF synchronizers · combinational logic driving a crossing (unregistered launch) · one-cycle pulse from fast to slow domain · binary counter crossed between domains · synchronizer buried inline in a multi-clock module (invisible to wildcard constraints and CDC tools) · open-loop crossing with no pulse-width assertion and no documented frequency analysis · signals named without domain prefixes in a multi-clock design · "we'll catch CDC bugs in simulation" (you won't — RTL sim has ideal timing).
