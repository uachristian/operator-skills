# Read-model producer commit attestation

Use this reference for scheduled producers that read third-party APIs, sanitize a bounded projection, and persist it through an RPC or database commit function.

## End-to-end acceptance contract

Treat source fetch, projection, commit, and scheduler outcome as one state machine:

1. **Source envelope accepted** — required list and pagination/total metadata are shape-valid.
2. **Window complete** — for a “latest N” contract with a source total, require `returned_count == min(source_total, N)`.
3. **Projection usable** — every row sanitizes, identity is unique, required secondary windows are independently complete, and no cap/truncation/future-time failure occurred.
4. **Commit confirmed** — parse the RPC body and require the server-observed generation identity, terminal status, accepted count, and `decision_usable=true`.
5. **Process success** — only after the commit confirmation; CLI exit zero is a receipt for database acceptance, not merely local computation.

HTTP 2xx proves only transport completion. A database may legitimately downgrade an apparently complete generation after contraction, invariant, or concurrency checks.

## Required credential-free probes

Stub the real transport boundary and run the production parser/state machine:

- malformed 2xx body where the list field is missing;
- source total at least N with 0, 1, and N-1 returned rows;
- valid primary window with malformed or incomplete secondary metadata;
- one malformed lane/page among otherwise valid lanes;
- RPC HTTP 200 with `status=partial` or `decision_usable=false`;
- RPC response whose generation ID/count does not match the attempted projection;
- healthy complete source plus matching commit response.

For each negative case require: no trusted-current publication, nonzero process exit, bounded sanitized diagnostics, and preservation of the previous canonical projection.

## Common destructive chain

An incomplete window can be mislabeled complete, causing replacement logic to delete prior rows absent from the short response. A client may then compare `accepted_count` only with the now-short stored list and display a trustworthy zero. Review producer, database replacement semantics, snapshot RPC, browser normalizer, and freshness classifier together; testing only the sanitizer misses this chain.

## Runtime and connector parity probe

A healthy MCP connector or legacy helper proves that the provider and credential are available through *that* transport; it does not prove the candidate's standalone producer. Before blaming credentials, compare only non-secret evidence (presence, length, and a one-way fingerprint), then inspect the exact candidate's authorization scheme, headers, query encoding, timeout, and envelope parser against a known-good connector. Run the exact candidate runner in read-only/dry-run mode and require aggregate reconciliation with zero dropped rows. Never print the credential or unrestricted provider payload.

Also resolve the installed scheduler's real working directory, module import path, interpreter/dependency path, and environment source. A passing script in an isolated worktree is not runtime parity when supervision still imports the legacy checkout. Bind the schedule to the reviewed release identity, or keep release on HOLD.

## Operational handoff

A producer is not release-ready merely because a standalone script exists. Require protected CI coverage for its migration verifier, installed schedule/supervision, semantic failure alerting, exact runtime-source identity, protected Preview invocation against an isolated target, executable rollback, and post-migration restore evidence.
