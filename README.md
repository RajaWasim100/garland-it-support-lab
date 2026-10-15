# Windows IT Support & Asset Lifecycle Lab

**Portfolio simulation for an entry-level onsite IT support role. All tickets, people, assets, dates, and shipping references are fictional. This is not Garland or employer work and does not claim physical hardware repairs or production account administration.**

The lab is designed to demonstrate repeatable support-ticket documentation, basic Windows/network/peripheral troubleshooting, endpoint security checks, equipment inventory, and onboarding/offboarding coordination—the task areas relevant to an onsite IT co-op. The scenario dataset is synthetic, not a real support queue. Only state an action was performed on your own device/VM if you actually did it; the supplied cases are scenario records.

## Portfolio contents

- `data/tickets.csv`: 30 fictional incidents/requests with symptom, priority, response/resolution time, resolution note, escalation/reopen flags, and linked asset.
- `data/assets.csv`: fictional 10 endpoint and 6 peripheral register rows; serial values use `SYN-` stubs.
- `data/lifecycle.csv`: simulated onboarding/offboarding with manager, access-review, retention, return, and shipping gates. Rows explicitly say no real administrative action occurred.
- `data/troubleshooting.csv`: clearly marked synthetic scenarios plus a dated personally performed Windows 11 VM NAT baseline/DHCP-renew exercise. That exercise found no connectivity fault and is not described as a repair. See `project/README.md` for factual observations; raw captures remain private and excluded.
- `src/build_report.py`, `sql/analysis.sql`, and `tests/`: validated data ingestion, SQLite evidence store, aggregate report and checks.
- `index.html`: responsive dashboard showing ticket themes, inventory posture, and lifecycle blockers.
- `project/README.md`: ticket-note template, setup/handoff, package handling, escalation boundaries, and factual account of the actual VM exercise.
- `project/evidence-log.csv`: dated observations; clearly separates the personally performed VM check from synthetic examples and notes unavailable tools.
- `docs/evidence/README.md`: safe evidence-capture practice and current Microsoft references.

## Run locally

Python 3.10+; standard library only.

```bash
python -m src.build_report
python -m unittest discover -s tests -v
python -m http.server 8000
```

Open `http://localhost:8000/`. The generated `reports/support-summary.json` is aggregate-only for the fictional scenario dataset; it does not include the separate actual VM evidence log. A private local SQLite store is created under `data/processed/` and is Git-ignored. Raw ticket-level scenario files remain in the repository because they are authored synthetic content, but individual ticket/requester/asset identifiers are never sent to the public dashboard/report. **Do not replace with real company/customer/device data.**

## What to show an interviewer

1. A ticket note distinguishing the user symptom from the diagnosed cause, timestamped checks, verification, resolution, and escalation owner.
2. A fictional asset register with model, tag, stub serial, location, warranty, custody/status, patch and encryption review state, and inventory check date.
3. The onboarding/offboarding approval gates, access owner and retention decision; actions on real accounts or devices were deliberately not executed.
4. A safe troubleshooting order: confirm scope, use reversible observation first, verify outcome, communicate clearly, escalate security/admin issues rather than bypassing controls.
5. The dashboard and reproducible tests, explicitly described as invented training data—not measured customer or SLA performance.

## Boundaries and evidence still to add

The recorded VM exercise is real but limited to baseline checks, a DNS cache flush, DHCP renew, and successful NAT gateway ping; it did **not** fix a fault. This project still does not prove physical equipment repair, printer-driver troubleshooting, a Windows Update/security remediation, shipping/receiving, corporate reporting knowledge, or ability to lift/carry equipment. Spiceworks, AD, and Nessus were not available in the checked environment; a 2026-10-15 readiness check found only about 1.89 GiB free host memory with the 6.3 GB VM running, so Nessus installation was deferred without attempting it. No ticket-platform, directory, or vulnerability-scan work is claimed. See the [readiness note](project/README.md#tool-installation-readiness--2026-10-15) and [evidence log](project/evidence-log.csv). Add further dated evidence only after personally performing each task on a device/account you own or are authorized to manage. Do not publish serials/recovery keys/IPs/usernames, change employer systems, create or disable real accounts, wipe devices, or ship equipment as a portfolio exercise.

For applicable Windows guidance and redaction reminders, see [Evidence Capture Guide](docs/evidence/README.md). All Microsoft references are learning resources; an employer's policies and approved procedures take precedence.
