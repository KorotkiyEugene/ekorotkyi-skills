---
name: writing-synthesizable-rtl
description: >-
  Coding patterns for RTL that synthesises into the hardware you intended — memory and
  DSP inference, reset style, latch avoidance, clock-domain crossings, and the places
  where simulation and synthesis diverge. Use this skill whenever you WRITE, EDIT, or
  REVIEW Verilog, SystemVerilog or VHDL that will be synthesised. Trigger on "write a
  module", "add a FIFO/RAM/ROM/counter/state machine", "implement this in
  Verilog/VHDL", "make this synthesisable", "review this RTL", "why did this infer
  latches", "the RAM became registers", "my multiplier didn't use a DSP block", "this
  works in simulation but not on hardware", "clock domain crossing", or any HDL change
  destined for an FPGA or ASIC. Not for testbench-only or simulation-only code.
---

# Writing Synthesisable RTL

The gap that costs the most time is not code that fails to compile — it is code that
compiles into something other than what you meant. Synthesis tools accept a wide range
of styles and silently pick a poor mapping when the pattern is not exactly what their
inference engine recognises.

## The one rule that matters most

**Write the pattern the tool recognises, then verify from the report that it recognised
it.** Inference is pattern matching, not understanding. A memory description that reads
perfectly to a human, and simulates correctly, becomes thousands of flip-flops if it
deviates from the expected shape — and nothing warns you.

Always close the loop: after synthesis, confirm the resource counts match intent. See
**verifying-fpga-builds**.

## Memory inference

### The read must be unconditional

This is the single most common way to lose block RAM inference:

```verilog
// BROKEN -- becomes flip-flops
always @(posedge clk) begin
    if (sel && !ready) begin
        if (we) ram[addr] <= din;
        rdata <= ram[addr];          // read gated by sel/ready
        ready <= 1'b1;
    end
end
```

```verilog
// CORRECT -- infers block RAM
always @(posedge clk) begin
    if (wr && we) ram[addr] <= din;
    rdata <= ram[addr];              // unconditional
end

always @(posedge clk) begin          // handshake in its own block
    ready <= sel && !ready;
end
```

Block RAM has a registered read port with no enable on the address path in its simplest
form. Gate the read and the tool can no longer map it, so it builds the array from
registers instead. Measured cost of exactly this mistake on an 8 KB memory: **66,794
registers and 2,304 memory bits**, versus **1,226 registers and 67,840 memory bits**
after moving the read out of the conditional — the same design, 40× the logic.

Keep handshake and control logic in a *separate* `always` block from the memory itself.

### Other inference requirements

- **One clock per memory block.** Mixing clocks in one `always` block prevents mapping.
- **No reset on the memory array.** Block RAM contents cannot be reset; a reset on the
  array forces registers. Reset the *output register* if you need to.
- **Byte enables** must be written as separate conditional assignments to slices of the
  same array element, all inside one clocked block.
- **Initial contents** come from a `.mif`/`.hex`/`.coe` via a synthesis attribute or an
  `initial` block, depending on vendor. Confirm the log shows the file was applied.
- **Read-during-write behaviour** must match what the hardware offers. Tools will add
  "pass-through logic" to match your description — a warning worth reading, because that
  logic costs fabric and may not be what you wanted.

## DSP inference

Multipliers map to hard DSP blocks only when the shape fits: register the inputs and
outputs, keep widths within the block's native size, avoid mixing signed and unsigned
without explicit casts. A multiplier that lands in fabric shows up as a large LUT count
and zero DSP blocks — check both.

## Latches

An incompletely specified combinational block infers a latch, which is almost never
intended and wrecks timing analysis.

```verilog
// Infers a latch: no else, no default
always @(*) begin
    if (sel) y = a;
end
```

Fix by assigning a default first, or covering every branch:

```verilog
always @(*) begin
    y = 1'b0;          // default
    if (sel) y = a;
end
```

Same rule for `case`: always include `default`. Treat any latch-inference warning as an
error unless you deliberately wanted a latch and said so in a comment.

## Resets

- **Prefer synchronous reset** in FPGA fabric; it maps into the register's own reset port
  and does not consume routing as a separate asynchronous network.
- **Reset only what needs it.** Datapath registers usually do not; control and state
  registers do. Resetting everything inflates fan-out on the reset net and can hurt Fmax.
- **Never reset a memory array** (see above).
- **Release reset synchronously.** An asynchronous assert with an asynchronous release
  can violate recovery/removal timing. Use a reset synchroniser.
- Constrain the reset input as a false path only if it is genuinely asynchronous — and
  then make sure the synchroniser exists. See **constraining-fpga-designs**.

## Clock domain crossings

Every crossing needs a structure appropriate to what is crossing:

- **Single-bit control/status**: two-flop synchroniser in the destination domain.
- **Multi-bit data**: never two-flop it bit by bit — the bits arrive on different cycles.
  Use a handshake, an asynchronous FIFO, or Gray coding for counters.
- **Pulses between domains of different rates**: toggle-and-synchronise, not a raw pulse.

The RTL structure and the timing constraint are two halves of one thing. A synchroniser
without a constraint leaves the tool trying to close an impossible path; a constraint
without a synchroniser is a documented metastability bug.

## Where simulation and synthesis diverge

| Construct | Simulation | Synthesis |
|---|---|---|
| `initial` blocks | run | FPGA: sets power-up state. ASIC: ignored |
| `#delay` | delays | ignored entirely |
| Incomplete sensitivity list | reads as written | tool infers the full list; behaviour differs |
| `x`/`z` propagation | tracked | `x` becomes 0 or 1; `z` only valid on tri-states |
| Blocking `=` in clocked blocks | order-dependent | race conditions between blocks |

Use non-blocking `<=` in clocked blocks and blocking `=` in combinational blocks. This
is not style — mixing them creates simulation/synthesis mismatches that appear only on
hardware.

## Before you call the RTL done

1. Synthesis log shows every memory and DSP you intended, inferred as such.
2. Zero unexplained latch warnings.
3. Register and memory-bit counts match your estimate to within an order of magnitude.
4. Every CDC has both a synchroniser and a constraint.

## Anti-patterns

| Smell | Why it is wrong |
|---|---|
| Memory read inside a conditional | Loses block RAM inference; array becomes flip-flops. |
| Reset on a memory array | Block RAM cannot be reset; forces registers. |
| Handshake logic in the memory `always` block | Perturbs the pattern the inference engine matches. |
| `case` with no `default` | Infers latches. |
| Two-flop synchroniser on a multi-bit bus | Bits arrive on different cycles; the value is corrupt. |
| Blocking assignments in clocked blocks | Simulation/synthesis mismatch. |
| Trusting simulation alone | Simulation cannot show you that a RAM became registers. |

## Vendor reference

Quartus specifics that this skill does not repeat (the full list of log codes and what
each means, editions and licensing, running in a container and on Apple Silicon,
measured compile times, where each output file lands) are in
`../../reference/quartus-toolchain.md`, relative to this file. Read it before quoting a
code, a runtime or a path for Quartus; every figure there came from a real run.
