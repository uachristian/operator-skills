# Classifier comparison and agreement-gate recipe

Use when the owner wants a cheaper/faster model  evaluated against an existing production classifier , or wants that classifier made more accurate.

## 1. Pick the target
- Inventory every cron (all profiles' `cron/jobs.json`) and note which steps already call an LLM with a small fixed label set. Those are the fits for a fast choice model; text-writing, money/date/AR logic, and private-message work are not.
- Private data (texts, customer records) stays on the local model regardless of speed. Hosted-model data exposure needs explicit owner approval; state exactly which fields will be sent.

## 2. Shadow + backfill (read-only)
- Script in default's `~/.hermes/scripts/`, reading the specialist's queue read-only, sending only minimized fields (sender display name + domain, subject; never mailbox local part or body), appending to a 0600 log under `~/.hermes/state/experiments/<topic>/`.
- Daily call cap; stdout silent except when every call in a run fails (no-agent cron delivers stdout).
- Backfill ~1 month at once (a few hundred items, minutes) instead of waiting weeks for live data.

## 3. Gold set and scoring
- Label by deterministic subject/domain rules first, then hand-label the remainder and every disagreement; allow multi-label acceptable sets for real ambiguity. Save it (e.g. `gold_v1.json`).
- Score incumbent and candidate overall, on non-trivial classes (exclude the bulk marketing class, which inflates everything), and on an even/odd-id holdout.

## 4. Fix definitions, then compare fairly
- Rewrite category definitions from the disagreement pairs (explicit inclusions, "only for our own domain" for internal, narrow "unknown").
- Rerun BOTH models with the same definitions and minimized inputs. Report the table: old incumbent / candidate old defs / candidate new defs / incumbent new defs / agreed-subset accuracy / share routed to review / incumbent errors caught by disagreement.

## 5. Install (owner-approved)
- One shared definitions dict feeds the incumbent prompt and the candidate criteria.
- Candidate called in parallel with a short timeout; invalid answer = no answer.
- Gate: downgrade to review on disagreement with reason `second_opinion_disagreement <cat>`; never upgrade; candidate outage = old behavior.
- Timestamped backup + sha256, scratch candidate, tests (gate truth table, minimization leak check, outage paths, one live call; add the profile scripts dir to sys.path so sibling imports resolve), atomic install under the job's own non-blocking process lock, hash + fresh import verification.
- Remove the shadow cron; capture the change to the vault with eval numbers and rollback path.
- Watch the next scheduled run. A run with no new items does not exercise the new path — report that honestly instead of claiming verification.
