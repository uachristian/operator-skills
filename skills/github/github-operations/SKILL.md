---
name: github-operations
description: "Use when working with GitHub end to end: auth, issues, PRs, review, CI triage, releases. Includes the public-push privacy gate."
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [github, gh, git, pull-requests, issues, ci, code-review]
---

# GitHub Operations Umbrella

## Overview

This is the class-level GitHub skill. It covers the full lifecycle from authentication and repository setup through issues, branches, PRs, reviews, CI, releases, and repository inspection. Prefer `gh` when available; fall back to `git` plus the GitHub REST/GraphQL API when `gh` is missing or not authenticated.

## When to Use

- Set up or troubleshoot GitHub authentication.
- Clone, create, fork, inspect, or configure repositories.
- Create, triage, label, assign, or close issues.
- Create branches, commits, pull requests, release notes, or tags.
- Review local diffs or GitHub PRs.
- Monitor or fix CI failures.
- Estimate codebase size/language mix before planning work.

## Baseline Discovery

Always discover before acting:

```bash
git status --short --branch
git remote -v
gh auth status || true
gh repo view --json nameWithOwner,defaultBranchRef,visibility 2>/dev/null || true
```

If `gh` is unavailable, use `git config --get remote.origin.url` and authenticated HTTPS/SSH directly.

## Authentication

Decision flow:

1. Check `gh auth status`.
2. If `gh` works, use it for API and PR/issue operations.
3. If only Git works, perform clone/fetch/push through existing SSH/HTTPS credentials.
4. If neither works, stop and ask the user to authenticate; do not request or type tokens yourself.

Useful fallback:

```bash
GITHUB_TOKEN=... curl -H "Authorization: Bearer $GITHUB_TOKEN" https://api.github.com/user
```

Never print tokens or persist them in repository files.

### Profile-local authentication for isolated specialists

When a specialist profile needs its own GitHub identity, isolate both `HOME` and `GH_CONFIG_DIR` under that profile. On macOS, use `gh auth login --web --insecure-storage` only with an owner-only profile directory (`0700`) and `hosts.yml` (`0600`) so the token does not silently become a shared keychain credential. The user must complete browser/device approval; never type their password, 2FA, or account confirmation.

If the reviewed commit contains `.github/workflows/*`, verify `gh auth status` includes `workflow` before push. The normal minimum OAuth set may include `repo` but omit `workflow`; add only the missing scope with `gh auth refresh --scopes workflow --insecure-storage`, then re-check scopes and file modes.


## Repository Management

Common operations:

```bash
gh repo clone OWNER/REPO
gh repo create OWNER/REPO --private --source=. --remote=origin --push
gh repo fork OWNER/REPO --clone
```

The combined `--source --push` form is convenient only when repository visibility and destination are already independently trusted. For a **first private source publication**, create an empty private repository without pushing, prove `visibility=PRIVATE`, attach the remote, push the frozen exact tip, then prove privacy and local/remote SHA equality again. Require CI completion for that exact head SHA, not merely a queued run.

For settings, branch protection, secrets, releases, and collaborators, prefer `gh api` with explicit endpoint payloads. Read current settings before patching.

### Private Hermes plugin/product source mirrors

When the owner asks to create a private repo to “encompass” a Hermes plugin plus its support code, use the same curated-mirror discipline as profile mirrors, but shape the repo around the product boundary:

```text
<repo>/
  README.md
  .env.example             # key names only
  .gitignore
  <plugin_name>/           # plugin source: plugin.yaml, tools, schemas, adapters, common, tests
    scripts/               # deterministic runtime scripts mirrored from profile scripts
  <owner>-bridge/     # only if the product depends on an owner-only bridge helper
  docs/                    # skill references and canonical vault docs copied for context
  scripts/
    install_to_profiles.py # local sync helper; no credential creation
    secret_scan.py         # reproducible scan
```

Do not push raw profile directories, `.env`, auth, runtime `state/`, logs, sessions, memories, backups, cron output, browser profiles, cookies, or audit JSONL. Sanitization must also remove live record IDs, media references, private-network addresses, personal absolute paths, and machine-specific active config when those are runtime evidence rather than source. Keep tests self-contained: copy a reviewed non-secret map into a synthetic fixture instead of reading live `state/`. Before first push: compile, run tests from the mirror with bytecode disabled, run repo-local `secret_scan.py`, generate and verify a source SHA-256 manifest, run `git diff --cached --check`, and verify forbidden tracked paths. Create the private remote **without pushing**, prove `visibility=PRIVATE`, push only after that gate, then prove privacy again after push.

