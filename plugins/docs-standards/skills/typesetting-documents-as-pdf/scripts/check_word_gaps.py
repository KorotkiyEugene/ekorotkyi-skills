#!/usr/bin/env python3
"""check_word_gaps.py OUT.pdf [--left-max L] [--right-min R] [--skip-front N]: fail on a justified
line of the body whose spaces between words are wider than a reader accepts.

A loose line is one TeX had to stretch to fill the measure. Its word spaces stand wider than the eye
accepts, though its badness may lie far below the build's \\tolerance: TeX judges badness by the
stretch of the font's spaces, not by their width on the page, and the engine's «Loose lines» warning
names only lines above a badness of 1000. A page reader sees the loose line at once.

Three thresholds, each measured on the page in points:

- MIN_GAP, the median space between the prose words of a line. Over one 200-page document the medians
  ran continuously with no natural break (half the lines at 2.8 pt or less, 99 % at 4.8 pt or less), so
  the threshold was set where a page reader's eye drew it: every line the reader named loose had a
  median of 4.99 pt or more, and the tightest line the reader accepted 4.89 pt. 4.95 pt lies between.
- MEAN_GAP, the mean over every space of the line. The space after a full stop or a colon stretches
  about three times as fast as a word space, so a line whose median passes may still read as loose; the
  reader's loose lines had means of 5.5 pt or more.
- CAPTION_GAP, for a caption's lines but its last: a caption is set smaller and tighter, so it has its
  own norm (3.7 pt, between the loosest caption line accepted and the tightest named loose).

The thresholds depend on the body font and size. For another font, run the script with --report on a
build a page reader has looked at, and set them from that reader's verdicts as above.

What counts as a justified line: a line of four words or more that starts at the text block's left
edge and ends at its right edge, in the body's size. Lines of the contents (dot leaders are words to
pdftotext), table cells, headings, listings and a paragraph's last line reach neither both edges nor
the body's size and are left out. The space between two words of a code span is left out of the
median: it is a character of the monospaced font and never stretches.

It also fails a punctuation mark set PUNCT_GAP or more apart from the prose word before it («cut-off
:»), which a font's italic correction before a colon produces; the fix is in the header (\\nocorrlist).

Needs `pdftotext` (poppler). The geometry defaults suit A4 with 70.9 pt margins; pass --left-max and
--right-min for another page (the left edge of the text block plus a little, and its right edge less
a little). --skip-front N leaves the first N pages (title, contents) out of the punctuation check.
"""
import html
import re
import statistics
import subprocess
import sys

MIN_GAP = 4.95      # pt, median word space of a justified body line
MEAN_GAP = 5.5      # pt, mean over every space of the line, sentence spaces included
PUNCT_GAP = 1.0     # pt, a gap before «:», «;», «)», «,», «.» or «]» that a reader sees
CAPTION_GAP = 3.7   # pt, a caption line's median
LEFT_MAX = 120      # pt, a line starting further right is indented or set in a cell
RIGHT_MIN = 520     # pt, a line ending further left is a paragraph's last line or a cell
BODY_HEIGHT = 11    # pt, a taller first word is a heading
MONO_HEIGHT = 10    # pt, a word box lower than this is the monospaced font (set from your font pair)


def gaps_of(words):
    """The word spaces of a line: a gap with a word of the body's font on at least one side; and, when
    the line holds three or more of them, only the gaps between two words of the prose. A space inside
    a code span never stretches, and a code span's own comma or bracket sits at its edge and would pull
    the median down while the prose words stand apart."""
    mono = [float(w[3]) - float(w[1]) < MONO_HEIGHT for w in words]
    gaps = [float(words[j + 1][0]) - float(words[j][2]) for j in range(len(words) - 1) if not (mono[j] and mono[j + 1])]
    prose = [float(words[j + 1][0]) - float(words[j][2]) for j in range(len(words) - 1)
             if not mono[j] and not mono[j + 1] and not re.search(r"[.:;?!]»?\)?$", html.unescape(words[j][4]))]
    return (prose if len(prose) >= 3 else gaps), gaps


