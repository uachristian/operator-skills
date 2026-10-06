# Operational Cron Change Checklist

Use this reference for production cron/scheduler changes where the user wants behavior preserved while timing, delivery, or notification rules change.

## Safe Sequence

1. Resolve the exact profile and job ID first.
   - Do not assume default profile; use the profile that owns the automation.
   - For Hermes crons, prefer `hermes --profile <profile> cron list` before editing.
2. Use the scheduler's edit command instead of hand-editing JSON when possible.
   - Example: `hermes --profile <profile> cron edit <job-id> --schedule '0 8 * * *'`.
3. Preserve orthogonal behavior.
   - A schedule change should not alter delivery, `no_agent`, script, skills, model, or workdir unless the user requested it.
   - If the user says "still want it to run" but "don't send messages", keep the cron schedule active and gate notifications inside the script.
4. Verify the persisted state.
   - Check list output and the underlying `jobs.json` entry for `schedule.expr`, display fields, enabled/state, script, delivery, and `next_run_at`.
5. Separate configuration readback from subsequent execution proof.
   - Do not manually clear historical errors or force a run merely to turn status green. If approval excludes forced runs, verify the settings and let the natural schedule update execution status.
   - For an approved manual run, prefer `cronjob(action='run', job_id=...)`; current Hermes dispatches it asynchronously and returns a handle. Do not wait or poll after dispatch; continue other work and process the completion event when it returns.
   - After completion, read the exact output artifact plus `jobs.json` status/error/delivery fields. Dispatch alone does not prove successful inference or delivery; `[SILENT]` output can intentionally suppress delivery.
   - CLI run behavior is version-dependent: inspect current help/docs before assuming it only marks a job due or launching an additional scheduler tick. Never start a duplicate run after an uncertain/interrupted result without inspecting state.
6. Update knowledge layers that mention the job.
   - Skill notes for the automation class.
   - Vault / runbook docs if the user requested or if the schedule is operationally durable.
7. Report only the final changed state and verification, not a long change-control narrative for routine green-lit changes.

## Pitfalls

- Do not move a job to weekdays-only when the requirement is "run daily but don't bother the team on weekends". That loses the background data collection/reconciliation value.
- Do not rely on cron delivery settings alone for notification behavior. A `deliver: local` no-agent job can still post to Slack directly from its script.
- Do not forget profile-scoped cron files under each profile's own `cron/jobs.json`.
- For `no_agent`/script-only jobs failing with `Script timed out after 120s`, check the measured script runtime before optimizing blindly. Hermes resolves the script timeout from `HERMES_CRON_SCRIPT_TIMEOUT`, then `cron.script_timeout_seconds` in `~/.hermes/config.yaml`, then the 120s default. Use `hermes config set cron.script_timeout_seconds <seconds>` for an approved fleet-level timeout increase, back up `config.yaml` first, and verify with `from cron.scheduler import _get_script_timeout` rather than hand-editing protected config files.
