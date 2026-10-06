---
name: automation-accuracy-audits
description: "Use when measuring or improving a bot's or classifier's real-world accuracy against evidence instead of adding more reports."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [accuracy, evaluation, sqlite, dedupe, automation]
    related_skills: [operational-change-control, build-execution-standard]
---

# Automation accuracy audits

## When to Use
Use this skill when the owner asks how to make a bot (triage bots, operations assistants, intake pipelines) more accurate or more useful. It also applies when evidence tables, backlog counts or watcher timeouts look wrong.

## Always-on rules
- **Cron health is step zero, not the answer.** Green jobs prove the bot runs, not that it is correct. Measure outcomes.
- **Don't add reports.** Owners want fewer, better human asks, not new digests or scorecards.
- **Keep the write boundaries.** External systems stay read-only (business systems, vendors, chat) unless a gate already exists for that write. A local DB mutation (compaction, table replace) needs the owner's go, plus a paused writer, a verified backup and a written rollback.
- **Tool approval cards need a click in the UI.** A chat "go" does not satisfy them. If a card times out, stop and report the exact remaining step; never reroute around it. Before a batch of install/live steps, tell the owner to stay near the app.

## Procedure
0. **Reconcile the test target before measuring.** Compare installed code, recovery/source mirrors, and the latest closeout; a clean mirror can still omit deployed accuracy safeguards. Inspect test fixtures and conftest overrides for disabled budgeting, substituted timing, or other legacy policy defaults. Label those tests as legacy controls rather than current-runtime qualification. Include required Git-ignored source/test dependencies in any explicit snapshot inventory; an archive of tracked files alone may omit the behavior being evaluated. Do not overwrite unknown-owner changes or treat source observations as measured production error rates.
1. **Separate unique facts from copies.** For every large table, compare `COUNT(*)` with the number of distinct rows by material content (business identifiers, ignoring timestamps). Hundreds of copies per fact means the row identity includes a volatile key. Fix that before trusting any count.
2. **Measure each stage against outcomes:**
   - extraction confidence and model error rate
   - which fields go missing most often
   - unlinked identifiers (PO without work order)
   - card funnel: posted, replied, expired, auto-closed
   - scorer spread: share of "show" answers and share of "high" confidence
3. **Build an answer key** from real outcomes:
   - Strong labels: verified human replies, live-system auto-closures, resolved queue items.
   - Weak labels: expired or stale items.
   - Exclude anything the bot authored itself.
   - Score per item, using the last prediction before the outcome, not per prediction.
4. **Rank fixes by payoff.** Usual order: dedupe the store → deterministic-first extraction → deterministic linking from the system of record → answer key → fix or retire scorers.
5. **Prove optimization invariants before restructuring the pipeline.** Write focused counterexamples for priority order, admission denial, deadline exhaustion, identity changes and failure preservation before batching or caching. Establish whether the proposed saving is compatible with those invariants; fewer calls alone is not acceptance. Use the bounded workflow in `references/pipeline-optimization-invariants.md`.
6. **Run independent fixes as parallel subagents** in separate git worktrees, then merge. Each subagent gets bounded scope, no live writes and a commit-when-green instruction. Finish any child that stopped short yourself, and re-run the full suite after merging.

