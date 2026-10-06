---
name: data-boundary-release-review
description: "Use when reviewing SQL, RPC, or API release candidates for privacy and data-boundary leaks before they ship."
version: 1.0.5
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [security-review, data-boundary, postgresql, acl, privacy, release-review]
    related_skills: [development-quality-loop]
---

# Data-Boundary Release Review

## Overview

Use this class-level skill for exact-commit, blocker-only reviews of systems that ingest untrusted external data, minimize it into SQL-backed projections, expose it through authenticated RPCs, and drive browser decisions or review cursors.

The central question is not whether each layer looks sanitized in isolation. It is whether malformed, partial, stale, mis-scoped, privacy-bearing, or concurrently reordered source data can cross the complete producer → database → ACL/RLS → RPC → browser → recovery boundary and still be labeled trustworthy.


For compact reproductions covering contradictory error-bearing success envelopes, raw-identifier-derived pseudonym leaks, capped-feed cursor skips, and recovery-verifier registration gaps, see `references/error-envelopes-pseudonyms-cursors-and-recovery.md`.


For reusable probes covering contact-shaped identifiers in sibling sources, delayed/out-of-order generation replay, timestamp-capture timing, and migration-ledger rollback parity, see `references/identifier-replay-and-ledger-probes.md`.

For the false-green upgrade pattern where a candidate edits an already-ledgered migration, so fresh installs and regenerated recovery baselines pass while the standard runner skips production changes, see `references/immutable-migration-upgrade-gaps.md`.


## When to Use

- A dashboard or decision engine imports SaaS/API data into PostgreSQL or another durable snapshot store.
- A release adds `SECURITY DEFINER` ingestion or browser-read RPCs.
- The task mentions data boundaries, RLS, ACLs, privacy minimization, fail-closed behavior, review cursors, snapshot provenance, or recovery parity.
- A maintained migration/recovery verifier may pass despite missing candidate objects or adversarial source cases.

## Review Workflow

### 1. Freeze the immutable target

Record exact commit, tree, parent/baseline ancestry, changed paths, and tracked status. Recheck commit/tree/status after executable probes and before the verdict. Prefer a detached exact worktree or immutable Git-object reads when the checkout can move.

Separate the verdict into evidence lanes:

1. external producer correctness;
2. database ingestion and provenance;
3. RLS/ACL/role behavior;
4. browser projection and semantic privacy;
5. cursor/pagination state machines;
6. recovery and rollback target state;
7. maintained verifier completeness.

A green result in one lane does not prove another.

### 2. Trace the full accepting path

Map every untrusted field and metadata claim through:

- HTTP status and response envelope;
- pagination/window completeness;
- scope/lane/tenant identity;
- producer normalization and semantic minimization;
- database ingestion validation;
- persisted generation/provenance records;
- authenticated projection RPC;
- browser normalization and decision gating;
- review/acknowledgement cursors;
- backup, restore, and rollback verification.

Do not stop at a key allowlist. Allowed fields can carry forbidden semantics.

### 3. Probe external envelopes adversarially

Use credential-free fake transports and healthy controls. Include:

- HTTP 2xx with non-empty `error` or `errors` plus plausible `data`;
- missing, null, partial, or contradictory pagination metadata;
- wrong returned scope/lane despite a correct request filter;
- missing `archived` versus explicit `archived: false`;
- duplicate identities across pages/scopes;
- source total larger than the received declared window;
- cap-plus-one rows;
- future timestamps and malformed falsey containers.

Require explicit clean success, terminal pagination, exact count arithmetic, and returned-scope identity. Never relabel a row from the requested filter without checking the response row.

### 4. Audit semantic privacy

Check whether allowed display strings can contain forbidden customer/contact data. Free-form labels, generated names, notes disguised as descriptions, and provider-composed vehicle/item names are high risk even when customer/phone/email keys were dropped.

Prefer labels built from separately validated structured components only when every component is constrained by a closed vocabulary or another independent semantic validator. A field named `make`, `model`, `description`, `generatedName`, or `id` is still untrusted and can carry customer/contact data. Pseudonyms must never be a visible prefix or suffix of the raw provider identifier: reject contact-shaped identifiers and derive display tokens from a domain-separated cryptographic digest or a server-held mapping. When no robust validator exists, intentionally downgrade the display to a coarse non-sensitive token derived from a narrow primitive (for example, `2020 vehicle`) or omit it. Test forbidden content in prefixes, suffixes, Unicode forms, nested aliases, raw identifier shapes, and otherwise valid-looking values. Trace each accepted string and identifier to every RPC, renderer, clipboard/export, print, deep-link, and browser state surface.

### 5. Revalidate at the SQL ingestion boundary

A trusted service role does not excuse malformed producer output. The lowest ingestion function should independently enforce:

- exact source/schema/exporter version;
- exact scope key-to-provider-ID mapping;
- row/page/window caps;
- per-scope terminal pagination;
- exact count equations;
- no duplicate identities;
- timestamp and value bounds;
- monotonic or CAS generation authority where delayed/concurrent producers are possible;
- exact allowed-key and semantic field contracts.

