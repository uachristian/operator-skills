# Autonomous Improvement Maintenance Notes

Use this reference when a default-profile improvement orchestrator reviews specialist observer/digest outputs and applies low-risk, behavior-preserving fixes.

## Active collector drift pattern

A specialist profile may have a profile-local observer collector script that has already been improved, while the default cron still runs a root/default copy of the same collector. Symptoms:

- The observer report flags impossible metric gaps, such as `propose_write` decisions but zero proposal records.
- Profile-local `scripts/<collector>.py` contains newer parsing logic than `~/.hermes/scripts/<collector>.py`.
- The cron `script` field points at the root/default script path through the scheduler wrapper, so the newer profile-local collector is not actually active.

Safe low-risk fix:

1. Create the required timestamped backup before edits.
2. Backup both the active root/default script and the profile-local source if both will be touched or compared.
3. Sync only behavior-preserving observability/parsing improvements from the profile-local collector into the active root/default script. Do not expand write authority or change downstream actions.
4. If duplicate evidence appears in observer reports, dedupe by stable evidence identity, not by display text. For Slack/Telegram feedback, a good key is permalink/message id + user correction text + bot context.
5. Validate with `py_compile` for touched Python and a smoke run of the collector. Verify the specific metric that was stale is now present.
6. Append one JSON object per fix to `~/.hermes/state/autonomous-improvements.jsonl` with timestamp, profile, area, change, files, risk level, and verification.

## What to defer

- Alias/category changes that require human domain verification.
- Social/public-action promotion.
- Physical-world automation changes.
- New crons, schedule changes, auth/provider/security boundary changes, or live-write expansion.
