# Delayed-result reconciliation

Use by the orchestrator profile after interruption, scope change, delayed delegation, or resume. This is a parent-owned evidence protocol, not a new autonomous runner.

1. Read the current mission handoff and live source first. Identify mission_id, scope_revision, candidate_id, assigned workers, required gates and parent-incorporated result IDs.
2. Validate exact typed identities. Missing/invalid records are not usable proof. A different mission is WRONG_MISSION; a changed scope/candidate is SUPERSEDED. Never infer matching source from titles or recency.
3. Check previously incorporated IDs only after matching mission, scope, candidate and assigned worker. The helper requires a unique `completed_result_bindings` record carrying that full identity tuple plus parent_verified=true; a bare reused result ID is insufficient. Delivery/summary text does not mark incorporation. Duplicate/out-of-order callbacks never authorize repeating external actions.
4. Inspect actual artifact paths, bytes/commits, exit codes and acceptance relevance. An assertion artifact_verified=true is metadata supplied by the parent, not cryptographic proof and never trusted from a child by itself. Failed/malformed outputs cannot become CURRENT proof.
5. Retain required-review obligations explicitly. A stale security finding remains a signal to reproduce on current source; a stale APPROVE is not release evidence. A reproduced current HOLD can reopen a released boundary.
6. Integrate only current verified in-scope work. Record which findings/tests/bytes were incorporated, then update the ledger. Preserve rejected/superseded evidence with reasons and avoid repetitive user notifications when already incorporated.

It cannot authenticate actors, inspect artifact bytes, establish freshness, verify runtime/remote state, mutate a journal, grant approvals or decide release. Use source inspection and required gates for those questions. Do not call it a production authorization or dedupe guard.
