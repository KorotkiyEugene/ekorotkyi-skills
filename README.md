# Claude Marketplace (internal)

A shared [Claude Code](https://docs.claude.com/en/docs/claude-code) **plugin
marketplace** for the team. Each plugin bundles reusable skills, commands, and
workflows so everyone applies the same practices across their own projects.

## Plugins

| Plugin | What it gives you |
|---|---|
| **docs-standards** | The `writing-technical-docs` skill (six documentation-quality standards + an audit checklist) and a `/review-doc` command. Triggers automatically whenever you write, review, or improve a technical document. |

## Install (for teammates)

From inside Claude Code:

```
/plugin marketplace add <git-host>/<org>/claude-marketplace
/plugin install docs-standards@claude-marketplace
```

Replace `<git-host>/<org>` with wherever this repo lives (e.g.
`github.com/acme/claude-marketplace`, or an internal Git URL). After installing, the
`writing-technical-docs` skill activates on documentation tasks and `/review-doc [path]`
runs a full audit.

To update later: `/plugin marketplace update claude-marketplace`.

## Auto-enroll a project (optional)

To make a repository offer this plugin to anyone who opens it, commit a
`.claude/settings.json` in that repo:

```json
{
  "extraKnownMarketplaces": {
    "claude-marketplace": {
      "source": { "source": "git", "repo": "<git-host>/<org>/claude-marketplace" }
    }
  },
  "enabledPlugins": ["docs-standards@claude-marketplace"]
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
│       │   └── writing-technical-docs/SKILL.md
│       └── commands/
│           └── review-doc.md
└── README.md
```

## Contributing a plugin or skill

1. Add a plugin under `plugins/<name>/` with a `.claude-plugin/plugin.json`.
2. Register it in `.claude-plugin/marketplace.json`.
3. Bump the plugin `version` on changes so teammates get updates.

Skills are authored with the [skill-creator](https://docs.claude.com/en/docs/claude-code/skills)
conventions: a `SKILL.md` whose `description` states clearly *when* to trigger, and a
body that reads as guidance with the reasoning behind each rule.
