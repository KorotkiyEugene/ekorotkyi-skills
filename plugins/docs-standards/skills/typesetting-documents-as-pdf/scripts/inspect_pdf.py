#!/usr/bin/env python3
"""Check a typeset PDF for the defects a successful build hides.

    python3 inspect_pdf.py OUT.pdf [--page-width 595.28] [--margin 70.9]

Needs `pdftotext` (poppler) on PATH.

Four checks, each catching a different class:

1. OVERFLOW. The rightmost text position on each page, against where the text
   block ends. Two things look alike in these numbers and must not be confused:
   microtype's deliberate character protrusion is about 2 pt and is correct
   typography, while anything beyond a few points is text running into the
   margin or off the paper.

2. DASH CENSUS. In a document full of file paths, an en-dash (U+2013) where a
   hyphen (U+002D) belongs means the paths are corrupted and no longer
   copy-pasteable. A few en-dashes are normal (page ranges); a lot are not.

3. QUOTE CENSUS. Opening (U+201C) and closing (U+201D) quotes should roughly
   balance. A large imbalance is the classic symptom of a Markdown source
   written with ASCII quotes converted without a "smart" typography pass, which
   turns every quote into a closing one.

4. ORPHANED HEADINGS. A page whose last content line is a heading has left that
   heading stranded from the material it introduces.

None of this replaces looking at the pages. It finds what can be counted; it
cannot see a diagram rendered as tofu or a caption that drifted from its figure.
Use contact_sheet.py for that.
"""
import argparse
import re
import subprocess
import sys
from collections import Counter

DASHES = {0x2D: "hyphen-minus", 0x2010: "hyphen", 0x2012: "figure dash",
          0x2013: "en dash", 0x2014: "em dash", 0x2212: "minus sign"}
QUOTES = {0x22: "straight double", 0x27: "straight single",
          0x2018: "left single", 0x2019: "right single",
          0x201C: "left double", 0x201D: "right double"}
HEADING = re.compile(r"^\s*\d+(\.\d+)*\.?\s+[A-Z]")
PAGENUM = re.compile(r"^\s*\d+\s*$")


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True).stdout


def preflight(pdf: str) -> None:
    """Fail loudly rather than reporting a clean bill of health for nothing.

    This exists because the script did the opposite. Given a path that did not
    exist, every check found nothing to complain about, so it printed four OKs
    and exited 0 -- indistinguishable from a perfect document. A verification
    tool that reports success when it has verified nothing is worse than no
    tool, because it manufactures exactly the false confidence this skill is
    written to prevent. It was hit in real use, from the wrong directory.
    """
    from pathlib import Path
    import shutil

    if shutil.which("pdftotext") is None:
        sys.exit("inspect_pdf: pdftotext not found on PATH (install poppler)")
    p = Path(pdf)
    if not p.exists():
        sys.exit(f"inspect_pdf: no such file: {pdf}")
    if not p.is_file():
        sys.exit(f"inspect_pdf: not a file: {pdf}")
    if p.stat().st_size == 0:
        sys.exit(f"inspect_pdf: file is empty: {pdf}")
    if p.read_bytes()[:5] != b"%PDF-":
        sys.exit(f"inspect_pdf: not a PDF (no %PDF- header): {pdf}")


def check_overflow(pdf, page_w, margin):
    bbox = run(["pdftotext", "-bbox", pdf, "-"])
    page, worst = 0, {}
    for line in bbox.split("\n"):
        if "<page" in line:
            page += 1
        m = re.search(r'xMax="([\d.]+)"', line)
        if m:
            worst[page] = max(worst.get(page, 0.0), float(m.group(1)))
    block_end = page_w - margin
    rows = [(p, x - block_end) for p, x in sorted(worst.items())]
    return block_end, rows


