---
sidebar_position: 3
title: "App Analysis"
---

# LED Glasses - App Analysis

## APK Structure

```
ledglasses.apk
├── classes.dex
└── lib/arm64-v8a/
    └── libAES.so  ← Native Library!
```

## Key Finding

```java
// AESCipher.java
public class AESCipher {
    static {
        System.loadLibrary("AES");  // Key hidden in native lib!
    }
    public static native byte[] encrypt(byte[] data);
}
```

The encryption key is in the native library → Ghidra analysis required!
