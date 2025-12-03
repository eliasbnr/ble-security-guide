---
sidebar_position: 3
title: "Verschlüsselung"
---

# LED Strips - XOR "Verschlüsselung"

## Extrahierter Key

Aus JADX-Analyse der `EncryptUtil.java`:

```java
private static byte[] key = {
    89, 76, 90, 75, 53, 49, 33, 41, 62, 72, 64,
    118, 100, 98, 81, 68, 94, 68, 63
};
```

## Verschlüsselungs-Algorithmus

```python
XOR_KEY = bytes([89, 76, 90, 75, 53, 49, 33, 41, 62, 72, 64,
                 118, 100, 98, 81, 68, 94, 68, 63])

def encrypt(data, counter):
    # Key = base_key + counter byte
    full_key = XOR_KEY + bytes([counter])
    
    result = bytearray(data)
    # XOR bytes 1-24 with full key
    for i in range(1, min(len(result), 25)):
        for k in full_key:
            result[i] ^= k
    
    return bytes(result)
```

## Schwächen

| Problem | Beschreibung |
|---------|--------------|
| XOR | Symmetrisch, mit bekanntem Key trivial |
| Hardcoded | Key identisch für alle Geräte |
| Counter | Vorhersagbar (0-255 zyklisch) |
| Byte 0 | Nicht verschlüsselt (immer 0x7E) |
