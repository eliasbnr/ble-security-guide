---
sidebar_position: 3
title: "Encryption"
---

# LED Strips - XOR "Encryption"

## Extracted Key

```java
byte[] key = {89, 76, 90, 75, 53, 49, 33, 41, 62, 72, 64,
              118, 100, 98, 81, 68, 94, 68, 63};
```

## Algorithm

```python
def encrypt(data, counter):
    full_key = XOR_KEY + bytes([counter])
    result = bytearray(data)
    for i in range(1, min(len(result), 25)):
        for k in full_key:
            result[i] ^= k
    return bytes(result)
```
