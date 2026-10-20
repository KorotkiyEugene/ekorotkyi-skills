# ekorotkyi-skills

A [Claude Code](https://code.claude.com/docs/en/overview) plugin marketplace with three
plugins, seventeen skills and one command. The skills encode engineering discipline for
technical writing, FPGA/ASIC design and Verilog/SystemVerilog coding, so Claude applies
the same practices in every project where the plugins are installed.

| Plugin | Skills | What it enforces |
|---|---|---|
| [docs-standards](#docs-standards) | 6 skills, 1 command | Technical documents and chat explanations that derive every claim, define every term before use, and verify every figure. Measurement reports, PDF typesetting, and analysis of inherited designs. Research design documents with refutable hypotheses, and theses or R&D reports written from artefacts. |
| [fpga-design](#fpga-design) | 3 skills | RTL that synthesises into the intended hardware, timing constraints on every build, and build reports read rather than trusted. |
| [sunburst-hdl](#sunburst-hdl) | 8 skills | Verilog/SystemVerilog rules distilled from Cliff Cummings' Sunburst Design papers: race-free coding, async FIFOs, clock-domain crossing, FSMs, case statements, SVA, simulation speed. |

## Install

From inside Claude Code, register the marketplace once and install the plugins you want:

```
/plugin marketplace add KorotkiyEugene/ekorotkyi-skills
/plugin install docs-standards@ekorotkyi-skills
/plugin install fpga-design@ekorotkyi-skills
/plugin install sunburst-hdl@ekorotkyi-skills
```

The same works from a shell with `claude plugin marketplace add` and `claude plugin
install`. The repository is public, so no GitHub account or credentials are needed.

To pick up new versions later:

```
/plugin marketplace update ekorotkyi-skills
```

`/plugin` lists what is installed and enabled. Each skill appears under its plugin name,
for example `docs-standards:writing-technical-docs`.

### Install from a local clone

For editing the skills, register the clone as a directory marketplace instead. Claude
Code then reads the plugin files in place, and edits take effect at the next session or
after `/reload-plugins`:

```
/plugin marketplace add /absolute/path/to/ekorotkyi-skills
/plugin install docs-standards@ekorotkyi-skills
```

### Auto-enroll a project

To make a repository offer the plugins to anyone who opens it, commit this
`.claude/settings.json` in that repository. The marketplace registers after the
contributor trusts the folder, and the plugins install at the next session start:

```json
{
  "extraKnownMarketplaces": {
    "ekorotkyi-skills": {
      "source": { "source": "github", "repo": "KorotkiyEugene/ekorotkyi-skills" }
    }
  },
  "enabledPlugins": {
    "docs-standards@ekorotkyi-skills": true,
    "fpga-design@ekorotkyi-skills": true
  }
}
```

## docs-standards

Standards for technical writing, a production process and an audit workflow. Version 0.9.0.

| Skill | Fires when | What it does |
|---|---|---|
| `writing-technical-docs` | Writing, reviewing or fixing a design doc, spec, README, report, or explaining something in chat | Applies thirteen standards: derive rather than assert, define before first use (with notation tables that carry code names, and every tool and command said what it is at its first use in each chapter), illustrate concepts, keep the document self-contained, write for two audiences, verify visuals, show every artefact you name, generate numbers and cross-references, propagate corrections, no dashes as connectives, address the reader not the reviewer (a bare title page, nominal headings, no sentence about the document itself), one running example (the product's own case in a document about a product), point by name or anchor. Adds sentence rules (one idea, at most 40 words, no semicolon, the noun in the sentence, no code identifier standing in for an idea) and a register of plain sentences with real counts. Prescribes the process: the heading tree approved first and frozen, one writer for the whole text, fresh outsider readers per chapter who know none of the stack, one audience read of the whole document with a verdict per criterion, bounded verification with the owner's yes before any sweep, one delivery with verdicts. Includes the two reader briefs and a reference on engineering prose in Ukrainian. |
| `reporting-experiments` | Writing up measured results: a comparison, benchmark, A/B test, parameter sweep, verification campaign or test report | Fixes the shape of the report: derived conditions, the measurement ceiling, calibrated metrics, controls before mechanisms, what the test does not show, how to reproduce it, a ledger of defects found on the way, and records that carry their commit and run times and are re-made when the thing under test changes. |
| `typesetting-documents-as-pdf` | Turning Markdown or text into a PDF, or when a PDF looks wrong | Chooses the toolchain from the content, measures the source before setting the page, then finds the layout defects a clean build hides: overflowing tables and code, wrong quotes, stranded headings, silently dropped glyphs, and the ones a long document grows: loose lines, breaks inside what the reader copies, stranded lead-ins, empty page feet, split short tables and listings, references by name, citations that resolve, attachments by hash. Ships inspection scripts (section references, sentences, word gaps) and a build template; the page gate runs once, at the end. |
| `documenting-existing-designs` | Describing a codebase or hardware design you did not write, including partial or mixed-revision trees | Produces a generated inventory first, puts a provenance tier on every claim, traces every number to a line, derives block diagrams from the netlist, flags anomalies instead of explaining them away, verifies against real artefacts where they exist, and closes with a verification statement and a «Not verified» list of what nobody ran. |
| `designing-research-studies` | Planning an R&D study, a thesis project, a method comparison or a measurement campaign before anything is run | Gives the research design document its shape: hypotheses with the result that refutes them, the candidate space with numbered sieve criteria and checkpoints (the sieve is a result), an evaluation protocol with splits by record, condition bands, seeds and operating points chosen on validation, a reproduced point of reference, the compute budget with the order of cuts and the never-cut path, and rulings and handoffs while the study runs. Ships a design-document template. |
| `writing-research-reports` | Writing or revising a thesis, an explanatory note, an R&D report, a paper's introduction, review, methods, results or conclusions, an abstract, a statement of novelty | Writes the chapters from artefacts in order (review from the literature protocol, methods from code and configurations, results from generated tables, conclusions, abstract and introduction last), fixes the introduction paragraph by paragraph, closes the review with gap and hypotheses tables, reports results by condition band with the discarded candidates, sets the impersonal register and glossary discipline, and ends with a pre-submission checklist. Ships a structure-and-checklist reference distilled from public thesis guides and a literature review protocol with a verified bibliography. |

The `/review-doc [path]` command runs the full audit on a document: the outsider read of
each chapter first, then every violation grouped by standard, the mechanical sweeps, each
class fixed in one pass by one writer, a bounded verification, and, for a finished
document, the audience read with its verdict per criterion. A Ukrainian document also
gets the prose reference; a document with measured results also gets the
reporting-experiments checklist; a document about a system someone else built also gets
documenting-existing-designs.

### Make the standards apply to first drafts too

Skills under-trigger on tasks Claude believes it can do directly. On the trigger evals
shipped with the skills, `writing-technical-docs` never fired on a query it should not
have, but fired on only about one in four plain "write me a design doc" requests;
`reporting-experiments` fired on about one in five "write up the results" requests. Both
fire reliably on review and fix requests and on `/review-doc`.

For the standards to apply every time, add them as an always-on rule in the consuming
repository's `CLAUDE.md` or in your personal `~/.claude/CLAUDE.md`. The skill then
covers review, audit and explicit invocation, and the rule covers first drafts:

```markdown
## Technical documentation
For any technical document, spec, or explanatory writeup (design docs, RFCs, ADRs,
API/reference docs, READMEs, test reports): (1) derive, don't assert: decode every
symbol, show every number's derivation, explain each causal step; (2) define every
term/convention/operation before first use, no forward references; (3) illustrate
geometric/conceptual claims with figures (computed from real data preferred; draw
vectors as vectors); (4) keep it self-contained, no load-bearing links to other docs;
(5) readable by a non-specialist engineer as well as an expert; (6) render and visually
inspect every figure/PDF before calling it done. When fixing feedback, sweep the whole
document for that *class* of issue in one pass; never patch only the flagged spot.
No em or en dashes as connectives, no status labels in titles. One idea per sentence,
at most 40 words, no semicolon in prose; every tool and command said what it is at its
first use in each chapter; a bare title page and nominal headings. One writer for the
whole text; before I see it, a reader who knows none of the stack reads each chapter and
one reader reads the whole document as its audience. Documents in Ukrainian use the
field's vocabulary, not calques. Run `/review-doc` for a full audit.
```

## fpga-design

Discipline for FPGA and ASIC digital design, vendor-neutral with Quartus specifics
measured on real runs. Version 0.1.1.

| Skill | Fires when | What it does |
|---|---|---|
| `writing-synthesizable-rtl` | Writing, editing or reviewing Verilog, SystemVerilog or VHDL that will be synthesised | Memory and DSP inference, reset style, latch avoidance, clock-domain crossings, and the places where simulation and synthesis diverge. |
| `constraining-fpga-designs` | Creating a project, adding a source, running a flow, or anything about timing | Never build without an SDC/XDC: clock definitions, I/O delays, false and multicycle paths, CDC exceptions, pin locations, and the log codes that mean the constraints were not read. |
| `verifying-fpga-builds` | After any synthesis, fitter, place-and-route or bitstream run | Four gates a build must pass: constraint warnings treated as failures, inferred resources checked against expectation, timing slack on every domain, and numbers reported rather than a status line. |

`reference/quartus-toolchain.md` holds the vendor lookup material the skills point to:
log codes, editions and licensing, containers, running Quartus on Apple Silicon, measured
runtimes, and output file locations.

## sunburst-hdl

Verilog/SystemVerilog rules from Clifford E. Cummings' award-winning Sunburst Design
papers. Each skill was written from a full read of its source papers and validated by
running a representative task without the skill, recording the failures, then re-running
with it. Version 0.1.0. The plugin's own [README](plugins/sunburst-hdl/README.md) maps
each skill to its papers.

| Skill | Fires when |
|---|---|
| `avoiding-verilog-races` | Writing or reviewing any always block, testbench, clock or reset sequence; results differ between runs or simulators; someone proposes `#0` delays to fix a nonblocking assignment |
| `designing-async-fifos` | Designing, reviewing or debugging a dual-clock FIFO or its full/empty flags |
| `crossing-clock-domains` | Any signal, bus, pulse or reset crossing asynchronous clock domains; adding synchronisers; CDC constraints |
| `coding-fsms` | Writing or refactoring a state machine: encodings, next-state logic, glitch-free outputs |
| `coding-case-statements` | Any case/casez/casex, priority encoder, one-hot mux; `full_case`/`parallel_case` pragmas; latches from a case |
| `using-sv-processes-and-ports` | Choosing `always_comb`/`always_ff`/`always_latch`, tasks and functions in RTL, port connection styles |
| `writing-designer-sva` | Adding assertions to RTL, choosing inline versus bind files, debugging a failing assertion |
| `speeding-up-simulation` | A slow simulation or regression; writing testbench infrastructure; reviewing code for simulation cost |

Where a project style guide conflicts on naming or formatting, the style guide wins;
these skills win on semantic rules such as assignment discipline and CDC structure.

## Repository layout

```
ekorotkyi-skills/
├── .claude-plugin/marketplace.json      # the catalog: name, owner, plugin entries
├── plugins/
│   ├── docs-standards/
│   │   ├── .claude-plugin/plugin.json
│   │   ├── commands/review-doc.md
│   │   └── skills/
│   │       ├── writing-technical-docs/       # SKILL.md, references/, evals/
│   │       ├── reporting-experiments/        # SKILL.md, evals/
│   │       ├── typesetting-documents-as-pdf/ # SKILL.md, scripts/, assets/
│   │       └── documenting-existing-designs/ # SKILL.md, references/, evals/
│   ├── fpga-design/
│   │   ├── .claude-plugin/plugin.json
│   │   ├── reference/quartus-toolchain.md
│   │   └── skills/                           # three skills
│   └── sunburst-hdl/
│       ├── .claude-plugin/plugin.json
│       ├── README.md
│       └── skills/                           # eight skills
├── CONTRIBUTING.md
└── README.md
```

Each plugin's `version` in its `plugin.json` is bumped on every change; that is how
installed copies learn there is an update. `claude plugin validate .` checks the catalog
and every plugin manifest.

## Contributing

[CONTRIBUTING.md](CONTRIBUTING.md) covers adding a skill, a command or a whole plugin,
writing a description that triggers correctly, testing from a local clone, and
versioning.
