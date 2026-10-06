# Classification examples

These examples capture reusable evidence patterns from a cross-project audit. Adapt the pattern; do not assume the same project remains in the same state later.

## True operational loose end

**Pattern:** An enabled scheduled job has repeated timeout/error metadata, a stale or empty lock remains, and the expected downstream phase did not run. Sibling jobs are healthy.

**Classification:** The specific job is a true operational loose end. The broader system is not necessarily failed.

**Report:** Name the bounded defect, latest failure class, downstream evidence, and one repair target such as phase budgeting/checkpointing/lock cleanup. Avoid recommending a whole-system rebuild.

## Source/live release hygiene loose end

**Pattern:** Runtime is mostly healthy, but the canonical repository is dirty and source-authority hashes or deployed copies disagree.

**Classification:** True source/release hygiene loose end, separate from runtime availability.

**Report:** Reconcile ownership and exact parity before commit/deploy. Do not overwrite one copy based only on mtime.

## Owner-gated ready work

**Pattern:** Research, assets, or a draft package exist, but publication requires owner-provided inventory facts, reauthentication, exact approval, or public-action confirmation.

**Classification:** Owner-gated ready to resume, not interrupted.

**Report:** State exactly what is complete and list the minimum missing owner inputs. A policy-ineligible sibling item is closed/rejected, not part of the pending queue.

## Intentionally deferred safety gate

**Pattern:** A closeout explicitly says a disabled installation or no-live-write phase completed and stopped before the next execution gate. Current state confirms disabled/no authority.

**Classification:** Intentionally deferred roadmap.

**Report:** Cite the stop boundary and the owner decision needed to resume. Do not call absence of later execution state a failure.

## At-home or physical-verification backlog

**Pattern:** A concept document says physical identity, button presses, device state, or rollback testing must happen while the owner is home, and explicitly says the note is not authorization.

**Classification:** Intentionally deferred, owner/physical-presence gated.

**Report:** Preserve the verification sequence. Do not remotely “finish” it or classify unknown/unavailable devices as stale.

## Completed but roadmap stale

**Pattern:** An older roadmap says an integration or recurring job is pending, while a later closeout and current cron metadata prove it is deployed and healthy.

**Classification:** Completed, documentation stale.

**Report:** The loose end is documentation hygiene only. Do not restart implementation.

## Reviewed change awaiting approval

**Pattern:** A review identified a valid prompt/ranking/behavior improvement, but the final session explicitly says no production change was applied pending an exact owner approval phrase. Current jobs remain healthy.

**Classification:** Intentionally deferred approval item, not an interruption.

**Report:** Optional next action is the exact approval-gated change. Rank it below current operational breakage.
