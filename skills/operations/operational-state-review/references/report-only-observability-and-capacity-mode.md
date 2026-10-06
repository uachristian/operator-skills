# Report-only observability and scheduled capacity modes

Use this pattern for read-only operational remediations that add evidence or prioritization without changing authorization, record eligibility, workflow state, or sends.

## Provenance coverage without enforcement

When a shared JSONL audit schema has incomplete authorization metadata:

1. Identify the live producer/store before patching a dormant plugin reporter.
2. Keep the legacy schema and dual-write an additive structured provenance object.
3. Record only explicit producer-supplied facts: authorization class, approving surface, safe session/correlation ID, authorization timestamp, and a whitelisted symbolic bounded intent.
4. Never infer structured proof from source labels and never backfill historical rows as approved without evidence.
5. Add parallel `complete / partial / legacy-only / missing` coverage metrics. Preserve existing authorization classifiers, alert thresholds, eligibility, hooks, and sends during the report-only phase.
6. Ensure merge code preserves existing nested approval fields; replacing a nested authorization dictionary while adding tier/platform metadata silently destroys provenance.
7. Use synthetic rows and aggregate-only output tests so review tooling cannot expose customer or payload content.

## Scheduled zero-ready capacity mode

For a daily board that should enter a read-only capacity-protection mode after repeated zero-ready mornings:

- Keep the high-frequency operational snapshot as the canonical source of readiness and blockers.
- Let the once-daily scheduled report own the streak observation.
- Qualify only explicit scheduled-morning, fresh, successful, non-duplicate observations where `ready == 0` and blocked/at-risk pressure is positive.
- Activate on the second qualifying morning; reset on one valid ready-positive morning; manual/stale/error/future/duplicate runs do not mutate state.
- Persist only aggregate streak metadata, never record/customer detail.
- If the scheduler does not attest job identity in the subprocess environment, use a dedicated scheduled wrapper with an explicit observation mode; keep manual/default execution non-observing.
- Change only report presentation: inline warning plus reranking of an already-eligible candidate pool. Do not modify underlying eligibility, readiness classification, write recommendations, queues, destinations, or cadence.
- Rank with structured evidence and conservative treatment of unknown blockers. Never claim “one action to unblock” unless exact evidence actually proves it.

Synthetic tests should prove state transitions, same-day idempotency, stale/manual/error no-ops, deterministic ranking, unchanged section membership, one warning, aggregate-only state, and no additional send path.
