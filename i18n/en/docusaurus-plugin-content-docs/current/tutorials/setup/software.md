---
sidebar_position: 2
title: "Software Installation"
---

# Software Installation

## Base Installation

```bash
# System packages
sudo apt update
sudo apt install python3 python3-pip wireshark adb default-jdk

# Python packages
pip install blatann pycryptodome pyserial scapy
```

## Verify blatann

```python
# test_blatann.py
import blatann
from blatann import BleDevice

print("blatann successfully imported!")
print(f"BleDevice class: {BleDevice}")
```

## JADX

```bash
# Download from GitHub
wget https://github.com/skylot/jadx/releases/download/v1.5.0/jadx-1.5.0.zip
unzip jadx-1.5.0.zip -d jadx
./jadx/bin/jadx-gui
```

## Ghidra

```bash
# Download from NSA GitHub
wget https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_11.2.1_build/ghidra_11.2.1_PUBLIC_20241105.zip
unzip ghidra_*.zip
./ghidra_*/ghidraRun
```

## Verification

```bash
# Python
python3 --version  # >= 3.9

# blatann
python3 -c "from blatann import BleDevice; print('OK')"

# Wireshark
wireshark --version
```

---

:::tip Next Step
Continue with [nRF Sniffer Setup](./nrf-sniffer).
:::
