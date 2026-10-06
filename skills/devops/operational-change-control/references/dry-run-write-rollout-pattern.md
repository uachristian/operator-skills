# Dry-Run Rollout Pattern for New Write Capabilities

When introducing automated writes to a third-party API (shop-management systems, CRMs, billing systems, ticketing, any system where wrong writes have user-visible blast radius), DO NOT go straight from "no automation" to "live writes." Use a three-phase rollout that grows trust before exposing the write surface.

## The three phases

### Phase 1 — DRY-RUN (1 week minimum)

**Build the decision logic with zero write surface.**

- Implement the full pipeline: read inputs, resolve entities, match, decide what to write
- Log every proposed write to an audit JSONL file (`<system>_writes_dryrun.jsonl` per target system)
- DM the supervising human a periodic summary so they can audit accuracy
- **DO NOT add the actual write tool/endpoint to any MCP allowlist or scope yet** — this is the key. The capability literally cannot fire even if the script has a bug, because the write API isn't reachable

Exit criterion: one full week of proposed writes where the human reviewer sees no false positives or wrong matches.

### Phase 2 — SUPERVISED LIVE (2 weeks)

Once dry-run logs look clean:

1. Add the write tool to the MCP server / API client
2. Add it to the per-profile allowlist (e.g. `~/.hermes/mcp_servers/<server>/tool_allowlist.json`)
3. Flip the script from "log proposed" to "actually write"
4. Keep DM-on-every-write enabled — the human sees a notification for each mutation
5. Maintain the audit log (now records actual writes, not proposed ones)

Exit criterion: 2 weeks of writes where every DM was either correct or rolled back without incident.

### Phase 3 — SILENT (steady state)

- Drop per-write DMs (otherwise the human develops alert fatigue)
- Keep the audit log
- Only DM on error: API failure, match-score below threshold, conflict, etc.
- Optionally surface a weekly summary so the human still has periodic visibility

## Why this works

- **Phase 1 has zero blast radius.** Bug in your matching logic? It writes a wrong proposal to a JSON file. Nobody cares.
- **Phase 2 is recoverable.** Wrong write happens? You see the DM the same minute, can reverse it, and the audit log shows exactly what changed.
- **Phase 3 trusts only what was empirically validated.** You're not betting on "the model is good enough" — you're betting on "this exact pipeline produced clean writes for 3+ weeks of real traffic."

## Implementation checklist

When designing a new write capability:

- [ ] What's the audit log path? (`state/<system>_writes_dryrun.jsonl`)
- [ ] What fields belong in each audit entry? (timestamp, source event, resolved entity, current state, proposed state, match score / confidence, decision)
- [ ] What's the supervisor DM cadence? (per-write in dry-run, per-batch summary, daily roundup?)
- [ ] What's the dry-run exit criterion? Concrete and machine-checkable, not "looks good"
- [ ] What's the supervised-period exit criterion?
- [ ] Where does the actual write tool live? (MCP server file path)
- [ ] Where's the allowlist that gates it? (`tool_allowlist.json` path for the relevant profile)
- [ ] Per-record granularity vs all-or-nothing? (per-part match vs whole-PO write is a common axis)
- [ ] What's the rollback procedure if a wrong write does land?

## Don't skip phases

Common temptations and why they fail:

| Shortcut | Failure mode |
|---|---|
| "I'll just turn writes on and watch carefully" | You can't watch carefully 24/7. The watcher cron fires at 3am. |
| "We'll trust the LLM to know when not to write" | LLM confidence is uncalibrated. Match scores aren't accuracy. |
| "Dry-run for one day is enough" | One day misses weekly patterns (Mondays, after-hours emails, edge cases). |
| "Skip the supervisor DM, just check the audit log" | Nobody actually reads audit logs. Push > pull for trust-building. |
| "We can rollback if needed" | Rollback works once or twice. Erodes trust on the third. |
