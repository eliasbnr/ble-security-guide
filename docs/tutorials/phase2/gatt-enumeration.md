---
sidebar_position: 1
title: "GATT Enumeration"
---

# GATT Enumeration

Nach der passiven Reconnaissance verbinden wir uns aktiv mit dem Gerät und enumerieren die GATT-Struktur.

## Ziel

```mermaid
flowchart LR
    A[Verbinden] --> B[Service Discovery]
    B --> C[Characteristic Discovery]
    C --> D[Descriptor Discovery]
    D --> E[Dokumentation]
```

## Mit gatttool (Linux)

```bash
# Interaktiver Modus
gatttool -i hci0 -b AA:BB:CC:DD:EE:FF -I

# Verbinden
[AA:BB:CC:DD:EE:FF][LE]> connect
Attempting to connect to AA:BB:CC:DD:EE:FF
Connection successful

# Primary Services auflisten
[AA:BB:CC:DD:EE:FF][LE]> primary
attr handle: 0x0001, end grp handle: 0x0009 uuid: 00001800-0000-1000-8000-00805f9b34fb
attr handle: 0x0010, end grp handle: 0x001c uuid: 0000fff0-0000-1000-8000-00805f9b34fb

# Characteristics auflisten
[AA:BB:CC:DD:EE:FF][LE]> characteristics
handle: 0x0011, char properties: 0x0c, char value handle: 0x0012, uuid: d44bc439-abfd-45a2-b575-925416129600

# Descriptor auflisten
[AA:BB:CC:DD:EE:FF][LE]> char-desc
handle: 0x0012, uuid: d44bc439-abfd-45a2-b575-925416129600
handle: 0x0013, uuid: 00002901-0000-1000-8000-00805f9b34fb
```

## Mit blatann (Python)

```python
#!/usr/bin/env python3
"""
GATT Enumeration mit blatann
Erstellt vollständige Dokumentation der GATT-Struktur
"""

import sys
import json
from blatann import BleDevice
from blatann.utils import setup_logger

def enumerate_gatt(target_addr, serial_port="/dev/ttyACM0"):
    setup_logger(level="INFO")
    
    ble_device = BleDevice(serial_port)
    ble_device.configure()
    ble_device.open()
    
    print(f"🔗 Connecting to {target_addr}...")
    peer = ble_device.connect(target_addr).wait(timeout=10)
    
    # MTU Exchange (optional, aber empfohlen)
    print("📐 Exchanging MTU...")
    peer.exchange_mtu(247).wait()
    print(f"   MTU: {peer.mtu_size}")
    
    # Service Discovery
    print("\n🔍 Discovering services...")
    peer.discover_services().wait(timeout=30)
    
    # Struktur aufbauen
    gatt_db = {
        "device": str(target_addr),
        "mtu": peer.mtu_size,
        "services": []
    }
    
    for service in peer.database.services:
        svc_info = {
            "uuid": str(service.uuid),
            "handles": f"{service.start_handle}-{service.end_handle}",
            "characteristics": []
        }
        
        for char in service.characteristics:
            char_info = {
                "uuid": str(char.uuid),
                "handle": char.value_handle,
                "properties": [],
                "descriptors": []
            }
            
            # Properties ermitteln
            if char.readable:
                char_info["properties"].append("READ")
            if char.writable:
                char_info["properties"].append("WRITE")
            if char.subscribable:
                char_info["properties"].append("NOTIFY/INDICATE")
            
            # Descriptors
            for desc in char.descriptors:
                char_info["descriptors"].append({
                    "uuid": str(desc.uuid),
                    "handle": desc.handle
                })
            
            svc_info["characteristics"].append(char_info)
        
        gatt_db["services"].append(svc_info)
    
    # Ausgabe
    print("\n" + "=" * 60)
    print("GATT DATABASE")
    print("=" * 60)
    
    for svc in gatt_db["services"]:
        print(f"\n📦 Service: {svc['uuid']}")
        print(f"   Handles: {svc['handles']}")
        
        for char in svc["characteristics"]:
            print(f"\n   └─ Characteristic: {char['uuid']}")
            print(f"      Handle: 0x{char['handle']:04x}")
            print(f"      Properties: {', '.join(char['properties'])}")
            
            for desc in char["descriptors"]:
                print(f"      └─ Descriptor: {desc['uuid']} @ 0x{desc['handle']:04x}")
    
    # Als JSON speichern
    with open(f"gatt_{target_addr.replace(':', '')}.json", "w") as f:
        json.dump(gatt_db, f, indent=2)
    print(f"\n💾 Saved to gatt_{target_addr.replace(':', '')}.json")
    
    peer.disconnect().wait()
    ble_device.close()
    
    return gatt_db

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <MAC_ADDRESS>")
        sys.exit(1)
    
    enumerate_gatt(sys.argv[1])
```

## Ergebnis dokumentieren

### Template

```markdown
## GATT Enumeration - [Gerätename]

**MAC**: AA:BB:CC:DD:EE:FF
**MTU**: 247 Bytes
**Datum**: YYYY-MM-DD

### Services

#### Service 1: Generic Access (0x1800)
- Handles: 0x0001 - 0x0009
- Standard BLE Service

| Characteristic | Handle | Properties | Beschreibung |
|----------------|--------|------------|--------------|
| Device Name (0x2A00) | 0x0003 | READ | Gerätename |
| Appearance (0x2A01) | 0x0005 | READ | Gerätetyp |

#### Service 2: Custom Service (0xFFF0)
- Handles: 0x0010 - 0x001C
- **Hauptservice für Gerätesteuerung**

| Characteristic | Handle | Properties | Beschreibung |
|----------------|--------|------------|--------------|
| Command (d44b...9600) | 0x0012 | WRITE | Steuerbefehle |
| Data (d44b...960a) | 0x0015 | WRITE | Datenübertragung |
| Notify (d44b...9601) | 0x001b | NOTIFY | Statusmeldungen |

### Security-Beobachtungen

- [ ] Characteristics ohne Authentifizierung zugreifbar?
- [ ] Security Level getestet?
- [ ] Sensitive Daten in lesbaren Characteristics?
```

## Nächste Schritte

Nach der GATT-Enumeration:

1. **Characteristic Testing**: Werte lesen/schreiben
2. **Security Level Testing**: Zugriffsbeschränkungen prüfen
3. **APK-Analyse**: Protokoll aus App extrahieren

---

:::tip Nächster Schritt
Weiter zum [Characteristic Testing](./characteristic-testing).
:::
