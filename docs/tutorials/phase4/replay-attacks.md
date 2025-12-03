---
sidebar_position: 2
title: "Replay Attacks"
---

# Replay Attacks

Testen ob das Gerät anfällig für Replay-Angriffe ist.

## Konzept

1. **Capture**: Legitimen Traffic aufzeichnen
2. **Replay**: Exakt gleiche Pakete erneut senden
3. **Observe**: Reagiert das Gerät?

## Test

```python
# Aus Wireshark extrahiertes Paket
captured_packet = bytes.fromhex("7e0404010001ff00ef")

# Replay
char.write(captured_packet).wait()
# Wenn das Gerät reagiert → Vulnerability!
```

---

:::tip Nächster Schritt
Weiter zu [Authentication Bypass](./auth-bypass).
:::
