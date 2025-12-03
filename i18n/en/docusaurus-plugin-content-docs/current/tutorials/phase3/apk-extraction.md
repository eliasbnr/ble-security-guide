---
sidebar_position: 1
title: "APK Extraction"
---

# APK Extraction

Extract the companion app from Android device.

## Using ADB

```bash
# Enable USB debugging on phone
adb devices

# Find package
adb shell pm list packages | grep -i led

# Get APK path
adb shell pm path com.example.app

# Download
adb pull /data/app/.../base.apk
```

---

:::tip Next Step
Continue with [JADX Decompilation](./jadx-decompilation).
:::
