---
name: writing-designer-sva
description: Use when adding SystemVerilog Assertions to RTL — protocol checks, invariants, X-checks, FSM one-hot checks — when deciding where assertion code lives (inline vs bindfile), when assertions are "too verbose" and being skipped, or when debugging why a failing assertion is hard to locate in a waveform viewer.
---

# SVA for RTL Designers

Distilled from Cummings, *SVA Design Tricks & SVA Bind Files* (SNUG-2009, Best Paper 1st) and *SVA — Bindfiles & Best Known Practices for Simple SVA Usage* (SNUG-2016, Best Paper 1st).

## Overview

Designers abandon SVA for one reason: verbosity ("the SVA circle of life": excited → trained → 3+ lines per check → abandoned). The fix is a *deliberately simple subset*: bindfiles + two macros + long labels. Division of labor: designers write the low-level/simple assertions; verification engineers write the complex ones.

## The 10 guidelines (2016 paper, verbatim-condensed)

1. Start using SVA after 2–3 h lecture + labs — don't wait for mastery of the full language.
2. **Bindfiles — use them!**
3. **Inline SVA in RTL — avoid it.**
4. Bind to **all instances of the module** (`bind fifo1 fifo1_asserts p1 (.*);`), never to one instance — you might bind to a working copy while another instance fails.
5. Add descriptive labels to every assertion.
6. **No `$error(...)`/`$display(...)` action blocks** — action-block messages reach only the transcript.
7. **Labels start with `ERR_`** + a short sentence of what is wrong: `ERR_FIFO_full_write_caused_wptr_to_change:`. The label appears in the transcript **and** in the waveform viewer, where expanding the failed assertion shows every tested signal — the label is an active design comment.
8. **Concurrent assertions; avoid immediate assertions.** Concurrent = sampled once per cycle at cycle end (like a register — ignores harmless combinational glitching); that fits ~95% of checks. Immediate assertions sample on demand — reserve them for genuinely asynchronous control (reset/preset going X), and even then put them in an `always @*` in the *bindfile*, labeled, one message + graceful `$finish`, not scattered per-register. (2016 reverses 2009's `assert($cast…)`/`assert(randomize())` advice: those are silently killed by `$assertoff` — use plain if-tests.)
9. **Macros** — the entire boilerplate lives in two `` `define``s; measured 50–80% less assertion code, and near-zero paren-balancing errors:
   ```systemverilog
   `ifndef ASSERT_MACROS
   `define ASSERT_MACROS
   `define assert_clk_xrst( arg ) \
       assert property (@(posedge clk) disable iff (!rst_n) arg);
   `define assert_clk( arg ) \
       assert property (@(posedge clk) arg);
   `endif
   ```
   (`default clocking`/`$assert*` tasks do the same job but with historically spotty tool/formal support; macros work everywhere.)
10. **`|->` with explicit `##n`; never `|=>`.** `|=>` ≡ `|-> ##1` and the two operators are visually near-identical at small font sizes — banning `|=>` (as ARM did) "dramatically" cut coding mistakes in training cohorts.

## Bindfile mechanics

A bindfile is **indirect instantiation**: `bind DUTMOD DUT_asserts p1 (.*);` projects the checker instance *inside* every DUTMOD as if it were instantiated there — so the checker sees ports **and internal signals** by name.

- Build the checker header by copying the DUT module: outputs→inputs, inputs stay, **all internal signals added as inputs too** (declare all of them, even unchecked ones — future assertions will want them). Same names ⇒ the bind connects with `.*`. Parameters must be passed by name (`.*` never matches parameters); the asserts module carries the same parameter list.
- Keep bind commands in a standalone two-line module `bindfiles` (`bindfiles.sv`), compiled as a **second top-level**; two run filelists — with and without assertions. Payoffs: RTL files never touched (no Makefile-triggered multi-hour re-runs from an assertion edit; no front-end tools choking on `checker`/`let` keywords), assertion-free speed runs for regressions.
- Bound modules must be monitors: **inputs only, no output drivers**; no nested binds (illegal per IEEE 1800, tools may drop support anytime); never use bind to configure/structure a design.
- Partition assertion files for gate-level reuse: ports-only / ports+registered-internals / everything — after synthesis the ports file still binds to the netlist unchanged.

## Canonical bindfile pair

```systemverilog
// fifo1_asserts.sv
`include "assert_macros.sv"
module fifo1_asserts (
  input logic [7:0] dout, din,
  input logic       full, empty, write, read, clk, rst_n,
  input logic [3:0] wptr, rptr, cnt);      // internals too

  ERR_FIFO_should_be_full:
    `assert_clk_xrst(cnt>15 |-> full);
  ERR_FIFO_full_write_caused_wptr_to_change:
    `assert_clk_xrst(full && write && !read |-> ##1 $stable(wptr));
  ERR_FIFO_reset_should_cause_empty1_full0:
    `assert_clk(!rst_n |-> (empty==1 && full==0));
endmodule

// bindfiles.sv — second top-level
module bindfiles;
  bind fifo1 fifo1_asserts p1 (.*);
endmodule
```

## Red flags

Assertions embedded in RTL source files · `|=>` anywhere · `else $error(...)` action blocks carrying the failure description instead of the label · labels like `as_check1` (name the *failure*, `ERR_...`) · `bind ... :u1` (single-instance bind) · bound module driving outputs · `assert($cast(...))`/`assert(x.randomize())` success-checking · per-register inline immediate reset-X asserts (one always-block check in the bindfile suffices) · three lines of property/endproperty ceremony for a one-line check the macro handles.
