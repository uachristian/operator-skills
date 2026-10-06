# API product-gap and survey audits

Use this pattern when the owner already has API access and asks what the vendor should improve, especially when the deliverable is a short survey response. This is different from a capability audit: the goal is to distinguish limitations in the vendor's public API from features that exist but are not wrapped locally or are intentionally disabled for safety.

## Workflow

1. Inventory the current public documentation from its live index/homepage; do not rely only on a prior endpoint list.
2. Parse rendered page text when methods and paths are separated by HTML tags. Raw regex over page HTML can falsely return zero endpoints.
3. Compare workflows, not just endpoint names: create, read, update, delete, lifecycle transitions, bulk operations, attachments, history/audit, reporting/export, and event/webhook recovery.
4. Recheck the vendor's webhook guide before claiming signatures, retries, diffs, delivery history, or replay are missing.
5. Classify every finding as:
   - missing or incomplete in the vendor's public API;
   - documented by the vendor but not yet wrapped locally;
   - intentionally unexposed locally for privacy, security, or approval reasons.
6. Validate the highest-value claims against both docs and safe live probes when possible; avoid write tests unless explicitly approved.
7. Draft the requested concise answer only after the classification pass. Prefer specific operational gaps over a long endpoint wishlist.

## False-positive guard

Do not describe a capability as absent merely because the local connector lacks a tool for it. Search the current docs for alternate endpoint families (for example integration/search, shared/public-order, or nested-resource routes), and distinguish UI-only recovery from API-accessible recovery.