def check_orphans(pdf, skip_pages):
    layout = run(["pdftotext", "-layout", pdf, "-"])
    out = []
    for n, page in enumerate(layout.split("\f"), 1):
        if n <= skip_pages:
            continue
        lines = [l for l in page.split("\n") if l.strip()]
        if len(lines) < 2:
            continue
        last, prev = lines[-1], lines[-2]
        # a heading never ends in sentence punctuation; a body line that happens to start with a number does
        if PAGENUM.match(last) and HEADING.match(prev) and not prev.rstrip().endswith((".", ",", ";", ":", ")")):
            out.append((n, prev.strip()[:70]))
    return out


def census(pdf, table):
    text = run(["pdftotext", pdf, "-"])
    c = Counter(ord(ch) for ch in text if ord(ch) in table)
    return c


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--page-width", type=float, default=595.28, help="pt (A4 default)")
    ap.add_argument("--margin", type=float, default=70.9, help="pt (25 mm default)")
    ap.add_argument("--protrusion-ok", type=float, default=4.0,
                    help="pt past the text block still considered microtype protrusion")
    ap.add_argument("--skip-front", type=int, default=0,
                    help="leading pages to skip in the orphan check (title/TOC)")
    a = ap.parse_args()

    preflight(a.pdf)

    problems = 0

    block_end, rows = check_overflow(a.pdf, a.page_width, a.margin)
    if not rows:
        sys.exit(f"inspect_pdf: extracted 0 pages from {a.pdf}. The file is a PDF "
                 "but no text came out of it -- a scanned image, an encrypted "
                 "file, or a broken build. Nothing below would have been checked, "
                 "so this is a failure and not a clean result.")
    bad = [(p, d) for p, d in rows if d > a.protrusion_ok]
    worst = max((d for _, d in rows), default=0.0)
    print(f"1. OVERFLOW  text block ends at {block_end:.1f} pt, paper at {a.page_width:.1f} pt")
    print(f"   max protrusion {worst:.2f} pt over {len(rows)} pages")
    if bad:
        problems += 1
        print(f"   *** {len(bad)} page(s) past the {a.protrusion_ok:g} pt threshold:")
        for p, d in bad:
            off_paper = " OFF THE PAPER" if d + block_end > a.page_width else ""
            print(f"       page {p:3d}  +{d:.1f} pt{off_paper}")
    else:
        print(f"   OK (<= {a.protrusion_ok:g} pt is microtype character protrusion)")

    print()
    d = census(a.pdf, DASHES)
    print("2. DASHES   " + ", ".join(f"{DASHES[k]} x{v}" for k, v in sorted(d.items())))
    en, hy = d.get(0x2013, 0), d.get(0x2D, 0)
    if hy and en > max(10, hy * 0.05):
        problems += 1
        print(f"   *** {en} en-dashes against {hy} hyphens: check that no file path was")
        print("       rewritten with en-dashes, which would make paths uncopyable")
    else:
        print("   OK")

    print()
    q = census(a.pdf, QUOTES)
    print("3. QUOTES   " + ", ".join(f"{QUOTES[k]} x{v}" for k, v in sorted(q.items())))
    lo, ro = q.get(0x201C, 0), q.get(0x201D, 0)
    if (lo + ro) and abs(lo - ro) > 0.25 * (lo + ro):
        problems += 1
        print(f"   *** opening {lo} vs closing {ro}: strongly unbalanced.")
        print("       If the source used ASCII quotes, enable smart typography.")
    else:
        print("   OK")

    print()
    orph = check_orphans(a.pdf, a.skip_front)
    print("4. ORPHANED HEADINGS")
    if orph:
        problems += 1
        for p, h in orph:
            print(f"   *** page {p}: {h}")
        print("       With titlesec: \\usepackage[nobottomtitles*]{titlesec} and")
        print("       \\renewcommand{\\bottomtitlespace}{0.22\\textheight}.")
        print("       \\Needspace does not work through titlesec.")
    else:
        print("   none")

    print()
    print("NOW LOOK AT THE PAGES. These checks find what can be counted; they")
    print("cannot see tofu glyphs, unreadably narrow columns, or a drifted caption.")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
