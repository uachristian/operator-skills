# Fleet Log Signal Classification

Use this reference when a fleet report is yellow because of “recent actionable log findings” while launchd, cron preflight, endpoints, and services appear healthy.

## Goal

Clear false positives without weakening the monitor or suppressing unresolved failures. A green result must mean the scanner understands current event state—not that broad error patterns were disabled.

## Investigation sequence

1. Run the live critical-only checker and watchdog before editing anything.
2. Read the latest structured report and identify each affected profile, source file, signal, and fingerprint.
3. Map fingerprints back to source lines locally. Redact IPs, tokens, URLs, customer data, and message bodies before displaying diagnostics.
4. Verify the service behind each finding independently:
   - launchd/systemd state and last exit
   - endpoint/listener probe
   - cron preflight/current marker
   - later success/recovery event
5. Classify each finding as:
   - unresolved operational failure
   - recovered transient
   - expected security enforcement
   - duplicate mirror of another stream
   - structured success data misread as text
   - stale timestamp-free history
6. Back up the scanner and confirm the tracked mirror is clean before patching.
7. Patch the classifier narrowly and add regression tests for both the suppressed case and the unresolved control case.
8. Run the full test suite, syntax check, live report write, critical-only checker, and watchdog.
9. Require report status GREEN/zero warnings only if all real services and probes are healthy. If a genuine warning remains, fix its source rather than adding another suppression.
10. Verify the live scanner and tracked mirror are byte-identical; commit locally according to the repository workflow and do not push without the applicable approval.

## Classification rules

### Structured JSON reports

Do not keyword-scan valid JSON line by line. Parse it and evaluate explicit operational fields.

Treat as failure when relevant fields indicate it, for example:

- `ok: false`
- `success: false`
- non-empty/non-null `error`
- positive or non-empty `errors`
- operational `status` equal to `error`, `failed`, `failure`, or `critical`

Treat `error: null`, `errors: 0`, `ok: true`, and business text that merely contains words such as “failed login” as non-failures unless an explicit operational field says otherwise.

### Timestamp semantics

A timestamp-free traceback or stderr continuation line must not inherit the file’s current modification time when the same file contains parseable timestamped records. Use the timestamped event header as the age authority.

A long-lived timestamp-free aggregate stderr file may be excluded only when a current structured stream or live probe covers the same failure mode. Do not use this rule to hide a failure that has no replacement signal.

### Duplicate streams

Hermes may write the same event to `agent.log`, `errors.log`, `gateway.log`, and process stderr. Deduplicate exact normalized fingerprints across streams before counting warnings.

The report should preserve source metadata, but one event must not become several warnings just because multiple handlers recorded it.

### Recovery correlation

A failure copied to `errors.log` may have its recovery only in `gateway.log`. Build a profile-level set of recovered fingerprints from the authoritative/current stream and use it when classifying duplicates.

Recovery suppression is valid only when a later success event follows the failure. The same failure without a later recovery must remain actionable.

### Expected enforcement and transport noise

Successful access-control blocks are evidence that the guard worked, not fleet failures. Transient transport fallback/reconnect attempts are noise only when a later recovery or successful live probe proves resolution.

Prefer stateful recovery logic over permanently suppressing a broad phrase such as “connection failed.”

## Minimum regression matrix

Add tests proving all of the following:

1. An identical current error in two mirrored logs counts once.
2. A recovered reconnect counts zero.
3. The same reconnect without a later recovery counts one.
4. Recovery in `gateway.log` clears the duplicate failure in `errors.log`.
5. Valid JSON with `error: null`/`errors: 0` counts zero.
6. Valid JSON with `ok: false` or a non-empty error counts one.
7. A timestamp-free traceback continuation in a timestamped log does not become current because the file was appended.
8. A timestamp-free aggregate is ignored only when another signal covers it.
9. A real timestamped `ERROR`/`CRITICAL` remains actionable.
10. Healthy critical-only and watchdog paths print nothing and exit zero.

## Verification contract

A log-signal fix is complete only when:

- syntax/compile checks pass
- the full tracked test suite passes
- live and tracked scanner copies match
- cron preflight has no new critical or warning state
- the written fleet report shows zero warnings only when live probes are healthy
- critical-only checker stdout is empty with exit 0
- independent watchdog stdout is empty with exit 0
- rollback backup exists
- the class-level skill and vault infrastructure note are updated

## Anti-patterns

- Adding a broad regex solely to force GREEN
- Deleting or truncating logs to clear a warning
- Treating file mtime as event time for mixed timestamped/untimestamped logs
- Counting raw JSON keys as text errors
- Suppressing every reconnect failure without proving recovery
- Trusting process exit 0 without reading the generated status report
- Reporting success after only the first warning clears while new warnings remain
