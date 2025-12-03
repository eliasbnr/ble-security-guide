---
sidebar_position: 5
title: "Findings"
---

# LED Strips - Findings

## F-001: Hardcoded XOR Key

**CVSS: 9.8 (Critical)**

XOR key is hardcoded in the app, identical for all devices.

## F-002: Trivial Encryption

XOR provides **no real protection**:
- Instantly decryptable with known key
- No brute-force needed
- Byte 0 not encrypted (known-plaintext)

## Recommendations

1. Use real encryption (AES-GCM)
2. Per-device keys from pairing
3. BLE Security Level 2+
