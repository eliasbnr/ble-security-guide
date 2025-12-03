---
sidebar_position: 2
title: "Protocol"
---

# LED Strips - Protocol

## Packet Structure

```
┌──────┬────────┬─────────┬──────────┬──────┐
│ 0x7E │ Length │ Command │ Payload  │ 0xEF │
└──────┴────────┴─────────┴──────────┴──────┘
```

## Commands

| Command | Opcode | Description |
|---------|--------|-------------|
| Power | 0x04 | On (0x01) / Off (0x00) |
| Color | 0x05 | R,G,B values |
| Brightness | 0x01 | Level (0-100) |