Do not store caller-supplied provenance counts without reconciliation. Parse the database RPC receipt after HTTP 200 and require returned status, usability, generation identity, and accepted count to match the producer claim.

### 6. Exercise RLS and ACLs as real roles

Inspect direct grants, effective grants, function owners, `SECURITY DEFINER`, `search_path`, RLS/FORCE state, policies, schema usage, and default privileges. Then execute role-realistic probes for anonymous, viewer, editor, admin, and service identities.

Compare behavior with the frozen authorization contract. For every denied mutation, assert zero state change. Pair denials with positive controls for each authorized role. Personal-state writes still violate a contract that explicitly says viewers are read-only.

### 7. Model review cursors as a paging state machine

Require exact equality between emitted change types and scoped query filters. Constrain the vocabulary in SQL when practical.

For capped feeds:

- return `has_more`;
- return the highest ID actually delivered;
- compute latest IDs per scope;
- allow CAS advancement only through the delivered boundary;
- never acknowledge unseen rows.

Test `limit + 1` changes and every transition type. A global latest ID paired with a limited page is a classic silent-skip defect.

### 8. Verify recovery and rollback against the candidate target

A recovery harness can pass while restoring a stale schema baseline that omits the release. It can also false-pass in the opposite direction: a regenerated candidate baseline contains the desired function bodies, but the candidate merely edited a migration version already recorded in the parent deployment ledger, so the standard runner never installs those bodies. Before comparing schemas, diff migration identities against the parent. Treat any security- or contract-relevant edit to an already-ledgered migration as an upgrade blocker unless a new higher migration carries the change.

Compare:

1. the committed target baseline restored fresh; and
2. the parent baseline plus exact ordered candidate migrations, applied through the standard runner with the parent ledger present.

Require canonical equality for object identities, policies, RLS/FORCE, owners, direct/effective ACLs, security-critical function definitions/search paths, and trigger bindings. Register new objects in source validators, recovery manifests, subject sets, critical-function hashes, and role probes in the same change batch.

Require executable transactional rollback, not a prose drop order. Prove apply → target verification → rollback normalized parity and ledger handling → standard-runner reapply.

Recovery integrity must bind behavior, not only object names, signatures, ACLs, and aggregate counts. Add every new security-critical `regprocedure` to the canonical function-definition subject set, hash normalized `pg_get_functiondef` output, execute a healthy restored-baseline behavior probe, then replace one function with a same-signature broken body and require the recovery verifier to fail. Run behavioral fixtures transactionally and roll them back so the restored baseline remains data-empty. When regenerating a public-schema baseline, preserve the repository's established privilege-dump convention; omitting grants can produce a structurally correct dump with unsafe or broken restored authority.

## Minimum Adversarial Matrix

- Producer-built healthy controls for every source.
- 2xx error-bearing/malformed envelopes.
- Wrong returned scope and missing archived flag.
- One-of-many, cap-plus-one, and count-equation mismatches.
- Duplicate IDs and forged SQL provenance.
- Contact-shaped identifiers through every producer, SQL, RPC, browser, export, and deep-link path—not only the originally reported source.
- Allowed-field PII suffix/prefix attacks.
- Newer generation followed by explicit stale replay, plus a true overlapping-commit race.
- Every change type through every scoped feed.
- `LIMIT + 1` cursor acknowledgement.
- Anonymous/viewer denials and editor/admin/service positive controls.
- SQL direct-call malformed-input rejection.
- Parent+ledger+standard-runner migrations versus target-baseline equality, including a candidate producer healthy control against the upgraded parent.
- Failed-apply atomicity and rollback parity, including migration-ledger deletion and standard-runner reapply.
- Restored-baseline healthy behavior plus same-signature critical-function body tamper detection.

## Reporting

Start with `APPROVE`, `HOLD`, or `BLOCK`. Report only reproducible release-blocking/high defects unless the user requests broader review. Each finding must include:

- exact file/line evidence;
- exploit or failure sequence;
- observed probe result when executable;
- narrowly sufficient remediation;
- required regression test.

State when maintained gates passed despite the exploit. That is a verifier-coverage finding, not evidence against the defect. Disclose live database/network evidence that was not executed. Confirm exact commit/tree and repository cleanliness at the end.

## Pitfalls

- Treating HTTP 200 or `success !== false` as a clean envelope.
- Trusting request filters as proof of returned lane/scope identity.
- Calling a key allowlist privacy-safe while free-form allowed strings remain.
- Checking producer counts but not rechecking them in a security-definer function.
- Returning a limited change page with a global latest cursor.
- Testing function grants without invoking the real caller role.
- Accepting a recovery PASS against a baseline that predates the candidate.
- Editing an already-ledgered migration and treating fresh-install or regenerated-baseline PASS results as upgrade evidence.
- Shipping rollback prose instead of executable, parity-tested rollback SQL.
- Letting a green maintained suite override a direct adversarial reproduction.
