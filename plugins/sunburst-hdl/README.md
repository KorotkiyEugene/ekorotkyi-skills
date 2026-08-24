# sunburst-hdl

Verilog/SystemVerilog design discipline distilled from Clifford E. Cummings'
award-winning Sunburst Design conference papers. Every skill was authored from
a full read of its source papers; each was validated by a RED/GREEN process:
a baseline agent solved a representative task *without* the skill (failures
recorded), the skill was written to target those failures, and the same task
was re-run *with* the skill and verified (including real Icarus/Verilator runs
where applicable).

## Skills

| Skill | Source papers (award) |
|---|---|
| `avoiding-verilog-races` | Nonblocking Assignments... Coding Styles That Kill! (SNUG-2000, 1st); NBA With Delays, Myths & Mysteries (SNUG-2002, 2nd); SystemVerilog Event Regions (SNUG-2006, w/ Salz) |
| `designing-async-fifos` | Async FIFO Design (FIFO1, SNUG-2002); Async Pointer Comparisons (FIFO2, SNUG-2002, 1st) |
| `crossing-clock-domains` | CDC Design & Verification Techniques (SNUG-2008, 1st); Multi-Asynchronous Clock Designs (SNUG-2001, 3rd) |
| `coding-fsms` | FSM Design & Synthesis Part I (SNUG-2019, 1st); FSM Fundamentals (ICU-2002, 2nd); SystemVerilog 3.0 FSM (SNUG-2003, 2nd); Glitch-Free FSM Outputs (SNUG-2000 Boston, 2nd) |
| `coding-case-statements` | full_case parallel_case, the Evil Twins (SNUG-1999, 1st) |
| `using-sv-processes-and-ports` | Logic Specific Processes (SNUG-2016, 2nd); Implicit Port Enhancements (SNUG-2007, 1st) |
| `writing-designer-sva` | SVA Design Tricks & Bind Files (SNUG-2009, 1st); SVA Bindfiles & Best Known Practices (SNUG-2016, 1st) |
| `speeding-up-simulation` | Verilog Coding Styles for Simulation Efficiency (ICU-1997, 1st); Yikes! Why is My SystemVerilog Still So Slooooow? (DVCon-2019, 1st, w/ Rose & Sherer) |

Papers: originally at sunburst-design.com/papers (now paradigm-works.com
technical library; archived copies via the Wayback Machine).

## Relation to other plugins

Complements `fpga-design` (constraints discipline, build verification, generic
synthesizable-RTL patterns). Where naming/formatting conventions conflict with
a project style guide (e.g. lowRISC), the project style guide wins on
naming/formatting; these skills win on semantic rules (assignment discipline,
CDC structure, case-statement safety).
