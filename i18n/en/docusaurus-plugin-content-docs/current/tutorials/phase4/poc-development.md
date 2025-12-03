---
sidebar_position: 1
title: "PoC Development"
---

# PoC Development

Create a Proof-of-Concept to validate vulnerabilities.

## PoC Structure

```python
#!/usr/bin/env python3
"""
PoC for [Vulnerability Name]
DISCLAIMER: Authorized testing only!
"""

from blatann import BleDevice

TARGET = "AA:BB:CC:DD:EE:FF"
SERVICE_UUID = "..."
CHAR_UUID = "..."
KEY = bytes.fromhex("...")

def exploit():
    # Connect
    # Send payload
    # Verify result
    pass

if __name__ == "__main__":
    exploit()
```

---

:::tip Next Step
Continue with [Replay Attacks](./replay-attacks).
:::
