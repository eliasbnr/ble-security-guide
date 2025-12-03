---
sidebar_position: 6
title: "Findings"
---

# LED Glasses - Findings

## F-001: Hardcoded AES Key

**CVSS: 9.8 (Critical)**

The AES-128 key is hardcoded in the native library, identical for all devices.

```
Key: 34522a5b7a6e492c08090a9d8d2a23f8
```

### Impact

- Attacker can decrypt all communication
- Send arbitrary commands
- One extracted key compromises ALL devices worldwide

### Remediation

- Derive per-device keys from pairing
- Use Key Derivation Function (KDF)
