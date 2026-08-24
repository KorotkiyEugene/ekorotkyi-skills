---
name: coding-case-statements
description: Use when writing or reviewing any Verilog/SystemVerilog case/casez/casex statement, priority encoder, one-hot mux or decoder; when full_case/parallel_case pragmas appear in code; when synthesis reports latches from a case statement; or when pre- and post-synthesis simulations disagree around select/decode logic.
---

# Case Statements, Priority Logic, and the Evil Twin Pragmas

Distilled from Cummings, *"full_case parallel_case", the Evil Twins of Verilog Synthesis* (SNUG-1999 Boston, Best Paper 1st).

## Overview

`// synopsys full_case parallel_case` tells the **synthesis tool** something the **simulator never hears**. When the pragmas change nothing, they're dead text; when they DO change synthesis, it is precisely because sim and synthesis now build different logic. **The directives are always most dangerous when they work.** The paper's alternate title: "How to add $200,000 and 3–6 months to your ASIC without trying" (a real ASIC respin: parallel_case on a priority-coded case; RTL and even gate-level sims passed, silicon failed).

Definitions: a case is **full** when every binary select pattern hits an item or default; **parallel** when no select value can match two items. Non-full ⇒ latch inference; non-parallel ⇒ priority logic in both sim and synth (consistent, but hidden).

## The rules

1. **Don't use `full_case parallel_case`** — with one sanctioned exception: one-hot FSMs coded with reverse case (`case (1'b1)` on the state vector), where SystemVerilog's `unique case (1'b1)` is the modern, checked replacement.
2. **Intentional priority → if-else-if**, not overlapping case items. Readers recognize a priority encoder in if-else-if; overlapping casez items hide it. (An ascending for-loop with last-assignment-wins is functionally the same priority encoder but equally unrecognizable — same objection applies.)
3. **Case statements are for tabular, truth-table-parallel logic** — decoders, muxes — where they beat if-else-if on readability.
4. **Kill latches with default assignments, not with `full_case`.** `full_case` only covers *missing case items*. If items assign different **subsets of outputs**, latches are inferred on every output anyway (the paper's address decoder: `full_case` present, three latches inferred). The robust idiom: assign every output a default value immediately after the process opens, *then* the case.
5. **`casez` with `?` (never `z` literals, never `casex`)** for don't-care matching. `casex` treats X in the *expression* as don't-care too — an unknown select silently matches the first item. Not synthesizable practice.
6. **Read the synthesis case-statement report** (`full/parallel` = auto|user|no). Any `user` entry is a pragma to justify or remove; `parallel: no` on logic you meant to be parallel means recode.
7. **Give sim and synthesis the same information.** That's the principle behind all of the above.

## Sim/synth mismatch mechanics (each documented in the paper)

| Coding | What happens |
|---|---|
| Non-full case + `full_case` | Sim: latch behavior on unmatched select. Synth: don't-care. Mismatch. |
| Full-by-default with `default: y = 1'bx` | Sim drives X; synth treats as don't-care — mismatch is *possible* in the unmatched space. Fine when that space is truly unreachable (and X aids debug/optimization — see the FSM skill); use a constant default when exact pre/post-synth equivalence is required. |
| Overlapping items + `parallel_case` | Sim: priority. Synth: no priority. The $200k respin. |
| `full_case` on decoder with enable folded into select | Synthesis **optimized the `en` pin away entirely** (dangling input); RTL sim showed nothing wrong — only post-synthesis sim differed. |

## SystemVerilog bridge

`unique case` ≈ parallel_case + full_case *as claims checked at runtime*: the simulator reports any overlap or unmatched select, so the assumption handed to synthesis is at least policed. `priority case` asserts full + intentional priority. They are better than pragmas — but a violation is only a runtime *warning*, so they still require a clean sim log, and they do not replace default-assignment latch hygiene. `unique case (1'b1)` is the sanctioned one-hot idiom. When one-hotness is an architectural guarantee exploited by AND-OR muxing, back it with an assertion (`$onehot`/`unique case`) instead of trusting the comment.

## Canonical patterns

```systemverilog
// Tabular parallel logic: full by construction — defaults first, then case
always_comb begin
  {mce1_n, mce0_n, rce_n} = 3'b111;          // rule 4: defaults kill latches
  casez (addr[31:30])
    2'b10: {mce1_n, mce0_n} = 2'b10;
    2'b11: {mce1_n, mce0_n} = 2'b01;
    2'b0?: rce_n            = 1'b0;
  endcase
end

// Intentional priority: if-else-if, visibly a priority encoder
always_comb begin
  id = '0; valid = 1'b1;
  if      (req[7]) id = 3'd7;
  else if (req[6]) id = 3'd6;
  // ...
  else if (req[0]) id = 3'd0;
  else             valid = 1'b0;
end

// One-hot select: reverse case, checked
always_comb begin
  y = '0;
  unique case (1'b1)
    sel[0]: y = d0;
    sel[1]: y = d1;
    sel[2]: y = d2;
    sel[3]: y = d3;
  endcase
end
```

## Red flags

`// synopsys full_case` or `parallel_case` anywhere outside a one-hot reverse-case FSM · `casex` in synthesizable code · `z` characters in casez items · overlapping case items without an explicit priority comment *and* if-else-if consideration · multi-output case items assigning different output subsets with no pre-case defaults · a synthesis case report you never looked at.
