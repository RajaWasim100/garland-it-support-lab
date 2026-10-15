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

## Personally performed VM exercise — 2026-10-14

A condensed evidence index is maintained in [`evidence-log.csv`](evidence-log.csv). This factual record is separate from synthetic `LAB-*` ticket data and is not counted in its dashboard or metrics.

This section records one real, low-risk activity performed in the owner's own Windows 11 Pro VirtualBox 7.2.4 VM, which was on NAT. A VirtualBox snapshot named `Pre-Garland-Support-Lab-20261014` was taken before continuing. The VM had been previously used for a separate lab; guest account credentials were not entered into this portfolio. The VM did not have VirtualBox Guest Additions available, so host-side guest-control collection was unavailable. The exercise is specifically a VM network-baseline/DHCP-renew check; it is not evidence of a broken adapter or a user-reported outage.

**Ticket VM-2026-10-14-01 — Verify guest connectivity**

- Observation: `ipconfig` showed a guest IPv4 lease, `/24` mask, and default gateway on the VirtualBox NAT network (exact addresses redacted from this write-up).
- Test: pinged the observed NAT gateway once; one reply, 0% packet loss. (The address is omitted from this write-up.) Gateway reachability was healthy; no connectivity fault was present.
- Action: ran `ipconfig /flushdns` (Windows reported success), then `ipconfig /renew` in the VM. No host or shared network settings were touched.
- Verification: guest retained its IPv4 lease; a post-action ping to the same NAT gateway returned one reply and 0% loss.
- Outcome: successful baseline check and reversible DHCP renew, **not a repair**. The initial gateway ping already passed before the change; renew retained the same lease and post-change ping passed. The exercise does not establish DNS failure or resolve a reported service incident.
- Disclosure: VM addresses and desktop captures are omitted from the tracked note. Raw screenshots/video remain private; redact addresses and crop personal desktop items before any public reuse.
- Evidence: VirtualBox console showed the guest address, gateway, successful gateway ping and post-renew ping. A VM screenshot/video was captured locally for personal review. Keep raw captures private: the VM desktop shows personal app shortcuts and internal addresses. Do not commit them; this project ignores screenshots/video.

**Ticket VM-2026-10-14-02 — Flush guest DNS cache**

- Action/result: `ipconfig /flushdns`; Windows confirmed `Successfully flushed the DNS Resolver Cache.`
- Scope: cache maintenance only; no DNS fault was observed and no before/after name-resolution defect was demonstrated. Do not describe this as fixing a DNS incident.

These entries are personally performed lab exercises; all other `LAB-*` tickets remain synthetic scenarios. No Spiceworks, Active Directory, or Nessus operations were performed. The VM has a rollback snapshot; restore only when needed and after preserving any privately needed evidence.

## Tool-installation readiness — 2026-10-15

A read-only readiness check found the VM still running with 6,345 MB assigned, 4 virtual CPUs, and NAT networking; host free physical memory was about 1.89 GiB. Guest Additions were unavailable, so host-side guest-control operations could not inspect or manage the guest. Nessus installation was **deferred, not attempted**: installing and initializing a scanner under this host-memory headroom could destabilize the running VM or host. Tenable lists 4 GB RAM as a minimum and 8 GB as recommended for a Nessus scanner ([hardware requirements](https://docs.tenable.com/general-requirements/Content/NessusScannerHardwareRequirements.htm)); its first startup also compiles plugins. There is no separate AD domain-controller lab in this environment, and no Spiceworks or Nessus service was installed. No account was created, installer downloaded, or scan run. These are blockers, not completed tool experience.

Before trying again, provide substantially more free host memory, a recoverable VM snapshot, and an authorized installation/activation path; verify the installed tool and plugin readiness before any scan, and use only authorized targets.

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
