---
sidebar_position: 7
title: "Encryption"
---

# BLE Encryption

## Link Layer Encryption

- **Algorithmus**: AES-CCM
- **Key Size**: 128 bit
- **Mode**: Counter with CBC-MAC

## Key Hierarchy

```
LTK (Long Term Key)
  └── Session Key
        └── Encrypted Link
```

## Bekannte Schwächen

- **KNOB**: Key Entropy Reduction
- **BLESA**: Reconnection Spoofing
