---
name: hermes-security-privacy-audits
description: "Use when auditing an agent deployment for security, privacy, prompt-injection exposure, or agents doing unauthorized things. Read-only first."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [security, privacy, audit, approvals, agent-behavior]
    related_skills: [operational-change-control]
---

# Hermes Security and Privacy Audits

## When to Use

Use when the owner asks for a security or privacy review, or asks whether agents are doing unauthorized, misguided or compromising things. Stay read-only unless they approves specific changes. Present the fix plan numbered so they can pick items ("go 1,3,4").

## Procedure

1. **Start from the prior baseline.** Read the security notes index in your knowledge base and the newest host-audit note. Re-verify every open finding live, and report each one as still-open, fixed, or new.
2. **Host posture (one batched terminal call):** `sw_vers`, `fdesetup status`, `defaults read` of the loginwindow `autoLoginUser` key, `socketfilterfw --getglobalstate --getstealthmode`, `csrutil status`, `spctl --status`, `softwareupdate -l`, `launchctl print system/com.openssh.sshd` (`systemsetup` needs admin), the authorized_keys key types and comments, `tmutil destinationinfo`.
3. **Exposure:**
   - Run `lsof -nP -iTCP -sTCP:LISTEN` and keep only non-loopback listeners.
   - For each cloudflared ingress hostname, curl `/` and `/api/status` and expect 404 or an auth failure.
   - For local api_server ports, an unauthenticated POST to `/v1/chat/completions` should return 401.
   - Each webhook should bind to 127.0.0.1 and have a secret. The dashboard should bind to loopback or a private VPN interface only.
4. **Per-profile config (one execute_code call over the default root plus `profiles/*`):**
   - modes of config, `.env` and auth files
   - literal token regex hits, reported as key path only
   - messaging `platform_toolsets`
   - the `approvals` block and `command_allowlist`
   - `security.tirith_fail_open`
   - `*_ALLOWED_USERS`/`_ALLOWED_BOTS`/`_ALLOWED_CHATS`, with IDs masked
   - MCP servers launched with `npx`, `@latest` or `uvx` (unpinned)
5. **Agent behavior from state.db.** Open every DB (the default `state.db` plus `profiles/*/state.db`) as `file:...?mode=ro` and use a 30-day window on `messages.timestamp`.
   - **Smart-approval volume:** find tool messages containing `auto-approved by smart approval`. Parse the reason in `Command was flagged (...)` and count by profile and `sessions.source`. To see the real commands, join each `tool_call_id` back to the assistant `tool_calls` JSON. Tally the targets for delete categories.
   - **Blocks:** count `BLOCKED:` reasons. Timeouts are not misuse.
   - **Bot-driven sessions:** filter `sessions.user_id` by allowlisted bot IDs. Tally their tools and their patch/write_file paths.
   - **Cron edits:** map `cron_<jobid>_<ts>` to the job name in `cron/jobs.json`. List patch/write_file/skill_manage targets, and terminal commands containing rm, launchctl, chmod, git push or `sed -i`.
   - **Privacy boundary:** in non-personal DBs, find tool arguments that reference personal-only vault folders or a personal profile. Classify each hit as metadata (cron, config, status) or content.
   - **Prompt injection:** regex user and tool messages for jailbreak phrasing. Drop hits whose surrounding ±300 characters mention injection, jailbreak, wrap_untrusted, untrusted, test or FILTERED; those are the system's own tests and docs. Do NOT include `untrusted_tool_result` in the jailbreak regex: Hermes wraps every web/browser/MCP result in that tag, so it yields thousands of false hits. Report only the residual hits and classify each (real payload vs synthetic eval fixture).
6. **Gateway logs:** grep `Blocked unauthorized user`, `blocked at load time` (the memory guard working), and `Skill security warning`. Your own bot IDs denied in a shared bot-coordination group are expected; only unknown human senders matter.
7. **Business-system write ledger (e.g. `logs/<system>-writes.jsonl`):**
   - Use `outcome == success` with non-GET methods, not `audit_intent` records.
   - Tally `provenance.authorization_class`, `approval_surface` and `cron_job_id`. Live writes from cron should be 0.
   - List DELETEs individually.
   - For writes with an empty `authorization`, resolve the session_id across all DBs to find the owning session.
8. **Secrets hygiene:** count token-shaped regex matches in current logs (counts and pattern prefixes only). Find secret-named files that are group/world-readable (`-perm -044`).
9. **Audit freshness:** check when your scheduled security audit last ran, how old its last report is, and which checks it lacks.
10. **Prompt-injection blast radius (when the owner asks about injection safety).** Map where untrusted text meets powerful tools, and when they approve fixes, apply them with the recipe; see `references/prompt-injection-posture.md`.
11. **Capture during the task** in your notes system under the security hub, linked to the prior audit (a notes-vault capture plugin is available in the sibling public repo [vault-memory](https://github.com/uachristian/vault-memory)).

## Report shape (Telegram)

- Bottom line first: intrusion, compromise or injection found or not, and the single biggest risk.
- Then:
  - host findings, split into still-open and fixed
  - agent behavior
  - what's solid
  - monitoring gaps
  - not-verified items (router/UPnP, cloud MFA and sessions, FDA inventory, DR freshness)
- End with a numbered fix plan. Separate changes the agent can make with backup and rollback from the owner-only admin or restart steps, and state the trade-off of each.

## Pitfalls

- Don't call smart approval a human gate. Smart mode plus permanent `command_allowlist` entries (`execute_code`, `shell command via -c/-lc flag`) means flagged commands in owner chats are LLM-approved. Measure the volume rather than assume the gate holds.
- `cron_mode: deny` blocks approval-requiring commands only. Cron agents can still edit cron stores, prompts and other profiles' files through file tools, so audit their edit targets.
- Classify keyword-grep "unauthorized" counts before reporting them. Third-party MCP 401s, which mean expired credentials, and gateway startup allowlist warnings dominate the raw numbers.
- Ledger session IDs often live in a specialist profile's own state DB. Search every DB before calling one unknown.
- Ledger `provenance.mode` can read `report_only` on live successes. Trust `outcome` and `http_status`, and flag the mislabel. A write with no approval record is a logging gap, not proof of unauthorized action.
- Never print token values, private message content or full allowlist IDs. Mask the IDs and report only key paths and counts.
