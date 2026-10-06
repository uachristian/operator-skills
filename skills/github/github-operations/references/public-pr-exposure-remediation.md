# Public PR exposure remediation

Use when a local/private Hermes/operator branch was accidentally pushed to a public fork or opened as a public PR.

## Goals

1. Determine whether the public material contains secrets or sensitive-but-not-secret details.
2. Sanitize what the authenticated user controls immediately.
3. Identify what remains cached in upstream GitHub PR refs and route a private purge request.
4. Add prevention gates so public pushes/PRs require approval and scan evidence first.

## Read-only triage

Collect evidence without printing secrets:

```bash
gh pr view <PR> --repo OWNER/REPO --json number,title,url,state,isDraft,mergedAt,headRefName,baseRefName,author,headRepository,commits,body > pr.json
gh pr diff <PR> --repo OWNER/REPO --patch > pr.diff
gh api repos/OWNER/REPO/issues/<PR>/comments > issue-comments.json
gh api repos/OWNER/REPO/pulls/<PR>/comments > review-comments.json
gh api repos/OWNER/REPO/pulls/<PR>/reviews > reviews-api.json
gh api repos/OWNER/REPO/issues/<PR>/events > events.json
```

Scan the PR body/diff/comments/reviews for:

- concrete credentials/tokens/private keys;
- private/Tailscale IPs such as `100.x.x.x`;
- personal names/emails/phone numbers;
- local paths such as `/Users/<name>`;
- business/customer/vendor details that are not intended to be public;
- `.env`, auth/session/log/state paths;
- org-specific constants embedded in shared public code.

Report concrete secret values only as `[REDACTED]`.

## If the exposed branch is in the user's fork

Before destructive remote changes, create local-only backups:

```bash
git branch backup/public-pr-<n>-head-pre-sanitize-$(date +%Y%m%d-%H%M%S) fork/<branch>
```

Then reduce active exposure:

```bash
# overwrite branch with a safe upstream commit first, then delete it
git push --force fork origin/main:refs/heads/<branch>
git push fork --delete <branch>
```

If other public fork branches carried the same personal author metadata or private details, delete/sanitize those too. Verify remaining fork-only commits after cleanup with a diff-based scan, not a full-tree scan: full-tree scans include upstream test fixtures and produce false positives.

## Editable PR material

Edit the PR body to a minimal sanitized note. Do not post a public issue/comment repeating the sensitive values.

```bash
gh pr edit <PR> --repo OWNER/REPO --body-file sanitized-body.md
```

Public comments by other users usually cannot be edited by the reporter; route privately if they quote sensitive material.

## Frozen upstream PR refs

Closed GitHub PRs can retain a frozen upstream ref such as:

```text
refs/pull/<PR>/head
```

Even after the fork branch is overwritten/deleted, `gh pr diff` may still show the original cached diff. A user without upstream write/admin permission cannot delete that ref:

```bash
git push origin :refs/pull/<PR>/head   # usually 403 unless maintainer/admin
```

If the ref remains, a maintainer or GitHub Support must purge/remove the cached PR ref/history.

## Private vulnerability reporting path

If the public repo has private vulnerability reporting enabled, use it instead of a public issue:

```bash
gh api repos/OWNER/REPO/private-vulnerability-reporting --jq '.'
```

If `{"enabled":true}`, submit a private report:

```bash
gh api -X POST repos/OWNER/REPO/security-advisories/reports \
  -H 'X-GitHub-Api-Version: 2022-11-28' \
  --input payload.json
```

Payload shape that worked reliably:

```json
{
  "summary": "Request to purge cached closed PR ref containing private operator details",
  "description": "Private request regarding closed draft PR ... The fork branch and editable PR body have already been sanitized/deleted from my side, but GitHub still exposes the frozen upstream pull ref/diff at refs/pull/<PR>/head. That cached ref contains private/operator-specific details. No credentials/tokens/private keys were found in my scan. Could a repo maintainer or GitHub Support purge/remove the cached PR ref/history? Please keep this report private and do not repeat the exposed values in public issues/comments.",
  "severity": "low",
  "cwe_ids": ["CWE-200"],
  "vulnerabilities": [
    {
      "package": {"ecosystem": "other", "name": "<repo>"},
      "vulnerable_version_range": "closed draft PR ref/cache only",
      "patched_versions": "fork branch sanitized/deleted; upstream cached PR ref still needs purge"
    }
  ],
  "start_private_fork": false
}
```

Pitfall: posting only `summary`, `description`, and `severity` may return a GitHub `500`/empty JSON in some cases. Including `cwe_ids` and a minimal `vulnerabilities` entry avoided that.

A successful response returns `201 Created`, a `GHSA-...` id, and a private advisory URL. Save the raw response locally, then monitor the advisory state.

## Monitoring

A no-agent cron is appropriate for private-report status checks. The script should be silent unless state/metadata changes or the check fails. Poll:

```bash
gh api repos/OWNER/REPO/security-advisories/GHSA-... --jq '{ghsa_id,state,html_url,summary,updated_at,closed_at,withdrawn_at}'
```

## Prevention gate for future public PRs

For Hermes/operator branches, do not push public branches or create public PRs until:

1. a public-safety scan is clean;
2. the user has explicitly approved the public push/PR;
3. commit author identity is public-safe, preferably GitHub noreply;
4. the PR body has no internal workflow details beyond what the user approved.

If the user expresses frustration that the public PR happened at all, strengthen the skill gate: the approval checkpoint is mandatory, not optional cleanup afterward.
