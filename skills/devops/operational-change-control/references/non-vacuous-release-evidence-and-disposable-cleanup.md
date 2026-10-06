# Non-vacuous release evidence and disposable cleanup

Use this procedure when a release depends on database migrations, restore proofs, disposable test environments, or exact-tip reviewer approval.

## 1. Treat reviewer HOLDs as executable evidence defects

- Keep release blocked on every reproducible critical/high/medium finding.
- Remediate the verifier or product contract, not only the prose.
- Convert each accepted finding into a maintained regression assertion or deterministic probe.
- Freeze a new immutable commit after remediation and re-review only the bounded delta plus directly affected contracts.
- Re-run release evidence on the final tree. Do not cite UAT IDs or scan output from an earlier remediation tree as final-tree evidence.

## 2. Build non-vacuous migration and restore probes

A verifier is insufficient when the accepted database happens to contain zero rows of the state being checked.

For migration assertions:

1. Create a collision-resistant disposable clone (UUID/random cryptographic suffix, not second-resolution timestamps).
2. Construct a fixture that satisfies every unrelated invariant: one tenant throughout, valid parent rows, valid foreign keys, valid principal/role/assignment relationships, and the canonical template.
3. Introduce only the defect under test.
4. Invoke the real role, transaction, migration-wrapper, and ledger path.
5. Prove rejection identifies the expected constraint, rolls back, creates no ledger row, and leaves no elevated helper behind.
6. Remove the defect, run the healthy path, and prove exactly one correct ledger row plus helper cleanup.

For restore semantics:

1. Compare the full canonical contract, not a convenient subset. Include template identity/status/synthetic predicates and every item tuple field that defines equality.
2. Create one valid terminal fixture so the check cannot pass vacuously.
3. Prove the exact fixture yields zero violations.
4. Mutate a field previously easy to omit (for example a section/item title) and prove exactly one violation.
5. Mutate a template predicate (for example active status) and prove exactly one violation.
6. Restore both mutations, delete the probe data, and prove data/security/contract fingerprints reconverge.

Use explicit `if ! check; then die ...; fi` or equivalent for release-critical assertions. Do not rely solely on shell `set -e`; invocation context and compound commands can make errexit behavior surprising.

### Forced-RLS upgrade backfills

A table/schema owner remains subject to `FORCE ROW LEVEL SECURITY`. A migration can add nullable baseline columns, run an `UPDATE` that sees zero historical rows, and then fail at `SET NOT NULL`; an owner-run assertion can likewise pass vacuously.

For a bounded historical backfill:

1. Reproduce against a non-empty Phase N-1 clone, not only a fresh database.
2. Add the new columns as nullable.
3. Inside the schema-owner migration transaction, either temporarily `DISABLE ROW LEVEL SECURITY` on only the affected table or use an explicitly authorized bootstrap/BYPASSRLS transaction-local path.
4. Backfill and validate historical rows.
5. Apply `NOT NULL`/check constraints.
6. Restore both `ENABLE ROW LEVEL SECURITY` and `FORCE ROW LEVEL SECURITY` before commit.
7. Read back populated-row cardinality plus `relrowsecurity` and `relforcerowsecurity` flags.
8. Keep the pre-migration rollback backup distinct from the post-migration restore-proof backup.

If policy forbids temporary RLS disablement, complete per-tenant enumeration is acceptable only when completeness is independently proven. Schema ownership or a same-owner `SECURITY DEFINER` function is not global visibility under forced RLS.

### Verify returned values, not function-row cardinality

For a function that returns one scalar row, this expression verifies the wrong property:

```sql
SELECT count(*) FROM app.reconcile_inventory();
```

It returns `1` because it counts the function's output row, even when the reconciliation value is zero. Read the scalar directly:

```sql
SELECT app.reconcile_inventory();
```

Then prove non-vacuity separately by asserting the exact expected subject identities/cardinality. Release harness errors should print sanitized actual values (for example `movements=4 reconciliationViolations=0`) instead of one opaque combined failure.

### Replay locking reads after least-privilege ACL changes

After revoking table-level `UPDATE`, execute every runtime `SELECT ... FOR UPDATE/SHARE` as the application role. PostgreSQL locking reads require update authority and can turn an intended domain 4xx response into a sanitized 500. When a parent lock already serializes all child mutations, remove only the redundant child lock; do not widen ACLs merely to satisfy an unnecessary locking read. Keep a regression assertion proving the parent lock remains and the unauthorized child lock does not.

## 3. Make disposable cleanup part of the gate

- Track whether each resource was actually created.
- Cleanup on every exit path, retry bounded termination/removal, and make cleanup failure override an otherwise successful exit.
- Read back resource absence from the authoritative inventory (for example `pg_database` and `docker ps -a`).
- Emit `PASS` only after absence is proved.
- Before release, scan globally for stale resources from earlier runs, including debug variants—not just resources created by the latest verifier.
- A stale container/database/network/volume is a release HOLD when the acceptance contract says every clone is destroyed.

When stale resources exist:

1. Inventory exact names and ownership first.
2. Exclude accepted/primary resources explicitly.
3. Obtain user approval for destructive cleanup.
4. Remove only the approved exact resources.
5. Verify zero leftovers and re-check accepted database/service health.
6. Re-run the release-evidence review.

If the execution approval bridge blocks a destructive action, do not bypass it with an indirect script, GUI automation, or arbitrary-code runner. Pause for explicit approval or have the user execute the exact commands. If Docker/database infrastructure is stopped, obtain separate approval before starting or restarting it because that affects all local workloads.

## 4. Exact-tip closeout

Require all of the following on the immutable tip before release:

- clean worktree and expected commit/tree identity;
- private/default-branch and fast-forward ancestry verification;
- unit/integration/runtime/security/dependency gates;
- non-vacuous migration and restore probes;
- two final-tree disposable UAT runs where required;
- global zero-leftover inventory readback;
- independent specification, security/transaction, and release-evidence APPROVE verdicts.

Only then fast-forward the private default branch, verify remote/local identity, and publish the handoff.
