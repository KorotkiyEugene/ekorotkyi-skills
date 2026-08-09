#!/usr/bin/env python3
"""Measure a Markdown source for the three things that decide page geometry.

Run this before writing a header, not after discovering a problem twenty pages in:

    python3 measure_source.py DOC.md

Reports:
  * the widest line inside a fenced code block, which sets the monospace size;
  * the widest table row, which decides whether columns must wrap and whether
    anything needs a landscape page;
  * whether Unicode box-drawing characters are used, which constrains the
    monospace font to one that covers U+2500-U+257F.

The monospace size suggestion assumes an advance width of 0.6 em, which is close
enough for Menlo (0.6018), DejaVu Sans Mono (0.6023) and most terminal faces to
be a useful starting point. Verify by rendering; this is arithmetic, not proof.
"""
import re
import sys
from pathlib import Path

BOX_DRAWING = range(0x2500, 0x2580)
PT_PER_MM = 72 / 25.4


def measure(path: Path):
    lines = path.read_text(encoding="utf-8").split("\n")
    in_fence = False
    fence_max = (0, 0, "")
    table_max = (0, 0, "")
    box_lines = []

    for n, line in enumerate(lines, 1):
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if any(ord(c) in BOX_DRAWING for c in line):
            box_lines.append(n)
        if in_fence:
            if len(line) > fence_max[0]:
                fence_max = (len(line), n, line)
        elif line.lstrip().startswith("|"):
            if len(line) > table_max[0]:
                table_max = (len(line), n, line)

    return lines, fence_max, table_max, box_lines


def suggest_size(cols: int, text_block_mm: float) -> float:
    """Largest monospace size at which `cols` characters fit `text_block_mm`."""
    if cols == 0:
        return 0.0
    return (text_block_mm * PT_PER_MM) / (cols * 0.6)


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    path = Path(sys.argv[1])
    # A4 with 25 mm margins by default; pass a second argument to override.
    block_mm = float(sys.argv[2]) if len(sys.argv) > 2 else 160.0

    lines, fence, table, box = measure(path)

    print(f"{path}: {len(lines)} lines")
    print()
    print(f"widest fenced line : {fence[0]} chars  (line {fence[1]})")
    if fence[2]:
        print(f"    {fence[2][:100]}")
    if fence[0]:
        s = suggest_size(fence[0], block_mm)
        print(f"    break-even monospace size for a {block_mm:g} mm text block: {s:.2f} pt")
        print(f"    -> choose one step smaller for headroom, and NEVER enable line")
        print(f"       breaking in verbatim if the fences contain diagrams")
    print()
    print(f"widest table row   : {table[0]} chars  (line {table[1]})")
    if table[0] > 200:
        print("    -> wrapping columns are mandatory; consider a landscape page")
    elif table[0] > 0:
        print("    -> wrapping columns still recommended")
    print()
    if box:
        print(f"box-drawing chars  : YES, on {len(box)} lines (first at line {box[0]})")
        print("    -> the monospace font MUST cover U+2500-U+257F.")
        print("       Menlo, DejaVu Sans Mono and most terminal fonts do.")
        print("       Without coverage you get tofu boxes or dropped glyphs.")
    else:
        print("box-drawing chars  : none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
