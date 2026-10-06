# Read-only PR watch cron

- Monitor script in `~/.hermes/scripts/` printing deterministic lines per PR from `gh pr view N -R OWNER/REPO --json number,title,state,mergeable,reviewDecision,labels,comments,reviews,statusCheckRollup --jq ...` (sorted labels, counts of pass/fail/pending checks, failed check names, review/comment author + truncated body). No timestamps, so unchanged ticks skip the agent.
- Create with `cronjob_manage action=create`, `schedule='0 9,17 * * *'`, `monitor=<script>`, `continuity=true`, deliver to origin.
- Prompt: strictly read-only (no push/comment/label/review); report only changes and whether the user must act; baseline run sends a one-line summary; when all PRs are MERGED/CLOSED report outcomes and remove the job by name.
- Fresh external PRs often show zero checks: maintainer approval of workflow runs is pending, not a CI failure. Triage bots add priority/area labels and possibly `needs-repro` within minutes.
