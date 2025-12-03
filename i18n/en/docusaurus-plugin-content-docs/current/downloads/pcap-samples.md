---
sidebar_position: 3
title: "PCAP Samples"
---

# PCAP Samples

Example captures for training.

:::note Note
PCAP files may contain sensitive data. For this project, no actual PCAP files are published - create your own during analysis!
:::

## Recommended Captures

During your own analysis, create these captures:

| Capture | Content | Use |
|---------|---------|-----|
| `advertising_scan.pcapng` | Advertising packets | Phase 1 |
| `connection_setup.pcapng` | Connection setup | Protocol analysis |
| `gatt_discovery.pcapng` | Service discovery | GATT mapping |
| `app_commands.pcapng` | App commands to device | Command RE |

## Creating Captures

```bash
# With tshark (CLI)
tshark -i nRF_Sniffer -w my_capture.pcapng

# With Wireshark (GUI)
# 1. Select "nRF Sniffer for Bluetooth LE" interface
# 2. Click Start
# 3. Perform actions
# 4. Stop and save
```

## Analysis Tips

### Filtering

```
# ATT protocol only
btatt

# Writes only
btatt.opcode == 0x12

# Specific device
btle.advertising_address == aa:bb:cc:dd:ee:ff
```

---

:::tip Own Captures
The best PCAP files are the ones you create yourself! They contain exactly the data of your target device.
:::
