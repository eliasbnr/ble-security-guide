---
sidebar_position: 3
title: "nRF Sniffer Setup"
---

# nRF Sniffer Setup

Der nRF Sniffer verwandelt deinen nRF52840 Dongle in ein **professionelles BLE-Sniffing-Tool** mit Wireshark-Integration.

## Installation

### 1. nRF Util installieren

```bash
# nRF Util herunterladen (von https://www.nordicsemi.com/Products/Development-tools/nRF-Util)
# Für Linux:
wget https://developer.nordicsemi.com/.pc-tools/nrfutil/x64-linux/nrfutil
chmod +x nrfutil
sudo mv nrfutil /usr/local/bin/

# Sniffer-Kommando installieren
nrfutil install ble-sniffer
nrfutil install device

# Version prüfen
nrfutil --version
```

### 2. Firmware flashen

```bash
# Dongle in Bootloader-Modus versetzen
# (Reset-Knopf beim Einstecken drücken - LED pulsiert rot)

# Verfügbare Geräte anzeigen
nrfutil device list

# Firmware flashen (Pfad wird von bootstrap angezeigt)
nrfutil ble-sniffer bootstrap

# Der Output zeigt die Firmware-Pfade, z.B.:
# ~/.nrfutil/share/nrfutil-ble-sniffer/firmware/

# Dongle flashen (Seriennummer aus device list)
nrfutil device program --firmware ~/.nrfutil/share/nrfutil-ble-sniffer/firmware/sniffer_nrf52840dongle_nrf52840_X.X.X.zip --serial-number <SERIAL>
```

### 3. Wireshark-Plugin installieren

```bash
# Bootstrap installiert das extcap-Plugin für Wireshark
# WICHTIG: Mit sudo/Admin-Rechten ausführen!
sudo nrfutil ble-sniffer bootstrap

# Alternativ für lokale Installation (ohne sudo):
nrfutil ble-sniffer bootstrap --extcap-dir ~/.local/lib/wireshark/extcap
```

## Wireshark-Konfiguration

### Sniffer-Interface aktivieren

1. **Wireshark öffnen**
2. **Capture → Refresh Interfaces** (F5)
3. **nRF Sniffer for Bluetooth LE** sollte erscheinen
4. **View → Interface Toolbars → nRF Sniffer for Bluetooth LE** aktivieren

### Capture starten

1. Doppelklick auf **nRF Sniffer for Bluetooth LE**
2. In der Toolbar: Gerät auswählen oder "All advertising" lassen
3. Grüner Start-Button klicken

## Display-Filter für BLE

### Grundlegende Filter

```wireshark
# Alle BLE-Pakete
btle

# Nur Advertising
btle.advertising_header

# ATT-Protokoll (GATT)
btatt

# L2CAP
btl2cap
```

### ATT/GATT-spezifische Filter

```wireshark
# Write Requests
btatt.opcode == 0x12

# Write Commands (ohne Response)
btatt.opcode == 0x52

# Read Requests
btatt.opcode == 0x0a

# Notifications
btatt.opcode == 0x1b
```

### Gerätefilter

```wireshark
# Nach MAC-Adresse
btle.advertising_address == aa:bb:cc:dd:ee:ff

# Nach Gerätenamen
btcommon.eir_ad.entry.device_name contains "LED"
```

## Troubleshooting

### "Interface not found"

```bash
# Prüfen ob Dongle erkannt wird
lsusb | grep Nordic

# Serielle Schnittstelle prüfen
ls /dev/ttyACM*

# Berechtigungen setzen
sudo usermod -a -G dialout $USER
# -> Neuanmeldung erforderlich!
```

### "No packets captured"

1. Ist das Gerät in Reichweite (< 10m)?
2. Sendet das Gerät Advertising-Pakete?
3. Toolbar: Alle Advertising-Kanäle aktiviert (37, 38, 39)?

### Bootstrap-Fehler

```bash
# extcap-Verzeichnis erstellen falls nicht vorhanden
mkdir -p ~/.local/lib/wireshark/extcap

# Nochmal versuchen
nrfutil ble-sniffer bootstrap --extcap-dir ~/.local/lib/wireshark/extcap
```

---

:::tip Nächster Schritt
Weiter zum [blatann Setup](./blatann) für die aktive BLE-Interaktion.
:::
