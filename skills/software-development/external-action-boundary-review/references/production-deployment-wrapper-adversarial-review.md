# Production deployment wrapper adversarial review

Use this for bounded, credential-free review of wrappers that upload an exact archive and perform one production deployment, promotion, or alias move.

## Required invariants

- Dry-run returns before credential loading, network setup, locks, result writes, or any remote mutation.
- The live gate is explicit and unambiguous; disable argparse-style long-option abbreviations when the exact flag is part of the approval contract.
- The reviewed archive is bound by a mandatory expected manifest digest, not only by a marker file containing a caller-supplied commit.
- Every archive entry is a regular contained file. Avoid check-then-reread: retain verified bytes or re-open/revalidate by descriptor immediately before upload. A path validated during manifest construction must not be followed again after credentials are loaded.
- Recheck mutable remote prerequisites at the lowest irreversible mutator. Checking the current production alias before a long upload phase is insufficient; a concurrent release can change it before deployment creation. When production creation promotes asynchronously, monitor drift until the candidate owns the alias or use a provider CAS/idempotency primitive.
- Exactly one explicit deployment-create call is reachable. No retry follows timeout, disconnect, malformed success, or create-then-error ambiguity unless the provider supports an idempotency key that is bound and reconciled.
- Require READY plus the intended target/environment. A production wrapper must never promote a Preview artifact, including during rollback.
- Read back and compare every claimed identity: deployment ID, target, commit, manifest digest, release channel, Git SHA/ref/provider metadata, and final alias. Verifying only one custom commit field is not enough.
- Rollback must target the recorded prior READY production deployment, use an executable endpoint/path, and verify the alias postcondition. A rollback dry-run must remain credential-free.
- Validate request payload types against the provider schema. In particular, JSON booleans must not be serialized as strings merely because metadata values are often strings.
- Do not print tokens, Authorization headers, provider bodies, or generic exception strings that can contain request headers. Sanitize every transport failure path.

## Credential-free fake-transport matrix

Import the exact wrapper with bytecode generation disabled and replace both credential and network helpers in memory. Do not alter the reviewed wrapper.

1. **Dry-run poison:** make credential and network helpers raise if called; canonical dry-run must still succeed.
2. **Manifest mismatch:** change one byte in a temporary archive copy; omission or mismatch of the expected digest must fail before credentials.
3. **Alias drift:** return the expected current alias initially, change it during uploads, and return the candidate after creation. Assert deployment creation is refused; a final candidate alias must not hide prerequisite drift.
4. **Symlink TOCTOU:** validate a regular file, replace it with an out-of-root symlink before live upload, and capture upload bytes. No external bytes may reach the fake transport.
5. **Metadata mismatch:** return READY/production with correct custom commit but wrong manifest and Git SHA/ref. Success must be rejected.
6. **Deployment failure:** return ERROR/BLOCKED/CANCELED and assert no alias mutation and no create retry.
7. **Alias postcondition:** return a different deployment after READY; assert failure without another create.
8. **Preview rejection:** pass READY with a null/preview target to both release and rollback paths; both must reject.
9. **Rollback control:** return the recorded prior READY production deployment, record exactly one rollback/promote call, then return that deployment from the production alias.
10. **Call accounting:** report upload count, create count, promotion/rollback count, and ordered GET/POST trace. Distinguish one wrapper invocation from one provider deployment.

For TOCTOU probes, use a temporary directory and swap the file after manifest construction but before the upload call. Capturing out-of-root bytes is a valid blocker even if the real provider would later reject a digest mismatch: confidentiality was already lost at the request boundary.

## Concurrent review-input drift

Hash the wrapper and archive at review start and again before verdict. Temporary scripts outside Git can change concurrently just like worktrees. If the wrapper hash changes:

1. Treat all prior outcomes as ancestor evidence only.
2. Re-read the final source and replay every still-relevant exploit against the final hash.
3. Drop findings demonstrably fixed by the new version.
4. Bind the verdict to the final hash and disclose the observed drift.
5. Never claim the reviewer modified the wrapper when another process changed it; report reviewer-created temporary probes separately.

## Reporting

Verdict first. For every critical/high blocker provide exact final-source lines, the deterministic probe command, and the observed state/call count. Then list passed controls and evidence boundaries. A no-network review may identify a schema-invalid payload by exact serialized types, but must label live provider acceptance as untested.