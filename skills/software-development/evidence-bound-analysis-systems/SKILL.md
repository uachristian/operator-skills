---
name: evidence-bound-analysis-systems
description: "Use when building read-only analysis systems whose every claim must trace to provenance-bound evidence and fail closed."
version: 1.0.5
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [evidence, provenance, release-review, fail-closed, read-only]
    related_skills: [development-quality-loop]
---

# Evidence-Bound Analysis Systems

## Purpose

Use this class-level skill for systems that ingest documents, manifests, logs, research claims, configuration-bundle inventories, forensic records, or other evidence and later emit analyses, hypotheses, recommendations, comparisons, or handoffs.

The central release question is not merely whether intake validated the source. It is whether **every public consumer can prove that its conclusions derive from the same canonical source bytes** rather than a caller-forged derived record, route identifier, stale cache, or hardcoded case behavior.

For model-neutral local semantic shadow workers, use `references/model-neutral-semantic-shadow-worker-boundaries.md`. It covers private-repository gating, copy-root/public-ingress parity, sensitivity/source/auth coupling, atomic snapshot enqueue, full-contract idempotency, private SQLite modes, malformed-model-output terminalization, strict tool-attempt rejection, and deterministic slow-transport deadline probes before exact-tip release.

For large deterministic inventories consumed by a bounded downstream analyzer, use `references/compact-authority-sidecars.md`: keep the consumer size cap, emit a path/value-free authority projection, preserve immutable historical pins while adding exact new pairs, reject mixed pairs, and wait for concurrent profile finalizers before freezing hashes. **An adjacent manifest is not an authority root:** the consumer must pin or cryptographically anchor the exact reviewed sidecar, manifest, inventory row, and provenance/source-artifact pair, then replay a forged sidecar+manifest attack at the public ingest boundary.

For exact candidates with operational rollback references or concurrent live remediation, use `references/exact-candidate-rollback-and-mid-review-drift.md`. Resolve every README/build-contract/closeout rollback pointer to its actual restore targets, reject current instructions that name a broader obsolete backup, require any referenced rollback packet to be frozen or separately identity-bound, and reject authority pointers to verdicts that do not yet exist. Re-hash archive and live identity at the end: if a successor appears mid-review, keep the supplied ancestor on HOLD rather than silently switching scope.

Never run attributable staged-candidate tests from the mutable worktree merely because `git status` looked stable earlier.

## Trust boundaries

Keep these identities separate:

1. source artifact bytes,
2. manifest/authority bytes,
3. deterministic ingestion record,
4. normalized eligible claims,
5. analysis projection,
6. handoff/report projection,
7. component release verdict,
8. integration authority.

No downstream layer may inherit authority merely because an upstream component was independently approved. A decoder can be approved for deterministic inventory while its integration remains provisional and non-authoritative.

### Operational artifact-custody invariants

For systems that organize live-session exports, configuration bundles, scans, logs, or other operational artifacts:

- A mutable manifest and an append-only/hash-chained journal must cross-check each other. Verifying their hashes independently is insufficient: require identical artifact-ID sets and compare role, relative path, hash, size, parent IDs, source actor, and closeout/report identity.
- Deduplication identity must include provenance context—not only role and file hash. Include parent lineage plus the operational discriminator that prevents identical bytes from collapsing across modules, tools, or methods. Normalize unordered parent sets before comparing.
- Parent-ID presence is not semantic lineage. Define allowed role edges, require same-domain/module ancestry where operationally relevant, reject cycles/orphans/unrelated parents, and require every authority-relevant path to terminate at an accepted root artifact.
- For completed operations, bind the exact human-selected candidate, exact authorization-evidence artifact, and exact operation log to each other. A role existing elsewhere in the session does not satisfy ancestry; for example, a release candidate must actually descend from the reviewed build it claims as its parent.
- Preserve source bytes with a hash-before/copy/hash-after transaction and reject a source that changes during capture. Keep original vendor filenames inside unique artifact directories rather than overwriting or silently renaming source reads.
- Reject source symlinks and every symlink component in a registered artifact/report path. Resolve containment from the canonical root, then rehash every registered file at verification and closeout.
- Hash generated handoffs and closeout reports too; they are downstream evidence, not exempt prose. Block completed closeout while registered bytes, manifest/journal linkage, required parentage, required roles, or unregistered managed-folder files remain unresolved.
- Folder names such as `Original`, `Approved`, `Final`, or `Release Candidate` are workflow labels, never evidence authority. Keep execution/approval authority as a separate explicit human boundary and default it false.

