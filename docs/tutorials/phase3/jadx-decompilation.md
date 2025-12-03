---
sidebar_position: 2
title: "JADX Decompilation"
---

# JADX Decompilation

**JADX** dekompiliert Android-APKs zu lesbarem Java-Quellcode.

## JADX starten

```bash
# GUI starten
jadx-gui smart_led.apk

# Oder CLI für schnelle Analyse
jadx -d output_dir/ smart_led.apk
```

## Navigationsstruktur

```
JADX-GUI
├── Source code
│   ├── wl.smartled (Hauptpaket)
│   │   ├── BluetoothLEService.java  ← BLE-Logik!
│   │   ├── MainActivity.java
│   │   └── utils/
│   │       └── EncryptUtil.java     ← Verschlüsselung!
│   └── Bibliotheken...
└── Resources
    └── AndroidManifest.xml
```

## Relevante Klassen finden

### Suche nach BLE-Keywords

```
Strg+Shift+F (Textsuche)

Suchbegriffe:
- "BluetoothGatt"
- "writeCharacteristic"
- "0000fff0"           (Service UUID)
- "AES" / "encrypt"
- "getBytes"
- "key"
```

### Typische BLE-Klassen

```java
// BluetoothLEService.java - Beispiel
public class BluetoothLEService extends Service {
    
    // UUIDs (WICHTIG!)
    public static final UUID SERVICE_UUID = 
        UUID.fromString("0000fff0-0000-1000-8000-00805f9b34fb");
    
    public static final UUID CHAR_WRITE_UUID = 
        UUID.fromString("0000fff3-0000-1000-8000-00805f9b34fb");
    
    // Schreibfunktion
    public void writeCharacteristic(byte[] data) {
        BluetoothGattCharacteristic characteristic = 
            mBluetoothGatt.getService(SERVICE_UUID)
                         .getCharacteristic(CHAR_WRITE_UUID);
        
        // Verschlüsselung!
        byte[] encrypted = EncryptUtil.encode(data, dataNum);
        
        characteristic.setValue(encrypted);
        mBluetoothGatt.writeCharacteristic(characteristic);
    }
}
```

## Verschlüsselung analysieren

### Beispiel: XOR-Verschlüsselung (LED Strips)

```java
// EncryptUtil.java
public class EncryptUtil {
    
    // HARDCODED KEY! 
    private static byte[] key = {
        89, 76, 90, 75, 53, 49, 33, 41, 62, 72, 64,
        118, 100, 98, 81, 68, 94, 68, 63
    };
    
    public static byte[] encode(byte[] data, int dataNum) {
        byte[] fullKey = new byte[key.length + 1];
        System.arraycopy(key, 0, fullKey, 0, key.length);
        fullKey[key.length] = (byte) dataNum;
        
        byte[] result = data.clone();
        for (int i = 1; i < Math.min(result.length, 25); i++) {
            for (byte k : fullKey) {
                result[i] ^= k;
            }
        }
        return result;
    }
}
```

### Beispiel: AES-Verschlüsselung (LED Brille)

```java
// Verweis auf Native Library
public class AESCipher {
    static {
        System.loadLibrary("AES");  // libAES.so
    }
    
    // Native Methode - Key in libAES.so!
    public static native byte[] encrypt(byte[] data);
}
```

:::warning Native Libraries
Wenn `System.loadLibrary()` verwendet wird, ist der Schlüssel in einer `.so`-Datei versteckt. → Ghidra-Analyse erforderlich!
:::

## Protokoll dokumentieren

```markdown
## Protokoll-Analyse - [App Name]

### Gefundene UUIDs

| UUID | Typ | Verwendung |
|------|-----|------------|
| 0xFFF0 | Service | Hauptservice |
| 0xFFF3 | Characteristic | Write |

### Verschlüsselung

**Typ**: XOR / AES / Keine
**Key**: [extrahiert oder in native lib]

### Command-Struktur

| Offset | Länge | Beschreibung |
|--------|-------|--------------|
| 0 | 1 | Prefix (0x7E) |
| 1 | 1 | Length |
| 2 | 1 | Opcode |
| 3-N | var | Payload |
| N+1 | 1 | Suffix (0xEF) |
```

---

:::tip Nächster Schritt
Weiter zur [UUID Extraction](./uuid-extraction).
:::
