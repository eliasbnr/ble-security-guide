---
sidebar_position: 3
title: "ATT Protocol"
---

# ATT Protocol

Das Attribute Protocol (ATT) definiert die Client-Server-Kommunikation.

## Opcodes

| Opcode | Name | Richtung |
|--------|------|----------|
| 0x02 | MTU Request | C→S |
| 0x03 | MTU Response | S→C |
| 0x0A | Read Request | C→S |
| 0x0B | Read Response | S→C |
| 0x12 | Write Request | C→S |
| 0x13 | Write Response | S→C |
| 0x52 | Write Command | C→S |
| 0x1B | Notification | S→C |
| 0x1D | Indication | S→C |

## Paket-Format

```
| Opcode (1B) | Handle (2B) | Value (N B) |
```
