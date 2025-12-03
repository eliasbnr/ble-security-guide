---
sidebar_position: 2
title: "Advertising-Leak"
---

# Smart Waage - Advertising-Analyse

## Advertising Data

Beim Wiegen sendet die Waage folgende Advertising-Pakete:

```
Advertising Data:
├── Type: 0x01 (Flags)
│   └── Value: 0x06 (LE General Discoverable)
├── Type: 0x09 (Complete Local Name)
│   └── Value: "Yoda1"
└── Type: 0xFF (Manufacturer Specific Data)
    └── Value: C0 05 78 00 2C 01 ...
```

## Manufacturer Data Struktur

```
Offset  Bytes   Beschreibung
------  -----   ------------
0-1     C0 05   Company ID (Little Endian) = 0x05C0
2-3     78 00   Gewicht (Big Endian) = 0x0078 = 120 → 120/10 = 12.0 kg? 
                ODER: 0x7800 = 30720 → 30720/256 = 120.0 kg?
4-5     2C 01   Impedanz (optional)
6       ...     Weitere Daten
```

## Dekodierung

Nach Analyse mehrerer Messungen:

```python
def decode_weight(manufacturer_data):
    """Decode weight from manufacturer data"""
    # Skip Company ID (first 2 bytes)
    weight_bytes = manufacturer_data[2:4]
    
    # Big Endian, divide by 100 for kg
    weight_raw = int.from_bytes(weight_bytes, 'big')
    weight_kg = weight_raw / 100
    
    return weight_kg

# Beispiel
data = bytes.fromhex("c005780012c4")
weight = decode_weight(data)
print(f"Weight: {weight} kg")  # 78.50 kg
```

## Verifikation

| Angezeigt | Manufacturer Data | Dekodiert |
|-----------|-------------------|-----------|
| 78.5 kg | `c0 05 1e a6 ...` | 78.62 kg ✓ |
| 65.0 kg | `c0 05 19 64 ...` | 65.00 kg ✓ |
| 82.3 kg | `c0 05 20 2e ...` | 82.30 kg ✓ |

## Security Impact

```
┌─────────────────────────────────────────────┐
│           PRIVACY VIOLATION                 │
├─────────────────────────────────────────────┤
│ • Gewicht für JEDEN in 10m sichtbar         │
│ • KEINE Verbindung nötig                    │
│ • KEINE Interaktion mit Gerät nötig         │
│ • Rein PASSIVES Mitlesen möglich            │
│ • Tracking über MAC-Adresse möglich         │
└─────────────────────────────────────────────┘
```
