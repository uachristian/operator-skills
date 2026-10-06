---
name: operational-backups
description: "Use when creating, verifying, rotating, pruning, or restoring operational backups. Prove recovery before deleting anything."
version: 2.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [backups, rollback, recovery, safety]
    related_skills: [operational-change-control]
---

# Operational Backups

## When to Use

Recovery evidence, fresh backups, full profile rollback, retention and cleanup. Choose the exact requested backup type; do not turn a small script change into a full secrets/database copy or treat a full recovery request as a source-only snapshot. Existing production/physical/privacy authority remains binding.

## Invariants

1. Prove actual account, home, profile, cwd and runtime roots; prefer explicit source and destination until verified. Scope environment overrides to one process.
2. Define every source as REQUIRED, OPTIONAL or FORBIDDEN/UNAPPROVED before work. Do not silently downgrade a failing required source. Expected optional exclusions must be visible in the manifest; unexpected storage/capture errors do not become harmless merely because a source was labeled optional.
3. Create new backup before deletion and verify before rotation. Outside-source destination, owner-only modes, exact inventory, source/candidate identities, hashes, exclusions and rollback instructions. Expand the backup BEFORE newly scoped edits.
4. Ordinary evidence excludes secrets, raw customer/private data and unnecessary large databases. Explicit full-profile/full-DR scope may include necessary profile-local secrets, never printed or copied between profiles. Use independent authenticated encryption for off-host/cloud/removable storage or absent FileVault protection. Modes alone are not encryption.
5. Checksums/archive readability are not restore proof. Prove required recovery in a disposable isolated environment before replacing critical recovery artifacts or enabling a new schedule. Preserve original until replacement proof succeeds.
6. No guessed, broad or automatic deletion. Inventory exact paths and recovery value, obtain exact approval, revalidate path/ownership/symlink/process use immediately before deletion, remove only safe approved items, then prove absence and retained recovery. Offload cold artifacts only to the owner's chosen archive destination; sensitive packs stay appropriately encrypted.

## Select the backup lane

- **Small edit / evidence snapshot:** only touched scripts/config definitions, relevant metadata and rollback context; no secret dump. Sanitize launchd plist environment/secret-like arguments before recording.
- **Full profile rollback:** explicit scope, hidden files/metadata/modes, bridges and centrally owned shims identified, destination outside profile. macOS metadata-preserving copy when appropriate. Inspect mutable state for consistent capture; a raw live directory copy is not automatically a coherent database backup. Record intentional secret inclusion and encryption requirements.
- **Live SQLite/restic DR:** required-source inventory, immutable verified database snapshots and staged copies of mutable cron/config files. Hash the exact staged bytes that the backup reads; restore those same bytes. Separate backup freshness from restore-proof success. Use the existing supported no-prune mode for the first repaired run; do not couple recovery proof with retention deletion.
- **Database authority/migration change:** capture exact direct/effective ACL, object/owner/default-ACL and ledger state plus executable forward/rollback; prove canonical equality in a disposable same-major database. Schema dumps alone are insufficient authority rollback.
- **Remote retirement:** one frozen source, separate encrypted exact recovery and sanitized history packages; small key roundtrip/encrypt/decrypt proof first, partial-transfer handling, ciphertext/decrypted hashes, expected paths and restore evidence before any removal/account/firewall change or reboot.

## Capacity, privacy, and process gates

Budget operational floor plus peak staging/restore footprint and safety margin; fixed minimum free space is not universally sufficient. APFS logical/du/clone size is not measured reclaimable space. Rollback and schema-probe copies created with APFS clonefile share most physical blocks with the live file: a fully allocated `st_blocks` result does not prove exclusivity. Before promising reclaim, sample physical extents (for example `fcntl(F_LOG2PHYS_EXT)`) against the live file; a large clone can free only a small fraction of its logical size. Report both raw `df` free space and the OS's "available for important usage" capacity: purgeable cloud-sync staging and OS-update snapshots can make them differ substantially. For chunked cloud offload, make each encrypted part independently verifiable and resumable only by regenerating the identical plaintext chunk hash; treat known transient sync errors as bounded retries, not success. A compressed replacement can allocate more physical space than its CoW original. Keep independent recovery until exact proof; do not invent savings.

TCC/FDA failures need exact identity/source classification, not broad shell/interpreter access. Preserve protected staging/encrypted-volume boundaries; do not relocate plaintext sensitive staging to ordinary temp directories to bypass permission failure. Browser-backed profile snapshots need required stopped/listener/process/lock proof. Manual success does not prove scheduled-context TCC behavior; verify real scheduled identity when separately authorized.

For an already-WAL SQLite source, an explicit read transaction plus a schema/read query can pin a stable snapshot before `Connection.backup`, avoiding rolling-copy restarts while normal writers continue. Prove this with a synthetic concurrent-writer test first; never use a write transaction for that backup source. Monitor WAL growth and disk headroom, close the read transaction promptly, and do not claim live completion from the synthetic proof. A large `pages=-1` backup step may not invoke Python progress/deadline callbacks until the step finishes; use an external supervisor and reconcile actual artifact integrity after any timeout.

Benchmark the actual encrypted destination before choosing a multi-gigabyte backup budget. Fast source reads do not establish encrypted disk-image write speed. Preserve encryption rather than moving plaintext into an ordinary staging directory to get a faster result. Where the host filesystem supports it, clone the authenticated encrypted image for restore/index rehearsal instead of modifying the sole verified backup or duplicating decrypted files; verify clone identity and original ciphertext preservation.

Before any retry, reconcile actual OS PID tree, lock owner, stage, logs and durable markers. Tracking loss is not completion. A zombie PID is not an active backup; determine outcome from durable proof. Do not start a second run or delete live staging. One-shot launchd submissions need proven once-only semantics. Restart refusal is not permission to detach or launch an alternate helper around it.

## Retention and rollback

Inventory all relevant backup roots first. Keep purpose/age/class/exact paths and retained replacements visible. Treat source bundles, database snapshots, full secret-bearing packs and nested release evidence differently. Verify replacements through disposable restore; pre-migration rollback and post-migration restore evidence are separate artifacts. No cache deletion while processes execute/map it. Skip drifted/in-use approved targets without substituting new paths.

Partial failure means inspect what happened before retry/removal; retain manifest and exact completed/skipped effects. Report created/retained/deleted items, actual measured space, verified recovery level, unproven boundaries and next approved action. A backup is not a Git mirror; local installation is not remote synchronization.

## Detailed procedures

Load the relevant reference before execution; the restrictions above still apply. Check every command against current tooling and owner authorization:

- `references/encrypted-recovery-proof-before-pruning.md` — prove encrypted, restorable recovery before pruning large backup trees or reclaiming space.
- `references/exact-cache-cleanup-under-active-workloads.md` — exact, process-aware cache cleanup while long-running tools may still be using the caches.
- `references/fresh-backup-and-oldest-rotation.md` — take a verified fresh backup, then rotate out only the oldest existing one.
- `references/git-worktree-archive-recovery.md` — worktree Git supplements, explicit-ref/dirty-source restore proof, encrypted staging and interrupted pack/checkout ownership.
- `references/large-encrypted-sqlite-validation.md` — bounded full integrity checks via caller-owned private mappings, SQLite library identity, and encrypted reopen proof.
- `references/restic-live-file-consistency-race.md` — checksum races on live mutable files during restic recovery proof.
- `references/source-release-archive-restore-proof.md` — source-only release or rollback bundles from an exact Git commit, with restore proof.

No live backup, stop/restart, retention change, third-party receiver installation, credential migration or destructive cleanup is authorized merely by loading this skill.
