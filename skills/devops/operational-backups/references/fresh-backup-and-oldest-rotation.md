# Fresh backup + oldest-rotation pattern

Use this when the owner asks for a "fresh backup" and to delete the oldest existing backup.

## Pattern

1. Inventory the backup directory first.
   - Count top-level backup items.
   - Identify the oldest and newest items by filesystem mtime.
   - Do not assume naming order equals age; use stat/mtime.
2. Create the new backup before deleting anything.
   - Put it under the normal backup root, e.g. `~/.hermes/backups/fresh-current-state-YYYYMMDD-HHMMSS/`.
   - Include a `MANIFEST.txt` explaining purpose, included files, and exclusions.
   - Exclude secrets/auth files, `.env`, tokens, raw customer data, large DBs, and anything not needed for rollback.
3. Verify the new backup is usable.
   - Check expected files exist and are non-empty.
   - Include enough state to restore the specific change: scripts, cron jobs JSON, relevant skills/references, vault doc snapshot/log tail when documentation was part of the change.
4. Delete exactly one oldest top-level backup item.
   - Guard the delete target so it must be a direct child of the backup root.
   - Prefer deleting after verification only.
   - Use the platform's dangerous-command approval flow for recursive deletion.
5. Verify after deletion.
   - List the new backup contents.
   - Show the new oldest few backups.
   - Confirm the top-level backup count.

## Example scope for Hermes runtime fixes

For a production automation fix, include:

- touched runtime scripts
- cron `jobs.json` for the owning profile/default profile
- relevant skill `SKILL.md` and references
- relevant vault doc snapshot and `log.md` tail, if docs were updated
- `MANIFEST.txt`

## Pitfalls

- Do not delete the oldest backup first. If backup creation fails midway, rollback coverage is worse than before.
- Do not back up secrets just because they are nearby in the same profile folder.
- Do not recursively delete a path unless it is verified to be under the expected backup root.
- Do not call this a repo backup unless the target is actually in git and committed/pushed; many Hermes runtime/state folders are not git repos.
