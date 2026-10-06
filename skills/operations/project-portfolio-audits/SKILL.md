---
name: project-portfolio-audits
description: "Use when auditing unfinished projects, backlogs, and roadmaps to decide what to finish, improve, park, or retire."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [project]
---

# Project portfolio audits

Use this skill for read-only audits of possibly unfinished, uncertain, interrupted, parked, or completed projects across Hermes conversations, the Obsidian vault, local repositories, staged artifacts, and live automation metadata.

## Objective

Separate actual loose ends from work that is intentionally deferred, owner-gated, completed-but-stale in documentation, rejected, or currently healthy. Do not turn every roadmap checkbox into an obligation.


## Concept recall and saved-for-later project selection

When the owner asks what projects were discussed, started, or saved to revisit so they can pick a build, use **backlog recall**, not an operational-priority audit or fresh ideation.

1. Discover existing named projects before recommending anything. Search canonical concept/backlog notes and session history for `parked`, `deferred`, `save as a concept`, `come back to`, and `later`. Search across business ventures, product prototypes, integrations, creative/device projects, and infrastructure rather than restricting discovery to the latest capability roadmap. Keep private-profile boundaries intact.
2. Build the candidate inventory before ranking. For each candidate, recover the original purpose, what was actually built, the explicit stopping point, and the remaining piece. Deduplicate project families and exclude concurrent workstreams and items already rejected in the current conversation.
3. Read the full decision-bearing note, including its ending and newer closeouts. An early candidate list may be superseded by a later rejection in the same document; do not resurrect it as the recommended next batch. Distinguish an existing narrow implementation from the broader unbuilt concept.
4. Verify session hits around the actual owner message. Broad searches can return compacted summaries and tool payloads rather than a real deferral; scroll a small user/assistant window around the anchor to identify what was postponed. Prefer targeted project queries after discovery instead of repeatedly hydrating unrelated long sessions.
5. Present a broad, compact selection menu: project name, one sentence describing it, and the recorded stopping point or remaining build. Separate concept-only, partially built, and owner-held activation. Do not substitute a few personally ranked business improvements for the requested inventory, and do not turn every entry into a pitch or speculative new feature.
6. Label documentation-only findings as recorded state, not freshly verified runtime state. Reserve deeper code/runtime checks for resolving a decisive ambiguity or for the project the owner selects; no completion or missing-feature claim follows merely from an old roadmap or an unsuccessful search.
7. Treat rejection of a batch as a discovery correction: broaden the search and omit those candidates, rather than repackaging them or asking the owner to supply a direction that their saved-project history can answer. A rejection for this selection does not permanently cancel the project.

For this lane, omit repair rankings and elaborate audit closeouts unless requested. Offer a recommendation only after giving the actual choices or when the owner asks for one. Selection is not authority to resume paused jobs, activate a release, or modify another profile.

## Improvement reviews versus cleanup reviews

The owner's request to give older builds a “second look” can mean **improve existing processes, plugins, and integrations**, not remove them. Do not carry a preceding disk-cleanup or retirement frame into that new task. Once the owner says “not wanting to remove, wanting to improve,” reset the scope immediately: no removal candidates, pruning proposals, or deprecation framing unless separately requested.

For an improvement-oriented review:

- Discover operational systems, not just repositories or old build folders.
- Lead with what the system does today and the concrete benefit of improving it: less steering, faster answers, stronger output, clearer approvals, or more reliable recovery.
- Separate **confirmed repair needs**, **capability/usability opportunities**, and **healthy systems worth evaluating**. Age, low recorded usage, or an old source timestamp alone does not prove a defect or obsolescence.
- Read newer closeouts before proposing a feature; do not rebuild an already completed integration or reopen an intentional owner gate as unfinished work.
- Respect concurrent workstreams that the owner has excluded. Prefer useful work on an existing system over synthetic model benchmarks or duplicate audits.
- Give one bounded next action and observable acceptance criterion per candidate. For a healthy content pipeline, inspect actual recent output quality before proposing an architectural rewrite.
- A shortlist is not implementation authority. Preserve profile isolation, live-action approvals, and production change control.

For Telegram, present a concise ranked bullet list rather than a dense table. Name the best capability upgrade separately from the most urgent reliability repair. If audit notes were written, say “operational files/services unchanged; audit notes created,” not “files modified: none.”

See `references/improvement-oriented-system-reviews.md` for the evidence-to-upgrade workflow.

## Cross-system inventory / registry planning

When the owner says they and Hermes are losing track of what exists or how systems connect across the vault, memory and repos, they want a durable inventory layer. Here is how to plan it:

1. Baseline with real counts before proposing anything: total vault notes, `_drafts` count, flat Concepts size and README length, local git repos vs `gh repo list`, profiles, and memory fill. Check whether any system map or registry already exists.
2. Design the layer to **observe, never control**. No production job may depend on it, so its worst failure is a stale map. The owner's hard constraints:
   - follow industry standards: a software catalog in the style of Backstage, docs-as-code, ADRs only for real decisions;
   - automatic maintenance;
   - add no new cron (one read-only step in an existing nightly job);
   - stdlib-only script plus one data file;
   - no per-repo duplicate docs;
   - no LLM writes to the registry;
   - report-on-change drift only;
   - one-line rollback.
3. Cut bloat before the owner asks. Name what was removed and why. Treat a duplicate-doc or a new-service proposal as a defect.
4. Keep the reusable engine separate from the private instance data from day one, so the engine contains no business or personal specifics.
5. Before building a foundational piece, run an independent multi-model review of the exact plan using the owner's preferred reviewer models. Run it in a task-scoped configuration, not the default. Get an explicit APPROVE / CHANGES / REWORK verdict plus a do-not-build list. Present the combined verdict for a final go.
6. Phase approvals: discovery plus registry first. Vault draft archiving (never deletion) and Concepts re-lane moves come later as separately approved, reversible batches.

## Evidence hierarchy

Correlate all three layers before final classification:

1. **Canonical intent** — current vault roadmap, concept, closeout, approval packet, or handoff.
2. **Conversation outcome** — recent session bookends, final status, explicit stop point, and approval language.
3. **Current reality** — bounded live metadata: cron state, artifact existence, enabled/disabled state, repository cleanliness/parity, deployment receipt, or exact completion evidence.

A current live artifact or later closeout outranks stale roadmap wording. A roadmap alone is evidence of planned scope, not evidence of interruption.

## Required classifications

Give each project one primary classification:

- **True operational loose end** — expected work is broken, timing out, split-brain, uncommitted/unreleased, or missing required closeout.
- **Owner-gated ready to resume** — preparation is complete, but the next step legitimately requires owner facts, login, approval, physical presence, or an external/public action.
- **Intentionally deferred roadmap** — explicitly parked at a gate, stop point, or later phase.
- **Completed, documentation stale** — current evidence proves completion while an older note still says pending.
- **Closed/rejected** — policy, safety, scope, or owner decision ended the item.
- **Active and healthy** — current work is operating normally and is not a loose end.

## Recent finished-but-not-installed audits

When the owner asks for new, relevant builds system-wide, do not answer from the current conversation's completed-work list. State a recent discovery window, include older work only when a recent release/activation update makes it relevant, and inspect shared infrastructure plus specialist deployment metadata. Keep personal-system checks content-blind unless separately authorized.

- Separate **source built**, **installed bytes**, **runtime activation**, and **natural-run or user acceptance**. A reviewed prototype is not an installable production integration; a successful build is not a replaced Desktop bundle.
- Distinguish an accidentally missed installation from an explicitly owner-held release, an installed-but-blocked workflow, a superseded candidate, and an active concurrent deployment. Do not present an inventory pilot's technical APPROVE as owner deployment authority.
- Reconcile overlapping manifests successor-first: different hashes from an older release are expected when a newer approved release owns those paths. Recheck decisive hashes before reporting if another session is actively installing. Accept a fresh explicit owner confirmation of working behavior as owner-verified evidence; close the corresponding stale reload or acceptance hold without repeating disruptive activation, while leaving the exact activation mechanism unknown if it was not observed.
- Startup commit identity can prove a process predates a patch; it does not prove which dependency versions are loaded in memory. Likewise, an old bundle timestamp identifies a packaging-verification gap, not a demonstrated vulnerability.
- Read current failure evidence for installed jobs. A fail-closed dependency/source pin may block read-only lookups as well as writers; an installation receipt does not make the current workflow healthy.
- Enumerate assessed candidates and unresolved coverage explicitly. Counts of notes, checkpoints, worktrees or release slices are not counts of independent products. Never turn bounded discovery into an unconditional all-host all-clear.
- Lead with the concrete unfinished activation or repair and one recommended next step. Do not start another architecture project or silently activate held work during the audit.

See `references/recent-build-install-reconciliation.md` for the evidence and closeout recipe.

## Workflow