For closeout across multiple private mirrors, commit the canonical product/source repo first when it is clean and fully verified. If an internal aggregate mirror has broader pre-existing dirty changes outside the task scope, do **not** bundle unrelated work just to make every mirror green. Either stage only the exact task-scoped files if safe, or explicitly leave that mirror uncommitted and report why. A pushed canonical private source repo plus verified live-runtime sync is better than one oversized mixed commit that hides unrelated changes.

### Private Hermes profile source mirrors

When the owner asks to put a Hermes specialist profile or “all of this” profile work into GitHub, keep the live profile improvement as the primary task and repo work as safety/rollback/source coverage. Do **not** let tracker or mirror perfection block the profile fix. Do **not** initialize Git in the raw profile directory. Build a curated private source mirror that excludes secrets/runtime state/logs/sessions/memories/raw ref maps/backups/caches, run token-pattern and tracked-path checks, then push the sanitized mirror. For broad repo hygiene, prefer a separate daily/background system-wide repo check/push workflow rather than interrupting the active profile-improvement batch.


### Private profile/source mirrors

When creating a private repo from a live Hermes profile or automation workspace, do **not** push the raw runtime directory. Build a curated source mirror that allow-lists source files and excludes secrets, auth, state, logs, sessions, memories, backups, raw ref maps, cron output, caches, pycache, and lock/PID files.

### Skill/profile mirror closeout must compare source vs destination

For curated mirrors such as `<private-skills-mirror>`, do not trust `git status` alone. A clean repo only proves the mirror has no local changes; it does **not** prove every new local skill reference was copied into the mirror. Before committing/closing out, compare each intended source artifact to its destination.

If there are multiple local mirrors of the same private skills/profile repo, align secondary mirrors only after the canonical mirror has been committed and pushed. Save a backup first (`git diff > <backup-dir>/secondary-working-tree.diff` plus copies of untracked files), then `git fetch origin && git reset --hard origin/main && git clean -fd -- <expected-untracked-paths>`, and finally compare key files byte-for-byte against the canonical mirror. Do not hard-reset a dirty secondary mirror without preserving its diff/untracked files.

Comparison pattern:

```bash
python3 - <<'PY'
from pathlib import Path
pairs = [
    (Path('~/.hermes/skills/<skill>/SKILL.md').expanduser(), Path('<repos-dir>/<private-skills-mirror>/<skill>/SKILL.md').expanduser()),
    (Path('~/.hermes/skills/<skill>/references/<file>.md').expanduser(), Path('<repos-dir>/<private-skills-mirror>/<skill>/references/<file>.md').expanduser()),
]
for src, dst in pairs:
    print(src, '->', dst, 'src_exists=', src.exists(), 'dst_exists=', dst.exists(), 'identical=', src.exists() and dst.exists() and src.read_bytes() == dst.read_bytes())
PY
```

If `dst_exists=False` or `identical=False`, copy the exact allowed artifact into the mirror, run `git diff --check`, do a narrow secret-pattern scan on the touched files, then commit and push.

## Issues

Use issues for durable task tracking. Include:

- concise title,
- context/background,
- steps to reproduce for bugs,
- expected vs actual behavior,
- acceptance criteria,
- labels/assignees only after checking what exists.

Templates belong under `templates/` support files if a project has recurring formats.

## PR Workflow

Reference: `references/local-branch-rebase-and-fork-pr.md` — use when cleaning up pre-existing local repo changes: commit coherent local work, create a backup branch before rebase, preserve both valid conflict behaviors, push to fork if upstream push is denied, open a draft PR, and restore canonical remotes.
Reference: `references/public-pr-exposure-remediation.md` — use when a local/private Hermes/operator branch was accidentally pushed to a public fork or opened as a public PR; covers scanning, branch overwrite/delete, PR-body redaction, frozen upstream PR refs, and GitHub Support/maintainer escalation.
Reference: `references/hermes-local-commit-public-push-gate.md` — use when closing out local Hermes/operator repair commits: verify exact remote visibility before push, preserve a local diff backup, and treat `origin`/`fork` as public unless `gh repo view OWNER/REPO` proves `visibility: PRIVATE`.

