---
sidebar_position: 5
title: "Findings"
---

# LED Strips - Findings

## F-001: Hardcoded XOR Key

**CVSS: 9.8 (Critical)**

```
Vector: CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H
```

Der XOR-Key ist fest in der App einprogrammiert:
```java
byte[] key = {89, 76, 90, 75, 53, 49, ...};
```

## F-002: Trivial Encryption (XOR)

**CVSS: 9.1 (Critical)**

XOR bietet **keinen echten Schutz**:
- Mit bekanntem Key sofort entschlüsselbar
- Kein Brute-Force nötig
- Byte 0 nicht verschlüsselt (Known-Plaintext)

## F-003: No BLE Authentication

**CVSS: 8.8 (High)**

- Kein Pairing erforderlich
- Keine Security Level auf Characteristics
- Jeder kann sich verbinden

## Empfehlungen

1. **Echte Verschlüsselung** (AES-GCM)
2. **Per-Device Keys** aus Pairing
3. **BLE Security Level 2+**
