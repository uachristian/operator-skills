# Thread-Local SQLite Descriptor Exhaustion in Long-Lived Services

Use this runbook when a supervised Python/ASGI service intermittently reports `OSError: [Errno 24] Too many open files` and shares one SQLite state store across worker threads.

## Root-Cause Workflow

1. Recover the complete traceback from the service log. Cropped chat alerts often stop at `Exception in ASGI application` and are insufficient for diagnosis.
2. Identify the failing operation, then determine whether it is the **cause** or merely the first victim of descriptor exhaustion. Recursive profile/skill scanning can fail even when SQLite consumed the descriptors.
3. Read the process's live soft limit and aggregate numbered descriptors by normalized type and name. On macOS, pair `launchctl limit maxfiles` with `lsof -nP -p <pid>`; do not count `txt`/`mem` mappings as ordinary open FDs.
4. If duplicate handles to the same database and its `-wal` dominate, trace connection lifetime against the service thread model.
5. Watch for the dangerous lifetime mismatch: a long-lived shared database object caches one `threading.local()` reader per thread, while the service creates a fresh short-lived thread per turn. A strong registry that drains only at database shutdown then grows one connection per completed turn.
6. Prove the mechanism against a temporary database: run many sequential reader threads and assert the retained-reader count grows on the old implementation.

## Durable Fix Pattern

Preserve WAL concurrency and same-thread reuse. Store a guard beside each thread-local reader so thread teardown unregisters and closes the tracked connection in its owning thread. The guard should:

- hold the reader strongly;
- hold the shared owner weakly;
- remove the reader under the existing connection-registry lock;
- call the tracked connection's real `close()`;
- contain destructor exceptions;
- leave owner `close()` as the final drain for still-active readers.

Also preserve the tracker and shutdown invariants:

- a tracked connection must unregister **only after** the real SQLite `close()` succeeds; a rejected cross-thread close must remain tracked so raw byte inspection stays refused;
- readers drained by another thread must be cross-thread-close-safe, or shutdown must otherwise synchronize closure with the owning thread;
- reader registration plus thread-local connection/guard assignment must be atomic under the same lifecycle lock, so `close()` cannot drain the set in the registration-to-TLS gap;
- once shutdown begins, cached-reader lookup must fail closed instead of returning a usable connection;
- the owning-thread guard should retry idempotent close so a best-effort owner drain cannot strand a descriptor or registry entry.

A restart or higher `maxfiles` limit is temporary containment only and must not be presented as a durable fix.

## Regression and Adversarial Probes

Require all of the following:

- 40+ sequential short-lived readers leave zero retained connections;
- same-thread reads reuse one live connection;
- dozens of simultaneous readers register while active and drain after join;
- a failed wrong-thread SQLite close remains tracked until the owning thread actually closes it, and raw pre-open inspection stays refused during that interval;
- owner shutdown racing an active reader leaves the tracked registry empty and no reader SQL succeeds after shutdown returns;
- owner shutdown racing the registration-to-TLS-assignment boundary cannot return a live untracked connection or deadlock;
- non-WAL and explicitly read-only fallbacks are unchanged;
- hundreds of sequential readers complete without failures or retained readers;
- focused state-store, SQLite tracking, TUI lifecycle, and dashboard/profile tests pass;
- syntax, lint, and diff checks pass.

## Baseline Test Contamination

If a broad pytest command reveals an unrelated asynchronous extra write or other order-dependent failure:

1. Run that assertion alone several times.
2. Run the identical broad command in a detached worktree at the untouched base commit.
3. If base reproduces it, record it as baseline evidence and do not expand the frozen fix scope.
4. Run the unaffected files separately and report the exclusion plus isolated outcome honestly; never label the broad suite green.

## Controlled Service Release

1. Create and hash the rollback archive and frozen candidate.
2. Obtain a bounded read-only review focused on teardown, shutdown races, SQLite thread affinity, and tracking-registry drainage.
3. Verify launchd resolves to the patched checkout.
4. Inspect process descendants and avoid interrupting active PTY/chat work.
5. Restart only the affected supervised service.
6. Verify new PID, low FD baseline, bounded FD behavior, HTTP health, supervisor state, and the independent endpoint monitor.
7. Preserve the rollback artifact and exact restore/restart procedure.

Do not announce release while a required candidate review remains pending. A late reproducible HOLD reopens the release.