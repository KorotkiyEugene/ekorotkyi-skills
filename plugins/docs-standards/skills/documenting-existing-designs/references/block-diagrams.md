# Block diagrams of an existing hardware design

Rules for a top-level or module-level block diagram that documents RTL someone else wrote.
They were learned from rounds of review on a real 48-instance FPGA top level; each rule
exists because its absence was rejected.

## Content comes from the netlist

- **Derive connectivity from the source**, never from a previous drawing. A block that was
  drawn with no inputs because the earlier version had none is the most common error.
- **Generate the diagram from a script** that carries the complete connection table, and
  make the script **fail** when any block is drawn unconnected or a required link is
  absent. Keep the audit in sync with every edit.
- **Verify content before rendering.** Check that every instance in the top level appears
  in exactly one block and every module-to-module link is a wire. Only then export and
  look at the picture.

## One box per instance, one box per part

- A block is one module instance: bold module name, italic instance name, nothing else.
  Connectivity lives in wires, wire labels and the legend, not in box text.
- Never collapse instances into "×N". The only permitted collapse is a true lane array
  (identical copies on slices of one bus), declared in the legend and in the build output.
- Off-chip devices: one box per physical part, drawn once. A part that serves several
  sections spans them or is reached by a wire routed around the margin; it is never
  duplicated.
- Every pin group has its off-chip source or sink drawn. Where the part is not documented,
  draw a generic device ("10 MHz reference"); never invent a specific part number.

## Non-components are not boxes

- Pin groups are small pads on the boundary where the wire crosses, with the pin names as
  plain text beside them.
- Clock and reset nets are net flags or domain cards, not component boxes. A clock card
  states its consumers ("drives every blue-filled block") and its frequency with the
  derivation.
- The design boundary (FPGA frame, chip edge, process boundary) is drawn explicitly; logic
  inside, devices outside.

## Every link is drawn

- Point-to-point links are wires. A multi-drop bus is a real trunk with junction dots
  teeing into each consumer; stub flags at consumers are not acceptable.
- No note-only links. If two modules exchange data or monitoring signals, there is a wire.
  Inline glue (status aggregation assigns) is its own drawn block.
- A wire may overlay another wire's segments exactly and branch with a junction dot.
- Anything deliberately not drawn (clock and reset fan-out, debug taps, status-word
  members) is a declared class, printed by the build and stated in the legend, never
  omitted silently.

## Encodings

- Fill colour = clock domain, defined by domain cards or a legend table before first use.
  Never let another encoding dim the fill (no opacity for "source missing").
- Border = source availability: solid for read source, dashed for absent. Two states only.
- Dual-clock blocks: hard split fill with zig-zag boundary marks, not a dot, not a gradient.
- Every visual encoding in use (shape, border, fill, wire weight, dashes, junctions,
  jumps) is explained in the legend. If it is not in the legend, it is not in the diagram.

## Geometry

- One global column grid and one row pitch; gutters wide enough for bus labels between
  boxes. Never place boxes ad hoc.
- Flow is left-to-right in every section. Long returns go through strip gaps and symmetric
  bus corridors, never by reversing flow.
- Every wire lane keeps about 20 px clearance from any block edge; no bend within about
  20 px of an endpoint; line jumps (arcs) where a crossing is unavoidable.
- Every wire exit and entry is computed so wires are exactly horizontal or vertical.

## Deliverable shape

- A full-detail sheet on an auto-fit page (`standalone` class in LaTeX/TikZ, or an
  editable master such as draw.io) plus a coarser A4 overview in the report. Both from one
  style file and one connection table so they cannot diverge.
- Render with the real tool (`pdftoppm` for PDF, the draw.io CLI for `.drawio`), inspect
  the full page and 2 to 3× crops, and re-render after every rebuild; never inspect stale
  images.
