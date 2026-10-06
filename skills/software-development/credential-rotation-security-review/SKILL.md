---
name: credential-rotation-security-review
description: "Use when designing or reviewing a credential/account rotation for identity binding, exposure, rollback, and secret handling."
version: 1.0.3
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [security-review, credentials, account-rotation, identity-binding]
    related_skills: [external-action-boundary-review, operational-change-control, development-quality-loop]
---

# Credential Rotation Security Review

## Purpose

Use this class-level skill to review or design a workflow that rotates a password, token, API key, certificate, or other credential for an existing remote account and then updates a local secret store. It is especially important when the workflow also resets permissions, performs a smoke test, or deletes a temporary/bootstrap administrator credential.

The security question is not merely whether the new credential works. Prove that every remote mutation remains bound to the intended non-privileged identity, that ambiguous/partial results do not cause unsafe retries, and that recovery authority survives until the new credential is confirmed usable.

## Threat model

Treat all remote identifiers and readbacks as untrusted transport data, even when they come from an authenticated administrative endpoint. Common hazards include:

- numeric ID aliases such as leading zeros, signs, Unicode digits, or whitespace that a server normalizes to a reserved administrator ID;
- duplicate or renamed account rows;
- role drift between preflight and mutation;
- HTTP success without semantic identity readback;
- permission reset applied to a different account than the password mutation;
- old local secret removal followed by new-store failure;
- bootstrap-admin deletion before credential usability is proven;
- password leakage through argv, output, exception text, temp files, or test fixtures;
- media/snapshot smoke tests that accidentally persist sensitive payloads.

Do not broaden a review into accepted same-user trust boundaries or unrelated hardening when the release request is blocker-only.

## Authority boundary

Treat credential rotation, local runtime installation, launchd/service activation, state purge, and remote account deletion as separate mutations. An approval to rotate or repair a credential does not authorize deploying/loading the runtime, and an approval to unload a stale service does not authorize reinstalling it. Bind the approval note to the exact mutation mode, stop after the approved receipt, and obtain a new explicit approval before crossing into deployment or activation.

## Immutable review setup

1. Freeze the exact target commit, tree, parent, and scoped changed paths from immutable Git objects.
2. Materialize the target into a disposable root with an immutable archive or detached exact worktree, according to whether tests require Git metadata.
3. Prevent tests from importing a moving canonical checkout. If an archive-only maintained test hard-codes the checkout root, rewrite only that root constant in memory before `compile`/`exec`; do not edit the archive.
4. Disable bytecode/test caches or account for them explicitly.
5. After testing, compare all extracted file bytes and modes against the original archive and remove the disposable root.
6. Never access live credentials, secret stores, remote services, cameras, databases, launchd, or installed artifacts unless explicitly authorized.

## Canonical identity binding

For numeric account IDs used in URLs or payloads, require a canonical grammar at the lowest mutator:

- exact string type;
- ASCII only;
- decimal digits only;
- round-trip equality: `value == str(int(value))`;
- numeric value outside the reserved/administrator range;
- exactly one exact-name target account;
- exact expected role/capability.

A check such as `isdigit()` plus `id != "1"` is unsafe: `01`, full-width digits, Arabic-Indic digits, mathematical digits, and superscript digits may pass or normalize unexpectedly.

Use a truth table with healthy canonical IDs and adversarial zero, reserved, leading-zero, sign, whitespace, Unicode-digit, decimal, exponent, fraction, empty, duplicate, renamed, and wrong-role cases. Pair every negative case with a positive canonical control.

## Prove remediation closure

When reviewing a fix for a prior alias or identity bug:

1. Reproduce the old behavior from the frozen parent.
2. Record whether each alias reaches the first remote mutation and the exact target path/payload.
3. Replay the same matrix against the remediation tip.
4. Require zero mutation calls for every rejected alias.

A green new unit test alone is not enough; parent exploit reproduction plus tip suppression shows that the dangerous path was actually closed.

## Multi-account OAuth pools and single-use refresh ownership

For multi-account OAuth pooling, treat labels, row count, usage meters, and token count as display metadata—not account identity or failover proof.

