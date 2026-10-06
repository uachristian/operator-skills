# Specialist Profile Readiness Gap Audit

Use this reference when a pilot capability has succeeded and the owner asks what remains before the specialist profile is "fully up," "ready," or operationally complete.

## Core distinction

Never collapse these maturity levels:

1. **Fixture-ready** — deterministic core passes synthetic tests.
2. **Pilot-ready** — one reviewed real item/workflow succeeds under explicit approval.
3. **Repeatable capability** — arbitrary in-policy inputs can move through a documented owner-facing workflow.
4. **Operational system** — intake, execution, exception handling, post-action lifecycle, accounting/audit, and recovery are covered.
5. **Autonomy-ready** — only separately graduated action classes may run with reduced supervision.

Lead with the highest level actually proven. Do not call a profile complete because one pilot worked.

## Evidence matrix

Check live state rather than relying on narrative docs:

- profile discovery, model, alias, and gateway state;
- subprocess environment baseline before any backup or CLI action: resolve the real user home, profile `HERMES_HOME`, terminal `home_mode`, and any inherited `PYTHONPATH`/`PYTHONHOME`; use explicit absolute paths until the environment is proven;
- exact enabled toolsets and MCP allowlists;
- each MCP server connection and discovered tool count;
- daemon/LaunchAgent health and loopback binding;
- credential **presence only**, never values;
- authenticated-session status and whether an active tab/session is actually present;
- database integrity, schema version, record counts, and external IDs;
- active test discovery count and results;
- live files versus rollback snapshots and docs;
- source-repository/mirror existence and privacy;
- owner-facing intake/status/action path;
- backup, encrypted recovery, and no-live-services restore proof.

A healthy daemon is not proof of an authenticated marketplace session. An exposed tool name is not proof that the action is implemented or permitted.

## Drift checks

Treat discrepancies as readiness findings:

- docs claim more tests than active discovery runs;
- a test exists only in a backup snapshot;
- runtime files are not represented in a private source mirror;
- docs say an action is hard-locked while the MCP allowlist still exposes confusing action controls;
- one pilot item is hard-coded into a selector map or driver;
- the database supports inventory but no owner-facing intake tool can create it;
- a candidate handoff exists only as fixtures and has no live producer;
- an order table exists but fulfillment, returns, and accounting are absent.

Do not silently count missing coverage as completed work. Identify the precise missing artifact and its recoverable source when available.

## Recommended sequencing

1. **Stabilize the proven pilot**
   - restore missing tests;
   - explain/prevent drift;
   - establish a private source mirror;
   - shrink confusing or unused tool exposure;
   - preserve rollback material.
2. **Make the capability repeatable**
   - add narrow intake/status tools;
   - make data and selectors item-agnostic where safe;
   - prove a second low-risk item under the same no-publish policy.
3. **Connect official read surfaces**
   - owner completes legal/terms/credential prerequisites locally;
   - begin with read-only account, inventory, offer, and order access.
4. **Build the post-action lifecycle**
   - reservation, fulfillment, tracking, messages, returns, fees, COGS, and audit.
5. **Prove recovery**
   - independently encrypted pack;
   - disposable restore;
   - no live gateways, daemons, browser writes, or marketplace actions.
6. **Graduate each external write separately**
   - exact object/digest binding;
   - fresh one-use approval;
   - one attempt;
   - immediate live readback;
   - reconciliation and rollback.

## Owner-interface decision

Prefer the lowest-infrastructure surface that is genuinely usable. A headless specialist controlled through default plus narrow MCP tools is often safer than adding another bot/gateway. Add a dedicated messaging identity only when it materially improves operations and its permissions, routing, and failure handling are fully defined.

## Reporting format

Return:

- **Current proven level**;
- **Verified live facts**;
- **Blockers in dependency order**;
- **Actions only the owner can perform**;
- **Recommended immediate package**;
- **Optional later graduation**, clearly separated from launch requirements.

For “what’s next,” perform forward gap analysis and do not re-list completed pilot work as recommendations.

## Pilot-versus-operation example

One successful end-to-end pilot action proves pilot readiness, not a repeatable operation. Repeatable readiness still requires stable tests/source, general intake, a second independent case, official read-only APIs, physical/financial policies, the post-transaction lifecycle, and recovery proof. Any public or irreversible action remains a separately graduated action class rather than an assumed next step.
