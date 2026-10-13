# Claude Marketplace (internal)

A shared [Claude Code](https://docs.claude.com/en/docs/claude-code) **plugin
marketplace** for the team. Each plugin bundles reusable skills, commands, and
workflows so everyone applies the same practices across their own projects.

## Plugins

| Plugin | What it gives you |
|---|---|
| **docs-standards** | Four skills and a command. `writing-technical-docs`: eleven documentation-quality standards with an audit checklist (derive, define with code-name notation tables, illustrate, self-contained, stage openings, verify visuals, show what you name, generated numbers, propagated corrections, no dashes as connectives, no status labels), plus a reference on writing engineering prose in Ukrainian. `reporting-experiments`: the shape of a measurement or comparison report (derived conditions, the measurement ceiling, calibrated metrics, controls before mechanisms, what the test does not show, reproduction, defect ledgers). `typesetting-documents-as-pdf`: toolchain choice and the layout defects a clean build hides, with checking scripts. `documenting-existing-designs`: reports and block diagrams of inherited or partial code with a provenance tier on every claim and verification against real artefacts. `/review-doc` runs the audit. |
| **fpga-design** | Three skills for FPGA/ASIC work: `writing-synthesizable-rtl` (inference, latches, resets, CDC), `constraining-fpga-designs` (never build without an SDC), and `verifying-fpga-builds` (a tool reporting "0 errors" is not success). Triggers on HDL edits, project setup, and after any synthesis run. |

## Install (for teammates)

From inside Claude Code:

```
/plugin marketplace add <git-host>/<org>/claude-marketplace
/plugin install docs-standards@ekorotkyi-skills
```

Replace `<git-host>/<org>` with wherever this repo lives (e.g.
`github.com/acme/claude-marketplace`, or an internal Git URL). After installing, the
`writing-technical-docs` skill activates on documentation tasks and `/review-doc [path]`
runs a full audit. `reporting-experiments` activates when the deliverable quotes
measured numbers (a test report, a comparison, a results section).

To update later: `/plugin marketplace update ekorotkyi-skills`. Confirm it is active
any time with `/plugin` (lists installed plugins); `docs-standards` should appear.

## Using it

Once installed, in any of your projects:

- **Automatically**: when you ask Claude to *review, tighten, or fix* a technical
  document, or you complain that something in one is undefined/unexplained/hand-wavy
  (e.g. "this spec is unclear", "these numbers have no derivation", "make this readable
  for a new hire"), the `writing-technical-docs` skill activates and applies the
  standards; a results section or test report also brings in `reporting-experiments`.
- **Explicitly**: run `/review-doc <path>` (or `/review-doc` for the doc in focus) to
  force a full audit: Claude lists every violation grouped by standard, fixes the whole
  class in one pass, and re-inspects any figures/PDFs it touched.
- **Always-on (recommended for first drafts)**: the skill under-triggers when you just
  say "write me a doc" (Claude writes it directly); pair it with the `CLAUDE.md` rule
  below so the standards apply even then.

## Reliable adoption: pair the skill with a CLAUDE.md rule

Skills **under-trigger by design**: Claude only consults a skill for tasks it can't
easily handle on its own, so it reliably fires the `writing-technical-docs` skill when
you ask it to *review/fix* a doc ("this spec is unclear", "the numbers have no
derivation", `/review-doc`) but often skips it when you just say "write me a design
doc"; it figures it can write that directly. (Measured: 100% precision, ~25% recall on
first-draft requests; this is inherent to the trigger mechanism, not the wording.
`reporting-experiments` measures the same way: 100% precision, and it fires on about
20% of runs for "write up the results of..." requests.)

For the standards to apply **every time**, add them as an always-on rule in the
consuming repo's `CLAUDE.md` (or your personal `~/.claude/CLAUDE.md`). The skill then
handles review/audit and explicit invocation; the CLAUDE.md rule guarantees the
standards on first drafts too. Paste this:

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
No em or en dashes as connectives, no status labels in titles. Documents in
Ukrainian use the field's vocabulary, not calques. Run `/review-doc` for a full audit.
```

## Auto-enroll a project (optional)

To make a repository offer this plugin to anyone who opens it, commit a
`.claude/settings.json` in that repo:

```json
{
  "extraKnownMarketplaces": {
    "ekorotkyi-skills": {
      "source": { "source": "git", "repo": "<git-host>/<org>/claude-marketplace" }
    }
  },
  "enabledPlugins": ["docs-standards@ekorotkyi-skills"]
}
```

## Repository layout

```
claude-marketplace/
├── .claude-plugin/
│   └── marketplace.json          # lists the plugins in this marketplace
├── plugins/
│   └── docs-standards/
│       ├── .claude-plugin/plugin.json
│       ├── skills/
│       │   ├── writing-technical-docs/        # SKILL.md, references/, evals/
│       │   ├── reporting-experiments/         # SKILL.md, evals/
│       │   ├── typesetting-documents-as-pdf/  # SKILL.md, scripts/, assets/
│       │   └── documenting-existing-designs/  # SKILL.md, references/, evals/
│       └── commands/
│           └── review-doc.md
├── plugins/fpga-design/ ...
├── plugins/sunburst-hdl/ ...
└── README.md
```

## Contributing a plugin or skill

1. Add a plugin under `plugins/<name>/` with a `.claude-plugin/plugin.json`.
2. Register it in `.claude-plugin/marketplace.json`.
3. Bump the plugin `version` on changes so teammates get updates.

Skills are authored with the [skill-creator](https://docs.claude.com/en/docs/claude-code/skills)
conventions: a `SKILL.md` whose `description` states clearly *when* to trigger, and a
body that reads as guidance with the reasoning behind each rule.
