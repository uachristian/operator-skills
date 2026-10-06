# When to prefer a DB queue over direct webhook agent runs

Use this pattern when a UI/service wants an agent action but you want to avoid giving the UI/service broad credentials or depending on a public inbound tunnel.

## Prefer queue-worker when

- The caller is a browser/static-hosted app and should not get access to backend systems such as the business system of record.
- The agent logic should remain centralized in Hermes skills so future skill improvements apply automatically.
- A stable public tunnel/webhook URL is not already verified.
- Requests can tolerate short async delay.
- You want durable retry/audit status: queued, processing, completed, failed.

## Flow

1. UI writes an authenticated request row to a database queue.
2. Hermes cron/worker polls and claims queued rows.
3. Worker loads the relevant skill and uses Hermes-only credentials/tools.
4. Worker writes result rows back to the database.
5. UI refreshes/polls database for result.