1. Decode only the minimum identity claims in-process and emit neither token bytes nor account IDs. Treat claims as lineage metadata, not authentication proof; require provider readback for live identity.
2. Trace every login-save, runtime resync, refresh, write-through, cooldown-clear, stale-writer merge, and terminal-error path. A write-side guard is incomplete if a later read/refresh path can still replace an independent account from a singleton.
3. Give each rotating refresh chain one authoritative store and one cross-process lock. Before promoting a quota-only credential into inference, inventory and migrate every meter, dashboard, exporter, profile, and container that can refresh it; two correct refreshers still race a single-use token.
4. Preserve newer generalized ownership architecture when adapting an older credential fix. Do not replay a divergent patch wholesale, duplicate provider logic in an obsolete module, replace current cooldown/status merging, or require literal configuration that current code supplies as a default.
5. For profile borrowing, lock the store that owns the token—not merely the active profile's local store. Never copy or mount a whole root auth store into an isolated runtime to share one provider.
6. At the final persistence boundary, reject a known cross-account replacement for the same row and keep a newer rotated pair over a stale snapshot. Preserve only explicitly monotonic metadata such as request counters; never let an unrelated status write restore a consumed refresh token.
7. Bind every fallback credential-import path to the expected account before persistence. In particular, a refresh failure followed by CLI recovery must compare the imported token's known identity with the rejected row's known identity; otherwise whichever account is currently logged into the CLI can silently replace the row. If continuity is unknown, fail closed to explicit reauthentication rather than adopting ambient credentials.
8. Fail a terminal independent-account refresh by quarantining only that row. Preserve established treatment for ordinary same-account manual-grant failures unless the provider proves a terminal account-lineage condition; do not broaden a cross-account terminal reason into deleting or killing healthy manual credentials.
9. Test with synthetic primary/secondary JWT fixtures and mocked provider calls: independent row never adopts singleton; wrong-account refresh retains old material; wrong-account CLI recovery makes zero persistence calls and retains singleton/pool bytes; concurrent instances make exactly one refresh POST; stale writer cannot restore the spent pair; targeted quota recovery clears only the proven account; quota exhaustion rotates to the secondary and verified recovery returns to primary priority.
10. Report usage display and inference failover separately as `meter-only`, `pool-active`, or `runtime-verified`. Two meters are not proof that two accounts are active in the inference pool.

## Post-mutation readback

After the credential mutation succeeds and before any permission or cleanup mutation:

- re-read identity from a trusted endpoint;
- reapply the same exact cardinality/name/role/canonical-ID validator;
- require the returned identity to equal the pre-mutation identity;
- fail closed on malformed, missing, duplicate, aliased, renamed, role-changed, or changed-ID readback;
- perform no later permission, secret-store, or bootstrap-admin deletion action after a failed readback.

Do not accept request echoes or generic HTTP status as identity evidence. Passwords usually cannot be read back; prove unchanged account identity and then prove credential usability through authentication.

## Permission and credential lifecycle

Mechanically assert the intended success order with a fake transport and event log:

1. exact account preflight;
2. credential mutation bound to the canonical identity in URL and payload;
3. unchanged exact identity readback;
4. least-privilege permission mutation;
5. structural permission readback;
6. authentication/smoke test with the new credential;
7. old local credential removal, only if required by storage semantics;
8. confirmed new local credential storage;
9. bootstrap/temporary-admin deletion last;
10. sanitized terminal output.

Inject a failure at every stage. Failures before confirmed local storage must retain recovery authority and return a retry/reconciliation state. Failures after confirmed storage must return a distinct cleanup-required state and must not repeat the remote credential mutation automatically.

If old-secret removal must precede new-secret insertion, explicitly prove that bootstrap recovery remains available throughout the gap. Prefer atomic replace/update when the secret store supports it.

## Secret boundary checks

Use synthetic secrets and monkeypatched subprocesses/transports to prove:

- no secret appears in process argv;
- prompted or STDIN delivery is the only subprocess secret channel;
- stdout/stderr and exception codes are static and sanitized;
- no secret-bearing file is created;
- subprocess success checks require both exit status and exact expected receipt;
- in-memory test capture does not get mistaken for terminal/log output;
- test fixtures use clearly synthetic values and are removed with the disposable root.

Remember that an authenticated HTTP request body necessarily contains the new secret in memory; the boundary is no unintended argv/log/disk exposure, not impossible zero-copy memory handling.

## CLI wrapper exposure and OAuth recovery

Treat package runners and wrappers as separate secret-output boundaries. `npx`, npm scripts, shell tracing, pagination hints, and command notices may print the fully expanded argv—including a value supplied through `--token`—even when the underlying command's business output is sanitized.

When that happens:

1. stop using the token immediately;
2. privately notify the owner and default to rotation;
3. identify the exact provider-side token by name plus recent activity;
4. require the destructive confirmation to name the expected token/count;
5. revoke it and verify only that row disappeared;
6. atomically remove the stale local secret reference without printing its value, preserving file owner/mode;
7. prefer supported browser/OAuth CLI authentication when no long-lived account token is needed;
8. verify identity without a token argument; and
9. keep deployment/apply/record/DNS actions outside the incident-response approval.

For short-lived OAuth callbacks, restart only when the authorization control can be handled immediately. Prefer background input; foreground the browser only with explicit approval. After an unverifiable input, verify the CLI callback or fresh page state before retrying. Never fall back to typing an API key through chat, tool input, argv, or logged process submission.

See `references/cli-wrapper-token-exposure-oauth-recovery.md` for the complete provider-dashboard revocation, local secret cleanup, OAuth recovery, and completion-evidence sequence.

## Disposable OAuth child isolation

A disposable auth home is not automatically a safe credential boundary. Rotating or single-use refresh tokens can be consumed inside the child and replaced in the temporary auth file; deleting that file then discards the replacement and can break the canonical profile. Prefer a distinct worker login. When an owner-approved workflow can tolerate fail-closed token expiry, project only the exact profile-local access token, force the child credential pool empty, exclude ambient provider homes/environment variables and fallback providers, and prove the actual runtime tool surface—not merely the intended `--toolsets` argv.

