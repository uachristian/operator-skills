# Report and alert evidence hygiene

Orchestrator reporting protocol. No automatic change to cron cadence, delivery, suppression, cooldown, monitor mode, permissions or live actions.

## Truth before brevity

- Bind every finding to the authoritative source, scope, observed time and coverage. Missing/partial/failed/stale inputs mean UNKNOWN or PARTIAL, not zero or healthy.
- Separate active incidents, verified recovered history, unchanged unresolved issues, already-applied source awaiting scheduled verification, proposals and expected silent runs.
- Report owner, concrete next action, blocking reason and severity when actionable. State 'no action needed' only when supporting coverage is complete.
- Count unique incidents by source identity and material state; retain raw attempt counts separately. Similar wording, retries and multiple observers are not necessarily independent incidents.
- Re-read exact current source/receipts before proposing a fix from an old observer packet. Do not reopen a completed fix just because a scheduled output predates it.

## Repetition handling

Compare bounded samples for the same job/source; include output timestamp and content identity, and distinguish recurring identical condition from identical whole report bytes. Confirm whether reminder repetition is intentional. Mark duplicate analysis already incorporated; never silently suppress new evidence, changed impact, unresolved critical failures, deadlines or required periodic coverage.

Monitor/no_agent conversion is a proposal until exact owner approval and before/after behavioral proof. Preserve periodic security, compliance, recovery, strategic and time-dependent checks even when source bytes are unchanged. A negative finding can depend on elapsed time. Do not invent a universal cooldown or force-run a team-facing report to obtain evidence.

Missing newest outputs are UNKNOWN. last_status=ok is scheduler metadata, not full pipeline health; last_status=error may be historical and requires current verification. Distinguish attempted send, confirmed transport delivery and completed business action; don't advance a dedupe ledger on an unsuccessful send.

## Runtime timing correlation

Do not subtract a persisted last-dispatch timestamp from last-run/completion and label the interval execution time unless both are bound to the same run. Hermes can preserve a recurring `last_dispatch` across a manual retry/replacement while stamping `last_run_at` for the latest completion. Queue time and mismatched attempts can turn a short run into an apparent many-minute bottleneck. Use exact attempt-start/completion or run-bound stage telemetry; otherwise label the interval a screening signal and the true runtime unknown. Source call counts can establish redundant work without inventing latency savings.

## Compact report opening

Lead with changed decisions and unresolved approvals. For each actionable/deferred item include stable issue/proposal ID, NEW/CHANGED/UNCHANGED/HELD, CURRENT/HISTORICAL/UNKNOWN, evidence timestamp, proposed owner (not assumed acceptance), exact next action, and approval boundary. Retain supporting detail as private evidence. A one-word output's meaning and confirmed delivery must be checked before declaring it successful suppression or redundant reporting.

## Audit receipt

For each sampled job: store/target owner, sample paths/time range, completeness, repeated condition/incident identities, live-source check, classification, actionable owner/next step, existing controls, and proposed exact improvement. Keep private data out of summaries. If no concrete fix is justified, return no-fix with evidence rather than manufacture a change.

## Safe rollout

Reporting-only wording must preserve all facts and failures. Test healthy, unknown/partial, historical recovery, unchanged active blocker and new critical evidence. Behavior-changing delivery/schedule/monitor/dedupe changes need separate approval; nothing in this document enables them. Retain original output as private evidence; never replace historical logs with sanitized successes.
