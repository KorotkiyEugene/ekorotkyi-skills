#!/usr/bin/env python3
"""check_section_refs.py OUT.pdf SRC.md [SRC2.md ...] -- verify hand-typed
section references against the built document.

pandoc-crossref numbers figures, tables and equations for you, but a
reference to a *section* written as "§5.4" is plain text: when a heading
is added, removed or reordered, every such reference silently points at the
wrong section. This script extracts the numbered headings from the PDF's
table of contents (pdftotext -layout) and checks every "§N", "§N.M",
"§N.M.K" (and "Chapter N", "Appendix A") in the Markdown sources against
them. It cannot know what you *meant* a reference to point at; it can tell
you which references point at nothing, and it prints the heading each
existing reference resolves to so you can read the list and spot the ones
that resolve to the wrong heading.

Exit status 1 if any reference has no target.
"""
import re, subprocess, sys

REF = re.compile(r'§\s*([0-9]+(?:\.[0-9]+){0,2}|[A-Z](?:\.[0-9]+){0,2})')
HEAD = re.compile(r'^\s*([0-9]+(?:\.[0-9]+)*|[A-Z](?:\.[0-9]+)*)\s+(\S.*?)\s*(?:(?:\.\s?){3,})?\s*[0-9]+\s*$')


def toc(pdf, pages=8):
    text = subprocess.run(['pdftotext', '-layout', '-f', '1', '-l', str(pages), pdf, '-'],
                          capture_output=True, text=True, check=True).stdout
    heads = {}
    in_toc = False
    for line in text.splitlines():
        if re.match(r'^\s*Contents\s*$', line): in_toc = True; continue
        if re.match(r'^\s*List of (Figures|Tables)', line): in_toc = False
        m = HEAD.match(line)
        if m and in_toc:
            heads.setdefault(m.group(1), m.group(2).strip())
    return heads


def main(argv):
    pdf, srcs = argv[0], argv[1:]
    heads = toc(pdf)
    if not heads:
        print('no numbered headings found in the first pages of', pdf); return 1
    bad = 0; seen = {}
    for src in srcs:
        for ln, line in enumerate(open(src, encoding='utf-8'), 1):
            for m in REF.finditer(line):
                key = m.group(1)
                seen.setdefault(key, []).append(f'{src}:{ln}')
                if key not in heads:
                    parent = key.rsplit('.', 1)[0]
                    if key.count('.') == 2 and parent in heads:
                        heads[key] = f'(a subsection of §{parent} {heads[parent]}, below the ToC depth)'
                    else:
                        bad += 1; print(f'MISSING  §{key}  at {src}:{ln}: {line.strip()[:90]}')
    print(f'\n{len(seen)} distinct section references; {bad} without a target.\n')
    for key in sorted(seen, key=lambda k: [int(x) if x.isdigit() else x for x in k.split('.')]):
        if key in heads:
            print(f'  §{key:<7} -> {heads[key][:60]:<60}  ({len(seen[key])} use{"s" if len(seen[key]) > 1 else ""})')
    print('\nRead the list: a reference that resolves to the wrong heading is not flagged, only shown.')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
