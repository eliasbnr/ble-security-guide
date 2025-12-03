---
sidebar_position: 1
title: "Case Studies Overview"
---

# Case Studies

These case studies document real security analyses of BLE IoT devices. All analyses were performed on **own devices**.

## Summary

| Device | Vulnerability | CVSS | Impact |
|--------|---------------|------|--------|
| **LED Glasses** | Hardcoded AES Key | 9.8 Critical | Full device control |
| **LED Strips** | XOR with hardcoded key | 9.8 Critical | Any device controllable |
| **Smart Scale** | Weight in unencrypted advertising | 5.3 Medium | Privacy violation |

## Detailed Analyses

| Case Study | Description |
|------------|-------------|
| [🕶️ LED Glasses](./led-glasses/summary) | AES-128 with proprietary transformation |
| [💡 LED Strips](./led-strips/summary) | XOR-based protocol with counter |
| [⚖️ Smart Scale](./smart-scale/summary) | Privacy leak via Manufacturer Data |
