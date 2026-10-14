# IT Support & Asset Lifecycle Runbook (Simulated Lab)

**All names, tickets, assets, dates, shipping IDs, and events in this lab are invented.** This is a portfolio simulation, not Garland work, employer experience, or a record of physical repairs or shipments. No real account/device was provisioned, disabled, wiped, or shipped.

## Ticket lifecycle / evidence form

1. **Intake:** record ticket ID, request time/channel, user-reported symptoms (not a guessed cause), affected asset tag, impact, urgency, priority, and callback preference in the internal system.
2. **Triage:** confirm identity with approved process; check known outage/knowledge article; ask scope, onset, error text, recent changes, and reproducibility. Never request a password, MFA code, or recovery key.
3. **Diagnose:** choose a least-invasive, reversible check first. Record action and result, not just “fixed.” Do not make policy, admin, registry, encryption, or security exceptions without authorization.
4. **Resolve / escalate:** verify with requester or documented test; explain next steps in plain language. Escalate security incidents immediately through the incident procedure; preserve evidence and do not investigate beyond authorization.
5. **Close:** record category, priority, resolution code, actual resolution, elapsed duration, user update, linked asset, and any follow-up owner. Reopen if verification fails.

### Ticket note template

- Symptom / impact / scope:
- Asset tag and user verification (no sensitive data):
- Checks and results (timestamped):
- Change made / approval reference:
- Verification with requester:
- Resolution / next owner / next update:

## Workstation setup checklist (fictional handoff)

- Confirm approved request, role, start date, manager, and asset allocation.
- Inventory tag, model, serial in controlled system, condition, accessories, and custody record.
- Validate approved image/build, patch state, endpoint protection, encryption status, and required software using organization procedures.
- Verify network and sign-in with a test account only when authorized; do not put credentials in ticket notes.
- Record device handoff, user orientation, support contact, and acceptance timestamp.
- Check returned peripherals, condition, stock location, and asset ledger updates.

## Onboarding / offboarding gates

Onboarding requires approval and role/access-owner validation before account or entitlement creation. Offboarding requires approved effective time, access owner, data-retention decision, custody/return tracking, and authorized executor. The CSV examples deliberately keep privileged actions marked “not executed” or blocked until approvals. No real account, license, recovery key, data, or hardware is changed here.

## Shipping / receiving evidence

Record request/reference, destination site (not home addresses in this portfolio), packaged asset tags, accessory list, fictional carrier reference, dispatch/receipt timestamps, condition on receipt, chain-of-custody acknowledgements, and discrepancy/next owner. Here tracking strings begin `SHIP-SIM` and are not real shipment identifiers.

## Escalation boundaries

- Suspected malware, exposed credentials, data loss, or account compromise: stop routine troubleshooting, use the security incident process, preserve evidence, notify the designated lead.
- Encryption/recovery, administrator privilege, production configuration, safety, warranty repair, or data-retention actions: obtain approved owner direction; do not improvise.
- Hardware opening/repair: only authorized and trained personnel, per warranty and safety guidance. This portfolio project performs no physical repair.
