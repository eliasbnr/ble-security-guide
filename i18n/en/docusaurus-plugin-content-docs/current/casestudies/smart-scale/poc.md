---
sidebar_position: 3
title: "Proof of Concept"
---

# Smart Scale - PoC

## Passive Scanner

```python
def on_scan(sender, report):
    mfr_data = report.advertise_data.manufacturer_specific_data
    if not mfr_data:
        return
    
    if mfr_data[0:2] == bytes([0xC0, 0x05]):  # Yolanda
        weight = int.from_bytes(mfr_data[2:4], 'big') / 100
        print(f"Weight: {weight} kg")

ble.scanner.on_scan_received.register(on_scan)
ble.scanner.start_scan()
```

## Demo Output

```
⚖️  Yoda1 @ XX:XX:XX:XX:XX:XX
   Weight: 78.50 kg
```
