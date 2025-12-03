---
sidebar_position: 1
title: "Prerequisites"
---

# Prerequisites

Before starting, make sure you have the necessary hardware and software.

## Hardware Requirements

| Component | Purpose | Price |
|-----------|---------|-------|
| **nRF52840 USB Dongle** | BLE Sniffing & Interaction | ~$10 |
| Linux System | Analysis Environment | - |
| BLE Test Device | Target for testing | varies |

### nRF52840 USB Dongle

**Sources:**
- [Mouser](https://www.mouser.com) (~$10)
- [DigiKey](https://www.digikey.com) (~$10)
- [Nordic Semiconductor](https://www.nordicsemi.com) (~$10)

## Software Requirements

### Required

| Software | Purpose | Installation |
|----------|---------|--------------|
| Python 3.9+ | PoC Development | `apt install python3` |
| Wireshark | Packet Analysis | `apt install wireshark` |
| JADX | APK Decompilation | GitHub Release |
| blatann | BLE Library | `pip install blatann` |

### Optional

| Software | Purpose | Installation |
|----------|---------|--------------|
| Ghidra | Native RE | NSA GitHub |
| Frida | Dynamic Analysis | `pip install frida-tools` |
| Android Studio | Emulation | Official Site |

## Knowledge Requirements

| Skill | Level | Notes |
|-------|-------|-------|
| Linux/Terminal | Required | Basic commands |
| Python | Required | Basic scripting |
| BLE | **Not required** | Covered in this guide |
| Reverse Engineering | Helpful | Basics taught here |

---

:::tip Next Step
Continue with [Methodology](./methodology).
:::
