# Bounded Filesystem Mutation and Capture Review

Use this reference for plugins and local services that mutate canonical files on iCloud/File Provider, network mounts, FUSE, removable media, or any storage whose metadata calls can stall. The same model applies to durable note capture, local proposal publication, generated manifests, and staged file promotion.

## Trust and liveness boundary

The request thread may validate cheap in-memory inputs and write a private local worker payload. Every source-backed operation belongs inside one killable worker deadline, including:

- `resolve`, `exists`, `is_file`, `stat`, globbing, and relative-path calculation;
- policy-file checks and allow/deny authorization;
- reading the current target, drafts, or audit log;
- atomic replacement, append, rollback, and source-marker reconciliation.

Do not claim boundedness when only the final `read_text` or `write_text` is in the worker. File Provider can stall during canonicalization or metadata lookup.

Partially initialized providers must still place payloads, locks, receipts, and temporary state under profile-local runtime state. Never fall back to creating worker state inside the source tree merely because an index/state path is absent.

## Transaction model

Classify side effects instead of pretending multiple files are one atomic transaction:

1. **Canonical commit** — the durable target or draft that represents the requested mutation.
2. **Required coordination** — a queue/index record whose absence makes the canonical commit operationally incomplete.
3. **Secondary audit** — logs/telemetry that should warn on failure but must not falsely turn a committed canonical write into an error.
4. **Local receipt** — private idempotency state, bounded by age/count and verified against current canonical source before trust.

Embed a deterministic operation marker in canonical source. Derive the operation ID from normalized semantic inputs, not a random retry-time UUID. Exact retries should first validate a private receipt against the marked source; if the receipt is missing after a crash, reconcile from the source marker before creating another draft/update.

A receipt alone is insufficient: users or other tools can delete or move the source. Reject stale receipts whose exact marked target/draft no longer exists. Bound receipt and stale-payload retention so reliability state cannot grow forever.

## Crash-window probe matrix

Use disposable copies or test-only monkeypatching; do not add production sleep hooks.

1. **Before source work** — inject a multi-second stall at the start of the worker transaction and set a short parent deadline. Require bounded return, worker termination, payload cleanup, no source note, and conservative dirty/refresh state.
2. **After canonical commit, before receipt** — inject a stall immediately after the atomic source write. The first call must time out with no receipt. An exact retry through the unmodified implementation must recover one source object, one marker, one receipt, and one content occurrence.
3. **After promotion, before required coordination** — for draft→published or target→queue workflows, stall after target/draft commit but before queue emission. The exact retry must finish the missing queue step once without duplicating the target or draft.
4. **Secondary log failure** — force audit-log append failure after the canonical commit. Return committed success with a warning, dirty the index/cache, and prove an exact retry remains idempotent instead of being rerouted as a new proposal.
5. **Rollback failure path** — force required coordination to fail normally (not by process death). Roll back only files carrying the current operation marker; never unlink a pre-existing or concurrently created unrelated target.
6. **Concurrency** — hold the real cross-process lock from another process and require a bounded busy/retry result with zero source mutation. Then run two exact operations and prove at most one canonical write/receipt.

Run the maintained focused and repository-wide suites after these probes. Re-run them from the frozen exact tip after the last remediation.

## Worker payload and receipt requirements

- Owner-only regular files (`0600`) under an owner-controlled local state directory.
- Size bounds and strict schema/type validation before plugin/provider invocation.
- No shell invocation; fixed interpreter and worker paths.
- Operation IDs validated before use as filenames.
- Atomic receipt writes and owner/type/mode checks on receipt reads.
- Count/age pruning that does not follow symlinks or delete foreign-owned files.
- Payload cleanup in `finally`; stale-payload cleanup must be owner/type/age bounded.
- Error output must not echo captured content, credentials, or raw worker stderr; use stable classifications or hashes.

## Release evidence

A release packet should include:

- frozen commit/tree and clean-status proof;
- public-handler call graph showing only the bounded worker entrypoint reaches source-backed methods;
- maintained tests for parent-thread isolation, timeout cleanup, receipts, stale receipts, partial initialization, locks, policy gates, secret rejection, and rollback ownership;
- actual-process kill probes for the pre-commit and post-commit windows;
- source/live byte parity, backup manifest, rollback script, one controlled restart, and live readback;
- a fresh exact-tip reviewer verdict. A reviewer run with exit code zero but no parseable final verdict, `completed=false`, or a session-storage failure is **not review evidence**. Do not count token/API activity as a verdict, and do not repeatedly redispatch the same broad review without fixing the failed evidence channel or narrowing the question.
