# Evidence Capture Guide

All examples in this repository are portfolio scenarios. Only label a step “performed” when you personally did it on a device or VM you control. Otherwise label it “proposed simulation.” Do not use employer/customer systems without written authorization.

## Networking

On a disposable guest VM, record Windows edition/build, adapter status, `ipconfig` summary, gateway reachability, DNS lookup result, and the final verification. Redact IP/MAC, hostnames, usernames, SSIDs, and domain names before publication. Avoid broad network reset as an early step; it can reset adapters and affect VPN/virtual-switch settings.

Microsoft guidance: [Wi-Fi troubleshooting](https://support.microsoft.com/en-us/windows/experience/connectivity-networking/fix-wi-fi-connection-issues-in-windows), [Ethernet troubleshooting](https://support.microsoft.com/en-us/windows/experience/connectivity-networking/fix-ethernet-connection-problems-in-windows), [wireless report details and privacy](https://support.microsoft.com/en-us/windows/experience/connectivity-networking/analyze-the-wireless-network-report).

## Peripherals and Device Manager

For a device you own, document Device Manager device status/error code, connection/power/cable/port check, driver provider/version if relevant, and successful functional test. In VMs, devices may be virtual or unavailable unless explicitly passed through. Prefer Windows Update or the manufacturer’s official driver page; don’t use third-party driver utilities.

Microsoft guidance: [Device Manager error codes](https://support.microsoft.com/en-us/windows/hardware/drivers/error-codes-in-device-manager-in-windows), [driver updates](https://support.microsoft.com/en-us/windows/update-drivers-through-device-manager-in-windows-ec62f46c-ff14-c91d-eead-d7126dc1f7b6), [USB-C troubleshooting](https://support.microsoft.com/en-us/windows/hardware/usb/fix-usb-c-problems-in-windows).

## BitLocker / security posture

`manage-bde -status C:` is an observation-only check. If you include output, redact recovery information, device identifiers, and organizational policy details. Don’t enable encryption, suspend protection, modify protectors, or delete keys for a demo. If a real support action is authorized, follow the organization’s escalation and recovery-key process first.

Microsoft guidance: [manage-bde status](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/manage-bde-status), [BitLocker overview](https://support.microsoft.com/en-us/windows/security/encryption/bitlocker-drive-encryption), [recovery key backup](https://support.microsoft.com/en-us/windows/security/encryption/back-up-your-bitlocker-recovery-key).

## Lifecycle exercises

The onboarding/offboarding CSV is intentionally fictional. Approval and retention gates are explicit; rows say “not executed” for live account/device actions. Do not disable real accounts, remove licenses, wipe or reassign devices, or send equipment. For a genuine organization, only approved administrators execute the current policy.
