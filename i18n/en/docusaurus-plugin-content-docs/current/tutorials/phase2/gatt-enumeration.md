---
sidebar_position: 1
title: "GATT Enumeration"
---

# GATT Enumeration

Connect to the device and enumerate the GATT structure.

## blatann Script

```python
peer = ble.connect(target).wait()
peer.discover_services().wait()

for service in peer.database.services:
    print(f"Service: {service.uuid}")
    for char in service.characteristics:
        print(f"  Char: {char.uuid} @ {char.value_handle}")
```

---

:::tip Next Step
Continue with [Characteristic Testing](./characteristic-testing).
:::
