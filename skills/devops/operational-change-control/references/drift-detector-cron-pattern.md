# Drift-Detector Cron Pattern

A "watcher" cron whose job is to stay silent until something has gone wrong, and to name the offending entity when it fires. Use this for steady-state guards rather than progress trackers.

## When to use

- A piece of state should remain at a known value indefinitely (e.g. "the default profile should run zero crons").
- The cost of the bad state is non-zero but not immediately catastrophic — you want a nudge, not a page.
- A human (or another agent) might accidentally violate the invariant via a normal-looking command (`hermes cron create` on the wrong profile, `cp` into the wrong directory, an env var landing in the wrong `.env`).

The "silent unless drift" idiom is preferable to a progress tracker (the inverse — "fires when migration completes") because steady-state guards remain useful long after any migration is done. They naturally outlive the project that motivated them.

## The pattern

A pure-script cron (`--no-agent`) that:
1. Reads the current state via the same CLI/API the user would.
2. Compares against the invariant.
3. Exits silently (`exit 0`, empty stdout) when state is clean.
4. Emits a single actionable alert payload — naming the offending entity by name and ID — when drift is detected.

Empty stdout in `--no-agent` mode = no message delivered. So "silent" is literally just `exit 0` after the check passes.

## Anti-pattern: bare "drift detected" alerts

A bare alert (`⚠️ default profile has unexpected crons`) sends the user on a hunt: "okay, *which* crons? what happened?" Always include enough detail to make the fix one targeted command:

```
⚠️ default-cron-drift detected

Cron(s) currently registered on default:
  • example-daily-job (id: <job-id>, schedule: 0 18 * * *)

Fix: assistant cron create ... (re-register on the right profile),
     then hermes cron remove <job-id>.
Runbook: <runbook-path>/adding-a-production-cron.md
```

Three things make this actionable:

- **Named offender(s)** with stable IDs the user can paste into the fix command.
- **Concrete fix command** — the user shouldn't have to remember the runbook syntax.
- **Pointer to the runbook** that explains the policy, in case the user wants to understand why the alert fired.

## Worked example: `default-cron-drift-detector`

Context: After consolidating production crons onto an `assistant` profile, the `default` profile should have zero crons. The detector sits on assistant (the production profile) so it survives any default-profile reset.

```bash
#!/bin/bash
# default-cron-drift-detector
#
# Steady-state guard. The default profile should run zero crons —
# every production-scheduled business job belongs on assistant.
# This watcher fires only when something landed on default by mistake.
#
# Designed for cronjob no_agent=True: empty stdout = silent (no message).

set -euo pipefail

default_output=$(hermes cron list 2>/dev/null || true)

if echo "$default_output" | grep -q 'No scheduled jobs'; then
  exit 0  # silent — clean state
fi

# Drift detected. Extract cron names + IDs from the output.
# `hermes cron list` formats each job as:
#   <id> [active|paused]
#     Name:      <name>
#     Schedule:  <schedule>
#     ...
offenders=$(echo "$default_output" | awk '
  /^  [a-f0-9]{12} \[/ { id=$1; name=""; sched=""; next }
  /^    Name:/ {
    name=$2; for (i=3; i<=NF; i++) name=name" "$i
  }
  /^    Schedule:/ {
    sched=$2; for (i=3; i<=NF; i++) sched=sched" "$i
    print "  • " name " (id: " id ", schedule: " sched ")"
  }
')

if [ -z "$offenders" ]; then
  # Output was non-empty but didn't match expected format — surface raw
  offenders="$default_output"
fi

cat <<EOF
⚠️ default-cron-drift detected

The default profile should run zero crons — production crons belong on assistant.

Cron(s) currently registered on default:
$offenders

Fix: assistant cron create ... (re-register on the right profile), then hermes cron remove <id>.
Runbook: <wiki>/workflows/adding-a-production-cron.md
EOF
```

Registered:

```bash
assistant cron create '0 9 * * 1' \
  --name default-cron-drift-detector \
  --deliver telegram \
  --script default_cron_drift_detector.sh \
  --no-agent
```

## Pitfall: parser ordering matches output ordering

When extracting fields from a CLI's verbose output, the printer must run in whichever block guarantees both fields have been seen. `hermes cron list` prints `Name:` before `Schedule:`, so:

- Wrong: `print` inside the `Name:` branch — `sched` is empty.
- Right: `print` inside the `Schedule:` branch — `name` was captured a line earlier.

Reset both fields when a new job header (`<id> [<state>]`) is matched, so values from a previous job don't bleed into the next when fields are missing.

Always smoke-test the alert path with simulated drift, not just the silent path. The simulation catches off-by-one parser bugs the clean-state run cannot:

```bash
# Pipe a fake "hermes cron list" through the awk block and verify the
# rendered offender line has both name and schedule populated.
cat <<'FAKE' | awk '...' 
  abc123def456 [active]
    Name:      stray-test-cron
    Schedule:  0 9 * * *
    ...
FAKE
```

## Generalizing

Drift-detector candidates anywhere you have a "should remain at X" invariant:

| Invariant | Detector |
|---|---|
| Default profile runs zero crons | Parse `hermes cron list`; alert if non-empty |
| the builder profile's `.env` has no production tokens | Grep for `SLACK_BOT_TOKEN=xoxb-…` and similar; alert if found |
| Nothing in `99-ARCHIVE/` was modified in the last 24h | `find 99-ARCHIVE/ -mtime -1` should be empty |
| All `~/.hermes/sessions/*.json` have `chmod 600` | `ls -la | grep -v '^-rw-------'` should be empty |
| The business-system API key still has `aud=api` | Decode JWT, check claim; alert if not `api` |

Schedule weekly or daily depending on cost — a daily detector that's silent 364 days a year is cheap and catches drift fast.

## Pattern: invert before deleting a "completion" watcher

When a migration completes and you have a watcher whose job was "tell me when this is done", the wrong move is to delete it. The right move is to invert it into a steady-state drift detector that uses the same machinery to guard against regression.

Concrete inversion (in practice):

- **Old:** `assistant-migration-watcher` — silent until `default cron list` is empty AND `assistant cron list` has ≥ N crons. Pings on completion.
- **New:** `default-cron-drift-detector` — silent while `default cron list` is empty. Pings if anything lands on default.

The script changed by ~10 lines. The cron registration was a 1:1 swap. The pattern doubled in value: it both confirmed the migration completed (by going silent) and immediately took on its long-term role (catching regression).
