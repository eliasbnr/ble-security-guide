---
sidebar_position: 4
title: "blatann Setup"
---

# blatann Setup

**blatann** ist eine Python-Bibliothek für BLE-Kommunikation mit Nordic-Hardware. Sie ermöglicht professionelle PoC-Entwicklung.

## Installation

```bash
# In virtueller Umgebung
python3 -m venv ~/ble-security-env
source ~/ble-security-env/bin/activate

# blatann installieren
pip install blatann
```

## Firmware für blatann

:::warning Wichtig
blatann benötigt eine **andere Firmware** als der nRF Sniffer! Du musst die Connectivity-Firmware flashen.
:::

### Firmware finden

Die Firmware wird mit `pc-ble-driver-py` installiert:

```bash
# Pfad zur Firmware finden
python3 -c "import pc_ble_driver_py; print(pc_ble_driver_py.__path__[0])"
# -> z.B.: ~/.local/lib/python3.10/site-packages/pc_ble_driver_py

# Firmware-Dateien anzeigen (für blatann v0.3+)
ls ~/.local/lib/python3.10/site-packages/pc_ble_driver_py/hex/sd_api_v5/
```

### Firmware auswählen

| Hardware | Firmware |
|----------|----------|
| nRF52840 USB Dongle | `connectivity_x.y.z_usb_with_s132_x.y.hex` |
| nRF52840 Devkit (USB-Port) | `connectivity_x.y.z_usb_with_s132_x.y.hex` |
| nRF52840 Devkit (J-Link) | `connectivity_x.y.z_1m_with_s132_x.y.hex` |
| nRF52832 Devkit | `connectivity_x.y.z_1m_with_s132_x.y.hex` |

### Firmware flashen (nRF52840 Dongle)

```bash
# 1. Dongle in Bootloader-Modus versetzen
#    (Reset-Knopf beim Einstecken drücken - LED pulsiert rot)

# 2. Port prüfen
ls /dev/ttyACM*

# 3. DFU-Paket erstellen
FIRMWARE_PATH=$(python3 -c "import pc_ble_driver_py; print(pc_ble_driver_py.__path__[0])")/hex/sd_api_v5
FIRMWARE=$(ls $FIRMWARE_PATH/connectivity_*_usb_*.hex | head -1)

nrfutil pkg generate --hw-version 52 --sd-req 0x00 \
    --application "$FIRMWARE" \
    --application-version 1 \
    connectivity.zip

# 4. Flashen
nrfutil dfu usb-serial -pkg connectivity.zip -p /dev/ttyACM0

# 5. Nach dem Flashen: Port kann sich ändern!
ls /dev/ttyACM*
```

## Erste Schritte

### Installation verifizieren

```python
# test_blatann.py
import blatann
from blatann import BleDevice

print("✅ blatann erfolgreich importiert!")
print(f"   BleDevice: {BleDevice}")
```

### Gerät initialisieren und scannen

```python
#!/usr/bin/env python3
"""
BLE Scanner mit blatann - Vollständiges Beispiel
"""
import sys
import time
from blatann import BleDevice
from blatann.utils import setup_logger

def main():
    # Port bestimmen
    port = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyACM0"
    
    # Logging aktivieren (sehr hilfreich bei Problemen!)
    # setup_logger(level="DEBUG")
    
    print(f"🔌 Verbinde mit {port}...")
    
    # BLE-Gerät erstellen und öffnen
    ble_device = BleDevice(port)
    ble_device.configure()
    ble_device.open()
    
    # Kurz warten bis Gerät bereit
    time.sleep(1)
    
    print("🔍 Scanne nach BLE-Geräten (10s)...")
    print("-" * 60)
    
    found_devices = {}
    
    def on_scan_report(scanner, report):
        """Callback für jeden gefundenen Advertising-Report"""
        addr = str(report.peer_address)
        if addr not in found_devices:
            name = report.advertise_data.local_name or "Unknown"
            found_devices[addr] = name
            print(f"[NEW] {addr} | {name} | RSSI: {report.rssi}")
    
    # Callback registrieren
    ble_device.scanner.on_scan_received.register(on_scan_report)
    
    # Scan starten und auf Completion warten
    try:
        ble_device.scanner.set_default_scan_params(
            interval_ms=200,
            window_ms=150,
            timeout_seconds=10,
            active_scanning=True
        )
        waitable = ble_device.scanner.start_scan()
        waitable.wait(timeout=15)  # Etwas mehr als scan timeout
    except Exception as e:
        print(f"❌ Scan-Fehler: {e}")
    finally:
        ble_device.close()
    
    print("-" * 60)
    print(f"✅ {len(found_devices)} Geräte gefunden")

if __name__ == "__main__":
    main()
```

### Mit Gerät verbinden

