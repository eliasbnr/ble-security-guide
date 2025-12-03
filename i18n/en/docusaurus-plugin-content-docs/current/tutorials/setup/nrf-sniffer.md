---
sidebar_position: 3
title: "nRF Sniffer Setup"
---

# nRF Sniffer Setup

The nRF Sniffer transforms your nRF52840 dongle into a **professional BLE sniffing tool** with Wireshark integration.

## Installation

### 1. Install nRF Util

```bash
# Download nRF Util (from https://www.nordicsemi.com/Products/Development-tools/nRF-Util)
# For Linux:
wget https://developer.nordicsemi.com/.pc-tools/nrfutil/x64-linux/nrfutil
chmod +x nrfutil
sudo mv nrfutil /usr/local/bin/

# Install sniffer command
nrfutil install ble-sniffer
nrfutil install device

# Check version
nrfutil --version
```

### 2. Flash Firmware

```bash
# Put dongle in bootloader mode
# (Hold reset button while plugging in - LED pulses red)

# List available devices
nrfutil device list

# Run bootstrap (shows firmware paths)
nrfutil ble-sniffer bootstrap

# The output shows firmware paths, e.g.:
# ~/.nrfutil/share/nrfutil-ble-sniffer/firmware/

# Flash dongle (serial number from device list)
nrfutil device program --firmware ~/.nrfutil/share/nrfutil-ble-sniffer/firmware/sniffer_nrf52840dongle_nrf52840_X.X.X.zip --serial-number <SERIAL>
```

### 3. Install Wireshark Plugin

```bash
# Bootstrap installs the extcap plugin for Wireshark
# IMPORTANT: Run with sudo/admin rights!
sudo nrfutil ble-sniffer bootstrap

# Alternative for local installation (without sudo):
nrfutil ble-sniffer bootstrap --extcap-dir ~/.local/lib/wireshark/extcap
```

## Wireshark Configuration

### Activate Sniffer Interface

1. **Open Wireshark**
2. **Capture → Refresh Interfaces** (F5)
3. **nRF Sniffer for Bluetooth LE** should appear
4. Enable **View → Interface Toolbars → nRF Sniffer for Bluetooth LE**

### Start Capture

1. Double-click on **nRF Sniffer for Bluetooth LE**
2. In toolbar: Select device or leave "All advertising"
3. Click green Start button

## Display Filters for BLE

### Basic Filters

```wireshark
# All BLE packets
btle

# Advertising only
btle.advertising_header

# ATT protocol (GATT)
btatt

# L2CAP
btl2cap
```

### ATT/GATT-specific Filters

```wireshark
# Write Requests
btatt.opcode == 0x12

# Write Commands (no response)
btatt.opcode == 0x52

# Read Requests
btatt.opcode == 0x0a

# Notifications
btatt.opcode == 0x1b
```

### Device Filters

```wireshark
# By MAC address
btle.advertising_address == aa:bb:cc:dd:ee:ff

# By device name
btcommon.eir_ad.entry.device_name contains "LED"
```

## Troubleshooting

### "Interface not found"

```bash
# Check if dongle is recognized
lsusb | grep Nordic

# Check serial port
ls /dev/ttyACM*

# Set permissions
sudo usermod -a -G dialout $USER
# -> Re-login required!
```

### "No packets captured"

1. Is the device in range (< 10m)?
2. Is the device sending advertising packets?
3. Toolbar: All advertising channels enabled (37, 38, 39)?

### Bootstrap Error

```bash
# Create extcap directory if missing
mkdir -p ~/.local/lib/wireshark/extcap

# Try again
nrfutil ble-sniffer bootstrap --extcap-dir ~/.local/lib/wireshark/extcap
```

---

:::tip Next Step
Continue with [blatann Setup](./blatann) for active BLE interaction.
:::
