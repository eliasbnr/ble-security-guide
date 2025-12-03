---
sidebar_position: 4
title: "Findings"
---

# Smart Waage - Findings

## F-001: Weight Data in Advertising

### Beschreibung

Die Waage sendet Gewichtsdaten unverschlüsselt in BLE Advertising-Paketen.
Diese Daten sind für jeden in BLE-Reichweite (~10m) lesbar, ohne Verbindung.

### CVSS v3.1

```
Vector: CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N
Score: 5.3 (Medium)

- Attack Vector: Adjacent (A) - BLE Reichweite
- Attack Complexity: Low (L) - Nur Scanner nötig
- Privileges Required: None (N)
- User Interaction: None (N)
- Confidentiality: Low (L) - Nur Gewicht, keine PII
- Integrity: None (N)
- Availability: None (N)
```

### Impact

| Aspekt | Bewertung |
|--------|-----------|
| Privacy | Gewicht ist sensitive Gesundheitsdaten |
| Tracking | MAC-Adresse ermöglicht Personenzuordnung |
| Reichweite | ~10m, auch durch Wände |
| Aufwand | Minimal (Standard BLE Scanner) |

### Betroffene Daten

- Gewicht (in kg, 2 Dezimalstellen)
- Impedanz (Body Composition)
- MAC-Adresse (statisch)

### Remediation

| Priorität | Maßnahme |
|-----------|----------|
| Hoch | Gewicht NICHT im Advertising senden |
| Hoch | Daten nur nach Verbindung + Auth übertragen |
| Mittel | MAC-Adresse rotieren (BLE Privacy) |
| Niedrig | Verschlüsselung der Advertising-Daten |

### DSGVO-Relevanz

Gewichtsdaten gelten als **Gesundheitsdaten** (Art. 9 DSGVO):

> "besondere Kategorien personenbezogener Daten"

Die unverschlüsselte Übertragung könnte gegen:
- Art. 5 (1) f) - Vertraulichkeit
- Art. 32 - Sicherheit der Verarbeitung

verstoßen.

---

:::warning Hinweis
Dieses Finding betrifft eine **Design-Entscheidung** des Herstellers.
Ein Firmware-Update könnte das Problem beheben, erfordert aber Änderungen am Protokoll.
:::
