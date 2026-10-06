# Fleet Change Guard

Use this pattern when the owner asks for restart-loop protection or fleet change supervision.

## Example implementation (macOS launchd)

- LaunchAgent: `~/Library/LaunchAgents/com.hermes.fleet-change-guard.plist`
- Label: `com.hermes.fleet-change-guard`
- Cadence: every 60 seconds, independent of Hermes cron
- State: `~/.hermes/state/fleet-change-guard-state.json`
- Log: `~/.hermes/logs/fleet-change-guard.log`

## Safety contract

The guard must never restart, kickstart, unload, or kill Hermes gateway labels (`ai.hermes.gateway*`). It may only quarantine temporary helper labels matching:

```text
^(?:com|ai)\.hermes\.gateway-fleet-restart-\d{8}-\d{6}$
```

That quarantine is allowed only when restart-loop evidence exists in recent gateway logs. Unknown-source loops are report-only.

Known planned-maintenance behavior: if owner-approved Hermes maintenance has been logged recently in `~/.hermes/state/autonomous-improvements.jsonl` with gateway restart wording, the guard may suppress the resulting fleet SIGTERM wave instead of paging the owner repeatedly as the 10-minute lookback window slides. This suppression must not hide helper LaunchAgents/processes and must not perform any gateway action.

Unknown critical fleet-wave alert signatures should be coarsened (not profile-list-specific) so one real incident does not page repeatedly while individual profiles age out of the window.

## Verification

```bash
plutil -lint ~/Library/LaunchAgents/com.hermes.fleet-change-guard.plist
launchctl list | grep com.hermes.fleet-change-guard
```

## Rollback

```bash
launchctl bootout gui/$(id -u)/com.hermes.fleet-change-guard
rm -f ~/Library/LaunchAgents/com.hermes.fleet-change-guard.plist
```

Restore pre-install files, if needed, from the backup you took before installing.