```python
#!/usr/bin/env python3
"""
BLE Verbindung mit blatann
"""
import sys
import time
from blatann import BleDevice
from blatann.utils import setup_logger

TARGET_NAME = "GLASSES-12B008"  # Anpassen!

def main():
    port = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyACM0"
    setup_logger(level="INFO")
    
    ble_device = BleDevice(port)
    ble_device.configure()
    ble_device.open()
    time.sleep(1)
    
    # Zielgerät suchen
    target_address = None
    
    def on_scan_report(scanner, report):
        global target_address
        name = report.advertise_data.local_name
        if name and TARGET_NAME in name:
            target_address = report.peer_address
            print(f"✅ Gefunden: {target_address} ({name})")
            scanner.stop()
    
    ble_device.scanner.on_scan_received.register(on_scan_report)
    
    print(f"🔍 Suche nach '{TARGET_NAME}'...")
    try:
        ble_device.scanner.start_scan().wait(timeout=15)
    except:
        pass  # Timeout ist OK wenn Gerät gefunden
    
    if not target_address:
        print("❌ Gerät nicht gefunden")
        ble_device.close()
        return
    
    # Verbinden
    print(f"🔗 Verbinde mit {target_address}...")
    try:
        peer = ble_device.connect(target_address).wait(timeout=10)
        print("✅ Verbunden!")
        
        # Services entdecken
        print("📋 Entdecke Services...")
        peer.discover_services().wait(timeout=20)
        
        # Services auflisten
        for service in peer.database.services:
            print(f"\nService: {service.uuid}")
            for char in service.characteristics:
                props = []
                if char.readable: props.append("READ")
                if char.writable: props.append("WRITE")
                if char.subscribable: props.append("NOTIFY")
                print(f"  └─ {char.uuid} [{', '.join(props)}]")
        
        # Trennen
        peer.disconnect().wait(timeout=5)
        print("\n✅ Getrennt")
        
    except Exception as e:
        print(f"❌ Fehler: {e}")
    finally:
        ble_device.close()

if __name__ == "__main__":
    main()
```

## GATT-Operationen

### Characteristic lesen

```python
# Nach Service Discovery...
char = peer.database.find_characteristic("d44bc439-abfd-45a2-b575-92541612960a")

if char and char.readable:
    result = char.read().wait(timeout=5)
    print(f"Gelesen: {result.value.hex()}")
```

### Characteristic schreiben

```python
# Daten vorbereiten
data = bytes([0x01, 0x02, 0x03])

# Schreiben (mit Response)
if char.writable:
    char.write(data).wait(timeout=5)

# Schreiben ohne Response (schneller, für Write Command)
char.write(data, with_response=False)
```

### Notifications empfangen

```python
import time

def on_notification(char, event_args):
    print(f"📥 Notification: {event_args.value.hex()}")

# Notification-Characteristic finden
notify_char = peer.database.find_characteristic("d44bc439-abfd-45a2-b575-925416129601")

if notify_char and notify_char.subscribable:
    # Notifications aktivieren
    notify_char.subscribe(on_notification).wait(timeout=5)
    
    # Warten auf Notifications
    print("⏳ Warte auf Notifications (10s)...")
    time.sleep(10)
    
    # Deaktivieren
    notify_char.unsubscribe().wait(timeout=5)
```

## Troubleshooting

### "TimeoutError: Timed out waiting for event to occur"

**Ursachen:**
1. **Falsche Firmware** - blatann braucht Connectivity-Firmware, nicht Sniffer-Firmware
2. **Falscher Port** - Port kann sich nach Firmware-Flash ändern
3. **Gerät nicht bereit** - `time.sleep(1)` nach `open()` einfügen
4. **Keine BLE-Geräte in Reichweite**

```bash
# Port prüfen
ls /dev/ttyACM*

# Mit DEBUG-Logging testen
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

- Falscher Port
- Falsche Baudrate (USB Dongle braucht keine spezielle Baudrate)
- Port bereits von anderem Programm verwendet

```bash
# Prozesse auf Port prüfen
lsof /dev/ttyACM0
```

### "Connection timeout"

- Gerät nicht in Reichweite (< 10m)
- Gerät bereits mit anderem Central verbunden
- Gerät advertised nicht

### Firmware-Version prüfen

```python
from blatann import BleDevice
from blatann.utils import setup_logger

setup_logger(level="DEBUG")  # Zeigt Firmware-Info beim Öffnen

ble_device = BleDevice("/dev/ttyACM0")
ble_device.configure()
ble_device.open()
# In den Logs erscheint die Firmware-Version
ble_device.close()
```

---

:::tip Nächster Schritt
Weiter zur [Phase 1: Passive Reconnaissance](../phase1/passive-scanning).
:::
