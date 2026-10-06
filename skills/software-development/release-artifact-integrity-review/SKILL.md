---
name: release-artifact-integrity-review
description: "Use when reviewing a release built from manifests, archives, or frozen commits. Prove the reviewed bytes are the shipped bytes."
version: 1.0.11
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [release, artifact-integrity, git, archives, replay, code-review]
---

# Release Artifact Integrity Review

## Overview

Use this skill for read-only, exact-candidate review of a release directory containing a manifest plus Git bundles, patches, full source archives, or unchanged carry-forward archives. The release question is whether every transport names and reconstructs the same immutable commit/tree without omissions, mode drift, archive path attacks, undeclared files, or stale approval reuse.

This is an identity and replay review, not a substitute for behavioral or security testing. Apply the requester's stated severity threshold exactly and keep production/shared candidate files unchanged.

## Reference files

- [`references/immutable-start-snapshot-for-moving-non-git-candidates.md`](references/immutable-start-snapshot-for-moving-non-git-candidates.md): before behavioral probes, capture and hash the exact starting implementation/test bytes, execute from those captured bytes rather than reopening mutable paths, and invalidate pathname-coupled probes immediately if a successor appears.
- [`references/pre-freeze-staged-index-hygiene.md`](references/pre-freeze-staged-index-hygiene.md): before freezing any candidate that will later be committed, stage the exact allowlist, pass staged whitespace/path/diff gates, and complete every byte-changing formatter before hashing or review.
- [`references/staged-tree-deterministic-tar-review-archives.md`](references/staged-tree-deterministic-tar-review-archives.md): for deterministic TAR review archives built from a staged Git tree, create from Git object bytes, compare tar permission modes to Git permission bits rather than full file-type modes, keep the final archive SHA in an external manifest, and require fresh exact-digest APPROVE verdicts after every byte change.
- [`references/git-archive-checkout-reconstruction.md`](references/git-archive-checkout-reconstruction.md): when a Git TAR extraction yields group-writable modes or tests require `.git`, prove archive safety and path/blob/executable parity first, normalize disposable files to checkout modes from `git ls-tree`, force-stage, require the exact target `git write-tree`, then run Git-dependent gates without touching the source checkout.
- [`references/tool-output-is-not-release-byte-transport.md`](references/tool-output-is-not-release-byte-transport.md): never derive candidate bytes from model-visible tool output.

## Review principles

- Enumerate and replay every mandatory command with its exact pinned tool and interpreter versions; audit runtime and CI-tool dependencies as separate scopes, and distinguish release-process severity from the underlying diagnostic or advisory severity.
- Bind hash-first/hash-last, self-test with the production interpreter, and scan every emitted field with privacy canaries without echoing sensitive values. A helper-level redaction test is not report-wide evidence: trace sensitive values through inventory, nested metadata, rendered warnings, latest output, and retained history.
- Separate per-file atomicity from cross-file generation consistency.
- For GraphQL or CRM-backed candidates, compare the dependency projection against a recursive scanner of every nested CRM record/relation field; a projection that omits nested filter values is not closure.
- A zero exit status or a printed `OK` from a harness cannot become release evidence unless the harness's semantic checks are themselves verified.
- Historical acknowledgment must be an internally derived result, not a status a source row can self-assert or obtain through broad hyphen/underscore normalization.
- Separate candidate-input approval from runtime/canary authority; approval of inputs never transfers to execution.
- For file handoffs, prefer authenticated private transfer channels, hash before sending, and verify the receiver-side hash; a "sent" status is not receipt.

## Required workflow

