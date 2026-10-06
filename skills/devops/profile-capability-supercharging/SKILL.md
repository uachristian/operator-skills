---
name: profile-capability-supercharging
description: "Use when building a major new capability for a specialist agent profile as reusable, safe operational infrastructure rather than one-off commands."
version: 1.1.12
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [profiles, capability-buildout, operations, automation, safety, skills, repos]
    related_skills: [operational-change-control, operational-backups]
---

# Profile Capability Supercharging

Use this skill when the owner asks to "supercharge capability," "add features and function," "level up" a Hermes profile, or build an overnight `/goal` that should materially transform how a specialist profile works.

The target shape is a reusable operational infrastructure layer, not a narrow one-off script.

## Core pattern

1. **Concept first, in the correct trust boundary.** Create or update a class-level concept/workflow doc that states the capability, current live surfaces, target state, non-goals, guardrails, smoke-test contract, repo/skill/vault closeout expectations, and future improvement loop. Normally this belongs in the canonical main vault. **Isolation exception:** when the owner explicitly requires a new commercial/partner project to stay out of default memory, the main vault, and existing business databases, do not create even a placeholder main-vault concept or default memory entry.
2. **Profile boundaries preserved.** Default/orchestrator coordinates; the specialist profile owns domain execution; do not copy credentials or weaken isolation unless the owner explicitly approves. Before any backup, config edit, or CLI-auth action, prove the effective account home, profile `HERMES_HOME`, terminal `home_mode`/`cwd`, and inherited Python/shell state.
3. **Authority and state audit.** Before extending a profile, compare live runtime files, cron definitions, mutable state, private source mirrors, and integration copies. Do not assume the repo is authoritative when verified live protections may be ahead. A copied source checksum manifest proves only what the source tree contained when generated; it does **not** prove the live runtime still matches. Maintain an explicit source-to-live deployment map/parity check, classify every difference, and reduce avoidable substitutions with profile-safe paths such as `$HERMES_HOME` or self-locating scripts. Keep live marketplace IDs and operational outcomes in runtime state/reports, never in source fixtures. When several jobs share a producer, separate observation from exposure: planning modes stay read-only and only the explicit execution workflow may mutate state for candidates it actually selected.
4. **Deterministic core.** Build scripts/modules/tools for core computation, classification, extraction, or routing. Use LLMs for summarization/judgment only after structured state exists. For private adaptive coaching/learning capabilities, split reviewed source content from content-free owner runtime state, make free-form responses structurally unpersistable, and prove the real private state—not only fixtures.
5. **Safe action model.** Start read-only/dry-run/proposal-only. Owner-gated write classes require evidence, rollback, and explicit approval. For authenticated seller/vendor portals, separate login approval from action approval, map controls read-only through accessibility snapshots, bind each remote write to an exact local digest, and never invent source lineage, inventory evidence, cost basis, or policy IDs to force a pilot through validation.
6. **Usability surface.** Add an on-demand helper/command and, where useful, a daily/weekly owner-facing artifact so the owner does not need to know internal script names. If the owner says existing reports/crons are too much to intake, build the compact replacement surface first and defer cron delivery changes until the output is verified.
7. **Cron consolidation after proof.** For day-to-day usability upgrades, do not pause/delete noisy reports in the same step as the replacement build. First ship and smoke-test the compact surface, then propose a separate backed-up cron consolidation patch that converts verbose reports to local/feeders or pauses direct delivery.
8. **Verification matrix.** Require unit/fixture tests, live read-only smoke, no-write assertions, secret scan over tracked **and non-ignored untracked** candidate files, explicit source/live parity, cron verification if scheduled, and backup verification. For isolated foundations with blocked real-data/external-account/deployment gates, add mutation-based rejection tests, an exact approved-secret-value containment scan, effective workload-UID inspection, and a restored-backup verification using `references/fail-closed-foundation-verification.md`. For path-sensitive profile services, include a real smoke with `HOME` deliberately remapped; release from a clean exact-commit worktree and read back the private remote tip.
9. **Readiness classification.** Distinguish fixture-ready, pilot-ready, repeatable capability, operational system, and autonomy-ready. When the owner asks “what’s next,” run the live gap audit in `references/specialist-profile-readiness-gap-audit.md` instead of re-listing completed pilot work.
10. **Close lifecycle gaps before adding adjacent intelligence.** A mature profile may already plan and execute while still lacking intake, assignment, confirmation, exception, or post-action closure. Prefer completing the broken operational loop over adding another report. If the owner selects multiple related capabilities, sequence the upstream evidence-producing loop first, then build analytics/recommendations that depend on its trustworthy lineage. Probe exact live resource visibility separately from permissions or tool names; granted scope without a visible account/object is fixture-ready, not operational readiness.
11. **Durability closeout.** Update vault docs, skills, plugin metadata, profile SOUL docs if boundaries changed, repo mirrors, cron prompts/scripts, backups, and `log.md`; verify item-by-item.
12. **Ongoing improvement.** Add or update a weekly proposal-only review cron instead of leaving the capability to decay.

