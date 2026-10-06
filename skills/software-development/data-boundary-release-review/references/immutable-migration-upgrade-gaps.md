# Immutable migration upgrade-gap probes

Use this when a candidate changes SQL functions, ACLs, identifiers, exporter versions, or recovery artifacts inside a migration version that may already be present in the deployment ledger.

## Why fresh-database gates can false-pass

A verifier that creates an empty database and directly applies the edited migration proves only fresh installation. A recovery verifier that restores a regenerated candidate baseline proves only the desired target snapshot. Neither proves that an existing deployment will execute the edited SQL.

If the parent already contains migration version `V` and production has ledger row `V`, changing the contents of `V.sql` does not upgrade production: the standard runner skips it. This can leave old function bodies live while new producers and clients deploy.

Typical consequences:

- a producer bumps its exporter version while the live commit RPC still expects the old version, causing a sync outage;
- stale-generation locks or privacy checks appear in source but are absent from production;
- the candidate baseline and recovery hashes look correct even though the upgrade path never reaches that state;
- an edited rollback drops the original feature instead of reverting only the new upgrade.

## Disposable reproduction

1. Restore the exact parent baseline.
2. Create the real migration-ledger schema and insert the parent migration version `V`.
3. Run the repository's standard migration runner, or faithfully model its ledger decision.
4. Assert whether candidate SQL ran. Inspect `pg_get_functiondef`, ACLs, policies, constraints, and exporter-version literals.
5. Invoke a candidate producer-shaped call against the resulting database.
6. Compare the result with a fresh candidate-baseline restore.

Minimum evidence to print:

```text
LEDGER_PRESENT=true
RUNNER_WOULD_APPLY_CANDIDATE=false
LIVE_FUNCTION_HAS_NEW_GUARD=false
CANDIDATE_PRODUCER_CALL=<failure or old behavior>
```

## Required remediation

- Never rely on edits to an already-ledgered migration for an upgrade.
- Add a new, strictly higher migration version containing the `CREATE OR REPLACE`, constraint, data-conversion, or ACL changes.
- Give the new migration its own rollback that restores the immediate parent state; do not reuse the original feature-removal rollback.
- Regenerate the recovery baseline only after the upgrade migration exists.
- Gate parent baseline + existing ledger + standard runner against the fresh candidate baseline using canonical object, ACL, policy, and function-definition fingerprints.
- Run producer healthy controls and adversarial fixtures against the upgraded parent path, not only against a fresh install.

## Adjacent boundary checks

When the upgrade changes pseudonymous identifiers, validate treatment of pre-existing raw identifiers during the transition. Before the first successful new generation, authenticated RPCs must not expose old privacy-bearing keys; clients should fail closed, and the migration should intentionally clear, convert, or quarantine incompatible canonical rows.
