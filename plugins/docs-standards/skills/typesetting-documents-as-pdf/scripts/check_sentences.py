#!/usr/bin/env python3
"""check_sentences.py SRC.md [--max-words N]: every prose sentence of the source is short and holds
no semicolon.

The rule it keeps: one idea per sentence, about 25 words, never more than MAX_WORDS, and no clause
chained to another by a semicolon. A reader takes a sentence of 25 words at once and a sentence of 60
not at all, and the sentence that fails is the one whose clauses a semicolon chained and whose «it» has
no clear noun. The sweep that fixes such a text is a rewrite of every long sentence into two; this
check keeps the result from eroding.

What it reads: the paragraphs and the list items of the Markdown source. It skips fenced blocks (code,
listings, raw LaTeX), table rows, headings, figure lines, `{{…}}` directives that stand on a line of
their own, and a «Sources:» clause to the end of its paragraph (the convention of a citation line at a
paragraph's end). Inside a sentence it blanks what is not the document's own prose: a code span, a «…»
quotation (a screen text, a log line, the name of a part), a gloss in parentheses («("sign out")») and
a parenthesis that holds only citations or references (a file with line numbers, «section «…»»,
«figure …»). A blanked span counts as one word.

It fails on a sentence of more than MAX_WORDS words, and on a semicolon anywhere in the prose, a list
item's last character included: a semicolon that ends a list item is a semicolon in prose too. A
semicolon inside a blanked span passes (a table cell may list with semicolons; a command may hold
one). Exits 1 and prints each offender with its line; exits 0 with the counts and the longest sentence.

A sentence may begin with a tool's name in lower case («psql answers …»): such a name after a full
stop starts a sentence as a capital does, so that two sentences are not counted as one. Add the tools
your document names to TOOLS.
"""
import re
import sys

# The longest sentence allowed, in words. A sentence of about 25 words reads at once; 40 leaves room for
# a sentence that needs a short list or a definition inside it; anything longer is two ideas.
MAX_WORDS = 40

# Tools whose names open a sentence in lower case in your document.
TOOLS = r"(?:psql|pg_dump|pg_restore|kubectl|docker|npm|npx|node|openssl|curl|git|grep|sed|awk|make|cargo|pip)\b"

# A parenthesis that holds only a citation or a reference: a file name with an extension and optional
# line numbers, or a named part of the document.
CITATION = re.compile(
    r"\(\s*(?:[^()]*?(?:\w[\w./@-]*\.(?:tsx?|m?js|json|md|sql|ya?ml|txt|sh|py|lua|tex|c|h|cpp|rs|go|java|v|sv)"
    r"(?::[\d, -]+)?|\b(?:sections?|chapters?|appendix|appendices|rows?|figures?|tables?|items?|steps?)\s+[«`\\\d])"
    r"[^()]*)\)")


def blank(s: str) -> str:
    s = re.sub(r"`[^`]*`", " X ", s)
    while True:
        n = re.sub(r"«[^«»]*»", " X ", s)
        if n == s:
            break
        s = n
    s = re.sub(r"\(\"[^\"]*\"[^()]*\)", " X ", s)          # a gloss: ("sign out")
    while True:
        n = CITATION.sub(" X ", s)
        if n == s:
            break
        s = n
    s = re.sub(r"\{\{[^}]*\}\}", " X ", s)
    s = re.sub(r"\^\[", " ", s)                              # a footnote's text reads as prose of its own
    s = re.sub(r"\\ref\{[^}]*\}|\{=latex\}", " ", s)
    s = re.sub(r"\*\*|\*", "", s)
    return s


# A full stop ends a sentence when a space and a capital, a digit, a quotation, a code span or a tool's
# name that the document writes in lower case follow, and the word before it is no abbreviation.
ABBREV = re.compile(r"(?:\be\.g|\bi\.e|\bvs|\betc|\bcf|\bNo|\bst|\bDr|\bMr)$")


def sentences(text: str):
    start = 0
    for m in re.finditer(r"[.?!](?=\s+(?:[A-Z0-9«X\"(]|" + TOOLS + r"|$))|[.?!]$", text):
        if ABBREV.search(text[start:m.start()]):
            continue
        yield text[start:m.end()].strip()
        start = m.end()
    rest = text[start:].strip()
    if rest:
        yield rest


def paragraphs(lines):
    """(line number, text) of every paragraph and list item of prose."""
    buf, at, fence = [], 0, False

    def flush():
        nonlocal buf
        if buf:
            yield at, " ".join(buf)
        buf = []

    for i, line in enumerate(lines, 1):
        s = line.strip()
        if s.startswith("```"):
            yield from flush()
            fence = not fence
            continue
        if fence:
            continue
        item = re.match(r"^\s*(?:[-*]|\d+\.|\([a-z]\))\s+", line)
        directive = re.fullmatch(r"\{\{[^}]*\}\}", s)        # a line that is one directive, not a sentence
        if not s or s.startswith(("|", "#", "![")) or directive or item:
            yield from flush()
            if item and s:
                buf, at = [line[item.end():].strip()], i
            continue
        if not buf:
            at = i
        buf.append(s)
    yield from flush()


def main(argv) -> int:
    global MAX_WORDS
    path = argv[1]
    if "--max-words" in argv:
        MAX_WORDS = int(argv[argv.index("--max-words") + 1])
    lines = open(path, encoding="utf-8").read().split("\n")
    problems, count, longest = [], 0, (0, 0, "")
    for at, text in paragraphs(lines):
        clean = re.split(r"\bSources:", blank(text))[0]     # after blanking: «Sources:» inside a quotation stays
        for sent in sentences(clean):
            words = len(sent.split())
            if words == 0 or sent == "X":
                continue
            count += 1
            if words > longest[0]:
                longest = (words, at, sent)
            if words > MAX_WORDS:
                problems.append(f"line {at}: {words} words: {sent[:160]}…")
            if ";" in sent.rstrip():
                problems.append(f"line {at}: a semicolon: {sent[:160]}…")
    for p in problems:
        print(f"check_sentences: {p}", file=sys.stderr)
    if problems:
        print(f"check_sentences: {len(problems)} problems in {count} sentences (at most {MAX_WORDS} words, no semicolon)",
              file=sys.stderr)
        return 1
    print(f"check_sentences: {count} sentences, none longer than {MAX_WORDS} words and none with a semicolon; "
          f"the longest, {longest[0]} words, at line {longest[1]}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
