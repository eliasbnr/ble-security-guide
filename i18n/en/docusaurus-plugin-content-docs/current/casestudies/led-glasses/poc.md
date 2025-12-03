---
sidebar_position: 5
title: "Proof of Concept"
---

# LED Glasses - PoC

## Usage

```bash
python3 glasses_poc.py --text "HELLO" --mode scroll-left
```

## Key Components

```python
from Crypto.Cipher import AES

KEY = bytes.fromhex("34522a5b7a6e492c08090a9d8d2a23f8")

def encrypt(plaintext):
    transformed = column_major_transform(plaintext)
    cipher = AES.new(KEY, AES.MODE_ECB)
    encrypted = cipher.encrypt(transformed)
    return column_major_transform(encrypted)
```

See [Downloads](/docs/downloads/scripts) for complete PoC.
