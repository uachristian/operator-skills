# Live mutable-file checksum race during restic recovery proof

## Symptom

An encrypted restic repository passed `check --read-data` and restored successfully. All 31 staged SQLite snapshots passed `PRAGMA quick_check`, but the critical-file SHA-256 verification failed for one Hermes profile `cron/jobs.json` file. Every other critical file matched.

## Why it happened

The backup generated the checksum manifest from live critical files, then passed both the live Hermes tree and a separate staging bundle to restic. A cron store can be atomically rewritten after hashing but before restic reads it. The resulting snapshot can therefore contain:

- a manifest digest from time A;
- the directly captured live cron file from time B;
- a staging bundle that does not contain the manifest-named critical-file copy.

Repository integrity remains valid, but the recovery proof is not coherent and must fail.

## Durable fix

Build one immutable critical-file bundle before invoking restic:

1. Create an owner-only staging root.
2. Copy all critical non-SQLite files into restore-relative paths under that root.
3. For frequently rewritten files, use a stable-copy retry:
   - stat the source;
   - copy to a temporary staged file;
   - stat the source again;
   - accept only if inode/size/mtime are unchanged;
   - atomically rename the staged temporary file into place.
4. Hash only the staged copies.
5. Back up that bundle as the canonical proof source.
6. Do not include duplicate live variants of manifest-named files in the restore-proof include set.
7. Restore and verify against the restored bundle root.
8. Only publish the restore-proof marker and enable schedules after a clean rerun.

## Failure handling

- Preserve the failed proof log, but remove restored secret-bearing temporary files on every exit path.
- Do not publish a restore-success marker after any checksum mismatch.
- Do not activate recurring backup/restore schedules merely because repository and SQLite checks passed.
- Create a fresh snapshot after fixing staging; do not reuse the incoherent snapshot as final proof.

## Evidence pattern

The useful diagnostic split is:

- `restic check --read-data`: proves stored packs are readable and structurally valid;
- isolated restore size/completion: proves data can be reconstructed;
- SQLite quick checks: prove database logical consistency;
- staged critical-file manifest: proves the exact captured configuration bundle is internally coherent.

All four gates are required for a defensible DR closeout.
