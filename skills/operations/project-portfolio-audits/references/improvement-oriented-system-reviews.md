# Improvement-oriented reviews of existing systems

Use when the owner asks which older processes, plugins, or integrations deserve another pass. This is distinct from disk cleanup, retirement, and a generic unfinished-project inventory.

## Frame the work correctly

A correction such as “processes, plugins, integrations” changes the unit of analysis from folders to working systems. “Not wanting to remove, wanting to improve” changes the objective from reducing inventory to increasing usefulness. Acknowledge that shift once and apply it to the shortlist; do not keep presenting removal as the main benefit.

## Bounded review sequence

1. Identify the user's desired outcome and excluded concurrent workstreams. Default to read-only discovery, not an unrequested rebuild.
2. Pick a small set of existing systems from canonical documentation and current runtime inventory. Include scripts, scheduled processes, native hooks, and service integrations—not only Git repositories.
3. Establish current truth using the latest closeout plus live metadata: enabled configuration, service/endpoint health, recent scheduled results, and relevant usage timestamps. Inspect actual output only within the authorized business/privacy lane.
4. Distinguish a live service from a useful workflow. A health response proves reachability, not real adoption, correct answers, provider health, or completed user journeys. Conversely, sparse local session history does not prove nobody uses a system through another path.
5. Classify each candidate:
   - **Repair:** a directly evidenced broken obligation or failure path.
   - **Capability upgrade:** an existing foundation could serve a concrete unmet user workflow.
   - **Usability/quality upgrade:** the system works, but observed outputs or handoffs impose avoidable steering.
   - **Keep as-is / gated:** healthy, recently completed, or intentionally waiting on an owner decision.
6. Propose the smallest next action that tests the value, with observable acceptance. Do not invent product defects merely to justify improvement work.
7. Rank by user value and present risk. Give the best capability opportunity and the most urgent reliability repair separate labels so urgent maintenance does not erase the requested improvement discussion.

## Examples of the right granularity

- **Voice foundation:** prove one authorized question-to-answer workflow through the existing operational runtime, rather than grant broad tools to an old sandbox or build another generic assistant.
- **Approval integration:** compare older text approvals with current exact-action cards; examine identity binding, ambiguous outcomes, and readback before proposing one consistent experience. Coexistence alone is not proof of a vulnerability or duplication.
- **Content automation:** review actual recent drafts for factual accuracy, photo fit, usefulness, and required editing. Improve the weakest observed step while retaining completed packaging and publication gates.
- **Recovery automation:** separate backup attempts, successful snapshots, restore proof, and current staging-space sufficiency. A service can be scheduled and still fail its required outcome.

## Reporting discipline

Use compact Telegram bullets: **system → current evidence → improvement → bounded next action**. Avoid dumping tool inventories or every roadmap phase. Say whether a finding is proven or a hypothesis. An investigation that did not establish the cause is not a completed root-cause diagnosis; an untested proposed probe is not a verified fix.

State the actual mutation boundary: no production changes, with audit-note writes disclosed separately. Keep personal data content-blind and do not revive excluded workstreams, retired products, or owner-gated capabilities merely because older documents mention them.