## Rules and pitfalls
- **Row identity:** hash only material content. Exclude `generated_at`, `captured_at`, `ingested_at`, `updated_at`, age/staleness counters and similar volatile keys, otherwise every regeneration re-inserts the whole snapshot. Upsert on that identity and keep the latest observation time. The same bug in a scorer's evidence fingerprint makes it re-score unchanged evidence.
- **Identifier regexes:** require a standalone label boundary and a digit in the value. Test both positive and negative cases, including forms glued to the number (`PO5678`), JSON keys (`"po_numbers": ["po1234"]`) and words containing the label (`published`, `popular`). A `\bpo\s*` pattern matches inside words, and `\bpo\b` misses glued forms.
- **Deterministic-first extraction:** try labelled patterns first and ask the model only for the gaps. Deterministic values always win. Drop any model identifier that does not appear literally in the source text. If the model is down, fall back to deterministic-only instead of exiting.
- **Linking:** use read-only lookups against the system of record and record a local link only when there is exactly one match. Ambiguous or missing results go to a human. Live evidence overrides a stored link. Cap and pace the lookups, and stop on auth errors or repeated errors.
- **Scorer retirement:** a scorer that flags about 100% of items at uniform high confidence, and saves zero unneeded human asks against the answer key, should be disabled rather than prompt-tuned on a handful of positives.
- **Schema-valid is not correct:** strict JSON schema plus consumer validation proves shape only. Qualification gates must also assert the expected semantic outcome per fixture and exit nonzero on any mismatch or missing case. A harness that computes a semantic flag but exits on consumer success alone gives a false green. Qualify with fixed synthetic positives, a fresh holdout and negative controls (withdrawn, fulfilled, none), run once each on the approved local route with no retries.
- **Reconcile dynamic-schema tests independently:** when restored source replaces a static schema with request-local ID enums, construct expected obligation, evidence and promise sets from the synthetic fixture and retain full-schema equality. Do not use the production schema builder as its own expected-value oracle or delete stale assertions merely to pass. Run installed-style flow tests alongside parser tests so producer/consumer compatibility is actually exercised.
- **Constrain generation from request-local facts, not by loosening validation:** build enums for the evidence, known-item and eligible-promise IDs in each request, and pass the eligible IDs explicitly in the prompt. Instructions that conflict with the validator ("reconcile every known item" vs "return one new item") produce steady rejections that look like model flakiness.
- **Clearing needs its own evidence:** a model's no-action or resolved state must cite the evidence that resolves it (for example a later direct cancellation). Otherwise downgrade it to `unknown` plus a review action. Carried historical items whose anchor left the bounded window stay `unknown`, never cleared. For multi-request threads, require independently verifiable request→promise→cancellation linkage before narrowing a thread-wide safety check; model citations, adjacency and topic similarity alone do not prove that linkage. If the source protocol lacks it, preserve unknown and characterize the limitation with positive and negative tests rather than present a looser rule as an accuracy fix.
- **Bind interpretation caches to implementation identity:** key cached model interpretations to a hash of the exact interpreter source or prompt and schema, not just input metadata and TTL. Otherwise a fix leaves old false results replaying until the TTL expires. Invalidate by identity mismatch; keep obligations, manual dispositions and fairness state. Expect a temporary wave of `unknown` while items are re-interpreted.
- **Agreement is not accuracy:** when comparing a candidate classifier against the incumbent, a shadow agreement rate says nothing about which model is right. Hand-check a gold set of real items first (allow a set of acceptable labels for genuinely ambiguous items) and split tune/holdout before iterating.
- **Disagreements usually expose the taxonomy:** group disagreements by (incumbent → candidate) pair before blaming either model. An overloaded or missing category (for example, vendor back-and-forth filed as "internal") drives most errors in both.
- **Same question vs same question:** after rewriting category definitions for the candidate, rerun the incumbent with the identical definitions and inputs before claiming a candidate win. The definition change alone can close most of the gap.
- **Second-opinion gates:** if two similar-accuracy models are far more accurate where they agree, auto-apply only on agreement and route disagreement to review with a recorded reason. The gate may only downgrade, and an outage of the second model must reproduce old behavior exactly. Report the review-load cost next to the accuracy gain.
- **Frozen-baseline parity tests:** add new output fields only on the new code path, so existing outputs stay byte-identical. Optional-module imports must fall back to the old behavior.

## Capacity and incomplete-evidence checks
- Preserve incomplete acquisition as unknown through the final human-facing renderer. A resolver's schema/query/truncation failure is not proof that tracking or other evidence is absent; test the actual resolver-to-digest path.
- Verify the installed scheduler contract before constructing a timing baseline or proposing a scheduler replacement. Inspect both the configuration and loaded service (`StartInterval` in the plist and `launchctl print gui/$(id -u)/<label>` on macOS), then read the entrypoint for one-shot versus completion-plus-delay behavior. Check the platform's busy/sleep/missed-slot semantics; do not infer them from a replay helper. If the desired interval already exists, stop the duplicate build and correct any recommendation based on a counterfactual baseline. Configuration proves scheduling intent, not measured jitter or continuous freshness.
- Compose refresh tests with the actual shared-budget implementation and one consistent virtual clock. Model the verified scheduler's interval/skip behavior; sample freshness throughout acquisition as well as at completion and before the next tick. Compare competing demand on equal wall-time arrival traces, not only equal cycle counts: a shorter cadence compresses per-cycle demand and can conceal increased requests per minute. Separate legacy fixtures that disable budgets or reset alert timing from current-policy proof. If every cycle already fills its service cap, earlier eligibility cannot create throughput—do not claim a threshold-only fix.
- Suppress repeated vendor fallback calls only for explicit terminal error codes, scoped to one vendor and one request. Retain the original error and test fresh-request retry eligibility plus healthy/transient controls; call-count savings do not establish elapsed-time savings.

## Contained qualification
Before parallel implementation, verify the exact interpreter can import the test runner and execute a representative contained test; share that adapter with workers instead of letting each repeat setup discovery. Keep collection/startup failures separate from semantic regressions. When nested test sandboxes fail before assertions, use `references/contained-qualification.md` to compose one verified boundary without weakening privacy or command restrictions.

## References
- `references/sqlite-evidence-compaction.md`: backup-gated build/verify/apply recipe for compacting a live SQLite evidence DB, plus a source-manifest merge note.
- `references/classifier-comparison-and-agreement-gate.md`: shadow → backfill → gold set → fair rerun → agreement-gate install recipe for replacing or backing up an LLM classifier.
