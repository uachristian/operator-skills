# Maintenance-batch observation gates

Use this during autonomous, owner-away operational review when a newly surfaced cron error may be transient but its safety contract must remain intact.

## Pattern

- Separate scheduler health from artifact health and child-action attestation. A scheduler may be healthy while an artifact is degraded; a script may also be correctly marked errored because it failed closed on unknown child state.
- Inspect metadata first: current job status, newest output, compact aggregate logs, and the immediately preceding scheduled run.
- If a child lookup times out and negative-write attestation is unknown, never reinterpret it as `write_performed=false`. Confirm the parent stopped before downstream processing.
- Do not force-run owner-sensitive or portal workflows merely to clear an error badge. Prefer the next normal scheduled run when the prior run was healthy and the cursor/batch design can advance naturally.
- For delayed readback, use a bounded one-shot background observer that only reads scheduler/output metadata after the next scheduled run. Do not create a recurring cron for a one-time observation.
- Escalate to a production change only after repeated normal-run evidence shows the same failure class, cursor stall, or sustained operational blindness.

## Owner-away boundaries

Safe: read-only audits, private-repo visibility verification, fetch-only remote-ref refresh, rollback-backed documentation corrections, local review branches, deterministic tests, and one-shot metadata readbacks.

Defer: gateway restarts, cron/config changes, credential/session retries, timeout increases, live-write authority, customer/team messages, public pushes, and any change that weakens fail-closed evidence.
