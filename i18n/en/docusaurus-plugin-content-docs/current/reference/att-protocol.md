---
sidebar_position: 3
title: "ATT Protocol"
---

# ATT Protocol

The Attribute Protocol defines client-server communication.

## Opcodes

| Opcode | Name | Direction |
|--------|------|-----------|
| 0x0A | Read Request | C→S |
| 0x0B | Read Response | S→C |
| 0x12 | Write Request | C→S |
| 0x13 | Write Response | S→C |
| 0x52 | Write Command | C→S |
| 0x1B | Notification | S→C |
