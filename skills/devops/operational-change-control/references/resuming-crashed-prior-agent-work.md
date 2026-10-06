# Resuming a Crashed Prior Agent's Partial Production Work

## When this applies

The current session is being asked to "finish what it started," "resume," "continue," or "pick up" work from a previous turn or session that ended abnormally (model crash, backend error, non-retryable client error, network drop, `'NoneType' object is not iterable` and similar provider-side failures mid-tool-loop). The prior agent had production-adjacent authority — touching `.env`, cron, gateway, profile config, public APIs, or any system with side effects beyond the local repo.

This is a CHANGE-CONTROL HIGH-RISK class of task. Treat it as such even when the user's tone is casual.

## The trap

When a prior agent crashes mid-plan, the on-disk state often does not match the plan it described. Specifically:

- The agent may have executed steps it had not yet announced.
- The agent may have skipped its own approval gate ("wait for the user's GO phrase before flipping the live gate") because the crash interrupted the conditional branch.
- The user's only context is the last message the prior agent successfully sent — which can be the plan/recommendation, not the actual diff.
- "Finish what it started" naturally reads as "execute the remaining steps of the recommendation." But the recommendation may already be obsolete because earlier steps over-shot.

If you continue from the plan without verifying disk state, you compound the violation instead of catching it.

## Mandatory protocol before any continuation

Before touching anything, run a forensic pass. Read-only tools only.

1. **Recover the original plan / approval gate.** Find the prior agent's last message (request dumps under `~/.hermes/sessions/request_dump_*.json`, session transcript, or what the user pasted). Identify:
   - The explicit GO phrase or approval condition.
   - The steps the prior agent said it would and would NOT execute before that gate.
   - The intended rollback/reversal procedure if any was named.
2. **Inventory current on-disk state** for every artifact the plan touched:
   - `.env` flags and gate variables — compare each variable named in the plan to its current value. List flipped-to-true gates separately.
   - `cron/jobs.json` (per-profile) — any new job ID, script reference, or schedule that matches the plan's executor.
   - Audit / actions logs (`state/.../*.jsonl`, `state/outbox/`) — look for entries where `gates.public_action_mode=true` or `api_status` is anything other than `dry_run` / `skipped`. These are evidence the live path actually ran.
   - Scripts, quarantine directories, backup snapshots — confirm they exist and are intact.
   - Profile launchd plists and `~/.hermes/processes.json` if the change touched lifecycle.
3. **Distinguish "tried but failed" from "did not run."** A live API call that returned HTTP 4xx/5xx is STILL a violation if the gate wasn't approved — the gate, not the response, is the safety boundary. Record both the attempt and the response separately.
4. **Build the actual-vs-intended diff** before talking to the user. For each plan step, mark one of: `not started`, `prep-only (matches intent)`, `over-shot (executed past gate)`, `failed cleanly (no side effect)`, `failed dirty (side effect partial)`.

## How to respond to the user

Lead with the over-shot items, not the prep work. The user will assume good-faith continuation; your job is to surface the gate violation immediately.

Recommended response shape:

- One-sentence headline naming the violation class ("prior agent enabled public-action gates before the GO phrase").
- "What was supposed to happen" — quote the approval gate verbatim from the prior plan.
- "What actually happened on disk" — numbered, with file paths and line evidence (`actions.jsonl` line N, `.env` line N, cron job ID).
- "Why the blast radius is bounded" (if applicable) — e.g. token lacked permission, daily cap zero, dry-run guard inside script caught it. Be explicit that this is luck, not authorization.
- Proposed rollback as numbered steps, each one a reversible operation tied to a specific file.
- Stop. Ask for explicit approval before executing the rollback. Do not chain "finish what it started" into the rollback either — the rollback is itself a change-control event.

## Pitfalls

- **Do not treat "finish what it started" as carte blanche.** The user is repeating the prior agent's stated intent, not authorizing every step the prior agent might have taken on disk. When the message is short and the prior context spans a crashed session, default to forensic mode, not execution mode.
- **Do not silently re-quarantine, revert, or "tidy up" before flagging.** Even reversible cleanup hides the evidence of what the prior agent did and prevents the user from learning that their isolation posture was breached. Flag first, rollback second.
- **Do not assume the request dump is the original prompt.** Crashed sessions often dump the FINAL turn (a "Status?" or trivial message), not the originating instruction. Check timestamps and message length before relying on it.
- **Do not skip the audit log scan.** The most damning evidence — `public_action_taken: false` lines with `gates.public_action_mode=true` and `reason: live_auto_like_attempt` — lives in JSONL state files, not in the .env or cron config. A surface-level inventory misses it.
- **Do not let a 4xx response talk you out of reporting the gate violation.** "The API rejected it so no harm done" is the wrong framing. The gate is the safety, not the upstream service's permission model.
- **Do not include the rollback step list in the same response as the execution.** Plan + risks + rollback → wait → execute. Even when the rollback feels obvious.

## Example trigger phrases that should activate this protocol

- "Finish what it started"
- "Continue from where the last session left off"
- "Resume the [feature] work"
- "The previous turn crashed, pick it up"
- "Here's what we were doing — keep going" (especially when pasted content is the prior agent's own recommendation rather than a fresh instruction)

## Related

- `references/cron-change-checklist.md` — when the over-shot artifact is a cron job, use this for the safe revert sequence.
- SOUL files of specialist profiles — the approval gates a prior agent violated are usually written there verbatim. Quote them back to the user during the forensic report.