1. **Finish index hygiene before freezing.** Stage the exact allowlisted candidate paths, require `git diff --cached --check`, inspect `git diff --cached --name-only` and `--stat`, and run any source-format gates that can still change bytes. Only then freeze the release-directory file set, hashes, sizes, modes, manifest bytes/hash, target commit, prerequisite/parent, tree, changed paths, and critical blob IDs. If a post-review cleanup changes even trailing newline bytes, mark the archive stale, re-freeze, and obtain a bounded exact-tip delta review; never transfer the old approval by calling the change non-semantic.
   - **Do not derive candidate bytes from model-visible tool output.** File-reader text, terminal stdout, and structured tool responses are display channels: they may truncate, decorate, normalize, suppress, or redact source text. Copy unchanged bytes through byte-preserving filesystem/Git operations, apply intentional edits separately, then scan/compile/diff the complete derived set before hashing. See `references/tool-output-is-not-release-byte-transport.md`.
2. **Bind every reviewer to that exact identity packet.** Give each reviewer one immutable path/archive and expected digest, require the reviewer to report the digest observed before and after, and compare it to the orchestrator's canonical digest before accepting the verdict. A completed batch whose reviewers report a different archive hash is valuable finding evidence only; it cannot approve or reject the current successor as exact-candidate evidence. Reproduce applicable findings on the successor, then obtain fresh review. If a runtime-identical but test-strengthened commit/archive supersedes a prior candidate, treat the previous review as non-approving because the release identity and artifact evidence changed; dispatch or require a fresh exact-tip review for the new commit/archive before closeout. When stale async review results arrive for obsolete commits, reduce them only into class findings/regressions that are mapped against the current tip, never into release approval.
   - **Drain predecessor evidence before the final successor review.** Enumerate every earlier review handle, recover each complete report rather than relying on a truncated completion notification, and replay every qualifying finding against the current candidate. If an older reviewer is still active, let it finish or explicitly cancel it before commissioning the final exact-tip reviewer. Otherwise late predecessor findings can repeatedly invalidate already-frozen successors and waste independent-review cycles.
   - A predecessor verdict never transfers to a successor, but a reproducible predecessor bug class remains evidence until a current regression or bounded probe closes it. Record the old target digest, finding class, current remediation, and current test/probe that proves closure.
3. Parse the manifest structurally with duplicate-key rejection. Require its artifact-key set to equal the directory file set minus the manifest.
4. Verify every artifact hash, size, and required mode against the manifest.
5. Verify bundle integrity, advertised references, prerequisites, and exact replay from a repository that contains the prerequisite but not the candidate tip. When creating a bundle, do not assume a raw object ID is accepted as a revision argument: `git bundle create <file> <sha>` may refuse an apparently empty bundle. Freeze the exact tip first, then bundle a symbolic ref/revision expression such as verified `HEAD` (or create a temporary exact ref), and require `git bundle list-heads` to advertise the intended immutable commit before accepting it.
6. Replay the patch against the exact prerequisite and require the exact target tree and changed-path boundary.
7. Inspect every archive member before extraction for duplicate, normalized-duplicate, traversal, escaping-link, and unsupported-member hazards.
8. Compare archive paths, blob bytes, symlink targets, and executable modes directly to the exact Git tree.
   - When building a tar by explicitly enumerating every path, add each member with `recursive=False`. Adding a directory recursively and later adding its enumerated children creates duplicate member names even when payloads are identical. Freeze `len(names) == len(set(names))` before accepting the transport, and rebuild/re-review the archive if duplicate entries are found.
   - If a `git archive` member differs from its raw blob, do not immediately call it drift and do not waive it as “just line endings.” Committed attributes such as `*.ps1 text eol=crlf` can deterministically transform export bytes. Sample normalized equality alone is non-approving.