Treat projection bytes and actual provider resolution as separate evidence lanes. In fresh processes for valid and expired cases, run the real resolver with synthetic sentinels and blocked network, then inspect provider/source/model, fallback chain, refresh calls, tool schemas, and auth/pool bytes before and after. Preserve the production relationship between `HOME` and `HERMES_HOME`; adding a synthetic symlink or host-home directory can manufacture a false fallback finding. Test refresh-only, pool-only, malformed, expired, whitespace-only, and wrong-provider states before launch, plus a healthy post-call assertion that no refresh authority appeared or persisted after teardown.

For the complete authority ordering, exact-path profile-auth merge, actual-resolver/cache-isolation probe, adversarial matrix, and sanitized live-probe pattern, see `references/disposable-oauth-sandbox-auth-projection.md`.

## macOS Keychain rebuild stability

For generic-password items consumed by frequently rebuilt local binaries, explicitly choose between executable-bound access and rebuild-stable same-user access:

- an executable ACL can fail after the binary is rebuilt, leaving an item present but unreadable by both the new binary and command-line recovery tools;
- `security add-generic-password ... -A` matches a documented same-user trust boundary but is broader than application-only access and must not be described as least privilege;
- prompting with `-w` avoids secret-bearing argv, but a PTY must handle both password and retype prompts, send carriage return, enforce a deadline, and treat/zero the transcript as secret-bearing because terminal echo can occur;
- after setting accessibility attributes, prove the exact final release binary can fetch secret data—an existence query or update receipt alone is insufficient;
- test the full helper against a disposable Keychain service and delete it in `finally` before touching the real item.


## Local credential-entry handoff in Hermes Desktop

When the owner must enter a credential locally, provide the command as one fenced `bash` block so Hermes Desktop renders its code card with a one-click copy control. Keep the command itself zsh-compatible on macOS, but use the `bash` fence label: the current renderer recognizes `bash` as a common code language, while a `zsh` fence can be misclassified as prose and lose the copy control. Do not call ordinary prose or an inline snippet a “copy box.” Put no secret value in the block; prompt locally with silent input or the native Keychain prompt.

If Desktop rendering changes, verify the visible copy control rather than assuming any Markdown fence still produces it.

## Sensitive smoke-test payloads

For image, document, or other sensitive smoke responses:

- bound response size while reading;
- validate type/magic before use;
- return only bounded metadata such as byte count or a boolean;
- write no payload to disk;
- print no payload bytes;
- ensure temporary test directories remain empty;
- distinguish no persistence from stronger claims about immutable language buffers, framework copies, swap, or core dumps.

## Offline verification pattern

Prefer dependency-free probes using the real parser, payload builder, state machine, and orchestration function with only external boundaries replaced:

- fake inventory/readback producer;
- fake remote request function with exact call counting;
- real structural permission parser;
- fake authentication/snapshot transport;
- fake secret-store subprocess that snapshots argv and STDIN at call time;
- event log for ordering and failure injection;
- output capture and disposable-directory before/after comparison.

Do not let a broad privacy/config gate that requires intentionally absent live configuration invalidate a focused archive-only code review. Report that evidence boundary separately and base the verdict on runnable exact-candidate gates.

## Verdict format

For Critical/High-only reviews:

1. begin with `APPROVE` or `HOLD`;
2. state only reproducible Critical/High blockers;
3. include exact commit/tree identity;
4. summarize parent exploit reproduction, tip suppression, maintained test outcome, and adversarial probe counts;
5. disclose prohibited/unexecuted live evidence without implying failure;
6. state whether repository files changed and whether disposable artifacts remain.

## Pitfalls

- Treating `str.isdigit()` as canonical ASCII decimal validation.
- Validating only the URL or only the payload instead of both.
- Checking the target account once before mutation but not immediately afterward.
- Accepting exactly one matching name while ignoring role or reserved-ID constraints.
- Deleting recovery credentials after remote success but before local storage success.
- Calling one wrapper invocation proof of one remote mutation without request call counts.
- Reporting password-in-memory as password-on-disk, or overlooking actual argv/output leakage.
- Claiming frame memory was zeroed when only a copied mutable buffer was cleared; report the narrower proven no-persistence result.
- Running archive tests that silently import the moving checkout through a hard-coded root.
- Leaving review archives or generated cache files behind after claiming no modifications.
- Giving the owner a credential-entry command in inline prose or a `zsh` fence that Hermes Desktop may classify as prose; use one zsh-compatible fenced `bash` block and verify it renders the copy control.
- Copying a rotating/single-use refresh token into a throwaway auth home. A successful refresh can invalidate the canonical token and strand its replacement when teardown deletes the sandbox; use a distinct login or an explicitly approved access-token-only projection that fails closed on expiry.

## References

- `references/disposable-oauth-sandbox-auth-projection.md` — refresh-safe authority ordering for disposable OAuth children, exact-path profile-auth merges, access-token-only projections, ambient/fallback exclusion, and the adversarial verification matrix.
