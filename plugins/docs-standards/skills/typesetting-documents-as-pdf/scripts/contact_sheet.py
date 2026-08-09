#!/usr/bin/env python3
"""Render a PDF to page thumbnails and tile them into contact sheets.

    python3 contact_sheet.py OUT.pdf workdir/ [--cols 5 --rows 3 --dpi 110]

Needs `pdftoppm` (poppler) and Pillow.

Why contact sheets rather than opening pages one at a time: a 25-page document
becomes two images. You can see every page's shape at once, spot the ones that
look wrong (a table running wide, a mostly-empty page, a heading alone at a
foot), and then open just those at full size. Paging through fifty separate
images is the reason "verify the visuals" gets skipped.

IMPORTANT: this deletes previously rendered thumbnails in `workdir/pages/`
before rendering. That is deliberate. Inspecting stale images after a rebuild is
the easiest mistake in this whole workflow — you fix a defect, rebuild, then
look at pictures from the previous build and draw a confident, wrong conclusion.
The script also prints the PDF's modification time and hash so you can confirm
the sheets belong to the build you think they do.
"""
import argparse
import glob
import hashlib
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

try:
    from PIL import Image, ImageDraw
except ImportError:
    sys.exit("Pillow is required: pip install pillow")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("workdir")
    ap.add_argument("--cols", type=int, default=5)
    ap.add_argument("--rows", type=int, default=3)
    ap.add_argument("--dpi", type=int, default=110)
    ap.add_argument("--thumb-width", type=int, default=430)
    a = ap.parse_args()

    pdf = Path(a.pdf)
    work = Path(a.workdir)
    pages = work / "pages"
    if pages.exists():
        shutil.rmtree(pages)
    pages.mkdir(parents=True)

    digest = hashlib.md5(pdf.read_bytes()).hexdigest()[:12]
    mtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(pdf.stat().st_mtime))
    print(f"source : {pdf}")
    print(f"         modified {mtime}, md5 {digest}")

    subprocess.run(["pdftoppm", "-r", str(a.dpi), "-png", str(pdf), str(pages / "p")],
                   check=True)
    files = sorted(glob.glob(str(pages / "p-*.png")))
    print(f"rendered {len(files)} pages at {a.dpi} dpi")

    per_sheet = a.cols * a.rows
    sheets = []
    for start in range(0, len(files), per_sheet):
        chunk = files[start:start + per_sheet]
        ims = []
        for f in chunk:
            im = Image.open(f)
            scale = a.thumb_width / im.width
            ims.append((f, im.resize((a.thumb_width, int(im.height * scale)),
                                     Image.LANCZOS)))
        th = max(i.height for _, i in ims)
        rows = (len(ims) + a.cols - 1) // a.cols
        sheet = Image.new(
            "RGB",
            (a.cols * a.thumb_width + (a.cols + 1) * 8, rows * (th + 22) + (rows + 1) * 8),
            "#d0d0d0")
        d = ImageDraw.Draw(sheet)
        for k, (f, im) in enumerate(ims):
            c, r = k % a.cols, k // a.cols
            x = 8 + c * (a.thumb_width + 8)
            y = 8 + r * (th + 22)
            sheet.paste(im, (x, y + 18))
            d.text((x + 4, y + 4), Path(f).stem.replace("p-", "page "), fill="#000")
        out = work / f"sheet{len(sheets) + 1}.png"
        sheet.save(out)
        sheets.append(out)
        print(f"  {out}  {sheet.size[0]}x{sheet.size[1]}")

    print()
    print("Open these and page through them. Then open any suspicious page at")
    print(f"full size from {pages}/.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