## Public analysis boundary

At every public CLI/API analysis entry:

1. Require bound source and manifest identities—not only a case or route ID.
2. Resolve paths through the canonical root and per-command lane policy.
3. Open and hash the actual source, manifest, and referenced artifacts.
4. Rerun canonical deterministic ingestion from those bytes.
5. Canonical-byte-compare the rebuilt record with the supplied persisted record after removing only explicitly permitted analysis-added fields.
6. Reject mismatches in raw evidence, claims, normalized eligibility, locators, ordering, hash, size, or provenance.
7. Derive Observed evidence and hypothesis support exclusively from eligible claims in the validated record.
8. Never synthesize observations or support from `case_id`, filename, route, or fixture name.

Private pure-projection helpers may accept prevalidated objects for unit testing. Release regressions must exercise the public boundary.

## Fail-closed semantics

- Unknown identity, ownership, units, dimensions, applicability, revision linkage, or provenance remains unresolved.
- Quarantined or compatibility-false claims may remain visible as context but cannot support hypotheses.
- Research support never proves current physical state or installed configuration.
- Free-form prose is not a trustworthy safety action type. Use a trusted typed enum with default deny, or fail closed for the entire free-form lane; do not grow a synonym blocklist and call it semantic validation.
- Pair every rejection test with a canonical producer-built positive control.

## Evidence-corpus and label audit

Before auditing whether `Observed`, `Likely`, `Possible`, or `Not proven` labels are justified, verify that the declared evidence corpus is itself reviewable:

1. Resolve every manifest entry to an exact artifact within the authorized scope.
2. Recompute each declared hash and size; a stale hash means the cited revision is not the reviewed revision.
3. Treat missing manifest artifacts as an evidence gap, not as permission to infer their contents from a report that cites them.
4. Keep provenance classes explicit: exact local artifact, official documentation, secondary/source-stated material, owner-reported physical state, and directly inspected/measured physical state are not interchangeable.
5. Phrase corpus-absence conclusions as `not found in the reviewed corpus`; headings such as `No master plan exists` overclaim unless the search boundary is complete and authoritative.
6. A source may prove that a vendor or owner *stated* something without proving the underlying physical or engineering fact.
7. If live configuration changes occurred after the last hashed artifact or readback, demote that artifact to `last supplied baseline`; do not call it the current installed state.

A report is on **HOLD as evidence-complete** when load-bearing claims depend on missing artifacts, stale hashes, unspecified image/source locators, or post-capture configuration drift, even if many individual technical claims remain sound.

## Credential boundary

Reject credentials before persistence when credentials are outside the system contract, and recursively redact projections as defense in depth. Cover:

- provider API tokens,
- bearer values and JWTs,
- HTTP Basic authorization statements,
- generic URI userinfo for database/cache/SSH-like schemes—not only HTTP(S),
- credential-shaped strings under innocuous nested keys.

A token detector is not complete if it only recognizes known provider prefixes.

## Exact-tip release loop

1. Freeze the goal, non-goals, authority limits, candidate file set, aggregate algorithm, acceptance gates, and rollback.
2. Run maintained tests and direct adversarial public-boundary probes.
3. Dispatch one bounded independent review against the exact bytes.
4. Reproduce every critical/HIGH finding in the parent lane.
5. Remediate narrowly and convert accepted findings into regressions.
6. Regenerate canonical records/reports through the public CLI.
7. Recompute all report hashes, counts, baseline paths, and manifests after the final regeneration.
8. Freeze a new exact candidate and obtain a fresh exact-tip verdict.

An ancestor APPROVE cannot release a descendant. An ancestor exploit remains actionable until independently disproved at the current tip. Keep the verdict unresolved while a required review is pending.

## Transport completeness and publication ordering

Determine transport truncation/error status from the original response **before** sanitization, primary-record selection, or removal of related-content/footer sections. Otherwise cleanup can remove the only omission marker and falsely promote a partial capture to complete evidence. Carry that status alongside the sanitized bytes. Regression-test a truncation marker located beyond a section the sanitizer removes, paired with a genuinely complete positive control.

