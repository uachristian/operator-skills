# Cleanup-Plan Table Pattern (multi-file deletes / batch refactors)

When a session produces a backlog of stale/duplicate/superseded files (deprecated docs, promoted drafts, renamed entities, dead wikilinks, etc.), the temptation is to fire a single mass-rm. **Don't.** Frame it as a Phase-1 audit even when the surface isn't a launchd service.

## The pattern

After audit reveals the cleanup scope, present a table BEFORE deleting anything:

```markdown
| # | Action                                      | Risk                                        |
|---|---------------------------------------------|---------------------------------------------|
| 1 | Fix `docs/foo.md` — update cron name + time | None — pure correction                      |
| 2 | **Delete** `legacy/old-flow.md` (superseded)| Low — content fully covered by new file     |
| 3 | **Delete** 4 stale `_drafts/` files         | Low — already merged into live versions     |
| 4 | Inspect `INDEX.md:52` — possible placeholder| None                                        |
| 5 | Leave orphans alone — indexed elsewhere     | None                                        |
```

End with: `Go ahead?` and STOP.

## Why a table (not a prose list)

- **Risk column forces honesty.** "None / Low / Medium / High" makes you actually think about each item rather than batching them all under one approval.
- **Numbered rows make selective approval easy.** User can say "do 1, 3, 5; hold 2 and 4" without ambiguity.
- **The "Leave alone" rows matter as much as the action rows.** They explicitly document the things you considered and chose NOT to touch — that's the difference between an audit and an aggressive cleanup. Documenting non-actions prevents the user from worrying you missed them.

## When the trigger fires

Use this table format whenever:

- ≥ 3 files will be deleted in one batch
- Mixed actions: some patches, some deletions, some "leave alone"
- The cleanup follows a rename/refactor where stale references could be either harmless history or active bugs
- You found orphans/broken links and need to triage which are real problems vs intentional standalones

For 1-2 file deletes with obvious justification, a prose proposal is fine.

## Approval phrases that count

- "Yes" / "go ahead" / "proceed" / "do it"
- "Do all of them"
- Numbered selections: "do 1, 3, 5"

NOT approval:
- "Looks reasonable" (passive review, not authorization)
- Silence
- Asking a clarifying question (still in Phase 1)

## After execution

Run a verification audit and report what changed. If the cleanup was tied to broken-link or stale-reference cleanup, re-run the broken-link audit to confirm zero remain — that's the only honest way to declare the cleanup complete.

## Real session

Found after a skill rename:
- 31 broken wikilinks
- 33 stale references to old skill name
- 13 orphan files
- 2 superseded workflow docs
- 4 promoted drafts still living in `_drafts/`

Built a 5-row plan table with risk column → user approved → executed → re-ran audit:
- 0 broken wikilinks
- 9 stale references all in legitimately historical contexts
- All deletions clean

What this pattern prevented: deleting `daily-flow.md` without first noticing `delivery.md` linked to it. The table forced the "what links here" check that would have produced a broken-link in production navigation if I'd just rm'd the file.

## Pitfall: don't number-jump in the response

If user approves "go ahead" on the full table, execute every row in order, in a single batch, and report once at the end. Do NOT:

- Stop after row 1 and ask "ready for row 2?" (annoying, defeats batching)
- Reorder rows (user reviewed the order; respect it)
- Add new rows mid-execution ("while I was deleting #3, I noticed X — also deleting it") — that's a new audit, save it for the next round
