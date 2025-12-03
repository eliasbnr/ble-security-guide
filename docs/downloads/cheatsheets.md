---
sidebar_position: 4
title: "Cheatsheets"
---

# Cheatsheets

## Wireshark BLE Filter

```
btle                     # All BLE
btatt                    # ATT Protocol
btatt.opcode == 0x12     # Write Request
btatt.opcode == 0x1b     # Notification
btle.advertising_address == aa:bb:cc:dd:ee:ff
```

## gatttool Befehle

```bash
gatttool -b MAC -I       # Interactive
> connect
> primary
> characteristics
> char-read-hnd 0x0012
> char-write-req 0x0012 0102
```

## blatann Schnellreferenz

```python
# Initialisierung
ble = BleDevice("/dev/ttyACM0")
ble.configure()
ble.open()

# Scannen
ble.scanner.start_scan().wait(10)

# Verbinden
peer = ble.connect(addr).wait()
peer.discover_services().wait()

# Lesen/Schreiben
char = peer.database.find_characteristic(uuid)
char.read().wait()
char.write(data).wait()
```

## Häufige UUIDs

```
0x1800 - Generic Access
0x1801 - Generic Attribute
0x180A - Device Information
0x180F - Battery Service
0x2902 - CCCD (Notifications)
0xFFF0 - Custom (häufig)
```
