# Identifier, stale-replay, ledger, and recovery-body probes

Use these probes when a remediation fixes the originally reported source path but equivalent privacy, ordering, or recovery defects may remain in sibling sources.

## 1. Enforce semantic identifier privacy end to end

For every producer, inject contact/customer-shaped values into each identifier accepted as a row key, domain key, deep-link key, or browser `id`:

- `victim@example.com`
- an international phone-shaped value
- a VIN-shaped value
- an account/customer-shaped value

Trace the accepted row through producer normalization, SQL ingestion, persistence, authenticated RPC, browser normalization, change facts, export/clipboard, and deep links. A projection that remains `complete` or `decision_usable` while serialized browser output contains the injected value is a privacy-boundary failure.

A non-empty-string check is not an identifier contract. Prefer keeping raw provider IDs inside the producer and publishing a domain-separated digest identity such as `<source>_<96-bit-hex>`. Independently enforce the published grammar in producer output, SQL, and browser normalization. Assert determinism, expected digest length, and absence of every raw adversarial identifier from serialized output. Keep user-facing business references such as order numbers separate and narrowly validated; do not overload a pseudonymous internal key as display copy.

If raw IDs must cross a boundary, enforce the canonical provider grammar independently at every layer and separately reject contact-shaped values. Do not derive visible labels from raw prefixes/suffixes.

## 2. Make generation authority monotonic

Rejecting only future timestamps does not stop an older, slower run from overwriting newer facts.

Producer contract:

1. Capture `source_observed_at` immediately before provider collection begins—not after fetch completion.
2. Preserve that timestamp through persistence and error reporting.
3. Never mint a newer authority timestamp merely because an old collection finished later.

SQL accepting-boundary contract:

1. Acquire a transaction-scoped advisory lock keyed by dashboard/source.
2. Under that lock, read the maximum prior source observation time.
3. Reject `incoming_time <= prior_time` before inserting a usable generation or mutating canonical facts.
4. Reconcile all counts and semantic fields before promotion.
5. Keep canonical facts unchanged on rejection.

Disposable probes:

- Commit a recognizable generation at `T2`, then replay different facts at `T1 < T2`; require the exact stale-generation failure and unchanged canonical facts.
- Run a true overlapping-commit race so the lock/compare occurs after waiting; generation IDs and completion order are not authority.
- Pair every rejection with a producer-built current healthy control.

Use real advancing clocks in multi-commit SQL fixtures. PostgreSQL `now()` is transaction-start stable, so repeated calls in one transaction can accidentally share a timestamp and either false-pass or fail for the wrong reason. Use explicit timestamps or `clock_timestamp()` and assert the exact failure reason.

## 3. Verify rollback ledger parity

An executable rollback is incomplete when it drops candidate objects but leaves the migration runner's ledger row. The runner may skip reapplication while the schema remains absent.

Required disposable sequence:

1. apply migration;
2. insert or confirm the exact ledger row;
3. verify target objects and ACLs;
4. run rollback;
5. verify object absence and ledger-row absence;
6. invoke the standard runner or faithfully model its ledger decision;
7. verify reapplication and target parity.

A direct `migration.sql → rollback.sql → migration.sql` loop does not test ledger handling. Guard ledger deletion only when the metadata table may legitimately be absent in isolated tests, and compare sibling rollback artifacts for the production convention.

## 4. Bind recovery to function behavior

Object counts, signatures, ACLs, and names are substitution-blind. `CREATE OR REPLACE FUNCTION` can preserve all of them while replacing a security-critical body with `{}` or a no-op.

For every new critical RPC/mutator:

1. Register the exact `regprocedure` in one canonical subject set.
2. Hash normalized `pg_get_functiondef` output in the recovery manifest.
3. Restore the baseline and run a healthy behavioral fixture against the restored function.
4. Replace one function with a same-signature broken body.
5. Recompute the fingerprint and require a mismatch.
6. Run the behavior fixture inside a transaction and roll it back so recovery still proves a data-empty baseline.

When regenerating a public-schema baseline from a parent plus candidate migration, preserve the established dump convention. In particular, dropping `GRANT`/`REVOKE` statements with `--no-privileges` can create a schema that restores structurally but fails authority probes. After regeneration, recompute the schema, ACL, object-identity, and critical-function fingerprints from the restored candidate—not only from the source database used to dump it.

## Reporting

When maintained gates pass despite one of these probes, report the implementation defect and verifier gap separately. Include the accepting sequence, observed final state, narrow remediation, and exact regression. A reviewed commit becomes superseded immediately after remediation; require a new immutable tip and exact-tip rereview before release.
