# Encrypted recovery proof before retention pruning

Use this runbook when Hermes backup trees are large, disk headroom is shrinking, FileVault or Time Machine coverage is absent/unclear, or the owner wants to reclaim space without weakening disaster recovery.

## Non-negotiable order

1. Inventory.
2. Create a fresh recovery pack.
3. Encrypt it independently of the storage provider.
4. Verify checksum and archive structure.
5. Restore into a disposable location.
6. Validate the restored control plane without starting live services.
7. Only then approve and execute exact-path pruning.

Do not reverse this order to free space faster.

## Scope inventory

Measure separately:

- `~/.hermes/backups/`
- `~/.hermes/state/backups/`
- `~/.hermes/state-snapshots/`
- profile-local `backups/` and `state/backups/`
- off-machine/cloud recovery-pack directory
- source checkout Git status and local patch coverage
- LaunchAgents and non-Hermes control-plane files
- Obsidian/vault recovery coverage where applicable

Classify each top-level artifact as current full recovery, monthly recovery, change-level rollback, state/DB snapshot, rebuildable cache, quarantine, or unknown.

## Encryption posture

When a pack contains `.env`, auth pools, tokens, customer/runtime state, or full profile rollback data:

- Use archive-level authenticated encryption such as `age` or an encrypted disk image.
- Keep the passphrase/private key out of chat, manifests, shell history, logs, and the archive directory.
- Set `umask 077`; keep temporary decrypted material owner-only.
- Treat FileVault and encrypted Time Machine as additional layers, not substitutes for portable archive encryption.
- If FileVault is off, call that out before creating more plaintext local backup copies. A production restore proof must use an independently encrypted disposable volume; an ordinary `TemporaryDirectory` is acceptable only for synthetic unit tests whose decrypted contents contain no real secrets or business state.
- If the key is provisioned by a setup script, treat that script as the Keychain naming authority. Read its service/account identifiers, make the harness match exactly, and test `KEYCHAIN_READY` without printing or requesting the passphrase in chat. A wrong service/account pair is a harness defect, not an absent-key conclusion.
- Query Keychain once per status operation. Repeated lookups can cause repeated prompts and inconsistent readiness reporting.
- Do not claim standard cloud-at-rest encryption is equivalent to independently controlled archive encryption; account security/advanced-data-protection state may vary.

## Fresh pack contents

Include enough to rebuild the current fleet, not merely yesterday's runtime:

- profile/default configs, SOULs, crons, scripts, plugins, skill/memory state, required secrets/auth, and live databases,
- current LaunchAgent plists and non-Hermes helper scripts,
- source checkout status, current commit, local commits/diff or verified private mirror reference,
- manifests describing excluded rebuildable directories,
- recovery runbook and exact version/install prerequisites.

Avoid embedding redundant `node_modules`, venvs, browser caches, old backup trees, or the backup destination inside itself unless they are explicitly required.

## Verification before restore

Record without exposing secrets:

- archive byte size,
- checksum,
- encryption/decryption test result,
- archive structure test result,
- manifest presence,
- critical-path presence counts,
- age and source commit/profile schema.

A checksum proves transfer integrity, not restoreability.

For archive/extracted-folder deduplication, also compare restored permission modes and extended-attribute names/value hashes. Plain tar archives may preserve every content byte while omitting `com.docker.grpcfuse.ownership` on Docker-produced reports. Keep mismatched originals; do not equate missing metadata with content corruption or silently waive it. When the macOS Python build lacks `os.listxattr`/`os.getxattr`, use `/usr/bin/xattr` and `/usr/bin/xattr -px <name> <path>` as read-only metadata readers, hashing values without printing them. A temporary encrypted-image drill must verify encryption and exact mount identity before extraction, preserve all original backups, and confirm detachment before deleting its exact run-owned image.

## Capture preconditions for browser-backed profiles

Before creating a pack that includes browser-adjacent state:

1. Confirm the expected loopback listener/process is absent.
2. Confirm the browser profile lock (for example `.parentlock`) is absent.
3. Do not delete a lock merely to satisfy the gate; determine whether it is stale and whether the browser was shut down cleanly.
4. If either signal is active or ambiguous, create no production pack and report the exact blocker.
5. Unit tests should mock this host-state precondition so they remain deterministic, then separately test that a synthetic lock/listener causes fail-closed behavior.

## Disposable restore drill

Restore under a new owner-only temporary root only when the host filesystem is encrypted and the pack contains no additional portability requirement. If FileVault is off, create and mount an independently encrypted disposable volume for production proof, restore there, then unmount and destroy it after evidence capture. Never point the drill at live `~/.hermes` and never start gateways, cron tickers, webhooks, tunnels, or platform sends.

Validate:

1. directory ownership and secret-file modes,
2. YAML/JSON config parsing,
3. all cron stores parse and job IDs/counts match the manifest,
4. SQLite `PRAGMA quick_check` on restored databases,
5. skill/reference links resolve,
6. LaunchAgent plists pass syntax checks without loading,
7. source diff/private-mirror recovery instructions are usable,
8. non-network smoke tests run against the disposable HOME,
9. no live platform token is exercised.

Write a restore-evidence artifact containing only status, counts, hashes, versions, and errors—not message bodies, secret values, customer data, raw URLs, or tokens.

## Retention proposal after proof

Offer exact, size-backed tiers:

- **Conservative:** keep two newest verified full packs plus one monthly; remove only clearly superseded change-level directories and rebuildable caches.
- **Balanced:** conservative plus older redundant full packs and expired quarantines after provenance checks.
- **Aggressive:** requires explicit owner approval and a documented reason; may reduce historical monthly points.

For each candidate list:

- exact direct-child path,
- size,
- age,
- class/purpose,
- what newer verified artifact supersedes it,
- rollback consequence if deleted.

## Safe pruning execution

- Back up the deletion manifest itself.
- Delete only explicitly approved direct children; never wildcard a backup root.
- Prefer quarantine/move when provenance is uncertain and sufficient space exists.
- Verify each target is absent and retained packs still pass checksum/archive checks.
- Re-measure free disk and backup-root size.
- Re-run live read-only health checks; storage cleanup should not restart anything.
- Update the recovery runbook's newest verified pack and restore-drill date.

## Browser/profile cache cleanup

Large browser profiles often mix durable auth state with disposable cache. Preserve Cookies, Local Storage, Login Data, Preferences, certificates, and vendor session material unless the workflow owner explicitly accepts re-authentication. Target only proven rebuildable cache directories such as ordinary Cache, Code Cache, GPUCache, and expired quarantine copies, with the browser/listener stopped or using a copied profile for validation.

## Failure handling

- If encryption or restore fails, prune nothing.
- If a database quick check fails only through `mode=ro` on a WAL database, retry on the restored copy with a normal connection plus `PRAGMA query_only=ON` before declaring corruption.
- If the pack omits recent local source commits or control-plane files, rebuild the pack rather than documenting the gap away.
- If available space is too low to stage a full new pack, move/copy one already-verified historical pack to an encrypted off-machine destination first; do not delete the only recovery point.

## Completion evidence

Report:

- fresh encrypted pack created and checksum verified,
- disposable restore path and validation result,
- exact retained recovery points,
- exact approved removals and bytes reclaimed,
- resulting free space,
- FileVault/Time Machine posture as separate owner decisions,
- next scheduled recovery-pack and restore-drill date.
