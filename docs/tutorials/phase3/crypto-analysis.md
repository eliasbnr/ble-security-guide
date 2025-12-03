---
sidebar_position: 4
title: "Crypto Analysis"
---

# Crypto Analysis

Analyse der Verschlüsselungsimplementierung.

## Häufige Schwachstellen

1. **Hardcoded Keys**: Schlüssel im Quellcode
2. **Weak Algorithms**: XOR, ROT13, Base64
3. **ECB Mode**: Muster im Ciphertext erkennbar
4. **No IV/Nonce**: Replay-Angriffe möglich

## Python-Implementierung

Nach der Analyse kannst du die Verschlüsselung in Python nachbauen:

```python
# Beispiel: XOR
def encrypt(data, key):
    return bytes(d ^ k for d, k in zip(data, key * len(data)))
```

---

:::tip Nächster Schritt
Weiter zur [Ghidra Native Analysis](./ghidra-native).
:::
