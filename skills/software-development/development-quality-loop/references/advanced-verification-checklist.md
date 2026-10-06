# Advanced verification checklist

Select applicability before implementation. Applicable security, recovery, and acceptance gates remain mandatory; this is not a universal per-edit checklist.

## Verification Checklist

- [ ] For deployed management dashboards, live artifact identity, isolated build health, data-truth semantics, and authority boundaries were verified as separate evidence lanes.
- [ ] Every protected SPA route was authenticated and asserted by a unique route landmark after clean-path reload; a generic sign-in shell or HTTP 200 was not accepted as route proof.
- [ ] Test discovery/scripts were compared with actual test files so an omitted suite could not hide behind a green canonical command.
- [ ] Protected JSON responses were checked for `private, no-store`, authorization variance, minimized browser projections, and security headers.
- [ ] Shared files audited by subagents were isolated in a snapshot or hash-checked before and after delegation.
- [ ] Git-dependent release gates ran in a disposable Git worktree/clone, not a metadata-free archive; shallow-CI invariants do not assume unavailable history.
- [ ] Expected test files and collection counts were checked before and after the suite when shared-state cleanup was possible.
- [ ] Sparse cross-repo integrations were built from a dependency-complete canonical overlay in a detached target worktree, not from today's diff alone.
- [ ] Multi-FK foundation tables were probed for same-tenant semantic mismatches with synthetic A/B aggregates; RLS and read-only ACLs were not treated as relationship-integrity proof.
- [ ] Every new fail-closed validator has both an adversarial rejection test and a canonical healthy-artifact acceptance test; production-adjacent releases also include sanitized installed-runtime readback when authorized.
- [ ] Chosen phase(s) match task risk.
- [ ] Root cause or acceptance criteria stated before implementation.
- [ ] Tests/commands run with real output.
- [ ] CI-parity tests ran in an environment containing only declared workflow dependencies, or host-framework imports were replaced with explicit test doubles.
- [ ] For multi-repo pushes, every latest workflow run completed successfully on the exact local/remote branch-tip SHA.
- [ ] Any reviewer dispatched as a release gate completed, was explicitly canceled with the missing evidence documented, or left the verdict unresolved; no required review handle is merely pending.
- [ ] The release verdict targets a commit created after the last remediation; any review of an earlier commit is marked superseded and is not used as exact-tip evidence.
- [ ] PostgreSQL ACL migrations use exact signature/set equality rather than aggregate counts or prefix-based regrants; direct grants are proven with normalized ACL rows, not effective-privilege helpers.
- [ ] ACL migration drift probes cover a missing direct service grant hidden by `PUBLIC`, a count-preserving identity swap, atomic failure with no partial ACL changes, and ledger-aware exact rollback parity.
- [ ] External-mutation release reviews injected commit-then-timeout, concurrent human-state drift, corrupt/unreadable journal, local-day-cap, and caller-supplied trigger-spoof cases; mutator calls stayed at zero or one as required, and every ambiguous outcome halted without retry.
- [ ] Any timed-out delegated worker was inspected before cleanup; valuable tracked and untracked changes were preserved, hashed, and reviewed as untrusted partial work.
- [ ] Operational candidate verification used a supported exact-worktree/clone boundary rather than weakening canonical path guards.
- [ ] Forward-only database changes retained separate pre-migration rollback and post-migration restore-proof backups, with direct migration-ledger/schema readback between them.
- [ ] Any historical migration assertion over forced-RLS tables was proven non-vacuous across all tenants: the actual migration rejected a malformed non-default-tenant fixture under its real wrapper/role sequence, emitted the exact expected constraint, and left no ledger row or persistent elevated callable surface.
- [ ] The real-wrapper historical-upgrade probe is a maintained canonical verifier, not a one-session temporary script; it also proves healthy replay, exact checksum ledgering, helper cleanup, collision-resistant disposable-clone naming, fail-closed teardown with direct absence readback, and no accepted-database mutation.
- [ ] Restore verification independently recomputes the tightened semantic invariant in source and restored databases and proves the rejection path non-vacuously with retained healthy subjects or a healthy→malformed→repaired restored-clone mutation probe; source/restore fingerprint equality or `violations = 0` over an empty subject set is not accepted.
- [ ] The exact promoted-table/migration set was propagated through manifest/validator allowlists, UAT baseline fingerprints and persisted-row counts, tenant/no-context RLS probes, restore/security hashes, and verifier output; emitted counts are asserted from live queries rather than printed constants alone.
- [ ] Every accepted zero-result ACL/RLS/security check also proved the exact expected subject identities/cardinality existed.
- [ ] Each PostgreSQL security subject family used one canonical identity set across existence, forbidden-privilege, live/restore, emitted-count, and static-contract checks; no independently maintained subset or printed constant can claim full coverage.
- [ ] Disposable-resource cleanup was verified twice: each run removed its exact resources, and a final family-wide PostgreSQL/container census covered current plus legacy/debug UAT, upgrade, and restore prefixes with the declared allowlist (normally zero).
- [ ] Temporary in-tree dependency links/generated artifacts were removed before whole-tree validators, secret scans, and final clean-status assertions.
- [ ] Diff reviewed.
- [ ] Final response includes changed files, verification, and blockers/risks.
