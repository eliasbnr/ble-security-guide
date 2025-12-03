---
sidebar_position: 2
title: "JADX Decompilation"
---

# JADX Decompilation

Decompile the APK to readable Java code.

## Start JADX

```bash
jadx-gui app.apk
```

## Search Patterns

```
"0000fff0"           # Service UUID
"BluetoothGatt"      # BLE code
"encrypt"            # Crypto
"System.loadLibrary" # Native libs
```

---

:::tip Next Step
Continue with [UUID Extraction](./uuid-extraction).
:::
