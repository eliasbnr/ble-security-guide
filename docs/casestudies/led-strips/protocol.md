---
sidebar_position: 2
title: "Protokoll-Analyse"
---

# LED Strips - Protokoll

## Paketstruktur

```
┌──────┬────────┬─────────┬──────────┬──────┐
│ 0x7E │ Length │ Command │ Payload  │ 0xEF │
│ (1B) │  (1B)  │  (1B)   │ (var)    │ (1B) │
└──────┴────────┴─────────┴──────────┴──────┘
```

## Command Reference

| Command | Opcode | Payload | Beschreibung |
|---------|--------|---------|--------------|
| Power | 0x04 | state | Ein (0x01) / Aus (0x00) |
| Color | 0x05 | R,G,B | RGB-Werte (0-255) |
| Brightness | 0x01 | level | Helligkeit (0-100) |
| Effect | 0x03 | mode | Effekt-Modus |

## Beispiel-Commands (vor Verschlüsselung)

```python
# Power On
[0x7E, 0x04, 0x04, 0x01, 0x00, 0x01, 0xFF, 0x00, 0xEF]

# Set Color Red (255, 0, 0)
[0x7E, 0x07, 0x05, 0x03, 0xFF, 0x00, 0x00, 0x10, 0xEF]

# Brightness 50%
[0x7E, 0x04, 0x01, 0x32, 0xFF, 0xFF, 0xFF, 0x00, 0xEF]
```
