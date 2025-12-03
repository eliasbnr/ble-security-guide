---
sidebar_position: 4
title: "blatann Setup"
---

# blatann Setup

**blatann** is a Python library for BLE communication with Nordic hardware. It enables professional PoC development.

## Installation

```bash
# In virtual environment
python3 -m venv ~/ble-security-env
source ~/ble-security-env/bin/activate

# Install blatann
pip install blatann
```

## Firmware for blatann

:::warning Important
blatann requires a **different firmware** than nRF Sniffer! You need to flash the Connectivity firmware.
:::

### Find Firmware

The firmware is installed with `pc-ble-driver-py`:

```bash
# Find firmware path
python3 -c "import pc_ble_driver_py; print(pc_ble_driver_py.__path__[0])"
# -> e.g.: ~/.local/lib/python3.10/site-packages/pc_ble_driver_py

# List firmware files (for blatann v0.3+)
ls ~/.local/lib/python3.10/site-packages/pc_ble_driver_py/hex/sd_api_v5/
```

### Select Firmware

| Hardware | Firmware |
|----------|----------|
| nRF52840 USB Dongle | `connectivity_x.y.z_usb_with_s132_x.y.hex` |
| nRF52840 Devkit (USB port) | `connectivity_x.y.z_usb_with_s132_x.y.hex` |
| nRF52840 Devkit (J-Link) | `connectivity_x.y.z_1m_with_s132_x.y.hex` |
| nRF52832 Devkit | `connectivity_x.y.z_1m_with_s132_x.y.hex` |

### Flash Firmware (nRF52840 Dongle)

```bash
# 1. Put dongle in bootloader mode
#    (Hold reset button while plugging in - LED pulses red)

# 2. Check port
ls /dev/ttyACM*

# 3. Create DFU package
FIRMWARE_PATH=$(python3 -c "import pc_ble_driver_py; print(pc_ble_driver_py.__path__[0])")/hex/sd_api_v5
FIRMWARE=$(ls $FIRMWARE_PATH/connectivity_*_usb_*.hex | head -1)

nrfutil pkg generate --hw-version 52 --sd-req 0x00 \
    --application "$FIRMWARE" \
    --application-version 1 \
    connectivity.zip

# 4. Flash
nrfutil dfu usb-serial -pkg connectivity.zip -p /dev/ttyACM0

# 5. After flashing: port may change!
ls /dev/ttyACM*
```

## Getting Started

### Verify Installation

```python
# test_blatann.py
import blatann
from blatann import BleDevice

print("✅ blatann successfully imported!")
print(f"   BleDevice: {BleDevice}")
```

### Initialize Device and Scan

```python
#!/usr/bin/env python3
"""
BLE Scanner with blatann - Complete Example
"""
import sys
import time
from blatann import BleDevice
from blatann.utils import setup_logger

def main():
    # Determine port
    port = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyACM0"
    
    # Enable logging (very helpful for debugging!)
    setup_logger(level="DEBUG")
    
    print(f"🔌 Connecting to {port}...")
    
    # Create and open BLE device
    ble_device = BleDevice(port)
    ble_device.configure()
    ble_device.open()
    
    # Wait briefly until device is ready
    time.sleep(1)
    
    print("🔍 Scanning for BLE devices (10s)...")
    print("-" * 60)
    
    found_devices = {}
    
    def on_scan_report(scanner, report):
        """Callback for each advertising report found"""
        addr = str(report.peer_address)
        if addr not in found_devices:
            name = report.advertise_data.local_name or "Unknown"
            found_devices[addr] = name
            print(f"[NEW] {addr} | {name} | RSSI: {report.rssi}")
    
    # Register callback
    ble_device.scanner.on_scan_received.register(on_scan_report)
    
    # Start scan and wait for completion
    try:
        ble_device.scanner.set_default_scan_params(
            interval_ms=200,
            window_ms=150,
            timeout_seconds=10,
            active_scanning=True
        )
        waitable = ble_device.scanner.start_scan()
        waitable.wait(timeout=15)  # Slightly more than scan timeout
    except Exception as e:
        print(f"❌ Scan error: {e}")
    finally:
        ble_device.close()
    
    print("-" * 60)
    print(f"✅ {len(found_devices)} devices found")

if __name__ == "__main__":
    main()
```

### Connect to Device

