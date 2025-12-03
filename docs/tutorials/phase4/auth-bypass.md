---
sidebar_position: 3
title: "Authentication Bypass"
---

# Authentication Bypass

Testen ob Authentifizierungsmechanismen umgangen werden können.

## Szenarien

1. **Kein Auth**: Gerät akzeptiert Commands ohne Authentifizierung
2. **Weak Auth**: Vorhersagbare Tokens, hardcoded Credentials
3. **Replay Auth**: Auth-Token kann wiederverwendet werden

## Test

```python
# Ohne vorheriges Pairing/Auth
peer = device.connect(target).wait()
peer.discover_services().wait()

# Direkt schreiben
cmd_char = peer.database.find_characteristic(CMD_UUID)
cmd_char.write(b'\x01\x02\x03').wait()

# Wenn erfolgreich → No Authentication!
```

---

:::tip Nächster Schritt
Weiter zur [Phase 5: Vulnerability Assessment](../phase5/vulnerability-assessment).
:::
