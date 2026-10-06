---
name: agentic-fleet-observer
description: "Use when adding a scheduled self-improvement observer to an autonomous agent fleet. Report-only review packets, never silent self-edits."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [autonomous-agents, cron-fleet, observer, self-improvement, framework]
---

# Agentic Fleet Observer — Framework

When you build a fleet of autonomous crons for any domain, add one Observer cron. It doesn't do the work — it watches the work and makes the fleet smarter over time.

## The Core Idea

Every cron fleet has two problems:
1. **Drift** — individual crons degrade silently (bad outputs, wrong thresholds, noisy format)
2. **Blindness** — the fleet never knows what it's missing relative to its own goals

The observer fixes both. It reads everything — cron outputs, live data, and the project's architectural intent — and returns a weekly synthesis: what's working, what's broken, and what should exist that doesn't yet.

The key insight: **the observer must read the concept doc at runtime**, not have the goals baked into its prompt. This means as the project evolves, the observer's frame of reference automatically updates without prompt changes.

---

## When to Add an Observer

Add an observer whenever:
- You have 3+ crons running in a fleet on a shared domain
- The fleet will run for weeks or months (not a one-off)
- You want the system to propose its own improvements over time
- The domain is complex enough that you can't anticipate all useful additions upfront

---

## Observer Anatomy

### Schedule
Run **after** the fleet's weekly cycle completes — typically Sunday evening after all weekly crons have fired. The observer needs real outputs to analyze.

### Model
Always Sonnet or better. The observer's job is synthesis and creative recommendation — not a place to save cost with Haiku.

### context_from
Wire to **all crons in the fleet**. The observer ingests the most recent output of every cron as context. This is what makes it aware of fleet-wide patterns without re-running any tools.

### Prompt Structure (7 sections)

**1. Read the concept doc first (critical)**
The observer must load the project's architectural intent at runtime:
```
Read the project concept doc at: [path to concept/architecture doc]
This defines: role definition, target architecture, completed phases,
planned phases, deferred tasks, known gaps.
Use this as your baseline — not just what the fleet does, but what it's supposed to become.
```
Also load any related fleet architecture docs if they exist.

**2. Cron Performance Review**
For each cron: was output actionable? Recurring noise? Thresholds right? Data quality?
One evaluation per cron, specific and named.

**3. Live Data Snapshot**
Pull a fresh snapshot from the domain's primary data source (operations board, CRM, analytics, etc.).
Look for systemic patterns the crons are missing — things that appear week after week.

**4. Pain Points**
Specific named issues only. No vague "could be better."
Format: what the problem is, which cron owns it, what the symptom looks like in output.

**5. Cron Recommendations**
```
Cron: [name]
Issue: [exact problem]
Fix: [specific change to prompt, threshold, or logic]
Priority: HIGH / MEDIUM / LOW
```

**6. Architecture Gaps (vs concept doc)**
Compare current fleet coverage against the concept doc's role definition.
What's in the goals that has no cron or tool covering it?
Are planned phases ready to start? What's blocking them?
What data sources or integrations are unused but should be?

**7. Ideas Outside the Plan**
The most important section. Based on observed patterns + domain knowledge:
- What would a human expert know at the start of each day that no cron surfaces?
- What would prevent the most common failure mode that the system currently misses?
- What communication or financial visibility gaps could automation close?
- Propose concrete additions, not vague improvements.

**8. Wins**
What worked well. Specific. Reinforce before changing.

---

## Concept Doc Requirements

For the observer to work well, the project needs a living concept doc that includes:
- **Role definition** — what the system owns, what it deliberately doesn't own
- **Architecture diagram** — layers, data flows, integrations
- **Build status** — phases complete, planned, deferred
- **Deferred tasks** — known gaps parked for later
- **Resume point** — always updated to current state

Keep this doc updated as phases complete. The observer reads it live — stale docs produce stale recommendations.

---

