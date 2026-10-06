---
name: operational-state-review
description: "Use when auditing live operations to find what humans actually need to act on, proportionate to real risk."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [operations, audit, workflow, human-process, live-state, proportionality]
    related_skills: [development-quality-loop]
---

# Operational State Review

## Purpose

Use this class-level skill when the user asks for the current state of an operational system and wants to know what people need to adjust or do. Examples include shop-management boards, CRM pipelines, collections queues, service desks, inventory workflows, delivery boards, and production-control dashboards.

The deliverable is a grounded, prioritized human action list. It is **not** an automatic invitation to redesign the system, build a new service, or clean every historical inconsistency.

## Scope freeze

Start with a short plain-language contract:

- the immediate operational question,
- authoritative live sources to inspect,
- whether the review is read-only,
- explicit non-goals,
- intended output and rough effort.

Default to active/current records and read-only inspection. Exclude historical, archived, estimate/quote, or separate-business records unless relevant. Do not send messages, mutate records, or start an automation build without separate authorization.

### Conversation and task-continuity gate

Treat an owner correction such as “weren’t we supposed to be working on X?” as an immediate scope interrupt, not as a request for another generic next-step list.

1. Stop the adjacent workstream and do not defend or extend it.
2. Search current session history, prior sessions, canonical project notes, and live project state for the exact named task plus reasonable spelling/product variants.
3. Recover the last approved scope, authority boundary, candidate identity, completed evidence, and unresolved checkpoint before resuming.
4. State the detour briefly, restore the intended checklist, and continue the already-approved read-only or reversible work when safe.
5. Do not infer ambiguous shorthand from folder numbers, version numbers, or the most recent project merely because it is prominent in context. Ask the owner only after source-first recovery is exhausted.
6. Keep completed adjacent work preserved but out of the active recommendation unless the owner explicitly brings it back into scope.

A context summary is evidence about prior conversation state, not proof of current external state. Re-read the live source before making operational claims.

## Evidence precedence

Use this order:

1. Current live source of truth.
2. Current documented SOP or workflow contract.
3. Fresh derived artifacts with visible generation time.
4. Historical reports only as context.

A file named `latest` is not automatically current. Check its embedded `generated_at`, source timestamp, or modification time. If a cached audit conflicts with live state, direct-read the small number of priority records and label the cache stale. Never turn stale findings into a mass human cleanup.

### Candidate-to-live correlation reviews

When joining an operational system to a second evidence source—such as open purchase orders to email, shipments to vendor portals, or service records to messages—freeze the authoritative live set before searching the secondary source:

1. Use cached findings, local feeds, and extracted records only to generate candidate identifiers.
2. Deduplicate to stable exact identifiers, then direct-read each candidate from the live system of record.
3. Classify each as current/open, closed, missing, or unknown. Continue correlation only for current/open; never let stale local state seed a confident match.
4. Preserve coverage evidence. A bounded workflow sample or board lane with `hasMore=true` is not a complete inventory; do not declare “all” without pagination-complete retrieval.
5. Exclude archived records even when a convenience endpoint returns them unexpectedly.
6. Search the secondary source by strongest identifiers first: exact PO/order/invoice/tracking/part number. Vendor-name-only or free-text similarity is supporting evidence, not identity proof.
7. Report source failures as unknown/incomplete coverage rather than `not found`, and keep every mutation outside the read-only review unless separately approved.

This sequence prevents a large historical candidate queue from becoming a noisy action list and makes the final matches explainable record by record.

### Observer improvement packets

When an observer packet cites aggregate queue metrics or a previously reviewed candidate, separate four states before proposing work: historical transport totals, current exact-revision accountability, staged candidate quality, and production activation authority. A reviewed candidate with `production_changed=false` and an owner-gated activation is intentionally held—not a fresh implementation failure. Verify the current source or baseline manifest, record an explicit HOLD when exact approval is absent, and prevent the same historical metric from repeatedly reopening the candidate.

Treat missing physical-world evidence as its own truth class. Workflow lane, due date, company location, and technician assignment do not prove where an asset is or who owns its next physical move. Start with a bounded local human-confirmed read-only pilot, explicit `UNKNOWN` state, hard freshness expiry, and no external writes or recurring automation.

### Integration inventory reconciliation

When an operational dashboard or device integration shows fewer objects than the owner expects, reconcile three separate counts before diagnosing the cause:

1. the authoritative source or physical inventory,
2. the integration's persisted configuration records, and
3. the runtime's currently active connections or telemetry.

