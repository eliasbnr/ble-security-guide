---
sidebar_position: 2
title: "Reconnaissance"
---

# LED Brille - Reconnaissance

## Phase 1: Passives Scanning

### Advertising-Daten

```
Device: GLASSES-12B008
MAC: XX:XX:XX:XX:XX:XX (Public)
RSSI: -45 dBm
Advertising Type: ADV_IND (Connectable, Scannable)
```

### Advertising Data Analysis

| AD Type | Wert | Beschreibung |
|---------|------|--------------|
| 0x01 | 0x06 | Flags: LE General Discoverable |
| 0x09 | "GLASSES-12B008" | Complete Local Name |
| 0x03 | 0xFFF0 | Complete 16-bit Service UUID |

**Beobachtungen**:
- Keine sensitiven Daten im Advertising
- Statische MAC-Adresse (kein Privacy-Modus)
- Custom Service UUID 0xFFF0

## Phase 2: GATT Enumeration

### Service Discovery

```
Service: 0x1800 (Generic Access)
├── 0x2A00: Device Name [READ]
└── 0x2A01: Appearance [READ]

Service: 0x1801 (Generic Attribute)
└── 0x2A05: Service Changed [INDICATE]

Service: 0xFFF0 (Custom - Main Service)
├── Char 1: d44bc439-abfd-45a2-b575-925416129600
│   └── Properties: WRITE, WRITE_NO_RESP
│   └── Handle: 0x0012
│   └── Purpose: Command/Control
│
├── Char 2: d44bc439-abfd-45a2-b575-92541612960a  
│   └── Properties: WRITE, WRITE_NO_RESP
│   └── Handle: 0x0015
│   └── Purpose: Data Transfer
│
└── Char 3: d44bc439-abfd-45a2-b575-925416129601
    └── Properties: NOTIFY
    └── Handle: 0x001b
    └── CCCD: 0x001c
    └── Purpose: Status Notifications
```

### Characteristic-Analyse

| UUID (kurz) | Handle | Properties | Vermutete Funktion |
|-------------|--------|------------|-------------------|
| ...9600 | 0x0012 | WRITE | Steuerbefehle |
| ...960a | 0x0015 | WRITE | Datenübertragung |
| ...9601 | 0x001b | NOTIFY | Gerätestatus |

## Phase 3: Traffic Capture

### Wireshark-Capture Strategie

1. nRF Sniffer auf GLASSES-12B008 konfiguriert
2. App gestartet → Verbindungsaufbau aufgezeichnet
3. Verschiedene Funktionen ausgeführt:
   - Text eingegeben: "HELLO"
   - Display-Modus gewechselt
   - Helligkeit geändert

### Beobachtete Pakete

```
Frame 1: Write Request @ Handle 0x0012
Value: 3e 9d 29 cf 48 fb 0a d2 7e 1a f5 c3 b1 20 8d 4f (16 bytes)

Frame 2: Write Request @ Handle 0x0012  
Value: a7 12 e8 5b 99 7c 63 21 ff 08 33 d1 45 7e 99 12 (16 bytes)

Frame 3: Write Request @ Handle 0x0015
Value: 8c 44 7a b3 e1 5d 9f 20 11 cc ab 78 e2 3f 91 00 (16 bytes)
...
```

### Analyse der Pakete

**Beobachtungen**:
- Alle Pakete sind **exakt 16 Bytes** lang
- Keine erkennbaren Muster (kein Klartext)
- **Vermutung**: Verschlüsselung aktiv (AES-128? 16-Byte-Blockgröße)

### Vergleich: Gleicher Text, verschiedene Captures

```
"HELLO" - Capture 1: 3e 9d 29 cf 48 fb 0a d2 ...
"HELLO" - Capture 2: 3e 9d 29 cf 48 fb 0a d2 ...
```

**Gleiche Eingabe = Gleiche Ausgabe** → ECB-Mode oder deterministisches Verfahren!

## Security Level Testing

### Test ohne Pairing

```bash
# Verbindung ohne Pairing
gatttool -b XX:XX:XX:XX:XX:XX --sec-level=low -I
> connect
Connection successful  # ✗ Kein Pairing erforderlich!

> char-write-req 0x0012 00112233445566778899aabbccddeeff
Characteristic value was written successfully  # ✗ Schreiben erlaubt!
```

### Ergebnis

| Test | Ergebnis | Bewertung |
|------|----------|-----------|
| Connect ohne Pairing | ✓ Erfolgreich | ✗ Unsicher |
| Write @ Level 1 | ✓ Erfolgreich | ✗ Unsicher |
| Write @ Level 2 | ✓ Erfolgreich | ✗ Unsicher |
| Write @ Level 3 | ✓ Erfolgreich | ✗ Unsicher |

**Fazit**: Keine BLE-Level-Authentifizierung vorhanden!

## Reconnaissance Summary

| Aspekt | Ergebnis | Security Impact |
|--------|----------|-----------------|
| Advertising | Keine Leaks | OK |
| MAC-Adresse | Statisch | Tracking möglich |
| GATT Access | Ungeschützt | ✗ Critical |
| Data Format | Verschlüsselt (16B) | Analyse nötig |
| Security Level | Keiner | ✗ Critical |

---

:::tip Nächster Schritt
Weiter zur [App-Analyse](./app-analysis) um die Verschlüsselung zu verstehen.
:::
