---
name: verifying-fpga-builds
description: >-
  How to tell whether an FPGA build actually succeeded, rather than merely reporting
  success — reading synthesis and place-and-route logs, the warning codes that mean
  failure, checking inferred resources against expectation, and gating on timing slack.
  Use this skill AFTER running any synthesis, fitter, place-and-route, or bitstream
  flow in Quartus, Vivado, Libero, Diamond or similar, and whenever interpreting their
  reports. Trigger on "compile finished", "the build succeeded", "did it fit", "check
  the report", "why is it using so many LUTs/ALMs/registers", "timing failed", "what
  Fmax", "the design got huge", "is this build good", "review the synthesis log", or
  any moment where a tool said Successful and that claim is about to be believed.
---

# Verifying FPGA Builds

**"0 errors" is not success.** FPGA tools report success while doing something quite
different from what was asked. The build log is evidence; read it before believing the
status line.

## The one rule that matters most

**Check the numbers against what you expected before looking at anything else.** If a
design you estimated at 2,000 logic cells comes out at 98,000, no amount of "0 errors"
makes that a good build. Form the expectation *first* — order of magnitude is enough —
then compare.

This catches the failure mode that warnings do not: the tool did exactly what you wrote,
and what you wrote was not what you meant.

## The gate

Run all four checks. A build passes only if all four pass.

### 1. Constraint warnings are failures, not warnings

In Quartus, these mean the build has no valid timing objective:

| code | meaning |
|---|---|
| `332012` | SDC file not found — the tool invented `derive_clocks -period 1.0` |
| `332144` | No user-constrained base clocks found |
| `332142` | Falling back to derived clocks |
| `332130` | Timing requirements not specified; "quality metrics may be sacrificed" |
| `169085` | No exact pin location assignments — placement is not reproducible |

Any of these present ⇒ the build is void, regardless of status. Fix the constraints and
rerun the fit; do not interpret the results. See **constraining-fpga-designs**.

Vivado's equivalents are the methodology checks (`report_methodology`) and
`check_timing` — an empty `check_timing` report is the goal, and unconstrained
`no_clock` / `no_input_delay` / `no_output_delay` entries are the same class of defect.

### 2. Resources match expectation

Compare the report against what the design should cost:

- **Registers** ≈ the flip-flops you actually wrote. A large excess usually means a
  memory or shift register was built from logic instead of a hard block.
- **Block memory bits** ≈ the memories you declared. Near-zero when you expected
  kilobits means inference silently failed.
- **DSP blocks** — zero when you wrote multipliers means they went into fabric.
- **Logic cells / LUTs / ALMs** — the headline number, and the one worth an order-of-
  magnitude sanity check.

A worked example: a small RISC-V SoC with 8 KB of RAM reported

```
Total registers          : 66794      <- expected ~1,300
Total block memory bits  : 2,304      <- expected ~67,000
Implemented 98169 logic cells         <- expected ~2,400
```

Every one of those is a red flag pointing at the same cause: the RAM had been built out
of flip-flops. The fix was one line of RTL. The build had reported *0 errors*.

### 3. Inference actually happened

Search the synthesis log for what the tool inferred, and confirm it matches intent:

```
Info (19000): Inferred 2 megafunctions from design logic
Info (276029): Inferred altsyncram megafunction from ... "cpuregs_rtl_0"
```

If a memory you declared is *absent* from that list, it was not inferred. Quartus also
emits `Warning (276020)` when it adds pass-through logic to match read-during-write
behaviour — benign, but it tells you which arrays became RAM.

See **writing-synthesizable-rtl** for the coding patterns that make inference work.

### 4. Timing closes, with margin

- Setup slack **positive**.
- Hold slack **positive** — hold is checked less often and fails just as hard.
- TNS (total negative slack) **zero**.
- Fmax comfortably above the constraint. Meeting 50 MHz at Fmax 50.1 MHz is not closure;
  it is a design that will fail on the next revision, corner, or temperature.
- Check the **slow** corner, and the fast corner for hold.

## Reproducibility

Two builds of identical sources must produce identical results. If they do not,
something is unconstrained — usually pin locations or a seed-dependent placement.
Freeze what varies before drawing conclusions from a comparison.

## Reading a report honestly

- **"ALMs needed" ≠ "ALMs used in final placement"** — the fitter reports both, plus an
  estimate of what dense packing could recover. Quote the one you mean.
- **Utilisation percentages hide absolutes.** "1%" of a large device is still thousands
  of cells, and still worth checking against expectation.
- **A tool's summary is a claim, not a measurement.** When a number matters, find the
  detailed table it came from.

## Anti-patterns

| Smell | Why it is wrong |
|---|---|
| Reporting "compiled successfully" with no numbers | Success status says nothing about whether the design is right. |
| Skimming past Critical Warnings | In Quartus these routinely mean the build is void. |
| Accepting resource counts without an expectation | The most expensive bugs pass every warning check. |
| Quoting Fmax from an unconstrained build | It is measured against a fabricated clock. |
| Checking setup slack only | Hold violations are unfixable in the field. |
| Comparing two builds where pins were auto-placed | The placements are not comparable. |
