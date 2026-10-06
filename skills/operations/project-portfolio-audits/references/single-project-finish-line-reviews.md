# Single-project status and finish-line reviews

Use when the owner asks for the current status of one named project plus what it takes to reach production. This is a decision brief for the owner, not a portfolio sweep.

## Sequence

1. **Vault first, sorted by recency.** Search the vault for the project noun, then list the concept/workflow folder sorted by mtime and note the date of the newest project note. The gap between that date and today is itself a finding ("frozen since <date>, N days"). Read the newest 3–5 notes fully; older notes are history.
2. **Session history, narrow query.** Use one or two exact project tokens with `sort=newest`, `limit<=8`, default adaptive detail. Do **not** use broad `A OR B OR C` FTS queries on a long-running project: one such query returned 5.8 MB of spillover and had to be re-parsed from disk. If a query spills, parse the saved file with `execute_code` for `when | title | session_id` rather than re-querying.
3. **Local artifacts.** For each release-candidate repo/directory: `git log -1`, `git status --porcelain | wc -l`, and whether a release directory under `~/.hermes/releases/` exists. Uncommitted edits in a "release candidate" are a loose end to surface by count, not content.
4. **Live automation metadata only.** `cronjob list` filtered to the project's jobs; `cron/executions.db` status rows; `cron/output/<job_id>/` latest files. `silent (empty output)` + `completed` is healthy for a watchdog. Do not run the watched script yourself from the interactive terminal—its permissions differ (see below).
5. **External dependency state.** If the project is waiting on a vendor/provider ticket, read the ticket thread's *metadata* (dates, senders, mailbox) and count human replies since the automated acknowledgment. Elapsed days without a human reply is the key number.
6. **Capture a checkpoint to the vault** before answering, in the same turn, linked to the project hub. It closes any previously recorded ambiguity (e.g. "sent but transport unclear" → "confirmed in Sent Mail on <date>").

## Output shape

Lead with a one-sentence verdict: moving / frozen since <date> / blocked on <thing>. Then:

- **What is live in production** (exact release ids, what data is actually in it—often "registry empty").
- **The single blocker** in plain language: what fails, why it cannot be fixed from inside the current boundary, what has already been submitted upstream and when.
- **Built but shelved** as a compact table: component, review state, local artifact + short SHA, dirty-edit count.
- **Decision fork** when the blocker is an external party that has gone quiet. Offer 2–3 real options with honest cost (wait + nudge / route around it, e.g. self-host the exact reviewed runtime / descope). Recommend one. Do not present "keep waiting" as the plan without saying how long it has already been.
- **Finish line after the blocker clears**, as a numbered sequence with the acceptance step first (synthetic smoke before real data).
- Housekeeping note for stale candidate directories/tarballs, gated on the owner's chosen path.

## Pitfalls

- A vault trail that stops on a date is evidence the project stopped there; say so with the day count instead of implying ongoing progress.
- An interactive Hermes terminal usually lacks Full Disk Access even when the cron/launchd context has it. A denied read of `~/Library/Mail`, `~/Library/Messages`, etc. from your shell says nothing about the scheduled job. Probe via the app's AppleScript surface (Mail.app `messages of mb whose subject contains ...`) or read the scheduler's execution records instead.
- Gmail-backed accounts show one message under `INBOX`, `Important`, and `All Mail`; deduplicate by date+sender+subject before counting replies.
- `ls -d ~/*proj*` can return hundreds of stale candidate archives; summarize by pattern and count, never enumerate them in the answer.
- Session-search results include the *current* session; skip it.
- Do not restate the last vault note as "status"; verify each claim it makes (ambiguous send, watcher health) against today's live evidence and record which ones changed.