Do not treat active sockets, recent events, or discovered devices as the configured inventory. Lazy connections, prebuffer behavior, protocol-discovery settings, offline devices, and recorder-only or proxied channels can all produce different counts. A missing persisted record means the object was never added or was removed; per-object logs are useful only when that record exists. Keep metadata-only discovery and secret-safe configuration inspection separate from remediation, and avoid opening sensitive media when identifiers, protocol status, and endpoint responses are sufficient to prove the gap.

## Review sequence

1. Pull the live board, queue, or pipeline and its status definitions.
2. Separate active work from archives, estimates, internal records, or adjacent businesses.
3. Identify due-today, due-next, overdue, no-date, and wrong-stage records.
4. Compare near-term commitments with visible capacity and unresolved dependencies.
5. Separate clean collections from records that still have production/service dependencies.
6. Distinguish real parts/inventory blockers from metadata hygiene.
7. Verify ownership/assignment directly on the highest-priority records before declaring it missing.
8. Classify telemetry honestly: missing data is unavailable evidence, not measured zero activity.
9. Produce exact human decisions and a small recurring operating cadence.
10. List small system corrections separately; do not begin them automatically.

## Operational truth classes

Keep these categories separate instead of collapsing them into one score:

- schedule risk,
- stage/lane hygiene,
- actual work completion,
- financial/invoice state,
- purchasing or inventory dependency,
- responsibility/assignment,
- customer/team response state,
- telemetry freshness and completeness.

A record can be in a collections lane without being invoiced or collection-ready. A record can have assigned labor while work remains incomplete. A line can lack SKU/cost/inventory linkage without blocking production. A telemetry feed can return no rows without proving no work occurred.

## Product/adoption reviews of operational assistants

When the system under review is an assistant, bot, command center, or scheduled reporting profile, separate **operational proof** from **adoption proof**:

- Operational proof: jobs run, outputs exist, scripts parse, health checks pass, queues populate, and guardrails remain enforced.
- Adoption proof: people initiate sessions, act on cards, accept or edit drafts, close loops, reduce aging work, and save measurable time.

A high-volume scheduler with near-zero user interaction is a working automation engine, not an adopted assistant. Compare outbound summaries and captures with inbound user messages and manual-like actions over the same exact rolling window. Treat compile/self-test receipts and “shipped” documentation as presence evidence only unless production usage or outcome telemetry corroborates them.

For privacy-safe adoption audits:

1. Query session/message databases read-only and aggregate roles, sources, and timestamps without selecting message content or user identifiers.
2. Aggregate action-audit types and dates without printing payloads, refs, labels, or raw messages.
3. Check embedded `generated_at` timestamps before trusting any `latest` scorecard.
4. Use exact rolling timestamps rather than date-only boundaries; boundary-day events can materially change sparse adoption counts.
5. Quantify output burden (lines, tasks, cards, cadence) and duplication (for example, normalized-line Jaccard) without reproducing sensitive text.
6. Compare documented state/audit contracts with live artifact existence. A script plus historical self-tests does not prove the current feedback loop exists.
7. End with a proportional `keep / fix / merge / move / retire-or-park` portfolio, centered on one canonical action surface and outcome telemetry.



## Focused direct readback

Use lane summaries for breadth and direct record reads for decisive claims. Before saying a record is ready, unassigned, collectible, or blocked, inspect the relevant service/assignment/invoice/parts fields for the records that drive the recommendation. Avoid opening every record when a focused sample resolves the uncertainty.

### Event-packet and message-source verification

When reviewing a bot escalation built from Slack, email, CRM, or another message source, treat the normalized packet/log as derived evidence rather than the source of truth:

1. Read the exact live source event by immutable channel/conversation ID and message timestamp when access exists.
2. Compare the live body with the logged copy; check for dropped links, mentions, thread metadata, edits, or preprocessing changes.
3. Resolve every mentioned principal through the source directory. Distinguish self-mentions, active humans, bots/apps, deleted users, and unknown IDs before deciding whether the request already has an owner.
4. Read the message thread for replies, then search later same-channel messages for an out-of-thread completion, order, ETA, or status confirmation. An empty thread alone does not prove the work remains open.
5. Keep classification correctness separate from extraction integrity. A packet may be correctly classified while still carrying an incomplete body or wrong ownership flags.
6. Route to the already-mentioned operational owner when evidence is clear. Do not escalate to an executive or mutate an adjacent system merely because the reporting bot asked for help.
7. Record any durable parser/normalization defect separately from the immediate human action. Do not silently patch production ingestion during a read-only review.

For a concrete Slack supplies-request recipe, see `references/message-event-source-verification.md`.

## Human-process-first rule

When the platform is functioning but staff data is inconsistent:

1. perform a bounded human cleanup,
2. establish a simple daily or weekly operating routine,
3. observe the corrected process for a bounded period,
4. automate only the recurring gap that remains.

