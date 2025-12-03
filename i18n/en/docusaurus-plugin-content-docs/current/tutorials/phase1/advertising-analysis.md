---
sidebar_position: 2
title: "Advertising Analysis"
---

# Advertising Analysis

Analyze the advertising packets to understand what the device broadcasts.

## Advertising Data Structure

```
┌─────────┬─────────┬──────────────┐
│ Length  │  Type   │    Data      │
│ (1 byte)│(1 byte) │ (Length-1)   │
└─────────┴─────────┴──────────────┘
```

## Common AD Types

| Type | Name | Description |
|------|------|-------------|
| 0x01 | Flags | Advertising flags |
| 0x09 | Complete Name | Device name |
| 0xFF | Manufacturer Data | Custom data |

## Privacy Leak Example

Real finding from Smart Scale:

```python
# Weight broadcast in clear text!
manufacturer_data = bytes.fromhex("c00578002c01")
company_id = int.from_bytes(manufacturer_data[0:2], 'little')
weight = int.from_bytes(manufacturer_data[2:4], 'big') / 100
print(f"Weight: {weight} kg")  # 120.0 kg
```

---

:::tip Next Step
Continue with [Wireshark Capture](./wireshark-capture).
:::
