# Review-bus packet structure and dedupe

Use this when an observer or autonomous-improvement cron needs to escalate findings to a supervising/default profile instead of directly changing production behavior.

## Packet shape

A packet should be a bounded work item, not a narrative report:

- `source`: profile/cron/script name that found the issue
- `scope`: affected profile, cron, repo path, or workflow lane
- `classification`: one of `low-risk-fix`, `needs-human-approval`, `security-sensitive`, `customer/team-facing`, `blocked`
- `evidence`: exact file paths, cron IDs, log snippets, test names, or message IDs needed to verify the claim
- `proposed_change`: concrete change in one or two sentences
- `risk`: what could break if wrong
- `rollback`: how to undo it
- `dedupe_key`: stable key based on source + affected object + issue class
- `cooldown`: when the same packet may be sent again if still unresolved
- `requested_owner`: default profile, a specialist profile, or the owner

## Sending helper (if you build one)

No helper script ships with this skill. If you write one, give it these properties:

- A dry-run mode that prints the packet and does not create cooldown state; live sends require an explicit flag.
- Per-packet-type required fields, enforced with a non-zero exit when missing. Suggested types: `help` (reporter-only observer found something it cannot fix: task, evidence checked, why blocked, requested next step), `decision` (one or more options), `resolved` (resolution and action taken), `unresolved` (task the agent started and got blocked on, with why blocked).
- Separate "mention the supervisor" from "route to a chat"; a mention does not change the destination.

Packet-type routing convention: use `help` (not `unresolved`) when the source is a reporter-only observer that cannot act on its own findings.

## Dedupe rules

- Build the dedupe key from stable identifiers, not message text: e.g. `<source>|<profile>:cron:<job-id>|delivery-route-error`.
- Check recent packets or the review-bus log before sending. If an unresolved packet with the same key exists, update/append evidence locally instead of posting a new bus message.
- Use a cooldown for persistent conditions. Re-send only when the evidence materially changes, the severity increases, or the cooldown expires.
- Avoid bot loops: send one packet to the supervisor/default bot; do not invite a freeform multi-bot conversation.

## Escalation boundary

- Low-risk behavior-preserving fixes can be applied by the default reviewer and summarized later.
- Workflow-changing, customer/team-facing, permission/security, secrets/auth/provider, gateway allowlist, or live-write changes need plan + risks + rollback and the owner/default approval before action.

## Verification expectations

Before marking a packet resolved, verify the fix with the smallest relevant test or probe. Include the verification command or tool result in the resolution note so future observers can distinguish fixed issues from stale silence.