Do not answer a workflow-hygiene problem with architecture by default.

## Output format

Lead with the operational verdict. Then prioritize:

1. actions required today,
2. overdue decisions,
3. next-day or capacity risks,
4. lane/queue/collections cleanup,
5. real purchasing or inventory exceptions,
6. one simple recurring human cadence,
7. small system-side corrections for later.

Every action should name the record, current state, observed dependency, and decision required. Prefer “Order 1234 is due today with open labor; deliver or re-promise” over “clean up overdue jobs.”

For repeated system-status checks and completed operational tasks, close with four concise headings so the result remains scannable across sessions:

- **Completed** — changes or checkpoints actually finished; say when the check was read-only and changed nothing.
- **Verified** — timestamped live evidence, including health, parity/drift, safety gates, test counts, and any bounded anomalies.
- **Next** — the immediate safe next stage, not an implied authorization to execute it.
- **Held** — mutations, restarts, publishes, broad auth, or other actions still blocked or awaiting exact approval.

Do not collapse a discovered anomaly into a green headline. State the initial failure, the bounded diagnosis, the verified recovery or fallback, and whether production code changed.

## Proportionality and stop rules

Do not let a current-state review become a multi-hour build. Pause and re-scope if the work:

- exceeds roughly twice the stated effort,
- adds a service, app, database, protocol, or permission boundary,
- changes from review to remediation,
- starts broad historical cleanup,
- or the user says it feels overbuilt or unclear.

A concern about overbuilding is a scope interrupt even if followed by “keep going.” Explain the reduced path before continuing.

## Common pitfalls

- Treating a cached `latest` artifact as live without checking time.
- Reporting an item as still open from past session text without a live recheck. Owner-step items are often already resolved, superseded or obsolete; close those with evidence instead of re-listing them.
- Counting cron output files or a frozen `last_delivered_at` as delivery volume; only gateway `delivered to …` log lines prove a human was messaged.
- Letting an intentional owner hold repeat as a daily CRITICAL; it trains the reader to ignore the channel that would carry a real new incident.
- Treating a generated card, staged proposal, script exit, source disappearance, or audit append as evidence that the underlying outcome closed.
- Letting canonical state and audit/value ledgers commit independently without an event-ID reconciliation path.
- Calling an authoritative read failure `not found`, which can make duplicate/conflict/reply checks fail open.
- Disabling a live callback while leaving misleading `Send`/`Create` affordances in legacy renderers.
- Hardening new audit schemas without migrating raw payloads out of active historical rows.
- Presenting a reply/commitment follow-up list as complete when the source snapshot reports incomplete coverage (unreadable threads, index/window caps, held identities, all-`unknown` states). Lead with the specific evidenced items, state the coverage gap in one line, and never convert `unknown` into either "owed" or "cleared".
- Reusing an older estimate/quote for a customer's new request without matching the scope; old estimates can be unrelated or duplicate already-paid work. Build a new draft from the customer's stated scope, leave unknown labor/pricing as TBD, and keep it owner-review-only.
- Calling every balance in a collections lane clean AR.
- Treating blank purchase status or missing inventory linkage as proof an item was never ordered.
- Inferring staff inactivity from an empty timesheet or telemetry response.
- Recommending mass metadata cleanup before confirming operational relevance.
- Mixing a separate business, internal record, or old estimate into the active operating picture.
- Reporting generic advice instead of exact records and decisions.
- Turning an audit into a new automation project without observing the human process first.

## Verification checklist

- [ ] Live source inspected and timestamped.
- [ ] SOP/workflow contract consulted where available.
- [ ] Archived/historical/estimate/separate-business scope handled explicitly.
- [ ] Stale derived artifacts did not override live state.
- [ ] Priority records direct-read before strong readiness/assignment/collection claims.
- [ ] Missing telemetry labeled unavailable rather than zero.
- [ ] Metadata hygiene separated from real blockers.
- [ ] Human actions list exact records and decisions.
- [ ] System changes remain separate and unstarted unless authorized.
- [ ] Review ended when the requested operational picture was clear.

## References

- `references/maintenance-batch-observation-gates.md` — owner-away maintenance boundaries, fail-closed timeout interpretation, normal-schedule observation, and bounded one-shot readback without creating a recurring cron.
- `references/report-only-observability-and-capacity-mode.md` — additive provenance coverage and scheduled zero-ready prioritization patterns that preserve authorization, eligibility, workflow state, and sends.
- `references/open-items-recall-and-backlog-triage.md`: owner asks "what's still open". Covers the session/Kanban DB recall recipe, live re-verification traps (preview vs stale production, false-negative one-shot checks, intentional scope changes that look like failures), evidence-backed Kanban closure, and a decision-first report.
