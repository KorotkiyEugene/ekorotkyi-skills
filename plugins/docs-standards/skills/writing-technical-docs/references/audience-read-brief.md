# The audience read: the whole document once, a verdict per criterion

A brief for the one reader who reads the finished document as the reader its title page
names, before the owner sees it. One fresh agent, the whole built PDF, every page, once. It
runs after the outsider reads of every chapter are applied, never beside them, and its
verdicts are the lines the delivery message carries.

Why a single bounded read: an agent asked to find defects finds defects every time, and
each fresh hunter applies a stricter bar than the last, so a loop of open-ended hunts never
converges. This read has five closed questions and a classification of every residue, so
that it can end.

---

You are the reader the title page names: [THE READER: role, what they must do with the
document, in what setting, with what they have and have not seen; for example «a senior
platform engineer who must deploy and run the service from this document alone, who has not
seen its code and will not open it»]. You read the built PDF once, start to end, every
page, as that reader, and you answer five questions. You are not a hunter: an open-ended
search for defects of every kind is not your task, and a list that grows with every reread
is the failure this read exists to avoid.

The PDF, its page count and the file for your answer are given in the launch message.
Render the pages yourself with `pdftoppm -r 80 -png` into your own directory under the
scratchpad named in the launch message and look at every page image. Use `pdftotext
-layout` for exact quotes.

## The five criteria, one verdict each

1. **Structure.** Each section is the thing its title names, headings are nominal, and
   nothing is in a section that belongs to another. You do not propose a different tree:
   the heading tree is frozen by the owner.
2. **Language.** Every prose sentence is one idea, at most 40 words, with no semicolon and
   no dash. Terms keep their full names where a short form would be an ordinary word out of
   context ([THE DOCUMENT'S FULL-NAME TERMS, listed]). The text reads as one hand's
   professional prose, with no self-narration and no notes to a reviewer.
3. **Facts, as the document presents them.** A fact stated in two places is stated the
   same way in both (a number, a port, a name, a default, a limit). Nothing the document
   itself says was not tested is presented elsewhere as verified. Nothing is asserted that
   the reader would need to check against the source and cannot, with no source line beside
   it.
4. **Form.** The title page is bare. No heading stands at the foot of a page with its text
   on the next. No table is split where the split loses the header. No page ends well above
   its foot without a cause the reader sees (a figure, a rotated page, a chapter end). No
   line is visibly loose.
5. **Completeness.** With this document alone you can do what the title promises: [THE
   TASKS THE TITLE PROMISES, listed in the document's order]. Every value you must set is
   named, every command you must run is printed, and every check tells you what to expect.

## What you write

Write to the file named in the launch message:

1. Five lines, one per criterion: «1 Structure: yes» or «1 Structure: no, page N, "quote"»,
   where the quoted place is the one that decides the verdict. A criterion is «no» only for
   a defect that stops the reader of the title page, not for a blemish.
2. Then the residues, grouped under the criterion they fall under: one line each, document
   page, the sentence or label quoted exactly, a few words on what is wrong. Mark each as
   «decisive» (it made the criterion «no») or «minor». No rewrites: the writer rewrites. No
   taste: a sentence does not fail for its style, its length under 40 words, its citations,
   or because you would have written it differently. No structure proposals.
3. One last line: the number of residues, decisive and minor.

Read once. When the list is written, stop. Change no other file.

---

What the agent running the process does with the answer: a «no» goes back to the one writer with its decisive
residues, and that criterion is read again on the next build; a «yes» with minor residues
goes to the writer once, as classes, and is not read again. The five verdict lines, with
the residue counts and what was done with them, are the delivery's verdict per criterion.
