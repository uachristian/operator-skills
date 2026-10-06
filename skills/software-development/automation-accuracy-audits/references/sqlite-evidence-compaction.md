# Backup-gated compaction of a live SQLite evidence DB

Prerequisite: the ingest identity fix must already be tested. A regenerated snapshot should add 0 rows, and a material change should add 1.

1. **Build** (live DB opened read-only):
   - Open the live DB with `file:<db>?mode=ro`.
   - Replay the stored payloads, oldest first, through the fixed store function into a new staged DB. Keep the original observation time when a payload has none.
   - Record a per-table fingerprint: count plus max `ingested_at`.
2. **Verify the staged DB:**
   - For every business identifier (PO, work order, tracking, line, vendor order, invoice, part), compare the distinct set in live and staged.
   - Every lost identifier must be explained. Real lost values mean the extractor regressed: fix it and rebuild.
3. **Quiesce:** pause the only writer cron with `HERMES_HOME=<profile> hermes cron pause <id>`, then confirm with `pgrep` that no writer process is running.
4. **Back up:**
   - Copy the DB into `profiles/<p>/backups/<name>/` with `sqlite3.Connection.backup`; set the folder to 0700 and files to 0600.
   - Confirm backup counts equal live counts and `quick_check = ok`. Record the sha256.
   - Also keep a copy of the pre-change script.
5. **Rebuild** the stage against the quiet DB. Install the fixed script and delete its stale `__pycache__` `.pyc`.
6. **Apply:**
   - Open one `BEGIN IMMEDIATE` transaction and refuse if the live fingerprint differs from the build.
   - `ATTACH` the staged DB. Use a plain path; the `mode=ro` URI form fails to attach unless the connection was opened with `uri=True`.
   - For each table, `DELETE` then `INSERT ... SELECT`. Check the counts, then `COMMIT`.
   - Then run `quick_check`, `wal_checkpoint(TRUNCATE)` and `VACUUM`.
7. **Prove the fix:**
   - Touch the source files, run ingest twice and confirm the counts are stable.
   - Resume the cron.
   - Confirm the live-parity check (for example `verify_source_authority.py --check-live`) shows 0 drift.
8. **Report** before/after sizes and row counts, the identifier-preservation result, the backup path and the rollback: pause the writer, then restore the backup DB and the saved script.

## Source-manifest merges
When parallel branches all edit a hash manifest such as `SOURCE_AUTHORITY.json`:
1. Union the entries by `source` from `git show HEAD:` and `git show MERGE_HEAD:`.
2. Recompute every sha256 from the working tree, then commit the merge.
3. Before installing, check that live drift lists exactly the changed and new files. Back up each existing target before copying.
