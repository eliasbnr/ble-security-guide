---
sidebar_position: 4
title: "Proof of Concept"
---

# LED Strips - PoC

```python
XOR_KEY = bytes([89, 76, 90, 75, 53, 49, 33, 41, 62, 72, 64,
                 118, 100, 98, 81, 68, 94, 68, 63])

class LEDController:
    def power_on(self):
        cmd = bytes([0x7E, 0x04, 0x04, 0x01, 0x00, 0x01, 0xFF, 0x00, 0xEF])
        return self._encrypt(cmd)
```

See [Downloads](/docs/downloads/scripts) for complete PoC.
