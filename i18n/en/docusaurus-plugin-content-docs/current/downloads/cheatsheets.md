---
sidebar_position: 4
title: "Cheatsheets"
---

# Cheatsheets

## Wireshark Filters

```
btle                     # All BLE
btatt                    # ATT Protocol
btatt.opcode == 0x12     # Write Request
btatt.opcode == 0x1b     # Notification
```

## blatann Quick Reference

```python
ble = BleDevice("/dev/ttyACM0")
ble.configure()
ble.open()
peer = ble.connect(addr).wait()
peer.discover_services().wait()
```
