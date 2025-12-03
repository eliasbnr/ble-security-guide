---
sidebar_position: 3
title: "Security Level Testing"
---

# Security Level Testing

Test which security levels the device requires.

## Security Levels

| Level | Description |
|-------|-------------|
| 1 | No Security |
| 2 | Unauthenticated Encryption |
| 3 | Authenticated Encryption |
| 4 | LE Secure Connections |

## Test with gatttool

```bash
gatttool --sec-level=low -b AA:BB:CC -I
> connect
> char-read-hnd 0x0012
```

---

:::tip Next Step
Continue with [Phase 3: APK Extraction](../phase3/apk-extraction).
:::
