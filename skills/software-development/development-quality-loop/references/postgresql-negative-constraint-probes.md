# PostgreSQL Negative Constraint Probes That Fail for the Right Reason

Use this pattern when a release gate must prove that PostgreSQL rejects an invalid relationship, state transition, or authorization mutation. A test that treats **any** SQL error as success is vacuous: a misspelled column, missing table, bad cast, or denied connection can make the gate green without reaching the intended constraint.

## Core rule

A negative database probe passes only when all three are true:

1. the connection and setup statements reach the target mutation under the intended application role;
2. the mutation is rejected;
3. stderr identifies the exact expected constraint or PostgreSQL error class.

Pair the negative probe with a valid rollback-only positive control when practical so the harness is proven selective rather than fail-shut.

## Shell pattern

```bash
probe_error="$(mktemp)"
trap 'rm -f "$probe_error"' EXIT

if role_psql app_role app_password product_db \
  -v ON_ERROR_STOP=1 -Atq \
  -c "BEGIN;
      SET LOCAL app.tenant_id='00000000-0000-4000-8000-000000000001';
      INSERT INTO app.child (...invalid same-tenant composite relationship...);
      ROLLBACK;" \
  >/dev/null 2>"$probe_error"; then
  echo "invalid relationship unexpectedly accepted" >&2
  exit 1
fi

if ! grep -Fq 'violates foreign key constraint "child_parent_scope_fkey"' "$probe_error"; then
  echo "negative probe failed for an unexpected reason" >&2
  exit 1
fi

rm -f "$probe_error"
trap - EXIT
```

Use `ON_ERROR_STOP=1`; otherwise `psql` can continue after the target error and return success. With fail-fast enabled, the connection closes while the transaction is aborted, so the probe remains rollback-only even when the explicit `ROLLBACK` is not reached.

## Same-tenant integrity matrix

RLS and independent foreign keys do not prove that a composite relationship is valid. Probe combinations where every individual identifier exists in the same tenant but the tuple is inconsistent:

- child names job A but work order B;
- work order names customer A but an asset owned by customer B;
- labor names technician A but job/order B;
- staff-only assignment names a non-staff principal.

Use composite `UNIQUE` targets and composite foreign keys when those values must agree as a unit. If the original migration is checksum-registered, add a new append-only remediation migration rather than rewriting history.

## Preventing harness drift

- Read canonical DDL before writing the probe; copy real column and constraint names.
- Use unique synthetic probe identifiers and the least-privileged application role.
- Capture stderr only long enough to classify the failure; never print credentials or connection strings.
- Add a static contract assertion for the canonical column list and expected constraint name.
- Query `pg_constraint` or replay migrations in disposable PostgreSQL to prove the named composite constraint exists.
- If the probe creates setup rows before the expected failure, use one transaction and ensure an unrelated setup error cannot satisfy the gate.
- Report the exact constraint reached, not merely `BLOCKED`.

## Failure mode to guard against

A negative probe that references a column name not in the real schema (for example `<table>.name` when the schema defines `<table>.display_name`) fails with `undefined_column` before the composite foreign key is ever exercised. If the harness accepts any nonzero `psql` result, that failure is misread as "constraint enforced". Capture stderr and require the expected constraint name in the error; then keep the probe as a durable regression contract.
