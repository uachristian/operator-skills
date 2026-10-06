# Model-Neutral Semantic Shadow Worker Boundary Probes

Use this reference when building or reviewing a read-only local-model worker that consumes copied operational evidence, queues jobs, calls a replaceable model endpoint, and stores proposed analyses without external actions.

## Stable architecture boundary

Keep the durable system independent of any one model or GPU host:

1. versioned job/result contract;
2. persistent queue with leases and bounded attempts;
3. policy and capability router;
4. replaceable inference adapter;
5. strict schema/evidence validator;
6. result and audit store.

Prompts, sampling, reasoning formats, runtime flags, context limits, and hardware assumptions belong behind the adapter. The existing deterministic system remains authoritative for detection, high-risk logic, and actions. A shadow worker may classify, consolidate, explain, or propose; it must not suppress deterministic alerts or inherit mutation authority.

If the owner requires a private repository, create it and verify `PRIVATE` visibility before implementation proceeds. Keep the remote empty until the candidate passes source-policy and exact-tip review.

## Public ingress must preserve the copy boundary

A guarded snapshot importer is not sufficient if a sibling CLI/API accepts arbitrary raw job files.

At every public ingest surface:

- refuse live profile/state roots;
- inspect every existing path component with `lstat` semantics and reject symlink ancestors, not only the leaf;
- require the source file to be inside an explicitly supplied copy root;
- open snapshots through a no-follow descriptor, require a regular file, bound total bytes, and compare descriptor/path inode, size, and modification metadata before and after reading;
- hash the exact stable source bytes and bind that digest into every canonical job before enqueue;
- reject partial or ambiguous source contracts;
- couple evidence source to sensitivity in the canonical job contract;
- require synthetic jobs to contain only synthetic evidence;
- require internal jobs to contain only approved copied/internal evidence;
- derive authentication policy centrally from the validated sensitivity/source, then enforce it again in the adapter.

Adversarial probe: place a structurally valid job under a live-state path and try every public command. A release passes only when no command reads, enqueues, or persists it.

## Batch and queue invariants

For multi-record snapshot import:

1. parse and validate the whole snapshot;
2. construct every canonical job in memory;
3. begin one database transaction;
4. resolve every idempotency collision;
5. enqueue all jobs and audit rows;
6. commit once.

A valid first record followed by an invalid second record must leave zero queued jobs and zero audit rows.

Idempotency must bind the complete canonical job contract, or the contract must explicitly document every excluded field and why exclusion is safe. Comparing only an evidence hash can silently reuse a job with a different identity, deadline, timestamp, or policy. Generate deterministic IDs/timestamps for replayable snapshot imports when exact-contract comparison is required.

Create private SQLite files with explicit owner-only permissions (`0600` on POSIX) before writing evidence. Verify database, WAL, and SHM exposure under the actual runtime user and directory permissions. Reject a queue path containing any symlinked ancestor.

## Model-output fail-closed probes

Treat the model response envelope and its content as untrusted:

- cap response bytes;
- reject redirects, inherited proxies, public/hostname endpoints, credentials in URLs, query strings, and fragments;
- reject both modern `tool_calls` and legacy `function_call`;
- reject `finish_reason` values that indicate a tool/function call even when the message omits the corresponding payload;
- parse only the declared content field;
- parse both envelope and content with a strict JSON loader that rejects duplicate keys, non-finite constants, excessive depth, and oversized documents;
- catch JSON/number/Unicode/recursion failures including `ValueError`, `OverflowError`, `UnicodeError`, and `RecursionError`;
- terminalize malformed output as `invalid` and release the lease;
- bind result identity to the exact `job_id` and normalized input content hash, then require every cited evidence ref to be a subset of the job refs;
- require canonical UTC timestamps with one documented representation and reject non-finite model sampling values before adapter invocation;
- make abstention a strict typed state, not free-form prose.

Probe oversized integers, deeply nested JSON, invalid UTF-8, empty content, forged evidence refs, unknown keys, tool-call finish reasons, and late/stale lease completions.

## Deadline warning

A socket-operation timeout plus an elapsed-time check after the response returns is **not** a hard wall-clock deadline. A slow-trickling loopback server can keep resetting per-read timeouts and outlive the lease.

Do not claim the deadline gate passes until a deterministic slow-header/slow-body server proves that:

- the foreground worker returns by the declared wall-clock limit;
- the queue reaches terminal `timeout` rather than remaining `running`;
- no stale background completion can persist a result;
- timed-out transport work cannot accumulate without a fixed bound;
- the next eligible job is not starved indefinitely.

A proposed thread/process watchdog is not release evidence until those probes pass on the supported platforms.

## Release sequence

1. Freeze scope, prohibited capabilities, acceptance gates, rollback, and source-policy rules.
2. Build synthetic replay fixtures before live copied inputs.
3. Run unit, package, CLI, source-policy, concurrency, and slow-transport probes.
4. Freeze an exact commit or immutable staged-index copy. For a commit candidate, build a clean `git archive`, run source-policy checks inside the extracted archive, build wheel/sdist there, and run the maintained suite against both archive source and the freshly installed wheel.
5. Obtain one bounded adversarial review.
6. Reproduce each HIGH/MEDIUM finding in the parent lane.
7. Convert accepted findings into regression tests and remediate narrowly.
8. Freeze a new exact tip and obtain a fresh verdict.
9. Push only after repository privacy and exact-tip gates pass.
10. Keep deployment, cron/autostart, live copied-data qualification, notifications, and mutations as separately approved phases.

An ancestor PASS cannot release a remediated descendant, and a HOLD candidate must not be pushed as though review were complete.
