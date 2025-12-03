---
sidebar_position: 6
title: "Pairing Mechanisms"
---

# Pairing Mechanisms

## Association Models

| Model | MITM-Schutz | Use Case |
|-------|-------------|----------|
| Just Works | ❌ | Headless devices |
| Passkey Entry | ✓ | Display + Keyboard |
| Numeric Comparison | ✓ | Two displays |
| OOB | ✓ | NFC, QR-Code |

## Legacy vs. LE Secure Connections

**Legacy** (BLE 4.0-4.1):
- TK-basiert
- MITM bei Just Works möglich

**LE Secure Connections** (BLE 4.2+):
- ECDH-basiert
- P-256 Kurve
- Stärker gegen MITM
