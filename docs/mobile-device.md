# Mobile Device & Android Bare-Metal AI Agent Security Review 📱🛡️

> Contributed to SlowMist Agent Security Framework by Bare-Metal AI Agent Research (`@kxx2026`).  
> Aligned with SlowMist Core Principle: **Every external input and host environment is untrusted until verified.**

---

## Trigger

- Agent operates on or controls a physical Android device (via ADB, Termux, Accessibility Service, or UIAutomator)
- Agent handles Web3 transactions, seed phrases, or sensitive clipboard operations on mobile endpoints
- Agent is requested to automate actions across third-party Android APKs or mobile web views

---

## Review Flow

### Step 1: Environment & Hardware Trust Verification

| Check | How | Threat Mitigated |
| :--- | :--- | :--- |
| **Physical Hardware Fingerprint** | Verify `ro.product.model`, `ro.product.brand`, baseband & real battery sensors | Cloud emulator detection / Sybil farm risk |
| **Root & Debugger State** | Check `su` binary existence, SELinux enforcing status, USB debugging exposure | Unauthorized privilege escalation |
| **Outbound IP Reputation** | Verify ASN, residential/commercial ISP rating, and fraud score | IP blacklisting & geolocation poisoning |

**Red flags at this stage:**
- Running in untrusted emulators (LDPlayer, BlueStacks) for financial operations without device attestation.
- Insecure open ADB listening over public 0.0.0.0 network interfaces without TLS/auth keys.

---

### Step 2: Mobile Attack Surface Audit

#### 1. Clipboard Hijacking (Address Replacement Attack)
* **Risk Level**: **CRITICAL**
* **Attack Vector**: Android background Trojan monitoring `ClipboardManager` and substituting copied Web3 addresses (ETH / BTC / SOL) with attacker's address.
* **Agent Rule**:
  - Never blindly paste clipboard content into transaction recipients.
  - Implement two-way checksum comparison between source address memory and target input before broadcasting.

#### 2. Accessibility Service Hijacking (`BIND_ACCESSIBILITY_SERVICE`)
* **Risk Level**: **HIGH**
* **Attack Vector**: Malicious APKs abusing Accessibility Services to scrape UI node trees, steal 2FA OTPs from SMS/Auth apps, or inject synthetic touch events.
* **Agent Rule**:
  - Audit all active accessibility services (`settings get secure enabled_accessibility_services`).
  - Flag any non-system accessibility services running alongside Agent operations.

#### 3. Overlay Attack (`SYSTEM_ALERT_WINDOW`)
* **Risk Level**: **HIGH**
* **Attack Vector**: Transparent floating window placed over genuine wallet/login screens to capture keystrokes or trick user into clicking approve.
* **Agent Rule**:
  - Inspect top-level window hierarchy (`dumpsys window`) to verify genuine target package focus before submitting credentials.

---

### Step 3: Outbound Data & Privacy Guard Baseline

For any outbound action (posting to social, sending API payloads, writing logs), apply hard regex enforcement:

1. **Private Keys & Seed Phrases**: Immediate redaction of 64-hex strings (`0x...`) and 12/24 BIP-39 mnemonic wordlists.
2. **Internal Infrastructure**: Redact RFC 1918 private IPs, Tailscale CGNAT IPs (`100.64.0.0/10`), and hardware identifiers (IMEI/MAC).
3. **Execution Block**: Any unredacted sensitive match triggers hard `SecurityViolationError` terminating the dispatch.

---

## Implementation Reference (Python / ADB)

See reference defense implementation in `mobile_agent_kit`:
- [mobile_agent_kit/web3_guard.py](https://github.com/kxx2026/MobileAgentKit)
- [mobile_agent_kit/guard.py](https://github.com/kxx2026/MobileAgentKit)
