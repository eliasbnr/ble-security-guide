---
sidebar_position: 4
title: "Crypto Analysis"
---

# LED Glasses - Crypto Analysis

## Extracted Key

From Ghidra analysis of `libAES.so`:

```c
unsigned char aes_key[16] = {
    0x34, 0x52, 0x2a, 0x5b, 0x7a, 0x6e, 0x49, 0x2c,
    0x08, 0x09, 0x0a, 0x9d, 0x8d, 0x2a, 0x23, 0xf8
};
```

**Key (hex)**: `34522a5b7a6e492c08090a9d8d2a23f8`

## Column-Major Transformation

```python
def column_major_transform(data):
    result = bytearray(16)
    for i in range(16):
        row = i % 4
        col = i // 4
        result[col + row * 4] = data[i]
    return bytes(result)
```
