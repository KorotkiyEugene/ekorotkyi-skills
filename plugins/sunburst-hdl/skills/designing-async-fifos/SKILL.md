---
name: designing-async-fifos
description: Use when designing, reviewing, or debugging an asynchronous/dual-clock FIFO, when passing multi-bit data between asynchronous clock domains through a buffer, when writing full/empty flag logic, or when a FIFO "works in simulation" but corrupts data in hardware.
---

# Asynchronous FIFO Design

Distilled from two Cummings SNUG-2002 papers: *Simulation and Synthesis Techniques for Asynchronous FIFO Design* (FIFO1) and *…with Asynchronous Pointer Comparisons* (FIFO2, Best Paper 1st, with Peter Alfke, Xilinx).

## Overview

An async FIFO passes multi-bit words between asynchronous clock domains; the only signals that may cross domains are the read/write **pointers, in Gray code, through 2-FF synchronizers**. Most wrong FIFOs work 99%+ of the time, and **RTL simulation cannot catch pointer-CDC bugs** (pointers behave ideally in sim; even back-annotated gate sims need luck) — correctness comes from construction, not from testing.

## The FIFO1 architecture (use this one)

Six modules, partitioned **one clock domain per module**, all module outputs registered:

| Module | Domain | Contents |
|---|---|---|
| `fifo1` | wrapper | instantiation only (discardable in a larger design) |
| `fifomem` | dual-port RAM | write port in wclk, read port async/rclk |
| `sync_r2w` | wclk | 2-FF sync of rptr → `wq2_rptr` (3-line always block) |
| `sync_w2r` | rclk | 2-FF sync of wptr → `rq2_wptr` |
| `rptr_empty` | rclk | read pointer + empty flag |
| `wptr_full` | wclk | write pointer + full flag |

**Naming convention is load-bearing**: prefix = the domain the signal is *clocked in now* (`wq2_rptr` = rptr after 2 sync stages in the **w**clk domain). Then STA setup is one wildcard: false-path everything named `r*` entering wclk-domain modules and vice versa. A synchronizer module contains flops only — no logic.

Pointer scheme (per domain, Gray counter "style #2" — preferred, exploits binary carry logic and is faster in FPGAs):

```systemverilog
// dual register pair: binary for arithmetic+addressing, Gray for crossing
always_ff @(posedge wclk or negedge wrst_n)
  if (!wrst_n) {wbin, wptr} <= '0;
  else         {wbin, wptr} <= {wbinnext, wgraynext};
assign waddr     = wbin[ADDR_W-1:0];            // binary addresses the RAM
assign wbinnext  = wbin + (winc & ~wfull);      // increment gated by flag
assign wgraynext = (wbinnext >> 1) ^ wbinnext;  // binary -> Gray
```

Pointers are **n+1 bits** for a 2^n-deep FIFO (extra MSB = wrap parity; depth must be a power of 2 — no odd-length Gray sequences exist).

## Full and empty — the part everyone gets wrong

- **Empty** (rclk domain): next read Gray pointer equals the synchronized write pointer, all bits:
  `rempty_val = (rgraynext == rq2_wptr);` — registered.
- **Full** (wclk domain): NOT simple "MSBs differ, rest equal". Gray code is reflected — the second MSB mirrors too. Three conditions: MSBs differ **and** 2nd MSBs differ **and** the rest equal:
  `wfull_val = (wgraynext == {~wq2_rptr[ADDR_W:ADDR_W-1], wq2_rptr[ADDR_W-2:0]});` — registered.
  The naive test both asserts false-full **and silently overwrites the last written word** (FIFO1 Fig. 6, 8-deep example).
- Compare against the **next** Gray value (`wgraynext`/`rgraynext`), not the current pointer — that's what lets the flag itself be a clean registered output that still asserts exactly on time.
- Flag **assertion is exact; removal is pessimistic** (~2 synchronizer clocks late). That's the safety mechanism, not a bug: the producer/consumer is merely held off a couple of extra cycles. Never "optimize" it away.
- A fast-domain pointer that increments twice between slow-domain samples is safe: the first transition settles long before the sampling edge — an argument valid **only** for Gray sequences.

## Safety belts (a "safe, general-purpose FIFO" has all of them)

1. Pointer increment gated by its flag (`winc & ~wfull`, `rinc & ~rempty`).
2. Memory write *separately* gated by `wfull` inside `fifomem`.
3. Optional sticky `ovf`/`unf` status bits (cleared only by reset) to record protocol violations.
4. Per-domain resets (`wrst_n`, `rrst_n`), asynchronous assert / synchronized release; async reset of both pointers is fine (reset means the data is void anyway). Reset makes `rempty` preset to 1, `wfull` clear to 0.

## Alternatives — know when they apply

- **Sampled binary pointers + ready/ack handshake**: crosses ANY multi-bit value (not just counters), allows arbitrary (non-power-of-2) depths and easy almost-full/empty arithmetic; costs ≥2+2 clock edges of extra pessimism per update. This is the general multi-bit CDC pattern of which the Gray FIFO is a specialization.
- **FIFO2 asynchronous-comparison style** (quadrant detection + direction latch, async-preset flags): fewer sync flops, award-winning — and its own author flags it "generally incompatible with STA and DFT": unregistered async flag-assertion paths that need hand analysis, legitimate runt pulses on `aempty_n/afull_n`. Don't pick it for new mainstream designs; harvest its Gray-counter style #2 and quadrant trick instead.
- A behavioral FIFO model (binary pointers, one module, both clocks) is fine **for the testbench only** — never synthesize it.

## Common mistakes

| Mistake | Consequence |
|---|---|
| Binary pointer crossed with 2-FF sync | multi-bit coherency loss → phantom full/empty, corruption |
| Full = "MSBs differ + LSBs equal" on Gray pointers | false full + overwrite of last word |
| Both clock domains coded in one module, inline synchronizers | STA/CDC tooling needs per-register hacks; wildcard false-path recipe impossible |
| Signal named for its source domain after synchronization | false-path wildcards hit the wrong flops |
| Flags compared from *current* pointers then registered | flags assert one cycle late → overflow window |
| "Fixing" pessimistic flag removal | removes the safety margin that makes overflow/underflow impossible |
| Trusting RTL sim to validate the CDC | pointer races are invisible in RTL simulation |