```python
#!/usr/bin/env python3
"""
BLE Connection with blatann
"""
import sys
import time
from blatann import BleDevice
from blatann.utils import setup_logger

TARGET_NAME = "GLASSES-12B008"  # Adjust!

def main():
    port = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyACM0"
    setup_logger(level="INFO")
    
    ble_device = BleDevice(port)
    ble_device.configure()
    ble_device.open()
    time.sleep(1)
    
    # Search for target device
    target_address = None
    
    def on_scan_report(scanner, report):
        global target_address
        name = report.advertise_data.local_name
        if name and TARGET_NAME in name:
            target_address = report.peer_address
            print(f"✅ Found: {target_address} ({name})")
            scanner.stop()
    
    ble_device.scanner.on_scan_received.register(on_scan_report)
    
    print(f"🔍 Searching for '{TARGET_NAME}'...")
    try:
        ble_device.scanner.start_scan().wait(timeout=15)
    except:
        pass  # Timeout is OK if device found
    
    if not target_address:
        print("❌ Device not found")
        ble_device.close()
        return
    
    # Connect
    print(f"🔗 Connecting to {target_address}...")
    try:
        peer = ble_device.connect(target_address).wait(timeout=10)
        print("✅ Connected!")
        
        # Discover services
        print("📋 Discovering services...")
        peer.discover_services().wait(timeout=20)
        
        # List services
        for service in peer.database.services:
            print(f"\nService: {service.uuid}")
            for char in service.characteristics:
                props = []
                if char.readable: props.append("READ")
                if char.writable: props.append("WRITE")
                if char.subscribable: props.append("NOTIFY")
                print(f"  └─ {char.uuid} [{', '.join(props)}]")
        
        # Disconnect
        peer.disconnect().wait(timeout=5)
        print("\n✅ Disconnected")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        ble_device.close()

if __name__ == "__main__":
    main()
```

## GATT Operations

### Read Characteristic

```python
# After Service Discovery...
char = peer.database.find_characteristic("d44bc439-abfd-45a2-b575-92541612960a")

if char and char.readable:
    result = char.read().wait(timeout=5)
    print(f"Read: {result.value.hex()}")
```

### Write Characteristic

```python
# Prepare data
data = bytes([0x01, 0x02, 0x03])

# Write (with response)
if char.writable:
    char.write(data).wait(timeout=5)

# Write without response (faster, for Write Command)
char.write(data, with_response=False)
```

### Receive Notifications

```python
import time

def on_notification(char, event_args):
    print(f"📥 Notification: {event_args.value.hex()}")

# Find notification characteristic
notify_char = peer.database.find_characteristic("d44bc439-abfd-45a2-b575-925416129601")

if notify_char and notify_char.subscribable:
    # Enable notifications
    notify_char.subscribe(on_notification).wait(timeout=5)
    
    # Wait for notifications
    print("⏳ Waiting for notifications (10s)...")
    time.sleep(10)
    
    # Disable
    notify_char.unsubscribe().wait(timeout=5)
```

## Troubleshooting

### "TimeoutError: Timed out waiting for event to occur"

**Causes:**
1. **Wrong firmware** - blatann needs Connectivity firmware, not Sniffer firmware
2. **Wrong port** - Port can change after firmware flash
3. **Device not ready** - Add `time.sleep(1)` after `open()`
4. **No BLE devices in range**

```bash
# Check port
ls /dev/ttyACM*

# Test with DEBUG logging
python3 -c "
from blatann import BleDevice
from blatann.utils import setup_logger
setup_logger(level='DEBUG')
d = BleDevice('/dev/ttyACM0')
d.configure()
d.open()
import time; time.sleep(2)
d.close()
print('OK')
"
```

### "Failed to open. Error code: 0x8029"

- Wrong port
- Wrong baud rate (USB Dongle doesn't need special baud rate)
- Port already used by another program

```bash
# Check processes on port
lsof /dev/ttyACM0
```

### "Connection timeout"

- Device not in range (< 10m)
- Device already connected to another central
- Device not advertising

### Check Firmware Version

```python
from blatann import BleDevice
from blatann.utils import setup_logger

setup_logger(level="DEBUG")  # Shows firmware info when opening

ble_device = BleDevice("/dev/ttyACM0")
ble_device.configure()
ble_device.open()
# Firmware version appears in logs
ble_device.close()
```

---

:::tip Next Step
Continue to [Phase 1: Passive Reconnaissance](../phase1/passive-scanning).
:::