1. Create a focused branch from the current base.
2. Make minimal commits with clear messages.
3. Run tests/lint relevant to the change.
4. For public PRs from local Hermes/operator branches, run a public-safety scan before pushing or opening the PR: secrets/tokens, private IPs/Tailscale `100.x`, business/customer/vendor names, personal names/emails, `.env`/auth/session/log/state paths, and org-specific plugin constants. If any hit is not intentionally public, keep the work private or scrub/rewrite commits first.
5. For any Hermes/operator branch going to a public repo, stop after the scan and get explicit user approval before the first public push/PR. Opening a public PR without this gate is a real, unrecoverable exposure risk (public PR refs cannot be deleted); treat public exposure prevention as a required approval checkpoint, not a best-effort cleanup after the fact.
6. Push branch and open PR with summary + test plan only after the public-safety scan is clean and approval is explicit.
7. Monitor CI and address failures.
8. Merge only when policy and user intent allow.

Commands:

```bash
git switch -c feature/name
git add <paths> && git commit -m "type: summary"
git push -u origin HEAD
gh pr create --title "..." --body-file /tmp/pr-body.md
gh pr checks --watch
```

## Code Review

Review the actual diff, not just file names:

```bash
git diff --stat
git diff --check
git diff --cached
gh pr diff <number>
```

Checklist:

- correctness and edge cases,
- security and secrets,
- tests for changed behavior,
- migration/backward compatibility,
- docs/config updates,
- CI status.

For GitHub PR reviews, use `gh pr review` or REST review comments only after collecting exact file/line context.

## Codebase Inspection

Use codebase inspection before estimates, rewrites, or unfamiliar repos. `pygount` gives language/LOC ratios; exclude generated/vendor/build directories.

```bash
pygount --format=summary --folders-to-skip node_modules,dist,build,.git .
```

If `pygount` is unavailable, use language-aware alternatives already present in the repo, but do not use raw file counts as LOC estimates.

## Common Pitfalls

- Treating repeated `CI / verify Failed` emails as one shared GitHub defect based only on the latest failed run. The email subject usually reuses the workflow/job names, even when each run failed for a different reason. For a recurring pattern, audit at least 30 days of push-triggered runs across the relevant owner, fetch each failed run's jobs, group by failed step and duration, and inspect representative failed logs before concluding root cause. Separate action-resolution/setup failures from real tests, lint, manifests, container dependencies, and host-specific contract checks. Also verify that hosted Linux CI does not execute tests that assume local macOS paths such as macOS home directories, `/private/tmp`, or a production-only interpreter; isolate those as local/macOS gates or make them platform-aware. Require the closest local equivalent of CI to pass before each push so iterative repair commits do not create one failure notification per commit.
- Validating Git LFS pointers by reading the normal working-tree file. A standard smudged checkout contains the real binary there; inspect the staged/index blob instead (for example `git show :path/to/file`) when checking pointer syntax, and use `git lfs fsck` for object integrity.
- Assuming every installed Git LFS version supports NUL output for `git lfs ls-files`. Some versions reject `-z`; for portable repository-policy scripts, use `git lfs ls-files --name-only` and split newline-delimited paths unless filenames with embedded newlines are an explicit supported requirement.
- Assuming `gh` auth implies Git push auth; check both when pushes fail.
- Creating labels/assignees without listing existing project conventions.
- Opening a PR before running the test plan the body claims was run.
- Reviewing a PR from the GitHub UI summary instead of the raw diff.
- Force-pushing or changing branch protection without explicit user approval.
- Treating `visibility=PRIVATE` as sufficient push approval when the local branch already has an unreviewed ahead stack. A normal push publishes every reachable commit in `origin/<branch>..HEAD`, not only the newest task-scoped commit. Inspect the entire ahead range first; if it is outside scope, make the narrow local commit for durability but leave it unpushed and report the boundary.
- Treating a closed PR as fully removed after deleting the fork branch. GitHub can retain frozen upstream `refs/pull/<PR>/head`; if sensitive data remains there, use the private vulnerability reporting flow or a maintainer/GitHub Support purge request. See `references/public-pr-exposure-remediation.md`.
- Posting sensitive cleanup requests as public issues/comments. For private IPs, personal/business author identity, or operator details, route privately and avoid repeating the values publicly.

## Verification Checklist

- [ ] Repository and branch confirmed.
- [ ] Auth mode known (`gh`, SSH Git, HTTPS token, or unavailable).
- [ ] Destructive/admin changes preceded by read-only inspection.
- [ ] PR/issue/release URLs or IDs captured after creation.
- [ ] For first private publication, visibility was proven private before and after push.
- [ ] Local and remote exact SHAs match; Git LFS upload/object integrity is verified when used.
- [ ] CI/test result reported from the exact pushed head, not a queued or stale run.
