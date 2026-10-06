# Mission handoff and worker ledger

Temporary authorized repo/task state, not persistent memory. No credentials, raw personal/customer text, or copied full transcripts.

- mission_id (stable):
- scope_revision (exact string):
- current candidate_id (exact source/artifact identity):
- Owner / approved outcome / non-goals / approval boundaries:
- Exact source paths and dirty/untracked ownership:
- Completed acceptance evidence, commands and exits:
- Required gates still open / required worker IDs:
- Long-running process owner/PID/generation and actual completion evidence:
- Rollback and next exact command:
- Budget used/remaining; blocked time separate from work:

## Worker/result ledger
| worker_id | required gate or optional lane | target revision/candidate | result_id | artifact path/hash | parent verified? | disposition/reason |
|---|---|---|---|---|---|---|

Allowed dispositions: CURRENT, UNVERIFIED, SUPERSEDED, ALREADY_INCORPORATED, WRONG_MISSION, INVALID. They classify relevance, not approval or release readiness. Do not drop required gates automatically. Optional workers are tracked separately from required-review obligations.

After a scope/candidate change, notify affected workers and update assignments; pause only dependent work. Classify every delayed result before action. Old security findings remain reproduction signals against current source. Record exact result identity only after parent verification/incorporation; never merely after delivery.

On resume, read current source/status and this handoff before old transcripts. Preserve useful partial work; do not replay completed commands or unchanged timeouts. Missing/mismatched metadata is UNVERIFIED/INVALID, not permission to guess.
