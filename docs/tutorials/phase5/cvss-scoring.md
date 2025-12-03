---
sidebar_position: 2
title: "CVSS Scoring"
---

# CVSS Scoring

Berechnung des Common Vulnerability Scoring System (CVSS) Scores.

## CVSS v3.1 Metriken

### Base Score Metriken

| Metrik | BLE-typischer Wert |
|--------|-------------------|
| Attack Vector | Adjacent (A) |
| Attack Complexity | Low (L) |
| Privileges Required | None (N) |
| User Interaction | None (N) |
| Scope | Unchanged (U) |

### Beispiel: Hardcoded Key

```
CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N

Base Score: 8.1 (High)
```

## Calculator

Nutze den [FIRST CVSS Calculator](https://www.first.org/cvss/calculator/3.1).

---

:::tip Nächster Schritt
Weiter zum [Report Writing](./report-writing).
:::
