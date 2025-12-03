---
sidebar_position: 3
title: "App-Analyse"
---

# LED Brille - App-Analyse

## APK Extraction

```bash
# Package finden
adb shell pm list packages | grep -i glass
# package:com.xl.ledglasses

# APK-Pfad ermitteln
adb shell pm path com.xl.ledglasses
# /data/app/~~abc123==/com.xl.ledglasses-xyz==/base.apk

# APK herunterladen
adb pull /data/app/.../base.apk ledglasses.apk
```

## APK-Struktur

```
ledglasses.apk
├── AndroidManifest.xml
├── classes.dex
├── lib/
│   ├── arm64-v8a/
│   │   └── libAES.so          ← Native Library!
│   └── armeabi-v7a/
│       └── libAES.so
├── res/
└── resources.arsc
```

**Wichtiger Fund**: Native Library `libAES.so` deutet auf AES-Verschlüsselung hin!

## JADX-Analyse

### BLE-Service Klasse

```java
// BluetoothLEService.java
public class BluetoothLEService extends Service {
    
    // Service UUID
    public static final UUID SERVICE_UUID = 
        UUID.fromString("0000fff0-0000-1000-8000-00805f9b34fb");
    
    // Characteristics
    public static final UUID CHAR_CONTROL = 
        UUID.fromString("d44bc439-abfd-45a2-b575-925416129600");
    public static final UUID CHAR_DATA = 
        UUID.fromString("d44bc439-abfd-45a2-b575-92541612960a");
    public static final UUID CHAR_NOTIFY = 
        UUID.fromString("d44bc439-abfd-45a2-b575-925416129601");
    
    public void sendCommand(byte[] data) {
        // Verschlüsselung vor dem Senden!
        byte[] encrypted = AESCipher.encrypt(data);
        
        BluetoothGattCharacteristic char = 
            mGatt.getService(SERVICE_UUID)
                 .getCharacteristic(CHAR_CONTROL);
        char.setValue(encrypted);
        mGatt.writeCharacteristic(char);
    }
}
```

### AES Cipher Wrapper

```java
// AESCipher.java
public class AESCipher {
    
    static {
        System.loadLibrary("AES");  // Lädt libAES.so
    }
    
    // Native Methode - Implementation in libAES.so!
    public static native byte[] encrypt(byte[] data);
    public static native byte[] decrypt(byte[] data);
}
```

**Problem**: Der eigentliche Verschlüsselungscode und der Key sind in der nativen Library versteckt!

### Command-Struktur

Aus der App-Analyse konnten wir die Command-Struktur rekonstruieren:

```java
// CommandBuilder.java
public class CommandBuilder {
    
    // ATATS - Text senden initiieren
    public byte[] buildATATS(int textLength) {
        byte[] cmd = new byte[16];
        cmd[0] = 7;           // Length
        cmd[1] = 'A';         // 0x41
        cmd[2] = 'T';         // 0x54
        cmd[3] = 'A';         // 0x41
        cmd[4] = 'T';         // 0x54
        cmd[5] = 'S';         // 0x53
        cmd[6] = 1;           // Parameter
        cmd[7] = (byte)(textLength >> 8);   // High byte
        cmd[8] = (byte)(textLength & 0xFF); // Low byte
        return AESCipher.encrypt(cmd);
    }
    
    // ATCP - Übertragung abschließen
    public byte[] buildATCP() {
        byte[] cmd = new byte[16];
        cmd[0] = 5;           // Length
        cmd[1] = 'A';         // 0x41
        cmd[2] = 'T';         // 0x54
        cmd[3] = 'C';         // 0x43
        cmd[4] = 'P';         // 0x50
        return AESCipher.encrypt(cmd);
    }
    
    // MODE - Display-Modus setzen
    public byte[] buildMODE(int mode, int direction) {
        byte[] cmd = new byte[16];
        cmd[0] = 6;           // Length
        cmd[1] = 'M';         // 0x4D
        cmd[2] = 'O';         // 0x4F
        cmd[3] = 'D';         // 0x44
        cmd[4] = 'E';         // 0x45
        cmd[5] = (byte)mode;
        cmd[6] = (byte)direction;
        return AESCipher.encrypt(cmd);
    }
}
```

### Identifizierte Commands

| Command | Bytes | Beschreibung |
|---------|-------|--------------|
| ATATS | `07 41 54 41 54 53 01 HH LL` | Start Text-Übertragung, HH/LL = Länge |
| ATCP | `05 41 54 43 50` | Complete - Übertragung abschließen |
| MODE | `06 4D 4F 44 45 MM DD` | Display-Modus setzen |
| DATA | `LL [data...]` | Datenpaket, LL = Länge im Paket |

### Display-Modi

```java
// Aus strings.xml und Code-Analyse
MODE_STATIC = 1;       // Statische Anzeige
MODE_SCROLL = 2;       // Scroll-Modus
  DIRECTION_LEFT = 0;
  DIRECTION_RIGHT = 1;
  DIRECTION_DOWN = 2;   // Vertikal (falls unterstützt)
```

## Font-Daten

Die App enthält eine Bitmap-Font für die LED-Matrix:

```java
// FontData.java (rekonstruiert)
public class FontData {
    // Jeder Buchstabe als Bitmap für 8x? LED Matrix
    // Format: Spaltenweise, LSB = oberste LED
    
    public static final byte[] CHAR_H = {
        0x7F,  // ███████
        0x08,  // ___█___
        0x08,  // ___█___
        0x08,  // ___█___
        0x7F,  // ███████
        0x00   // Spacing
    };
    
    public static final byte[] CHAR_E = {
        0x7F,  // ███████
        0x49,  // █__█__█
        0x49,  // █__█__█
        0x41,  // █_____█
        0x00   // Spacing
    };
    // ... weitere Zeichen
}
```

## Zusammenfassung App-Analyse

| Fund | Details | Nächster Schritt |
|------|---------|------------------|
| UUIDs | Service 0xFFF0, 3 Characteristics | ✓ Dokumentiert |
| Verschlüsselung | AES (native) | → Ghidra-Analyse |
| Command-Format | ATATS, ATCP, MODE, DATA | ✓ Dokumentiert |
| Font-Daten | Bitmap pro Zeichen | ✓ Extrahiert |
| Key | In libAES.so versteckt | → Ghidra-Analyse |

---

:::tip Nächster Schritt
Weiter zur [Crypto-Analyse](./crypto-analysis) um den AES-Key aus der nativen Library zu extrahieren.
:::