## Kanban Card Creation (Section 8)

The observer should create Kanban cards for HIGH priority findings — closing the loop between "observer surfaces a problem" and "problem gets tracked and resolved." Without this, weekly reports are read-once messages. With it, they become a living backlog.

**Two card types:**

- **Cron improvement cards** — one per HIGH priority cron recommendation
  - Title: `fleet-observer: [cron name] — [brief issue]`
  - Body: exact issue + recommended fix + which cron output showed the problem
  - Assignee: default (human reviews and applies prompt changes)

- **System improvement cards** — one per HIGH priority architecture gap or idea outside the plan
  - Title: `fleet-observer: [what it is]`
  - Body: gap description + what it unlocks + suggested approach
  - Assignee: default

**Rules:**
- Only HIGH priority items get cards. MEDIUM/LOW stay in the report only.
- Deduplicate — check for existing open cards before creating. Don't re-create cards for issues already tracked.
- List created cards at the bottom of the report: `**Kanban cards created this week:** [titles]`

**Prerequisite:** The profile running the observer must have kanban dispatch enabled in its config .

---

## Fleet-wide observer coverage (don't leave an active profile unwatched)

A multi-profile fleet needs TWO things to be self-improving, and they're easy to confuse:
1. **Per-profile observers** — one dedicated observer cron per *active* profile that produces autonomous work (the per-fleet critique described above).
2. **A cross-profile orchestrator/scout** — default-profile crons that read every profile's observer/digest output and either apply low-risk fixes (orchestrator) or propose larger changes (scout).

When asked to "verify self-improvement coverage," audit BOTH layers against the **live** profile list, not a remembered one. Build the matrix: for each `~/.hermes/profiles/*/` dir (plus `default`), does it have (a) a dedicated observer, (b) explicit orchestrator scope, (c) scout coverage? Then classify each gap as a real blind spot vs. correct-by-design exclusion.

**Correct-by-design exclusions** (no dedicated observer needed): script-only/no-agent signal producers (e.g. `<profile-a>`), privacy-restricted profiles where only cron-health is reviewable (e.g. `<profile-b>`), and dormant profiles with zero crons (e.g. `<profile-c>`). The orchestrator should still health-check these; they just don't need their own analytical observer.

**Real blind spots to fix:** any profile running autonomous agentic crons with NO dedicated observer. A content/social/marketing profile is the highest-value catch — it most needs tone/brand-drift and dry-run-boundary review.

### Pitfall — hardcoded orchestrator INPUTS silently miss new profiles
The default orchestrator's review list is the #1 place coverage rots. If its prompt enumerates profiles by hand (`assistant, research, ops, ...`), every profile added later falls through invisibly, AND it can keep referencing a profile that no longer exists. The durable fix is to make the orchestrator **enumerate profiles dynamically via a `~/.hermes/profiles/*/cron/jobs.json` glob** (the read-only scout usually already does this) and instruct it to trust the live glob over any named list. Keep the named list only as a per-profile *authority-guard* reference (privacy/dry-run/physical-world caveats), not as the discovery mechanism. A typical audit finds a hardcoded list missing several newer profiles (`<profile-a>`, `<profile-b>`) and still naming a deleted one; switching to a glob and adding an observer for the uncovered content profile closes it.

