---
sidebar_position: 1
title: "APK Extraction"
---

# APK Extraction

Um das BLE-Protokoll zu verstehen, extrahieren wir die Companion-App vom Android-Gerät.

## Methode 1: ADB (Android Debug Bridge)

```bash
# USB-Debugging aktivieren auf dem Smartphone
# Einstellungen → Über das Telefon → 7x auf Build-Nummer tippen
# Einstellungen → Entwickleroptionen → USB-Debugging aktivieren

# Gerät verbinden und prüfen
adb devices

# Package-Name finden
adb shell pm list packages | grep -i led
# Beispiel: package:wl.smartled

# APK-Pfad ermitteln
adb shell pm path wl.smartled
# Beispiel: package:/data/app/~~xxx==/wl.smartled-xxx==/base.apk

# APK herunterladen
adb pull /data/app/~~xxx==/wl.smartled-xxx==/base.apk smart_led.apk
```

## Methode 2: Online APK-Mirror

Falls kein Gerät verfügbar:

1. [APKMirror.com](https://www.apkmirror.com)
2. [APKPure.com](https://apkpure.com)

:::warning Vorsicht
Lade APKs nur von vertrauenswürdigen Quellen. Prüfe SHA256-Checksums.
:::

## Methode 3: Aus Google Play (Alternativer Weg)

```bash
# Mit gplaycli (erfordert Google-Konto)
pip install gplaycli
gplaycli -d wl.smartled
```

## APK-Struktur

Nach dem Download:

```
smart_led.apk (eigentlich ein ZIP)
├── AndroidManifest.xml     # App-Metadaten, Berechtigungen
├── classes.dex             # Dalvik Bytecode (Java-Code)
├── classes2.dex            # Weitere Klassen
├── lib/
│   ├── arm64-v8a/
│   │   └── libAES.so       # Native Libraries!
│   └── armeabi-v7a/
│       └── libAES.so
├── res/                    # Ressourcen
└── resources.arsc          # Kompilierte Ressourcen
```

## Wichtige Dateien identifizieren

```bash
# APK entpacken
unzip smart_led.apk -d smart_led_extracted/

# Native Libraries finden
find smart_led_extracted/ -name "*.so" -type f

# DEX-Dateien zählen
ls -la smart_led_extracted/*.dex
```

## Split-APKs behandeln

Neuere Android-Versionen verwenden oft Split-APKs:

```bash
# Alle APK-Teile finden
adb shell pm path wl.smartled
# Zeigt möglicherweise mehrere Pfade

# Alle Teile herunterladen
adb pull /data/app/~~xxx==/wl.smartled-xxx==/base.apk
adb pull /data/app/~~xxx==/wl.smartled-xxx==/split_config.arm64_v8a.apk
adb pull /data/app/~~xxx==/wl.smartled-xxx==/split_config.de.apk
```

---

:::tip Nächster Schritt
Weiter zur [JADX Decompilation](./jadx-decompilation).
:::
