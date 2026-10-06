# Open-items recall and backlog triage

Use when the owner asks "what's still open / to do from the last days/weeks" or asks you to work through a list of leftover items and decide Kanban approvals.

## 1. Gather candidates (read-only, one batch)

1. Check for a same-day session with the same ask first; reuse its result instead of redoing the sweep.
2. Sessions: if `session_search` browse times out, read `~/.hermes/state.db` read-only (`sqlite3 -readonly`): list titled sessions from the window (`sessions.started_at`, `source`, `title`, `message_count`), skip cron-only noise, then pull the LAST long assistant message per session. The last message usually states the unresolved checkpoint ("waiting on…", "go ahead with…?").
3. Kanban: open `~/.hermes/kanban.db` read-only; select tasks not done/cancelled/archived with body, `block_kind`, and the latest `task_comments` row. The last comment carries the real hold reason.
4. Classify each item: owner step pending / unresolved defect / approved-but-stalled / stale backlog.

## 2. Verify live before reporting or acting

Session text is evidence of past state only. For each item the owner asks you to work:

- **Deploy/"go live" requests**: first prove which host actually serves the public domain (`curl -sI https://<domain>` plus the page `generator`/framework markers), because a hosting project's "Production" environment may have no custom domain and the real site may be a different platform. Then compare the preview with what the domain really serves (`vercel ls --environment production`, age and commit). If production is far behind the branch, "go live" would ship all unreleased work, not just the patch. Surface that choice (full release vs patch-only vs "the patch never touched the live site") instead of promoting. For a review-only refresh, moving the stable noindex review alias (`vercel alias set <preview-url> <stable-alias>`) is reversible and does not touch the domain; record the previous alias target for rollback.
- **Provider/model failures**: read `logs/errors.log` / `agent.log` for the exact upstream error text before theorizing. It often names the concrete fix, such as a required client version. Then re-run a tiny no-fallback smoke and confirm `provider=`/`model=` on the logged API call.
- **One-shot verification checks** that report "not confirmed": cross-check the scheduler log line (`delivered to <target> … message_id=`) before trusting the check. Checks keyed on fields like `last_delivered_at` can read stale values and give false negatives.
- **"Section unavailable" in recurring briefs**: read the current job prompt and skill mode before calling it a defect. A later intentional scope change (e.g., a section deliberately removed) supersedes old failure incidents. Scan the last several outputs to see whether the failure still recurs.
- **Record-scoped cards**: direct-read each record. If it no longer comes back, or already left the flagged lane, the card is obsolete.

## 3. Kanban disposition

- Always pass `--board default` (the current board may be a different one).
- Close obsolete cards yourself when live readback proves them moot and no external write is involved: `hermes kanban --board default comment <id> "<reason + evidence>"`, then `complete <id> --summary "<evidence>"`. Completion without `--summary`/`--result` is refused, and goal cards are judged on that evidence.
- Never execute the production action a card proposes during triage; approval cards need exact owner approval.
- Parent-owned goal cards whose workers ended long ago: recommend close-and-reopen-narrowly rather than resuming.
- Group months-old observer design suggestions into one "archive, restart what still matters" decision instead of listing each.
- When the owner says "do it based on your suggestions", execute exactly the recommended picks: comment the reason on each card, then `hermes kanban --board default archive <ids...>` for stale backlog. A `scheduled` card refuses `complete` (reported as terminal/unknown); `unblock` it first, then `complete --summary`. Archive only the reminder card for a live record the owner still owns (e.g. an order with no due date); never edit the record itself.

## 3a. Installing an approved-but-stale staged candidate

Approved fixes parked for days usually hit preimage drift (the installer's expected hash no longer matches the live file because unrelated commits landed).

1. Hash every target against the installer's preimage list; do not force the installer past a drift guard.
2. Rebase in scratch: copy the current live file, `patch --dry-run` the candidate hunk for that file, then apply; copy untouched staged files as-is. `py_compile` everything.
3. Run the candidate's own tests against the rebased tree, then run the repo's existing suite on a scratch copy with and without the rebased files and `diff` the sorted pass/fail lines. Pre-existing failures are acceptable only if identical before/after.
4. Install with a timestamped backup dir plus `preimage.sha256`; use temp-file + `mv`; note new files separately so rollback deletes them.
5. Run the live read-only acceptance the approval named (e.g. combined-filter parity against manual filtering) using the same interpreter/env the runtime uses (profile venv + profile `.env`), calling the library layer directly if the MCP wrapper needs a request context.
6. If live acceptance fails, roll back immediately, verify hashes equal the preimages, comment the exact failure on the card, and leave it blocked. Synthetic-test success never substitutes for live acceptance.

## 4. Report shape

Sections: waiting on owner, fixed/verified now, closed (with reason), needs decision. Put a recommended pick on every decision and give a one-line reply format the owner can answer with.