Treat source custody, semantic validation, rendered-artifact review and publication as separate gates. A fixed collector can receive a bounded JSON URL request, perform the permitted extraction itself, and persist the returned evidence plus an integrity index; the model supplies projections, not reconstructed transport responses. Hashes establish custody, not independent source truth or permission to execute the collector in another context.

Render without advancing the last-good pointer. Inspect the resulting PDF/contact sheet, then verify the same input, report and PDF hashes before publication. Do not re-render after visual approval and assume the new bytes inherit that approval. Historical replay can verify the renderer, but cannot establish fresh research or successful scheduled delivery.

For owner-facing operational claims, distinguish **configured/enabled**, **component-verified**, **scheduled-artifact-verified**, and **delivery-verified**. A successfully delivered blocker notice is not a successful analysis. For the owner, state the pending layer plainly rather than leading with an unqualified activation claim.

## Closeout evidence

Machine and human closeouts must agree with current bytes. Derive rather than hand-copy:

- maintained test count,
- source/hash gate count,
- research accepted/quarantined counts,
- current report hashes,
- baseline and rollback paths,
- component versus integration verdicts,
- forbidden capability scan results.

Stale closeout evidence is a release defect, not cosmetic documentation debt.

## Rollback

Use manifest-owned file-by-file restoration. Validate containment, expected hash/size, and destination policy. Preserve append-only outcomes, backups, and unknown/new files. Never recursively delete a runtime directory to restore a reviewed candidate.

## Reporting

Return verdict first:

- `APPROVE` only when exact identity is stable before/after review and no reproducible critical/HIGH path remains.
- `HOLD` when a public-boundary bypass, credential persistence, safety-classification bypass, stale evidence, or required review gap reproduces.

Keep component verdicts separate and state authority scope precisely.

## Pitfalls

- Hardening intake while downstream analysis trusts caller-supplied derived JSON.
- Testing only private helpers after the public boundary changed.
- Hardcoding Observed facts in a case-specific analysis function.
- Treating `case_id` as evidence.
- Using finite prose regexes for safety-critical semantic authorization.
- Updating status labels after hashing reports without recomputing closeout hashes.
- Treating one approved component as authority for the integrating system.
- Treating a successful first document chunk as whole-document completion, or enforcing result limits by slicing text/pages without explicit omission metadata.
- Recursively deleting runtime state during rollback.
- Trusting rollback prose without checking machine-readable cleanup lists, backup-manifest digest/count, and whether named release files actually exist.
- Treating a prospective exact verdict path as an already-issued release; keep the candidate HOLD until the verdict is durably created.
- Accepting green maintained tests without replaying every prior HIGH at the exact tip.

## Verification checklist

- [ ] Every manifest entry resolves within the authorized review scope; missing artifacts are reported.
- [ ] Declared hashes and sizes match the exact reviewed files.
- [ ] `Observed` claims identify whether evidence is artifact-derived, official-document-derived, secondary/source-stated, owner-reported, or physically measured.
- [ ] Absence claims are bounded to the reviewed corpus unless a complete authority proves global absence.
- [ ] Any post-capture live edits demote the prior artifact from `current installed state` to `last supplied baseline` until a new readback is pinned.
- [ ] Exact candidate set and aggregate algorithm are documented and reproduced.
- [ ] Pre/post review identity matches.
- [ ] Public analysis rebuilds canonical ingestion from current source/manifest bytes.
- [ ] Multi-call document intake accounts for every source page, reports `complete`/`next_page` explicitly, and binds continuation ranges to the same source hash.
- [ ] Oversized batches fail without returning partial or silently truncated evidence.
- [ ] Tampered raw evidence, claims, normalization, source identity, and manifest identity fail.
- [ ] Canonical producer-built positive record succeeds.
- [ ] Observed/support output is a projection of eligible claims only.
- [ ] Generic URI userinfo and HTTP Basic probes reject before persistence.
- [ ] Recursive report redaction contains no forbidden descendant values.
- [ ] Free-form safety actions default deny unless a trusted typed classifier exists.
- [ ] Component and integration verdicts remain separate.
- [ ] Current closeout hashes/counts/baselines match final bytes.
- [ ] Rollback is manifest-owned, binds the current backup-manifest digest/count, has cleanup fields consistent with restore prose, and preserves append-only/unknown/audit state.
- [ ] Any prospective verdict pointer names the exact planned file, remains non-authoritative while pending, and resolves before release is claimed.
- [ ] Fresh exact-tip independent verdict is complete before release.