## Overnight `/goal` handoff shape

When the owner wants the build to run overnight, provide a single self-contained `/goal` prompt that includes:

- exact concept doc path;
- skills/docs to load;
- mission and definition of done;
- explicit non-goals and forbidden actions;
- implementation sequence;
- smoke-test and closeout contract;
- final report requirements;
- no recursive cron scheduling;
- no secrets/customer PII in outputs.

The prompt must be concrete enough that a fresh session can complete the build without relying on chat history.

## What "fully set up" means

Before reporting done, verify all relevant surfaces:

- live profile files;
- default/orchestrator scripts if changed;
- cron job definitions and next-run state;
- plugin metadata/tool descriptions/schemas if applicable;
- source repo and internal mirrors;
- skill files and references;
- vault concept/workflow/README/log entries;
- backup manifest and restore notes;
- tests/smokes with real outputs.

A clean git status alone is not enough. Compare live profile files to mirrors when runtime files matter.

## High-value examples

- Owner control tower: cross-profile command surface for money, blockers, leads, messages, and automation health.

## Pitfalls

- Do not turn a supercharge request into a narrow one-off script.
- Do not skip the concept doc; future agents need the target state and guardrails.
- Do not create duplicate crons if an existing observer/review cron can safely absorb the new review scope.
- Do not perform live writes just because the capability is ambitious. Graduate write classes separately.
- Do not claim "vault/repo/skills/plugin fully updated" until every surface is checked directly.
- Do not trust a successful config-write message for list-valued tool settings. Re-read the YAML type and verify the resolved CLI/messaging tool lists; a quoted JSON-looking string may leave broad defaults enabled.
- Do not judge skill isolation by count alone. Scan retained skills and references for forbidden vault lanes, unrelated credentials, default-profile authority, and stale runtime instructions.
- Do not treat dependency/package health as proof that an end-to-end capability works. Smoke-test it through the target profile using the same runtime, user, architecture, and persistence boundaries it will have in service. If it fails, diagnose configuration and image/runtime compatibility, then remediate through a reviewed build or explicitly document the temporary limitation. Do not let an agent improvise global or package-runner installs into a persistent profile; dependency changes must be explicitly approved, tracked, and reverified.
- Do not let a narrow newer review silently supersede an older reproduced finding when the affected file or trust boundary did not change. Prove the finding is remediated at the current exact tip or carry it forward as a blocker. Security verdicts must require an exact hashed report set and derive severity totals from scanner records; caller-supplied counts, empty report maps, successful report-generation exits, or experimental comparison-tool output are not vulnerability clearance. Prefer independently generated candidate and upstream SARIF when comparison tooling is unstable.
- For non-root Docker candidates derived from an s6-supervised upstream image, test the image's real default startup rather than only probes that override the entrypoint. The inherited pre-init may require root even when every capability probe passes; candidate-only images should clear that entrypoint and use an inert command unless the supervisor boundary is separately reviewed. Do not nest writable state/raw mounts beneath a read-only live-profile bind: stage a sanitized candidate profile root with explicit mountpoints and mount the exact source checkout separately. When testing Git recovery, run `git bundle verify` from repository context before cloning the bundle into a disposable root. Treat every external Docker volume as part of the recovery artifact graph: an image archive is not offline-capable when malware databases or other required runtime assets live only in a named volume. Export and hash the exact volume, restore it under a new isolated name, mount it through the real read-only runtime boundary, and prove both a healthy control and the adversarial control (for ClamAV, clean scan plus EICAR) before accepting document/runtime recovery.
- For privacy-sensitive adaptive tools, do not preserve the personal story behind a learner setting, accept arbitrary strings in an otherwise allowlisted state schema, or call fixture-ready logic personalized before the real private state and owner launcher pass. When the exact native toolchain is unavailable, ship a verified shared-core surface and leave native UI, voice, messaging, and credentials behind separate gates rather than editing an unbuildable target.

## References

- `references/fail-closed-foundation-verification.md` — convert blocked data/account/deployment policies into executable invariants, mutation-based rejection tests, two-layer secret containment scans, effective container-workload checks, exact-tip re-review, and restored-backup evidence.
- `references/specialist-profile-readiness-gap-audit.md` — live evidence matrix and maturity model for separating a successful pilot from a repeatable, operational, or autonomy-ready specialist profile.
