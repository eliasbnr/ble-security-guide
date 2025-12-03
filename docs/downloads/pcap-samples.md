---
sidebar_position: 3
title: "PCAP Samples"
---

# PCAP Samples

Beispiel-Captures für das Training.

:::note Hinweis
PCAP-Dateien können sensible Daten enthalten. Für dieses Projekt wurden keine echten PCAP-Dateien veröffentlicht - erstelle deine eigenen während der Analyse!
:::

## Empfohlene Captures

Während deiner eigenen Analyse solltest du folgende Captures erstellen:

| Capture | Inhalt | Verwendung |
|---------|--------|------------|
| `advertising_scan.pcapng` | Advertising-Pakete aller Geräte | Phase 1 |
| `connection_setup.pcapng` | Verbindungsaufbau | Protokoll-Analyse |
| `gatt_discovery.pcapng` | Service Discovery | GATT Mapping |
| `app_commands.pcapng` | App-Befehle an Gerät | Command RE |

## Capture erstellen

```bash
# Mit tshark (CLI)
tshark -i nRF_Sniffer -w my_capture.pcapng

# Mit Wireshark (GUI)
# 1. Interface "nRF Sniffer for Bluetooth LE" wählen
# 2. Start klicken
# 3. Aktionen durchführen
# 4. Stop und speichern
```

## Analyse-Tipps

### Filtering

```
# Nur ATT-Protokoll
btatt

# Nur Writes
btatt.opcode == 0x12

# Bestimmtes Gerät
btle.advertising_address == aa:bb:cc:dd:ee:ff
```

### Export für Python

```bash
# Als JSON exportieren
tshark -r capture.pcapng -T json > capture.json

# Nur ATT-Daten
tshark -r capture.pcapng -Y "btatt" -T fields \
    -e frame.number \
    -e btatt.opcode \
    -e btatt.handle \
    -e btatt.value
```

---

:::tip Eigene Captures
Die besten PCAP-Dateien sind die, die du selbst erstellst! Sie enthalten genau die Daten deines Zielgeräts.
:::
