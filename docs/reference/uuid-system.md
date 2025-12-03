---
sidebar_position: 4
title: "UUID System"
---

# UUID System

UUIDs identifizieren Services, Characteristics und Descriptors.

## 16-bit vs 128-bit

**16-bit** (Bluetooth SIG reserviert):
```
0x1800 → Generic Access
0x180F → Battery Service
```

**128-bit** (Custom):
```
d44bc439-abfd-45a2-b575-925416129600
```

## Konvertierung

```
Base UUID: 00000000-0000-1000-8000-00805F9B34FB
16-bit:    0xABCD
128-bit:   0000ABCD-0000-1000-8000-00805F9B34FB
```
