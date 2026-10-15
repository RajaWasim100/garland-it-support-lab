# Charter — Windows IT Support & Asset Lifecycle Lab

**Status:** mixed-evidence portfolio lab. No Garland or employer participation. The original ticket/asset/lifecycle examples remain fictional; a small dated Windows VM exercise is separately identified as personally performed lab work.

## Objective
Demonstrate entry-level IT support behaviors relevant to an onsite co-op: structured ticket notes, basic endpoint/network/peripheral troubleshooting, asset tracking, security posture awareness, lifecycle coordination, user communication, and careful escalation.

## Deliverables
- Synthetic ticket, endpoint/peripheral register, and lifecycle request examples, plus a separately labeled factual record of one user-owned Windows VM baseline exercise.
- Standard-library data validation and local SQLite evidence store.
- Aggregate JSON report for synthetic records, SQL examples, responsive dashboard, tests, evidence-capture guidance, runbook, and a separate dated record of personally performed VM baseline checks.

## In scope
- Fictional user scenarios with timestamps, asset links, priorities, response/resolution notes, escalation and reopen flags; real VM checks are not mixed into their fabricated KPI dataset.
- Mock onboarding/offboarding approvals, inventory, patch/encryption review, shipping receipt checkpoints.
- Safe troubleshooting sequence in a personally controlled VM; only directly observed commands/results are marked performed. No physical repair is inferred.

## Out of scope and controls
- No real Garland/customer/employer data, people, equipment, accounts, network, security portal, shipment, or claims of employment experience.
- No account create/disable, privilege grant, license removal, wipe, BitLocker protector change, data deletion, actual shipping, or hardware opening.
- No SLA claims from the illustrative ticket times; they are invented test values.

## Acceptance criteria
- Pipeline validates required fields, timestamps, durations, booleans, and ticket-to-asset references.
- Synthetic aggregate report contains no ticket, requester, asset, serial, shipment IDs, or free-text notes; actual VM evidence is kept separate and redacted before public release.
- SQLite database, secrets, and any future actual evidence stay ignored/private.
- Dashboard works from a local HTTP server, with an explicit simulation disclaimer.
- Tests cover expected counts, invalid records, referential integrity, output privacy, and SQL query execution.