1. Define the requested scope and explicit exclusions.
2. Search vault filenames/content for project nouns plus `roadmap`, `closeout`, `remaining`, `deferred`, `approval`, `pilot`, `gate`, `staging`, and `at-home`.
3. Read the canonical note and any newer closeout/capture that can supersede it.
4. Search recent sessions for the project name and decisive phrases such as `waiting for approval`, `stopped before`, `fully complete`, `remaining`, `timed out`, and `no live change applied`. For pain-point reviews, verify actual owner messages rather than counting `role=user` hits: compaction summaries, worker packets, automatic notifications and restated prompts can share that role. Exclude synthetic records, deduplicate exact session/timestamp/content copies, decode only text from multimodal records, and inspect surrounding responses plus the latest outcome before classifying repeated friction.
5. Inspect only the minimum current state needed to resolve ambiguity. Prefer metadata over private content. Keep personal-profile checks content-blind unless the user explicitly authorizes more.
6. For code/automation, compare canonical source, deployed copies, and repository status. A healthy runtime can coexist with release/source drift; classify those separately.
8. Do not limit discovery to Git roots. Inventory non-Git project markers (`package.json`, `pyproject.toml`, `Package.swift`, build contracts) and profile-owned code lanes such as `scripts/`, `skills/`, `plugins/`, and explicitly source-like tool directories under otherwise runtime-oriented trees. Treat code under a `state/tools/` boundary as a source candidate, but never treat the surrounding runtime state, evidence, logs, credentials, or generated artifacts as publishable source.
9. Separate discovery from remediation. Freeze and rank the complete candidate set first; then take one source-authority candidate at a time through curation, tests, secret/path policy, private-visibility proof, push, remote SHA parity, and exact-head CI before starting the next build. Parallel discovery may continue, but do not accumulate several unverified local mirrors.
10. For operational audits, rank by present operational impact, then owner readiness and value—not by roadmap size. For concept/backlog recall, preserve the selection-menu workflow above instead of filtering out interesting parked projects on operational-priority grounds.
11. Give one true next action per project. Do not recommend every optional phase.

## Evidence standards

- Cite exact vault paths and Hermes session links.
- For live state, report compact fields only: enabled/state, last status/run/error class, artifact presence, dirty count, or parity result.
- Distinguish one failed parent stage from healthy downstream/sibling jobs; do not label the whole system failed without evidence.
- A partial artifact after timeout is not completion evidence. Check downstream-phase evidence and stale lock/process state.
- An exact approval hold is intentional deferral, not interruption.
- A policy-disallowed deliverable is closed/rejected, not pending.

## Output format

Lead with the outcome. For concept/backlog recall, use the concise unranked selection menu above. For operational portfolio audits, prefer a compact ranked table where the channel renders it; use bullets in chat and plain text in CLI:

| Rank | Project | Classification | Evidence-backed status | True next action |
|---|---|---|---|---|

Then summarize:

- Actual repair priorities
- Owner-gated ready work
- Items that should remain deferred
- Completed work obscured by stale notes
- Evidence paths/session links
- Files created or modified
- Issues encountered

For a read-only audit, state whether operational files/services changed. Use `Files modified: none` only if no audit artifacts, skill updates or vault notes were written; otherwise list those evidence/documentation writes separately.

## Session closeout: “is everything installed and done?”

Answer from the work actually selected in this session, not the earlier idea menu or every discovered opportunity.

1. List each selected item once and assign its final disposition: installed, pending acceptance, source-closeout needed, deliberately rejected, or unnecessary after verification. Do not count a rejected optimization or an already-existing capability as unfinished implementation.
2. Recheck installation receipts against the exact target bytes, then inspect only relevant activation metadata. Distinguish fresh-process consumers from cached in-process plugins: identify the real import boundary before recommending a restart. A connected gateway does not establish that the owner's confirmation flow works.
3. Compare task-scoped installed files with the canonical recovery repository. A feature branch containing the fix is not canonical reconciliation. When authorized, inspect the entire ahead range, preserve unrelated drift, use a clean fast-forward where possible, verify the destination is private, push the intended branch, and require remote SHA equality plus exact-head CI. Name the branch; a successful feature-branch push is not a default-branch merge.
4. Put the verified current disposition at the top of the owning handoff and move prior incompatible states into clearly historical sections. Replace stale next actions rather than stacking contradictory “current” summaries; otherwise the next worker can reinstall completed work or resume a rejected candidate.
5. Close with two short lists: engineering/deployment complete, and real-use acceptance still open. Name the exact owner action and any natural-run observation still missing. Do not simulate an owner confirmation, force a staff/customer message to make a check green, or equate remote CI with production acceptance.

## Single-project status and finish-line reviews

When the owner asks “where does project X stand and what's needed to finish it,” run the same evidence hierarchy but shape the output as a decision brief, not a ranked table. See `references/single-project-finish-line-reviews.md` for the sequence, the stalled-external-dependency decision fork, and the evidence-gathering pitfalls (vault trail dating, session-search spillover, TCC-scoped probes).

## Pitfalls

- Never infer unfinished work from unchecked roadmap phases alone.
- Never infer completion from a green sibling cron or valid partial artifact.
- Do not call login-, approval-, or at-home-gated work a system failure.
- Do not let stale docs override current live state; report documentation drift.
- Do not bury a narrow defect inside a recommendation to rebuild the whole project.
- Do not over-rank ambitious future roadmaps above current operational breakage.

## References

- `references/classification-examples.md` — representative evidence patterns for true loose ends, owner gates, conscious deferrals, and stale-roadmap false positives.
- `references/single-project-finish-line-reviews.md` — decision-brief shape for “where does project X stand / what finishes it”: recency-dated vault trail, narrow session queries, artifact and cron metadata, provider-ticket silence counting, and the wait/route-around/descope fork.
