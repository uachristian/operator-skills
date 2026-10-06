---
name: founder-alignment-launch-gates
description: "Use when a venture or partnership needs explicit founder decisions on ownership, roles, money, and pilot scope before anything launches."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [founders, venture, ownership, partners, pilot, launch-gates, decision-packet]
    related_skills: [project-portfolio-audits, operational-change-control]
---

# Founder alignment and launch gates

## Purpose

Use this skill when a private concept, prototype, brand direction, or website is complete enough that the next risk is no longer design quality—it is ambiguous ownership, partner authority, economics, customer/data ownership, liability, pilot scope, and launch readiness.

The output is a decision-ready founder packet, not legal advice, a public launch, a filing, partner representation, customer intake, or permission to build production operations.

## Core rule

Separate **what has been proven** from **what founders must decide** and **what third parties must authorize**. A polished artifact does not create company, supplier, compatibility, media, customer, or commercial authority.

## Workflow

1. **Preserve the approved artifact**
   - Record the exact approved commit/archive and scope.
   - Keep that release branch/tip unchanged.
   - Start founder/strategy work on a separate local branch so later documentation commits cannot be mistaken for the approved artifact.

2. **Read the current source of truth**
   - Founding charter or purpose statement.
   - Decision register.
   - Partner/portfolio map.
   - Revenue or offer hypothesis.
   - Launch roadmap.
   - Current project context and latest approval/closeout.
   - Prefer current active documents over historical release briefs.

3. **Classify the state honestly**
   - Website/prototype complete for its approved private scope.
   - Founder alignment owner-gated.
   - Partner authority unestablished until written evidence exists.
   - Public/commercial launch blocked until named gates close.
   - Do not call an owner decision a system failure or unfinished build.

4. **Draft recommended defaults**
   Cover at minimum:
   - controlling founder and equity principle;
   - strategic partner versus founder distinction;
   - arm's-length relationship with any affiliated business;
   - revenue architecture;
   - customer, consent, records, IP, and data ownership;
   - product, technical, delivery, warranty, and support responsibility map;
   - first controlled pilot;
   - partner-authority sequence;
   - working-name screening path.

5. **Make decisions recordable**
   Each decision must support:
   - Accepted / Modified / Deferred with owner and date / Rejected;
   - recommendation and alternatives;
   - evidence still needed;
   - decision authority;
   - operational consequence;
   - owner and due date.

6. **Create a launch-gate matrix**
   Use exact states such as Closed for private scope, Open, Blocked, or Not applicable. Name the evidence and authority needed to close each gate. Typical gates:
   - founder alignment;
   - name/entity;
   - partner authority;
   - affiliate/partner agreement;
   - customer/privacy/legal/contact surfaces;
   - revenue/economics;
   - product/technical feasibility;
   - independent operating workflow;
   - controlled pilot;
   - explicit public-launch approval.

7. **Align active documentation**
   - Update the current decision register, roadmap, context, and repository index.
   - Remove current-state contradictions such as named tiers after a one-package decision.
   - Preserve historical briefs as history instead of rewriting them.
   - Run internal-link checks, stale-phrase searches, and `git diff --check` before commit.

8. **Stop at the owner gate**
   - Do not file entities, buy domains, contact partners, publish, accept clients, purchase products, or build production integrations unless separately authorized.
   - Ask the founder decisions one at a time, leading with the recommended option.

## Recommended packet structure

1. Purpose and evidence boundary.
2. Current truth.
3. Recommended founder defaults.
4. Decision worksheet.
5. Time-boxed founder workshop agenda.
6. Launch-gate matrix.
7. Phase acceptance criteria.
8. Immediate post-decision outputs.
9. Decision record and action table.

## Common default patterns

### Controlling founder

Do not grant equity merely for product access, referrals, delivery capacity, or one supplier relationship. Start with commercial agreements unless a durable founder contribution, time commitment, governance role, capital/IP contribution, vesting path, and downside obligation justify equity.

### Affiliated businesses

Keep customer records, consent, accounting, credentials, and systems separate from any affiliated business. Contract delivery, validation, fulfillment, content, or referral work at arm's length with explicit pricing, data, liability, warranty, IP/media, and termination terms.

### Revenue

Model expertise/service value separately from product margin. Add a project-management fee when the venture coordinates suppliers, logistics, exceptions, or delivery. Avoid hiding all service value inside product markup.

### Pilot

Prefer one controlled, paid, customer/project-specific pilot. Internal readiness briefs may compare several candidates, but they are not public products, eligibility tiers, or universal-compatibility claims.

## Verification

Before committing the packet:

- all active relative links resolve;
- required packet sections exist;
- current active docs contain no superseded product/tier language;
- recommendations are labeled as recommendations, not decisions;
- external actions remain explicitly gated;
- the approved release tip remains unchanged on its branch;
- the founder branch is clean after commit;
- no remote/public action occurred.

## Pitfalls

- Treating the approved website tip as permission to form or launch the business.
- Granting equity to solve a contractable supplier-access problem.
- Blurring an affiliated business's customers, systems, warranties, and liabilities into the new venture.
- Asking for exact pricing before the revenue principle and responsibility map are decided.
- Publishing internal readiness briefs as fixed product programs.
- Updating historical briefs instead of current canonical documents.
- Advancing the approved release branch with strategy documents and then overstating approval scope.
- Letting Markdown trailing spaces stop the commit; use bullets or explicit blank fields and run `git diff --check`.
- Retrying a destructive reviewer-temp cleanup after an approval timeout. Disclose the hygiene boundary and wait for fresh consent.
