---
name: coding-fsms
description: Use when writing, reviewing, or refactoring any finite state machine in Verilog/SystemVerilog — state registers, next-state logic, state encodings (binary/onehot/output-encoded), registered or glitch-free FSM outputs — or when an FSM synthesizes large/slow, is hard to debug in waveforms, or someone proposes a "recover to IDLE" default arm.
---

# FSM Coding Styles

Distilled from four award-winning Cummings papers: *FSM Design & Synthesis using SystemVerilog Part I* (SNUG-2019, Best Paper 1st), *Fundamentals of Efficient Synthesizable FSM Design* (ICU-2002), *Synthesizable FSM Design using SystemVerilog 3.0* (SNUG-2003), *Coding & Scripting Techniques for FSMs with Synthesis-Optimized Glitch-Free Outputs* (SNUG-2000 Boston).

## The style decision

| Style | Verdict | Why (measured across fsm1/fsm7/fsm8/prep4 benchmarks, DC + 2 libraries) |
|---|---|---|
| **3-always** (state reg · `always_comb` next · registered outputs from `case (next)`) | **Default choice** | Least code (1-always needs 41–165% more), outputs once per state, glitch-free registered outputs, easy to modify |
| **4-always** (3-always + separate `always_comb` next-output logic from `state`+inputs, registered once) | Timing upgrade | Matches/beats 1-always synthesis QoR at ~half the code; convert a 3-always to it only when timing demands |
| 2-always (combinational outputs) | Only for Mealy/comb-output needs | Best area, but outputs glitch and eat the downstream module's clock cycle |
| 1-always | **Avoid** | Outputs assigned per *transition arc*, not per state → code explosion, error-prone, hard to change; no consistent QoR win |
| Onehot **index-parameter** reverse-case | FPGA favorite | Parameters are bit *indexes*; `case (1'b1)` / `state[IDLE]:` does 1-bit compares. The only sanctioned `full_case parallel_case` site — in SV use `unique case (1'b1)` |
| Onehot with onehot-*encoded* parameters | **Avoid** | Forces full-vector compares — consistently the largest/slowest style measured |
| Output-encoded | Most area-efficient for registered outputs | Outputs ARE state bits (`assign {ds,rd} = state[1:0];`) — glitch-free with zero output logic; encoding built by the 2000 paper's table procedure (dedupe output patterns, add extra MSBs for uniqueness) |

## The checklist (SNUG-2019, condensed)

1. Ports and internals: `logic`; fills with `'0 / '1 / 'x`.
2. States: `typedef enum` for `state, next` — **with an extra `XXX = 'x` member**, which requires a 4-state base type: `enum logic [1:0] {...}`. Keep two package files (`fsm_pkg_a.sv` abstract, `fsm_pkg_b.sv` encoded) declaring the *same* package name — swap encodings by compile order, RTL untouched.
3. State register: exactly 3 lines, `always_ff`, **no `begin-end`** (a `begin-end` invites statements before the reset `if`, which breaks DC elaboration), at the top after the typedef:
   ```systemverilog
   always_ff @(posedge clk, negedge rst_n)
     if (!rst_n) state <= IDLE;
     else        state <= next;
   ```
4. Next-state `always_comb` opens with **`next = XXX;`** (start with X-style; `next = state` is the allowed alternative that permits omitting loopback arcs). Then `case (state)` with one if/else-if per transition arc — arcs on the diagram must equal assignments in the code (self-check) — `next` assignments in one neat column, `default: next = XXX;`.
5. Registered outputs: pre-default output assignments, then **`case (next)`** — decode the state being *entered*, never `case (state)` (that delays outputs a cycle):
   ```systemverilog
   always_ff @(posedge clk, negedge rst_n)
     if (!rst_n) begin rd <= '0; ds <= '0; end
     else begin
       rd <= '0; ds <= '0;
       case (next)
         READ, DLY: rd <= '1;
         DONE     : ds <= '1;
         IDLE     : ;
         default  : {rd,ds} <= 'x;
       endcase
     end
   ```
   (Two NBAs to one variable in a block is standard-defined: last one wins — this default-then-override style is proper, not a race.)

## Why X, not "safe recovery"

`next = 'x` pre-defaults do two measured jobs: **debug** — a forgotten transition arc makes the waveform go red exactly at the missing assignment instead of silently looping; **synthesis** — X's are don't-cares (K-map holes), never worse and often smaller/faster than `next = state` in the benchmarks.

The "what if the FSM reaches an illegal state" fear is, per Cummings, "generally invalid or poorly developed": state registers don't spontaneously change any more than other flops. Where upsets are real (space, medical, radiation): **silently returning to IDLE is *not good enough*** — the rest of the design is mid-transaction and locks up waiting. Transition to a dedicated **error state** that tells the surrounding logic to reset. Never write `default: next = IDLE;` as reflexive "robustness" — it's the worst of both worlds (hides bugs in sim, doesn't actually recover the system).

## Structural rules

- One FSM per module (FSM tools and reuse depend on it); parameters/enums for encodings, never `` `define `` (global, collides across FSMs).
- Registered outputs support cloud-register partitioning: no combinational logic on module outputs → per-module time budgeting and trivially scriptable constraints (the 2000 paper's core argument).
- Asynchronous Mealy outputs violate that partitioning — usually better moved into the receiving module's input logic.
- Sequential `always_ff` = NBAs only; `always_comb` = blocking only (see avoiding-verilog-races).

## Red flags

`default: next = IDLE;` without a documented radiation/safety story · outputs decoded from `case (state)` in a registered-output FSM · enum without an `XXX` member / 2-state base type blocking `'x` · onehot FSM with onehot-encoded parameters · one giant clocked always with per-arc output assignments · `` `define `` state encodings · `begin-end` around the 3-line state register.