9. Extract only to a disposable root; initialize Git, force-stage all paths, and require exact path count and `git write-tree` identity.
10. Before running archived tests, inspect their import roots, workspace constants, helper executable paths, and fixture paths. A test launched from an archive is not archive-bound if it imports code from a hard-coded mutable checkout. Prefer relative-to-`__file__` resolution; when reviewing an immutable candidate that cannot be edited, rebind the root only in a transparent disposable/in-memory harness and state that the committed entrypoint itself remains unbound. For Python archive tests, isolate ambient imports: clear inherited `PYTHONPATH`/`PYTHONHOME`, set `PYTHONPATH` only to archive-local package roots, use `PYTHONDONTWRITEBYTECODE=1`, and prefer `python3 -S -B -m unittest ...` (or the product's equivalent no-site/no-bytecode mode). If an initial archive test failure resolves under this archive-only no-site invocation, report the first result as harness contamination, not candidate behavior.
11. For unchanged components, require byte-for-byte equality to the exact previously approved artifact and bind the comparison to its recorded digest.
   - For narrow data-only commits, explicitly freeze blob equality for protected application, feature, curated-data, inventory, package-manifest, and lockfile paths. A changed-path list proves scope, while direct blob equality proves named carry-forward features and dependencies were preserved.
   - When privacy removals are claimed, compare IDs as a set for exact removal/zero addition, then separately prove retained order and semantic equality. Reconcile count, image-total, manufacturer-subtotal, and exclusion-bucket deltas to the removed records.
   - Do not infer the producer's privacy decision from a public page or CDN HTTP status. Public HTML/media can return `200` while API metadata returns `401`/`403`; verify any status claim against the exact endpoint/method/auth context, and run removed parent records through the exact reviewed classifier or sanitizer. Report mismatched supplied status evidence without converting a conservative omission into a blocker unless product impact reaches the requested threshold.
   - For fixture-only updates, inspect a word-level diff and require changed expectations to be exactly the independently verified aggregate deltas, with schema, uniqueness, accounting, privacy, and curated-content assertions preserved.
12. Enumerate every mandatory command declared by archived CI workflows, verification blocks, and release scripts; replay each with the exact declared tool and interpreter versions. Audit shipped/runtime dependencies and CI/build/test tools as separate scopes.
13. Run the verifier as a non-destructive invocation and capture its evidence before any standalone harness-file deletion. Keep disposable replay-root cleanup inside the verifier's `finally` path; do not append `rm` or another approval-gated cleanup action to the same shell command, because a denied cleanup must not prevent the verifier from running.
14. Re-freeze candidate and production/live runtime identities separately. If the fixed-path runtime changes during review, stop using earlier production-path runs as candidate evidence: preserve archive-only findings, reproduce applicable blockers against the frozen archive, and keep approval at `HOLD` until live parity is restored and fresh exact-byte production validation is obtained. Confirm disposable replay roots are gone and report cleanup. Remove a temporary harness file separately only when the active tool policy permits it.
15. **Reserve the closeout budget before optional depth.** When the tool/runtime enforces a call limit, consolidate the final archive re-hash, extracted path/byte/mode parity, reviewer-process shutdown, and disposable-root cleanup into one bounded closeout action and run it before optional screenshot or polish batches consume the remaining budget. If the required post-review identity/parity check cannot be completed, do not emit `APPROVE`; use the requester's non-approval vocabulary (`HOLD`, `BLOCK`, or `NO_VERDICT`) and state the exact missing evidence. Cleanup inability alone may be an evidence boundary rather than a candidate defect, but it must never be silently presented as completed.

## Core invariants

- No undeclared or missing release-directory file exists.
- JSON duplicate keys cannot override artifact metadata.
- Bundle replay proves exact tip, parent, and tree from the named prerequisite.
- Patch replay proves the exact tree, not merely a clean textual apply.
- Every archive path is unique before and after POSIX normalization and remains confined after link resolution.
- Full archive reconstruction includes tracked paths ignored by the archived `.gitignore`.
- File bytes, symlink targets, and Git executable modes match the exact candidate, either as raw blobs or—only for a proven `git archive` lane—as the complete deterministic exact-tip export stream under committed attributes.
- Carry-forward approval follows exact bytes/digests only; matching labels or extracted semantics are insufficient.
- Unchanged manifests/locks retain exact prerequisite, tip, and archive-contained blob IDs.
- Candidate/shared/production files remain untouched throughout review.

### Python bytecode-shadow and verifier-bootstrap pitfall

A manifest/verifier can falsely approve declared `.py` source while Python executes undeclared cached bytecode instead—especially `__pycache__/*.pyc` in unchecked-hash mode. Never silently exclude executable cache paths from a Python release aggregate when any verifier, test, demo, or runtime import could resolve them.

For manifest-backed Python candidates:

1. inventory the entire tree before importing or executing candidate code;
2. fail closed on undeclared regular files, symlinks, `.git`, `__pycache__`, `.pyc`, `.pyo`, startup hooks such as `sitecustomize.py`, and platform metadata unless each is intentionally manifest-bound and reviewed;
3. skip all candidate source/tests/demo execution when inventory or manifest validation fails;
4. run the authoritative verifier with an isolated/no-site/no-bytecode interpreter where supported (for CPython: `python3 -I -S -B verifier.py`);
5. load reviewed source/tests from their exact manifest-bound `.py` bytes with explicit `compile`/`exec` or an equivalently source-forced loader rather than normal import-cache resolution;
6. reproduce an unchecked-hash `.pyc` attack in a disposable copy and require `HOLD`, no marker side effect, and proof that candidate execution was skipped;
7. bind trust externally too: a self-verifier cannot prove its own honesty if the verifier bytes themselves are replaced before startup, so retain the independently frozen manifest/archive/verifier digests; and

### Archive mode-preservation pitfall

A ZIP can preserve file bytes while an extractor silently normalizes POSIX modes. If the manifest or application behavior binds read-only/executable modes, do not weaken the verifier after a restored ZIP fails. Either use a transport/extractor pair with proven mode preservation (for example a constrained PAX/TAR archive), or bundle an explicit restore helper whose mode normalization is itself manifest-bound and tested. In both cases:

1. inspect all members before extraction and reject duplicates, traversal, links, and unsupported types;
2. extract into a disposable root;
3. run the candidate's verifier from the extracted tree;
4. require the exact pre-package aggregate and behavioral gates;
5. remove the disposable root; and
6. discard the failed convenience archive so it cannot be mistaken for the approved transport.

## Severity and verdict

Treat as **HIGH / HOLD** when a reproducible defect allows the release to reconstruct a different tree, omit tracked payloads, change executable/symlink semantics, accept undeclared or hash-mismatched files, extract outside the disposable root, or carry approval to non-identical bytes.

Do not inflate a convenience frozen-copy mode normalization into a blocker when the actual release archive independently matches every Git path/blob/mode and reconstructs the exact tree. Do not use such a normalized copy for tests whose behavior depends on executable mode.

When the requester asks for critical/high blockers only, begin the verdict with exactly `APPROVE` or `HOLD`, then report only threshold-relevant findings plus concise nonblocking evidence boundaries.

## Verification checklist

- [ ] Exact directory file set and manifest digest frozen before and after.
- [ ] Duplicate JSON keys rejected.
- [ ] Artifact names, hashes, sizes, and modes match.
- [ ] Target commit, parent, tree, and changed paths match manifest.
- [ ] Candidate tip was absent before prerequisite-only bundle replay.
- [ ] Bundle replay produced exact tip/parent/tree.
- [ ] Patch replay produced exact tree and boundary.
- [ ] Archives have no duplicate, normalized-duplicate, traversal, escaping-link, or unsupported entries.
- [ ] Archive-to-Git path/blob/mode comparison is exact, or any committed-attribute export conversion is bound by a complete fresh exact-tip `git archive` stream comparison.
- [ ] Force-staged archive reproduces exact path count and tree.
- [ ] Carry-forward archives are byte-identical to approved predecessors.
- [ ] Critical unchanged blobs agree across prerequisite, tip, and archive.
- [ ] Every mandatory archived CI/release command was replayed with its declared tool and interpreter version; runtime and CI-tool dependency audits were scoped separately.
- [ ] Disposable roots removed; candidate/shared repository unchanged and clean.
