---
sidebar_position: 3
title: "UUID Extraction"
---

# UUID Extraction

Systematisches Extrahieren aller UUIDs aus der APK.

## Automatische Extraktion

```bash
# Alle UUID-Patterns in dekompiliertem Code finden
grep -rEo "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}" sources/
grep -rEo "0x[0-9a-fA-F]{4}" sources/ | grep -i uuid
```

## Kategorisierung

| UUID | Typ | Standard? | Beschreibung |
|------|-----|-----------|--------------|
| 0x1800 | Service | ✓ | Generic Access |
| 0xFFF0 | Service | ✗ | Custom |
| 0xFFF3 | Char | ✗ | Custom Write |

---

:::tip Nächster Schritt
Weiter zur [Crypto Analysis](./crypto-analysis).
:::
