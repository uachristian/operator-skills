---
name: external-action-boundary-review
description: "Use when reviewing wrappers around outbound messages, filesystem writes, or other external mutations: dry-run, retries, idempotency, receipts."
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [security-review, reliability, outbound-actions, filesystem-mutations, bounded-workers, idempotency, receipts]
---

# External Action Boundary Review

## Purpose

Use this skill for focused read-only reviews of code that can send messages, publish artifacts, update remote systems, trigger deployments, mutate canonical files on stall-prone storage, or perform another externally visible mutation. The critical boundary is the **lowest real mutator**, not merely the host wrapper or subprocess invocation.

The main failure class is a wrapper that appears manual, fixed-target, one-shot, and fail-closed while a downstream CLI/SDK silently retries, chunks, reformats, reroutes, or returns weak evidence.

Detailed manual-message review procedures and bounded probes are in `references/manual-outbound-delivery-adversarial-review.md`.

For exact-archive production deployment and alias/promotion wrappers, use `references/production-deployment-wrapper-adversarial-review.md`: it covers mandatory manifest binding, lowest-boundary alias-drift checks, symlink TOCTOU swaps, full metadata readback, API payload-type validation, one-create call accounting, executable rollback, fake-transport probes, and concurrent wrapper-hash drift.

For durable filesystem captures and other source-backed mutations, use `references/bounded-filesystem-mutation-capture-review.md`: it covers full metadata/path containment inside a killable worker, deterministic source markers plus bounded receipts, commit/log/queue outcome classification, and actual-process crash probes before commit, after commit, and before required coordination.

For scheduled third-party read-model producers, use `references/read-model-producer-commit-attestation.md`: it covers bounded-window completeness, malformed 2xx envelopes, independently complete secondary windows, database-semantic commit confirmation, destructive short-window replacement chains, and Preview/scheduler/rollback handoff gates.

## Core workflow

1. Freeze the exact diff/commit, scoped status, and file hashes. Recheck after tests and before the verdict.
2. Map untrusted inputs to the final action boundary: destination, body, media/directives, credentials/profile, mode flags, and receipt identity.
3. Trace the exact installed/current downstream CLI, SDK, adapter, or helper reached by production argv. Do not infer its behavior from wrapper mocks.
4. Build a truth table for dry-run, confirmation, live action, existing receipt, uncertain attempt, and retry/reconciliation states.
5. Distinguish one wrapper invocation from one external mutation. Inspect retries, fallbacks, chunking, pagination/fanout, and provider idempotency.
6. Validate final transport units after formatting/escaping. If one logical action can fan out, journal and receipt every part and test partial success.
7. Require destination evidence from the provider response, not an echo of the requested destination.
8. Audit receipt schema, path safety, atomicity, authenticity assumptions, and crash windows.
9. For source-backed filesystem writers, prove the parent never touches source metadata, separate canonical commit from required coordination and secondary logs, and inject real worker-death windows before commit, after commit/before receipt, and after promotion/before queueing.
10. Run bounded no-network probes using real parsers/formatters/state machines with fake transports.
11. Rank findings by reachable external impact and issue an explicit APPROVE/HOLD recommendation.

## Invariants

- A dry run returns before locks, journals, credential loading, executable checks, and transport.
- A live action requires the complete intended approval gate; ambiguous CLI abbreviations are disabled when exact flags are part of the contract.
- Untrusted artifacts cannot select destination, profile, executable, transport mode, media, buttons, callbacks, or promotion behavior.
- Evidence is revalidated from trusted current sources; every claimed provenance hash is bound, not merely shape-checked.
- One logical action causes at most one external mutation unless multipart behavior is explicit, fully journaled, and fully receipted.
- Commit-then-error ambiguity never triggers an automatic retry without a provider-supported idempotency key.
- Success receipts contain strict identities and server-observed result fields; malformed or partial receipts fail closed.
- Failed/uncertain attempts block automatic retry and produce a manual reconciliation path.
- Secret-like input and transport directives are rejected at every artifact surface that policy claims to validate.

## Verification requirements

Prefer local, credential-free tests:

- actual parser tests for dry-run and approval flags;
- lowest-level transport call counts under transient failures;
- real formatter plus platform length/chunk calculations;
- fixed-route argv and no-shell assertions;
- path escape, direct-child, symlink, oversized, and TOCTOU-aware file checks;
- strict receipt readback, malformed/forged receipt cases, and crash-window state transitions;
- destination mismatch using the real result-normalization path;
- positive healthy controls alongside every adversarial rejection.

Do not invoke live delivery, network access, credentials, or production writes unless explicitly authorized.

## Reporting format

Return:

1. release recommendation (`APPROVE` or `HOLD`),
2. findings ranked critical/high/medium/low with exact file/line evidence,
3. direct answers for route injection, transport controls, evidence bypass, duplicates, receipt forgery, secret leakage, and dry-run escape,
4. test/probe commands and real outcomes,
5. explicit evidence boundaries and residual trust assumptions.

A green wrapper test suite is not proof of one provider mutation when the runner is mocked. State precisely what each test proves and what remains downstream.

## Pitfalls

- Counting subprocess invocations instead of provider calls.
- Treating HTTP 2xx from a persistence/RPC boundary as semantic success. Parse the returned generation/result, require the database-confirmed terminal state and identity, and make CLI/process success follow that result; probe HTTP 200 plus `partial`/`decision_usable=false`.
- Trusting documentation that says “no retry” without inspecting the downstream sender.
- Bounding raw characters before Markdown/HTML escaping and platform formatting.
- Recording only the last message ID after a multipart send.
- Treating request-echoed `chat_id` as provider attestation.
- Calling an unsigned local receipt “unforgeable” without defining the state-directory trust boundary.
- Reviewing moving worktree line numbers after another process commits remediation.
- Counting reviewer process exit code, token usage, or API-call activity as a verdict when the final artifact is missing, unparseable, targets a superseded tip, or records `completed=false`. Keep the release unresolved; fix or replace the evidence channel, and do not repeatedly redispatch the unchanged broad review.
- Treating unused malicious sidecar content as transport injection; report policy mismatch separately from reachable external impact.
