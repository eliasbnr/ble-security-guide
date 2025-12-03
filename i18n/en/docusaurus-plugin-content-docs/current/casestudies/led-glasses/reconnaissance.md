---
sidebar_position: 2
title: "Reconnaissance"
---

# LED Glasses - Reconnaissance

## GATT Structure

```
Service: 0xFFF0 (Custom)
├── Char: d44b...9600 (WRITE) - Commands
├── Char: d44b...960a (WRITE) - Data
└── Char: d44b...9601 (NOTIFY) - Status
```

## Security Testing

| Test | Result |
|------|--------|
| Connect without pairing | ✓ Success |
| Write at Level 1 | ✓ Success |
| Write at Level 2 | ✓ Success |

**Result**: No BLE-level authentication!
