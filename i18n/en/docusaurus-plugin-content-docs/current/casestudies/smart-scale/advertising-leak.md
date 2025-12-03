---
sidebar_position: 2
title: "Advertising Leak"
---

# Smart Scale - Advertising Analysis

## Manufacturer Data

```python
def decode_weight(manufacturer_data):
    # Skip Company ID (first 2 bytes)
    weight_bytes = manufacturer_data[2:4]
    weight_raw = int.from_bytes(weight_bytes, 'big')
    weight_kg = weight_raw / 100
    return weight_kg

# Example
data = bytes.fromhex("c005780012c4")
weight = decode_weight(data)  # 78.50 kg
```

## Privacy Violation

- Weight visible to ANYONE in 10m range
- NO connection required
- Purely PASSIVE eavesdropping
- Tracking via MAC address possible