def loose_lines(pdf: str, skip_front: int):
    out = subprocess.run(["pdftotext", "-bbox-layout", pdf, "-"], capture_output=True, text=True, check=True).stdout
    hits, medians, captions = [], [], []
    word_re = r'<word xMin="([0-9.]+)" yMin="([0-9.]+)" xMax="([0-9.]+)" yMax="([0-9.]+)">(.*?)</word>'
    for page, body in enumerate(out.split("<page ")[1:], 1):
        # a caption's lines but its last: a block that opens with «Figure N:» or «Table N:»
        for block in re.findall(r"<block [^>]*>(.*?)</block>", body, re.S):
            lines = [re.findall(word_re, l) for l in re.findall(r"<line [^>]*>(.*?)</line>", block, re.S)]
            first = " ".join(html.unescape(w[4]) for w in lines[0]) if lines and lines[0] else ""
            if re.match(r"(Figure|Table|Рисунок|Таблиця) \d+:", first):
                for words in lines[:-1]:
                    gaps = [float(words[j + 1][0]) - float(words[j][2]) for j in range(len(words) - 1)]
                    if len(gaps) >= 3:
                        median = statistics.median(gaps)
                        captions.append(median)
                        if median >= CAPTION_GAP:
                            hits.append((page, median, " ".join(html.unescape(w[4]) for w in words)))
        for line in re.findall(r"<line [^>]*>(.*?)</line>", body, re.S):
            words = re.findall(word_re, line)
            # a punctuation mark set apart from the prose word before it; only a word of the body's font
            # counts on the left, since pdftotext's boxes of the monospaced font end short of the glyph
            for a, b in zip(words, words[1:]):
                if re.fullmatch(r"[:;),.\]]+", html.unescape(b[4])) and not re.fullmatch(r"\W+", html.unescape(a[4])) \
                        and float(a[3]) - float(a[1]) > MONO_HEIGHT and float(b[0]) - float(a[2]) >= PUNCT_GAP \
                        and page > skip_front:
                    hits.append((page, float(b[0]) - float(a[2]),
                                 f"a gap before «{html.unescape(b[4])}» after «{html.unescape(a[4])}»"))
            if len(words) < 4:
                continue
            if float(words[-1][2]) < RIGHT_MIN or float(words[0][0]) > LEFT_MAX:
                continue
            if float(words[0][3]) - float(words[0][1]) > BODY_HEIGHT:
                continue
            text = " ".join(html.unescape(w[4]) for w in words)
            if ". . ." in text:          # a line of the contents: its dot leaders are not word spaces
                continue
            gaps, every = gaps_of(words)
            if len(gaps) < 3:
                continue
            median = statistics.median(gaps)
            medians.append(median)
            mean = sum(every) / len(every)
            if median >= MIN_GAP or mean >= MEAN_GAP:
                hits.append((page, median if median >= MIN_GAP else mean, text))
    return hits, medians, captions


def main(argv) -> None:
    global LEFT_MAX, RIGHT_MIN
    pdf = argv[1]
    skip_front = int(argv[argv.index("--skip-front") + 1]) if "--skip-front" in argv else 0
    if "--left-max" in argv:
        LEFT_MAX = float(argv[argv.index("--left-max") + 1])
    if "--right-min" in argv:
        RIGHT_MIN = float(argv[argv.index("--right-min") + 1])
    hits, medians, captions = loose_lines(pdf, skip_front)
    if not medians:
        print("check_word_gaps: no justified body line found; check --left-max and --right-min against the page geometry")
        sys.exit(2)
    if "--report" in argv:
        s = sorted(medians)
        print(f"check_word_gaps: {len(s)} justified lines; medians: p50 {s[len(s)//2]:.2f} pt, "
              f"p99 {s[int(len(s)*0.99)]:.2f} pt, p99.9 {s[min(len(s)-1, int(len(s)*0.999))]:.2f} pt, max {s[-1]:.2f} pt")
    print(f"check_word_gaps: {len(medians)} justified lines, the median word gap {statistics.median(medians):.2f} pt; "
          f"{len(captions)} caption lines, their median {statistics.median(captions):.2f} pt; " if captions else
          f"check_word_gaps: {len(medians)} justified lines, the median word gap {statistics.median(medians):.2f} pt; ",
          end="")
    print(f"{len(hits)} at {MIN_GAP} pt or more, or with a mean gap of {MEAN_GAP} pt or more, "
          f"or a caption's at {CAPTION_GAP} pt or more")
    for page, median, text in hits:
        print(f"   *** page {page}: {median:.2f} pt between words: {text[:90]}")
    if hits:
        print("   Set the paragraph so that the line tightens: a non-breaking space or a hyphenation hint first,\n"
              "   a recast of the sentence only where the setting cannot do it.")
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv)
