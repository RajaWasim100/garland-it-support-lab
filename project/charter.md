# Charter — Windows IT Support & Asset Lifecycle Lab

**Status:** portfolio simulation. No Garland or employer participation. All operational records are fictional.

## Objective
Demonstrate entry-level IT support behaviors relevant to an onsite co-op: structured ticket notes, basic endpoint/network/peripheral troubleshooting, asset tracking, security posture awareness, lifecycle coordination, user communication, and careful escalation.

## Deliverables
- Small synthetic ticket, endpoint/peripheral register, lifecycle request register, and troubleshooting evidence log.
- Standard-library data validation and local SQLite evidence store.
- Aggregate JSON report, SQL examples, responsive dashboard, tests, evidence-capture guidance, and runbook.

## In scope
- Fictional user scenarios with timestamps, asset links, priorities, response/resolution notes, escalation and reopen flags.
- Mock onboarding/offboarding approvals, inventory, patch/encryption review, shipping receipt checkpoints.
- Safe simulated troubleshooting sequences; actual physical work is explicitly not inferred.

## Out of scope and controls
- No real Garland/customer/employer data, people, equipment, accounts, network, security portal, shipment, or claims of work experience.
- No account create/disable, privilege grant, license removal, wipe, BitLocker protector change, data deletion, actual shipping, or hardware opening.
- No SLA claims from the illustrative ticket times; they are invented test values.

## Acceptance criteria
- Pipeline validates required fields, timestamps, durations, booleans, and ticket-to-asset references.
- Aggregate report contains no ticket, requester, asset, serial, shipment IDs, or free-text notes.
- SQLite database, secrets, and any future actual evidence stay ignored/private.
- Dashboard works from a local HTTP server, with an explicit simulation disclaimer.
- Tests cover expected counts, invalid records, referential integrity, output privacy, and SQL query execution.
