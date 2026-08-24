---
name: using-sv-processes-and-ports
description: Use when writing or modernizing SystemVerilog RTL modules — choosing always_comb/always_ff/always_latch vs plain always or always @*, using tasks/functions inside RTL, or instantiating modules (positional/named/.name/.* connections, top-level assembly); also when a synthesis log shows "does not contain a latch/flip-flop" warnings or a sim/synth mismatch traces to a sensitivity list.
---

# SystemVerilog Processes and Port Connections

Distilled from Cummings, *SystemVerilog Logic Specific Processes for Synthesis* (SNUG-2016, Tech Paper 2nd) and *SystemVerilog Implicit Port Enhancements* (SNUG-2007 Boston, Best Paper 1st).

## Processes: always_comb / always_latch / always_ff — always, no exceptions

The always_type processes exist to make **designer intent compiler-checkable**. What each buys you:

1. **Guideline #6 becomes a compile error.** Assigning one variable from two always_type processes (or an always_type + plain always) fails simulation compilation (VCS "Illegal combination of drivers"). With plain `always` the same bug simulates nondeterministically and surfaces only in synthesis — late.
2. **Blocking `#delay` assignments become compile errors.** `always @(posedge clk) #2 q <= d;` silently *misses asynchronous resets* in RTL sim (simulator is parked in the delay) — a sim/synth mismatch found only at gate level. `always_ff` rejects it at compile time. (Delays on the *RHS of NBAs* remain legal.)
3. **`always_comb` beats `always @*` on sensitivity**: it is sensitive to signals read *inside called functions* (`@*` reads only function/task *header* arguments — body-referenced signals become hidden inputs and a silent sim/synth mismatch); it triggers once automatically at time-0; it can't be assigned from another process; `@*` can be nested in an always — `always_comb` can't be abused that way.
4. **`always_ff` does NOT build a sensitivity list** — nothing in the body names the clock, its polarity, or sync/async reset. The edge list is still mandatory and still yours to get right: `always_ff @(clk, rst_n)` (no edges) gets only a DC *warning*, then synthesizes an AND gate with a dangling clk and — worse — no warning that `d` is missing from the sensitivity list.

**Tasks are dead in RTL: replace every RTL task with a `void function`.** Void functions are 0-time, reject delays/event controls at compile time, and — the hidden gem — `always_comb` deep-scans their bodies for sensitivity. This enables *narrative combinational coding*: a big always_comb reduced to `step_a; step_b; step_c;` calls of argument-less void functions, each independently maintainable.

**Treat these DC warnings as errors** (they are exactly the mismatch happening): `Netlist for always_comb block contains a latch (ELAB-974)` · `Netlist for always_latch block does not contain a latch (ELAB-975)` · `Netlist for always_ff block does not contain a flip-flop`. The tools won't stop; you must.

## Port connections: the .* methodology

Top-level netlists are pages of `.BORING(BORING)` with near-zero information value. SystemVerilog `.*` (and `.name`) fix both the tedium and — more importantly — the *checking*:

| Situation | Verilog-2001 named ports | SV `.*` / `.name` |
|---|---|---|
| Port/net size mismatch | warning, sim runs (almost always a real bug) | **ERROR** |
| Port omitted from instantiation | legal, silently unconnected | **ERROR** (with `.*`) |
| Undeclared 1-bit net at top | legal, silently springs into existence | **ERROR** |

The rules (all from IEEE 1800 via the paper):

1. `.*` once per instance; position anywhere but **put it last** (tooling convention).
2. No mixing with *positional* ports; mixing with *named* ports is required whenever rules 3–5 apply.
3. Name differs → named port: `.din(alu_out[7])`.
4. Port narrower than the bus → named with part-select: `.dataout(dataout[7:0])`.
5. Port wider than the net → named with concatenation: `.din({4'b0, nibble})`.
6. Unconnected ports listed explicitly empty: `.zero(), .ones(), .*`.

**Prefer `.*` over `.name`**: an IEEE 1800-2005 wording gap lets `.name` silently omit unconnected ports (backward compatibility blocked the fix in 1800-2008), so `.name` forfeits the very check that motivates implicit ports. Also `.name`+`.*` mixing (for wildcard-imported package nets) is standard-legal but effectively unsupported by tools — avoid packages of net declarations; that's what `interface` is for.

**Exceptions**: never use implicit ports in **gate-level netlists** (hundreds of primitives share port names a/b/y/q — `.*` would short unrelated ports together). Arrays-of-instance and generate loops work with `.*` for the shared pins (clk/rst/ce); the per-stage chained buses need named connections.

**Naming convention is the enabler**: `.*` pays off in proportion to nets being named identically to the ports they connect (the paper's retro-fit case study: 7% code reduction with hostile naming, 29.6% after normalizing names). Choose port/net names for `.*` compatibility from day one — this composes with the CDC domain-prefix convention: a signal named for its domain on both sides of a module boundary connects via `.*` for free.

## Red flags

Plain `always` (or `always @*`) in new SystemVerilog RTL · a `task` called inside an RTL process · `always_ff` whose sensitivity list lacks edge keywords · a DC "does not contain a latch/flip-flop" warning scrolling past unfixed · positional port connections anywhere outside generated netlists · a port-width mismatch warning being ignored · `.name` chosen where `.*` would compile.
