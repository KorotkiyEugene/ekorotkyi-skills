# Adding knowledge to this marketplace

This repo is a Claude Code **plugin marketplace**. New knowledge is added as skills,
commands, or whole plugins, then pushed so teammates pull it with
`/plugin marketplace update ekorotkyi-skills`.

## 1. Pick the right artifact

| The knowledge is… | Save it as… | Location |
|---|---|---|
| A repeatable practice / checklist / workflow | a **skill** (`SKILL.md`) | `plugins/<plugin>/skills/<name>/` |
| An action invoked by name | a **slash command** | `plugins/<plugin>/commands/<name>.md` |
| A new theme/domain | a **new plugin** | `plugins/<new>/` + register in the marketplace manifest |
| Long detail supporting a skill | a **reference file** | `plugins/<plugin>/skills/<name>/references/` |
| A deterministic helper a skill runs | a **script** | `plugins/<plugin>/skills/<name>/scripts/` |

A **plugin** is one coherent theme (`docs-standards`, later maybe `dsp-fpga`,
`code-review`). Related skills live together in one plugin. One marketplace holds many
plugins.

## 2a. Add a skill to an existing plugin

1. Create `plugins/<plugin>/skills/<new-skill>/SKILL.md`:

   ```markdown
   ---
   name: <skill-name>
   description: >-
     WHEN to trigger, in the third person, starting with "Use when". Be specific and a
     little pushy: list the concrete phrasings and contexts that should invoke it. Do not
     summarise what the skill does: an agent that reads a workflow summary in the
     description follows the summary instead of the skill. The description is the entire
     triggering mechanism.
   ---

   # <Title>
   The guidance, with the *reasoning* behind each rule (not bare MUSTs). Keep it under
   ~500 lines; push long detail into references/.
   ```

2. Skills are auto-discovered under `skills/`; **no manifest edit needed**.
3. Bump `version` in `plugins/<plugin>/.claude-plugin/plugin.json`.
4. Commit and push.

## 2b. Add a whole new plugin

1. `plugins/<new>/.claude-plugin/plugin.json`:

   ```json
   {
     "name": "<new>",
     "version": "0.1.0",
     "description": "One line on what this plugin gives you.",
     "author": { "name": "<you/org>" }
   }
   ```

2. Add its `skills/` and/or `commands/`.
3. Register it in `.claude-plugin/marketplace.json` under `plugins`:

   ```json
   { "name": "<new>", "source": "./plugins/<new>", "description": "…" }
   ```

4. Commit and push. Teammates then `/plugin install <new>@ekorotkyi-skills`.

## 3. Test locally before pushing

Add the marketplace from its local path, install, and try the skill in a real task:

```
/plugin marketplace add /absolute/path/to/claude-marketplace
/plugin install <plugin>@ekorotkyi-skills
```

Iterate on the SKILL.md, then push once it behaves.

## 4. Author with skill-creator (recommended)

The fastest good path is to let Claude scaffold it: in any Claude Code session say
*"add a skill to my claude-marketplace for X"*. Claude uses the `skill-creator` skill to
draft the SKILL.md, and can run the **description-optimization loop** (generates
trigger / no-trigger eval queries and tunes the `description`). Save the eval set under
the skill's `evals/` so the optimization is reproducible; git-ignore the `*.log`.

Note: skills **under-trigger** for tasks Claude can already do directly (e.g. "just
write this"). For guidance that must apply *every time*, pair the skill with an
always-on rule in the consuming repo's `CLAUDE.md` (see the README).

## 5. Versioning & distribution

- Bump the plugin `version` on every change; that is the signal teammates have updates.
- They pull with `/plugin marketplace update ekorotkyi-skills`.
- Keep the marketplace pushed to the shared Git host; it is consumed *as a git repo*.
