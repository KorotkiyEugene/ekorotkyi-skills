# Writing engineering prose in Ukrainian

Read before drafting or editing a technical document in Ukrainian. The rules below were
learnt from documents that native engineers rejected as "translated": each entry names
what was rejected and what replaced it.

## Write it, do not translate it

A Ukrainian document is drafted in Ukrainian, sentence by sentence, in the order a
Ukrainian engineer would put the thoughts. Drafting in English and translating keeps the
English rhetorical skeleton ("What this is.", "Verification status:", "The pair is
exact", "Visual summary"), and that skeleton is what a reader notices first. When an
English mirror is wanted, it is a second document (`README.en.md` beside `README.md`,
`docs/` beside `docs/uk/`) with the same numbers, written the same way in the other
direction; the two are kept in step by the propagation rule of `writing-technical-docs`
(standard 9), never by sentence-by-sentence translation.

What stays untouched in either language: code identifiers, file paths, command lines,
literal program output (`MEASURED:` lines), and the proper names of packages and products.

## Vocabulary the field uses

| Use | Not | Why |
|---|---|---|
| рівень шуму | шумова підлога | calque of "noise floor" |
| точний відлік; випереджальний / точний / запізнілий (E / P / L) | промпт, early/late in prose | correlator taps have Ukrainian names |
| захоплення (пошук і захоплення) | захват | Russianism |
| підтверджений розв'язок (`pvtStatus`) | фікс | calque of "fix" |
| вихідна редакція; у вихідній редакції | у постачанні, постачений, delivered version | "as delivered" is not a Ukrainian idiom |
| матриця Тепліца, теплицева матриця | тепліцева | the noun is Тепліц, the adjective is теплицева |
| ФАПЧ, ЧАПЧ, ССЗ | ФАП, ЧАП, АСЗ, PLL/FLL/DLL in prose | established abbreviations; the English ones are given once in the glossary |
| імітатор (сигналів) | генератор | a model that produces a scene is an імітатор; a генератор is a signal source inside it |
| ГНСС | GNSS in prose | Cyrillic abbreviation; the Latin one belongs in the glossary |
| пригнічення (завади) | придушення | the term the product documentation uses |
| оцінка за методом моментів; детектор; естиматор named by its method | оцінювач | invented noun |
| стек | LIFO | where the meaning is a stack |
| перебудова ваг, оновлення ваг | апдейт, ресольв | |
| зерно генератора випадкових чисел | сід | |
| прогін, запис, вибірка, відвід, лінія затримки, кенселер, промінь, вектор наведення, псевдодальність, далекомірний код, мітка часу, стеження, взаємні завади, проблема «ближній-дальній» | | the established vocabulary of the accepted documents; reuse it before inventing |

Words that were invented by translation and rejected on sight: запускний, двостанове,
заважачі, пришпилює, посів стеження, найгарячіший цикл, чесна метрика, "модель бреше".
A metric is not честна and a model does not брехати; say what was measured and what it
showed.

## Numbers, units, ranges

- Units in Cyrillic with the established spacing: 24.7 дБ, 45 дБ·Гц, 4 МГц, 5 мс,
  0.978 мкс, 9.51 см. The decimal mark follows the code and the tables (24.7), so a
  number can be grepped between the document and the results file.
- Ranges without dashes: "13...15 с", "від 13 до 15 с", "1...7 джерел". Counts as
  "9 з 9", "8 з 9".
- A minus sign in a number is the minus sign (−2.2 дБ), not a hyphen.

## Figures

Figure labels, legends and titles are in the document's language and come from the
figure script, so the vocabulary rules above apply to the script: regenerate the figure,
do not annotate the prose around a figure that says "noise floor" in its legend. The
dash grep of `writing-technical-docs` runs over figure scripts too.

## The sweep before delivery

```bash
grep -n -i "шумов[а-я]* підлог\|промпт\|захват\|фікс\b\|фікси\|постачанн\|постачен\|тепліцев\|придуш\|оцінювач\|ФАП\b\|ЧАП\b\|АСЗ\|запускн\|двостанов\|заважач\|пришпил\|посів\|найгарячіш\|чесн[аі] метрик\|бреше\|—\|–" docs/uk/*.md scripts/*figures*.m
```

Every hit is rewritten, not just the first; a calque is a class, and a reader who finds
one looks for the rest.
