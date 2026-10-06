# Pipeline optimization without accuracy regressions

Use when reducing repeated reads, batching metadata validation, or changing the acquisition/interpretation order of an existing automation.

## Procedure

1. Freeze the recovered current-behavior baseline, not a stale mirror or rejected candidate. Qualify its representative producer→parser→consumer path before optimization; keep recovery-source reconciliation in its own commit.
2. Describe the saving and the protected event ordering separately. Record when admission happens, which item has priority, when an attempt is recorded, which reads certify which histories, and how budget exhaustion preserves unresolved work.
3. Build actual-code synthetic counterexamples before editing:
   - A high-priority discrepant item followed by a lower-priority matched item, with interpretation consuming most of the remaining time.
   - Multiple discrepant items sharing a late metadata observation, then enough time for interpretation but not another read.
   - Admission denial on the first eligible item; verify no extra histories or interpretations occur beyond the baseline contract.
   - Identity/blacklist/activity changes in the revalidation response; incomplete, duplicate or missing index rows; failure and deadline boundaries.
4. Assert each invariant independently. A priority test should assert order or which item gets the first scarce slot, not an arbitrary total call count. If eliminating work frees enough time to process a second item, that is not itself a priority violation. Keep throughput, admission limits and budget assertions separate so correcting a test cannot conceal a real ordering defect.
5. Share a metadata observation only if it occurs after every history it certifies and satisfies the existing freshness/identity contract. Do not reuse an early observation for later histories. Do not prefetch additional private histories merely to enable batching when baseline admission would have stopped acquisition.
6. Charge the remaining budget for operations still required: distinguish unacquired history, an outstanding shared metadata read and interpretation-only work. Test exact-fit and insufficient-time boundaries. Preserve fairness/attempt semantics; recording a history attempt must not silently stand in for completing interpretation.
7. Compare baseline and candidate on the same traces. Report actual read counts separately from elapsed-time measurements, output equivalence, and unknown/review workload. Run the representative combined gate after each accepted change and disclose unrelated full-suite blockers without calling a subset a release pass.
8. If the bounded remediation fails, retain the reproducible tests and trial patch, restore the qualified source baseline in isolation, and explicitly supersede the optimistic candidate report. Do not leave a rejected optimized HEAD appearing release-ready while only the working tree contains the fallback; record both identities and isolate any later redesign from the qualified baseline.

## Completion decision

- Fewer calls with preserved admission, priority, evidence and deadlines: eligible for frozen review, not automatic deployment.
- Fewer calls requiring extra acquisition after denial or weaker evidence: reject the optimization.
- No safe sharing opportunity under current contracts: document the proven constraint and keep baseline behavior; a new data/scheduling contract is separate scope.
- Cancellation ambiguity without explicit linkage: retain conservative unknown; a standalone contract validator or design is not an integrated cancellation feature.
