---
sidebar_position: 1
title: "Passive Scanning"
---

# Passive Scanning

The first phase of any BLE security assessment: **Collect information without active interaction**.

## Why Start Passive?

| Reason | Benefit |
|--------|---------|
| Undetected | Device doesn't know you're watching |
| No logs | No connection attempts recorded |
| Complete picture | See all advertising behavior |
| Privacy leaks | Find sensitive data in advertising |

## Scanning Methods

### 1. bluetoothctl (Recommended)

The modern method for Bluetooth LE scanning:

```bash
# Interactive
bluetoothctl
[bluetooth]# scan le
# Wait for results...
[bluetooth]# devices
[bluetooth]# info AA:BB:CC:DD:EE:FF
[bluetooth]# scan off
[bluetooth]# quit

# Or as one-liner
bluetoothctl scan le
```

### 2. hcitool (Legacy - Bluetooth 4.x only)

:::caution Deprecated
`hcitool` is **deprecated** and does **not work** with Bluetooth 5.x adapters!
With Bluetooth 5.x devices you'll get: `Set scan parameters failed: Input/output error`
Use `bluetoothctl scan le` instead.
:::

```bash
# Only for older Bluetooth 4.x adapters:
sudo hciconfig hci0 up
sudo hcitool lescan
```

### 3. blatann (Script-based)

```python
#!/usr/bin/env python3
"""
Passive BLE Scanner
Collects information without connecting
"""
import sys
import time
from blatann import BleDevice
from blatann.utils import setup_logger

def scan_passive(serial_port, duration=30):
    setup_logger(level="INFO")
    
    ble_device = BleDevice(serial_port)
    ble_device.configure()
    ble_device.open()
    time.sleep(1)
    
    devices = {}
    
    def on_adv(sender, report):
        addr = str(report.peer_address)
        adv = report.advertise_data
        
        # Collect information
        info = {
            "name": adv.local_name or report.device_name,
            "rssi": report.rssi,
            "services": [str(u) for u in adv.service_uuids],
            "manufacturer_data": adv.manufacturer_data.hex() if adv.manufacturer_data else None,
        }
        
        if addr not in devices:
            devices[addr] = info
            print(f"[NEW] {addr} | {info['name']} | RSSI: {info['rssi']}")
    
    ble_device.scanner.on_scan_received.register(on_adv)
    
    print(f"🔍 Passive scan ({duration}s)...")
    
    ble_device.scanner.set_default_scan_params(timeout_seconds=duration)
    ble_device.scanner.start_scan().wait(timeout=duration + 5)
    
    print(f"\n✅ {len(devices)} unique devices found")
    ble_device.close()
    return devices

if __name__ == "__main__":
    port = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyACM0"
    scan_passive(port)
```

## What to Look For

### Advertising Data

| Field | Security Relevance |
|-------|-------------------|
| **Local Name** | Device identification |
| **Manufacturer Data** | May contain sensitive data! |
| **Service UUIDs** | Hints at device capabilities |
| **TX Power** | Range estimation |

### Privacy Leaks

Many devices send **sensitive data** in advertising:

:::danger Example: Smart Scale
Some smart scales broadcast your **current weight** unencrypted in the advertising packet - visible to anyone in range!
:::

---

:::tip Next Step
Continue with [Advertising Analysis](./advertising-analysis).
:::
