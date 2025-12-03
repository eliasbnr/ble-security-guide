---
sidebar_position: 5
title: "Ghidra Native Analysis"
---

# Ghidra Native Analysis

Analyse von Native Libraries (.so-Dateien) mit Ghidra.

## Workflow

1. **Import**: File → Import File → libAES.so
2. **Analyze**: Analysis → Auto Analyze
3. **Find Functions**: Suche nach "encrypt", "key", "AES"
4. **Decompile**: Fenster "Decompile" öffnen

## Key-Extraction

```c
// Typisches Pattern in libAES.so
unsigned char key[16] = {
    0x34, 0x52, 0x2a, 0x5b, 0x7a, 0x6e, 0x49, 0x2c,
    0x08, 0x09, 0x0a, 0x9d, 0x8d, 0x2a, 0x23, 0xf8
};

void encrypt(unsigned char* data) {
    AES_encrypt(data, data, &key);
}
```

---

:::tip Nächster Schritt
Weiter zur [Phase 4: PoC Development](../phase4/poc-development).
:::
