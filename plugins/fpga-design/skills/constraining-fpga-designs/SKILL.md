---
name: constraining-fpga-designs
description: >-
  Timing constraints for FPGA and ASIC projects — SDC/XDC files, clock definitions,
  I/O delays, false and multicycle paths, clock-domain-crossing exceptions, and pin
  location assignments. Use this skill whenever you CREATE a new FPGA project, ADD
  a source file to one, RUN a synthesis/place-and-route flow, or TOUCH anything about
  timing — in Quartus, Vivado, Libero, Diamond, iCEcube, or any other EDA tool.
  Trigger on "set up a Quartus/Vivado project", "compile this design", "synthesise
  this", "add an SDC", "constrain the clock", "why is timing failing", "what Fmax do
  we get", "the fitter placed it badly", "make the build reproducible", or any request
  to build an FPGA design where no .sdc/.xdc exists yet. ALSO trigger when reviewing
  someone else's project for missing constraints.
---

# Constraining FPGA Designs

**Never build an FPGA project without constraints.** Not for a quick test, not for
a throwaway experiment, not "just to see if it fits". An unconstrained build is not
a faster build — it is a build whose result means nothing.

## Why this is a hard rule

EDA tools do not fail when constraints are missing. They warn, invent something, and
report success. Quartus, for example:

```
Critical Warning (332012): Synopsys Design Constraints File file not found: 'top.sdc'.
  ... Without it, the Compiler will not properly optimize the design.
Info (332144): No user constrained base clocks found in the design
Info (332142): ... Calling "derive_clocks -period 1.0"
Info (332130): Timing requirements not specified -- quality metrics such as
  performance may be sacrificed to reduce compilation time.
```

It fabricates a **1 ns (1 GHz)** clock, then reports "Timing requirements not met" —
which is meaningless, because nothing asked for 1 GHz. The placer and router had no
objective, so the placement is arbitrary. The build says *Successful*.

Everything downstream is then worthless: the Fmax number, the resource counts after
optimisation, the floorplan, any comparison against another build. You cannot tell a
design that fails timing from one that was never asked to meet it.

## The minimum every project needs

Create the constraint file **before the first compile**, not after the first failure.

### 1. A clock for every clock

```tcl
create_clock -name clk -period 20.000 [get_ports {clk}]
```

Period in nanoseconds. Every primary clock input needs one. Clocks generated on-chip
(PLL/MMCM outputs, divided clocks) need `create_generated_clock`, or must be derived
automatically — in Quartus `derive_pll_clocks` does this for PLL outputs.

An unconstrained clock is worse than a slow one: paths in its domain are simply not
analysed.

### 2. Clock uncertainty

```tcl
derive_clock_uncertainty
```

Must come *after* every `create_clock`. This budgets jitter and PLL uncertainty. Without
it the tool optimises against an ideal clock that no board provides.

### 3. I/O timing

```tcl
set_input_delay  -clock clk -max 4.000 [get_ports {data_in[*]}]
set_input_delay  -clock clk -min 1.000 [get_ports {data_in[*]}]
set_output_delay -clock clk -max 5.000 [get_ports {data_out[*]}]
set_output_delay -clock clk -min -1.000 [get_ports {data_out[*]}]
```

Unconstrained I/O paths are not analysed at all. If you genuinely do not know the
external timing, budget a fraction of the period and say so in a comment — a stated
assumption is reviewable, silence is not.

### 4. Exceptions, stated deliberately

```tcl
# Asynchronous reset: released with no defined phase relationship to clk.
set_false_path -from [get_ports {resetn}]
```

Only cut a path you can justify in one sentence. `set_false_path` on something that is
actually timed hides a real failure. Multicycle paths need the same discipline:

```tcl
set_multicycle_path -setup 2 -from [get_cells {slow_reg*}] -to [get_cells {dst_reg*}]
set_multicycle_path -hold  1 -from [get_cells {slow_reg*}] -to [get_cells {dst_reg*}]
```

A `-setup` multicycle without a matching `-hold` is a classic silent bug: it relaxes
setup and leaves hold analysed at the wrong edge.

### 5. Pin locations

Unassigned pins are re-picked on every fit, so two builds of the same source are not
comparable and a board build is a coin toss. Quartus flags this:

```
Critical Warning (169085): No exact pin location assignment(s) for 11 pins
```

Assign every port a location, even for a reference build with no board — pick the ones
the fitter chose and freeze them, so the build becomes reproducible.

## Clock domain crossings

Every CDC needs *both* a synchroniser in RTL and a constraint telling the tool not to
time the crossing. The constraint alone is a lie; the synchroniser alone leaves the
tool trying to close timing on a path that cannot close.

```tcl
set_false_path -from [get_clocks clk_a] -to [get_clocks clk_b]
```

Prefer scoping to the specific crossing registers over blanket clock-to-clock cuts —
a blanket cut also hides genuine paths you did not intend to cross domains.

## Wiring it into the project

The constraint file must be *referenced*, not merely present:

```tcl
# Quartus (.qsf)
set_global_assignment -name SDC_FILE top.sdc
```

A `.sdc` sitting in the directory that nothing includes is the same as no `.sdc`, and
the 332012 warning still fires. Check it.

## Before you call the build done

Verify the constraints actually took effect rather than assuming they did. See the
**verifying-fpga-builds** skill for the full gate; the constraint-specific part is:

- No 332012 / 332144 / 332130 / 332142 / 169085 (Quartus) or equivalent.
- Every clock you defined appears in the timing report.
- Setup **and** hold slack are positive, with TNS 0.
- The reported Fmax is against *your* constraint, not a derived one.

## Anti-patterns

| Smell | Why it is wrong |
|---|---|
| "It's just a quick test build" | The result cannot be compared to anything, so the test answers nothing. |
| Adding the SDC after timing fails | The placement is already fixed by an arbitrary objective; rerun the fit. |
| `set_false_path` to make a warning go away | Hides a real path. Cut only what you can justify. |
| `-setup` multicycle with no `-hold` | Relaxes setup, leaves hold checked at the wrong edge. |
| Constraining only the fast clock | Unconstrained domains are not analysed at all. |
| `.sdc` present but not in the project file | Identical to having no constraints. |
