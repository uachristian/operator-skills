# operator-skills

A curated set of 29 agent skills that encode an operator's discipline for
**building, reviewing, changing, and running** software and automations safely.
They were distilled from a single operator's day-to-day use of an AI agent fleet
and sanitized for public use: business, person, and host specifics are replaced
with placeholders such as `<owner>`, `<business>`, `<CRM>`, and `<shop-system>`.

Each skill is a directory with a `SKILL.md` (YAML frontmatter + Markdown body) and
optional `references/` and `templates/`. The format is the
[Hermes Agent](https://hermes-agent.nousresearch.com/docs) skill format, but the
content is plain Markdown and works with any harness that can load instructions.

See [INDEX.md](INDEX.md) for the full list with "when to use" triggers.

## What's inside

- **Build and quality** — `build-execution-standard`, `development-quality-loop`,
  test-isolation debugging, `upstream-open-source-contributions`.
- **Adversarial release reviews** — dependency/lockfile, data-boundary,
  credential rotation, external-action wrappers, release-artifact integrity,
  one-shot approval authority, evidence-bound analysis.
- **Operations and change control** — change control, backups with recovery
  proof, reliability/SRE lanes, security/privacy audits, read-only third-party API
  audits, webhook-driven runs, fleet observers.
- **Planning and review** — operational-state review, project-portfolio audits,
  founder launch gates, GitHub workflows including a public-push privacy gate.

## Install

### Hermes Agent

Copy or symlink a skill into your skills directory, keeping the category folder:

```bash
git clone https://github.com/uachristian/operator-skills.git
mkdir -p ~/.hermes/skills/software-development
ln -s "$PWD/operator-skills/skills/software-development/build-execution-standard" \
      ~/.hermes/skills/software-development/build-execution-standard
```

Or add the whole `skills/` directory as an external skills directory
(`skills.external_dirs` in `config.yaml`; see `hermes skills --help`). New skills
are picked up by new sessions.

### Other harnesses

Point the harness at the relevant `SKILL.md` (for example as a custom instruction,
rules file, or system-prompt include). Reference files are linked relatively from
each `SKILL.md`; load them on demand.

## Conventions

- Descriptions start with `Use when ...` so routers can match triggers.
- Skills describe rules and the lesson behind them, not incident logs.
- Anything that mutates production is approval-gated; read-only is the default.

## Validate

```bash
python3 scripts/validate_skills.py
```

Checks frontmatter fields, description length, broken relative links, and file
size (no file over 200 KB). PyYAML is used when available.

## License

MIT — see [LICENSE](LICENSE).
