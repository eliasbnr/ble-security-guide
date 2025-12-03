---
sidebar_position: 4
title: "Proof of Concept"
---

# LED Strips - PoC

## Minimaler PoC

```python
#!/usr/bin/env python3
"""LED Strips Control PoC"""

from blatann import BleDevice

XOR_KEY = bytes([89, 76, 90, 75, 53, 49, 33, 41, 62, 72, 64,
                 118, 100, 98, 81, 68, 94, 68, 63])

class LEDController:
    def __init__(self):
        self.counter = 0
    
    def _encrypt(self, data):
        key = XOR_KEY + bytes([self.counter])
        self.counter = (self.counter + 1) % 256
        
        result = bytearray(data)
        for i in range(1, min(len(result), 25)):
            for k in key:
                result[i] ^= k
        return bytes(result)
    
    def power_on(self):
        cmd = bytes([0x7E, 0x04, 0x04, 0x01, 0x00, 0x01, 0xFF, 0x00, 0xEF])
        return self._encrypt(cmd)
    
    def set_color(self, r, g, b):
        cmd = bytes([0x7E, 0x07, 0x05, 0x03, r, g, b, 0x10, 0xEF])
        return self._encrypt(cmd)

# Usage
ctrl = LEDController()
print(f"Power On: {ctrl.power_on().hex()}")
print(f"Red: {ctrl.set_color(255, 0, 0).hex()}")
```

## Vollständiger PoC

Siehe [Downloads](/docs/downloads/scripts) für `led_strips_poc.py`.
