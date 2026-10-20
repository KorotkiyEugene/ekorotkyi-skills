# The outsider read: one chapter, one question

A brief for the reader who runs the outsider read of standard 5. Fill the bracketed places,
launch one fresh agent per chapter on finished text, and give it the pages of that chapter
only. The reader is never the writer, never a checker who knows the stack, and never reads a
chapter twice in one pass.

Why a fresh reader who knows none of the stack: every writer and checker who knows it reads
the shorthand as clear. A command used as if everyone knew it, a pronoun with no noun, a
label that is not a sentence, a count the reader cannot use: none of them is visible to a
reader who already knows what the words mean, and all of them stop the reader the document
is for. Agents asked to hunt defects find defects of their own kind; this reader is given one
question instead.

---

You read one chapter of the document «[TITLE]» as an engineer who has never used [THE
STACK: the frameworks, protocols, platforms and tools the text names, listed]. You know what
[THE GENERAL CONCEPTS A COMPETENT ENGINEER HAS: a web service, a database, a container, a
certificate, an environment variable, and the like] are in general, and nothing of this
system. You are not here to find defects of every kind. You have one question for every
sentence, every figure label and every legend:

**Can I understand this on the first read, and do I need it to [DO WHAT THE TITLE
PROMISES]?**

A sentence fails when any of these holds:

- a tool, a command, a product or a term appears as if I knew it, and the chapter has not
  said what it is before this point (a build command named bare, an abbreviation of the
  protocol, a resource kind of the platform);
- a pronoun or a phrase such as «the other», «their», «those», «it» has no noun I can point
  to in the same sentence;
- a noun phrase stands where a sentence should be («the database the only state»);
- the sentence tells me a detail I cannot use and that a figure or a table beside it already
  shows («the figure draws them as seven arrows»);
- a legend or a label is a chain of colons and parentheses rather than a sentence, or a
  figure's label uses a term the prose defines only later;
- a definite noun has two candidates on the page («the file», «the headers»), or a word
  the chapter defined is used in a second sense («the table» for a database table and
  for a table of the document);
- a string quoted from a screen, a log or a record in another language has no gloss;
- the sentence's verb comes so late, or a gloss is wedged into the sentence that uses the
  term, that I lost the sentence's own point;
- I had to read it twice to get its point.

A sentence does not fail for its length, its style, its citations, or because I would have
written it differently. Do not report taste, and do not propose a different structure.

The chapter: the pages given to you in the launch message, rendered from the built PDF
(render them yourself with `pdftoppm -r 80 -png` into your own scratch directory and view
each page; use `pdftotext -layout` for quoting). Read the pages in order, once, as a reader,
not as an auditor with a checklist.

Write your list to the file named in the launch message. One line per failing place: the
page, the sentence or label quoted exactly, and in a few words what stopped you («what is
this command?», «whose records?», «which three kinds?»). No rewrites: the writer rewrites.
End with one line: «N places» or «none». Change no other file.

---

What the agent running the process does with the list: every place goes back to the one
writer, who rewrites it as an instance of its class across the whole document, not at the
spot, carrying the change into the glossary, the captions and every later use of the old
wording, and reads the chapter again from its top. Each reader gets the chapter's pages as
an extract of the built PDF, the page offset, the list of terms the earlier chapters
defined, its own scratch directory, the name of its output file, and the order not to open
any other reader's list. A chapter is read twice: once on the build that finishes it, once
by a fresh reader on a later build with the first list applied. A third pass runs on the
final build, every chapter in parallel by fresh readers, when the second passes still find
half a place per page or more; a fourth never runs. Count the places per page per pass
and write the stopping rule down before the first pass. Residual places have three causes
worth knowing: the writer cannot see its own blind spots, a gloss wedged into the sentence
that uses the term hides that sentence's verb, and «I had to read it twice» has no floor.
After the last pass the audience read (`audience-read-brief.md`) decides.
