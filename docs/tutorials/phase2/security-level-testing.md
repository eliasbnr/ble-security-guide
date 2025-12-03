---
sidebar_position: 3
title: "Security Level Testing"
---

# Security Level Testing

BLE definiert verschiedene Security Levels. Wir testen, welche Level das Gerät erfordert.

## Security Levels

| Level | Beschreibung | Pairing |
|-------|--------------|---------|
| 1 | No Security | Keins |
| 2 | Unauthenticated Encryption | Just Works |
| 3 | Authenticated Encryption | Passkey/OOB |
| 4 | LE Secure Connections | LESC |

## Test mit gatttool

```bash
# Level 1 (keine Sicherheit)
gatttool --sec-level=low -b AA:BB:CC -I
> connect
> char-read-hnd 0x0012

# Level 2 (Verschlüsselung)
gatttool --sec-level=medium -b AA:BB:CC -I
> connect
> char-read-hnd 0x0012

# Level 3 (Authentifizierte Verschlüsselung)
gatttool --sec-level=high -b AA:BB:CC -I
> connect
> char-read-hnd 0x0012
```

## Ergebnisse dokumentieren

| Characteristic | Level 1 | Level 2 | Level 3 |
|----------------|---------|---------|---------|
| 0x0012 (Command) | ✓ | ✓ | ✓ |
| 0x0015 (Data) | ✓ | ✓ | ✓ |
| 0x001b (Notify) | ✓ | ✓ | ✓ |

**Ergebnis**: Gerät akzeptiert alle Security Levels → **Keine Zugriffskontrolle!**

---

:::tip Nächster Schritt
Weiter zur [Phase 3: APK Extraction](../phase3/apk-extraction).
:::