### Observer placement consistency
Prefer running each per-profile observer **under the profile it observes** (`profile:` field), A profile-override observer registered in the central scheduler still fires correctly (the scheduler loads the target profile's env/skills at run time) and won't appear under `hermes --profile X cron list` — that's expected, not a fault. Data-injection collector scripts (e.g. `<profile>_observer_collect.sh`) must exist under the target profile's `scripts/` before relocating an observer to it.

## Delivery

Observer output goes directly to the human owner (Telegram DM, Slack DM, email) — not to team channels. It contains system-level critique and future roadmap suggestions that are owner-facing, not operational.

## Review-bus Escalation Packets

When an observer or autonomous-improvement cron needs another profile/default supervisor to act, send a bounded packet instead of a narrative report. Include source, affected scope, classification, evidence, proposed change, risk, rollback, dedupe key, cooldown, and requested owner. Dedupe by stable object identifiers (profile + cron/job/path + issue class), not message text, and avoid bot loops by sending one packet to the supervisor/default bot only. See `references/review-bus-packets.md` for the full packet contract.

For default-profile maintenance passes that act on observer outputs, see `references/autonomous-improvement-maintenance.md`. It covers active collector drift (profile-local collector newer than the root/default script a cron actually runs), evidence dedupe by stable identifiers, required validation, and audit logging.

---

## Wiring Example (jobs.json)

A reusable observer prompt template is in `templates/observer-prompt.md` — copy and adapt for any new fleet.

```json
{
  "name": "fleet-observer",
  "schedule": "0 19 * * 0",
  "model": {"model": "claude-sonnet-4-6", "provider": "anthropic"},
  "deliver": "origin",
  "context_from": ["<id1>", "<id2>", "<id3>", "...all fleet cron IDs"],
  "prompt": "..."
}
```

---

## What Changes as the Fleet Matures

**Phase 1 — new fleet:** Observer mostly does cron performance review. Section 7 (Ideas) is the most valuable — the fleet is new and there's a lot it doesn't cover yet.

**Phase 2 — stable fleet:** Observer shifts to architecture gaps and phase readiness. Cron performance section gets shorter as prompts dial in.

**Phase 3 — mature fleet:** Observer becomes a strategic advisor. Cron tuning is routine. The value is in surfacing non-obvious patterns and keeping the roadmap current.

**Phase 6+ — vault curation:** Wire an additional cron (or extend the observer) to write durable insights from the week's outputs to a vault or knowledge base. The observer synthesizes; the vault curation cron promotes findings to long-term memory.

---

## context_from — The Feedback Loop

`context_from` is the built-in mechanism for cron-to-cron memory. It injects the most recent completed output of a prior cron into the next run's context. This is what separates a stateless fleet from one that compounds on itself.

**Standard wiring patterns:**
- **Same-day chain:** `daily-close` ← `daily-open` (EOD sees what the day opened with, reports delta)
- **Day-over-day carry:** `daily-open` ← `daily-close` (morning knows how yesterday closed)
- **Week-over-week self:** `weekly-snapshot` ← `weekly-snapshot` (this Monday sees last Monday's snapshot, reports trend)
- **Weekend carry:** `week-start` ← `daily-close` (Friday's close flows into Monday, no cold start)
- **Observer:** ← all fleet crons (sees the full week in one pass)

**What NOT to wire:** Haiku crons doing mechanical threshold checks gain nothing from context — adds cost with no reasoning benefit. Wire Sonnet crons that synthesize, compare, or narrate.

**Limitation:** context_from injects the single most recent output per source cron. It is not a rolling history. For week-over-week trend data across multiple runs, vault curation (Phase 6) is needed.

---

## Pitfalls

- **Don't bake concept doc content into the prompt** — always read at runtime. Baked-in context goes stale the moment a phase completes.
- **context_from injects most recent output only** — the observer sees last week's snapshot, not every snapshot ever. For true week-over-week history, the vault curation cron (Phase 6) is needed.
- **Section 7 requires domain prompting** — generic "what are we missing?" gets generic answers. Prompt the observer with domain-specific framings: "What does a human [role] know at 7am that no cron surfaces?"
- **Observer on wrong profile = wrong skill tree** — the observer needs access to the same MCP tools and skills as the fleet it's observing. Keep it on the same profile, or ensure the profile has what it needs.
- **Schedule after all weekly crons** — if the observer runs before Monday crons fire, it has stale context. Sunday evening (7–9pm) works for a weekday fleet.
- **Deliver to owner only** — observer output is system critique, not team comms. Route to DM.
