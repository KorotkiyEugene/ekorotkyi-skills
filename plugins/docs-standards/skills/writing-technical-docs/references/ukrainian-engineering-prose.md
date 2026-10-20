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

## Vocabulary of research and machine-learning work

A thesis or an R&D report in Ukrainian is read by examiners who stop at the first
transliterated English word. The left column is the established form; the right column
is what drafts contain and what reviewers strike out. The English term may appear once,
in parentheses, at the first use, when the reader needs it to search the literature.

| Use | Not | Why |
|---|---|---|
| набір даних | датасет | calque |
| опорний метод, опорний результат | бейзлайн | calque |
| контрольна точка перевірки, етап перевірки | гейт, ворота | calque of "gate" |
| перевірка працездатності на мінімальних даних | димовий тест, смок-тест | calque of "smoke test" |
| режим мінімальних підвибірок | smoke-режим | |
| конвеєр обробки | пайплайн | calque |
| обсяг роботи | скоуп | |
| розгортання (на платі, на платформі) | деплой | |
| виконання моделі, обчислення виходу мережі | інференс | |
| середовище виконання | рантайм | |
| пакет прикладів, розмір пакета | батч | |
| збережений стан моделі | чекпоінт | |
| файл налаштувань, конфігурація | конфіг | |
| початкове значення (зерно) генератора випадкових чисел | сід | |
| навчальна, валідаційна, тестова вибірки; розбиття | трейн, вал, тест; спліт | |
| ознаки | фічі | |
| мітка, розмітка | лейбл | |
| приклад, зразок, відлік | семпл | |
| підбір гіперпараметрів; перебір за сіткою | тюнінг; грід-серч | |
| перенавчання | оверфіт | |
| витік даних між вибірками | лік | |
| донавчання; передтренування | файнтюнінг; претрейн | |
| доповнення даних | аугментація | |
| квантування (після навчання; з урахуванням квантування) | квантизація | the Ukrainian technical term is квантування |
| спільна базова мережа (екстрактор ознак); вихідна гілка | бекбон; голова | a network has no head in Ukrainian; a гілка is what it has |
| обмежувальна рамка | бокс | |
| фрагмент (зображення, спектрограми) | тайл | |
| придушення немаксимумів | НМС as a word | the abbreviation NMS may follow the term once |
| пропускна здатність; затримка | тхрупут; лейтенсі | |
| використання ресурсів | утилізація | |
| часові обмеження, аналіз часових характеристик | таймінги | |
| тактова частота | клок | |
| IP-ядро | айпі | |
| порівняльне дослідження з вилученням компонента | абляція | |
| остаточні методи, методи, що пройшли відсів | фіналісти | |
| робочий процес | воркфлоу | |

Register of the genre, learnt from rejected drafts:

- Impersonal forms carry the text: «у роботі запропоновано», «виміряно», «показано»,
  «встановлено». No «я» and no «ми зробили»: the examiner reads the first person as a
  diary, and the department template does not allow it.
- A heading names the subject of the analysis as a noun phrase («Аналіз методів
  виявлення…», «Протокол оцінювання»), never a person, a metaphor or working jargon
  («Що робимо далі», «Точка відліку», «Наш підхід»).
- Percentage points are «п.п.», never «%» when a difference of two percentages is meant.
- A Cyrillic abbreviation is used after its first definition («відношення сигнал/шум
  (ВСШ)»); a Latin one stays only for established designations (FPGA, GPU, STFT, IQ)
  and is listed in the abbreviations table.
- Ranges and comparisons without dashes: «від −10 до 0 дБ», «13...15 с», «у 2,5 раза».
- Decimal comma in the prose and the tables of a Ukrainian document (24,7 дБ); the
  results files keep the decimal point, and the table script converts once.

The sweep for this section, run over the prose and the figure scripts before delivery:

```bash
grep -n -i "датасет\|бейзлайн\|гейт\b\|ворота\|смок\|димов\|пайплайн\|скоуп\|деплой\|інференс\|рантайм\|батч\|чекпоінт\|конфіг\b\|сід\b\|спліт\|фіч\|лейбл\|семпл\|тюнінг\|оверфіт\|файнтюн\|претрейн\|аугментац\|квантизац\|бекбон\|голов[аи] мереж\|бокс\|тайл\|тхрупут\|лейтенсі\|утилізац\|таймінг\|клок\|айпі\|абляц\|фіналіст\|воркфлоу" docs/*.md
```
