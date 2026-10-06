---
name: upstream-open-source-contributions
description: "Use when turning local commits into upstream public PRs. Privacy gate, clean rebase, real before/after tests."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [github, upstream, pull-requests, privacy, docker, testing]
    related_skills: [github-operations, build-execution-standard]
---

# Upstream Open-Source Contributions

Porting local fixes (carry commits on an operator checkout) into public PRs against an upstream repo such as NousResearch/hermes-agent: isolated worktree, Docker before/after tests, privacy gate, verified PR bodies, read-only watch. Opening a PR is irreversible (upstream keeps `refs/pull/N/head`); pushing a branch to the user's fork is recoverable. Explain that difference if asked, and treat the PR step as the privacy point of no return.

## When to Use

- Local/carry commits should go upstream as public PRs.
- Building, testing, privacy-gating, publishing or watching those PRs.

## Procedure

1. **Isolate.** `git worktree add --detach <worktrees-dir>/<name> origin/main`. Never switch branch, edit, or touch the venv of the live checkout. One `fix/<desc>` branch per logical change.
2. **Port.** `git cherry-pick -n <sha>`, recommit as a Conventional Commit with no `carry(...)`, `Carry-Origin`, `cherry picked from`, or local-SHA trailers. Replace test strings/comments that echo private script, job, host or business names with generic identifiers that exercise the same path. Local carry notes never go upstream.
3. **Duplicate + overlap.** `gh search prs --repo OWNER/REPO --state open "<symbol>"`; for any open PR touching the same file, read `gh pr view N --json files` and its diff and state in the body whether yours is complementary.
4. **Audit callers before narrowing a rule.** When a fix removes a prefix/allow-list entry or tightens a predicate, `git grep` every caller of the predicate and every literal name in the family. Callers elsewhere (override paths, env strip/scrub loops) may depend on the old membership; the module's own tests will not show that regression. Narrow only what no caller relies on, and list the remaining names exhaustively from real reads.
5. **Test in Docker, before/after** (recipe: `references/docker-before-after-testing.md`). Per branch: test hunks alone on origin/main FAIL; full patch PASSES; sibling directory shows no new failures vs the same run on unpatched main. For security/scope changes also sweep every test file referencing the changed symbol and diff FAILED sets with `comm`.
6. **Privacy gate.** Run a privacy gate such as `tools/privacy_gate.py` from the sibling public repo [operator-safety-kit](https://github.com/uachristian/operator-safety-kit): `python3 privacy_gate.py --denylist <private-denylist> origin/main..<branch>` must exit 0 for each branch (empty range must exit 2). Author/committer must be a noreply identity. Separately grep PR body and comment files for owner name, business names, home paths, private IPs, emails. See [references/upstream-pr-privacy-gate.md](../../github/github-operations/references/upstream-pr-privacy-gate.md).
7. **Bodies.** Fill the repo PR template using only numbers seen in tool output. Title and body in separate files. State the test environment honestly (container, Python version) and leave the full-suite checkbox unchecked if only directories ran.
8. **Publish on explicit go only.** `git push fork <b>:refs/heads/<b>`; verify `git ls-remote --heads fork <b>` equals local SHA; `gh pr create -R OWNER/REPO --base main --head <user>:<b> --title "$(cat t)" --body-file b.md`. Re-read each PR (`gh pr view --json files,commits,body`) and re-scan the rendered body.
9. **Triage labels.** For `needs-repro`, run a minimal real-import repro on unpatched main and with the patch in the same container, privacy-grep it, then post script + both outputs with `gh pr comment --body-file`. Never post output you did not execute.
10. **Watch + cleanup.** Offer a read-only watch cron (`references/pr-watch-cron.md`). Remove test containers/images at the end (needs owner approval).

## Always-on rules

- Report only test counts and transitions you saw in tool output. Truncated output, a failed image build, or a shared scratch dir means the result is unknown: say so and rerun. Never present a code-reading inference as a test result. If an earlier report was wrong, correct it explicitly before the user approves anything public.
- Use a unique scratch dir and unique image/container names per session; concurrent sessions can overwrite a shared scratch dir and silently change what ran.
- A "not ready" branch with a confirmed regression gets fixed at the design level (keep what callers depend on), re-tested before/after, re-gated, then pushed; do not push it with a caveat.
- Reply format for the owner: short status per PR (link, one-line what it fixes, verified numbers), then what is still open.
