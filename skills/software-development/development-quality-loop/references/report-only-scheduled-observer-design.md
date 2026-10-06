# Deterministic report-only scheduled observers

Use this pattern when a hardened exporter or sync command must be observed for days before any proposal, commit, deployment, or source-system mutation is allowed.

## Separate the exporter from the observer

A `--check` flag proves only that committed output is not replaced. It is not automatically a usable observer contract. Before scheduling, verify that check mode can distinguish:

- semantic no-change;
- ordinary change;
- policy hold;
- source/validation failure;
- lock contention.

Require a machine-readable bounded report containing old/new counts, public IDs and display names, sanitized field deltas, duration, aggregate retries, hold reasons, and a canonical semantic hash. Remove volatile timestamps before hashing. Keep stable sanitized error codes; never surface response bodies, query-bearing URLs, headers, cookies, stack traces, or credentials.

A useful child-process exit vocabulary is `0` for no-change/change, a distinct code for policy hold, a distinct temporary-failure code for lock busy, and `1` for source/internal failure. The outer observer may translate expected hold/busy outcomes so a no-agent scheduler delivers a clean alert rather than a generic crash message.

## Freeze the authority surface

At observation start, persist:

- exact implementation commit;
- committed snapshot raw hash;
- committed snapshot semantic hash;
- explicit IANA timezone;
- explicit first and end-exclusive calendar dates;
- expected schedule slots.

Refuse or hold on implementation drift, baseline-byte drift, corrupt state, or unexpected repository changes. If the shared checkout changes during review, continue reading the immutable Git object and state clearly that the moving worktree supersedes any current-worktree verdict.

For a strictly read-only audit, remember that many check commands still create lock files, temp files, caches, or state. Do not execute them unless that local mutation is authorized. Prefer source inspection and pure no-I/O function probes, and disclose any transient artifact that was created.

## Keep scheduler execution deterministic

For script-only/no-agent scheduling:

1. Use one real script under the scheduler's allowed scripts directory; do not rely on an escaping symlink.
2. Invoke the runtime directly rather than a package-manager wrapper whose banners would make healthy stdout nonempty.
3. Set the child subprocess `cwd` explicitly to the repository root. Verify actual scheduler code/behavior instead of trusting a documented `workdir` claim.
4. Re-exec or spawn with an allowlisted minimal environment. Public-source observers should not inherit provider, gateway, CRM, or customer-data credentials.
5. Pin the scheduler's IANA timezone. A blank setting that happens to match the host today is not a durable timezone contract.
6. Compare the scheduler's outer script timeout with the exporter's request/retry budget. Add a shorter observer-level deadline with cleanup margin; avoid an outer timeout that kills the process before it can persist evidence and emit a sanitized alert.
7. Confirm empty stdout is truly silent and that nonzero script exits are delivered as watchdog failures.

## Local state and evidence

Keep state outside the repository in owner-private directories. Recommended artifacts:

- immutable observation config;
- atomically replaced state JSON;
- one bounded JSONL evidence file per local date;
- ephemeral candidate directory removed in `finally`;
- advisory lock under an owner-private run directory.

Use directory mode `0700`, file mode `0600`, fsync-before-rename state updates, and bounded retention. Record each scheduled slot, outcome, counts, deltas, semantic hash, retries, duration, baseline hash, and whether the baseline remained unchanged.

For removal safety, persist distinct complete-source observations with timestamps. Two observations must be far enough apart to be independent; a single incomplete index is never removal authority.

## Silence, alerting, and dedupe

- Healthy no-change: exit success with completely empty stdout.
- New semantic change or hold: emit one bounded fixed-shape private alert.
- Repeated identical candidate: silence by deduping on `{state, semantic_hash}`.
- First handled source failure: log locally and remain silent if policy requires two consecutive failures.
- Second consecutive failure or freshness breach: emit one sanitized private alert, then dedupe until the condition changes.
- Internal observer/state/lock failure: exit nonzero immediately so the scheduler's watchdog path alerts.

Base freshness on expected scheduled slots when the longest normal interval equals the alert threshold; raw completion-time jitter otherwise creates false alarms.

## Observation completion is not promotion

At the end of the explicit window, emit a one-time `ELIGIBLE_FOR_REVIEW` or `HOLD` summary. Require:

- elapsed calendar window and accounted expected slots;
- required consecutive successful validated reads;
- at least one true no-change;
- no unresolved freshness, lock, scheduler, delivery, state, or baseline-integrity failures;
- secret/raw-body scan clean;
- every real change summarized and held;
- no repository, deployment, or source mutation.

Never switch modes automatically. A successful report-only period authorizes only human review for a later proposal-only stage. Automatic publication needs a separate evidence period and a new explicit approval.